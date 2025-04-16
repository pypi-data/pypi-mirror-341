"""Login dialog box. Used to switch users on-the-fly too.
"""

from PyQt5 import QtWidgets

from beamline_console.gui.InputDialog_ui import Ui_InputDialog
from beamline_console.logger.logit import Logit


# ----------------------------------------------------------------------
class InputDialog(QtWidgets.QDialog, Logit):
    """
    """

    # ----------------------------------------------------------------------
    def __init__(self, mode, super_user_password="", max_attempts=0, motor_handle=None):
        QtWidgets.QDialog.__init__(self)
        Logit.__init__(self)

        self._ui = Ui_InputDialog()
        self._ui.setupUi(self)

        self._mode = mode

        self._super_user_password = [int(d) for d in str(super_user_password)]
        self._max_attempts = max_attempts

        self._ui.lb_titel.setText("Enter superuser pin" if mode=="pin" else "New position")
        self._ui.but_punkt.setVisible(mode=="position")
        self._ui.but_sign.setVisible(mode=="position")

        self._motor_handle = motor_handle

        if mode=="position":
            self._ui.but_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                                QtWidgets.QDialogButtonBox.Ok |
                                                QtWidgets.QDialogButtonBox.Reset)
            self.new_position = motor_handle.position()
        else:
            self._ui.but_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)

        self._ui.but_box.clicked.connect(self._button_box_clicked)

        self._ui.lb_number.setText("")

        self._attempts = 0
        self._last_typed = []
        self._sign = 1

        for ind in range(10):
            getattr(self._ui, f'but_{ind}').clicked.connect(lambda state, x=ind: self._button_pressed(x))

        self._ui.but_punkt.clicked.connect(lambda: self._new_position(dot=True))
        self._ui.but_sign.clicked.connect(lambda: self._new_position(sign=True))

    # ----------------------------------------------------------------------
    def _button_box_clicked(self, button):
        role = self._ui.but_box.buttonRole(button)
        if role == QtWidgets.QDialogButtonBox.AcceptRole:
            self.apply_new_position()
        elif role == QtWidgets.QDialogButtonBox.RejectRole:
            self.reject()
        elif role == QtWidgets.QDialogButtonBox.ResetRole:
            self._new_position(clear=True)

    # ----------------------------------------------------------------------
    def _button_pressed(self, ind):
        self._last_typed.append(ind)
        if self._mode == "pin":
            self._check_pin()
        else:
            self._new_position()

    # ----------------------------------------------------------------------
    def _check_pin(self):
        if len(self._last_typed) >= len(self._super_user_password):
            if self._last_typed == self._super_user_password:
                self.accept()
            else:
                self._attempts += 1
                self._last_typed = []

                if self._attempts > self._max_attempts:
                    self.reject()

        self._ui.lb_number.setText("".join(["*" for _ in self._last_typed]))

    # ----------------------------------------------------------------------
    def _new_position(self, dot=False, clear=False, sign=False):
        if clear:
            self._last_typed = []
        elif sign:
            self._sign *= -1
        elif dot:
            if '.' not in self._last_typed:
                self._last_typed.append('.')

        value = "-" if self._sign < 0 else ""
        value += "".join([str(v) for v in self._last_typed])
        self._ui.lb_number.setText(value)

    # ----------------------------------------------------------------------
    def apply_new_position(self):
        position = "".join([str(v) for v in self._last_typed])
        try:
            self.new_position = float(position) * self._sign
            self.accept()
        except ValueError:
            self.logger.error(f"Not a number typed: {position}")
            self.reject()
