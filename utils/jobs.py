import minescript
import asyncio

async def handler():
    
    jobs = minescript.job_info()
    asyncio.sleep(0.002)
    return jobs


