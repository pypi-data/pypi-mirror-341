# Django Layered Start

**Django Layered Start** is a powerful CLI tool that helps you kickstart your Django projects by automatically creating a clean, SOLID‑compliant layered architecture. This package sets up your Django project and apps with separate layers for presentation, application, domain, and infrastructure, providing you with an organized and scalable foundation for your development.

---

## 🚀 Features

- **Automated Project Setup:** Instantly generate a new Django project using `django-admin`.
- **Layered App Creation:** Create Django apps with a predefined folder structure:
  - **Presentation:** Contains view logic and URL configurations.
  - **Application:** Houses business logic and service layers.
  - **Domain:** Includes domain‑specific utilities, selectors, and validators.
  - **Infrastructure:** Manages models and integration with external systems.
- **SOLID Principles:** Ensures your code remains clean, maintainable, and scalable by following core SOLID design principles.
- **Interactive CLI Interface:** A guided command‑line experience for setting up your project and apps without hassle.

---

## 🛠 Installation

To install the package from PyPI, run:

```bash
pip install django-layered-start
```

Then start the CLI tool:

```bash
django-layered-start
```

---

## 💻 Creating the Project & Apps

Follow the interactive prompts to scaffold your project:

```text
📦 Project name: myproject
✅ Django project "myproject" created!

🧱 App name (or N to stop): accounts
📂 App "accounts" created with layered structure.

❓ Do you want to add another app? (Y/N): Y
🧱 App name (or N to stop): products
📂 App "products" created with layered structure.

❓ Do you want to add another app? (Y/N): N
```

---

## 📁 Project Structure

After running the CLI, your directory tree will look like this:

```text
myproject/
├── manage.py
├── myproject/
│   └── settings.py
├── accounts/
│   ├── presentation/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── application/
│   │   ├── __init__.py
│   │   └── services.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── selectors.py
│   │   └── utilities.py
│   └── infrastructure/
│       ├── __init__.py
│       └── models.py
└── products/
    ├── presentation/
    │   ├── __init__.py
    │   ├── views.py
    │   └── urls.py
    ├── application/
    │   ├── __init__.py
    │   └── services.py
    ├── domain/
    │   ├── __init__.py
    │   ├── validators.py
    │   ├── selectors.py
    │   └── utilities.py
    └── infrastructure/
        ├── __init__.py
        └── models.py
```

---

**Django Layered Start** gives you a robust, SOLID‑driven foundation from day one — saving time and enforcing best practices in every app you build.


## Contributing
Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author
Developed by [Moataz Fawzy](https://github.com/Moataz0000).