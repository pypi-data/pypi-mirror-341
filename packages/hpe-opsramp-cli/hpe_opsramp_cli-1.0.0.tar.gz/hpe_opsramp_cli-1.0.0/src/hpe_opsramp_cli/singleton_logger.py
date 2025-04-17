import logging
import logging.config
import threading
from typing import Optional

# import logging.Logger

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "opsramp-cli.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
        },
        "my_module": {  # custom logger for a specific module
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


class SingletonLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SingletonLogger, cls).__new__(cls)
                    cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)

    def get_logger(self, log_level:  Optional[str]  = "INFO") -> logging.Logger:
        if log_level:
            log_level = getattr(logging, log_level.upper(), None)
            if not isinstance(log_level, int):
                raise ValueError(f"Invalid log level: {log_level}")
            self.logger.setLevel(log_level)
            # self.logger.info("Logging level set to %s", log_level)

        return self.logger
