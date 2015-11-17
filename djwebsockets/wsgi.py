from django.core.wsgi import get_wsgi_application as django_wsgi
from djwebsockets import server
from django.conf import settings


def get_wsgi_application():
    host = settings.WEBSOCKET_HOST
    port = settings.WEBSOCKET_PORT
    wsgihandler = django_wsgi()
    ws_server = server.WebSocketServer(host, port)
    ws_server.run_server()

    return wsgihandler

