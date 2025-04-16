# yury.matveev@desy.de

from PyQt5 import QtWidgets

from beamline_console.logger.logit import Logit

# ----------------------------------------------------------------------
class BaseWidget(QtWidgets.QWidget, Logit):

    WIDGET_NAME = ""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        Logit.__init__(self)

        self._settings = parent.settings
        self._beamline_hal = parent.beamline_hal

    # ----------------------------------------------------------------------
    def save_ui_settings(self, settings):
        """
        """
        settings.setValue(f"{self.WIDGET_NAME}/geometry", self.saveGeometry())

    # ----------------------------------------------------------------------
    def load_ui_settings(self, settings):
        """
        """
        try:
            self.restoreGeometry(settings.value(f"{self.WIDGET_NAME}//geometry"))
        except:
            pass

