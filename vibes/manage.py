#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry import trace, _logs
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import set_meter_provider

def setup_tracing():
    # Define the service name and resource
    resource = Resource.create({"service.name": "vibes-django-app"})  # Adjust as needed

    # Create a tracer provider with the resource
    provider = TracerProvider(resource=resource)

    # Set up an OTLP exporter to send traces to SigNoz
    exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")

    # Add a simple span processor
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    # Set the provider for OpenTelemetry
    trace.set_tracer_provider(provider)

    # Set up logging
    log_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint="http://localhost:4318/v1/logs")
    log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    _logs.set_logger_provider(log_provider)

    # Attach OpenTelemetry logs to Python logging module
    handler = LoggingHandler(level=logging.DEBUG, logger_provider=log_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)

    # Set up metrics
    metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics"))
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    set_meter_provider(meter_provider)

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vibes.settings")

    # Initialize OpenTelemetry Instrumentation
    setup_tracing()
    DjangoInstrumentor().instrument(enable_response_hook=True)
    LoggingInstrumentor().instrument()  # Ensures logging is instrumented
    Psycopg2Instrumentor().instrument()  # Instrument PostgreSQL queries

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
