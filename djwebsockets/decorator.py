from djwebsockets.server import WebSocketServer
import djwebsockets as settings


def Namespace(namespace):
    def socketplacer(clsitem):
        if WebSocketServer.NameSpaces.get(namespace) is None:
            WebSocketServer.AddNameSpace(namespace, clsitem)
            print("Websocket namespace \"{}\" registered for {}".format(settings.WEBSOCKET_BASE_URI+namespace, clsitem.__name__))
        return clsitem
    return socketplacer

