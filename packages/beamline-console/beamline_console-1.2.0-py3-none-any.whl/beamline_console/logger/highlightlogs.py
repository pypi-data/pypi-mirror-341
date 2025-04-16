# yury.matveev@desy.de

from PyQt5 import QtGui, QtCore

from beamline_console.constants import DEBUG_COLOR, INFO_COLOR, WARNING_COLOR
from beamline_console.constants import ERROR_COLOR, DATE_COLOR


# ----------------------------------------------------------------------
class HighlightLogs(QtGui.QSyntaxHighlighter):

    # ----------------------------------------------------------------------
    def __init__(self, document):
        super().__init__(document)

        self.rules = []             # (pattern, style) pairs

        self._add_rule("\\bDEBUG\\b", DEBUG_COLOR)
        self._add_rule("\\bINFO\\b", INFO_COLOR)
        self._add_rule("\\bWARNING\\b", WARNING_COLOR)
        self._add_rule("\\bERROR\\b", ERROR_COLOR)

        self._add_rule("\\b[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\b", DATE_COLOR)

    # ----------------------------------------------------------------------
    def _add_rule(self, token, color):
        """
        """
        style = QtGui.QTextCharFormat()
        style.setForeground(color)
        
        self.rules.append((QtCore.QRegExp(token), style))

    # ----------------------------------------------------------------------
    def highlightBlock(self, text):
        """Highlight block of text according to defined rules
        """
        for pattern, style in self.rules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text, 0)

            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, style)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

