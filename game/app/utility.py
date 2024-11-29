import math
import random

import pygame as pg


def generate_nickname():
    adjectives = ["Cool", "Speedy", "Brave", "Sneaky", "Happy", "Funky"]
    nouns = ["Dragon", "Ninja", "Panda", "Tiger", "Phoenix", "Wizard"]
    number = random.randint(1, 999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{number}"


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


SIDE_DIRECTION = {
    pg.K_a: pg.math.Vector2(-1, 0),
    pg.K_w: pg.math.Vector2(0, -1),
    pg.K_s: pg.math.Vector2(0, 1),
    pg.K_d: pg.math.Vector2(1, 0),
}


def get_nearest_side(vector):
    if vector.length() != 0:
        vector = vector.normalize()

    if abs(vector.x) > abs(vector.y):
        if vector.x > 0:
            return pg.K_d
        return pg.K_a

    if vector.y > 0:
        return pg.K_s
    return pg.K_w
