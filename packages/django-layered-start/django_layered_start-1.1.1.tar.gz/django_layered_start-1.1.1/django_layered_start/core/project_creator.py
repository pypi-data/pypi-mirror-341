import subprocess
import os


class ProjectCreator:
    def create(self, project_name: str) -> None:
        subprocess.run(['django-admin', 'startproject', project_name])
        print(f"The Project '{project_name}' is created successfully ✅:")

        self._create_requirements_folder(project_name)


    def _create_requirements_folder(self, project_name: str):
        req_dir = os.path.join(project_name, 'requirements')
        os.makedirs(req_dir, exist_ok=True)

        for filename in ('local.text', 'production.text'):
            file_path = os.path.join(req_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('# Add your dependencies here\n')

        print(f"📦 Requirements folder initialized with local.text & production.text at '{req_dir}'")
