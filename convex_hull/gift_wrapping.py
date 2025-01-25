import matplotlib.pyplot as plt
import random
from datetime import datetime

def are_collinear(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (x2 - x1) * (y3 - y1) == (y2 - y1) * (x3 - x1)

def check_collinearity(points):
    num_points = len(points)
    for i in range(num_points - 2):
        p1 = points[i]
        for j in range(i + 1, num_points - 1):
            p2 = points[j]
            for k in range(j + 1, num_points):
                p3 = points[k]
                if are_collinear(p1, p2, p3):
                    return True
    return False

def generate_random_points(n, x_range=(0, 100), y_range=(0, 100)):
    points = [(random.uniform(*x_range), random.uniform(*y_range)) for _ in range(n)]
    return points

def visualize_points(points, convex_hull=None):
    x_coords, y_coords = zip(*points)
    plt.scatter(x_coords, y_coords, color='blue', label="Points")
    
    if convex_hull:
        hull_x, hull_y = zip(*convex_hull)
        hull_x += (hull_x[0],)
        hull_y += (hull_y[0],)
        plt.plot(hull_x, hull_y, color='red', linewidth=2, label="Convex Hull")

    plt.title("Randomly Generated Points with Convex Hull")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.savefig('diagram/gift_wrapping.png')

def distance(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def orientation(p, q, r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

def gift_wrapping(points_from_input):
        if len(points_from_input) < 3:
            return points_from_input

        hull = []

        start = min(points_from_input, key=lambda p: (p[1], p[0]))
        point_on_hull = start

        while True:
            hull.append(point_on_hull)
            next_point = points[0]
            for candidate in points:
                if candidate == point_on_hull:
                    continue
                cross_product = (
                    (next_point[0] - point_on_hull[0]) * (candidate[1] - point_on_hull[1])
                    - (next_point[1] - point_on_hull[1]) * (candidate[0] - point_on_hull[0])
                )
                if cross_product > 0 or (cross_product == 0 and distance(point_on_hull, candidate) > distance(point_on_hull, next_point)):
                    next_point = candidate
            
            if next_point == start:
                break
            else:
                point_on_hull = next_point

        return hull

if __name__ == "__main__":
    points = generate_random_points(10)
    while check_collinearity(points):
        points = generate_random_points(100)
    
    visualize_points(points)
    start_time = datetime.now()
    points_result = gift_wrapping(points)
    end_time = datetime.now()
    elapsed_time = end_time - start_time

    print("Elapsed Time:", elapsed_time)
    visualize_points(points, points_result)