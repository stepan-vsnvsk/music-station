import logging
from util.json_util import JsonUtils


class Logger:
    """Wrapper class for logging

    '_logger' - access point to (singletone) logging instance.
    """

    _logger = logging.getLogger("logger")
    logger_config = JsonUtils.read_from_json('config_logger.json')
    logging.basicConfig(level=logging.INFO,
                        filemode=logger_config['filemode'],
                        format=logger_config['format'])

    @staticmethod
    def set_file_handler(name):
        """FileHandler initialization.

        Create FileHandler with a proper name and add it
        to a logger instance.

        Args:
            name(str): name of test function/class from conftest file
        """
        filename = Logger.logger_config['path'] + name + '.log'  # name by test method (fixture)
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        Logger._logger.addHandler(file_handler)

    @staticmethod
    def set_level(level):
        """Set level for logging."""
        Logger._logger.setLevel(level)

    @staticmethod
    def get_logger():
        """Get logging instance"""
        return Logger._logger

    @staticmethod    
    def info(message):
        """Wrapper for logging.info."""
        Logger._logger.info(msg=message)

    @staticmethod    
    def debug(message):
        """Wrapper for logging.debug."""
        Logger._logger.debug(msg=message)

    @staticmethod    
    def warning(message):
        """Wrapper for logging.warning."""
        Logger._logger.warning(msg=message)

    @staticmethod    
    def error(message):
        """Wrapper for logging.error."""
        Logger._logger.error(msg=message)
