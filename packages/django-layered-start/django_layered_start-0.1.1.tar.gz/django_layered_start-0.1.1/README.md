# Django Layered Start

**Django Layered Start** is a powerful CLI tool that helps you kickstart your Django projects by automatically creating a clean, SOLID-compliant layered architecture. This package sets up your Django project and apps with separate layers for presentation, application, domain, and infrastructure, providing you with an organized and scalable foundation for your development.

---

## 🚀 Features

- **Automated Project Setup:** Instantly generate a new Django project using `django-admin`.
- **Layered App Creation:** Create Django apps with a predefined folder structure:
  - **Presentation:** Contains view logic and URL configurations.
  - **Application:** Houses business logic and service layers.
  - **Domain:** Includes domain-specific utilities, selectors, and validators.
  - **Infrastructure:** Manages models and integration with external systems.
- **SOLID Principles:** Ensures your code remains clean, maintainable, and scalable by following core SOLID design principles.
- **Interactive CLI Interface:** A guided command-line experience for setting up your project and apps without hassle.

---

## 🛠 Installation

To install the package from PyPI, run:

```
pip install django-layered-start
```

Then Start With This Command:

```
django-layered-start
```

## Creating The Project

* Project name: myproject📦
  * Django project "myproject" created!✅

* App name (or N to stop): accounts 🧱
  * App "accounts" created with layered structure.📂

* Do you want to add another app? (Y/N): Y 
  * App name (or N to stop): products
  * 
* App "blog" created with layered structure.
  * Do you want to add another app? (Y/N): N


## The Project Structure Will Be:

```
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
```
