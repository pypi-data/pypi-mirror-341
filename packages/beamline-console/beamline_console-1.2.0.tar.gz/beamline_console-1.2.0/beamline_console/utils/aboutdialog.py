"""'About program' dialog
"""

from datetime import datetime
import os

from PyQt5 import QtWidgets

from beamline_console.gui.AboutDialog_ui import Ui_AboutDialog


# ----------------------------------------------------------------------
class AboutDialog(QtWidgets.QDialog):
    """
    """
    SOURCE_DIR = "src"
    DATETIME = "%Y-%m-%d %H:%M:%S"

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        super().__init__(parent)

        self._ui = Ui_AboutDialog()
        self._ui.setupUi(self)

        # in case of multiple screens center on the primary one
        frame = self.frameGeometry()

        desktop = QtWidgets.QApplication.desktop()
        centerPoint = desktop.screenGeometry(desktop.primaryScreen()).center()

        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())