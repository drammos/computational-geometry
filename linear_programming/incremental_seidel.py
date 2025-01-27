from scipy.optimize import linprog
import numpy as np

def incremental_linear_program(constraints, objective):
    n = len(constraints)
    d = 2

    initial_constraints = constraints[:d + 1]
    A = np.array([[a, b] for a, b, _ in initial_constraints])
    B = np.array([c for _, _, c in initial_constraints])

    result = linprog(c=objective, A_ub=A, b_ub=B, method="highs")

    if not result.success:
        return "No result for the starting problem"

    x_opt = result.x

    for i in range(d + 1, n):
        a, b, c = constraints[i]
        
        if a * x_opt[0] + b * x_opt[1] > c:
            A = np.vstack([A, [a, b]])
            B = np.append(B, c)

            result = linprog(c=objective, A_ub=A, b_ub=B, method="highs")

            if not result.success:
                return f"No result for step {i + 1}"

            x_opt = result.x

    optimal_value = np.dot(objective, x_opt)
    return x_opt, optimal_value

if __name__ == "__main__":
    
    constraints = [
        (-2, 1, 12),           # -2x1 + x2 <= 12
        (-1, 3, 3),            # x1 - 3x2 >= -3       --------------> -x1 + 3x2 <= 3
        (6, 7, 18),            # 6x1 + 7x2 <= 18
        (3, -12, -8),          # -3x1 + 12x2 >= 8     --------------> 3x1 - 12x2 <= -8
        (2, -7, 35),           # 2x1 - 7x2 <= 35
        (-1, 8, 29),           # -x1 + 8x2 <= 29
        (2, -6, 9),            # -2x1 + 6x2 >= -9    --------------> 2x1 - 6x2 <= 9
        (-1, 0, 0),            # x1 >= 0             --------------> -x1 < = 0
        (0, -1, 0),            # x2 >= 0             --------------> -x2 < = 0
    ]
    objective = [-3, 10]       # MAX( 3x1 - 10x2) 

    solution = incremental_linear_program(constraints, objective)

    print("Solution is:", solution)