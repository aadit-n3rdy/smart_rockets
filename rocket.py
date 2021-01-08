#!/usr/bin/env python3

from neural_network import neural_network
import numpy as np
import enum
from constants import *

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
    def __init__(self, asteroid_count):
        network_arg_count = asteroid_count*2 + 6
        self.network = neural_network([network_arg_count, 10, 10, 2])
        self.position = start_position.copy()
        self.velocity = np.array([start_velocity, 0.0])
        self.angle = 0.0
        self.angular_velocity = 0.0
        self.status = ROCKET_STATUS.ALIVE
    def from_parent(self, parent : rocket):
        self.network.from_parent(parent.network)
        self.position = start_position.copy()
        self.velocity = np.array([start_velocity, 0.0])
        self.angle = 0.0
        self.angular_velocity = 0.0
        self.status = ROCKET_STATUS.ALIVE
    def update(self, asteroids, deltaTime):
        if self.status == ROCKET_STATUS.ALIVE:
            inp = np.array([])
            for asteroid in asteroids:
                rel_pos = asteroid.position - self.position
            inp.append(rel_pos[0])
            inp.append(rel_pos[1])
            inp.append(target_position[0])
            inp.append(target_position[1])
            inp.append(self.position[0])
            inp.append(self.position[1])
            inp.append(self.velocity[0])
            inp.append(self.velocity[1])
            inp.append(self.angle)
            inp.append(self.anglular_velocity)
            out = self.network.calculate(inp)
            self.velocity[0] += out[0] * deltaTime * velocity_coeff * np.cos(self.angle)
            self.velocity[1] += out[0] * deltaTime * velocity_coeff * np.sin(self.angle)
            self.angular_velocity += out[1] * deltaTime * angular_velocity_coeff
            self.position += self.velocity * deltaTime
            self.angle += self.angular_velocity * deltaTime
            for asteroid in asteroids:
                dx = self.position[0] - asteroid.position[0]
                dy = self.position[1] - asteroid.position[1]
                if dx**2 + dy**2 <= (asteroid.radius + rocket_radius)**2:
                    self.status = ROCKET_STATUS.DEAD
                    break
            if self.status != ROCKET_STATUS.DEAD:
                dx = self.position[0] - target_position[0]
                dy = self.position[1] - target.position[1]
                if dx**2 + dy**2 <= (target_radius + rocket_radius)**2:
                    self.status = ROCKET_STATUS.DONE
            


                
        
                        
