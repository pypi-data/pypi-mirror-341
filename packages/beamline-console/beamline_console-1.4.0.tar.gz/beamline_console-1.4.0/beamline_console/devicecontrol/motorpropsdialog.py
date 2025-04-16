"""Basic motor's properties show/edit dialog.
"""

import math
import subprocess

from PyQt5 import QtWidgets, QtCore

from beamline_console.logger.logit import Logit
from beamline_console.gui.MotorPropsDialog_ui import Ui_MotorPropsDialog


# ---------------------------------------------------------------------- 
class MotorPropsDialog(QtWidgets.QDialog, Logit):
    """
    """

    VALIDATOR_REFRESH = 500               # ms
    EPSILON = 1e-8

    NORMAL_STYLE = "QLineEdit {background-color: white};"
    ERROR_STYLE = "QLineEdit {background-color: #FFC4C4};"
    CHANGED_STYLE = "QLineEdit {background-color: #FFFCC4};"

    PARAMS_EDITOR = "atkpanel"

    # ---------------------------------------------------------------------- 
    def __init__(self, motor, parent=None):
        """
        Args:
            motor (see beamlinehal/motor)
        """
        QtWidgets.QDialog.__init__(self, parent)
        Logit.__init__(self)

        self._motor = motor             # HAL handle

        self._ui = Ui_MotorPropsDialog()
        self._ui.setupUi(self)
      
        self._ui.btnSaveProps.clicked.connect(self._saveProperties)
        self._ui.btnCalibrate.clicked.connect(self._calibrateMotorPosition)
        self._ui.btnUndo.clicked.connect(self._undoChanges)
        self._ui.btnAllParams.clicked.connect(self._editAllParams)
   
            # backup current values
        self._conversionBak = self._motor.parameter("Conversion")
        self._slewRateBak = self._motor.parameter("SlewRate")
        self._accelerationBak = self._motor.parameter("Acceleration")
        self._backlashBak = self._motor.parameter("StepBacklash")
    
        self._lowLimitBak = self._motor.parameter("UnitLimitMin")
        self._highLimitBak = self._motor.parameter("UnitLimitMax")
        self._decimalsBak = self._motor.decimals


        self._baseRateBak = self._motor.parameter("BaseRate")

            # user limits (on top of TANGO)
        self._lowLimitUserBak = self._motor.user_low_limit
        self._highLimitUserBak = self._motor.user_high_limit

        self._ui.chbUserLimits.toggled.connect(self._enableUserLimits)
        self._ui.chbUserLimits.setChecked(bool(self._motor.user_low_limit and
                                               self._motor.user_high_limit))
        self._refreshGui()

        self._validatorTimer = QtCore.QTimer(self)
        self._validatorTimer.timeout.connect(self._maybeColor)
        self._validatorTimer.start(self.VALIDATOR_REFRESH)
        
            # in case of multiple screens center on the primary one
        frame = self.frameGeometry()

        desktop = QtWidgets.QApplication.desktop()
        idxPrimary = desktop.primaryScreen()
        centerPoint = desktop.screenGeometry(idxPrimary).center()
        
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())

        #self.setModal(True)

    # ---------------------------------------------------------------------- 
    def _refreshGui(self):
        """
        """
        self._ui.lbMotorName.setText(str(self._motor.name))
        self._ui.lbTangoServer.setText(str(self._motor.tango_server))

        self._ui.leConversion.setText("{:.2f}".format(self._motor.parameter("Conversion")))
        self._ui.leCalibration.setText("0.0")
    
        self._ui.leSlewRate.setText(str(self._motor.parameter("SlewRate")))
        self._ui.leAcceleration.setText(str(self._motor.parameter("Acceleration")))
        self._ui.leBacklash.setText(str(self._motor.parameter("StepBacklash")))
    
        self._ui.leLowLimit.setText("{:.2f}".format(self._motor.parameter("UnitLimitMin")))
        self._ui.leHighLimit.setText("{:.2f}".format(self._motor.parameter("UnitLimitMax")))
        self._ui.leDecimals.setText(f"{self._motor.decimals:d}")
        
        self._ui.leBaseRate.setText("{:.2f}".format(self._motor.parameter("BaseRate")))

        if (self._motor.user_low_limit and
            self._motor.user_high_limit):
            self._ui.leLowLimitUser.setText(f"{self._motor.user_low_limit:.2f}")
            self._ui.leHighLimitUser.setText(f"{self._motor.user_high_limit:.2f}")

        self._ui.frameUserLimits.setEnabled(self._ui.chbUserLimits.isChecked())

    # ---------------------------------------------------------------------- 
    def _saveProperties(self):
        """Validate user input and save changes to the TANGO database.
        """
        try:
            self._motor.set_parameter("Conversion", float(self._ui.leConversion.text()))
            self._motor.set_parameter("SlewRate", int(self._ui.leSlewRate.text()))
            self._motor.set_parameter("Acceleration", int(self._ui.leAcceleration.text()))
            self._motor.set_parameter("StepBacklash", int(self._ui.leBacklash.text()))
    
            self._motor.set_parameter("UnitLimitMin", float(self._ui.leLowLimit.text()))
            self._motor.set_parameter("UnitLimitMax", float(self._ui.leHighLimit.text()))
            self._motor.decimals = int(self._ui.leDecimals.text())

            if self._ui.chbUserLimits.isChecked():
                self._motor.user_low_limit =  float(self._ui.leLowLimitUser.text())
                self._motor.user_high_limit = float(self._ui.leHighLimitUser.text())
            else:
                self._motor.user_low_limit =  None
                self._motor.user_high_limit = None
            
            self._motor.set_parameter("BaseRate", float(self._ui.leBaseRate.text()))

            self.logger.info(f"motor {self._motor.name} properties changed!")

        except ValueError as err:
            self.logger.warning(f"{err}")
            QtWidgets.QMessageBox.warning(self, "Experiment Control",
                                      f"Exception: {str(err)}", QtWidgets.QMessageBox.Ok)
            return
   
        self.properties_changed.emit()
    
        super().accept() 
  
    # ---------------------------------------------------------------------- 
    def _calibrateMotorPosition(self):
        """
        """
        physicalPos = float(self._ui.leCalibration.text())
        self._motor.calibrate(physicalPos)
      
        self.logger.info(f"Motor {self._motor.name} recalibrated, position {physicalPos:.2f}")

    # ----------------------------------------------------------------------
    def _editAllParams(self):
        """
        """
        subprocess.Popen([self.PARAMS_EDITOR, self._motor.tango_server])

    # ---------------------------------------------------------------------- 
    def _enableUserLimits(self, flag):
        """
        """
        self._ui.frameUserLimits.setEnabled(flag)

        if flag:
            self._ui.leLowLimitUser.setText("%.2f" % self._motor.parameter("UnitLimitMin"))
            self._ui.leHighLimitUser.setText("%.2f" % self._motor.parameter("UnitLimitMax"))
        else:
            self._ui.leLowLimitUser.clear()
            self._ui.leHighLimitUser.clear()

    # ---------------------------------------------------------------------- 
    def _maybeColor(self):
        """
        """
        self._colorLineEdit(self._ui.leConversion, self._conversionBak)
        self._colorLineEdit(self._ui.leCalibration, 0.0)
    
        self._colorLineEdit(self._ui.leSlewRate, self._slewRateBak)
        self._colorLineEdit(self._ui.leAcceleration, self._accelerationBak)
        self._colorLineEdit(self._ui.leBacklash, self._backlashBak)
    
        self._colorLineEdit(self._ui.leLowLimit, self._lowLimitBak)
        self._colorLineEdit(self._ui.leHighLimit, self._highLimitBak)

        if self._ui.chbUserLimits.isChecked():
            if not self._lowLimitUserBak:
                self._lowLimitUserBak = self._lowLimitBak
            if not self._highLimitUserBak:
                self._highLimitUserBak = self._highLimitBak

            self._colorLineEdit(self._ui.leLowLimitUser, self._lowLimitUserBak)
            self._colorLineEdit(self._ui.leHighLimitUser, self._highLimitUserBak)

    # ---------------------------------------------------------------------- 
    def _colorLineEdit(self, lineEdit, prevValue):
        """
        """
        try:
            value = float(lineEdit.text())
    
            if math.fabs(value - float(prevValue)) > self.EPSILON:
                lineEdit.setStyleSheet(self.CHANGED_STYLE)
                lineEdit.setToolTip(f"Previous value {prevValue}")
            else:
                lineEdit.setStyleSheet(self.NORMAL_STYLE)
                lineEdit.setToolTip("")

        except ValueError as err:
            lineEdit.setStyleSheet(self.ERROR_STYLE)
            lineEdit.setToolTip("Not a number")

    # ---------------------------------------------------------------------- 
    def _undoChanges(self):
        """
        """
        self._ui.leConversion.setText(f"{self._conversionBak:.2f}")
        self._ui.leCalibration.setText("0.0")

        self._ui.leSlewRate.setText(str(self._slewRateBak))
        self._ui.leAcceleration.setText(str(self._accelerationBak))
        self._ui.leBacklash.setText(str(self._backlashBak))
    
        self._ui.leLowLimit.setText(f"{self._lowLimitBak:.2f}")
        self._ui.leHighLimit.setText(f"{self._highLimitBak:.2f}")

        if self._ui.chbUserLimits.isChecked():
            if self._lowLimitUserBak and self._highLimitUserBak:
                self._ui.leLowLimitUser.setText(f"{self._lowLimitUserBak:.2f}")
                self._ui.leHighLimitUser.setText(f"{self._highLimitUserBak:.2f}")
            else:
                self._ui.leLowLimitUser.clear()
                self._ui.leHighLimitUser.clear()
 
