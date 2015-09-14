from django.core.wsgi import get_wsgi_application as django_wsgi
from djwebsockets import server
from django.conf import settings


def get_wsgi_application():
    try:
        host = settings.WEBSOCKET_HOST
    except Exception as exec:
        host = "localhost"
    try:
        port = settings.WEBSOCKET_PORT
    except Exception as exec:
        port = "8001"

    wsgihandler = django_wsgi()
    ws_server = server.WebSocketServer(host, port)
    ws_server.run_server()

    return wsgihandler

