import matplotlib.pyplot as plt
import random

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
    
    visualize_points(points)
    points_result = gift_wrapping(points)
    visualize_points(points, points_result)