FROM python:3.12-rc-slim-bookworm
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install base tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git=1:2.39.5-0+deb12u1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --upgrade pip==24.1

WORKDIR /app
COPY . .

RUN python -m pip install --no-cache-dir .

ENTRYPOINT ["aqctl_thorlabs_cube"]
CMD ["-p", "3255", "-P", "kpz101", "-d", "/dev/ttyUSB0", "--bind", "*"]
