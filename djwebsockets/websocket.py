from djwebsockets.mixins import BaseWSMixin, MixinFail
import asyncio

class WebSocket:
    loop = None

    def __init__(self, socket, close, send):
        self.socket = socket
        self.close_handler = close
        self.send_handler = send
        self.id = id(socket)
        self.closed = False

    def send(self, Message):
        self.loop.call_soon_threadsafe(self._send, Message)

    def _send(self, Message):
        self.send_handler.put_nowait(Message)

    def close(self):
        self.closed = True
        self.loop.call_soon_threadsafe(self._close)

    def _close(self):
        self.close_handler.set_result(-1)


class BaseWSClass:
            @staticmethod
            def super_classes(cls):
                return reversed(cls.__mro__)

            @classmethod
            def call_methods(cls, method, *args):
                for clus in cls.super_classes(cls):
                    try:
                        if hasattr(clus, method):
                            getattr(clus, method)(*args)
                    except MixinFail:
                        args[0].close()
                        return

            @classmethod
            def _on_connect(cls, socket, path):
                cls.call_methods("on_connect", socket, path)

            @classmethod
            def _on_message(cls, socket, message):
                cls.call_methods("on_message", socket, message)

            @classmethod
            def _on_close(cls, socket):
                cls.call_methods("on_close", socket)