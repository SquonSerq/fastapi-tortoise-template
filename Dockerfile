# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.3.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the working directory
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
RUN poetry install --no-root

# Copy the application code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
