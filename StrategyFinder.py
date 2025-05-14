from typing import List

import numpy as np
from scipy.optimize import linprog


def solve_zero_sum_game(matrix: list[list[int]]) -> dict:
    """
    Solves a two-player zero-sum game using linear programming.
    Returns optimal strategies for Player A (x), Player B (y), and game value (v).

    Args:
        matrix : The m x n payoff matrix from Player A's perspective.

    Returns:
        dict: Optimal strategies and game value.
    """
    payoff_matrix = np.array(matrix)
    m, n = payoff_matrix.shape  # m = Player A's strategies, n = Player B's strategies

    # --- Player A's LP: Maximize v (subject to A^T x >= v, sum(x) = 1, x >= 0) ---
    # Rewrite as: -A^T x + v <= 0, sum(x) = 1
    c_A = np.zeros(m + 1)
    c_A[-1] = -1  # Objective: Maximize v (linprog minimizes, so -v)

    A_ub_A = np.column_stack((-payoff_matrix.T, np.ones(n)))  # Inequality constraints
    b_ub_A = np.zeros(n)
    A_eq_A = np.append(np.ones(m), 0).reshape(1, -1)  # sum(x) = 1
    b_eq_A = np.array([1.0])
    bounds_A = [(0, None) for _ in range(m)] + [(None, None)]  # x >= 0, v unbounded

    res_A = linprog(c=c_A, A_ub=A_ub_A, b_ub=b_ub_A, A_eq=A_eq_A, b_eq=b_eq_A, bounds=bounds_A)
    x = res_A.x[:-1]
    v_A = res_A.x[-1]

    # --- Player B's LP: Minimize v (subject to A y <= v, sum(y) = 1, y >= 0) ---
    c_B = np.zeros(n + 1)
    c_B[-1] = 1  # Objective: Minimize v

    A_ub_B = np.column_stack((payoff_matrix, -np.ones(m)))  # Inequality constraints
    b_ub_B = np.zeros(m)
    A_eq_B = np.append(np.ones(n), 0).reshape(1, -1)  # sum(y) = 1
    b_eq_B = np.array([1.0])
    bounds_B = [(0, None) for _ in range(n)] + [(None, None)]  # y >= 0, v unbounded

    res_B = linprog(c=c_B, A_ub=A_ub_B, b_ub=b_ub_B, A_eq=A_eq_B, b_eq=b_eq_B, bounds=bounds_B)
    y = res_B.x[:-1]
    v_B = res_B.x[-1]

    assert np.isclose(v_A, v_B), "Game values for Players A and B do not match!"

    return {
        'Hider': x,
        'Seeker': y,
        'Game value (v)': v_A
    }


def run_test_cases():
    test_cases = [
        {
            "name": "Pure Strategy Equilibrium",
            "matrix": [[3, 1], [0, 2]],
            "expected_x": [1.0, 0.0],
            "expected_y": [0.0, 1.0],
            "expected_v": 1.0
        },
        {
            "name": "Mixed Strategy Required",
            "matrix": [[2, -1], [-1, 1]],
            "expected_x": [0.6667, 0.3333],
            "expected_y": [0.3333, 0.6667],
            "expected_v": 0.3333
        },
        {
            "name": "Identical Rows",
            "matrix": [[1, 1], [1, 1]],
            "expected_x": [0.5, 0.5],
            "expected_y": [0.5, 0.5],
            "expected_v": 1.0
        },
        {
            "name": "Degenerate Game",
            "matrix": [[0, 0], [0, 0]],
            "expected_x": [0.5, 0.5],
            "expected_y": [0.5, 0.5],
            "expected_v": 0.0
        },
        {
            "name": "Non-Square Matrix",
            "matrix": [[1, -2], [0, 3], [-1, 1]],
            "expected_x": [0.6, 0.4, 0.0],
            "expected_y": [0.8, 0.2],
            "expected_v": 0.2
        }
    ]

    for test in test_cases:
        result = solve_zero_sum_game(test["matrix"])
        x = np.round(result['Hider'], 4)
        y = np.round(result['Seeker'], 4)
        v = np.round(result['Game value (v)'], 4)
        print(test["name"])
        print("Optimal strategy for Player A (x):", np.round(result['Hider'], 4))
        print("Optimal strategy for Player B (y):", np.round(result['Seeker'], 4))
        print("Game value (v):", np.round(result['Game value (v)'], 4))
        print("----------------------------------------------------------------------------------")


if __name__ == "__main__":
    run_test_cases()