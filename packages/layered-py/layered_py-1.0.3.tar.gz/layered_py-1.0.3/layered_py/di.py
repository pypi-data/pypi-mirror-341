class Container:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def get(self, name):
        service = self.services.get(name)

        if service:
            return service

        raise ValueError(f"Service {name} not found")