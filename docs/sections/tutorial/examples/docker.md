# **Docker Container**

As a user, you may want to spin up a Docker container to launch your Thorlabs application and interact with it; follow the steps below to use containers to host Thorlabs controllers

### Step 1. Describe a container within _**compose.yml **_
```
container_name: ksc101
        restart: always
        ports:
            - 3255:3255
        devices:
            - /dev/kdc101:/dev/ttyUSB0
        networks:
            - thorlabs_cube
        build:
            context: ./
            dockerfile: ./Dockerfile
        # to run in simulation mode, include "--simulation"
        # in the entrypoint command after port number
        entrypoint: [aqctl_thorlabs_cube]
        command: [-p, '3255', -P, ksc101, -d, /dev/ttyUSB0, --bind, '*']
```
### Explanation of Key Elements:

- **`container_name`**
  The name given to the container, used to identify which containers are spun up.
  In this example, the container is named `ksc101`.

- **`restart`**
  Specifies the restart policy for the container. `always` ensures the container restarts automatically if it stops.

- **`ports`:**
  Maps port `3255` on the host to port `3255` inside the container. Format `<host_port>:<container_port>`

- **`devices`**
  Maps the hardware device `/dev/ksc101` on the host to `/dev/ttyUSB0` inside the container. This enables the container to access the hardware directly.

- **`networks`**
  Indicates the custom network `thorlabs_cube` to which the container belongs. This allows communication between containers in the same network.

- **`build`**
  Specifies how the container image should be built. `context` points to the build directory (here, the current directory `./`). `dockerfile` path to the Dockerfile used to build the image.

- **`entrypoint`**
  Specifies the executable that runs when the container starts. In this case, it is `aqctl_thorlabs_cube`.

- **`command`**
  Specifies additional arguments passed to the `entrypoint`.
    - `-p '3255'`: Specifies the port.
    - `-P ksc101`: Specifies the device protocol.
    - `-d /dev/ttyUSB0`: Points to the device.
    - `--bind '*'`: Allows binding to all network interfaces.

### Step 2. Build and launch the Thorlabs application with [**Docker Compose**](https://docs.docker.com/compose/):
```
$ docker compose build
$ docker compose up -d
```
* Uses the information given within the compose.yml file to build and spin up the Thorlabs application in a container
