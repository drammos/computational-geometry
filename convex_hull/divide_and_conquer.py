import random
import matplotlib.pyplot as plt
import time
import numpy as np

def generate_random_points(n, x_range=(0, 100), y_range=(0, 100)):
    points = [(random.uniform(*x_range), random.uniform(*y_range)) for _ in range(n)]
    return points

def visualize_points(points, hull=None):
    x_coords, y_coords = zip(*points)
    plt.scatter(x_coords, y_coords, color="blue", label="Points")

    if hull:
        hull_x, hull_y = zip(*(hull + [hull[0]]))
        plt.plot(hull_x, hull_y, color="red", label="Convex Hull")

    plt.title("Convex Hull using Divide and Conquer")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.savefig('diagram/divide_and_conquer.png')

def orientation(p1, p2, p3):
    return (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])

def rightmost(right_points):
    rightmostIndex = 0
    for i in range(1, len(right_points)):
        if right_points[i][0] > right_points[rightmostIndex][0]:
            rightmostIndex = i
        elif right_points[i][0] == right_points[rightmostIndex][0] and right_points[i][1] > right_points[rightmostIndex][1]:
            rightmostIndex = i
    return rightmostIndex

def leftmost(left_points):
    leftmostIndex = 0
    for i in range(1, len(left_points)):
        if left_points[i][0] < left_points[leftmostIndex][0]:
            leftmostIndex = i
        elif left_points[i][0] == left_points[leftmostIndex][0] and left_points[i][1] < left_points[leftmostIndex][1]:
            leftmostIndex = i
    return leftmostIndex

def upper_bridge_fn(left, right):
    i = rightmost(left)
    j = leftmost(right)

    while True:
        if orientation(left[i], left[(i + 1) % len(left)], right[j]) <= 0 and orientation(right[j], right[(j - 1) % len(right)], left[i]) >= 0:
            break

        if orientation(left[i], left[(i + 1) % len(left)], right[j]) > 0:
            i = (i + 1) % len(left)
        if orientation(right[j], right[(j - 1) % len(right)], left[i]) < 0:
            j = (j - 1) % len(right)

    return [left[i], right[j]]

def lower_bridge_fn(left, right):
    i = rightmost(left)
    j = leftmost(right)
    
    while True:
        if orientation(left[i], left[(i - 1) % len(left)], right[j]) >= 0 and orientation(right[j], right[(j + 1) % len(right)], left[i]) <= 0:
            break

        if orientation(left[i], left[(i - 1) % len(left)], right[j]) < 0:
            i = (i - 1) % len(left)
        if orientation(right[j], right[(j + 1) % len(right)], left[i]) > 0:
            j = (j + 1) % len(right)

    return [left[i], right[j]]

def merge_hulls(left_hull, right_hull):
    upper_bridge = upper_bridge_fn(left_hull, right_hull)
    lower_bridge = lower_bridge_fn(left_hull, right_hull)
    merged_hull = []

    merged_hull.append(upper_bridge[1])
    merged_hull.append(upper_bridge[0])

    common_points_left = [i for i, point in enumerate(left_hull) if np.array_equal(point, upper_bridge[0])]
    common_points_right = [i for i, point in enumerate(right_hull) if np.array_equal(point, lower_bridge[1])]

    if common_points_left:
        common_point_index_left = common_points_left[0] % len(left_hull)
        for i in range(len(left_hull)):
            if orientation(merged_hull[-1], left_hull[(common_point_index_left + 1 + i) % len(left_hull)], lower_bridge[0]) < 0:
                merged_hull.append(left_hull[(common_point_index_left + 1 + i) % len(left_hull)])

    merged_hull.append(lower_bridge[0])
    merged_hull.append(lower_bridge[1])

    if common_points_right:
        common_point_index_right = common_points_right[0] % len(right_hull)
        for i in range(len(right_hull)):
            if orientation(merged_hull[-1], right_hull[(common_point_index_right + 1 + i) % len(right_hull)], upper_bridge[1]) < 0:
                merged_hull.append(right_hull[(common_point_index_right + 1 + i) % len(right_hull)])

    return merged_hull

def divide_and_conquer(points):
    if len(points) <= 3:
        hull = sorted(points)
        if len(hull) == 3 and orientation(hull[0], hull[1], hull[2]) > 0:
            hull[1], hull[2] = hull[2], hull[1]
        return hull

    mid = len(points) // 2
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)

if __name__ == "__main__":
    num_points = 100
    points = generate_random_points(num_points)
    points_sorted = sorted(points)
    hull = divide_and_conquer(points_sorted)
    visualize_points(points, hull)