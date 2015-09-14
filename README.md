#djwebsockets
The library adds websocket support to django. It gives event driven websocket control for convenience of http programmers.
</br>
The idea is to create a separate websocket server when an instance of django wsgi application instance is produced. and kill it as soon as the instance dies.

##Installation
1. copy the repo into your project directory.
2. add ```djwebsockets``` to ```settings.INSTALLED_APPS``` 
3. in wsgi.py file, replace line
```python
    from django.core.wsgi import get_wsgi_application 
```
with
```python
    from djwebsockets.wsgi import get_wsgi_application
```


###djwebsockets
