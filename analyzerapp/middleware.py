"""Middleware for container health checks.

The platform probes the container over its private HTTP interface. Answer this
single path before security middleware so the probe does not need a public host
header or an HTTPS redirect.
"""
from django.http import HttpResponse


class HealthcheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health":
            return HttpResponse("ok", content_type="text/plain")
        return self.get_response(request)
