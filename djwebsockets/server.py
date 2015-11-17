import asyncio
import websockets
import os
import inspect
from threading import Thread
from djwebsockets.websocket import WebSocket
import djwebsockets as settings

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
    def AddNameSpace(namespace, clsitem):
        BASE_URI=settings.WEBSOCKET_BASE_URI
        path = BASE_URI+namespace
        WebSocketServer.NameSpaces.update({path:clsitem})

    @staticmethod
    def get_namespace(path):
        BASE_URI=settings.WEBSOCKET_BASE_URI
        return WebSocketServer.NameSpaces.get(path,None)
        # for regex in WebSocketServer.NameSpaces:
        #     uri = BASE_URI+regex
        #     reg = re.compile(uri)
        #     if reg.search(path) is not None:
        #         cls = WebSocketServer.NameSpaces.get(regex, None)
        #     else:
        #         cls = None
        #     return cls

    @staticmethod
    def get_callbacks(cls):
        callbacks = inspect.getmembers(cls, predicate=inspect.ismethod)
        callbacks = {b[0]: b[1] for b in callbacks}
        return callbacks

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
        callbacks["_on_connect"](ws, path)
        if ws.closed:
            return
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
                    callbacks["_on_message"](ws, receivetask.result())
                except KeyError:
                    pass
            else:
                receivetask.cancel()
            if close_handler in done:
                try:
                    callbacks["_on_close"](ws)
                except KeyError:
                    pass
                break
            if connection_closed in done:
                try:
                    callbacks["_on_close"](ws)
                except KeyError:
                    pass
                break

    def _run_server(self, loop):
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.server)
            loop.run_forever()
        except KeyboardInterrupt:
            pass

    def run_server(self):
        if self.loop.is_running():
            print("server already running")
            return
        print("Starting websocket server at ws://{}".format(self.host+":"+str(self.port)))
        thread = Thread(target=self._run_server, args=(self.loop,))
        thread.start()

    def _stop_server(self):
        self.server.close()
        print("WebSocket server Exiting...")

    def stop_server(self):
        self.loop.call_soon_threadsafe(self._stop_server)

    @staticmethod
    def get_websocket_by_id(id):
        return WebSocketServer.websockets.get(id)


if __name__ == "__main__":
    server = WebSocketServer("localhost", "8000")
    server.run_server()
