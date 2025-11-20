import minescript
import keyboard
import time
import random
import winsound
import utils.smooth as smooth
import sys
sys.path.append("..") 

ding = "C:\\Users\\jani\\Downloads\\ding.wav"


x,y,z = minescript.player().position
pitch = minescript.player().pitch
yaw = minescript.player().yaw

i = 1


while True:
    cx,cy,cz = minescript.player().position
    cpitch = minescript.player().pitch
    cyaw = minescript.player().yaw

    if cy <= y - 1 or cy >= y + 1:
        minescript.echo("stop, Y level has changed significantly")

        winsound.PlaySound(ding, winsound.SND_FILENAME)
        
        time.sleep(random.uniform(0.2,0.5))

        minescript.player_press_attack(False)
        minescript.player_press_forward(False)

        break
