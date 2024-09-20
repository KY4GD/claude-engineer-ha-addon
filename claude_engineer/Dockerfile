ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Enable command tracing
set -x

# Install required packages
echo "Installing required packages..."
RUN apk add --no-cache python3 py3-pip git 2>&1

# Set working directory
echo "Setting working directory..."
WORKDIR /app

# Copy application files
echo "Copying application files..."
COPY . . 2>&1

# Clone Claude Engineer repository
echo "Cloning Claude Engineer repository..."
RUN git clone https://github.com/Doriandarko/claude-engineer /claude-engineer 2>&1

# Install Python dependencies
echo "Installing Python dependencies..."
RUN pip3 install --verbose -r requirements.txt 2>&1
RUN pip3 install --verbose -r /claude-engineer/requirements.txt 2>&1

# Set execute permissions
echo "Setting execute permissions..."
RUN chmod a+x run.sh 2>&1

echo "Dockerfile execution completed."

CMD [ "./run.sh" ]