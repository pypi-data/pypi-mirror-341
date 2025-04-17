import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# from opentelemetry.sdk.logs import LoggingHandler


class Siva_OTEL_Logger:

    @classmethod
    def get_otel_logger(
        self,
        service_name: str,
        instrumenting_module_name: str,
        endpoint: str = "http://localhost:4317",
    ):
        # Set up the tracer provider
        # service_name= "my-python-service"
        resource = Resource(attributes={"service.name": service_name})
        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer = trace.get_tracer(instrumenting_module_name)

        # Set up the OTLP exporter
        otlp_exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        # Optionally, add a console exporter for debugging
        console_exporter = ConsoleSpanExporter()
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(console_exporter)
        )

        # Instrument logging
        LoggingInstrumentor().instrument(set_logging_format=True)

        # Configure the logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger = logging.getLogger(service_name)

        return logger

    @classmethod
    def get_jagger_logger(self):
        # Set up the tracer provider
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)

        # Set up the Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
        )
        """
         DeprecationWarning: Call to deprecated method __init__. (Since v1.35, the Jaeger supports OTLP natively. Please use the OTLP exporter instead. Support for this exporter will end July 2023.) -- Deprecated since version 1.16.0.
    jaeger_exporter = JaegerExporter(
        """

        # Set up the span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        tracer_provider.add_span_processor(span_processor)

        # Get a tracer
        tracer = trace.get_tracer(__name__)

        # Create a span
        with tracer.start_as_current_span("example-span") as span:
            span.set_attribute("example-attribute", "value")
            print("Hello, Jaeger!")

    @classmethod
    def get_jagger_logger1(cls):
        # Set up the tracer provider
        resource = Resource(attributes={"service.name": "example-service"})

        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer = trace.get_tracer(__name__)

        # Set up the span processor and exporter
        span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        trace.get_tracer_provider().add_span_processor(span_processor)

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.addHandler(LoggingHandler())

        # Example function to demonstrate logging

        with tracer.start_as_current_span("example-span"):
            logger.info("This is an info log message")
            logger.error("This is an error log message")


# Example log messages
# logging.info("This is an info message")
# logging.error("This is an error message")
