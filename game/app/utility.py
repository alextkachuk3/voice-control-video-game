import math


def limit_coordinates(obj_pos, target_pos, radius):
    obj_x, obj_y = obj_pos
    target_x, target_y = target_pos
    distance = math.sqrt((target_x - obj_x) ** 2 + (target_y - obj_y) ** 2)

    if distance <= radius:
        return target_x, target_y

    scale = radius / distance
    new_x = obj_x + (target_x - obj_x) * scale
    new_y = obj_y + (target_y - obj_y) * scale
    return new_x, new_y