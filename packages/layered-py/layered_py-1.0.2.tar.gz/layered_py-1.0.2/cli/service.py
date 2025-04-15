import os
import sys

def create(service_name):
    service_template = f"""
from service_layer.service import Service

class {service_name}(Service):
    def setup(self):
        pass

    def handle(self):
        raise NotImplementedError
    """

    # Ensure the 'services' directory exists
    directory = "services"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/{service_name}.py"

    with open(file_path, "w") as file:
        file.write(service_template)

    print(f"Service '{service_name}' created at {file_path}")


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "create":
        print("Usage: python service.py create <ServiceName>")
        sys.exit(1)

    command, service_name = sys.argv[1], sys.argv[2]
    if command == "create":
        create(service_name)

if __name__ == "__main__":
    main()