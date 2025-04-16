"""Displays currently being selected device(s).
"""

import sys
import json
import time
from PyQt5 import QtWidgets, QtCore

from beamline_console.logger.logit import Logit
from beamline_console.devices.motordevice import MotorBasedDevice
from beamline_console.snapshot.slot import Slot
from beamline_console.devicecontrol.motoritemwidget import MotorItemWidget

from beamline_console.gui.DeviceWidget_ui import Ui_DeviceWidget

# ----------------------------------------------------------------------
class DeviceWidget(QtWidgets.QWidget, Logit):
    """
    """
    save_snapshot = QtCore.pyqtSignal(str)  # motors selection info

    DATETIME = "%Y/%m/%d %H:%M:%S"

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """
        Args:
            parent (QWidget)
        """

        QtWidgets.QWidget.__init__(self, parent)
        Logit.__init__(self)

        self._ui = Ui_DeviceWidget()
        self._ui.setupUi(self)

        self._selected_devices = []
        self.widgets_map = {}

        self._beamline_hal = None
        self._settings = None

        self._device_widget_layout = QtWidgets.QVBoxLayout(self._ui.wi_device_container)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.refresh_gui)

        self._ui.but_save.clicked.connect(self._save_snapshot)
        self._ui.but_stop.clicked.connect(self.stop_motors)

    # ----------------------------------------------------------------------
    def initialize(self, beamline_hal, settings):
        """
        """
        self._beamline_hal = beamline_hal
        self._settings = settings

        for dev_name, dev_handle in sorted(self._beamline_hal.device_map.items()):
            for motor_name, motor_handle in dev_handle.motors.items():
                self.widgets_map[f"{dev_name}/{motor_name}"] = MotorItemWidget(self._beamline_hal, dev_handle, motor_handle, self)

        self._timer.start(int(self._settings.option("beamline_ui", "selected_device_refresh_period")))

        self.logger.info("DeviceWidget initialized successfully")

    # ----------------------------------------------------------------------
    def refresh_gui(self):
        """Synchronize GUI (beamline state can be changed by Jive, Astor, etc.)
        """
        for device_name in self._selected_devices:
            try:
                device = self._beamline_hal.device(device_name)
                if isinstance(device, MotorBasedDevice):
                    for motor in device.list_motors():
                        self.widgets_map[f"{device.name}/{motor}"].refresh_gui()
                elif isinstance(device, Slot):
                    for motor in device.list_motors():
                        self.widgets_map[motor].refresh_gui()
            except KeyError:
                pass
            except Exception as e:
                self.logger.error(f"DeviceWidget: cannot refresh gui: {e}")

    # ----------------------------------------------------------------------
    def stop_motors(self):
        """
        """
        try:
            self._beamline_hal.group_action("stop_motors")
            time.sleep(0.5)

            self.sync_gui("absolute")

        except Exception as err:
            self.logger.error(err, exc_info=sys.exc_info())
            raise

            # non motor devs TODO

        self.logger.info("All motors stopped")

    # ----------------------------------------------------------------------
    def selected_device_changed(self, selected_devices):
        """Called when a device is selected in the BeamlineWidget.
        """

        layout = self._device_widget_layout

        for i in reversed(list(range(layout.count()))):
            item = layout.itemAt(i)
            if item:
                widget = layout.itemAt(i).widget()
                if widget:
                    layout.removeWidget(widget)
                    widget.setVisible(False)
                else:
                    layout.removeItem(item)

        self._selected_devices = selected_devices

        for name in selected_devices:
            device = self._beamline_hal.device(name)
            for motor_name in device.list_motors():
                if isinstance(device, MotorBasedDevice):
                    motor_name = f"{device.name}/{motor_name}"
                self.widgets_map[motor_name].setVisible(True)
                layout.addWidget(self.widgets_map[motor_name])
            spacer = QtWidgets.QSpacerItem(22, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
            layout.addSpacerItem(spacer)

        self.sync_gui("absolute")

    # ----------------------------------------------------------------------
    def _save_snapshot(self):
        """
        """
        # support for non-motor devices? TODO
        self.save_snapshot.emit(json.dumps({"devices": self._selected_devices}))

    # ----------------------------------------------------------------------
    def sync_gui(self, mode="absolute"):
        """
        """
        try:
            for device in self.widgets_map.values():
                if isinstance(device, MotorItemWidget):
                    device.sync_pos(mode, "async")
                elif isinstance(device, Slot):
                    for motor in device:
                        motor.sync_pos(mode, "async")
        except:
            pass
