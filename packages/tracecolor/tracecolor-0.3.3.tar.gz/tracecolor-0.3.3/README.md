# TraceColor

A lightweight, colorized Python logger with TRACE and SLOW_TRACE level support.

## Features

- Custom TRACE logging level (lower than DEBUG)
- Custom SLOW_TRACE logging level (between DEBUG and INFO)
- Colorized output for different log levels
- Rate-limiting for SLOW_TRACE messages (once per second)
- Simple and clean API

## Installation

```bash
pip install tracecolor
```

## Usage

```python
from tracecolor import MLog

# Create a logger
logger = MLog(__name__)

# Log at different levels
logger.trace("Detailed tracing information")
logger.slow_trace("Frequent tracing information (rate-limited)")
logger.debug("Debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error")
```

## Color Scheme

- TRACE: White
- SLOW_TRACE: White
- DEBUG: Cyan
- INFO: Green
- WARNING: Yellow
- ERROR: Red
- CRITICAL: Bold Red

## License

MIT