# yury.matveev@desy.de

import logging

from beamline_console.constants import APP_NAME

# ----------------------------------------------------------------------
class Logit:
    def __init__(self):
        self.logger = logging.getLogger(APP_NAME)
