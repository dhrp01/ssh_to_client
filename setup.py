from setuptools import setup, find_packages

setup(
    name="ssh-shell-client",  # Name of your package
    version="0.1.0",  # Initial version
    description="A library to establish SSH connections and execute commands interactively",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="<YOUR NAME>",  # YOUR NAME
    author_email="<YOUR EMAIL@email.com>",  # YOUR EMAIL
    url="https://github.com/dhrp01/ssh-shell-client",  # Update with your repo URL
    packages=find_packages(where="src"),  # Automatically find packages in 'src'
    package_dir={"": "src"},  # Specify the source directory
    install_requires=[
        "paramiko>=3.5.0",  # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)