from djwebsockets.server import WebSocketServer
from djwebsockets.mixins import BaseWSMixin, MixinFail
import inspect


def Namespace(namespace):
    def socketplacer(clsitem):
        class BaseWSClass(BaseWSMixin):
            @staticmethod
            def super_classes(cls):
                return reversed(cls.__mro__)

            @classmethod
            def call_methods(cls, method, *args):
                for clus in cls.super_classes(clsitem):
                    try:
                        if hasattr(clus, method):
                            getattr(clus, method)(*args)
                    except MixinFail:
                        args[0].close()
                        return

            @classmethod
            def on_connect(cls, socket, path):
                cls.call_methods("on_connect", socket, path)

            @classmethod
            def on_message(cls, socket, message):
                cls.call_methods("on_message", socket, message)

            @classmethod
            def on_close(cls, socket):
                cls.call_methods("on_close", socket)
        if WebSocketServer.NameSpaces.get(namespace) is None:
            WebSocketServer.NameSpaces[namespace] = BaseWSClass
            print("Websocket namespace \"{}\" registered for {}".format(namespace, clsitem.__name__))
        return clsitem
    return socketplacer

