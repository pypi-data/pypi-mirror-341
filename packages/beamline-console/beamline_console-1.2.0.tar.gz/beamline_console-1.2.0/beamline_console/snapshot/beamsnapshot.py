from datetime import datetime
import re
import logging
import sys
import threading
import time

from beamline_console.constants import APP_NAME

from xml.dom.minidom import (Document, parseString)

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class BeamlineSnapshot(threading.Thread):
    """
    """
    TIME_STAMP_FMT = "%Y-%m-%d %H:%M:%S"
    REFRESH_RATE = 1.5            # seconds

    # ----------------------------------------------------------------------
    def __init__(self, beamline_hal=None, filename="", name="",):
        """
        """
        super().__init__()

        self.filename = filename
        self.name = name

        self.beamline_hal = beamline_hal

        self.motor_items = []           # list of tuples
   
        self.date_time = ""

        if self.filename:
            self.load(self.filename)    # can throw

        self.break_loop = False
        self.state = "idle"

        self.exc_type = None
        self.exc_value = None
    
    # ----------------------------------------------------------------------
    def add_item(self, device_name, motor_name, position, step_number):
        """
        """
        self.motor_items.append([device_name, motor_name, position, step_number])

    # ----------------------------------------------------------------------
    def update_position(self):
        for item in self.motor_items:
            full_name = f"{item[0]}/{item[1]}"
            item[2] = self.beamline_hal.motor_position(full_name)

    # ----------------------------------------------------------------------
    def validate(self):
        """Check if motors from this snapshot can be moved to requested target
        positions.
        """
        for item in self.motor_items:
            full_name = f"{item[0]}/{item[1]}"
            target_pos = float(item[2])

            flag, msg = self.beamline_hal.is_move_valid(full_name, target_pos)
            if not flag:
                logger.error(msg)
                raise RuntimeError(msg)
  
    # ----------------------------------------------------------------------
    def run(self):
        """Move motors to positions save in the snapshot.
        """
        try:
            self._execute()

        except Exception as exc:
            self.exc_type, self.exc_value = sys.exc_info()[:2]   # for thread's caller
            logger.exception(exc)
            raise

    # ----------------------------------------------------------------------
    def _execute(self):
        """
        """
        self.break_loop = False
        self.state = "running"

        logger.info(f"Moving to snapshot {self.name}")

        move_groups = {}
        for item in self.motor_items:
            step = item[3]

            if not step in move_groups:
                move_groups[step] = []

            move_groups[step].append(item[:3])

            # move motors in groups
        for group_idx, move_group in list(move_groups.items()):
            logger.debug(f"START mv group {group_idx}")
            
            n_motors = len(move_group)
            for motor_idx in range(n_motors):
                dev_name, motor_name, position = move_group[motor_idx]
      
                    # TODO 
                    # all motors or none should be moved! 
                try:
                    full_name = f"{dev_name}/{motor_name}"
                    self.beamline_hal.move_motor(full_name, position,
                                                 "absolute", "snapshot")
        
                except RuntimeError as err:   #, PyTango.DevFailed) as err:
                    self.beamline_hal.group_action("stop_motors")
                    raise       # requires more work if one wants to transfer exception to higher level TODO
      
            while True:
                time.sleep(self.REFRESH_RATE)

                if self.break_loop:
                    self.set_state("finished")
                    return

                if self.state in ["idle", "paused"]:
                    logger.debug(f"snapshot state {self.state}")
                    continue

                    # wait until all motors are moved to target positions
                n_finished = 0
                for motor_idx in range(n_motors):  
                    full_name = f"{dev_name}/{motor_name}"
                    dev_name, motor_name = move_group[motor_idx][:2]

                    if self.beamline_hal.motor_state(full_name) != "moving":
                        n_finished += 1
       
                if n_finished == n_motors:
                    logger.debug(f"group {group_idx} finished")
                    break
    
        self.set_state("finished")

        logger.info(f"Snapshot {self.name} completed")

    # ----------------------------------------------------------------------
    def abort(self):
        """
        """
        self.break_loop = True
        self.set_state("finished")

    # ----------------------------------------------------------------------
    def pause(self):
        """
        """
            #self.pause_movement() TODO
        self.set_state("paused")

    # ----------------------------------------------------------------------
    def resume(self):
        """
        """
        self.set_state("running")

    # ----------------------------------------------------------------------
    def load(self, filename):
        """Load snapshot from a given file.
    
        Args:
            filename (str)
        """
        self._reset()

        self.filename = str(filename)
        with open(self.filename) as f:
            content = f.read()
   
        dom = parseString(content)        # DOM
      
        nodes = dom.getElementsByTagName("beamline_snapshot") 
        try:
            root_node = nodes[0]

            self.name = root_node.getAttribute("name")
            self.date_time = root_node.getAttribute("datetime")

            item_nodes = root_node.getElementsByTagName("item")

            for item in item_nodes:
                device_name = item.getAttribute("device_name")
                motor_name  = item.getAttribute("motor_name")
                position    = float(item.getAttribute("target_position"))
                step_number = int(item.getAttribute("step_number"))
        
                self.add_item(device_name, motor_name, position, step_number) 
    
        except Exception as err:
            self.exc_type, self.exc_value = sys.exc_info()[:2]
     
        return len(self.motor_items) > 0

    # ----------------------------------------------------------------------
    def save(self, filename=""):
        """
        """
        if filename:
            self.filename = str(filename)

        doc = Document()

        root_node = doc.createElement("beamline_snapshot")
        doc.appendChild(root_node)
        root_node.setAttribute("name", self.name)
      
        self.date_time = datetime.now().strftime(self.TIME_STAMP_FMT)
        root_node.setAttribute("datetime", self.date_time)

        for item in self.motor_items:
            node = doc.createElement("item")
            root_node.appendChild(node)
      
            node.setAttribute("device_name", str(item[0]))
            node.setAttribute("motor_name", str(item[1]))
            node.setAttribute("target_position", str(item[2]))
            node.setAttribute("step_number", str(item[3]))

        with open(self.filename, "w") as f:
            f.write(doc.toprettyxml(indent="  "))

    # ----------------------------------------------------------------------
    def last_exception(self):
        """
        """
        exc_type, exc_value = self.exc_type, self.exc_value
        self.exc_type, self.exc_value = None, None

        return exc_type, exc_value

    # ----------------------------------------------------------------------
    def empty(self):
        """
        """
        return len(self.motor_items) < 1

    # ----------------------------------------------------------------------
    def set_state(self, new_state):
        """
        """
        self.state = new_state

    # ----------------------------------------------------------------------
    def _reset(self):
        """
        """
        self.filename = ""
        self.name = ""
        self.motor_items = []
   
        self.exc_value = None
        self.exc_type = None
    
        self.date_time = ""

        self.break_loop = False
        self.state = "idle"

    # ----------------------------------------------------------------------
    @staticmethod
    def is_valid_name(snapshot_name):
        """Validate given snapshot name.

        Returns:
            (bool)
        """
        if not snapshot_name:
            return False

        if 'global' in snapshot_name:
            return False
        
        return re.match(r"^[a-zA-Z0-9_\-=]+$", snapshot_name) is not None

