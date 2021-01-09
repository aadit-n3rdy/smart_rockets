import numpy as np

window_width = 800
window_height = 600
accel_coeff = 1.0
torque_coeff = 1.0
velocity_coeff = 0.5
angular_velocity_coeff = 1.0
start_velocity = 10.0
start_position = np.array([0.0, window_width/2.0])
rocket_radius = 44.0
target_position = np.array([window_height, 0.0])
target_radius = 30.0

