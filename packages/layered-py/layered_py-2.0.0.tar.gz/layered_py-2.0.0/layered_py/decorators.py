from .di import Container

container = Container()

def register(name):
    def decorator(class_name):
        container.register(name, class_name)
        return class_name

    return decorator

def inject(name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            class_name = container.get(name)
            setattr(self, name, class_name)  # Attach the class_name to the class instance
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
