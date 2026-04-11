"""
WSGI entry point for Mesop application
"""
import os

# Set mesop app path
os.environ['MESOP_APP_PATH'] = 'app.py'

# Import app.py to register the pages BEFORE creating WSGI app
import app  # This registers the @me.page decorators

# Import mesop's WSGI application
from mesop.server.wsgi_app import create_wsgi_app

# Create WSGI app (no arguments - uses MESOP_APP_PATH env var)
mesop_app = create_wsgi_app()

# Middleware to fix Origin/Host mismatch for Mesop's CSRF validation
class OriginAdjustingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Mesop checks if Origin matches Host for CSRF protection
        # When behind App Router, Origin is the public URL but Host is the internal CF route
        # We need to make Host match the Origin

        if 'HTTP_ORIGIN' in environ:
            # Extract the host from the Origin URL
            origin = environ['HTTP_ORIGIN']
            # Origin format: https://hostname or http://hostname
            if '://' in origin:
                origin_host = origin.split('://')[1]
                # Set the Host header to match the Origin
                environ['HTTP_HOST'] = origin_host
                environ['SERVER_NAME'] = origin_host.split(':')[0]  # Without port
                if ':' in origin_host:
                    environ['SERVER_PORT'] = origin_host.split(':')[1]
                else:
                    environ['SERVER_PORT'] = '443' if origin.startswith('https') else '80'

        return self.app(environ, start_response)

# Wrap the application with the middleware
application = OriginAdjustingMiddleware(mesop_app)
