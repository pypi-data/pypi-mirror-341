# yury.matveev@desy.de

"""
Widget displaying saved beamline snapshots.
"""

import os
import sys

from distutils.util import strtobool

from PyQt5 import QtWidgets, QtCore, QtGui

from beamline_console.base_widget import BaseWidget
from beamline_console.snapshot.snapshotmanager import SnapshotManager
from beamline_console.snapshot.beamsnapshot import BeamlineSnapshot
from beamline_console.snapshot.savesnapshotdialog import SaveSnapshotDialog
from beamline_console.gui.SnapshotWidget_ui import Ui_SnapshotWidget


# ----------------------------------------------------------------------
class SnapshotWidget(BaseWidget):
    """
    """
    WIDGET_NAME = "SnapshotWidget"

    motors_moved = QtCore.pyqtSignal()

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        BaseWidget.__init__(self, parent)

        self._ui = Ui_SnapshotWidget()
        self._ui.setupUi(self)

        self._snapshot_manager = SnapshotManager(parent.beamline_hal)

        self._snapshot_dir = ""
        self.device_selected([""])

        self._access_level = "user"

        self._ui.tw_snapshots.cellDoubleClicked.connect(self._use_selected_snapshot)
        self._ui.but_apply.clicked.connect(self._use_selected_snapshot)
        self._ui.but_delete.clicked.connect(self._delete_selected_snapshot)

        self._context_menu = QtWidgets.QMenu("SnapshotsWidget_ctxmenu", self)

        act_use_snapshot = QtWidgets.QAction("Use Snapshot", self)
        act_use_snapshot.triggered.connect(self._use_selected_snapshot)
        self._context_menu.addAction(act_use_snapshot)

        self.act_update_snapshot = QtWidgets.QAction("Update Snapshot", self)
        self.act_update_snapshot.triggered.connect(self._update_selected_snapshot)
        self.act_update_snapshot.setVisible(False)
        self._context_menu.addAction(self.act_update_snapshot)

        act_delete_snapshot = QtWidgets.QAction("Delete Snapshot", self)
        act_delete_snapshot.triggered.connect(self._delete_selected_snapshot)
        self._context_menu.addAction(act_delete_snapshot)

        act_refresh = QtWidgets.QAction(QtGui.QIcon(":/icons/refresh.png"), "Refresh", self)
        act_refresh.triggered.connect(self.refresh)

        self._context_menu.addSeparator()
        self._context_menu.addAction(act_refresh)

        self._ui.tw_snapshots.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._ui.tw_snapshots.customContextMenuRequested.connect(lambda:
            self._context_menu.exec_(QtGui.QCursor.pos()))

        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    # ----------------------------------------------------------------------
    def refresh(self):
        """
        """
        self._snapshot_manager.load(self._snapshot_dir)
        self._ui.tw_snapshots.setRowCount(0)

        headers = ["Name"]

        if self._snapshot_manager.beamline_snapshots:
            for ind, motor in enumerate(self._snapshot_manager.beamline_snapshots[0].motor_items):
               headers.append(motor[1])

        # headers += [""]

        self._ui.tw_snapshots.setColumnCount(len(headers))
        self._ui.tw_snapshots.setHorizontalHeaderLabels(headers)

        for idx, snapshot in enumerate(self._snapshot_manager.beamline_snapshots):
            self._ui.tw_snapshots.setRowCount(idx + 1)
            self._ui.tw_snapshots.setItem(idx, 0, QtWidgets.QTableWidgetItem(snapshot.name))
            for ind, motor in enumerate(snapshot.motor_items):
                self._ui.tw_snapshots.setItem(idx, 1 + ind, QtWidgets.QTableWidgetItem(str(motor[2])))

        header = self._ui.tw_snapshots.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for ind in range(1, len(headers)):
            header.setSectionResizeMode(ind , QtWidgets.QHeaderView.ResizeToContents)

    # ----------------------------------------------------------------------
    def access_level_changed(self, access_level):
        """
        """
        self._access_level = access_level
        self.act_update_snapshot.setVisible(access_level=="superuser")

    # ----------------------------------------------------------------------
    def device_selected(self, devices):
        app_dir = os.path.join(os.path.join(os.path.expanduser('~'), '.beamline_console'))
        if "bl_snapshots" not in os.listdir(app_dir):
            os.mkdir(os.path.join(app_dir, "bl_snapshots"))

        self._snapshot_dir = os.path.join(app_dir, "bl_snapshots")

        device = devices[0]
        if device:
            if device not in os.listdir(self._snapshot_dir):
                os.mkdir(os.path.join(self._snapshot_dir, device))

            self._snapshot_dir = os.path.join(self._snapshot_dir, device)

        self.refresh()

    # ----------------------------------------------------------------------
    def _update_selected_snapshot(self):
        if self._access_level == "superuser":
            items = self._ui.tw_snapshots.selectedItems()
            if items:
                snapshot_name = items[0].text()
                msg = f"Are you sure you want to update snapshot {snapshot_name}?"
                if QtWidgets.QMessageBox.question(self, "Confirm", msg,
                                              QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:

                    self._snapshot_manager.update_snapshot(snapshot_name)
                    self.refresh()

    # ----------------------------------------------------------------------
    def _use_selected_snapshot(self):
        items = self._ui.tw_snapshots.selectedItems()
        if items:
            filename = f"{os.path.join(self._snapshot_dir, items[0].text())}.xml"

            try:
                if strtobool(self._settings.option("snapshots", "confirmation_to_apply")):
                    response, move_scheme = self._confirm_move(filename)
                else:
                    response = True

            except Exception as err:
                self.logger.error(f"Cannot confirm move: {repr(err)}", exc_info=sys.exc_info())
                raise
            else:
                if response:
                    try:
                        self._beamline_hal.move_snapshot(filename, "async")
                    except Exception as err:
                        self.logger.error(f"Error during move: {repr(err)}", exc_info=sys.exc_info())
                        raise

    # ----------------------------------------------------------------------
    def _delete_selected_snapshot(self):
        items = self._ui.tw_snapshots.selectedItems()
        if items:
            snapshot_name= items[0].text()

            msg = f"Are you sure you want to delete snapshot {snapshot_name}?"
            if QtWidgets.QMessageBox.question(self, "Confirm", msg,
                                          QtWidgets.QMessageBox.Yes,
                                          QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:

                self._snapshot_manager.delete_snapshot(snapshot_name)
                self.refresh()

    # ----------------------------------------------------------------------
    def _confirm_move(self, filename):
        """
        Args:
            filename (str)
        Returns:
            flag
            move_map
        """
        move_groups = {}

        snapshot = BeamlineSnapshot(filename)
        for item in snapshot.motor_items:
            step = item[3]

            if not step in move_groups:
                move_groups[step] = []

            move_groups[step].append(item[:3])

        move_map = {"status": "ok",
                   "type": "move_motor",
                   "details": []}

        scheme = ""
        for group_idx, (group_name, group_handle) in enumerate(move_groups.items()):
            scheme += f"Step {group_idx}\n"

            for item in group_handle:
                scheme += f"   {item[0]}/{item[1]}, target: {float(item[2]):.5f}\n"

                motor_name = "{}/{}".format(*item[:2])

                prev_pos = self._beamline_hal.motor_position(motor_name)

                move_map["details"].append({"motor_name": motor_name,
                                           "prev_pos": prev_pos,
                                           "target_pos": item[2]
                                          })

        msg = "Use snapshot {} created on {}?\n\n{}".format(filename,
                                                            snapshot.date_time,
                                                            scheme)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(msg)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg_box.setWindowTitle("Confirm")

        return (msg_box.exec_() == QtWidgets.QMessageBox.Yes), move_map

    # ----------------------------------------------------------------------
    def save_snapshot(self, selection):
        """
        Args:
            (map) selection, e.g. {"device": ["table", "manipulator"]}
        """
        SaveSnapshotDialog(self._beamline_hal, selection, self._snapshot_manager).exec_()
        self.refresh()
