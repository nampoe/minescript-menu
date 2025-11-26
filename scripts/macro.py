import minescript
import random
import mouse
import asyncio

# Global toggle state
active = False
last_x2_state = False


async def attack_loop():
    global active, last_x2_state
    while True:
        await asyncio.sleep(0.004)

        # Detect x2 button toggle
        x2_pressed = mouse.is_pressed(button="x2")
        if x2_pressed and not last_x2_state:
            active = not active  # toggle the active state
        last_x2_state = x2_pressed

        if active:
            # Attack
            if mouse.is_pressed(button='left'):
                minescript.player_press_attack(True)
                await asyncio.sleep(random.uniform(0.066, 0.088))
                minescript.player_press_attack(False)

            # Use
            if mouse.is_pressed(button='right'):
                minescript.player_press_use(True)
                await asyncio.sleep(random.uniform(0.06,0.07))
                minescript.player_press_use(False)

async def echo_loop():
    while True:
        await asyncio.sleep(10)  # 1 second interval
        if active:
            minescript.echo("The script is active!")

async def main():
    minescript.echo("started")
    await asyncio.gather(
        attack_loop(),
        echo_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
