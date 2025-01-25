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
    plt.savefig('diagram/quick_hull.png')

def orientation(p, q, r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

def farthest_point(points, p, q):
    max_dist = -1
    farthest = None
    for r in points:
        if orientation(p, q, r) > 0:
            dist = abs((q[1] - p[1]) * r[0] - (q[0] - p[0]) * r[1] + q[0] * p[1] - q[1] * p[0])
            if dist > max_dist:
                max_dist = dist
                farthest = r
    return farthest

def find_hull(points, p, q):
    if not points:
        return [p]

    farthest = farthest_point(points, p, q)

    points_left = [r for r in points if orientation(p, farthest, r) > 0]
    points_right = [r for r in points if orientation(farthest, q, r) > 0]


    left_hull = find_hull(points_left, p, farthest)
    right_hull = find_hull(points_right, farthest, q)

    return left_hull + [farthest] + right_hull

def quick_hull(points):
    leftmost = min(points, key=lambda p: p[0])
    rightmost = max(points, key=lambda p: p[0])

    left_points = [p for p in points if orientation(leftmost, rightmost, p) > 0]
    right_points = [p for p in points if orientation(leftmost, rightmost, p) < 0]

    convex_hull_left = find_hull(left_points, leftmost, rightmost)
    convex_hull_right = find_hull(right_points, rightmost, leftmost)

    return convex_hull_left + convex_hull_right

if __name__ == "__main__":
    points = generate_random_points(100)
    while check_collinearity(points):
        points = generate_random_points(100)
    
    visualize_points(points)
    start_time = datetime.now()
    points_result = quick_hull(points)
    end_time = datetime.now()
    elapsed_time = end_time - start_time

    print("Elapsed Time:", elapsed_time)
    visualize_points(points, points_result)