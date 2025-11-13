FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your MCP server code
COPY . .

# Expose FastMCP HTTP port
EXPOSE 8001

CMD ["python", "mcp_server.py"]
