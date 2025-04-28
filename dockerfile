# Use an official lightweight Python image
FROM python:3.12

# Set the working directory
WORKDIR /app  
ENV CONTROLLER_HOST=127.0.0.1
# Copy project files into the container
COPY . /app  

# Install dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for Flask
EXPOSE 8000  