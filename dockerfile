# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app
# Copy the application files (including .env)
COPY . /app


# Install dependencies (including python-dotenv)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask application
CMD ["python","app.py"]
