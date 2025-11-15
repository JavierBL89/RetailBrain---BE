pip install watchdog
watchmedo auto-restart --directory=. --pattern="*.py" --recursive python mcp_server.py



## Start container

 - docker compose up orchestrator -d
 

 # Official MCP handshake flow

 We must send a JSON-RPC 2.0 request with the proper method and fields

### Step 1 — Establish the SSE connnectin by creating a new session and capture its ID
SESSION=$(curl -sD - \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-10-05","capabilities":{},"clientInfo":{"name":"manual-client","version":"0.0.0"}}}' \
  http://localhost:8000/mcp |
  grep -i "mcp-session-id" | awk '{print $2}' | tr -d '\r')

echo "Session ID: $SESSION"

### Step 2 - Notify about the initialization:
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 7528a13672404021bba2e52b7b600eef" \
  -H "X-Service-Token: MCP_SERVICE_TOKEN" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'


### Step 3 — Subsequent requests (paste session id to header "mcp-session-id")

### paste session id to header "mcp-session-id"

## List available tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 7528a13672404021bba2e52b7b600eef" \
  -H "X-Service-Token: MCP_SERVICE_TOKEN" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/list",
    "params": {
    }
  }'

## Call your health tool
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 7528a13672404021bba2e52b7b600eef" \
  -H "X-Service-Token: kalandrakatech1234" \
  -d '{
  "jsonrpc": "2.0",
  "id": "2",
  "method": "tools/call",
  "params": {
    "name": "health",
    "arguments": {}
  }
}'

## Call echo with an argument
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: SESSION_ID" \
  -H "X-Service-Token: MCP_SERVICE_TOKEN" \
  -d '{
  "jsonrpc": "2.0",
  "id": "2",
  "method": "tools/call",
  "params": {
    "session_id": "default",
    "name": "echo",
    "arguments":  {message": "hola"}
  }
}'


## Call semantic_products_search
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 7528a13672404021bba2e52b7b600eef" \
    -H "X-Service-Token: kalandrakatech1234" \
  -d '{                      
    "jsonrpc": "2.0",                                      
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "semantic_products_search",
        "arguments": {
            "user_query": {
            "query": "I need stylish summer sandals, maybe around $75"
        }
      }
    }
  }'
