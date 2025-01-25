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
    plt.savefig('diagram/incremental.png')

def orientation(p, q, r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

def incremental(points_from_input):
        points = sorted(points_from_input)
        upper = [points[0], points[1]]
        lower = [points[-1], points[-2]]

        for p in points[2:]:
            upper.append(p)
            while len(upper) >= 3 and orientation(upper[-3], upper[-2], upper[-1]) <= 1:
                upper.pop(-2)

        for i in range(len(points) - 3, -1, -1):
            lower.append(points[i])
            while len(lower) >= 3 and orientation(lower[-3], lower[-2], lower[-1]) <= 1:
                lower.pop(-2)
        
        lower.pop(0)
        lower.pop()
        l = upper + lower
        return l

if __name__ == "__main__":
    points = generate_random_points(100)
    visualize_points(points)
    points_result = incremental(points)
    visualize_points(points, points_result)