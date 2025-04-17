from hpe_opsramp_cli import cli_logger

# E   AttributeError: module 'hpe_opsramp_cli.cli_logger' has no attribute '_singleton_logger'
# logger=cli_logger._singleton_logger
logger = cli_logger.CLILogger(name=__name__)


def test_info():
    # logger = CLILogger(__name__)
    logger.get_logger().info("sivayana")


def test_debug():
    # logger = CLILogger(__name__)
    logger.get_logger().debug("sivayana")


def test_debug2():
    # logger = CLILogger(__name__)
    logger.set_level("debug")
    logger.get_logger().debug("sivayana")


def test_info2():
    # logger = CLILogger(__name__)
    logger.set_level("INFO")
    logger.get_logger().info("sivayana")
