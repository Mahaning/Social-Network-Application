# Use a slim Python 3.9 base image (adjust if needed)
FROM python:3.9

# Create a working directory within the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy your Django project code
COPY . .

# Expose the port where Django runs (usually 8000)
EXPOSE 8000

# Set the command to execute when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
