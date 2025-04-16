"""Graphical representation of device in QGraphicsScene
"""

from PyQt5 import QtCore

from beamline_console.logger.logit import Logit
from beamline_console.devicecontrol.deviceitem.frameitem import FrameItem
from beamline_console.devicecontrol.deviceitem.statusitem import StatusItem
from beamline_console.devicecontrol.deviceitem.titleitem import TitleItem


# ----------------------------------------------------------------------
class DeviceGraphicsItem(QtCore.QObject, Logit):

    # ----------------------------------------------------------------------
    def __init__(self, scene, device_name, geometry, no_pen=False):
        QtCore.QObject.__init__(self)
        Logit.__init__(self)
      
        self.device_name = device_name

        self.offsetX = 0
        self.offsetY = 0

        # constituents of "device graphics item"
        self._frame = FrameItem(geometry, no_pen)
        scene.addItem(self._frame)

        self.status_diode = StatusItem(geometry)
        scene.addItem(self.status_diode)

        self._title = TitleItem(device_name, geometry)
        scene.addItem(self._title)

    # ----------------------------------------------------------------------
    def set_active(self, flag):
        """
        """
        self._frame.setActive(flag)
        self._title.setActive(flag)
        self.status_diode.setActive(flag)
         
    # ----------------------------------------------------------------------
    def set_visible(self, flag):
        """
        """
        self._frame.setVisible(flag)
        self._title.setVisible(flag)
        self.status_diode.setVisible(flag)

    # ----------------------------------------------------------------------
    def updateOffsetX(self, offsetX):
        """
        """
        self.offsetX = offsetX

        self._frame.updateOffsetX(offsetX)
        self._title.updateOffsetX(offsetX)
        self.status_diode.updateOffsetX(offsetX)

    # ----------------------------------------------------------------------
    def intersect(self, point):
        """
        Returns:
            bool, True if given point lies inside selection rectangle
                  (takes into account potential x/y offsets)
        """
        return self._frame.rect().contains(point)
