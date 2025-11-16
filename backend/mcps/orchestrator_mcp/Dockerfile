FROM python:3.11

# Set the working directory
WORKDIR /app

# Install dependencies first (to leverage Docker layer caching)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the orchestrator code
COPY backend/mcps/orchestrator_mcp /app/orchestrator_mcp

# Expose MCP HTTP port
EXPOSE 8000

# Set the default command to run the orchestrator
CMD ["python", "-m", "orchestrator_mcp.mcp_server"]
