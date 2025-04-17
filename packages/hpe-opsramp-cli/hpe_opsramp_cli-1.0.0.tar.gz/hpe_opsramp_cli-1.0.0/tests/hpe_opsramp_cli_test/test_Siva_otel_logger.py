from hpe_opsramp_cli.otel_logger import Siva_OTEL_Logger
import rich


def test_otel_logging():
    otel_logger = Siva_OTEL_Logger()
    logger = otel_logger.get_otel_logger(
        service_name="test", instrumenting_module_name="HPE-opsramp-cli"
    )
    logger.info("sivayanama")
    logger.error("sivayanama")
    rich.print("namo kumaraya")


def test_jagger_logging():
    otel_logger = Siva_OTEL_Logger()
    otel_logger.get_jagger_logger()
    rich.print("namo kumaraya")
