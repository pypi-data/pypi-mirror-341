"""Logger propagating log records to the LoggingWidget.
"""

from logging import StreamHandler
from PyQt5 import QtCore


# ----------------------------------------------------------------------
class GuiLogger(StreamHandler):

    def __init__(self):
        StreamHandler.__init__(self)
        self.logger = Logger()

    # ----------------------------------------------------------------------
    def emit(self, record):
        try:
            self.logger.emit_record.emit(int(record.levelno), f'{record.asctime.split(",")[0]} {record.levelname} {record.msg}')
        except:
            print(f'{int(record.levelno)}: {record.asctime.split(",")[0]} {record.levelname} {record.msg}')


# ----------------------------------------------------------------------
class Logger(QtCore.QObject):

    emit_record = QtCore.pyqtSignal(int, str)
