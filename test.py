import numpy as np

arr = np.arange(-10, 10.001, 0.1)

for i in range(0, 3):
    print(np.random.choice(arr, (3, 3)))

