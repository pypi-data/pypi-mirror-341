import uuid
import logging
import contextvars
import os
import sys
import importlib.util
import traceback

logger = logging.getLogger("tropir")

# Configure logger for additional debug info if needed
if os.environ.get("TROPIR_DEBUG_FRAMEWORKS") == "1":
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    print("Tropir framework integration debug logging enabled")

# Create a context variable for request ID
request_id_ctx_var = contextvars.ContextVar("request_id", default=None)

# Flag to track if we've already patched
_fastapi_patched = False
_flask_patched = False
_django_asgi_patched = False
_django_wsgi_patched = False


def verify_fastapi_patch():
    """Verify that FastAPI is properly patched."""
    try:
        from fastapi import FastAPI
        from fastapi.routing import APIRoute
        patched = getattr(APIRoute.get_route_handler, '_is_request_id_patched', False)
        print(f"FastAPI patch verification: {'PATCHED' if patched else 'NOT PATCHED'}")
        return patched
    except ImportError:
        print("FastAPI not installed - cannot verify patch")
        return False


def setup_fastapi_logging():
    """Set up request ID tracking for FastAPI applications."""
    global _fastapi_patched
    if _fastapi_patched:
        logger.debug("FastAPI already patched, skipping...")
        print("FastAPI already patched, skipping...")
        return True
        
    try:
        print("Attempting to patch FastAPI...")
        from fastapi import FastAPI
        from fastapi.routing import APIRoute
        print("FastAPI modules imported successfully")

        # Check if already patched
        if getattr(APIRoute.get_route_handler, '_is_request_id_patched', False):
            logger.debug("APIRoute.get_route_handler already patched; skipping patch")
            print("APIRoute.get_route_handler already patched; skipping patch")
            _fastapi_patched = True
            return True

        original_get_route_handler = APIRoute.get_route_handler
        print("Original get_route_handler function captured")

        def custom_get_route_handler(self):
            # Only log this in debug mode with high verbosity
            if os.environ.get("TROPIR_DEBUG_FRAMEWORKS_VERBOSE") == "1":
                print("Custom get_route_handler called")
            original_handler = original_get_route_handler(self)

            async def custom_handler(request):
                request_id = str(uuid.uuid4())
                # Only log this in debug mode with high verbosity
                if os.environ.get("TROPIR_DEBUG_FRAMEWORKS_VERBOSE") == "1":
                    print(f"Custom handler called with request_id: {request_id}")
                token = request_id_ctx_var.set(request_id)
                try:
                    response = await original_handler(request)
                    return response
                finally:
                    request_id_ctx_var.reset(token)
            return custom_handler

        # Mark the patched function to prevent double patching
        custom_get_route_handler._is_request_id_patched = True

        # Apply the patch
        APIRoute.get_route_handler = custom_get_route_handler
        print("FastAPI patching applied successfully")
        logger.debug("Successfully monkey-patched APIRoute.get_route_handler for request ID injection")
        _fastapi_patched = True
        
        # Verify patching
        verify_fastapi_patch()
        
        return True
    except ImportError as e:
        logger.debug(f"FastAPI not available - skipping FastAPI integration: {e}")
        print(f"FastAPI not available - skipping FastAPI integration: {e}")
        return False
    except Exception as e:
        logger.error(f"Error patching FastAPI: {e}")
        print(f"Error patching FastAPI: {e}")
        traceback.print_exc()
        return False

def setup_flask_logging():
    """Set up request ID tracking for Flask applications."""
    global _flask_patched
    if _flask_patched:
        logger.debug("Flask already patched, skipping...")
        return True
        
    try:
        from flask import Flask
    except ImportError:
        logger.debug("Flask not available - skipping Flask integration")
        return False

    if getattr(Flask.__init__, '_is_request_id_patched', False):
        logger.debug("Flask.__init__ already patched; skipping patch")
        _flask_patched = True
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
    _flask_patched = True
    return True

def setup_django_asgi_logging():
    """Set up request ID tracking for Django ASGI applications."""
    global _django_asgi_patched
    if _django_asgi_patched:
        logger.debug("Django ASGI already patched, skipping...")
        return True
        
    try:
        from django.core.handlers.asgi import ASGIHandler

        # Check if already patched
        if getattr(ASGIHandler.__call__, '_is_request_id_patched', False):
            logger.debug("ASGIHandler.__call__ already patched; skipping patch")
            _django_asgi_patched = True
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
        _django_asgi_patched = True
        return True
    except ImportError:
        logger.debug("Django ASGIHandler not available - skipping ASGI integration")
        return False

def setup_django_wsgi_logging():
    """Set up request ID tracking for Django WSGI applications."""
    global _django_wsgi_patched
    if _django_wsgi_patched:
        logger.debug("Django WSGI already patched, skipping...")
        return True
        
    try:
        from django.core.handlers.wsgi import WSGIHandler

        # Check if already patched
        if getattr(WSGIHandler.__call__, '_is_request_id_patched', False):
            logger.debug("WSGIHandler.__call__ already patched; skipping patch")
            _django_wsgi_patched = True
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
        _django_wsgi_patched = True
        return True
    except ImportError:
        logger.debug("Django WSGIHandler not available - skipping WSGI integration")
        return False


def initialize_framework_integrations():
    """Initialize all framework integrations."""
    logger.debug("Initializing framework integrations")
    print("Initializing framework integrations")
    
    # Try to patch FastAPI first
    try:
        setup_fastapi_logging()
    except Exception as e:
        print(f"Error initializing FastAPI integration: {e}")
        logger.error(f"Error initializing FastAPI integration: {e}")
    
    # Then try Flask
    try:
        setup_flask_logging() 
    except Exception as e:
        print(f"Error initializing Flask integration: {e}")
        logger.error(f"Error initializing Flask integration: {e}")
    
    # Then try Django
    try:
        setup_django_asgi_logging()
        setup_django_wsgi_logging()
    except Exception as e:
        print(f"Error initializing Django integration: {e}")
        logger.error(f"Error initializing Django integration: {e}")
    
    print("Framework integrations initialization complete")
    logger.debug("Framework integrations initialization complete")


# Create auto-patching mechanism for FastAPI - patch when FastAPI is imported
original_import = __import__

def patched_import(name, globals=None, locals=None, fromlist=(), level=0):
    module = original_import(name, globals, locals, fromlist, level)
    
    # Check if TROPIR is enabled
    if os.environ.get("TROPIR_ENABLED") == "1" and os.environ.get("TROPIR_PATCH_FRAMEWORKS") == "1":
        try:
            # If fastapi module or any fastapi submodule is imported, apply patching
            if name == "fastapi" or name.startswith("fastapi."):
                logger.debug(f"Detected import of {name}, patching FastAPI...")
                print(f"Detected import of {name}, patching FastAPI...")
                setup_fastapi_logging()
            # If flask module or any flask submodule is imported, apply patching
            elif name == "flask" or name.startswith("flask."):
                logger.debug(f"Detected import of {name}, patching Flask...")
                setup_flask_logging()
            # If django module or any django submodule is imported, apply patching
            elif name == "django" or name.startswith("django."):
                logger.debug(f"Detected import of {name}, patching Django...")
                setup_django_asgi_logging()
                setup_django_wsgi_logging()
        except Exception as e:
            logger.error(f"Error in patched import for {name}: {e}")
            print(f"Error in patched import for {name}: {e}")
    
    return module

# Apply the import hook
logger.debug("Installing Tropir framework import hooks")
print("Installing Tropir framework import hooks")
sys.modules["builtins"].__import__ = patched_import 