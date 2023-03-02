import asyncio
import json

import websockets

from server.config.config import HOST, PORT

URL = f"ws://{HOST}:{PORT}"


async def run_client(id, *, a, f):
    async with websockets.connect(URL) as ws:
        await ws.send(json.dumps({"a": a, "f": f}))
        async for message in ws:
            print(f"client {id} received {message}")


async def main():
    clients = [
        dict(a=1, f=1),
        dict(a=1, f=2),
        dict(a=1, f=1),
        dict(a=3, f=3),
    ]
    cor_clients = [run_client(id, **kwargs) for id, kwargs in enumerate(clients)]
    await asyncio.gather(*cor_clients)


if __name__ == "__main__":
    asyncio.run(main())
