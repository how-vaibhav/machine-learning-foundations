# Gaussian Elimination Method for solving linear equations
# Input format:
# First line: number of variables n
# Next n lines: coefficients of each equation, each line contains n+1 values
# Example:
# 3
# 2 1 -1 8
# -3 -1 2 -11
# -2 1 2 -3


def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])

    row = 0
    for col in range(n):
        pivot = None
        for r in range(row, n):
            if abs(matrix[r][col]) > 1e-12:
                pivot = r
                break

        if pivot is None:
            continue

        if pivot != row:
            matrix[row], matrix[pivot] = matrix[pivot], matrix[row]

        pv = matrix[row][col]
        for j in range(col, m):
            matrix[row][j] /= pv

        for r in range(n):
            if r == row:
                continue
            factor = matrix[r][col]
            if abs(factor) < 1e-12:
                continue
            for j in range(col, m):
                matrix[r][j] -= factor * matrix[row][j]

        row += 1
        if row == n:
            break

    # Check for inconsistency or infinitely many solutions
    for i in range(n):
        zero_row = all(abs(matrix[i][j]) < 1e-12 for j in range(n))
        if zero_row and abs(matrix[i][n]) > 1e-12:
            return None

    # Back-substitute to get values
    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = matrix[i][n]
        for j in range(i + 1, n):
            s -= matrix[i][j] * solution[j]
        solution[i] = s

    return solution


def input_system():
    n = int(input("Enter the number of variables (n): "))
    print(f"Enter {n} equations, each with {n} coefficients and 1 constant value:")

    matrix = []
    for i in range(n):
        row = list(map(float, input(f"Equation {i + 1}: ").split()))
        if len(row) != n + 1:
            raise ValueError(f"Each equation must contain {n} coefficients and 1 constant value.")
        matrix.append(row)

    return matrix


def main():
    print("Gaussian Elimination Solver")
    print("===========================")
    matrix = input_system()

    solution = gaussian_elimination(matrix)

    if solution is None:
        print("The system has no solution (inconsistent system).")
    else:
        print("\nSolution:")
        for i, value in enumerate(solution, start=1):
            print(f"x{i} = {value:.4f}")


if __name__ == "__main__":
    main()
