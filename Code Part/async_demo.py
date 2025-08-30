import time
import asyncio
from timeit import default_timer as timer

async def run_task(name, seconds):
    print(f"{name} Starting task: {timer()}")
    await asyncio.sleep(seconds)
    print(f"{name} Completed task: {timer()}")

async def main():
    start = timer()
    await asyncio.gather(
        run_task("Task 1", 2),
        run_task("Task 2", 3),
        run_task("Task 3", 1)
    )
    print(f"All tasks completed in: {timer() - start:.2f} seconds")
    
asyncio.run(main())