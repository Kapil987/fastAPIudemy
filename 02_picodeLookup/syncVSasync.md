import asyncio
import time
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

# 1. This runs natively on the Main Thread/Event Loop as a Coroutine
@app.get("/async-route")
async def fast_route():
    # The coroutine pauses here, freeing the Event Loop to handle other users
    await asyncio.sleep(1) 
    return {"message": "Handled efficiently by the Event Loop!"}

# 2. This is a blocking synchronous function
def heavy_blocking_task():
    time.sleep(2)  # Blocks for 2 seconds
    return "Done with heavy work"

@app.get("/sync-route")
async def slow_route():
    # FastAPI automatically offloads this sync function to the THREAD POOL 
    # so it doesn't freeze the Main Thread/Event Loop for other users!
    result = await run_in_threadpool(heavy_blocking_task)
    return {"message": result}