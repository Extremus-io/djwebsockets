#djwebsockets
The library adds websocket support to django. also gives event driven websocket control for convenience of http programmers.
The idea is to create a separate websocket server when an instance of django wsgi application instance is produced. and kill it as soon as the instance dies.

##Installation
- copy the repo into your project directory.
- put ```djwebsockets``` in ```settings.INSTALLED_APPS``` 


###djwebsockets
