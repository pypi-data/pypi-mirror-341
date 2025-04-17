from hpe_opsramp_cli.singleton_logger import SingletonLogger


def test_singleton_debug_log() -> None:
    logger_debug = SingletonLogger().get_logger(log_level="DEBUG")
    logger_debug.debug("Sivayanama logger_debug.debug")
    logger_debug.error("Sivayanama logger_debug.error")
    logger_debug.info("Sivayanama logger_debug.info")
    logger_debug.warning("Sivayanama logger_debug.warning")
    logger_debug.exception("Sivayanama logger_debug.exception")


def test_singleton_info_log() -> None:
    logger_info = SingletonLogger().get_logger(log_level="INFO")
    logger_info.debug("  logger_info debug Sivayanama")
    logger_info.error(" logger_info error Sivayanama")
    logger_info.info(" logger_info info Sivayanama")
    logger_info.warning(" logger_info warning Sivayanama")
    logger_info.exception("logger_info exception Sivayanama")


def test_singleton_debug_log1() -> None:
    logger_debug0 = SingletonLogger().get_logger(log_level="DEBUG")
    logger_debug = SingletonLogger().get_logger()
    logger_debug.debug("Sivayanama logger_debug.debug")
    logger_debug.error("Sivayanama logger_debug.error")
    logger_debug.info("Sivayanama logger_debug.info")
    logger_debug.warning("Sivayanama logger_debug.warning")
    logger_debug.exception("Sivayanama logger_debug.exception")
