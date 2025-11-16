### How to Test Communication between MCP servers

1. Ensure containers are up and running

 - docker compose ps

2. Test it from inside the client container

E.g:
- docker compose exec orchestrator bash

3. Ping the server to reach to

 - curl http://product-vector-search:8000/health

If deines health() tool, we can JSON-GPR it directly:

- curl -X POST http://service-name:PORT/mcp \
  -H "Content-Type: application/json" \
  -H "X-Service-Token: $MCP_SERVICE_TOKEN" \
  -d '{"jsonrpc": "2.0", "id": "1", "method": "tools/health", "params": {}}'

