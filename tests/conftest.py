import logging
import warnings

from loguru import logger


# Forward Loguru to the standard logging system
class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PropagateHandler(), level="INFO")
logger.info("loguru INFO messages passed to standard logging for pytests")

logger.add(PropagateHandler(), level="DEBUG")
logger.info("loguru DEBUG messages passed to standard logging for pytests")

# Forward every WARNING‐level log to the Python warnings subsystem
logger.add(
    warnings.warn,  # the sink
    format="{message}",  # plain message text
    level="WARNING",  # only WARNING and above
    filter=lambda r: r["level"].name == "WARNING",  # safety net
)
logger.info("loguru WARNING messages passed to the warnings module for pytests")
