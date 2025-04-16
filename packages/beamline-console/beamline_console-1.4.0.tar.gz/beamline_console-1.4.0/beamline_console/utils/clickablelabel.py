#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author:        Sebastian Piec <sebastian.piec@desy.de>
# Last modified: 2017, October 9
# ----------------------------------------------------------------------

"""Emits clicked signal, which normal QLabel is lacking.
"""

from PyQt5 import QtWidgets, QtCore

# ----------------------------------------------------------------------
class ClickableLabel(QtWidgets.QLabel):

        # args: ctrl key is pressed
    double_clicked = QtCore.pyqtSignal()
     
    # ----------------------------------------------------------------------
    def __init(self, parent):
        super().__init()
 
    # ----------------------------------------------------------------------
    def mouseDoubleClickEvent(self, event):
        self.double_clicked.emit()
        event.accept()