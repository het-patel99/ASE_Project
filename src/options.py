import re
import sys
from utils import coerce


class Options:
    def __init__(self):
        self.options_dict = {}
        self.conversions_dict = {}

    def parse_cli_settings(self, help_string):
        """
        Parses command-line interface (CLI) settings from the help string.
        """
        regex = "\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)"
        settings = re.findall(regex, help_string)
        self.conversions_dict = {k: v for v, k in re.findall(
            "\n[\s]+[-]([\S]+)[\s]+[-][-]([\S]+)[^\n]+= [\S]+", help_string)}

        for key, value in settings:
            self.options_dict[key] = coerce(value)

        for key, value in self.options_dict.items():
            value_str = str(value)
            for index, arg in enumerate(sys.argv):
                if arg == "-" + key[0] or arg == "--" + key or arg == '-' + self.conversions_dict[key]:
                    value_str = (sys.argv[index + 1] if index + 1 < len(
                        sys.argv) else False) or value_str == "False" and "true" or value_str == "True" and "false"
                self.options_dict[key] = coerce(value_str)

    def items(self):
        """
        Returns a list of key-value pairs of all options.
        """
        return self.options_dict.items()

    def __getitem__(self, key):
        """
        Returns the value for the specified option key.
        """
        return self.options_dict[key]

    def __setitem__(self, key, value):
        """
        Sets the value for the specified option key.
        """
        self.options_dict[key] = value


options = Options()