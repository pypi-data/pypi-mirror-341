from functools import wraps
from .di import Container

container = Container()

def register_service(service_name):
    def decorator(service):
        container.register(service_name, service)
        return service

    return decorator

def inject(service_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            service = container.get(service_name)
            setattr(self, service_name, service)  # Attach the service to the class instance
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
