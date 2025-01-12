from setuptools import find_packages, setup

setup(
    name="thorlabs_cube",
    version="0.1.0",
    url="https://github.com/quantumion/thorlabs_cube",
    description="ARTIQ NDSP for Thorlabs T/K-Cube controllers",
    install_requires=[
        "sipyco@git+https://github.com/m-labs/sipyco.git@v1.8",
        "asyncserial@git+https://github.com/m-labs/asyncserial.git@1.0",
    ],
    extras_require={
        "docs": [
            "sphinx==7.3.7",
            "sphinx-argparse==0.4.0",
            "sphinx-autodoc-typehints==2.2.2",
        ],
        "lint": [
            "flake8==7.0.0",
            "flake8-bugbear==24.4.21",
        ],
        "types": [
            "mypy==1.10.0",
        ],
    },
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "aqctl_thorlabs_cube = thorlabs_cube.aqctl_thorlabs_cube:main",
        ],
    },
)
