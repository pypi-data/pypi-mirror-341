from setuptools import setup, find_packages

setup(
    name='onn512',
    version='0.0.3',
    author='onn512',
    description='Name reservation 😎',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.6',
)
