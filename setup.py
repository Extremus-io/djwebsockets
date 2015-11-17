from distutils.core import setup

setup(
    name='djwebsockets',
    version='0.9.0',
    packages=['djwebsockets', 'djwebsockets.demo', 'djwebsockets.mixins'],
    keywords=['django', 'websockets', 'websocket', 'wsgi', 'simple websocket', 'simple', 'realtime', 'realtime server', 'realtime django'],
    url='https://github.com/extremus-io/djwebsockets',
    requires=['websockets', 'asyncio', 'django'],
    license='MIT',
    author='kittuov',
    author_email='kittuov@gmail.com',
    description='Simple Evented websocket interface for wsgi applications',
    long_description='''
    This is a part of a project extremus-io.
    ##### update V0.8.1:
        - minor bug fix
    ##### update V0.8:
        - added mixin support. now you can control the auth work flow in every event on_connect, on_message, on_close.

        - now supports any wsgi application see documentation for more information.

        - \* experimental * added django middleware support via a mixin (djwebsockets.mixins.wsgi.WSGIMixin) you can run django middleware for requests only for now
        added a demo chatroom websocket configuration.

    > The app is almost production ready. It lacks good documentation. partial documentation is available at https://pythonhosted.org/djwebsockets and https://extremus-io.github.io/djwebsockets
    > Note: requires python > 3
    ''',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3'
    ]
)
