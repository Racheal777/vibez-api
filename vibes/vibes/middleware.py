from opentelemetry.metrics import get_meter

meter = get_meter("vibes-django-app")
request_counter = meter.create_counter("http_requests_total", description="Total number of HTTP requests")


class RequestCounterMiddleware:
    """Middleware to count all incoming HTTP requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_counter.add(1)  # Increment counter for each request
        response = self.get_response(request)
        return response
