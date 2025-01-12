# Thorlabs Controllers

The following documentation define the installation, setup, usage and error forum for the QuantumION Thorlabs Controllers

## 1. [ Installation 🔗](sections/installation.md)
This section explains how to install the Thorlabs repository and setup an environment locally
## 2. [ Thorlabs Cubes 🔗](sections/cube/cube.md)
This section explains how the Thorlabs controllers work, use cases, and code examples
## 3. [ Tutorials 🔗](sections/tutorial/tutorials.md)
This section outlines how to interact with the Thorlabs Cube controllers



## Repository Layout

```
📁 .github/workflows/        # GitHub actions for CI/CD pipelines and automation
📁 docs/                     # Documentation-related files, built with MkDocs
📁 src/thorlabs_cube/
   📁 driver/                   # Drivers for the supported Thorlabs products
       📁 kcube/                    # Driver for Thorlabs K-Cube controllers
       📁 tcube/                    # Driver for Thorlabs T-Cube controllers
       📄 base.py                   # Base class for K-Cube and T-Cube drivers
       📄 message.py                # Defines enumerated constants (hex) for communication
   📄 aqctl_thorlabs_cube.py    # ARTIQ communication for controllers
📁 test/                     # Test files and test case implementations
📄 Dockerfile                # Docker container configuration
📄 compose.yml               # Multi-container setup configuration
📄 README.md                 # Project overview and guide
📄 setup.py                  # Python package setup script
📄 .pre-commit-config.yaml   # Pre-commit hooks for linting/formatting
📄 .flake8                   # Linter configuration
📄 .gitignore                # Git ignored files
📄 .dockerignore             # Docker ignored files
```
