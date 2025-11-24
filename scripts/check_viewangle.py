import minescript
sys.path.insert(1, '../utils')
import smooth


yaw,pitch = minescript.player_orientation()

print(yaw % 90)
print(pitch)

x,y,z = minescript.player_position()

minescript.player_look_at(31.5,-60,-8.5)