# djwebsockets
The library adds websocket support to django (now any wsgi app). It gives event driven websocket control for simple and straight forward programming.


The idea is to create a separate websocket server when an instance of django wsgi application instance is produced. and kill it as soon as the instance dies.


#### Change-log:
> V0.9
> > *Breaking Changes*
> > all the websocket classes you want to use have to inherit `djwebsockets.websocket.BaseWSClass`.

> v0.8.1
> > Added mixin support
> > Added ability to run django request middleware on websocket requests through a mixin (see demo chatroom example)
> > Now works on any WSGI application or desktop application.
> > Added a demo chatroom example. 

##### Note:
> requires python 3.4 to work

### Installation:
- run `pip install djwebsockets`.
- add ```djwebsockets``` to ```settings.INSTALLED_APPS``` 
- add ```WEBSOCKET_HOST``` and ```WEBSOCKET_PORT``` to settings.py
- in wsgi.py file, replace line
```python
    from django.core.wsgi import get_wsgi_application 
```
   with
```python
    from djwebsockets.wsgi import get_wsgi_application
```

###Usage:
* in any app's ```models.py``` add
```python
    from djwebsockets.decorator import Namespace
    from djwebsockets.websocket import BaseWSClass
```
* create a websocket handler with a namespace 
```python 
    @Namespace("/example/"):
    class ExamplerHandler(BaseWSClass):
       @classmethod
       on_connect(cls, websocket, path):
           ...
       @classmethod
       on_message(cls, websocket, message):
           ...
       @classmethod
       on_close(cls, websocket):
           ...
```
* `Namespace` takes a regex expression. if it matches with any websocket connecting, the methods in this class get called.

### Mixins:
- mixins essentially process all or some of the events before actual handler, allowing to tweak the data or block the event call.
- creating mixin is a lot similar to creating the handler itself. 
```python
    class ExampleMixin(BaseMixin):
        @classmethod
        on_connect(cls, websocket, path):
            ...
        @classmethod
         on_message(cls, websocket, message):
            ...
        @classmethod
        on_close(cls, websocket):
            ...
```
- The mixin has to extend `djwebsockets.mixins.BaseMixin` class
- To use this mixin in your app, extend your handler with this mixin
```python 
    @Namespace("/example/"):
    class ExamplerHandler(ExampleMixin, BaseWSClass):
       @classmethod
       on_connect(cls, websocket, path):
           ...
       @classmethod
       on_message(cls, websocket, message):
           ...
       @classmethod
       on_close(cls, websocket):
           ...
```
- You can also add multiple mixins. They will be executed from right to left.
```python 
    @Namespace("/example/"):
    class ExamplerHandler(ExampleMixin1 ,ExampleMixin2, ExampleMixin3, BaseWSClass):
       @classmethod
       on_connect(cls, websocket, path):
           ...
       @classmethod
       on_message(cls, websocket, message):
           ...
       @classmethod
       on_close(cls, websocket):
           ...
```

### \*\*Experimental\*\* django middleware support:

- Django middleware can be used to authentication, sessions etc. (```websocket.user``` and ```websocket.session```)
- To activate django middleware, extend your websocket handler with `djwebsockets.mixins.wsgi.WSGIMixin`.
- add middle you want to run just like django.
```python
    WEBSOCKET_MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    ]
```
> For general Auth, session the above three or their equivalents will be sufficient.

