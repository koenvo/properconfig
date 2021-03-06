# -*- coding: utf-8 -*-
"""
Created by @dtheodor at 2015-09-06
"""
import os
from argparse import _CountAction, _StoreConstAction
from ConfigParser import ConfigParser, DEFAULTSECT, \
    Error as ConfigParserError

from .common import ParseAttempt, failed_attempt, sources, SourceInfo


def get_local_filename(prog):
    return os.path.join(os.path.expanduser("~"), prog)

class FileSource(SourceInfo):
    source = sources.FILE
    __slots__ = ("filename", "option")

    def __init__(self, filename, option):
        self.filename = filename
        self.option = option


class FileParser(object):
    """Parses values from an .ini file.

    Uses the ConfigParser module.
    """
    def __init__(self, fp, filename=None):
        if filename is None:
            try:
                filename = fp.name
            except AttributeError:
                filename = "<Unknown filename>"
        self.filename = filename
        config = self.config = ConfigParser()
        config.readfp(fp)

    @classmethod
    def from_filename(cls, filename):
        with open(filename) as f:
            return FileParser(f, filename)

    @staticmethod
    def cli_option_to_file_option(option):
        """Turns '--my-cli-option' into 'my-cli-option'."""
        return option.lstrip("-")

    def parse(self, action):
        for string in action.option_strings:
            option = self.cli_option_to_file_option(string)
            try:
                count = 1
                # TODO: change DEFAULTSECT to program name
                if isinstance(action, _StoreConstAction):
                    value = self.config.has_option(DEFAULTSECT, option)
                    if value is False:
                        continue
                elif isinstance(action, _CountAction):
                    count = self.config.getint(DEFAULTSECT, option)
                    value = count
                else:
                    value = self.config.get(DEFAULTSECT, option)
                return ParseAttempt(
                    success=True,
                    value=[value],
                    count=count,
                    option_name=string,
                    source=FileSource(filename=self.filename,
                                      option=option))
            except ConfigParserError:
                pass
        return failed_attempt
