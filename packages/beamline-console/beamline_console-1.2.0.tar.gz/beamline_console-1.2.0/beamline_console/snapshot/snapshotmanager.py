# yury.matveev@desy.de
"""
Class used for management of beamline state snapshots.
"""

import os
import shutil

from PyQt5 import QtCore

from beamline_console.logger.logit import Logit
from beamline_console.snapshot.beamsnapshot import BeamlineSnapshot

# ----------------------------------------------------------------------
class SnapshotManager(QtCore.QObject, Logit):
    """
    """
    changed = QtCore.pyqtSignal()

    # ---------------------------------------------------------------------- 
    def __init__(self, beamline_hal, snapshots_dir=""):
        """
        """
        QtCore.QObject.__init__(self)
        Logit.__init__(self)

        self._snapshots_dir = ""
        self._trash_dir = ""

        self._beamline_hal = beamline_hal
        self.set_snapshots_dir(snapshots_dir)

        self.beamline_snapshots = []

        self._current_snapshot = None

    # ----------------------------------------------------------------------
    def add_snapshot(self, snapshot):
        """
        """
        if snapshot.name in [s.name for s in self.beamline_snapshots]: 
            raise RuntimeError(f"Snapshot {snapshot.name} already exists")

        self.beamline_snapshots.append(snapshot)
    
    # ----------------------------------------------------------------------
    def update_snapshot(self, snapshot_name):
        """Update snapshot to current position.
        """
        self.logger.info(f"Snapshot {snapshot_name} updated")

        for snapshot_idx, snapshot in enumerate(self.beamline_snapshots):
            if snapshot.name == snapshot_name:
                os.remove(snapshot.filename)
                snapshot.update_position()
                snapshot.save(snapshot.filename)

    # ----------------------------------------------------------------------
    def delete_snapshot(self, snapshot_name):
        """Move snapshot to the "trash directory".
        """
        self.logger.debug(f"Removing snapshot {snapshot_name}")

        for snapshot_idx, snapshot in enumerate(self.beamline_snapshots):
            if snapshot.name == snapshot_name:
                dest_fname = os.path.join(self._trash_dir, os.path.basename(snapshot.filename))
                if os.path.exists(dest_fname):
                    os.remove(dest_fname)

                shutil.move(snapshot.filename, self._trash_dir)
        
                del self.beamline_snapshots[snapshot_idx]
                break

    # ---------------------------------------------------------------------- 
    def load(self, snapshots_dir):
        """Reload snapshots from the snapshots directory.
        """
        self.set_snapshots_dir(snapshots_dir)
        self._reload_all(sorted(os.listdir(snapshots_dir)))

    # ----------------------------------------------------------------------
    def _reload_all(self, file_list):
        """
        """
        self.beamline_snapshots = []
    
        for filename in file_list:
            full_name = os.path.join(self._snapshots_dir, filename)
            if os.path.isdir(full_name):
                continue

            snap_name, ext = os.path.splitext(filename)
            if ext.lower() == ".xml" and snap_name:
                snapshot = BeamlineSnapshot(self._beamline_hal)
                if snapshot.load(full_name):
                    self.add_snapshot(snapshot)
 
    # ----------------------------------------------------------------------
    def empty(self):
        """
        Returns:
            (bool)
        """
        return len(self.beamline_snapshots) < 1  

    # ----------------------------------------------------------------------
    def set_snapshots_dir(self, snapshots_dir):
        """Set directory used for beamline snapshots and update "trash" accordingly.
        """
        self._snapshots_dir = snapshots_dir
        self._trash_dir = os.path.join(snapshots_dir, "_trash")
    
        if not os.path.exists(self._trash_dir):
            os.mkdir(self._trash_dir)

    # ----------------------------------------------------------------------
    def snapshots_dir(self):
        """
        Returns:
            (str)
        """
        return self._snapshots_dir

    # ----------------------------------------------------------------------
    def __len__(self):
        """
        """
        return len(self.beamline_snapshots)


    # NOTE: here, SnapshotManager acts as proxy for the currently being executed snapshot!
    # ----------------------------------------------------------------------
    def state(self):
        """
        Returns:
            (str) state of the currently being executed snapshot
        """
        if not self._current_snapshot:
            return "idle"
       
        return self._current_snapshot.state

    # ----------------------------------------------------------------------
    def pause(self):
        """Pause currently executed snapshot - works in async mode only!
        """
        if self._current_snapshot:
            self._current_snapshot.pause()
     
    # ----------------------------------------------------------------------
    def resume(self):
        """Pause currently executed snapshot - works in async mode only!
        """
        if self._current_snapshot:
            self._current_snapshot.resume()

    # ----------------------------------------------------------------------
    def abort(self):
        """Pause currently executed snapshot - works in async mode only!
        """
        if self._current_snapshot:
            self._current_snapshot.abort()
