# TraceColor

A lightweight, colorized Python logger with TRACE and PROGRESS level support.

## Features

- Custom TRACE logging level (lower than DEBUG)
- Custom PROGRESS logging level (between DEBUG and INFO)
- Colorized output for different log levels
- Rate-limiting for PROGRESS messages (once per second)
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
logger.progress("Progress update information (rate-limited)")
logger.debug("Debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error")
```

## Color Scheme

- TRACE: Gray (dim white)
- PROGRESS: Blue
- DEBUG: Cyan
- INFO: Green
- WARNING: Yellow
- ERROR: Red
- CRITICAL: Bold Red

## License

MIT