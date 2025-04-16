"""Show historical positions of the device.
"""

from PyQt5 import QtWidgets

from beamline_console.logger.logit import Logit
from beamline_console.ui_experimentcontrol.DeviceHistoryDialog_ui import Ui_DeviceHistoryDialog


# ----------------------------------------------------------------------
class DeviceHistoryDialog(QtWidgets.QDialog, Logit):
    """
    """
    TIMESTAMP_STYLE = "color: #777777;"

    # ----------------------------------------------------------------------
    def __init__(self, deviceName, beamlineHal, parent):
        """
        Args:
        """
        QtWidgets.QDialog.__init__(self, parent)
        Logit.__init__(self)

        self._ui = Ui_DeviceHistoryDialog()
        self._ui.setupUi(self)

        msg = ""
        for entry in reversed(beamlineHal.history):
            if entry[0] == deviceName:
                msg += self._makeEntry(entry)

        self._ui.teHistory.setText(msg)

        self.setWindowTitle(f"{deviceName} logs")

    # ----------------------------------------------------------------------
    def _makeEntry(self, entry):
        """
        """
        return "<span style=\"{}\">[{}]</span> {}/{} moved from {:.2f} to {:.2f}<br>".format(
            self.TIMESTAMP_STYLE, entry[-1], *entry[:-1])

