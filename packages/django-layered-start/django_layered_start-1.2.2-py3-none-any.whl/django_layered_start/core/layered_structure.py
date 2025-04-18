import os

class LayeredStructure:
    def __init__(self):
        self.layers = {
            'presentation': {
                'files': {
                    'views.py': (
                        "# Presentation layer: This module contains the view functions or class-based views.\n"
                        "def index(request):\n"
                        "    # TODO: implement the logic to render the homepage\n"
                        "    pass\n"
                    ),
                    'urls.py': (
                        "# Presentation layer: Define URL patterns for the app here.\n"
                        "from django.urls import path\n\n"
                        "urlpatterns = [\n"
                        "    # TODO: add URL patterns here\n"
                        "]\n"
                    )
                }
            },
            'application': {
                'files': {
                    'services.py': (
                        "# Application layer: Contains business logic and use cases.\n"
                        "def perform_action(data):\n"
                        "    # TODO: implement business logic here\n"
                        "    pass\n"
                    )
                }
            },
            'domain': {
                'files': {
                    'validators.py': (
                        "# Domain layer: Contains validation rules for the domain entities.\n"
                        "def validate_entity(entity):\n"
                        "    # TODO: implement validation logic\n"
                        "    pass\n"
                    ),
                    'selectors.py': (
                        "# Domain layer: Contains selectors for querying domain-specific data.\n"
                        "def select_active_items(items):\n"
                        "    # TODO: implement selection logic\n"
                        "    return [item for item in items if item.get('active')]\n"
                    ),
                    'utilities.py': (
                        "# Domain layer: Utility functions related to the domain.\n"
                        "def format_entity(entity):\n"
                        "    # TODO: implement a method to format or transform the domain entity\n"
                        "    pass\n"
                    )
                }
            },
            'infrastructure': {
                'files': {
                    'models.py': (
                        "# Infrastructure layer: Contains Django models.\n"
                        "# IMPORTANT: Move your model definitions here from the default models.py.\n"
                        "from django.db import models\n\n"
                        "class ExampleModel(models.Model):\n"
                        "    # TODO: define your model fields\n"
                        "    name = models.CharField(max_length=255)\n\n"
                        "    def __str__(self):\n"
                        "        return self.name\n"
                    )
                }
            }
        }

    def setup(self, app_name: str):
        """
        Create the layered folder structure along with sample files for the given app.
        """
        base_path = os.path.join(app_name)
        for layer, config in self.layers.items():
            layer_path = os.path.join(base_path, layer)
            os.makedirs(layer_path, exist_ok=True)

            init_file = os.path.join(layer_path, '__init__.py')
            with open(init_file, 'w', encoding='utf-8'):
                pass

            for filename, content in config.get('files', {}).items():
                file_path = os.path.join(layer_path, filename)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

        print(f"📂 The layered structure with sample files was created for the app: {app_name}")
