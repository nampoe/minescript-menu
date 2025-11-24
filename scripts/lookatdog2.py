import minescript
import time
import asyncio
import math
import random
import smooth

import tracemalloc

tracemalloc.start()





async def main():
    while True:
        entities = minescript.get_entities()
        for ent in entities:
            if(ent.name == "dog2"):
                x,y,z = ent.position
                target = x-0.5, y, z-0.5
                await smooth.look(target)


if __name__ == "__main__":
    asyncio.run(main())