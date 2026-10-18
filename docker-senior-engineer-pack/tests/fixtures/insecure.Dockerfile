# Synthetic test fixture for tooling/container_lint.py. Deliberately insecure; never build it.
# Every value below is fake.
FROM ubuntu:latest
MAINTAINER fixture@example.invalid
ARG NPM_TOKEN
ENV DB_PASSWORD=synthetic-not-a-real-secret \
    LOG_LEVEL=debug
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://example.invalid/install.sh | sh
ADD https://example.invalid/tool.tar.gz /opt/
WORKDIR /app
COPY . .
RUN chmod -R 777 /app
USER root
CMD node server.js
