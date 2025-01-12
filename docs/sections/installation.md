#**Installation**

### Step 1: Clone the repository, then install using [_**pip**_](https://pip.pypa.io/en/stable/installation/):
```
$ git clone git@github.com:quantumion/thorlabs_cube.git
$ cd thorlabs_cube
```

It is suggested to create python environment using [_**venv**_](https://docs.python.org/3/library/venv.html) for repository dependencies
### Step 2: Create a Python virtual environment
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .
```
-   _**venv**_ is the standard naming convention for Python environments
- _**setup.py**_ will be targetted for the installation of all repository dependencies

### Step 3: Optionally, build MkDocs documentation
```bash
$ mkdocs serve
```
