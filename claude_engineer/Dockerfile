ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG=C.UTF-8

# Install required packages and set up environment
RUN apk add --no-cache python3 py3-pip git || (echo "Failed to install packages" && exit 1)

RUN echo "Setting working directory..." && \
    mkdir -p /app || (echo "Failed to create /app directory" && exit 1)

RUN echo "Cloning Claude Engineer repository..." && \
    git clone https://github.com/Doriandarko/claude-engineer /claude-engineer || (echo "Failed to clone repository" && exit 1)

# Set working directory
WORKDIR /app

# Copy application files
ADD . .

# Install Python dependencies
RUN echo "Installing Python dependencies..." && \
    pip3 install --no-cache-dir -r requirements.txt 2>&1 || (echo "Failed to install requirements.txt" && exit 1) && \
    pip3 install --no-cache-dir -r /claude-engineer/requirements.txt 2>&1 || (echo "Failed to install claude-engineer requirements" && exit 1) && \
    echo "Setting execute permissions..." && \
    chmod a+x run.sh || (echo "Failed to set execute permissions on run.sh" && exit 1)

CMD ["./run.sh"]