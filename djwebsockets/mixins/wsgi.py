from djwebsockets.mixins import BaseWSMixin
from django import http
from django.conf import settings
import importlib


class WSGIMixin(BaseWSMixin):
    middleware_loaded = False
    _request_middleware = []

    @classmethod
    def on_connect(cls, socket, path):
        cls.mod_for_wsgi(socket, path)
        cls.run_middleware(socket)

    @staticmethod
    def mod_for_wsgi(socket, path):
        environ = {
            'HTTP_COOKIE': socket.socket.request_headers["Cookie"],
            'PATH_INFO': path,
            'SERVER_PROTOCOL': '',
            'HTTP_HOST': socket.socket.request_headers.get("Host"),
            'HTTP_ACCEPT': '',
            'SERVER_PORT': '8000',
            'REMOTE_ADDR': socket.socket.remote_address[0],
            'REMOTE_HOST': '',
        }
        try:
            socket.COOKIES = lambda: None
            socket.COOKIES = {}
            socket.COOKIES = http.parse_cookie(environ.get("HTTP_COOKIE"))
            socket.user = lambda: None
            socket.user = None
            socket.session = lambda: None
            socket.session = None
            socket.environ = lambda: None
            socket.environ = environ
            socket.META = lambda: None
            socket.META = {}
            socket.get_host = lambda: environ.get("HTTP_HOST")
            socket.path = lambda: None
            socket.path = path
        except AttributeError:
            pass
        return environ

    @staticmethod
    def load_middleware():
        if WSGIMixin.middleware_loaded:
            return
        WSGIMixin.middleware_loaded = True
        try:
            str_midddleware = settings.WEBSOCKET_MIDDLEWARE
        except AttributeError:
            return

        for middleware in str_midddleware:
            try:
                parts = middleware.split(".")
                size = len(parts)
                module = None
                for part in parts[0:size-1]:
                    if module is None:
                        module = part
                    else:
                        module += "."+part
                module = importlib.import_module(module)
                mware = getattr(module, parts[size-1])
                WSGIMixin._request_middleware.append(mware().process_request)
            except:
                pass

    @staticmethod
    def run_middleware(ws):
        if not WSGIMixin.middleware_loaded:
            WSGIMixin.load_middleware()
        for middleware in WSGIMixin._request_middleware:
            middleware(ws)