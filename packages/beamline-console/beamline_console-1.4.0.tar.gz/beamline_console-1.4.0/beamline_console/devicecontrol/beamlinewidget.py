"""Displays (most of) the beamline components on a single widget.
"""

from PyQt5 import QtWidgets, QtCore
from beamline_console.base_widget import BaseWidget
from beamline_console.devicecontrol.beamlinegraphicsscene import BeamlineGraphicsScene
from beamline_console.gui.BeamlineWidget_ui import Ui_BeamlineWidget


# ----------------------------------------------------------------------
class BeamlineWidget(BaseWidget):

    WIDGET_NAME = "BeamlineWidget"

    save_snapshot = QtCore.pyqtSignal(str)
    device_selected = QtCore.pyqtSignal(list)

    # ----------------------------------------------------------------------
    def __init__(self, parent):

        BaseWidget.__init__(self, parent)

        self._ui = Ui_BeamlineWidget()
        self._ui.setupUi(self)

        self._access_level = "user"

    # ----------------------------------------------------------------------
    def finish_init(self):

        # widget displaying currently selected devices
        self._ui.device_widget.initialize(self._beamline_hal, self._settings)
        self._ui.device_widget.save_snapshot.connect(lambda selection: self.save_snapshot.emit(selection))
        self._selected_devices = []          # support multi-selection of devices

        self._ui.beamline_view.setFixedHeight(int(self._settings.option("beamline_ui", "section_height"))+25)

        device_list = list(self._beamline_hal.device_map.keys())
        if len(device_list) > 1:
            self._scene = BeamlineGraphicsScene(self._ui.beamline_view, self._beamline_hal, self._settings)
            self._scene.device_selection_changed.connect(self._ui.device_widget.selected_device_changed)
            self._scene.device_selection_changed.connect(lambda dev_list: self.device_selected.emit(dev_list))
            self._ui.beamline_view.setScene(self._scene)
            self._ui.beamline_view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._ui.beamline_view.centerOn(0, 0)
            self._ui.but_show_selector.clicked.connect(lambda checked: self._ui.beamline_view.setVisible(checked))
        else:
            self._scene = None
            self._ui.fr_device_selector.setVisible(False)
            self._ui.device_widget.selected_device_changed(device_list)
            self.device_selected.emit(device_list)

        # keep GUI in sync TODO
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._synchronize)
        self._timer.start(int(self._settings.option("beamline_ui", "beamline_refresh_period")))

        self._move_tick = 0

    # ----------------------------------------------------------------------
    def access_level_changed(self, access_level):
        """
        """
        self._access_level = access_level

    # ----------------------------------------------------------------------
    def sync_control_widget(self):
        """
        (called e.g. when beamline snapshot is executed)
        """
        self._ui.device_widget.sync_gui()

    # ----------------------------------------------------------------------
    def _synchronize(self):
        """TANGO devices might be moved using other clients like jive...
        """

        self._move_tick += 1

        if self._scene:
            for device in self._scene.device_items:
                if self._move_tick % 2 == 1:
                    self._scene.device_items[device].status_diode.setColor('blue')
                else:
                    there_is_error = False
                    there_is_moving = False
                    try:
                        for motor in self._ui.device_widget.device_tuple_map[device]:
                            motor_state, limits_state = motor.get_status()
                            if motor_state == "fault" or limits_state != []:
                                there_is_error = True
                            elif motor_state == "moving":
                                there_is_moving =  True
                                self._scene.device_items[device].status_diode.setColor('green')
                    except AttributeError:
                        pass
                    finally:
                        if there_is_error:
                            self._scene.device_items[device].status_diode.setColor('ligthred')
                        elif there_is_moving:
                            self._scene.device_items[device].status_diode.setColor('green')

    # ----------------------------------------------------------------------
    def resizeEvent(self, event):
        self._ui.beamline_view.fitInView(self._scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)