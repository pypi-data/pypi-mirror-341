# tests/test_logger.py
#from log.logger import log_info, log_warn, log_error, log_debug
from minakicoin.log.logger import log_info, log_warn, log_error, log_debug

def test_logging():
    log_info("✅ This is info")
    log_warn("⚠️ This is a warning")
    log_error("❌ This is an error")
    log_debug("🐞 This is debug")
