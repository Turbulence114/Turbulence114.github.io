import asyncio
import aiohttp
import time
from aiohttp import web

async def process_request(batch):
    await asyncio.sleep(1)
    return [f"Processed: {req}" for req in batch]

class RequestQueue:
    def __init__(self, batch_size, timeout):
        self.queue = []
        self.batch_size = batch_size
        self.timeout = timeout
        self.lock = asyncio.Lock()

    async def add_request(self, request):
        async with self.lock:
            future = asyncio.get_event_loop().create_future()
            self.queue.append((request, future))
            if len(self.queue) >= self.batch_size:
                await self.process_batch()
            return await future

    async def process_batch(self):
        async with self.lock:
            if not self.queue:
                return
            batch = [req for req, _ in self.queue]
            futures = [future for _, future in self.queue]
            self.queue.clear()
        
        results = await process_request(batch)
        
        for future, result in zip(futures, results):
            future.set_result(result)

    async def periodic_batch_processor(self):
        while True:
            await asyncio.sleep(self.timeout)
            await self.process_batch()

async def handle_request(request):
    data = await request.json()
    user_request = data.get('request')
    response = await request_queue.add_request(user_request)
    return web.json_response({'response': response})

batch_size = 16
timeout = 2  # seconds

request_queue = RequestQueue(batch_size, timeout)

loop = asyncio.get_event_loop()
loop.create_task(request_queue.periodic_batch_processor())
