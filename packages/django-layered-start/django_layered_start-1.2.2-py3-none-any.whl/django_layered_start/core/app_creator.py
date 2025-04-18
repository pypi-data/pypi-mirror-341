import os
import subprocess
from .layered_structure import LayeredStructure



class AppCreator:
    def __init__(self, project_name: str, structure: LayeredStructure):
        self.project_name = project_name
        self.structure = structure

    def create(self, app_name: str) -> None:
        os.chdir(self.project_name)
        subprocess.run(['python', 'manage.py', 'startapp', app_name])
        self.structure.setup(app_name)
        os.chdir('..')
        print(f"The app '{app_name}' has been created ✅")