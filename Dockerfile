# Use the node base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy all the Python files into the container
COPY . .

# Install Redis server and Python Redis library
RUN apt-get update && apt-get install -y \
    redis-server

# Copy the requirements file into the container
COPY requirements.txt .

# Install required Python packages
RUN pip install -r requirements.txt

# Set environment variable for input ports
ENV INPUT_PORT=53

# Expose the input port
EXPOSE $INPUT_PORT

# Set environment variable for output ports
ENV OUTPUT_PORT=53

# Expose the output port
EXPOSE $OUTPUT_PORT

# Start Redis server and the server
CMD redis-server --bind 0.0.0.0 && python Main.py