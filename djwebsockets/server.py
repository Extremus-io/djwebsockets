import asyncio
import websockets
import os
import inspect
from threading import Thread
from django.conf import settings
from django import http
import importlib
from .websocket import WebSocket

BASE_DIR = os.path.dirname(__file__)


class WebSocketServer:
    NameSpaces = {}
    server_running = False
    loop = None
    server = None
    host = None
    port = None
    _request_middleware = []
    middleware_loaded = False
    websockets = {}

    def __init__(self, host, port):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.server = websockets.serve(self.receiver, host, port, loop=self.loop)
        self.host = host
        self.port = port
        WebSocket.loop = self.loop

    @staticmethod
    def get_namespace(path):
        cls = WebSocketServer.NameSpaces.get(path, None)
        return cls

    @staticmethod
    def get_callbacks(cls):
        callbacks = inspect.getmembers(cls, predicate=inspect.ismethod)
        callbacks = {b[0]: b[1] for b in callbacks}
        return callbacks

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
            socket.COOKIES = http.parse_cookie(environ.get("HTTP_COOKIE"))
        except AttributeError:
            pass
        return environ

    def run_middleware(self, ws):
        if not self.middleware_loaded:
            self.load_middleware()
        for middleware in self._request_middleware:
            middleware(ws)

    @asyncio.coroutine
    def receiver(self, websocket, path):
        cls = WebSocketServer.get_namespace(path)
        if cls is None:
            yield from websocket.send("Invalid path")
            return

        callbacks = self.get_callbacks(cls)
        close_handler = asyncio.Future()
        send_handler = asyncio.Future()
        ws = WebSocket(websocket, close_handler, send_handler)
        self.websockets[id(websocket)] = ws
        self.mod_for_wsgi(ws, path)
        self.run_middleware(ws)
        try:
            callbacks["on_connect"](ws, path)
        except KeyError:
            pass
        while True:
            receivetask = asyncio.async(websocket.recv())
            connection_closed = websocket.connection_closed
            done, pending = yield from asyncio.wait([receivetask, close_handler, send_handler, connection_closed], return_when=asyncio.FIRST_COMPLETED)
            if send_handler in done:
                try:
                    yield from websocket.send(send_handler.result())
                except KeyError:
                    pass
                send_handler = asyncio.Future()
                ws.send_handler = send_handler

            if receivetask in done:
                try:
                    callbacks["on_message"](ws, receivetask.result())
                except KeyError:
                    pass
            else:
                receivetask.cancel()
            if close_handler in done:
                try:
                    callbacks["on_close"](ws)
                except KeyError:
                    pass
                break
            if connection_closed in done:
                try:
                    callbacks["on_close"](ws)
                except KeyError:
                    pass
                break
        #
        # yield from websocket.send("Authenticating")
        # a = open(os.path.join(BASE_DIR, "apikeys.json"), mode='r')
        # keys = json.loads(a.read())['keys']
        # auth = False
        # try:
        #     if websocket.request_headers["API_KEY"] in keys:
        #         auth = True
        #         yield from websocket.send("Authentication Successful")
        #     else:
        #         yield from websocket.send("invalid API_KEY. is your device registered?")
        # except:
        #     yield from websocket.send("Required Headers are missing")
        #
        # #TODO: implement auth module here!
        #
        # if auth:
        #     yield from websocket.send("Successfully connected!")
        #     print("Successfully connected")
        #     while True:
        #         data = yield from websocket.recv()
        #         print("< {}".format(data))
        #         output = "Received : \"{}\"".format(data)
        #         yield from websocket.send(output)

    def load_middleware(self):
        if self.middleware_loaded:
            return
        self.middleware_loaded = True
        try:
            str_midddleware = settings.WEBSOCKET_MIDDLEWARE
        except:
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
                        module+="."+part
                module = importlib.import_module(module)
                mware = getattr(module, parts[size-1])
                self._request_middleware.append(mware().process_request)
            except:
                pass

    def _run_server(self, loop):
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.server)
            loop.run_forever()
        except KeyboardInterrupt:
            pass

    def run_server(self):
        print("Starting websocket server at ws://{}".format(self.host+":"+str(self.port)))
        thread = Thread(target=self._run_server, args=(self.loop,))
        thread.start()
        self.server_running = True

    def _stop_server(self):
        self.server.close()
        print("WebSocket server Exiting...")

    def stop_server(self):
        self.loop.call_soon_threadsafe(self._stop_server)


if __name__ == "__main__":
    server = WebSocketServer("localhost", "8000")
    server.run_server()
