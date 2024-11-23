import pygame as pg


from app.base.tail_map_builder import TailMapBuilder

def get_random_background(path, bg_size, tai_size, fill=(0, 0)):
    tail_w, tail_h = tai_size
    image = pg.image.load(path).convert_alpha()
    image.set_colorkey("black")
    builder = TailMapBuilder(image, bg_size, (tail_w, tail_h))
    builder.fill(fill).fill_random()

    return builder.tail_map()