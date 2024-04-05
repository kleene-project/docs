import httpx

from klee.client.api.default.image_list import sync_detailed as image_list
from klee.client.client import Client

kwargs = {}

response = image_list(
    httpx.HTTPTransport(uds="/var/run/kleened.sock"),
    client=Client(base_url="http://localhost"),
    **kwargs
)
for image in response.parsed:
    print(image.id)
