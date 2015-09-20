from djwebsockets.decorator import Namespace
from djwebsockets.mixins.wsgi import WSGIMixin


@Namespace("/chatroom")
class ChatRoom(WSGIMixin):
    rooms = {}

    @classmethod
    def on_connect(cls, socket, path):
        room = cls.get_room(path)
        room.append(socket)
        msg = "{} has joined room".format(str(socket.user))
        cls.publish(room, msg)

    @classmethod
    def on_message(cls, socket, message):
        room = cls.get_room(socket.path)
        msg = str(socket.user)+" : "+message
        cls.publish(room, msg)

    @classmethod
    def on_close(cls, socket):
        room = cls.get_room(socket.path)
        msg = "{} has left the room".format(str(socket.user))
        room.remove(socket)
        cls.publish(room, msg)

    @staticmethod
    def get_room(path):
        room = ChatRoom.get(path)
        if room is not None:
            return room
        else:
            ChatRoom[path] = []
            return ChatRoom[path]

    @staticmethod
    def publish(room, message):
        for socket in room:
            socket.send(message)

