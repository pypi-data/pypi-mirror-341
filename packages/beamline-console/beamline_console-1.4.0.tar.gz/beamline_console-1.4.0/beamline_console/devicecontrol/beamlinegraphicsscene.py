"""Manage DeviceGraphicsItem objects representing beamline devices.
This class is tightly coupled with BeamlineGraphicsView.
"""

import os

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, QRectF, Qt
from PyQt5.QtGui import QPixmap
from distutils.util import strtobool
from beamline_console.logger.logit import Logit
from beamline_console.devicecontrol.deviceitem.devicegraphicsitem import DeviceGraphicsItem


# ----------------------------------------------------------------------
class BeamlineGraphicsScene(QGraphicsScene, Logit):
    """
    """
    device_selection_changed = pyqtSignal(list)

    # ----------------------------------------------------------------------
    def __init__(self, parent, beamline_hal, settings):

        self._device_list = list(beamline_hal.device_map.keys())

        widget_rows = int(settings.option("beamline_ui", "widget_rows"))
        scene_height = int(settings.option("beamline_ui", "section_height"))

        slot_mode = strtobool(settings.option("general", "enable_slots"))

        if slot_mode:
            main_folder = os.path.join(os.path.expanduser('~'), '.beamline_console')
            background_file = os.path.join(main_folder, settings.option("background", "background_file"))
            if not os.path.isfile(background_file):
                raise RuntimeError(f"Cannot open background file {background_file}")
            pixmap = QPixmap(background_file)
            scene_width = scene_height * pixmap.width()/pixmap.height()
        else:
            scene_width = len(self._device_list) // widget_rows
            scene_width += 1 if len(self._device_list) % widget_rows else 0
            scene_width *= scene_height

        QGraphicsScene.__init__(self, QRectF(0, 0, scene_width, scene_height), parent)
        Logit.__init__(self)

        self._selected_devices = []
        self.device_items = {}

        if slot_mode:
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.addItem(pixmap_item)

            for slot_name, slot_item in beamline_hal.slots_map.items():
                self.device_items[slot_name] = DeviceGraphicsItem(self, slot_item.name, slot_item.position, True)

            for device_name, device_item in beamline_hal.device_map.items():
                if device_item.widget_position is not None:
                    self.device_items[device_name] = DeviceGraphicsItem(self, device_item.name, device_item.widget_position)

            for item in list(self.device_items.values()):
                item.set_active(False)

        else:
            horizontal_step = int(settings.option("beamline_ui", "horizontal_step"))
            vertical_step = int(settings.option("beamline_ui", "vertical_step"))
            device_width = int(settings.option("beamline_ui", "device_width"))
            device_height = int(settings.option("beamline_ui", "device_height"))

            shift_x = (horizontal_step - device_width) // 2
            shift_y = (vertical_step - device_height) // 2

            row_count = 0
            column_count = 0
            for device in self._device_list:
                geometry = [shift_x + column_count * horizontal_step,
                            shift_y + row_count * vertical_step, device_width, device_height]
                self.device_items[device] = DeviceGraphicsItem(self, device, geometry, False)
                row_count += 1
                if row_count == widget_rows:
                    row_count = 0
                    column_count += 1
   
    # ----------------------------------------------------------------------
    def mouseMoveEvent(self, event):
        """
        """
        super().mouseMoveEvent(event)
        
        #pos = event.scenePos()

    # ----------------------------------------------------------------------
    def mousePressEvent(self, event):
        """
        """
        super().mousePressEvent(event)

        pos = event.scenePos()

        if Qt.ControlModifier != event.modifiers():
            self._selected_devices = []
            
        device_name = self._intersect(pos)
        if device_name:
            if device_name not in self._selected_devices:
                self._selected_devices.append(device_name)
            else:
                self._selected_devices.remove(device_name)

        self.logger.debug(f"BeamlineGraphicsScene: new selection: {self._selected_devices}")
        self.device_selection_changed.emit(self._selected_devices)

    # ----------------------------------------------------------------------
    def _intersect(self, pos):
        """
        """
        for name, graphics_item in list(self.device_items.items()):
            if graphics_item.intersect(pos):
                return name

        return None
