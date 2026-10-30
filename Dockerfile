# Start with a lightweight official Python image
FROM python:3.11-slim

# Set the working directory inside the sandbox
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the rest of our project files into the sandbox
COPY . .

# Expose the port our API uses
EXPOSE 8000

# The command to start our FastAPI server inside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]