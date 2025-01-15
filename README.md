# Create a python package
This repo includes steps need to create an installable python package. Source includes a simple ssh connection script. Unit test has been added to verify the code remain functional.

## Steps
1. Ensure the repo structure matches as below
                repo/
                |--src/
                |----package name
                |------__init__.py
                |------source code
                |--tests/
                |----__init__.py
                |----test file
                |--setup.py
                |--pyproject.toml
                |--README.md
                |--LICENSE
                |--requirements.txt

2. Create `src\<package name>`. This marks the `<package name>` directory as a Python package. Create test files inside `tests` directory to ensure that the core code (`src\<package name>`) remains functional even if there are any changes made down the line.

2. Create `setup.py` and add the given code. This file defines metadata and configuration for your Python package. It specifies the package name, version, description, author details, dependencies, and more. It will be used by tools like pip and setuptools to build and install your package. Make changes as need. For further explaination visit python [documentation](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#setup-args)

3. Create `pyproject.toml`. A typical pyproject.toml file includes at least a `[build-system]` table, and optionally others like `[tool.*]` for tool-specific configurations. [build-system] section is mandatory and specifies the tools required to build your package. For further reading please check pip documentation for [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)

4. Add `requirements.txt` listing all dependencies required for your project

5. Add `README.md`. It provides a detailed overview of your project.

7. Add `LICENCE`. It specifies the legal terms under which your package can be used and distributed.

8. Optionally, add `.gitignore` file with the needed files and directories that are to be excluded from the versioning.

6. Build package using below commands
    ```
    pip install setuptools wheel
    python setup.py sdist bdist_wheel
    ```
    This will create `.tar.gz` and `.whl` files in the `dist/` directory. `dist/` contains the built distribution files of your package.

7. Install package
    ```
    pip install ./dist/ssh_shell_client-0.1.0-py3-none-any.whl
    ```

To publish a package you will need to install `twine` and have [PyPI](https://pypi.org/) account. For Further documentation visit Python Guide for [Packaging and distributing projects](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)

### Running the SSH connection code
1. ```cd src/ssh_shell/```
2. python code to establish ssh connection to a client using paramiko
ssh_shell.py will establish ssh connection to your client. 
Command: 
```python ssh_shell.py -ht <hostname_of_your_machine> -u <username_of your_machine> -o <password_of_username> -pt <port_number_for_machine>```

### Running tests
1. ```python -m unittest test.test_ssh_shell```
