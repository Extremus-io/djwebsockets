#djwebsockets
The library adds websocket support to django. It gives event driven websocket control for convenience of http programmers.


The idea is to create a separate websocket server when an instance of django wsgi application instance is produced. and kill it as soon as the instance dies.

#####Note:
> requires python 3.4 to work

###Installation:
- clone the repo ```git clone https://github.com/Extremus-io/djwebsockets.git```
- open terminal and ```cd``` to the repo directory.
- execute ```pip install -r requirements.txt```
- copy the ```djwebsockets``` directory in the repo into your django project directory.
- add ```djwebsockets``` to ```settings.INSTALLED_APPS``` 
- add ```WEBSOCKET_HOST``` and ```WEBSOCKET_PORT`` to settings.py
- in wsgi.py file, replace line
```python
    from django.core.wsgi import get_wsgi_application 
```
with
```python
    from djwebsockets.wsgi import get_wsgi_application
```
- **optional**: use following for session variables and user (```websocket.user``` and ```websocket.session```)
```python
    WEBSOCKET_MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]
```

###Usage:
* in any app's ```models.py``` add
```python
    from djwebsockets.decorator import Namespace
```
* create a websocket handler with a namespace 
```python 
    @Namespace("/example/"):
    class ExamplerHandler:
       @classmethod:
       on_connect(cls, websocket, path):
           ...
       @classmethod:
       on_message(cls, websocket, message):
           ...
       @classmethod:
       on_close(cls, websocket, message):
           ...
```


#####PS:
>There are many more features already present and being made. i'm busy at the moment but documentation will be made soon.
