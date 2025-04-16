# yury.matveev@desy.de

"""Base class for other motor types.
"""

import time
import json


# ---------------------------------------------------------------------- 
class AbstractMotor:
    """
    """

    # ---------------------------------------------------------------------- 
    def __init__(self, name="noname"):
        """
        Args:
            (str) motor's alias
        """
        self.name = name

        # extra software limits (on top of Tango)
        self.user_low_limit = None
        self.user_high_limit = None
        self.decimals = 3
        self._target_pos = 0
        self._access = "user"
        self._is_allowed = True

        self.new_position_when_moving_is_allowed = True

    # ----------------------------------------------------------------------
    def access_level_changed(self, superuser_mode):
        if self._access == "superuser":
            self._is_allowed = superuser_mode

    # ----------------------------------------------------------------------
    def access_guaranteed(self):
        return self._is_allowed

    # ----------------------------------------------------------------------
    def set_access(self, access):
        self._access = access

    # ----------------------------------------------------------------------
    def state(self):
        """
        Returns:
            (str) current state of the motor, e.g.: "on", "moving"
        """
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def progress(self):
        """
        Returns:
            (int) current moving progress in range 0-1
        """
        raise NotImplementedError("Not implemented")


    # ----------------------------------------------------------------------
    def position(self):
        """
        Returns:
            (float) current position of the motor
        """
        raise NotImplementedError("Not implemented")

    # ---------------------------------------------------------------------- 
    def stop(self):
        """Stops the motor.
        """
        raise NotImplementedError("Not implemented")

    # ---------------------------------------------------------------------- 
    def calibrate(self, actual_pos):
        """Calibrates the motor (actual_pos should be given in units specific
        to the motor).
        """
        raise NotImplementedError("Not implemented")

    # ---------------------------------------------------------------------- 
    def initialize(self):
        """Optional extra initialization.
        """
        return True

    # ----------------------------------------------------------------------
    def move_absolute(self, target_pos, mode="sync"):
        """Moves motor to a given target position. 
        NOTE that the motor will not move if it's in the "moving" state already.
      
        Depending on the "mode" parameter the function will run in either
        synchronous or asynchronous mode.

        Args:
            target_pos (float)
            mode (str): sync, async
        """
        state = self.state()
        if state == "on":
            self._target_pos = target_pos
            if mode.lower() == "sync":
                self._move_absolute_sync(target_pos)
            elif mode.lower() in ["async", 'snapshot']:
                self._move_absolute_async(target_pos)
            else:
                raise RuntimeError(f"Invalid mode '{mode}'")

        elif state == "moving":  # stop and move?
            if self._target_pos != target_pos:
                self.stop()
                self.move_absolute(target_pos, mode)

        else:
            raise RuntimeError("Cannot move motor if it's in '{}'"
                               "state".format(state))

    # ---------------------------------------------------------------------- 
    def move_relative(self, delta, mode="sync"):
        """Moves the motor by a given delta.

        Args:
            delta (float)
            mode (str): sync, asyns
        """
        self.move_absolute(self.position() + delta, mode)

    # ----------------------------------------------------------------------
    def is_move_valid(self, target_pos):
        """Checks if the given target position is within limits.

        Args:
            target_pos (float)
        """
        if not self._is_allowed:
            return False, f"Current user is not allowed to move {self}"

        if self.user_low_limit and target_pos < self.user_low_limit:
            return False, \
                f"motor ({self}), target position ({target_pos:.2f}) below user low limit ({self.user_low_limit:.2f})"

        if self.user_high_limit and target_pos > self.user_high_limit:
            return False, \
                f"motor ({self}), target position ({target_pos:.2f}) below above low limit ({self.user_high_limit:.2f})"

        if not self.new_position_when_moving_is_allowed and self.state() == "moving":
                return False, "motor is moving and new position is not allowed"

        return True, ""

    # ----------------------------------------------------------------------
    def _move_absolute_sync(self, target_pos):
        """Synchronous version of the "move absolute" command.

        Args:
            target_pos (float)
        """
        self._move_absolute_async(target_pos)

        # wait a little bit when the motor is moving
        RATE_SEC = 0.5
        while self.state() == "moving":
            time.sleep(RATE_SEC)

    # ----------------------------------------------------------------------
    def _move_absolute_async(self, target_pos):
        """Asynchronous version of the "move absolute" command
        (control is returned immediately).
    
        Workhorse for other kinds of "move" commands (to be reimplemented in
        derived classes).

        Args:
            target_pos (float)
        """

    # ----------------------------------------------------------------------
    def move_to_high_limit(self):
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def move_to_low_limit(self):
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def parameter(self, param_name):
        """
        Returns:
            (float) value of the motor's parameter (delegates request to the
            Tango database typically).
        """
        return 0.0
    
    # ----------------------------------------------------------------------
    def updated_properties(self, node):

        for attribute in list(node._attrs.keys()):
            if (attribute != 'name') and (attribute != 'tango_server'):
                if not hasattr(self, attribute):
                    self.attribute = lambda: None
                try:
                    value = json.loads(node.getAttribute(attribute).lower())
                except:
                    value = node.getAttribute(attribute)
                finally:
                    setattr(self, attribute, value)

    # ----------------------------------------------------------------------
    def set_parameter(self, param_name, param_value):
        """
        """
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def get_low_limit(self):
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def get_high_limit(self):
        raise NotImplementedError("Not implemented")

    # ----------------------------------------------------------------------
    def __repr__(self):
        """
        """
        return self.name
