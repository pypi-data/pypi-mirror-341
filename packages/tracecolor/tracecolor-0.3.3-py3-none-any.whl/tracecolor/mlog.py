import logging
import colorlog
import time

class MLog(logging.Logger):
    """
    Enhanced logger with colorized output and TRACE level.
    
    Features:
    - Custom TRACE logging level (lower than DEBUG)
    - Colorized output for different log levels
    - Rate-limiting for TRACE messages (once per second)
    - Timestamped log format
    
    Usage:
    ```python
    from tracecolor import MLog
    
    logger = MLog(__name__)
    logger.trace("Detailed trace message")
    logger.debug("Debug information")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical error")
    ```
    """
    TRACE_LEVEL = 5  # TRACE below DEBUG (10)
    SLOW_TRACE_LEVEL = 15  # SLOW_TRACE between DEBUG (10) and INFO (20)

    def __init__(self, name):
        super().__init__(name)

        # Register custom levels
        logging.addLevelName(self.TRACE_LEVEL, "TRACE")
        logging.addLevelName(self.SLOW_TRACE_LEVEL, "SLOW_TRACE")

        # Set up color formatter for standard log levels
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname).1s%(reset)s |%(asctime)s.%(msecs)03d| %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
                'TRACE': 'white',
                'SLOW_TRACE': 'white',
            }
        )

        # Console handler for standard log levels
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # Set the logger level to the lowest to capture all messages
        self.setLevel(self.TRACE_LEVEL)
        self.propagate = False

        # Initialize last log time for rate-limiting
        self._last_trace_log_time = 0

    def trace(self, message, *args, **kwargs):
        """Log a message with severity 'TRACE'."""
        if self.level <= self.TRACE_LEVEL:
            self.log(self.TRACE_LEVEL, message, *args, **kwargs)

    def slow_trace(self, message, *args, **kwargs):
        """Log a message with severity 'STRACE' (for very frequent logs)."""
        if self.level <= self.SLOW_TRACE_LEVEL:
            current_time = time.time()
            # Rate-limiting: Log only if a second has passed since the last log
            if current_time - self._last_trace_log_time >= 1:
                self._last_trace_log_time = current_time
                self.log(self.SLOW_TRACE_LEVEL, message, *args, **kwargs)
    
    def debug(self, message, *args, **kwargs):
        """Log a message with severity 'DEBUG'."""
        if self.level <= logging.DEBUG:
            super().debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log a message with severity 'INFO'."""
        if self.level <= logging.INFO:
            super().info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log a message with severity 'WARNING'."""
        if self.level <= logging.WARNING:
            super().warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log a message with severity 'ERROR'."""
        if self.level <= logging.ERROR:
            super().error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log a message with severity 'CRITICAL'."""
        if self.level <= logging.CRITICAL:
            super().critical(message, *args, **kwargs)

# Monkey-patching removed as methods are defined in MLog class
