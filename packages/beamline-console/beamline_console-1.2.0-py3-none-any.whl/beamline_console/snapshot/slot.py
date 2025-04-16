# yury.matveev@desy.de

from beamline_console.logger.logit import Logit


class Slot(Logit):

    # ----------------------------------------------------------------------
    def __init__(self, device_name, beamline_hal):
        """
        """
        super().__init__()
        self.name = device_name
        self.beamline_hal = beamline_hal
        self.logger.debug(f"Instantiating device object {device_name}")
        self.position = []
        self.snapshots = {}
        self.motors_list = []
        self.xml_node = None

        # ----------------------------------------------------------------------
    def from_xml(self, xml_node):
        """
            Load device's configuration from a given XML node.
        """
        general_access = xml_node.getAttribute('access')
        if not general_access:
            general_access = "user"

        widget = xml_node.getElementsByTagName("widget")[0]
        self.position = [int(widget.getAttribute("x")), int(widget.getAttribute("y")),
                         int(widget.getAttribute("width")), int(widget.getAttribute("height"))]

        self.xml_node = xml_node

    # ----------------------------------------------------------------------
    def list_motors(self):
        return self.motors_list

    # ----------------------------------------------------------------------
    def initialize(self):
        """
        """
        for snapshot_node in self.xml_node.getElementsByTagName("snapshot"):
            snapshot_name = str(snapshot_node.getAttribute(f"name"))
            motor_found = True
            counter = 1
            while motor_found:
                motor_name = str(snapshot_node.getAttribute(f"motor{counter}"))
                if motor_name == "":
                    motor_found = False
                    continue
                if motor_name not in self.beamline_hal.list_motors():
                    self.logger.error(f"Slot {self.name}: snapshot {snapshot_name}: motor {motor_name} not defined in BeamlineHal")
                    return False

                if motor_name not in self.motors_list:
                    self.motors_list.append(motor_name)

                counter += 1

        return True
