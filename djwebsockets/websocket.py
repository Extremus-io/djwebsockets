from .server import WebSocketServer


class WebSocket:
    loop = None

    def __init__(self, socket, close, send):
        self.socket = socket
        self.close_handler = close
        self.send_handler = send
        self.id = id(socket)
        self.closed = False
        self.session = None
        self.COOKIES = {}
        self.user = None
        self.environ = None

    def send(self, Message):
        self.loop.call_soon_threadsafe(self._send, Message)

    def _send(self, Message):
        self.send_handler.set_result(Message)

    def close(self):
        self.closed = True
        self.loop.call_soon_threadsafe(self._close)

    def _close(self):
        self.close_handler.set_result(-1)

    @staticmethod
    def get_websocket_by_id(id):
        return WebSocketServer.websockets.get(id)
