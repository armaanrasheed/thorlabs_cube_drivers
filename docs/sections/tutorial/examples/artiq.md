# Adding Thorlabs T/K Cube Devices to ARTIQ Device Database and Interacting via RPC

Adding Thorlabs T/K-Cube devices to the ARTIQ device database and interacting with them using `artiq_rpctool` involves the following steps.

---

## **Step 1: Set Up Your Device and Controller**
Before configuring the device database:

1. **Connect USB First, Then Power Up**: Always connect the USB cable before powering up the device to prevent it from entering a problematic state.
2. **Start the Controller**: Run the appropriate controller for your Thorlabs Cube device using the `aqctl_thorlabs_cube` command. Example for different devices:

### **TPZ001 (T-Cube Piezo Controller)**
```bash
aqctl_thorlabs_cube -P tpz001 -d /dev/ttyUSBx
```

**Notes**:
- On Windows, the `-d` argument will be of the form `COMx`.
- You can specify the device using its Vendor/Product ID and USB Serial Number with the `hwgrep` URL format:
  ```bash
  -d "hwgrep://<VID>:<PID> SNR=<serial_number>"
  ```

---

## **Step 2: Add Device to the ARTIQ Device Database**
Modify the `device_db.py` file to include an entry for the Thorlabs device. For example:

```python
device_db = {
    # Core device configuration

    "core": {
        "type": "local",
        "module": "artiq.coredevice.core",
        "class": "Core",
        "arguments": {
            "host": "192.168.1.100",  # Replace with your host device's IP
        }
    },

    # Thorlabs TPZ001 Controller

    "thorlabs_tpz001": {
        "type": "controller",
        "host": "localhost",         # Replace with the IP of the controller
        "port": 3255,                # Port where the Thorlabs controller listens
        "target": "tpz001",          # Controller target name
        "command": "aqctl_thorlabs_cube -P tpz001 -d /dev/ttyUSB0",
    }
}
```

### Explanation:
- **`type`**: Set to `controller` for remote (non-real-time) devices.
- **`host`**: Set to `localhost` if the controller is running on the same machine or the IP of the machine hosting the controller.
- **`port`**: TCP port the controller is listening on (`3255` in this example).
- **`target`**: The target name (use `artiq_rpctool ::1 <port> list-targets` to confirm).
- **`command`**: Command to start the controller.

---

## **Step 3: Interact with the Device Using `artiq_rpctool`**
You can send commands to the Thorlabs device via the `artiq_rpctool` utility. Below are examples for different devices.

### **TPZ001 (T-Cube Piezo Controller)**
```bash
artiq_rpctool ::1 3255 list-targets
artiq_rpctool ::1 3255 call set_output_volts 15   # Set output voltage to 15 V
artiq_rpctool ::1 3255 call get_output_volts      # Read back output voltage
artiq_rpctool ::1 3255 call set_tpz_io_settings 150 1 # Set max output voltage to 150 V
artiq_rpctool ::1 3255 call close                 # Close the device
```

---

## **Step 4: Verify and Debug with `artiq_rpctool`**

1. **List Targets**:

```bash
$ artiq_rpctool ::1 3255 list-targets
```
   Output example:
   ```
   Target(s):   kdc101
   ```

2. **List Available Methods**:
```bash
$ artiq_rpctool ::1 3255 list-methods
```

3. **Call a Method**:
```bash
$ artiq_rpctool ::1 3255 call move_relative 10000
```

---

## **Notes**
1. **Persistent Device Database**:
   After modifying `device_db.py`, update the ARTIQ master:
   ```bash
   artiq_client scan-devices
   ```

2. **Controller State**:
   Ensure the controller is running and listening on the configured port (`aqctl_thorlabs_cube` should still be active).

3. **Troubleshooting**:
   - If the device is unresponsive, ensure USB is connected before power-up.
   - Use `--help` with `aqctl_thorlabs_cube` for detailed command-line options.

---
