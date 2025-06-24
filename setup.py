from setuptools import setup, find_packages

setup(
    name="jobtracker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "python-multipart",
    ],
)
