# Using SiPyCo's RPC Tool with Thorlabs Controllers

This document provides an overview of using **SiPyCo's RPC tool** (`sipyco_rpctool`) to communicate with Thorlabs controllers. SiPyCo enables seamless interaction with devices through remote procedure calls (RPC). Below is a step-by-step guide and example commands for effectively using the tool.

---

## Prerequisites

**Install SiPyCo**: Ensure that SiPyCo is installed within your [venv](https://docs.python.org/3/library/venv.html):

```bash
$ pip install git+https://github.com/m-labs/sipyco.git
```

**Running the Device Server**: Start the server that wraps the Thorlabs device driver using either Docker or locally run server

#### 1.  [Docker Container Server 🔗](docker.md)
#### 2.  [Local Server 🔗](local.md)


**Device Connectivity**: Ensure the Thorlabs device is properly connected to your system, and its driver is functioning.

---

## Commands Overview

### 1. **List Targets**

To view the available targets (endpoints) exposed by the Thorlabs driver implementation, use the `list-targets` command:

```bash
sipyco_rpctool [localhost or IP address] [port] list-targets
```

#### Example:
```bash
sipyco_rpctool localhost 5000 list-targets
```

This command will return a list of all the exposed targets that can be called via RPC.

---

### 2. **List Methods**

To view the available methods provided by a specific target, use the `list-methods` command:

```bash
sipyco_rpctool [localhost or IP address] [port] list-methods
```

#### Example:
```bash
sipyco_rpctool localhost 5000 list-methods
```

This command outputs all methods exposed by the server, detailing the API functions supported by the Thorlabs device driver.

---

### 3. **Call Methods**

To call a specific API function exposed by the Thorlabs device driver, use the `call` command. The syntax is:

```bash
sipyco_rpctool [localhost or IP address] [port] call [method_name] [arguments]
```

#### Example:
Calling a method `move_to_position` with an argument `100`:

```bash
sipyco_rpctool localhost 5000 call move_to_position 100
```

The output will display the result of the function call.

---

## Workflow Example

1. Start by listing the available targets:
```bash
$ sipyco_rpctool localhost 5000 list-targets
```

2. Select a target and view its methods:
```bash
$ sipyco_rpctool localhost 5000 list-methods
```

3. Call a specific method with the required arguments:
```bash
$ sipyco_rpctool localhost 5000 call move_to_position 150
```

---

## Notes

- **Error Handling**: If the command fails, check:
    - The device server is running and listening on the specified IP and port.
    - The Thorlabs device is connected and properly initialized.
    - The correct target and method names are used.

---

This approach simplifies interaction with Thorlabs devices using SiPyCo’s RPC mechanism, making it ideal for automation and testing setups.
