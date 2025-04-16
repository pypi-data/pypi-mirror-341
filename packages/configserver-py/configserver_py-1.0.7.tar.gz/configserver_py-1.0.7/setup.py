from setuptools import setup, find_packages

setup(
    name="configserver-py",
    version="1.0.7",
    description="A Python library for consuming Spring Cloud Config Server and managing configurations.",
    author="Luis Martinez",
    author_email="linuxlondo1211@gmail.com",
    url="https://github.com/your-repo/backstage-lib",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
