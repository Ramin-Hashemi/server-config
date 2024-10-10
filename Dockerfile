# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy your Python application code into the container
COPY . /app

# Install any necessary dependencies (e.g., requirements.txt)
RUN pip install -r requirements.txt

# Expose the port your application will listen on
EXPOSE 9000

# Define the command to run your application
CMD ["python", "main.py"]

# Build the Docker Image:
#     Open your terminal and navigate to the directory containing your Dockerfile.
#     Run the following command to build the Docker image:
#     docker build -t iME .
    
#     Run the Docker Container:
#     Once the image is built, you can run a container from it:
#     docker run -p 9000:9000 iME
    
#     This maps port 9000 from the container to your host machine.
#     Access Your LLM Application:
#     Visit http://localhost:9000 in your web browser or use an API client to interact with your LLM-powered application.