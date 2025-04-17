import os


class LayeredStructure:
    def __init__(self):
        self.leyers = ['presentation', 'application', 'domain', 'infrastructure']

    
    def setup(self, app_name: str) -> None:
        for leyer in self.leyers:
            path = os.path.join(app_name, leyer)
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, '__init__.py'), 'w'):
                pass
        print(f"Layered structure created for the application: {app_name} 📂")
