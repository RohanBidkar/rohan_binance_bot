import logging
from logging.handlers import RotatingFileHandler


LOG_FILE = "bot.log"

logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)


logger.propagate= False
logger.handlers.clear()



file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 *1024 *1024, # 5 mb 
        backupCount=3
    )

formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)