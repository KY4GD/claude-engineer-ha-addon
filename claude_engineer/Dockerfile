ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install required packages
RUN apk add --no-cache python3 py3-pip git

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Clone Claude Engineer repository
RUN git clone https://github.com/Doriandarko/claude-engineer /claude-engineer

# Install Python dependencies
RUN pip3 install -r requirements.txt
RUN pip3 install -r /claude-engineer/requirements.txt

# Set execute permissions
RUN chmod a+x run.sh

CMD [ "./run.sh" ]