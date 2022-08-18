import sys
from loguru import logger as _logger


class CoreApplication:
    """Contains implementation-specific application structures, such as configuration"""

    def __init__(self, name: str):
        """Initialize the application"""

        # Set up logging
        _logger.remove()
        _logger.add(sys.stderr,
                    colorize=True,
                    format="<green>{time:MMM/DD/YYYY HH:mm:ss}</green>"
                           " | <cyan>{extra[name]}</cyan>"
                           " | <level>{level: <8}</level>"
                           " | <level>{message}</level>")

        self.logger = _logger.bind(name=name)
        self.logger.info("Starting Parthenon...")

        # Read configuration
        self.logger.warning("TODO: read config from file")
