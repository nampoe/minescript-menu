import minescript
import time
import asyncio
import math
import random

EYE_HEIGHT = 1.62



def get_relative_angles(target):
    px, py, pz = minescript.player_position()
    yaw0, pitch0 = minescript.player_orientation()

    ex, ey, ez = px, py + EYE_HEIGHT, pz
    x, y, z = target

    dx, dy, dz = x + 0.5 - ex, y + 0.5 - ey, z + 0.5 - ez
    horiz = math.hypot(dx, dz)

    rel_yaw = normalize(-math.degrees(math.atan2(dx, dz)) - yaw0)
    rel_pitch = normalize(-math.degrees(math.atan2(dy, horiz)) - pitch0)

    return rel_yaw, rel_pitch

def normalize(angle):
    return (angle + 180) % 360 - 180

def get_delta_angles(target):
    px, py, pz = minescript.player_position()
    yaw, pitch = minescript.player_orientation()

    ex, ey, ez = px, py + EYE_HEIGHT, pz
    dx, dy, dz = target[0] - ex, target[1] - ey, target[2] - ez

    horiz = math.hypot(dx, dz)
    desired_yaw = -math.degrees(math.atan2(dx, dz))
    desired_pitch = -math.degrees(math.atan2(dy, horiz))

    delta_yaw = normalize(desired_yaw - yaw)
    delta_pitch = normalize(desired_pitch - pitch)

    return delta_yaw, delta_pitch

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

async def look(target): # chatgpt ai pmo
    # --- tweakable realism variables ---
    max_speed = 3         # max per-frame turn
    min_speed = 1          # slow near target
    arch_strength = 6      # controls curve of motion
    micro_jitter = 0.3      # tiny hand shake
    slowdown_angle = 5       # degrees for easing near target
    good_enough_angle = 3       # kattoo millo koodi kattoo että on tarpeeks lähellä ja lopettaa aimaamise
    
    # -----------------------------------

    yaw, pitch = minescript.player_orientation()
    rel_yaw, rel_pitch = get_relative_angles(target)
    total_dist = math.hypot(rel_yaw, rel_pitch)

    if total_dist < good_enough_angle:
        return  # Already aligned

    # --- Non-linear speed curve (fast start, slow near target) ---
    speed = clamp(max_speed * (total_dist / 30), min_speed, max_speed)

    # --- Curved human-like arch using sine on relative yaw ---
    arch = math.sin(math.radians(rel_yaw * 0.7)) * arch_strength * total_dist / 20
    rel_pitch += arch

    # --- Micro jitter to simulate hand shake ---
    rel_yaw += random.uniform(-micro_jitter, micro_jitter)
    rel_pitch += random.uniform(-micro_jitter, micro_jitter)

    # --- Normalize movement vector ---
    norm = math.hypot(rel_yaw, rel_pitch)
    step_yaw = (rel_yaw / norm) * speed
    step_pitch = (rel_pitch / norm) * speed

    # --- Slow down when very close ---
    if total_dist < slowdown_angle:
        factor = total_dist / slowdown_angle
        step_yaw *= factor
        step_pitch *= factor

    # --- Apply rotation ---
    minescript.player_set_orientation(yaw + step_yaw, pitch + step_pitch)

if __name__ == "__main__":
    minescript.echo("dont run this shit bruh its a utility")