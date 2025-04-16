"""Selection frame around device's graphicsitem, including title.
"""

from PyQt5 import QtWidgets, QtGui, QtCore

from beamline_console.logger.logit import Logit

# ----------------------------------------------------------------------
class FrameItem(QtWidgets.QGraphicsRectItem, Logit):

        # adjust to your needs and taste
    INACTIVE_PEN = QtGui.QPen(QtGui.QBrush(QtGui.QColor(170, 170, 170)), 2,
                              QtCore.Qt.DotLine, QtCore.Qt.SquareCap,
                              QtCore.Qt.BevelJoin)
    ACTIVE_PEN = QtGui.QPen(QtGui.QBrush(QtGui.QColor(30, 144, 255, 120)), 2,
                            QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                            QtCore.Qt.BevelJoin)
    
    INACTIVE_BRUSH = QtGui.QBrush(QtGui.QColor(30, 144, 255, 10))
    ACTIVE_BRUSH = QtGui.QBrush(QtGui.QColor(30, 144, 255, 50))

    # ----------------------------------------------------------------------
    def __init__(self, geometry, no_pen=False):
        QtWidgets.QGraphicsRectItem.__init__(self, *geometry)
        Logit.__init__(self)
       
        self._initialGeom = self.rect()
        self.no_pen = no_pen

        if not self.no_pen:
            self.setPen(self.INACTIVE_PEN)
        self.setBrush(self.ACTIVE_BRUSH)

            # 
        self.offsetX = 0
        self.offsetY = 0
        
    # ----------------------------------------------------------------------
    def setActive(self, isActive):
        """
        """
        if not self.no_pen:
            self.setPen(self.ACTIVE_PEN if isActive else self.INACTIVE_PEN)
        self.setBrush(self.ACTIVE_BRUSH if isActive else self.INACTIVE_BRUSH)
       
    # ----------------------------------------------------------------------
    def updateOffsetX(self, offsetX):
        """
        """
        self.offsetX = offsetX
        
        rect = self.rect()
        rect.setLeft(self._initialGeom.left() + self.offsetX)
        rect.setRight(self._initialGeom.right() + self.offsetX)
        
        self.setRect(rect)
        
