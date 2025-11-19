import minescript
import keyboard
import time
import random
import winsound

ding = "C:\\Users\\jani\\Downloads\\ding.wav"


x,y,z = minescript.player().position
pitch = minescript.player().pitch
yaw = minescript.player().yaw

i = 1

minescript.player_press_attack(True)
minescript.player_press_forward(True)

while True:
    cx,cy,cz = minescript.player().position
    cpitch = minescript.player().pitch
    cyaw = minescript.player().yaw

    if cy <= y - 0.2 or cy >= y + 0.2:
        minescript.echo("stop, Y level has changed significantly")

        winsound.PlaySound(ding, winsound.SND_FILENAME)
        
        time.sleep(random.uniform(0.2,0.5))

        minescript.player_press_attack(False)
        minescript.player_press_forward(False)

        break

    if cpitch != pitch or cyaw != yaw:
        minescript.echo("stop, Viewangle has changed")

        winsound.PlaySound(ding, winsound.SND_FILENAME)

        time.sleep(random.uniform(0.2,0.5))


        minescript.player_press_attack(False)
        minescript.player_press_forward(False)

        break


    if(i % 13900 == 0):
        minescript.player_press_attack(False)
        time.sleep(random.uniform(0.1, 0.2))
        minescript.player_press_attack(True)
        minescript.echo("randomized +attack")


    if(i % 24090 == 0):
        minescript.player_press_forward(False)
        time.sleep(random.uniform(0.1, 0.2))
        minescript.player_press_forward(True)
        minescript.echo("randomized +w")

    
    i+=1
    time.sleep(0.001)
    