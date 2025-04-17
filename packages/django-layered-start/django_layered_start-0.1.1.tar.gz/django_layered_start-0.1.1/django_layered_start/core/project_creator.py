import subprocess



class ProjectCreator:
    def create(self, project_name: str) -> None:
        subprocess.run(['django-admin', 'startproject', project_name])
        print(f"The Project '{project_name}' is created successfully ✅:")

