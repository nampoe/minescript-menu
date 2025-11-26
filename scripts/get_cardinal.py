import minescript
import time



for _ in range(1):
    yaw,pitch = minescript.player_orientation()

    ryaw = yaw % 360
    ryaw = round(ryaw,1)
    time.sleep(0.1)
    print(ryaw)

    if (ryaw >= 315 or ryaw <= 45):
        print("south")
    if (ryaw >= 45 and ryaw <= 135):
        print("west")
    if (ryaw >= 135 and ryaw <= 225):
        print("north")
    if (ryaw >= 225 and ryaw <= 315):
        print("east")
    
x,y,z = minescript.player_position()
minescript.echo(x,y,z)