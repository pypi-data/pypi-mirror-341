"""Base class for all motor based devices
"""

import logging

from beamline_console.constants import APP_NAME

from beamline_console.devices.tangomotor import TangoMotor
from beamline_console.devices.dummymotor import DummyMotor

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class MotorBasedDevice:
    """
    """

    # ----------------------------------------------------------------------
    def __init__(self, device_name, beamline_hal):
        """
        """
        self.name = device_name

        self._history = {}
        self.motors = {}
        self.widget_position = None

        self.beamline_hal = beamline_hal

        logger.debug(f"Instantiating device object {device_name}")

    # ----------------------------------------------------------------------
    def motor(self, motor_name):
        """
        Returns:
            motor handle
        """
        if motor_name in self.motors:
            return self.motors[motor_name]

        return None

    # ----------------------------------------------------------------------
    def progress(self):
        progress = []
        for m in list(self.motors.values()):
            if m.state() == "moving":
                progress.append(m.progress())
        if len(progress):
            return min(progress)
        else:
            return None

    # ----------------------------------------------------------------------
    def state(self):
        """
        """
        if any([m.state() == "moving" for m in list(self.motors.values())]):
            return "moving"
        
        if all([m.state() == "idle" for m in list(self.motors.values())]):
            return "ready"          # or "idle"
        
        if any([m.state() == "fault" for m in list(self.motors.values())]):
            return "fault"
        
        return "unknown"
        #return "ready"

    # ----------------------------------------------------------------------
    def move(self, motor_name, target_position, mode="async"):
        """Move given motor to the target position.
        """
        motor = self.motor(motor_name)
        if motor:
            motor.move_absolute(target_position, mode)
        else:
            raise RuntimeError(f"Invalid motor name {motor_name}")

    # ----------------------------------------------------------------------
    def stop_motors(self):
        """Stop all motors.
        """
        logger.info(f"Stopping device {self.name}")
        for motor in list(self.motors.values()):
            motor.stop()

    # ----------------------------------------------------------------------
    def initialize(self):
        """
        """
        status = True

        for motor in list(self.motors.values()):
            status = status*motor.initialize()

        return status

    # ----------------------------------------------------------------------
    def access_level_changed(self, access_level):
        for motor in list(self.motors.values()):
            motor.access_level_changed(access_level)

    # ----------------------------------------------------------------------
    def from_xml(self, xml_node):
        """Load device's configuration from a given XML node.
        """
        general_access = xml_node.getAttribute('access')
        if not general_access:
            general_access = "user"

        if len(xml_node.getElementsByTagName("widget")) > 0:
            widget = xml_node.getElementsByTagName("widget")[0]
            self.widget_position = [int(widget.getAttribute("x")), int(widget.getAttribute("y")),
                                    int(widget.getAttribute("width")), int(widget.getAttribute("height"))]

        for motor_node in xml_node.getElementsByTagName("motor"):
            name = str(motor_node.getAttribute("name"))
            if name in self.motors:
                raise RuntimeError(f'Duplication of motors name {name} in {self.name}')
            motor = self._make_motor(motor_node, general_access)
            if motor:
                self.motors[name] = motor

    # ----------------------------------------------------------------------
    def _make_motor(self, motor_node, general_access):
        """Factory method
        """

        motor_type = motor_node.getAttribute("type")
        if  motor_type== "tango":
            motor = TangoMotor()
            motor.tango_server = str(motor_node.getAttribute("tango_server"))
            motor.updated_properties(motor_node)

        elif motor_type == "dummy":
            motor = DummyMotor()
        else:
            raise ValueError(f"Invalid motor type {motor_type}")

        access = motor_node.getAttribute('access')
        motor.set_access(access if access else general_access)

        motor.name = str(motor_node.getAttribute("name"))

        try:
            motor.user_low_limit = float(motor_node.getAttribute("low_limit_user"))
            motor.user_high_limit = float(motor_node.getAttribute("high_limit_user"))

        except ValueError:
            print(f"(motordevice.py) no user limits for motor {motor.name} defined")

        print(f"(motordevice.py) loaded motor {motor.name}")
    
        return motor

    # ----------------------------------------------------------------------
    def list_motors(self):
        """
        Returns:
            [str] list of motor names
        """
        return list(self.motors.keys())