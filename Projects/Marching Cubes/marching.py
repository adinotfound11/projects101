import numpy as np
import pyvista as pv
from itertools import product

# Step 1: Define the marching cubes lookup table
# This lookup table determines the possible ways a cube can be triangulated.
# For simplicity, we will use a minimal version of this table.

# Define the edge table for 3D cubes
EDGE_TABLE = [
    0x0, 0x109, 0x103, 0x10A, 0xF, 0x106, 0x100, 0x107, 0xF8, 0x1, 0x9, 0x8, 0xA, 0x6, 0x3, 0x5, 0xC
]

# Step 2: Interpolation function to find the intersection point of the surface
def interpolate(p1, p2, valp1, valp2, iso_value):
    if abs(iso_value - valp1) < 1e-5:
        return p1
    if abs(iso_value - valp2) < 1e-5:
        return p2
    if abs(valp1 - valp2) < 1e-5:
        return p1
    t = (iso_value - valp1) / (valp2 - valp1)
    return p1 + t * (p2 - p1)

# Step 3: Marching cubes algorithm to generate the mesh from a scalar field
def marching_cubes(grid, iso_value):
    # Create the output list of triangles
    triangles = []

    # Get grid dimensions
    nx, ny, nz = grid.shape

    # Traverse all cubes in the grid (excluding boundaries)
    for i, j, k in product(range(nx - 1), range(ny - 1), range(nz - 1)):
        # 8 corners of a cube
        cube = grid[i:i+2, j:j+2, k:k+2]

        # Generate the index based on the corners of the cube and the iso_value
        cube_index = 0
        for idx, corner in enumerate(product([0, 1], repeat=3)):
            x, y, z = corner
            if cube[x, y, z] < iso_value:
                cube_index |= (1 << idx)

        # Get edges based on the cube index
        edge_mask = EDGE_TABLE[cube_index]

        # If no edges are activated, continue
        if edge_mask == 0:
            continue

        # List of vertex positions for this cube
        vertices = []

        # Interpolate edges
        for edge in range(12):
            if edge_mask & (1 << edge):
                # Interpolate the position of the intersection point for this edge
                v0, v1 = get_edge_vertices(edge)
                p0, p1 = grid[i + v0[0], j + v0[1], k + v0[2]], grid[i + v1[0], j + v1[1], k + v1[2]]
                vertices.append(interpolate(np.array([i + v0[0], j + v0[1], k + v0[2]]),
                                            np.array([i + v1[0], j + v1[1], k + v1[2]]),
                                            p0, p1, iso_value))

        # Create triangles (assuming there are up to 5 possible triangles per cube)
        for triangle in get_triangle_indices(cube_index):
            triangles.append([vertices[i] for i in triangle])

    return triangles

# Step 4: Get edge vertices (define the connections between the corners of the cube)
def get_edge_vertices(edge):
    edge_vertices = [
        [(0, 0, 0), (1, 0, 0)],  # Edge 0
        [(1, 0, 0), (1, 1, 0)],  # Edge 1
        [(1, 1, 0), (0, 1, 0)],  # Edge 2
        [(0, 1, 0), (0, 0, 0)],  # Edge 3
        [(0, 0, 1), (1, 0, 1)],  # Edge 4
        [(1, 0, 1), (1, 1, 1)],  # Edge 5
        [(1, 1, 1), (0, 1, 1)],  # Edge 6
        [(0, 1, 1), (0, 0, 1)],  # Edge 7
        [(0, 0, 0), (0, 0, 1)],  # Edge 8
        [(1, 0, 0), (1, 0, 1)],  # Edge 9
        [(1, 1, 0), (1, 1, 1)],  # Edge 10
        [(0, 1, 0), (0, 1, 1)]   # Edge 11
    ]
    return edge_vertices[edge]

# Step 5: Triangle indices for each possible cube configuration
def get_triangle_indices(cube_index):
    # This function returns the list of triangle indices for each case
    # For simplicity, we return a few predefined configurations (not the full table)
    # These should be taken from a full Marching Cubes lookup table.
    triangles = {
        0: [],
        1: [[0, 8, 3]],
        2: [[0, 1, 9]],
        3: [[1, 8, 3], [1, 9, 8]],
        4: [[1, 2, 10]],
        5: [[0, 8, 3], [1, 2, 10]],
    }
    return triangles.get(cube_index, [])

# Step 6: Visualize the result using PyVista
def visualize_mesh(triangles):
    # Convert triangles to vertices and faces for PyVista
    vertices = np.array([t for triangle in triangles for t in triangle])
    faces = np.array([3] * len(triangles))  # 3 vertices per triangle

    mesh = pv.PolyData(vertices)
    mesh.faces = np.hstack([[3] + list(tri) for tri in triangles])

    # Plot the mesh
    mesh.plot(show_edges=True)

# Step 7: Generate and visualize an example 3D grid
def create_example_grid():
    # Create a simple 3D scalar field (a sphere)
    x, y, z = np.meshgrid(np.linspace(-1, 1, 30),
                          np.linspace(-1, 1, 30),
                          np.linspace(-1, 1, 30))
    grid = np.sqrt(x**2 + y**2 + z**2)
    return grid

# Main function to run the marching cubes
def main():
    # Create example grid (sphere)
    grid = create_example_grid()

    # Apply marching cubes to generate the mesh at iso_value = 0.5
    iso_value = 0.5
    triangles = marching_cubes(grid, iso_value)

    # Visualize the result
    visualize_mesh(triangles)

if __name__ == "__main__":
    main()