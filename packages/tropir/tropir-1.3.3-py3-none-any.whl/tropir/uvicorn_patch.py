"""
Special patching module for uvicorn/FastAPI.
This is loaded by the CLI when running uvicorn.
"""

import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger("tropir.uvicorn_patch")

if os.environ.get("TROPIR_DEBUG_FRAMEWORKS") == "1":
    logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.debug("Uvicorn patch debug mode enabled")
    print("Uvicorn patch debug mode enabled")


def patch_uvicorn():
    """
    Patch Uvicorn's Server class to apply our FastAPI patches at the right time.
    This ensures FastAPI is fully loaded before we try to patch it.
    """
    try:
        import uvicorn
        from uvicorn.server import Server
        
        # Import our fastapi patch function
        from .framework_integrations import setup_fastapi_logging, verify_fastapi_patch
        
        logger.debug("Patching uvicorn.Server.run")
        print("Patching uvicorn.Server.run")
        
        original_run = Server.run
        
        async def patched_run(self):
            """Patched run method that ensures FastAPI is patched before server starts."""
            print("Patched uvicorn.Server.run called")
            logger.debug("Patched uvicorn.Server.run called")
            
            # Ensure FastAPI is patched here before we run the server
            # By this point, the ASGI app should be fully loaded
            try:
                print("Applying FastAPI patch from uvicorn hook")
                setup_fastapi_logging()
                verify_fastapi_patch()
            except Exception as e:
                print(f"Error applying FastAPI patch from uvicorn hook: {e}")
                logger.error(f"Error applying FastAPI patch from uvicorn hook: {e}")
            
            # Call the original run method
            return await original_run(self)
        
        # Apply our patch
        Server.run = patched_run
        
        logger.debug("Successfully patched uvicorn.Server.run")
        print("Successfully patched uvicorn.Server.run")
        return True
    except ImportError as e:
        logger.error(f"Failed to import uvicorn: {e}")
        print(f"Failed to import uvicorn: {e}")
        return False
    except Exception as e:
        logger.error(f"Error patching uvicorn: {e}")
        print(f"Error patching uvicorn: {e}")
        return False


# Also patch starlette since it's the base for FastAPI
def patch_starlette():
    """
    Patch Starlette's routing mechanisms to apply our request ID tracking.
    This is a more direct approach than patching FastAPI.
    """
    try:
        from starlette.routing import Route
        
        logger.debug("Patching Starlette.routing.Route")
        print("Patching Starlette.routing.Route")
        
        # Import the request_id_ctx_var
        from .framework_integrations import request_id_ctx_var
        import uuid
        
        original_handle = Route.handle
        
        async def patched_handle(self, scope, receive, send):
            """Add request ID to context before handling request."""
            request_id = str(uuid.uuid4())
            print(f"Starlette route handler called with request_id: {request_id}")
            token = request_id_ctx_var.set(request_id)
            try:
                return await original_handle(self, scope, receive, send)
            finally:
                request_id_ctx_var.reset(token)
        
        # Apply our patch
        Route.handle = patched_handle
        
        logger.debug("Successfully patched Starlette.routing.Route.handle")
        print("Successfully patched Starlette.routing.Route.handle")
        return True
    except ImportError as e:
        logger.error(f"Failed to import starlette: {e}")
        print(f"Failed to import starlette: {e}")
        return False
    except Exception as e:
        logger.error(f"Error patching starlette: {e}")
        print(f"Error patching starlette: {e}")
        return False 