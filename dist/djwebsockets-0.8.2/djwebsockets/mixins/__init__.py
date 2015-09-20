class BaseWSMixin(object):

    @classmethod
    def on_connect(cls, socket, path):
        pass

    @classmethod
    def on_message(cls, socket, message):
        pass

    @classmethod
    def on_close(cls, socket):
        pass


class MixinFail(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
