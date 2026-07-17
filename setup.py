from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-drift_monitoring_pipeline",
    version="0.1",
    author="Salma Ahmed",
    packages=find_packages(),
    install_requires = requirements,
)