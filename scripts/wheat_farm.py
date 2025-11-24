import keyboard
import time
import random
import winsound
import sys
import asyncio
import minescript

sys.path.insert(1, '../utils')
from smooth import look

import tracemalloc
tracemalloc.start()

ding = "C:\\Users\\jani\\Downloads\\ding.wav"


x,y,z               = minescript.player().position
pitch               = minescript.player().pitch
yaw                 = minescript.player().yaw

cx, cy, cz          = x,y,z
cpitch              = pitch
cyaw                = yaw

flag_move_forward   = 0
flag_move_left      = 0
flag_move_back      = 0
flag_move_right     = 0


moving_flag         = 0

minescript.player_press_forward(False)
minescript.player_press_left(False)
minescript.player_press_backward(False)
minescript.player_press_right(False)


def w():
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right

    minescript.player_press_forward(True)
    minescript.player_press_left(False)
    minescript.player_press_backward(False)
    minescript.player_press_right(False)
    flag_move_forward   = 1
    flag_move_left      = 0
    flag_move_back      = 0
    flag_move_right     = 0
def a():
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right

    minescript.player_press_forward(False)
    minescript.player_press_left(True)
    minescript.player_press_backward(False)
    minescript.player_press_right(False)
    flag_move_forward   = 0
    flag_move_left      = 1
    flag_move_back      = 0
    flag_move_right     = 0
def s():
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right

    minescript.player_press_forward(False)
    minescript.player_press_left(False)
    minescript.player_press_backward(True)
    minescript.player_press_right(False)
    flag_move_forward   = 0
    flag_move_left      = 0
    flag_move_back      = 1
    flag_move_right     = 0
def d():
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right

    minescript.player_press_forward(False)
    minescript.player_press_left(False)
    minescript.player_press_backward(False)
    minescript.player_press_right(True)
    flag_move_forward   = 0
    flag_move_left      = 0
    flag_move_back      = 0
    flag_move_right     = 1



def check_y_changed():
    if cy <= y - 1 or cy >= y + 1:
            minescript.echo("stop, Y level has changed significantly")

            winsound.PlaySound(ding, winsound.SND_FILENAME)
            
            time.sleep(random.uniform(0.2,0.5))

            minescript.player_press_attack(False)
            minescript.player_press_forward(False)
            
            minescript.execute(r"\killjob -1")



async def moving(rounding = 1):
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right
    while True:
        opos = [cx,cy,cz]
        opos_r = [round(p, rounding) for p in opos]

        await asyncio.sleep(0.01)

        cpos = minescript.player().position
        cpos_r = [round(p, 1) for p in cpos]

        if(opos_r != cpos_r):
            moving_flag = 1
        if(opos_r == cpos_r):
            moving_flag = 0
           
async def main():
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right
    moving_flag = 1
    d()
    coolflag = 0
    minrandom = 0.05
    maxrandom =0.3
    while True:
        await asyncio.sleep(0.1)
        cx,cy,cz    = await asyncio.to_thread(lambda: minescript.player().position)
        cpitch      = await asyncio.to_thread(lambda: minescript.player().pitch)
        cyaw        = await asyncio.to_thread(lambda: minescript.player().yaw)
        
        check_y_changed()
# ------------------ moving logic ------------------

        
        if(moving_flag == 0 and flag_move_right == 1):
            w()
            await asyncio.sleep(random.uniform(minrandom,maxrandom))
    
        if(moving_flag == 0 and flag_move_forward == 1 and coolflag == 0):
            a()
            await asyncio.sleep(random.uniform(minrandom,maxrandom))

        

        if(moving_flag == 0 and flag_move_left == 1):
            w()
            coolflag = 1
            await asyncio.sleep(random.uniform(minrandom,maxrandom))


        if(moving_flag == 0 and flag_move_forward == 1 and coolflag == 1):
            d()
            coolflag = 0
            await asyncio.sleep(random.uniform(minrandom,maxrandom))
# ------------------ moving logic ------------------
        
async def look_at_wheat():
    while True:
        target2 = 31, -60.4, -9
        await look(target2)
    
    







async def main_loop():

    await asyncio.gather(
        moving(),
        main(),
        look_at_wheat(),
    )

             


         

if __name__ == "__main__":
    
    minescript.echo("running wheat farm")
    asyncio.run(main_loop())
    
