from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Walk through the cyhello directory to gather all .py files to compile
def find_modules(base_dir="cyhelllo"):
    extensions = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__init__") and "tests" not in root:
                module_path = os.path.join(root, file)
                module_name = module_path[:-3].replace(os.path.sep, ".")
                extensions.append(Extension(module_name, [module_path]))
    return extensions

setup(
    name="cyhelllo",
    version="0.1.0",
    description="A Cythonized Hello World example",
    author="Abhinivesh",
    author_email="abhinivesh.s0305@email.com",
    url="https://github.com/abhinives/cyhello",
    license="Proprietary - See LICENSE file",
    packages=["cyhelllo"],
    ext_modules=cythonize(find_modules(), compiler_directives={"language_level": "3"}),
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "pytest-cov"],
    },
    classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Cython",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
],
    python_requires=">=3.9,<3.13",
    include_package_data=True,
)
