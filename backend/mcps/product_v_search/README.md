# Tests Commands


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
  -H "mcp-session-id: 1308127115f84fc59b0b27283b39ff15" \
  -H "X-Service-Token: MCP_SERVICE_TOKEN" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'



## Call semantic_products_search
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 1308127115f84fc59b0b27283b39ff15" \
-H "X-Service-Token: kalandrakatech1234" \
  -d '{                      
    "jsonrpc": "2.0",                                      
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "semantic_product_search",
        "arguments" :{
            "conversation_id": "user123-abc",
            "user_query": {
                "query": "can you help me to find a pair of sandals for my systers wedding day??, maybe around $75"
            }
        }
    }
  }'

  curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 1308127115f84fc59b0b27283b39ff15" \
-H "X-Service-Token: kalandrakatech1234" \
  -d '{                      
    "jsonrpc": "2.0",                                      
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "semantic_products_search",
        "arguments" :{
            "conversation_id": "user123-abc",
            "user_query": {
                "query": "mmm maybe a light color, such us beige or gold, rather comfortable, no high heel. Shandals probably"
            }
        }
    }
  }'

 curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 1308127115f84fc59b0b27283b39ff15" \
-H "X-Service-Token: kalandrakatech1234" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "route_request",
        "arguments" :{
            "conversation_id": "user123-abc",
            "action": "semantic_products_search",
            "user_query": {
                "query": "beige or gold"                                         
            }
        }
    }
  }'