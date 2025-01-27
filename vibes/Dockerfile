# Use an official Python image with a specific version for consistency
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first for leveraging Docker caching
COPY requirements.txt ./

# Install system dependencies and Python requirements
RUN apk add --no-cache build-base gcc libffi-dev musl-dev postgresql-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY .. .

# Run database migrations during the build process
#RUN python manage.py migrate

# Expose the port the app will run on
EXPOSE 8000

# Command to run the Django development server
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "vibes.wsgi.application"]

