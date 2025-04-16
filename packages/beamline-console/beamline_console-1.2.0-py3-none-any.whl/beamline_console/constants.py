#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author:   spiec@
# Modified: 2019
# ----------------------------------------------------------------------
import os
import logging

from PyQt5 import QtCore, QtGui

APP_NAME = 'ExperimentalControl'
SCRIPT_LOG = 'ExperimentalControlScript'

LOG_FOLDER = f"{os.path.expanduser('~')}/.beamline_console/logs"
LOG_FORMATTER = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)-8s %(message)s")

# Log widget coloring

DEBUG_COLOR = QtGui.QColor(0, 0, 0)
INFO_COLOR = QtGui.QColor(80, 230, 80)
WARNING_COLOR = QtGui.QColor(255, 93, 42)
ERROR_COLOR = QtGui.QColor(255, 42, 42)

DATE_COLOR = QtGui.QColor(90, 90, 90)

DEVICE_TITEL = QtGui.QFont("Bitstream Charter", 18, QtGui.QFont.Bold)