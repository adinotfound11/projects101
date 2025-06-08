import numpy as np
import matplotlib.pyplot as plt
def fade(t):
    return 6 * t**5 - 15 * t**4 + 10 * t**3
def lerp(a, b, t):
    return a + t * (b - a)
def grad(hash, x, y):
    h = hash & 3
    if h == 0:
        return x + y
    elif h == 1:
        return -x + y
    elif h == 2:
        return x - y
    else:
        return -x - y
def perlin(x, y, perm):
    x0 = int(np.floor(x)) & 255
    y0 = int(np.floor(y)) & 255
    x1 = (x0 + 1) & 255
    y1 = (y0 + 1) & 255

    xf = x - np.floor(x)
    yf = y - np.floor(y)

    u = fade(xf)
    v = fade(yf)

    aa = perm[perm[x0] + y0]
    ab = perm[perm[x0] + y1]
    ba = perm[perm[x1] + y0]
    bb = perm[perm[x1] + y1]

    x1y1 = grad(aa, xf, yf)
    x1y2 = grad(ab, xf, yf - 1)
    x2y1 = grad(ba, xf - 1, yf)
    x2y2 = grad(bb, xf - 1, yf - 1)

    lerp_x1 = lerp(x1y1, x2y1, u)
    lerp_x2 = lerp(x1y2, x2y2, u)
    return lerp(lerp_x1, lerp_x2, v)

perm = np.arange(256, dtype=int)
np.random.seed(0)
np.random.shuffle(perm)
perm = np.tile(perm, 2)

width, height = 200, 200
scale = 20.0  
image = np.zeros((height, width))
for i in range(height):
    for j in range(width):
        x = j / scale
        y = i / scale
        image[i, j] = perlin(x, y, perm)

image = (image - image.min()) / (image.max() - image.min())
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.title("2D Perlin Noise (Grayscale)")
plt.show()
