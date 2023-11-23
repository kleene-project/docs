import json
from contextlib import asynccontextmanager

import httpx
import websockets
from websockets.sync.client import unix_connect

from klee.client.client import Client
from klee.client.api.default.container_create import sync_detailed as container_create
from klee.client.api.default.exec_create import sync_detailed as exec_create
from klee.client.models.container_config import ContainerConfig
from klee.client.models.exec_config import ExecConfig

kwargs = {}


def exec_start(exec_id):
    conn = unix_connect("/var/run/kleened.sock", uri="ws://localhost/exec/start")
    conn.send(json.dumps({"exec_id": exec_id, "attach": True, "start_container": True}))
    while True:
        try:
            message = conn.recv()
        except websockets.exceptions.ConnectionClosed as closed:
            print(closed)
            break

        print(message)


transport = httpx.HTTPTransport(uds="/var/run/kleened.sock")
client = Client(base_url="http://localhost")

response = container_create(
    transport=transport,
    client=client,
    **{
        "json_body": ContainerConfig.from_dict(
            {"image": "FreeBSD-13.2-STABLE:latest", "cmd": ["/bin/sh", "-c", "ls"]}
        )
    }
)

response = exec_create(
    transport=transport,
    client=client,
    **{"json_body": ExecConfig.from_dict({"container_id": response.parsed.id})}
)

exec_start(response.parsed.id)
