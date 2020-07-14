# STAGE: base
# -----------
# The base image (intermediate).
FROM laudio/pyodbc:1.0.33 AS base

WORKDIR /source

COPY ["setup.py", "README.md", "./"]
COPY ["musicrs", "./musicrs"]

RUN pip install .

# STAGE: main
# -----------
# The main image that is published.
FROM base AS main

# STAGE: test
# -----------
# Image used for running tests.
FROM base AS test


RUN apt-get update \
  && apt-get install -y curl xz-utils \
  && curl -O https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz \
  && mkdir -p /usr/local/lib/nodejs \
  && tar -xJf node-v${NODE_VERSION}-linux-x64.tar.xz -C /usr/local/lib/nodejs \
  && rm node-v${NODE_VERSION}-linux-x64.tar.xz \
  && apt-get remove -y curl libcurl4 libnghttp2-14 libpsl5 librtmp1 libssh2-1 publicsuffix xz-utils \
  && apt-get autoremove -y \
  && apt-get autoclean -y \
  && rm -rf /var/lib/apt/lists/*


COPY ["./"]

RUN pip install .[dev] 

COPY ["tests", "./"]

# Test the code is good, types are safe and tests are passing.
CMD \
  echo "\nRUNNING CODE STYLE CHECK (BLACK)" && black --check --diff . && \
  echo "\nRUNNING TESTS" && pytest -vvv
