from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="drf-builder",
    version="0.1.0",
    author="Caio Ferreira, Eliandro de Souza, João Alves",
    author_email="caio.tomaz@alunos.ifsuldeminas.edu.br",
    description="API dinâmica para Django que gera endpoints RESTful automaticamente para qualquer modelo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/campusinteligente/drf-builder",
    project_urls={
        "Bug Tracker": "https://github.com/campusinteligente/drf-builder/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "."},
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "django>=3.0",
        "djangorestframework>=3.11.0",
        "django-filter>=21.1",
        "djangorestframework-simplejwt>=5.2.2",  # Added simplejwt dependency
    ],
    keywords="django, api, rest, dynamic, drf, automatic, endpoints",
)