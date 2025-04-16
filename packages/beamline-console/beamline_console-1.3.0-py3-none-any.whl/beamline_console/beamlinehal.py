"""Beamline Hardware Abstraction Layer.

Extra software layer on top of the hardware middleware (e.g. TANGO)

Provides a few additional services:
    - access control (e.g. restrict users to move only selected motors)
    - device history (e.g. previous positions of a selected motor/device)
    - additional user limits, on top of Tango
    - collision detection
    - ...
"""

import collections
import os
import sys
import numpy as np

from collections import OrderedDict
from datetime import datetime
from xml.dom.minidom import parseString

import tango

from beamline_console.logger.logit import Logit
from beamline_console.devices.motordevice import MotorBasedDevice
from beamline_console.snapshot.beamsnapshot import BeamlineSnapshot
from beamline_console.snapshot.slot import Slot


# ----------------------------------------------------------------------
class BeamlineHAL(Logit):
    """
    """
    SOFTWARE_VERSION = "1.0"

    TIME_STAMP_FMT = "%Y-%m-%d %H:%M:%S"
  
    HISTORY_BUFFER_SIZE = 1000

    # ---------------------------------------------------------------------- 
    def __init__(self, parent, initial_user):
        """
        """
        Logit.__init__(self)

        self.settings = parent.settings
        self.device_map = OrderedDict()     # (dev_name, dev_handle)
        self.slots_map = OrderedDict()     # (slot_name, slot_handle)

        devices_file = os.path.join(os.path.join(os.path.expanduser('~'), '.beamline_console'), "devices.xml")
        self.load_file(devices_file, self.device_map, "device", MotorBasedDevice)

        slots_file = os.path.join(os.path.join(os.path.expanduser('~'), '.beamline_console'), "slots.xml")
        self.load_file(slots_file, self.slots_map, "slot", Slot)

        self.access_level = initial_user

        # use ring buffer TODO
        # memorize positions of devices and motors
        self.history = []       # (dev_name, motor_name, current_pos, target_pos)

        self._timeout = 0
    
    # ----------------------------------------------------------------------
    def __del__(self):
        """ 
        """
        self.group_action("stop_motors")
        self.logger.debug("BeamlineHAL object released successfully!")

    # ----------------------------------------------------------------------
    def access_level_changed(self, access_level):
        self.logger.info(f"Access level changed to {access_level}")
        self.access_level = access_level
        for device in self.device_map:
            if hasattr(device, "access_level_changed"):
                device.access_level_changed(access_level)

    # ----------------------------------------------------------------------
    def progress(self):
        progress = []
        for device in self.device_map.values():
            device_progress = device.progress()
            if device_progress:
                progress.append(device_progress)

        if progress:
            return min(progress)*100
        else:
            return 0

    # ----------------------------------------------------------------------
    def device(self, name):
        """
        Args:
            name (str)
        Returns:
            handle to a given device.
        """
        if name in self.device_map:
            return self.device_map[name]

        if name in self.slots_map:
            return self.slots_map[name]

        raise RuntimeError(f"BeamlineHal: Device {name} not found")
    
    # ---------------------------------------------------------------------- 
    def group_action(self, func_name):
        """Calls function for all controlled devices
        """
        self.logger.info(f"Group action {func_name} requested")

        for device_handle in list(self.device_map.values()):
            try:
                getattr(device_handle, func_name)()
      
            except AttributeError as err:
                if func_name != 'safe_close':
                    self.logger.error(f"No {func_name} function available {str(err)}", exc_info=sys.exc_info())
                else:
                    self.logger.debug(f"No {func_name} function available {str(err)}")
 
    # ----------------------------------------------------------------------
    def get_motor_handle(self, motor_name):
        device_name, motor_name = str(motor_name).split("/")

        device_handle = self.device_map[device_name]
        if isinstance(device_handle, MotorBasedDevice):
            motor_handle = device_handle.motor(motor_name)
            if not motor_handle:
                raise RuntimeError(f"Invalid motor name ({device_name}/{motor_name})")
        else:
            raise RuntimeError(f'MotorBasedDevice object expected (given {device_name})')

        return motor_handle

    # ----------------------------------------------------------------------
    def move_motor(self, motor_name, value, scale="absolute", mode="async"):
        """
        Args:
            motor_name (str): name of motor including device (e.g. "manipulator/x")
            value (float): "target position" or "delta" (depending on "scale")
            scale (str): "relative" or "absolute"
            mode (str): "sync" or "async" or 'snapshot'

            Examples:
                hal.move_motor("manipulator/x", 20.2, "absolute")
                hal.move_motor("manipulator/y", 0.2, "relative", "sync")
        """

        motor_handle = self.get_motor_handle(motor_name)
        current_pos = motor_handle.position()

        if scale.lower() == "relative":
            target_pos = current_pos + value
        elif scale.lower() == "absolute":
            target_pos = value
        else:
            raise RuntimeError(f"Invalid scale {scale}")

        if not motor_handle.access_guaranteed():
            raise RuntimeError(f"Current user is not allowed to move {motor_name}")

        # memorize move
        timestamp = datetime.now().strftime(self.TIME_STAMP_FMT)
        self.history.append((motor_name, current_pos, target_pos, timestamp))
        self.logger.info(f"Moving {motor_name} from "
                         f"{current_pos:.{motor_handle.decimals}f} to {target_pos:.{motor_handle.decimals}f}")

        motor_handle.move_absolute(target_pos, mode)

    # ----------------------------------------------------------------------
    def stop_motor(self, motor_name):
        self.get_motor_handle(motor_name).stop()

    # ----------------------------------------------------------------------
    def move_motor_eta(self, motor_name, value, scale):
        """
        Returns:
            (int) estimated time of mv command completion in seconds
        """
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def move_snapshot(self, filename, mode="sync"):
        """Move beamline's motors to a given state.

        NOTE that movement is performed in a separate thread (special
        treatment of exceptions comming from the thread is needed).
        """
        snapshot = BeamlineSnapshot(self, filename)

        snapshot.validate()   # in case of error RuntimeError is thrown
        snapshot.start()
    
        if mode != "async":      # ??? TODO otherwise don't wait?
            snapshot.join()
  
            exc_type, exc_value = snapshot.last_exception()
            if exc_type:
                raise RuntimeError(f"Beamline snapshot exception, {exc_type}, {exc_value}")

    # ----------------------------------------------------------------------
    def move_group(self, move_group):
        """Move group of motors in async mode.

        e.g. tuple
            (device_name, motor_name, target_position) -> take into account sync/async! TODO
        """
        for move_tuple in move_group:
            dev_name, motor_name, position = move_tuple[:3]
            full_name = f"{dev_name}/{motor_name}"

            try: 
                self.move_motor(full_name, position, "absolute", "async")

            except (RuntimeError, tango.DevFailed) as err:
                self.stop_all()
                raise               # propagate the exception somehow nicer...
  
    # ----------------------------------------------------------------------
    def stop_all(self):
        """Stop all moving motors.
        """
        self.group_action("stop_motors")

    # ----------------------------------------------------------------------
    def safe_close(self):
        """Stop all moving motors.
        """
        self.group_action("safe_close")

    # ----------------------------------------------------------------------
    def load_file(self, file_name: str, entry_dict: OrderedDict, elements_name: str, base_class) -> None:
        """
        """
        self.logger.info(f"Loading file {file_name}")
  
        with open(file_name) as dev_file:
            dom = parseString(dev_file.read())
        root_elements = dom.getElementsByTagName("beamline_settings")
        if len(root_elements) > 0:
            root_element = root_elements[0]
            self._validate_compatibility(root_element)
    
            # clean-up first (important when Beamline object is reloaded)
            entry_dict.clear()

            entry_list = root_element.getElementsByTagName(elements_name)

            for entry in entry_list:
                entry_name = entry.getAttribute("name")            # alias

                if entry_name in (list(self.device_map.keys()) + list(self.slots_map.keys())):
                    raise RuntimeError(f'Non-unique name found: {entry_name}')

                try:
                    obj = base_class(entry_name, self)
                    obj.from_xml(entry)
                    status = obj.initialize()
                    if status:
                        entry_dict[entry_name] = obj
                    else:
                        self.logger.error(f'Cannot make {entry_name}')

                except Exception as ex:
                    self.logger.error(f'Cannot make {entry_name}', exc_info=sys.exc_info())
                    raise ex
        else:
            raise RuntimeError('No root node "beamline_settings" found!')

    # ----------------------------------------------------------------------
    def _validate_compatibility(self, xml_node):
        """
        """
        software_version = xml_node.getAttribute("version")

        if software_version != self.SOFTWARE_VERSION:
            self.logger.warning(f"Probable software incompatibility! ({software_version} vs. {self.SOFTWARE_VERSION})")

    # ----------------------------------------------------------------------
    def motor_state(self, motor_name):
        """
        Args:
            (str) absolute motor name (e.g. manipulator/x)
        Returns:
            (str) representing state of a given motor (e.g. "on", "moving")
        """
        device_name, motor_name = motor_name.split("/")

        device_handle = self.device_map[device_name]
        if not isinstance(device_handle, MotorBasedDevice):
            raise RuntimeError(f"MotorBasedDevice object expected ({device_name})")

        motor_handle = device_handle.motor(motor_name)
        if not motor_handle:
            raise RuntimeError(f'Invalid motor name "{motor_name}"')

        return motor_handle.state()

    # ---------------------------------------------------------------------- 
    def motor_position(self, motor_name):
        """
        Example usage:
            beamlineHal.motor_position("manipulator/x")
    
        Returns:
            (float) position of a given motor.
        """
        try:
            device_name, motor_name = motor_name.split("/")

        except ValueError:
            raise RuntimeError(f"Invalid motor name '{motor_name}'!")

        device_handle = self.device_map[device_name]
        if isinstance(device_handle, MotorBasedDevice):

                # get handle to the motor identified by the name
            motor_handle = device_handle.motor(motor_name)
            if not motor_handle:
                raise RuntimeError('Invalid motor name "{}/{}"'.format(device_name,
                                                                       motor_name))

            return np.round(motor_handle.position(), decimals = motor_handle.decimals)

        else:
            raise RuntimeError(f'MotorBasedDevice object expected (device name: "{device_name}")')

    # ----------------------------------------------------------------------
    def list_motors(self):
        """
        Returns:
            [str] complete list of motor names
        """
        motor_list = []

        for dev_name, device in list(self.device_map.items()):
            if isinstance(device, MotorBasedDevice):
                motor_list += [f"{dev_name}/{name}"
                               for name in device.list_motors()]
    
        return motor_list

    # ----------------------------------------------------------------------
    def is_any_moving(self):
        """
        Returns:
            (bool) True if any of constituent motors is currently moving
        """
        return any([handle.state() == "moving" for handle in list(self.device_map.values()) if
                    isinstance(handle, MotorBasedDevice)])

    # ----------------------------------------------------------------------
    def is_move_valid(self, motor_name, position):
        """Check if given motor can be moved to requested target position.
        Args:
            motor_name (str)
            position (float)
        """
        dev_name, motor_name = motor_name.split("/")

        dev_handle = self.device_map[dev_name]
        if not isinstance(dev_handle, MotorBasedDevice):
            return False, f"MotorBasedDevice object expected ({dev_name})"

        motor_handle = dev_handle.motor(motor_name)
        if not motor_handle:
            return False, f"invalid motor name {motor_name}"

        # check access and limits
        return motor_handle.is_move_valid(position)
