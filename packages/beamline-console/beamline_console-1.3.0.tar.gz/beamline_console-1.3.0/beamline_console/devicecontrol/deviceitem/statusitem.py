"""Device status diode
"""

from PyQt5 import QtWidgets, QtCore, QtGui

from beamline_console.logger.logit import Logit


# ----------------------------------------------------------------------
class StatusItem(QtWidgets.QGraphicsRectItem, Logit):

        # adjust to your needs and taste
    SELECTED_STYLE = {"pen": QtGui.QPen(QtGui.QBrush(QtGui.QColor(50, 205, 50)), 2,
                                        QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                        QtCore.Qt.BevelJoin),
                      "brush": QtGui.QBrush(QtGui.QColor(10, 30, 190, 10))
                     }
                      
    DESELECTED_STYLE = {"pen": QtGui.QPen(QtGui.QBrush(QtGui.QColor(200, 200, 200)), 1,
                                          QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                          QtCore.Qt.BevelJoin),
                        "brush": QtGui.QBrush(QtGui.QColor(10, 30, 190, 10))
                       }

    WIDTH = 25
    HEIGHT = 18

    # ----------------------------------------------------------------------
    def __init__(self, frame_geometry):
        QtWidgets.QGraphicsRectItem.__init__(self)
        Logit.__init__(self)
       
        self._initial_geom = QtCore.QRectF(*frame_geometry)
        self._frame_geometry = frame_geometry
        x = frame_geometry[0] + frame_geometry[3] - self.WIDTH   #+ frameGeometry[2] - self.WIDTH
        y = frame_geometry[1] - 25 + 18 #headerPos
        
        self.setRect(x, y + 8, self.WIDTH, frame_geometry[3] - 1)

        rect = self.boundingRect()
        lgrad = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())
        lgrad.setColorAt(1.0, QtGui.QColor(30, 144, 255, 200))
        lgrad.setColorAt(0.0, QtGui.QColor(30, 144, 255, 0))
        self.setBrush(lgrad)

        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))

    # ----------------------------------------------------------------------
    def setActive(self, isActive):
        """
        """
        #self.selRect.setPen(self.ACTIVE_PEN if isActive else self.INACTIVE_PEN)
        
    # ----------------------------------------------------------------------
    def updateOffsetX(self, offsetX):
        """
        """
        self.offsetX = offsetX
        
        rect = self.rect()
        #rect.setLeft(self._initialGeom.left() + self._initialGeom.width() - self.WIDTH + self.offsetX)
        rect.setLeft(self._initial_geom.left() + self.offsetX + self._frame_geometry[2] - self.WIDTH)
        rect.setRight(self._initial_geom.right() - self._initial_geom.width() + self.offsetX + self._frame_geometry[2])
        self.setRect(rect)

    # ----------------------------------------------------------------------
    def setColor(self, color):
        rect=self.rect()
        lgrad = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())
        lgrad.setColorAt(0.0, QtGui.QColor(30, 144, 255, 0))

        if color =='strongred':
            self.setBrush(QtGui.QBrush(QtGui.QColor(30, 144, 255, 70))) #QtGui.QColor(255, 10, 10, 190)
            self.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255, 120))) #QtGui.QColor(255, 10, 10, 255)
        elif color == 'ligthred':
            lgrad.setColorAt(1.0, QtGui.QColor(205, 10, 10, 150))
            self.setBrush(lgrad)

        elif color =='green':
            lgrad.setColorAt(1.0, QtGui.QColor(50, 205, 50, 190))
            self.setBrush(lgrad)

        elif color =='blue':
            lgrad.setColorAt(1.0, QtGui.QColor(30, 144, 255, 120))
            self.setBrush(lgrad)

            #self.setBrush(QtGui.QBrush(QtGui.QColor(30, 144, 255, 70))) #50, 205, 50, 190

            #
        elif color == 'orange':
            self.setBrush(QtGui.QBrush(QtGui.QColor(205, 205, 50, 190)))


