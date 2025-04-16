# yury.matveev@desy.de

"""Simple abstraction on top of the TANGO based stepping motor.

Example usage:
    m = TangoMotor("p09/motor/exp.01")
    m.initialize()

    m.move_absolute(22.1)
    print("Current position:", m.position())

    m.move_relative(-4.5, "async")
"""

import tango
from beamline_console.devices.abstractmotor import AbstractMotor

# ---------------------------------------------------------------------- 
class TangoMotor(AbstractMotor):
    """ 
    """
   
    # ---------------------------------------------------------------------- 
    def __init__(self, server_name="", name="empty"):
        """
        Args:
            (str) TANGO server's name
            (str) user friendly motor's alias
        """
        super().__init__(name)
    
        self.tango_server = str(server_name)
        self.device_proxy = None

    # ----------------------------------------------------------------------
    def state(self):
        """
        Returns:
            (str) current state of the motor as a string
        """
        return str(self.device_proxy.state()).lower()

    # ----------------------------------------------------------------------
    def progress(self):
        """
        Returns:
            (int) current moving progress in range 0-1
        """
        if self.device_proxy.totalmovetime != 0:
            return min(max(1 - self.device_proxy.remainingtime/self.device_proxy.totalmovetime, 0), 1)

        return 0

    # ----------------------------------------------------------------------
    def position(self):
        """
        Returns:
            (float) current position of the motor
        """
        return self.parameter("position")

    # ----------------------------------------------------------------------
    def move_to_high_limit(self):
        if self.device_proxy.conversion > 0:
            self.device_proxy.movetocwlimit()
        else:
            self.device_proxy.movetoccwlimit()

    # ----------------------------------------------------------------------
    def move_to_low_limit(self):
        if self.device_proxy.conversion > 0:
            self.device_proxy.movetoccwlimit()
        else:
            self.device_proxy.movetocwlimit()

    # ----------------------------------------------------------------------
    def check_limits(self):
        """
        Returns:
            (str) 'high', 'low' or ''
                   if conversion positive, then cwlimit - high, ccwlimit - low and vise versa
         """

        try:
            status = []

            if self.device_proxy.get_property_list("IgnoreLimitSw") and \
                    bool(self.device_proxy.get_property("IgnoreLimitSw")['IgnoreLimitSw'][0]):
                return status

            if self.device_proxy.cwlimit:
                if self.device_proxy.conversion > 0:
                    status.append('high')
                else:
                    status.append('low')

            if self.device_proxy.ccwlimit:
                if self.device_proxy.conversion > 0:
                    status.append('low')
                else:
                    status.append('high')

            return status

        except AttributeError:
            return status

    # ----------------------------------------------------------------------
    def stop(self):
        """Stops the motor, if in the moving state.
        """
        if self.state().lower() == "moving":
            self.device_proxy.stopMove()

    # ----------------------------------------------------------------------
    def calibrate(self, actual_pos):
        """
        Returns:
            actual_pos (float), actual motor's position
        """
        self.device_proxy.command_inout("calibrate", actual_pos)

    # ---------------------------------------------------------------------- 
    def initialize(self):
        """Tango device proxy initialization.
        """
        self.device_proxy = tango.DeviceProxy(self.tango_server)

        elapsed = self.device_proxy.ping()
        print(f"(tangomotor.py) ping {self.tango_server} ({elapsed} us)")

        return True

    # ----------------------------------------------------------------------
    def is_move_valid(self, target_pos):
        """Checks if given target position is within limits.

        Args:
            target_pos (float)
        """
        is_valid, msg = super().is_move_valid(target_pos)
        if not is_valid:
            return False, msg

        else:
            low_limit = self.parameter("UnitLimitMin")        # Tango limits
            high_limit = self.parameter("UnitLimitMax")

            if (target_pos < low_limit or
                target_pos > high_limit):
        
                return False, f"Motor ({self}) target position ({target_pos:.2f}) is "\
                              f"out of range ({low_limit:.2f}, {high_limit:.2f})"

        return True, ""

    # ---------------------------------------------------------------------- 
    def _move_absolute_async(self, target_pos):
        """Asynchronous version of the "move absolute" command. 

        Args:
            target_pos (float)
        """
        is_valid, msg = self.is_move_valid(target_pos)

        if is_valid:
            self.device_proxy.position = target_pos
        else:
            raise ValueError(msg)

    # ----------------------------------------------------------------------
    def status(self):
        """
        Returns:
            (str) status information, e.g. "motor is moving", "idle"
        """
        return str(self.device_proxy.status()).lower()

    # ----------------------------------------------------------------------
    def parameter(self, param_name):
        """
        Returns:
            value of selected motor's parameter (from Tango database).
        """
        return self.device_proxy.read_attribute(param_name).value

    # ----------------------------------------------------------------------
    def set_attribute(self, attribute, value):

        try:
            self.device_proxy.write_attribute(attribute, float(value))
            return True
        except ValueError:
            self.device_proxy.write_attribute(attribute, value)
            return True
        except Exception:
            return False

    # ----------------------------------------------------------------------
    def set_parameter(self, param_name, param_value):
        """Save value of selected motor's property (from Tango database).
        """    
        self.device_proxy.write_attribute(param_name, param_value)

    # ----------------------------------------------------------------------
    def load_xml(self, xml_node):
        """
        """
    # ----------------------------------------------------------------------
    def get_low_limit(self):
        return float(self.parameter("UnitLimitMin"))

    # ----------------------------------------------------------------------
    def get_high_limit(self):
        return float(self.parameter("UnitLimitMax"))