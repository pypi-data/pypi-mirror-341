# yury.matveev@desy.de

"""
Widget representing single motor.
"""

import logging
import sys
import time
import threading

from queue import Queue, Empty

from PyQt5 import QtWidgets, QtCore

from beamline_console.constants import APP_NAME
from beamline_console.devicecontrol.motorpropsdialog import MotorPropsDialog
from beamline_console.utils.input_dialog import InputDialog

from beamline_console.gui.MotorItemWidget_ui import Ui_MotorItemWidget

logger = logging.getLogger(APP_NAME)

CONTINUOUS_MOVE_DELAY = 0.5
CONTINUOUS_MOVE_REFRESH = 0.1


# ----------------------------------------------------------------------
class MotorItemWidget(QtWidgets.QWidget):
    """
    """

    # ----------------------------------------------------------------------
    def __init__(self, beamline_hal, device_handle, motor_handle, parent=None):
        super().__init__()

        self._beamline_hal = beamline_hal
        self._device_handle = device_handle
        self._motor_handle = motor_handle

        self._ui = Ui_MotorItemWidget()
        self._ui.setupUi(self)

        self._access_level = "user"

        self._ui.lb_name.setText(self.absolute_motor_name())
        if hasattr(self._motor_handle, "tango_server"):
            self._ui.lb_name.setToolTip(f"{self._motor_handle.tango_server}")

        self._ui.lb_name.double_clicked.connect(self._show_properties)

        self._ui.but_move_up.pressed.connect(lambda: self._move_pressed("up"))
        self._ui.but_move_up.released.connect(self._move_released)
        self._ui.but_move_up.grabGesture(QtCore.Qt.TapAndHoldGesture)
        self._ui.but_move_up.installEventFilter(EventFilter())

        self._ui.but_move_down.pressed.connect(lambda: self._move_pressed("down"))
        self._ui.but_move_down.released.connect(self._move_released)
        self._ui.but_move_down.grabGesture(QtCore.Qt.TapAndHoldGesture)
        self._ui.but_move_down.installEventFilter(EventFilter())

        self._ui.but_increase_step.clicked.connect(lambda: self._change_step("increase"))
        self._ui.but_decrease_step.clicked.connect(lambda: self._change_step("decrease"))
        self._ui.lb_pos.double_clicked.connect(self._move_motor_to)

        self._stop_continuous_move = threading.Event()
        self._moving_continuous = threading.Event()
        self._ignore_click = threading.Event()
        self._movement_worker = None
        self._last_clicks = Queue()

        self._move_tick = 0

        self._target_pos = 0

        self.refresh_gui()

    # ----------------------------------------------------------------------
    def access_level_changed(self, access_level):
        """
        """
        self._access_level = access_level

    # ----------------------------------------------------------------------
    def sync_pos(self, scale, mode="sync"):
        """
        Set "new position" QLineEdit to "current" QLineEdit.
        """
        DELAY = 0.2  # <<< TODO

        if mode.lower() == "sync":
            while self._motor_handle.state() == "moving":
                time.sleep(DELAY)

        if scale == "absolute":
            position = self._motor_handle.position()
        else:
            position = 0

        self._ui.lb_pos.setText(f"{position:.{self._motor_handle.decimals}f}")
        self._target_pos = position

    # ----------------------------------------------------------------------
    def _move_motor_to(self):
        """Move motor associated with the item
        """

        try:
            motor_name = self.absolute_motor_name()
            dlg = InputDialog(mode="position", motor_handle=self._motor_handle)
            if dlg.exec_():
                target_pos = dlg.new_position
                is_valid, status = self._motor_handle.is_move_valid(target_pos)

                if is_valid:
                    self._target_pos = target_pos
                    self._beamline_hal.move_motor(motor_name, target_pos, "absolute", "async")
                else:
                    logger.error(status)

        except Exception as err:
            logger.error(err, exc_info=sys.exc_info())
            raise

    # ----------------------------------------------------------------------
    def _change_step(self, direction):

        current_step = self._ui.sb_step.value()

        if direction == "increase":
            self._ui.sb_step.setValue(current_step*2)
        else:
            self._ui.sb_step.setValue(current_step/2)

    # ----------------------------------------------------------------------
    def _move_pressed(self, direction):
        self._stop_continuous_move.clear()
        self._moving_continuous.set()
        print("Put")
        self._last_clicks.put(1)

        if self._movement_worker is None or not self._movement_worker.is_alive():
            self._movement_worker = threading.Thread(target=self._do_move, args=[direction], daemon=True)
            self._movement_worker.start()

    # ----------------------------------------------------------------------
    def _move_released(self):
        self._stop_continuous_move.set()
        try:
            print("Get")
            self._last_clicks.get(block=False)
        except Empty:
            pass

    # ----------------------------------------------------------------------
    def _do_move(self, direction):
        time.sleep(CONTINUOUS_MOVE_DELAY)
        try:
            self._last_clicks.get(block=False)
            print("Got")
        except Empty:
            delta = abs(self._ui.sb_step.value())
            if direction == "down":
                delta *= -1
            try:
                position = self._motor_handle.position()
                self._target_pos = position + delta
                self._beamline_hal.move_motor(self.absolute_motor_name(), self._target_pos, "absolute")

            except Exception as err:
                logger.error(err, exc_info=sys.exc_info())
        else:
            if not self._stop_continuous_move.is_set():
                self._ignore_click.set()
                logger.info(f"Start continuous move, direction {direction}")
                try:
                    if direction == "up":
                        self._motor_handle.move_to_high_limit()
                    else:
                        self._motor_handle.move_to_low_limit()
                except Exception as err:
                    logger.error(f'Cannot move to limit: {repr(err)}')

                while not self._stop_continuous_move.is_set():
                    time.sleep(CONTINUOUS_MOVE_REFRESH)

                logger.info(f"Stop continuous move")
                self._motor_handle.stop()
                self._target_pos = self._motor_handle.position()

            self._moving_continuous.clear()

    # ----------------------------------------------------------------------
    def refresh_gui(self):
        """Called periodically by the DeviceWidget.
        """

        try:
            decimals = self._motor_handle.decimals
            position = self._motor_handle.position()
            self._ui.lb_pos.setText(f"{position:.{decimals}f}")

            motor_state, limits_state = self.get_status()
            self._colorize_diodes(motor_state, limits_state)

            self._ui.le_low_limit.setText(f"{self._motor_handle.get_low_limit():.{decimals}f}")
            self._ui.le_high_limit.setText(f"{self._motor_handle.get_high_limit():.{decimals}f}")

            low_lim = self._motor_handle.get_low_limit()
            slider_range = self._motor_handle.get_high_limit() - low_lim
            self._ui.sl_position.setMaximum(slider_range)
            self._ui.sl_position.setSingleStep(slider_range/100)

            if not self._moving_continuous.is_set():
                self._ui.but_move_up.setEnabled(motor_state != "moving")
                self._ui.but_move_down.setEnabled(motor_state != "moving")

            if self._target_pos < position:
                self._ui.sl_position.setLow(self._target_pos-low_lim)
                self._ui.sl_position.setHigh(position-low_lim)
            else:
                self._ui.sl_position.setLow(position-low_lim)
                self._ui.sl_position.setHigh(self._target_pos-low_lim)

            self._ui.sb_step.setDecimals(decimals)

        except Exception:  # PyTango.DevFailed:
            self._colorize_diodes("fault", '')

    # ----------------------------------------------------------------------
    def get_status(self):

        return self._motor_handle.state(), self._motor_handle.check_limits()

    # ----------------------------------------------------------------------
    def _colorize_diodes(self, motor_state, limits_state):
        """Update the "diodes" signaling associated motor's state and update status label
        """
        error_style = "QToolButton {background-color: rgb(242, 101, 101);}"

        lim_green_style = "QToolButton {background-color: rgb(103, 214, 98);}"
        lim_red_style = "QToolButton {background-color: rgb(242, 101, 101);}"

        low_style = lim_green_style
        low_status = 'Limit is OK'

        high_style = lim_green_style
        high_status = 'Limit is OK'

        if motor_state == "moving":
            self._move_tick += 1  # make diode blinking
            if self._move_tick % 3 == 0:
                st_style = "QToolButton {background-color: rgb(103, 98, 214);}"
            elif self._move_tick % 3 == 1:
                st_style = "QToolButton {background-color: rgb(186, 48, 176);}"
            else:
                st_style = "QToolButton {background-color: rgb(191, 197, 42);}"

            st_tip = "Motor moving"

        # elif motor_state != "on":
        #     self._move_tick = 0
        #     st_style = error_style
        #     st_tip = "Motor OFF"
        else:
            st_style = lim_green_style
            st_tip = "Motor ON"

        if len(limits_state) > 1:
            st_style = error_style
            st_tip =  "Both Limits are touched"

            low_style = high_style = lim_red_style
            low_status = high_status = 'Limit touched'
        elif len(limits_state):
            st_style = error_style

            if limits_state[0] == 'low':
                st_tip = "Low limit are touched"
                low_style = lim_red_style
                low_status = 'Limit touched'
            else:
                st_tip = "High limit are touched"
                high_style = lim_red_style
                high_status = 'Limit touched'

        self._ui.tb_status.setStyleSheet(st_style)
        self._ui.tb_status.setToolTip(st_tip)

        self._ui.tb_low_limit.setStyleSheet(low_style)
        self._ui.tb_low_limit.setToolTip(low_status)

        self._ui.tb_high_limit.setStyleSheet(high_style)
        self._ui.tb_high_limit.setToolTip(high_status)

    # ----------------------------------------------------------------------
    def absolute_motor_name(self):
        """
        Returns:
            (str) name of the motor associated with the widget
        """
        return f"{self._device_handle.name}/{self._motor_handle.name}"

    # ----------------------------------------------------------------------
    def _show_properties(self):
        """
        """
        if self._access_level == "superuser":
            dialog = MotorPropsDialog(self._motor_handle, self)
            dialog.show()


class EventFilter(QtCore.QObject):
    def eventFilter(self, parent, event):
        print(f"Got event: {event} from {parent}")