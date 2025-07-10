# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy server script
COPY server.py .

# Install Flask
RUN pip install Flask

# Expose port
EXPOSE 5000

# Command to run the server
CMD ["python", "server.py"]