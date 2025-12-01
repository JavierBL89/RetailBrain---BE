

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
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
  -H "X-Service-Token: MCP_SERVICE_TOKEN" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'


### Step 3 — Subsequent requests (paste session id to header "mcp-session-id")

 (paste session id to header "mcp-session-id"**)

## List available tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
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
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
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



## Call Insert product (MOCK DATA)

curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
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


curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
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
          "sku": "MEISABLACK",
          "category": "Boot",
          "brand": "Aldo",
          "variants": [
            {
              "variant_sku": "MEISABLACK-BLK",
              "name": "Meisa Abanico",
              "description": "Make a bold statement with these knee-high lace-up boots featuring a sleek stiletto heel. The premium leather construction and full-length lacing provide a custom fit while delivering dramatic style.",
              "category": "Boot",
              "color": "Black",
              "material": "Leather",
              "gender": "Women",
              "brand": "Aldo",
              "price": 113.0,
              "image_url": "MEISABLACK-BLK.jpg",
              "tags_string": "black knee-high boots, stiletto heel, lace-up boots, leather boots, high heel boots, women''s boots, aldo, dress, event, evening wear, statement boots, tall boots",
              "metadata": {
                "occasion": "evening wear, special occasion, party, formal event",
                "heel_type": "stiletto",
                "heel_height": "high"
              },
              "sizes": [
                { "size_label": "36", "stock_quantity": 1, "available": true },
                { "size_label": "37", "stock_quantity": 2, "available": true },
                { "size_label": "38", "stock_quantity": 3, "available": true },
                { "size_label": "39", "stock_quantity": 4, "available": true },
                { "size_label": "40", "stock_quantity": 3, "available": true },
                { "size_label": "41", "stock_quantity": 2, "available": true }
              ]
            }
          ]
        }
      }
    }
  }'

# Call fetch all products
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
-H "X-Service-Token: kalandrakatech1234" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "route_request",
        "arguments" :{
            "conversation_id": "user123-abc",
            "action": "fetch_products"
    }}
  }'

# Call delete by variant sku
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
-H "X-Service-Token: kalandrakatech1234" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "route_request",
        "arguments" :{
            "conversation_id": "user123-abc",
            "action": "delete_variant_by_sku",
            "user_query":{
              "variant_skus":  ["MEISABLACK-BLK", "ABACOGNANT-BUR"]
            }
    }}
  }'


  # Call get_top_selling_products

  curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
  -H "X-Service-Token: kalandrakatech1234" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "route_request",
      "arguments": {
        "conversation_id": "user123-abc",
        "action": "report",
        "user_query": {
          "report_type": "top_selling_products",
          "date_from": "2025-05-01",
          "date_to": "2025-11-30",
          "limit": 10,
          "group_by": "month",
          "threshold": 1,
          "product_id": null,
          "filters": {
          }
        }
      }
    }
  }'



  # Call

  curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
  -H "X-Service-Token: kalandrakatech1234" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "route_request",
      "arguments": {
        "conversation_id": "user123-abc",
        "action": "report",
    "user_query": {
      "report_type": "top_products_with_trends_over_time",
      "date_from": "2025-07-01",
      "date_to": "2025-09-30",
      "limit": 5
    }
    }
    }
  }'





curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 0e18c31bc7c74eaaa2d4b45a539ebd87" \
  -H "X-Service-Token: kalandrakatech1234" \
  -d @- <<'EOF'
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "route_request",
    "arguments": {
      "conversation_id": "user123-abc",
      "action": "insert_product",
      "products": [
          {
            "sku": "MEISABLACK",
            "brand": "Aldo",
            "category": "Boot",
            "variants": [
              {
                "name": "Meisa Abanico",
                "brand": "Aldo",
                "color": "Black",
                "price": 113.0,
                "sizes": [
                  { "available": true, "size_label": "36", "stock_quantity": 1 },
                  { "available": true, "size_label": "37", "stock_quantity": 2 },
                  { "available": true, "size_label": "38", "stock_quantity": 3 },
                  { "available": true, "size_label": "39", "stock_quantity": 4 },
                  { "available": true, "size_label": "40", "stock_quantity": 3 },
                  { "available": true, "size_label": "41", "stock_quantity": 2 }
                ],
                "gender": "Women",
                "material": "Leather",
                "metadata": {
                  "occasion": "evening wear, special occasion, party, formal event",
                  "heel_type": "stiletto",
                  "heel_height": "high"
                },
                "image_url": "MEISABLACK-BLK.jpg",
                "description": "Make a bold statement with these knee-high lace-up boots featuring a sleek stiletto heel. The premium leather construction and full-length lacing provide a custom fit while delivering dramatic style.",
                "tags_string": "black knee-high boots, stiletto heel, lace-up boots, leather boots, high heel boots, women's boots, aldo, dress, event, evening wear, statement boots, tall boots",
                "variant_sku": "MEISABLACK-BLK"
              }
            ]
          },
          {
            "sku": "ABACOGNANT",
            "brand": "Granada Norte",
            "category": "Boot",
            "variants": [
              {
                "name": "Granada Norte",
                "brand": "Granada Norte",
                "color": "Burgundy",
                "price": 99.0,
                "sizes": [
                  { "available": true, "size_label": "36", "stock_quantity": 2 },
                  { "available": true, "size_label": "37", "stock_quantity": 4 },
                  { "available": true, "size_label": "38", "stock_quantity": 6 },
                  { "available": true, "size_label": "39", "stock_quantity": 8 },
                  { "available": true, "size_label": "40", "stock_quantity": 6 },
                  { "available": true, "size_label": "41", "stock_quantity": 4 }
                ],
                "gender": "Women",
                "material": "Synthetic",
                "metadata": {
                  "occasion": "evening wear, special occasion, party, celebration",
                  "heel_type": "stiletto",
                  "heel_height": "high"
                },
                "image_url": "ABACOGNANT-BUR.jpg",
                "description": "Step into luxury with these rich burgundy knee-high boots designed for maximum impact. The streamlined silhouette and stiletto heel create an elongated leg line perfect for special occasions.",
                "tags_string": "burgundy boots, granate boots, knee-high boots, stiletto heel, synthetic boots, women's boots, red boots, evening wear, party, event, celebration, dress, tall boots",
                "variant_sku": "ABACOGNANT-BUR"
              }
            ]
          }
        ]
    }
  }
}
EOF