import keyboard
import time
import random
import winsound
import sys
import asyncio
import minescript

sys.path.insert(1, 'C:/Users/jani/AppData/Roaming/.minecraft/minescript/menu/utils')
import smooth
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

moving_flag         = 1
coolflag            = 0

minrandom           = 0.05
maxrandom           =0.3

initial_delay_checked = 0

breakflag = 0

minescript.player_press_forward(False)
minescript.player_press_left(False)
minescript.player_press_backward(False)
minescript.player_press_right(False)

# --------------- movement osasto ---------------

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


 #

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

async def move_loop():
    global flag_move_forward,flag_move_left,flag_move_back,flag_move_right,moving_flag, minrandom,maxrandom,moving_flag,coolflag

    minescript.echo("mf: ", moving_flag)
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
    

# --------------- movement osasto ---------------

# --------------- anti macro check osasto ---------------


def check_y_changed():
    if cy <= y - 1 or cy >= y + 1:
        minescript.echo("stop, Y level has changed significantly")
        return True
    
def check_viewangle_changed():
    if cpitch != pitch or cyaw != yaw:
        minescript.echo("stop, Viewangle has changed")
        return True
       
def anti_macro_check(a):
    global breakflag
    if(a):
        winsound.PlaySound(ding, winsound.SND_FILENAME)

        time.sleep(random.uniform(0.2,0.5))


        minescript.player_press_attack(False)
        minescript.player_press_forward(False)
        minescript.player_press_left(False)
        minescript.player_press_backward(False)
        minescript.player_press_right(False)
        breakflag = 1

async def anti_macro_check_loop(initial_delay_checked):
    if initial_delay_checked == 0:
        await asyncio.sleep(3)

        results = [fn() for fn in checks]
        anti_macro_check(results)
        initial_delay_checked = True
        return
    else:
        return

checks = [check_y_changed, check_viewangle_changed]


# --------------- anti macro check osasto ---------------

# --------------- 👀 osasto ---------------

def get_cardinal_dir(yaw):

    yaw = yaw % 360

    if (yaw >= 315 or yaw <= 45):
        # print("south")
        return 3
    if (yaw >= 45 and yaw <= 135):
        # print("west")
        return 4
    if (yaw >= 135 and yaw <= 225):
        # print("north")
        return 1
    if (yaw >= 225 and yaw <= 315):
        # print("east")
        return 2

async def look_at_wheat():
    while True:
        return

        target2 = 31, -60.4, -9

        on_target = await smooth.look(target2, good_enough_angle = 0.1)
        if (on_target):
            break

# --------------- 👀 osasto ---------------



           
async def main():
    global cx,cz,cy,cpitch,cyaw,moving_flag,flag_move_forward,flag_move_left,flag_move_back,flag_move_right,breakflag
    d()
    moving_flag = 1
    cardinal_dir = get_cardinal_dir(cyaw)

    while True:
        if(breakflag):
            break

        await asyncio.sleep(0.1)
        cx,cy,cz    = await asyncio.to_thread(lambda: minescript.player().position)
        cpitch      = await asyncio.to_thread(lambda: minescript.player().pitch)
        cyaw        = await asyncio.to_thread(lambda: minescript.player().yaw)


        await move_loop()



async def main_loop():

    await asyncio.gather(
        moving(),
        main(),
        look_at_wheat(),
        anti_macro_check_loop(initial_delay_checked)
    )
             

if __name__ == "__main__":
    
    minescript.echo("running wheat farm")
    asyncio.run(main_loop())
    
