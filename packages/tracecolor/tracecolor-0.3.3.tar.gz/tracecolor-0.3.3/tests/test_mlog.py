import pytest
import logging
from tracecolor import MLog
import io
import sys
import re

def test_mlog_creation():
    """Test basic logger creation."""
    logger = MLog("test_logger")
    assert isinstance(logger, MLog)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"

def test_log_levels():
    """Test all log levels are properly defined."""
    logger = MLog("test_logger")
    assert logger.TRACE_LEVEL == 5
    assert logging.getLevelName(logger.TRACE_LEVEL) == "TRACE"
    assert logger.SLOW_TRACE_LEVEL == 15
    assert logging.getLevelName(logger.SLOW_TRACE_LEVEL) == "SLOW_TRACE"
    
    # Test standard levels still work
    assert logger.level <= logging.DEBUG
    assert logger.level <= logging.INFO
    assert logger.level <= logging.WARNING
    assert logger.level <= logging.ERROR
    assert logger.level <= logging.CRITICAL

def test_log_output(capsys):
    """Test that log messages are properly formatted."""
    # Redirect stdout to capture log messages
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        logger = MLog("test_output")
        logger.info("Test info message")
        
        # Use capsys to capture stderr (where logging outputs by default)
        captured = capsys.readouterr()
        output = captured.err
        # Remove ANSI color codes for assertion
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        clean_output = ansi_escape.sub('', output)
        # Check for basic format
        assert "I |" in clean_output
        assert "Test info message" in clean_output
        
        # Check timestamp format using regex
        timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"
        assert re.search(timestamp_pattern, output) is not None
        
    finally:
        sys.stdout = old_stdout

def test_slow_trace_rate_limiting():
    """Test that slow_trace messages are rate-limited."""
    logger = MLog("test_rate_limit")
    
    # Capture all handler calls
    calls = []
    
    class MockHandler(logging.Handler):
        def emit(self, record):
            calls.append(record)
    
    mock_handler = MockHandler()
    logger.handlers = [mock_handler]  # Replace the default handler
    
    # Two immediate slow_trace calls should result in only one log
    logger.slow_trace("First slow_trace message")
    logger.slow_trace("Second slow_trace message")
    
    assert len(calls) == 1

@pytest.mark.parametrize("set_level,expected_levels", [
    (MLog.SLOW_TRACE_LEVEL, ["SLOW_TRACE", "INFO", "WARNING", "ERROR", "CRITICAL"]), # SLOW_TRACE is 15
    (MLog.TRACE_LEVEL, ["TRACE", "DEBUG", "SLOW_TRACE", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    (logging.DEBUG, ["DEBUG", "SLOW_TRACE", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    (logging.INFO, ["INFO", "WARNING", "ERROR", "CRITICAL"]),
    (logging.WARNING, ["WARNING", "ERROR", "CRITICAL"]),
    (logging.ERROR, ["ERROR", "CRITICAL"]),
    (logging.CRITICAL, ["CRITICAL"]),
])
def test_log_level_filtering(set_level, expected_levels, capsys):
    logger = MLog("test_level_filter")
    logger.setLevel(set_level)
# Restore original colorlog formatter usage
# standard_formatter = logging.Formatter("%(levelname).1s |%(asctime)s.%(msecs)03d| %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# original_handlers = list(logger.handlers)
# for handler in logger.handlers:
#     handler.setFormatter(standard_formatter)
    
        
    # Map level names to log calls
    log_calls = [
        ("SLOW_TRACE", lambda: logger.slow_trace("slow_trace message")),
        ("TRACE", lambda: logger.trace("trace message")),
        ("DEBUG", lambda: logger.debug("debug message")),
        ("INFO", lambda: logger.info("info message")),
        ("WARNING", lambda: logger.warning("warning message")),
        ("ERROR", lambda: logger.error("error message")),
        ("CRITICAL", lambda: logger.critical("critical message")),
    ]
    
    # Patch time to avoid rate-limiting for SLOW_TRACE
    import time as _time
    orig_time = _time.time
    _time.time = lambda: 0
    try:
        # Ensure SLOW_TRACE is not rate-limited by resetting _last_trace_log_time
        logger._last_trace_log_time = -1000
        for idx, (level, call) in enumerate(log_calls):
            if level == "SLOW_TRACE": # Only SLOW_TRACE has rate-limiting now
                logger._last_trace_log_time = -1000
            call()
    finally:
        _time.time = orig_time
        # No need to restore formatters now
        # for i, handler in enumerate(logger.handlers):
        #      if i < len(original_handlers):
        #          handler.setFormatter(original_handlers[i].formatter)

    captured = capsys.readouterr().err
    # Remove ANSI color codes for assertion
    import re
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    clean_captured = ansi_escape.sub('', captured)
    for level, _ in log_calls:
        if level in expected_levels:
            # Adjust assertion for STRACE first letter
            expected_char = level[0] if level != "SLOW_TRACE" else "S"
            assert f"{expected_char} |" in clean_captured
        else:
            expected_char = level[0] if level != "SLOW_TRACE" else "S"
            assert f"{expected_char} |" not in clean_captured