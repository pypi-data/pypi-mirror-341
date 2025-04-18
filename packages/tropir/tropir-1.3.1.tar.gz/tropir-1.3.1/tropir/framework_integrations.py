import uuid
import logging
import contextvars

logger = logging.getLogger("tropir")

# Create a context variable for request ID
request_id_ctx_var = contextvars.ContextVar("request_id", default=None)

def setup_fastapi_logging():
    """Set up request ID tracking for FastAPI applications."""
    try:
        from fastapi import FastAPI
        from fastapi.routing import APIRoute

        # Check if already patched
        if getattr(APIRoute.get_route_handler, '_is_request_id_patched', False):
            logger.debug("APIRoute.get_route_handler already patched; skipping patch")
            return True

        original_get_route_handler = APIRoute.get_route_handler

        def custom_get_route_handler(self):
            original_handler = original_get_route_handler(self)

            async def custom_handler(request):
                token = request_id_ctx_var.set(str(uuid.uuid4()))
                try:
                    response = await original_handler(request)
                    return response
                finally:
                    request_id_ctx_var.reset(token)
            return custom_handler

        # Mark the patched function to prevent double patching
        custom_get_route_handler._is_request_id_patched = True

        APIRoute.get_route_handler = custom_get_route_handler
        logger.debug("Successfully monkey-patched APIRoute.get_route_handler for request ID injection")
        return True
    except ImportError:
        logger.debug("FastAPI not available - skipping FastAPI integration")
        return False

def setup_flask_logging():
    """Set up request ID tracking for Flask applications."""
    try:
        from flask import Flask
    except ImportError:
        logger.debug("Flask not available - skipping Flask integration")
        return False

    if getattr(Flask.__init__, '_is_request_id_patched', False):
        logger.debug("Flask.__init__ already patched; skipping patch")
        return True

    original_init = Flask.__init__

    def custom_init(self, *args, **kwargs):
        # Initialize the Flask app normally.
        original_init(self, *args, **kwargs)
        # Only patch the wsgi_app if not already patched.
        if not getattr(self.wsgi_app, '_is_request_id_patched', False):
            original_wsgi_app = self.wsgi_app

            def custom_wsgi_app(environ, start_response):
                token = request_id_ctx_var.set(str(uuid.uuid4()))
                try:
                    return original_wsgi_app(environ, start_response)
                finally:
                    request_id_ctx_var.reset(token)
            # Mark the wsgi_app wrapper as patched to prevent duplication.
            custom_wsgi_app._is_request_id_patched = True
            self.wsgi_app = custom_wsgi_app

    # Mark our custom __init__ so we don't patch twice.
    custom_init._is_request_id_patched = True
    Flask.__init__ = custom_init
    logger.debug("Successfully patched Flask.__init__ with non-duplicating request ID injection")
    return True

def setup_django_asgi_logging():
    """Set up request ID tracking for Django ASGI applications."""
    try:
        from django.core.handlers.asgi import ASGIHandler

        # Check if already patched
        if getattr(ASGIHandler.__call__, '_is_request_id_patched', False):
            logger.debug("ASGIHandler.__call__ already patched; skipping patch")
            return True

        original_asgi_call = ASGIHandler.__call__

        async def custom_asgi_call(self, scope, receive, send):
            token = request_id_ctx_var.set(str(uuid.uuid4()))
            try:
                response = await original_asgi_call(self, scope, receive, send)
                return response
            finally:
                request_id_ctx_var.reset(token)

        # Mark the patched function to avoid double patching
        custom_asgi_call._is_request_id_patched = True

        ASGIHandler.__call__ = custom_asgi_call
        logger.debug("Successfully monkey-patched ASGIHandler.__call__ for request ID injection")
        return True
    except ImportError:
        logger.debug("Django ASGIHandler not available - skipping ASGI integration")
        return False

def setup_django_wsgi_logging():
    """Set up request ID tracking for Django WSGI applications."""
    try:
        from django.core.handlers.wsgi import WSGIHandler

        # Check if already patched
        if getattr(WSGIHandler.__call__, '_is_request_id_patched', False):
            logger.debug("WSGIHandler.__call__ already patched; skipping patch")
            return True

        original_wsgi_call = WSGIHandler.__call__

        def custom_wsgi_call(self, environ, start_response):
            token = request_id_ctx_var.set(str(uuid.uuid4()))
            try:
                response = original_wsgi_call(self, environ, start_response)
                return response
            finally:
                request_id_ctx_var.reset(token)

        # Mark the patched function to avoid double patching
        custom_wsgi_call._is_request_id_patched = True

        WSGIHandler.__call__ = custom_wsgi_call
        logger.debug("Successfully monkey-patched WSGIHandler.__call__ for request ID injection")
        return True
    except ImportError:
        logger.debug("Django WSGIHandler not available - skipping WSGI integration")
        return False

def initialize_framework_integrations():
    """Initialize all framework integrations."""
    setup_fastapi_logging()
    setup_flask_logging()
    setup_django_asgi_logging()
    setup_django_wsgi_logging() 