from djwebsockets.server import WebSocketServer


def Namespace(namespace):
    def socketplacer(clsitem):
        if WebSocketServer.NameSpaces.get(namespace) is None:
            WebSocketServer.NameSpaces[namespace] = clsitem
            print("Websocket namespace \"{}\" registered for {}".format(namespace, clsitem.__name__))
        return clsitem
    return socketplacer