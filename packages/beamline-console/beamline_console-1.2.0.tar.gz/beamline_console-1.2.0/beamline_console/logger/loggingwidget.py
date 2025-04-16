# yury.matveev@desy.de

import logging
import re
import os
from collections import namedtuple
from dateutil.parser import parse

from PyQt5 import QtWidgets, QtCore

from beamline_console import LOG_FOLDER

from beamline_console.base_widget import BaseWidget
from beamline_console.logger.highlightlogs import HighlightLogs
from beamline_console.gui.LoggingWidget_ui import Ui_LoggingWidget

BUFFER_SIZE = 1000

LVL_MAP = {0: logging.DEBUG,
           1: logging.INFO,
           2: logging.WARNING,
           3: logging.ERROR}

NAME_MAP = {"debug": 0,
            "info": 1,
            "warning": 2,
            "error": 3}

# ----------------------------------------------------------------------
class LoggingWidget(BaseWidget):

    WIDGET_NAME = "LoggingWidget"

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        BaseWidget.__init__(self, parent)

        self._logs_buffer = []           # (log_level, message) pairs

        self._ui = Ui_LoggingWidget()
        self._ui.setupUi(self)

        default_log_level = str(parent.settings.option("general", "log_level")).lower()

        if default_log_level in NAME_MAP:
            self._ui.cb_log_level.setCurrentIndex(NAME_MAP[default_log_level])

        self._ui.cb_log_level.currentIndexChanged.connect(self._display_logs)

        self._highlighter = self._setup_text_edit()

        self.read_log()

    # ----------------------------------------------------------------------
    def access_level_changed(self, access_level):
        pass

    # ----------------------------------------------------------------------
    def get_record(self, log_level, message):

        if len(self._logs_buffer) > BUFFER_SIZE:        # circular buffer
            self._logs_buffer.pop(0)

        self._logs_buffer.append((log_level, message))
        self._display_logs()

    # ----------------------------------------------------------------------
    def _display_logs(self):
        """
        """
        self._ui.te_logs.clear()

        for level, msg in self._logs_buffer:  #reversed(self._logsBuffer)
            if level >= self._current_level():
                self._ui.te_logs.append(msg)

    # ----------------------------------------------------------------------
    def _current_level(self):
        """
        Returns:
            current logging level (normalized)
        """
        return LVL_MAP[self._ui.cb_log_level.currentIndex()]

    # ----------------------------------------------------------------------
    def _setup_text_edit(self):
        """
        """
        return HighlightLogs(self._ui.te_logs)

    # ----------------------------------------------------------------------
    def read_log(self):

        log_file = os.path.join(LOG_FOLDER, "main.log")

        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                file_lines = f.readlines()

            if len(file_lines) > BUFFER_SIZE:
                file_lines = file_lines[-BUFFER_SIZE:]

            prog_dialog = QtWidgets.QProgressDialog("", "Cancel", 0, len(file_lines), self)
            prog_dialog.setWindowTitle("Loading logs")
            prog_dialog.setLabelText("Loading logs")
            prog_dialog.setWindowModality(QtCore.Qt.WindowModal)
            prog_dialog.show()

            count = 0
            for line in file_lines:
                data = re.split(" +", line)
                if self.is_date(data[0]):
                    message = f"{' '.join(data[0:2])} {data[3]} {' '.join(data[5:])[:-1]}"
                    self._logs_buffer.append((logging._nameToLevel[data[3]], message))

                QtCore.QCoreApplication.processEvents()
                if prog_dialog.wasCanceled():
                    break
                prog_dialog.setValue(count)
                count += 1

            prog_dialog.close()

            self._display_logs()

    # ----------------------------------------------------------------------
    def is_date(self, string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False
        
    # ----------------------------------------------------------------------
    def save_ui_settings(self, settings):
        """
        """
        BaseWidget.save_ui_settings(self, settings)

    # ----------------------------------------------------------------------
    def load_ui_settings(self, settings):
        """
        """
        BaseWidget.load_ui_settings(self, settings)
