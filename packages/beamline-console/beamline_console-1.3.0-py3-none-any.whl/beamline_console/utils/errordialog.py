"""
"""

import traceback
import logging

from PyQt5 import QtWidgets
from beamline_console.gui.ErrorDialog_ui import Ui_ErrorDialog


# ----------------------------------------------------------------------
class ErrormsgLogger(logging.Handler):

    # ----------------------------------------------------------------------
    def emit(self, record):
        if record.levelno >= 40:
            ErrorDialog(record.msg).exec_()



# ----------------------------------------------------------------------
class ErrorDialog(QtWidgets.QDialog):
    """
    """

    # ---------------------------------------------------------------------- 
    def __init__(self, record):
        super().__init__()

        self._ui = Ui_ErrorDialog()
        self._ui.setupUi(self)
        self._ui.teDetails.setText(repr(record))
