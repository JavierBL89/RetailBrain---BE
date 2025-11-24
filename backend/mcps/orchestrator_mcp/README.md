

### How to Test MCP server Communication from inside container

## Start container


## Stop and build containers

Option A
  - docker compose down
  - docker compose up --build

Option B
 - docker compose up orchestrator -d

2. Ensure containers are up and running

 - docker compose ps

## Open Container bash

- docker compose exec orchestrator bash


## Official MCP handshake flow

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
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
  -H "X-Service-Token: MCP_SERVICE_TOKEN" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'


### Step 3 — Subsequent requests (paste session id to header "mcp-session-id")

 (paste session id to header "mcp-session-id"**)

## List available tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
  -H "X-Service-Token: kalandrakatech1234" \
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
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
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
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
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
                "query": "can you help me to find a pair of sandals for my systers wedding day??, maybe around $75"
            }
        }
    }
  }'

  curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
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
                "query": "mmm maybe a light color, such us beige or gold, rather comfortable, no high heel. Shandals probably"
            }
        }
    }
  }'

 curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
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


## Call Insert product (MOCK DATA)

curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 418e95a421414e3a852dfbe97ac92ae6" \
  -H "X-Service-Token: kalandrakatech1234" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "route_request",
      "arguments": {
        "conversation_id": "user123-abc",
        "action": "insert_product",
        "product": {
          "sku": "MASTER-123",
          "category": "Footwear",
          "brand": "Kalandraka",
        "variants": [
          {
            "variant_sku": "MASTER-123-BEIGE",
            "name": "Elegant Summer Sandals",
            "description": "Light beige comfortable sandals with no heel.",
            "category": "Footwear",
            "color": "Beige",
            "material": "Leather",
            "gender": "Women",
            "brand": "Kalandraka",
            "price": 59.99,
            "image_url": "https://example.com/sandals-beige.jpg",
            "tags_string": "sandals,summer,beige,comfort",
            "sizes": [
              { "size_label": "36", "stock_quantity": 5, "available": true },
              { "size_label": "37", "stock_quantity": 8, "available": true },
              { "size_label": "38", "stock_quantity": 5, "available": true },
              { "size_label": "39", "stock_quantity": 3, "available": true },
              { "size_label": "40", "stock_quantity": 2, "available": true }
            ]
          }
        ]
        }
        }
    }
  }'
