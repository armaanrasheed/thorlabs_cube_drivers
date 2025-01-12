# Thorlabs Cube Drivers

## Introduction
[Thorlabs](https://www.thorlabs.com/) products are typically controlled through their proprietary Kinesis software. However, Kinesis has limitations in terms of customizability, restricts advanced control, and lacks support for seamless integration into larger software ecosystems. 

## Solution
To address these challenges, I developed Python-based device drivers that interface directly with Thorlabs motor controllers, enabling precise control of various peripherals and allowing for enhanced programmability and integration into custom workflows.

## [NDSP (Network Device Support Package)](https://m-labs.hk/artiq/manual/developing_a_ndsp.html) Communication
In addition to the device drivers, i created a Network Device Support Package (NDSP) to instruct the controllers remotely. This package further expands the system’s flexibility, enabling distributed control across networked devices and improving remote operability for large-scale quantum computing setups. 

## Demo Video
[![SH05R Beam Shutter Control Demo](https://img.youtube.com/vi/tGyUHgEy60A/0.jpg)](https://youtu.be/tGyUHgEy60A)

This video outlines how to control the [SH05R Beam Shutter](https://www.thorlabs.com/thorproduct.cfm?partnumber=SH05R) which is being instructed by the [KSC](https://www.thorlabs.com/thorproduct.cfm?partnumber=KSC101). The control process utilizes the custom Python software package from this repository, enabling precise shutter actuation and seamless integration into automated workflows.

## Advantages of [NDSP](https://m-labs.hk/artiq/manual/developing_a_ndsp.html) Communication
The Network Device Support Package (NDSP) also extends network accessibility to previously “network-deaf” devices, such as Thorlabs motor controllers that lack built-in network capabilities. By exposing these devices on the network, NDSP enables remote communication and control, significantly enhancing their usability in distributed quantum computing systems.

# Repository Instructions

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


[ARTIQ NDSP](https://m-labs.hk/artiq/manual/developing_a_ndsp.html) for motors controlled by [Thorlabs T/K-Cube controllers](https://www.thorlabs.com/navigation.cfm?guide_id=6).
Derived from the [thorlabs_tcube](https://github.com/m-labs/thorlabs_tcube) package.
