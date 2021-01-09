#!/usr/bin/env python3

import numpy as np
import pygame as pg
from constants import window_height, window_width
from rocket import rocket
from obstacle import obstacle
from global_rng import rng
import global_rng

pg.init()
screen_size = (window_width, window_height)
screen = pg.display.set_mode(screen_size)

rocket_img = pg.transform.smoothscale(pg.image.load(
    'rocket.png').convert_alpha(), (253//4, 439//4))
obstacle_img = pg.transform.smoothscale(
    pg.image.load('obstacle.png').convert_alpha(), (200, 200))
obst = obstacle([window_width//2, window_height//2], 50)
rng = np.random.default_rng()
rockets = []
(tmp, rng) = rocket.init(1, rng)
rockets.append(tmp)
(tmp, rng) = rocket.init(1, rng)
rockets.append(tmp)
(tmp, rng) = rocket.init(1, rng)
rockets.append(tmp)

done = False
if rockets[0].network.weights[0].flat[0] == rockets[1].network.weights[0].flat[0]:
    print("ERROR: STUPID WEIGHTS ARE EQUAL")
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    screen.fill((25, 25, 25))
    for rocket in rockets:
        rocket_rotated_img = pg.transform.rotate(
            rocket_img, rocket.angle - np.pi/2.0)
        rocket_rect = rocket_rotated_img.get_rect(
            center=(rocket.position[0] + rng.uniform(-10, 10), rocket.position[1]))
        screen.blit(rocket_rotated_img, rocket_rect)
        rocket.update([obst], 0.1)
    obstacle_rect = obstacle_img.get_rect(
        center=(obst.position[0], obst.position[1]))
    # new_rect = new_rect.move(angle*0.1, angle*0.1)
    screen.blit(obstacle_img, obstacle_rect)
    pg.display.flip()
