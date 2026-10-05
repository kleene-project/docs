import httpx

from klee.client.api.default.container_stop import sync_detailed as container_stop
from klee.client.client import Client

response = container_stop(
    httpx.HTTPTransport(uds="/var/run/kleened.sock"),
    client=Client(base_url="http://localhost"),
    **{"container_id": "7f5175d852d5"}
)

print(response.parsed.id)
