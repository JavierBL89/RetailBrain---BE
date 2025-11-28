FROM python:3.11

# Set the working directory
WORKDIR /app

ENV PYTHONPATH="/app:${PYTHONPATH}"

# Install dependencies first (to leverage Docker layer caching)
COPY mcps/orchestrator_mcp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the code *only for production builds*
# (in dev, your docker-compose volume will mount the code instead)
COPY . .

# Expose MCP HTTP port
EXPOSE 8000

CMD ["python", "mcps/orchestrator_mcp/mcp_server.py"]
