from django.conf import settings
from . import default_settings

if hasattr(settings,'WEBSOCKET_BASE_URI'):
    WEBSOCKET_BASE_URI = settings.WEBSOCKET_BASE_URI
else:
    WEBSOCKET_BASE_URI = ""
if hasattr(settings,'WEBSOCKET_HOST'):
    WEBSOCKET_HOST=settings.WEBSOCKET_HOST
else:
    WEBSOCKET_HOST="localhost"
if hasattr(settings,'WEBSOCKET_PORT'):
    WEBSOCKET_PORT=settings.WEBSOCKET_PORT
else:
    WEBSOCKET_PORT=8001
