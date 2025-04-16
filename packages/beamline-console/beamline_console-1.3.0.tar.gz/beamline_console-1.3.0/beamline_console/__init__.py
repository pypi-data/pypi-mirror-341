import sys
import os
import logging
import traceback
import time
import shutil

try:
    from io import StringIO
except ImportError:
    from io import StringIO

from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from logging.handlers import RotatingFileHandler

from optparse import OptionParser
from beamline_console.constants import APP_NAME, LOG_FORMATTER, LOG_FOLDER
from beamline_console.main_window import ExperimentalControl


# ----------------------------------------------------------------------
def abspath(*path):
    """A method to determine absolute path for a given relative path to the
    directory where this setup.py script is located"""
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(setup_dir, *path)


# ----------------------------------------------------------------------
def check_installation():
    home_path = os.path.join(os.path.expanduser('~'), '.beamline_console')
    if not os.path.exists(home_path):
        os.mkdir(home_path)

        # copy default settings
        shutil.copyfile(abspath('default_config/main.cfg'), os.path.join(home_path, 'main.cfg'))
        shutil.copyfile(abspath('default_config/devices.xml'), os.path.join(home_path, 'devices.xml'))
        shutil.copyfile(abspath('default_config/slots.xml'), os.path.join(home_path, 'slots.xml'))
        shutil.copyfile(abspath('default_config/background.png'), os.path.join(home_path, 'background.png'))

        snapshot_folder = os.path.join(home_path, 'bl_snapshots')
        os.mkdir(snapshot_folder)

# --------------------------------------------------------------------
def excepthook(exc_type, exc_value, traceback_obj):
    """
    Global function to catch unhandled exceptions. This function will result in an error dialog which displays the
    error information.

    :param exc_type: exception type
    :param exc_value: exception value
    :param traceback_obj: traceback object
    :return:
    """
    separator = '-' * 80
    log_path = f"{Path.home()}/.beamline_console/logs/error.log"
    time_string = time.strftime("%Y-%m-%d, %H:%M:%S")
    tb_info_file = StringIO()
    traceback.print_tb(traceback_obj, None, tb_info_file)
    tb_info_file.seek(0)
    tb_info = tb_info_file.read()
    errmsg = f'{str(exc_type)}: \n{str(exc_value)}'
    sections = [separator, time_string, separator, errmsg, separator, tb_info]
    msg = '\n'.join(sections)
    try:
        f = open(log_path, "a")
        f.write(msg)
        f.close()
    except OSError:
        pass

    msg_box = QtWidgets.QMessageBox()
    msg_box.setModal(False)
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setText(msg)
    msg_box.setInformativeText(msg)
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.show()


# --------------------------------------------------------------------
def setup_logger(args):

    while not os.path.exists(LOG_FOLDER):
        folder = LOG_FOLDER
        while not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except FileNotFoundError:
                folder = os.path.dirname(folder)

    log_level = logging.DEBUG

    filename = os.path.join(LOG_FOLDER, "main.log")
    print(f"Main logs to file: {filename}")

    main_handler = RotatingFileHandler(filename, mode='a', maxBytes=5 * 1024 * 1024,
                                     backupCount=2, encoding=None, delay=0)
    main_handler.setFormatter(LOG_FORMATTER)
    main_handler.setLevel(log_level)

    app_log = logging.getLogger(APP_NAME)
    app_log.setLevel(log_level)

    app_log.addHandler(main_handler)

    if args.log:
        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(LOG_FORMATTER)
        app_log.addHandler(console)


# --------------------------------------------------------------------
def get_options(args=None):
    parser = OptionParser()

    parser.add_option("-u", "--user", dest='user', default='user')
    parser.add_option("--log", action='store_true', dest='log', help="print logs to console")
    parser.add_option("-c", "--config", dest='config', default='main.cfg')

    (options, _) = parser.parse_args(args)

    if not options.config.endswith('.cfg'):
        options.config += '.cfg'

    return options


# --------------------------------------------------------------------
def main():

    check_installation()

    args = get_options(sys.argv)
    setup_logger(args)

    app = QtWidgets.QApplication([])
    sys.excepthook = excepthook

    mainWindow = ExperimentalControl(args)
    if mainWindow.finish_init():
        mainWindow.show()
        app.exec_()
    else:
        mainWindow.exit_program(True)

# --------------------------------------------------------------------
# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    main()
