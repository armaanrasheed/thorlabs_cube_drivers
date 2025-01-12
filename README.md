# Thorlabs Cube
[ARTIQ NDSP](https://m-labs.hk/artiq/manual/developing_a_ndsp.html) for motors controlled by [Thorlabs T/K-Cube controllers](https://www.thorlabs.com/navigation.cfm?guide_id=6).
Derived from the [thorlabs_tcube](https://github.com/m-labs/thorlabs_tcube) package.

## Installation
Clone the repository then install using [pip](https://pip.pypa.io/en/stable/installation/):
```sh
$ git clone git@github.com:quantumion/thorlabs_cube.git
$ cd thorlabs_cube
```

## Virtual Environment
Recommended, create virtual environment using [venv](https://docs.python.org/3/library/venv.html) for dependency isolation
```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .
```

## Usage
See the [documentation](/docs) for setup and usage instructions.

## Documentation
Recommended, build [MkDocs Documentation](https://www.mkdocs.org/):
```sh
$ mkdocs build
$ mkdocs serve
```
