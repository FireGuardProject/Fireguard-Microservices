# Use the official Python 3.12 image as a base image
FROM python:3.12

# Set the working directory to /app
WORKDIR /app

# Copy the project files into the container at /app
COPY . .

# Install pipx and Poetry globally
RUN pip install pipx \
    && pipx install poetry

# Use Poetry to install the dependencies
RUN /root/.local/bin/poetry install --no-dev

# Expose the port the app runs on
EXPOSE 8000

# Command to run on container start, adjust the module path as needed
CMD ["/root/.local/bin/poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
