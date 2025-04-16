"""Wrapper around CFG files parser
"""

import configparser


# ----------------------------------------------------------------------
class Settings:

    # ----------------------------------------------------------------------
    def __init__(self, filename):
        """
        Args:
            str
        """
        self._config_parser = configparser.ConfigParser()
        
        self.filename = str(filename)
        if self.filename:
            self.load_file(filename)

    # ----------------------------------------------------------------------
    def load_file(self, filename):
        """
        Args:
            str, config file name
        """
        self._config_parser.read(filename)

    # ----------------------------------------------------------------------
    def option(self, section, option):
        """
        Args:
            str, section id
            str, option id
        """
        return self._config_parser.get(section, option)

    # ----------------------------------------------------------------------
    def getDict(self, section):
        """
        Args:
            str, section id
        """
        return self._config_parser._sections[section]

    # ----------------------------------------------------------------------
    def saveOption(self, section, option, value):

        self._config_parser[section][option] = value  # update

        with open(self.filename, 'w') as configfile:  # save
            self._config_parser.write(configfile)

    # ----------------------------------------------------------------------
    def saveOptionSet(self, section, options_values):

        for option, value in list(options_values.items()):
            self._config_parser.set(section, option, value)

        with open(self.filename, 'w') as configfile:  # save
            self._config_parser.write(configfile)


