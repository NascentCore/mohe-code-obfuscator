from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
import sys

def get_python_files():
    python_files = []
    skip_modules = {
        "app",
        "__main__",
        "config",
        "v1.api.dependencies",
        "v1.exceptions.files",
        "v1.repositories.files",
        "v1.schemas.files",
        "v1.schemas.errors",
        "v1.clients.bases",
    }
    for root, dirs, files in os.walk("src"):
        if "migrations" in dirs:
            dirs.remove("migrations")
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, "src"))[0].replace("/", ".")
                if module_name in skip_modules:
                    print(f"🛑 Skipping module: {module_name}")
                    continue
                python_files.append((module_name, module_path, os.path.dirname(module_path)))
    return python_files

setup(
    name="mohe",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": ["VERSION"],
    },
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "alembic",
        "psycopg2-binary",
        "python-dotenv",
        "eval_type_backport",
    ],
    ext_modules=cythonize(
        [Extension(module_name, [module_path]) for module_name, module_path, _ in get_python_files()],
        compiler_directives={
            "language_level": "3",
            "annotation_typing": False,
            "boundscheck": False,
            "wraparound": False,
            "initializedcheck": False,
            "nonecheck": False,
        },
        build_dir="build",
        include_path=["src"],
    ),
    zip_safe=False,
)