# setup.py

from setuptools import setup, find_packages

setup(
    name='django-layered-start',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.0',
    ],
    entry_points={
        'console_scripts': [
            'django-layered-start=django_layered_start.cli:start',
        ],
    },
    author='Moataz Fawzy',
    description='Create Django projects and apps with layered architecture.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
