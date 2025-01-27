import numpy as np
import random
import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull
from datetime import datetime
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def generate_3d_points(num_points):
    return [(random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_points)]

def plot_convex_hull_3d(points, hull):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='black', label='Points')

    for simplex in hull.simplices:
        vertices = points[simplex]
        face = Poly3DCollection([vertices], color='red', alpha=0.5, edgecolor='black')
        ax.add_collection3d(face)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title("3D Convex Hull")
    plt.legend()
    plt.savefig('diagram/quick_hull_3d.png')


if __name__ == "__main__":
    points = np.array(generate_3d_points(80))

    start_time = datetime.now()
    hull = ConvexHull(points)
    convex_hull_points = points[hull.vertices]
    end_time = datetime.now()
    elapsed_time = end_time - start_time

    print("Elapsed Time:", elapsed_time)
    plot_convex_hull_3d(points, hull)