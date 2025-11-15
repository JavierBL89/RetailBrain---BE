FROM python:3.11

# Set the working directory
WORKDIR /app

# Install dependencies first (to leverage Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code *only for production builds*
# (in dev, your docker-compose volume will mount the code instead)
COPY . .

# Expose MCP HTTP port
EXPOSE 8001

# Default command (can be overridden by docker-compose)
CMD ["python", "mcp_server.py"]