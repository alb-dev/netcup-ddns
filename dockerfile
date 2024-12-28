# Use Debian slim as the base image
FROM debian:bookworm-20241223-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install Python and required dependencies
RUN apt-get update && apt upgrade -y && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && apt-get clean && apt autoremove && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install requests

# Copy the script into the container
COPY ddns.py /app/ddns.py


# Set the entrypoint to run the script
ENTRYPOINT [\"python3\", \"/app/ddns.py\"]