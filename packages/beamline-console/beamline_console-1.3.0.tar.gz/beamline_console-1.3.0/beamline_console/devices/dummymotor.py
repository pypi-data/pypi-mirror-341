# yury.matveev@desy.de

"""Dummy motor implementation, used for the test purposes mainly.
"""

from beamline_console.devices.abstractmotor import AbstractMotor


# ----------------------------------------------------------------------
class DummyMotor(AbstractMotor):
    """Dummy motor used for tests mainly.
    """

    # ---------------------------------------------------------------------- 
    def __init__(self, name="noname"):
        """
        Args:
            (str) user friendly motor's alias
        """
        super().__init__(name)

        self._position = 0.0

        self._min_position = -100.0
        self._max_position = 100.0
        self.decimals = 2

        self.tango_server = "dummy.server"
        self.device_proxy = None

    # ----------------------------------------------------------------------
    def state(self):
        """
        Returns:
            (str) current "state" of the Motor, e.g. "on", "moving", "unknown"
        """
        return "on"

    # ----------------------------------------------------------------------
    def position(self):
        """
        """
        return self._position

    # ---------------------------------------------------------------------- 
    def calibrate(self, actual_pos):
        """Calibrate this motor.
        """
        self._position = actual_pos

    # ----------------------------------------------------------------------
    def is_move_valid(self, target_pos):
        """
        """
        # check user defined limits first
        is_valid, msg = super().is_move_valid(target_pos)
        if not is_valid:
            return False, msg

        if target_pos < self._min_position or target_pos > self._max_position:
            return False, "(%s) Target position (%.2f) is out of range (%.2f, %.2f)" % \
                   (str(self), target_pos, self._min_position, self._max_position)

        return True, ""

    # ---------------------------------------------------------------------- 
    def _move_absolute_async(self, target_pos):
        """
        """
        is_valid, msg = self.is_move_valid(target_pos)

        if is_valid:
            self._position = target_pos
        else:
            raise ValueError(msg)

    # ----------------------------------------------------------------------
    def parameter(self, param_name):
        """
        """
        param_name = param_name.lower()

        if param_name == "position":
            return self._position
        elif param_name == "unitlimitmin":
            return self._min_position
        elif param_name == "unitlimitmax":
            return self._max_position

        return 0.0

    #        raise ValueError("Parameter {} not available".format(param_name))

    # ----------------------------------------------------------------------
    def __repr__(self):
        """
        """
        return self.name

    # ----------------------------------------------------------------------
    def check_limits(self):
        return []

    # ----------------------------------------------------------------------
    def get_low_limit(self):
        return self._min_position

    # ----------------------------------------------------------------------
    def get_high_limit(self):
        return self._max_position

    # ----------------------------------------------------------------------
    def stop(self):
        pass
