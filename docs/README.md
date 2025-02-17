# OpenTelemetry Integration with Django for SigNoz Monitoring

This guide provides step-by-step instructions for setting up OpenTelemetry in a Django application to send traces, logs, and metrics to SigNoz for observability. It includes the setup for distributed tracing, logging, and metrics collection with SigNoz as the monitoring tool.

---

## Prerequisites

Before we begin, ensure you have the following:

- A **Django** application set up and running.
- **SigNoz** installed and running locally or in the cloud.
- Python 3.6+ installed on your system.
- Required Python packages (`opentelemetry-sdk`, `opentelemetry-exporter-otlp`, etc.) installed.

---

## Steps to Set Up OpenTelemetry with Django

### 1. Install the Required Python Packages

First, install the necessary OpenTelemetry packages for Django:

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-django \
    opentelemetry-instrumentation-logging opentelemetry-exporter-otlp opentelemetry-instrumentation-psycopg2 \
    opentelemetry-sdk-metrics opentelemetry-exporter-otlp-metrics
```

These packages provide:
- **Django instrumentation**: To automatically trace requests, views, and database queries.
- **Logging instrumentation**: To capture logs.
- **Metrics instrumentation**: To gather custom metrics.
- **OTLP exporters**: To send data to SigNoz.

---

### 2. Set Up OpenTelemetry in `manage.py`

The first step in configuring OpenTelemetry is to set it up in your Django application. OpenTelemetry is initialized in the `manage.py` file where we configure the trace, logging, and metric exporters.

Here's how to modify your `manage.py` file:

```python
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
```

### Key Sections Explained:
1. **Tracing**: 
   - Sets up the **OTLP exporter** to send traces to SigNoz.
   - Creates a **TracerProvider** with a `service.name` resource to identify the application in SigNoz.

2. **Logging**:
   - Configures the **OTLP log exporter** to send logs to SigNoz.
   - Adds a **logging handler** to capture log data and forward it to SigNoz.

3. **Metrics**:
   - Sets up a **metric provider** and **periodic exporting** to send metrics data to SigNoz.

4. **Instrumenting Django**:
   - Automatically instruments Django views and database queries.
   - Also instruments **logging** and **PostgreSQL queries** using `Psycopg2Instrumentor`.

---

### 3. Configure SigNoz

Ensure that **SigNoz** is properly set up and running on your local machine or cloud environment. SigNoz should be accessible at `http://localhost:4318/` (or your configured endpoint). If you haven't set up SigNoz, you can follow their [installation guide](https://signoz.io/docs/install/).

- **Traces** should be available at `http://localhost:4318/v1/traces`.
- **Logs** should be available at `http://localhost:4318/v1/logs`.
- **Metrics** should be available at `http://localhost:4318/v1/metrics`.

---

### 4. Run Your Django Application

With the configuration in place, you can now run your Django application:

```bash
python manage.py runserver
```

Your Django application will now send traces, logs, and metrics to SigNoz. You should be able to view these in the SigNoz dashboard.

---

## Observing Your Data in SigNoz

Once the Django app is running and generating data, you can access the SigNoz dashboard:

1. **Traces**: Navigate to the **Traces** section to view request traces and the performance of your application. Look for the `vibes-django-app` service name to filter relevant traces.
2. **Logs**: Go to the **Logs** section to view the logs captured from your Django application.
3. **Metrics**: Check the **Metrics** section for any custom or default metrics you've configured in your app.

---

## Additional Customization

### Adding Custom Metrics

You can create and export custom metrics to SigNoz for more fine-grained monitoring. For example, to create a counter for HTTP requests:

```python
from opentelemetry.metrics import get_meter

meter = get_meter("vibes-django-app")
request_counter = meter.create_counter("http_requests_total", description="Total number of HTTP requests")

def my_view(request):
    request_counter.add(1)  # Increments the counter each time the view is called
    return HttpResponse("Hello, World!")
```

### Logging


### Error Monitoring

To capture and monitor errors, you can send custom exceptions or error logs to SigNoz:

```python
try:
    # Some risky operation
    pass
except Exception as e:
    logging.error(f"Error occurred: {e}")
```

This will send the error logs to SigNoz, allowing you to track error rates and investigate issues in your application.

---

## Troubleshooting

1. **SigNoz Not Receiving Data**:
   - Ensure SigNoz is running and accessible at the specified endpoint.
   - Check the OpenTelemetry exporter endpoints (`http://localhost:4318/v1/traces`, etc.).
   - Verify that your service name matches the one configured in SigNoz.

2. **Missing Metrics or Logs**:
   - Ensure that the metrics and logs are being sent to SigNoz by confirming that the `LoggingHandler` and `MetricReader` are set up correctly.
   - Check the OpenTelemetry SDK documentation for additional configuration options.

---

## Conclusion

By following this guide, you've successfully integrated OpenTelemetry with your Django application to send tracing, logging, and metrics to SigNoz. This provides end-to-end observability, helping you monitor and debug your application effectively.

For more details on OpenTelemetry, visit the [official documentation](https://opentelemetry.io/docs/). For SigNoz setup and features, refer to the [SigNoz documentation](https://signoz.io/docs/).