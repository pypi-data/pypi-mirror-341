import logging
import logging.config

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


class CLILogger:

    def __init__(self, name: str):
        self.get_logger(name)

    def get_logger(self, name: str = "") -> logging.Logger:
        if hasattr(self, "logger"):
            return self.logger
        else:
            logging.config.dictConfig(LOGGING_CONFIG)
            self.logger = logging.getLogger(name)
            return self.logger

    def set_level(self, log_level: str):
        log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(log_level, int):
            raise ValueError(f"Invalid log level: {log_level}")
        self.logger.setLevel(log_level)
        self.logger.info("Logging level set to %s", log_level)
