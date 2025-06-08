import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex

# --- MATRIX TRANSFORMATIONS ---
def scale_matrix(sx, sy):
    """Creates a scaling matrix."""
    return np.array([[sx, 0], [0, sy]])

def rotation_matrix(theta):
    """Creates a rotation matrix."""
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

def shear_matrix(shx, shy):
    """Creates a shear transformation matrix."""
    return np.array([[1, shx], [shy, 1]])

# --- PERLIN NOISE GENERATION ---
def generate_perlin_noise(width, height, scale, rotation=0, shear_x=0, shear_y=0, octaves=4, persistence=0.5, apply_transform=True):
    """
    Generates Perlin noise with or without matrix transformations.

    Parameters:
    - width, height: Dimensions of the noise map.
    - scale: Controls feature size.
    - rotation: Rotation angle (in radians).
    - shear_x, shear_y: Shearing values.
    - octaves: Number of noise layers for added complexity.
    - persistence: Controls amplitude reduction per octave.
    - apply_transform: Whether to apply the matrix transformation.
    """
    noise = np.zeros((height, width))
    simplex = OpenSimplex(seed=np.random.randint(0, 100000))  # Random seed for variety

    if apply_transform:
        # Compute transformation matrix: Scaling -> Rotation -> Shear
        transform = shear_matrix(shear_x, shear_y) @ rotation_matrix(rotation) @ scale_matrix(scale, scale)
    else:
        transform = np.eye(2)  # Identity matrix (no transformation)

    for y in range(height):
        for x in range(width):
            point = np.array([x / width, y / height])  # Normalize points
            transformed_point = transform @ point  # Apply transformation

            # Multi-octave noise combination
            amplitude = 1
            frequency = 1
            value = 0
            for _ in range(octaves):
                value += amplitude * simplex.noise2(transformed_point[0] * frequency, transformed_point[1] * frequency)
                amplitude *= persistence
                frequency *= 2

            noise[y, x] = value

    # Normalize to 0-1 range
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    return noise

# --- TERRAIN VISUALIZATION ---
def plot_terrain(noise1, noise2):
    """Plots the original vs transformed terrain side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    axes[0].imshow(noise1, cmap='terrain', interpolation='bilinear')
    axes[0].set_title("Original Perlin Noise Terrain")
    axes[0].axis("off")

    axes[1].imshow(noise2, cmap='terrain', interpolation='bilinear')
    axes[1].set_title("Transformed Perlin Noise Terrain")
    axes[1].axis("off")

    plt.show()

# --- RANDOMIZATION ---
width, height = 512, 512  # Resolution
scale = np.random.uniform(3, 10)  # Random scale factor
rotation = np.random.uniform(0, np.pi / 2)  # Random rotation (0° to 90°)
shear_x, shear_y = np.random.uniform(0, 0.3), np.random.uniform(0, 0.3)  # Random shearing values

# Generate terrains
terrain_original = generate_perlin_noise(width, height, scale, 0, 0, 0, apply_transform=False)  # No transformation
terrain_transformed = generate_perlin_noise(width, height, scale, rotation, shear_x, shear_y, apply_transform=True)  # With transformation

# Compare results
plot_terrain(terrain_original, terrain_transformed)

# Print transformation values for reference
print(f"Scale Factor: {scale:.2f}")
print(f"Rotation (Degrees): {np.degrees(rotation):.2f}")
print(f"Shear X: {shear_x:.2f}, Shear Y: {shear_y:.2f}")
