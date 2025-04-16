"""Selection frame around device's graphicsitem, including title.
"""

from PyQt5 import QtWidgets

from beamline_console.constants import DEVICE_TITEL

# ----------------------------------------------------------------------
class TitleItem(QtWidgets.QGraphicsTextItem):

    # ----------------------------------------------------------------------
    def __init__(self, text, geometry):
        QtWidgets.QGraphicsTextItem.__init__(self, text)

        self._geometry = geometry
        self._width= int(self.textWidth())
        self.setPos(self._geometry[0], self._geometry[1])
        self.setFont(DEVICE_TITEL)

        #
        self.offsetX = 0
        self.offsetY = 0

    # ----------------------------------------------------------------------
    def updateOffsetX(self, offsetX):
        """
        """
        self.offsetX = offsetX
        self.setX(self._geometry[0] + self.offsetX)
