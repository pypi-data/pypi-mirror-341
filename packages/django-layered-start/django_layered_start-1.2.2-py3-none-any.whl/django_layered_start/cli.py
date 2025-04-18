from .core.project_creator import ProjectCreator
from .core.app_creator import AppCreator
from .core.layered_structure import LayeredStructure

def start():
    project_name = input("Project Name: ").strip()

    project_creator = ProjectCreator()
    project_creator.create(project_name)

    structure = LayeredStructure()
    app_creator = AppCreator(project_name, structure)

    while True:
        app_name = input("🧱 App name (or N to exit): ").strip()
        if app_name.upper() == 'N':
            break
        app_creator.create(app_name)

        more = input("Do you want to add another app? (Y/N): ").strip()
        if more.upper() != 'Y':
            break
