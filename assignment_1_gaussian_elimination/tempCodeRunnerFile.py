
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