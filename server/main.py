import asyncio
import json
import websockets

from server.config.config import HOST, PORT
from server.sinusoid import Signal


async def handler(ws):
    task_signal = None
    try:
        async for message in ws:
            if task_signal:
                task_signal.cancel()
                print(f"removed signal")

            try:
                signal = Signal.from_dict(json.loads(message))
            except Exception:
                print(f"received invalid message: {message}")
            else:
                task_signal = asyncio.create_task(signal.run(ws))
                print(f"new signal {signal}")
    except websockets.ConnectionClosedError:
        print("client closed suddenly")
    finally:
        if task_signal:
            task_signal.cancel()


async def main():
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
