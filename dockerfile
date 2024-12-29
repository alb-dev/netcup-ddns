# Use Debian slim as the base image
FROM python:3.13.1-slim-bookworm AS compiler

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.13.1-slim-bookworm AS runner

# OS Updates for images
RUN apt-get update && apt upgrade -y && apt-get clean && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY ./ddns.py /app/

# Set the entrypoint to run the script
ENTRYPOINT ["python", "/app/ddns.py"]


