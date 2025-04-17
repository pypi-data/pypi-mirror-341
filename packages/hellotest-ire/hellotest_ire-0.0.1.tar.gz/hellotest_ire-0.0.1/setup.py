from setuptools import setup, find_packages

setup(
    name="hellotest_ire",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description="This is my simple print package",
    author="ABS EMON",
    author_email="iotandrobotics@gmail.com",
)
