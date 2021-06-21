import os
import logging
import time


class LogHandler(logging.FileHandler):
    """
    :Class Name     : LogHandler
    :Description    : log handler to generate file path
    """
    def __init__(self, logdirectory, filename, level=logging.DEBUG):
        """
        :Function Name      : __init__
        :param logdirectory : contains the name of the log directory
        :param filename     : contains the name of the file
        :param level        : log level to be set
        """
        logdirectory = os.path.abspath(logdirectory)
        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)
        filename = self.generate_filepath(logdirectory, filename)
        logging.FileHandler.__init__(self, filename)
        self.setLevel(level)
        self.setFormatter(FileFormat())

    @classmethod
    def generate_filepath(cls, logdirectory, filename='lcioutput.log'):
        """
        :Function Name      : generate_filepath
        :param logdirectory : name of the log directory
        :param filename     : name of the file
        :return:
        """
        return os.path.join(logdirectory, filename)


class StdFormatter(logging.Formatter):
    """
    :Class Name     : StdFormatter
    :Description    : class to set the format of the logs captured
    """
    std_format = '[%(name)s] %(funcName)s %(lineno)s %(levelname)s %(message)s'

    def __init__(self):
        logging.Formatter.__init__(self, self.std_format)


class ColorFormatter(StdFormatter):
    """
    :ClassName      : ColorFormatter
    :Description    : setting the colour for log level
    :return         : None
    """
    std_format = ('%(bold_cyan)s[%(name)s]%(normal)s %(level_color)s'
                  '%(levelname)s%(normal)s %(message)s')

    def __init__(self, terminal):
        """
        :Function Name  : __init__
        :Description     : function to initialize the colour for log level
        :param terminal : terminal value
        :return         : None
        """
        self.colors = {
            'DEBUG': terminal.magenta,
            'INFO': terminal.green,
            'WARNING': terminal.red,
            'ERROR': terminal.white_on_red,
            'CRITICAL': terminal.bold_white_on_red,
        }
        self.bold_cyan = terminal.bold_cyan
        self.normal = terminal.normal
        StdFormatter.__init__(self)

    def format(self, record):
        """
        :Function Name  : format
        :Description    : function to set the colour for record
        :param record   : record
        :return         : None
        """
        record.level_color = self.colors.get(record.levelname)
        record.bold_cyan = self.bold_cyan
        record.normal = self.normal
        return logging.Formatter.format(self, record)


class FileFormat(StdFormatter):
    """
    :Class Name     : FileFormat
    :Description    : class to set the format of the log file
    """
    std_format = '%(asctime)s: [%(name)s] [%(funcName)s] [%(lineno)s] [%(levelname)s] %(message)s'
    
    def formatTime(self, record, datefmt=None):
        """
       :Function Name      : formatTime
       :Description        : function to set the format of the date and time
       :param record       : record
       :param datefmt      : format of date and time
       :return             : format of the date and time
       """
        if datefmt:
            s = StdFormatter.formatTime(self, record, datefmt)
        else:
            time_struct = self.converter(record.created)
            # msecs isn't available in time_struct so inject them manually
            s = time.strftime(
                "%Y-%m-%d %H:%M:%S.{:03.0f} %Z".format(record.msecs),
                time_struct)
        return s
