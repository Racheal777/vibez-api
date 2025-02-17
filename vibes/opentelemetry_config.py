from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor



# Set up OpenTelemetry Tracing Provider
resource = Resource.create({"service.name": "django-rest-api"})
tracer_provider = TracerProvider(resource=resource)

# Configure OTLP Exporter (Replace with your Signoz Collector URL)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Apply Django Instrumentation
DjangoInstrumentor().instrument()

# Set the global tracer provider
from opentelemetry import trace
trace.set_tracer_provider(tracer_provider)

Psycopg2Instrumentor().instrument()


#OTEL_RESOURCE_ATTRIBUTES=service.name=vibes OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317" OTEL_EXPORTER_OTLP_PROTOCOL=grpc opentelemetry-instrument python manage.py runserver
