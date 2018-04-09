# !/usr/bin/python
from configparser import ConfigParser
import logging
import os
import sys

logging.getLogger(__name__)


def config(section):
    filename = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/configuration.ini'
    # create a parser
    parser = ConfigParser()
    # read config file
    logging.info('Get params from ' + filename)
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise logging.info(str(Exception('Section {0} not found in the {1} file'.format(section, filename))))

    return db
