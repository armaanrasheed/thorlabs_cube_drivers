# Starting a Local Server for Thorlabs Application

To start a local server to run the Thorlabs application using the `aqctl_thorlabs_cube.py` module, you need the following components:

1. **Module**: The `aqctl_thorlabs_cube.py` file must be targeted as the module.
2. **Port**: Specify a port for the server to listen on.
3. **Product Identifier**: Provide a valid product identifier (e.g., `ksc101`).
4. **Device Address**: Indicate the address where the hardware is connected (e.g., `/dev/ttyUSB0`).

---

## Command Syntax

The command follows this structure:

```bash
python3 -m thorlabs_cube.aqctl_thorlabs_cube -p [port] --product [product_identifier] --device [device_address]
```

---

## Example Command

Here is an example of starting the server:

```bash
python3 -m thorlabs_cube.aqctl_thorlabs_cube -p 3257 --product ksc101 --device /dev/ttyUSB0
```

- **`-m thorlabs_cube.aqctl_thorlabs_cube`**: Specifies the module to run.
- **`-p 3257`**: The server listens on port `3257`.
- **`--product ksc101`**: The product identifier for the Thorlabs device (e.g., `ksc101` for a stepper motor controller).
- **`--device /dev/ttyUSB0`**: The system address where the hardware is connected (e.g., `/dev/ttyUSB0` for Linux).

---

## Key Points

1. **Virtual Environment**: Ensure you activate your Python virtual environment if required before running the command.
   ```bash
   source venv/bin/activate
   ```
2. **Port Availability**: Make sure the specified port (e.g., `3257`) is available and not used by another application.
3. **Device Connection**: Verify the hardware is connected and accessible via the specified address (e.g., `/dev/ttyUSB0`).

---

## Supported Device Drivers

The following are the currently supported device drivers. These are the strings to use with the `--product` flag:

- `tdc001` (T-Cube DC Servo Driver)
- `kdc101` (K-Cube DC Servo Motor Driver)
- `tpa101` (T-Cube Piezo Actuator Driver)
- `kpa101` (K-Cube Piezo Actuator Driver)
- `tpz001` (T-Cube Piezo Controller)
- `kpz101` (K-Cube Piezo Controller)
- `tsc001` (T-Cube Stepper Controller)
- `ksc101` (K-Cube Stepper Controller)

---

With this setup, the local server should start successfully, allowing you to communicate with the Thorlabs device using SiPyCo's RPC or ARTIQ.
