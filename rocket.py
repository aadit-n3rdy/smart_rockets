#!/usr/bin/env python3

from neural_network import neural_network
import numpy as np
import enum
from obstacle import obstacle
from constants import *
import math


class ROCKET_STATUS(enum.Enum):
    ALIVE = 0
    DONE = 1
    DEAD = 2


class rocket:
    network: neural_network
    position: np.array
    velocity: np.array
    angle: float
    angular_velocity: float
    status: ROCKET_STATUS

    def __init__(self, obstacle_count, seed):
        # self.network_arg_count = obstacle_count*2 + 8
        # self.network = neural_network([self.network_arg_count, 10, 10, 2])
        self.position = start_position.copy()
        # self.velocity = np.array([start_velocity, 0.0])
        # self.angle = 0.0
        # self.angular_velocity = 0.0
        # self.status = ROCKET_STATUS.ALIVE

    def init(obstacle_count, rng):
        rkt = rocket(obstacle_count, 0)
        rkt.network_arg_count = obstacle_count*2 + 8
        (rkt.network, rng) = neural_network.init([rkt.network_arg_count, 10, 10, 2], rng)
        rkt.position = start_position.copy()
        rkt.velocity = np.array([start_velocity, 0.0])
        rkt.angle = 0.0
        rkt.angular_velocity = 0.0
        rkt.status = ROCKET_STATUS.ALIVE
        return (rkt, rng)

    def from_parent(self, parent):
        self.rng = np.random.default_rng()
        self.network.from_parent(parent.network)
        self.position = start_position.copy()
        self.velocity = np.array([start_velocity, 0.0])
        self.angle = 0.0
        self.angular_velocity = 0.0
        self.status = ROCKET_STATUS.ALIVE

    def update(self, obstacles, deltaTime):
        if self.status == ROCKET_STATUS.ALIVE:
            inp = []
            for obstacle in obstacles:
                rel_pos = np.array(obstacle.position) - self.position
                inp.append(rel_pos[0])
                inp.append(rel_pos[1])
            inp.append(target_position[0])
            inp.append(target_position[1])
            inp.append(self.position[0])
            inp.append(self.position[1])
            inp.append(self.velocity[0])
            inp.append(self.velocity[1])
            inp.append(self.angle)
            inp.append(self.angular_velocity)
            out = self.network.calculate(np.array(inp, dtype=object))
            if out[0] <= 0:
                out[0] = 0
            self.velocity[0] += out[0] * deltaTime * \
                velocity_coeff * math.cos(self.angle)
            self.velocity[1] += out[0] * deltaTime * \
                velocity_coeff * math.sin(self.angle)
            tmp = self.angular_velocity
            self.angular_velocity = tmp + \
                out[1] * deltaTime * angular_velocity_coeff
            self.position += self.velocity * deltaTime
            tmp = self.angle
            self.angle = tmp + self.angular_velocity * deltaTime
            for obstacle in obstacles:
                dx = self.position[0] - obstacle.position[0]
                dy = self.position[1] - obstacle.position[1]
                if dx**2 + dy**2 <= (obstacle.radius + rocket_radius)**2:
                    self.status = ROCKET_STATUS.DEAD
                    break
            if self.status != ROCKET_STATUS.DEAD:
                dx = self.position[0] - target_position[0]
                dy = self.position[1] - target_position[1]
                if dx**2 + dy**2 <= (target_radius + rocket_radius)**2:
                    self.status = ROCKET_STATUS.DONE
