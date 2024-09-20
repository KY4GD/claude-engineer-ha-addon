ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG=C.UTF-8 \
    PYTHON_VERSION=3.9.17 \
    PIP_VERSION=23.1.2

# Install required packages and set up environment
RUN apk add --no-cache python3=${PYTHON_VERSION}-r0 py3-pip=${PIP_VERSION}-r0 git && \
    echo "Setting working directory..." && \
    mkdir -p /app && \
    echo "Cloning Claude Engineer repository..." && \
    git clone https://github.com/Doriandarko/claude-engineer /claude-engineer

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN echo "Installing Python dependencies..." && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir -r /claude-engineer/requirements.txt && \
    echo "Setting execute permissions..." && \
    chmod a+x run.sh

CMD ["./run.sh"]