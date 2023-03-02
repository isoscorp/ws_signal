import asyncio
import json
import math
import time
from dataclasses import dataclass

import websockets


@dataclass
class Signal:
    amplitude: float
    frequency: float

    @classmethod
    def from_dict(cls, data: dict) -> "Signal":
        return cls(amplitude=float(data["a"]), frequency=float(data["f"]))

    def compute(self):
        t = time.time()
        return self.amplitude * math.sin(self.frequency * t / 100), t

    async def run(self, ws):
        while True:
            try:
                v, t = self.compute()
                await ws.send(json.dumps({"v": v, "t": t}))
                await asyncio.sleep(1)
            except websockets.ConnectionClosedOK:
                break

