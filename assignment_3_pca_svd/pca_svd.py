# =============================================================================
# Assignment 3 | PCA Using Singular Value Decomposition (SVD)
# =============================================================================
# Mathematical steps are implemented from scratch.
# numpy.linalg.svd() and sklearn.decomposition.PCA are used ONLY for
# verification at the end of the program.
#
# Dataset : Iris (sepal length, sepal width, petal length, petal width)
# =============================================================================

import math
import csv
import os
import urllib.request


# ---------------------------------------------------------------------------
# Section 0 – tiny matrix helpers (pure Python, no numpy for core logic)
# ---------------------------------------------------------------------------

def mat_shape(A):
    """Return (rows, cols) of a 2-D list."""
    return len(A), len(A[0])


def mat_zeros(r, c):
    return [[0.0] * c for _ in range(r)]


def mat_identity(n):
    I = mat_zeros(n, n)
    for i in range(n):
        I[i][i] = 1.0
    return I


def mat_transpose(A):
    r, c = mat_shape(A)
    return [[A[i][j] for i in range(r)] for j in range(c)]


def mat_mul(A, B):
    rA, cA = mat_shape(A)
    rB, cB = mat_shape(B)
    if cA != rB:
        raise ValueError(f"Incompatible shapes ({rA},{cA}) x ({rB},{cB})")
    C = mat_zeros(rA, cB)
    for i in range(rA):
        for j in range(cB):
            s = 0.0
            for k in range(cA):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C


def mat_sub(A, B):
    r, c = mat_shape(A)
    return [[A[i][j] - B[i][j] for j in range(c)] for i in range(r)]


def vec_norm(v):
    return math.sqrt(sum(x * x for x in v))


def vec_dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def frobenius_norm(A):
    return math.sqrt(sum(A[i][j] ** 2
                         for i in range(len(A))
                         for j in range(len(A[0]))))


def print_matrix(A, title="", fmt=".6f", col_width=13):
    if title:
        print(f"\n{'-' * 60}")
        print(f"  {title}")
        print(f"{'-' * 60}")
    r, c = mat_shape(A)
    for i in range(r):
        row_str = "  ".join(f"{A[i][j]:{col_width}{fmt}}" for j in range(c))
        print(f"  [ {row_str} ]")




# ---------------------------------------------------------------------------
# Section 1 – Eigenvalue / Eigenvector solver (QR algorithm)
# ---------------------------------------------------------------------------

def gram_schmidt(A):
    """QR decomposition via Gram-Schmidt. Returns (Q, R)."""
    r, c = mat_shape(A)
    Q = [list(col) for col in mat_transpose(A)]  # work column-wise
    R = mat_zeros(c, c)
    for i in range(c):
        for j in range(i):
            R[j][i] = vec_dot(Q[j], Q[i])
            Q[i] = [Q[i][k] - R[j][i] * Q[j][k] for k in range(r)]
        R[i][i] = vec_norm(Q[i])
        if abs(R[i][i]) < 1e-14:
            Q[i] = [0.0] * r
        else:
            Q[i] = [Q[i][k] / R[i][i] for k in range(r)]
    Q = mat_transpose(Q)
    return Q, R


def qr_eigen(S, max_iter=2000, tol=1e-12):
    """
    Compute eigenvalues and eigenvectors of a real symmetric matrix S
    using the iterative QR algorithm.

    Returns
    -------
    eigenvalues  : list of floats (unsorted)
    eigenvectors : 2-D list, each row is one eigenvector
    """
    n = len(S)
    Ak = [row[:] for row in S]
    V  = mat_identity(n)

    for _ in range(max_iter):
        Q, R = gram_schmidt(Ak)
        Ak = mat_mul(R, Q)
        V  = mat_mul(V, Q)
        off = math.sqrt(sum(Ak[i][j] ** 2
                            for i in range(n)
                            for j in range(n) if i != j))
        if off < tol:
            break

    eigenvalues  = [Ak[i][i] for i in range(n)]
    eigenvectors = mat_transpose(V)   # each row = one eigenvector
    return eigenvalues, eigenvectors


# ---------------------------------------------------------------------------
# Section 2 – Part A: SVD of an arbitrary matrix A = U Sigma V^T
# ---------------------------------------------------------------------------

def svd(A):
    """
    Compute the thin SVD of matrix A.

    Steps
    -----
    1. Compute A^T A.
    2. Eigendecompose A^T A: eigenvalues lambda_i, eigenvectors v_i (columns of V).
    3. Singular values sigma_i = sqrt(lambda_i).
    4. Left singular vectors u_i = A v_i / sigma_i.
    5. Build U, Sigma, V^T.

    Returns
    -------
    U   : (m x r) list  - left singular vectors
    S   : list of r singular values (descending)
    Vt  : (r x n) list  - rows are right singular vectors
    """
    m, n = mat_shape(A)
    At  = mat_transpose(A)
    AtA = mat_mul(At, A)

    eigenvalues, eigenvectors = qr_eigen(AtA)

    # Sort by descending eigenvalue
    pairs = sorted(zip(eigenvalues, eigenvectors), key=lambda p: -p[0])

    singular_values = []
    V_cols = []

    for lam, vec in pairs:
        if lam < -1e-9:
            lam = 0.0
        sigma = math.sqrt(max(lam, 0.0))
        if sigma < 1e-10:
            continue
        singular_values.append(sigma)
        V_cols.append(vec)

    r = len(singular_values)

    # Build V^T (r x n)
    Vt = [V_cols[i] for i in range(r)]

    # Build U column by column
    U_cols = []
    for i in range(r):
        vi  = [[V_cols[i][j]] for j in range(n)]
        Avi = mat_mul(A, vi)
        ui  = [Avi[k][0] / singular_values[i] for k in range(m)]
        U_cols.append(ui)

    U = [[U_cols[j][i] for j in range(r)] for i in range(m)]

    return U, singular_values, Vt


def reconstruct_from_svd(U, S, Vt):
    """Reconstruct A = U Sigma V^T."""
    r     = len(S)
    m     = len(U)
    n     = len(Vt[0])
    A_rec = mat_zeros(m, n)
    for k in range(r):
        for i in range(m):
            for j in range(n):
                A_rec[i][j] += S[k] * U[i][k] * Vt[k][j]
    return A_rec


# ---------------------------------------------------------------------------
# Section 3 – Part B: PCA using SVD
# ---------------------------------------------------------------------------

def compute_mean(X):
    """Column-wise mean of dataset X (n_samples x n_features)."""
    m, n = mat_shape(X)
    return [sum(X[i][j] for i in range(m)) / m for j in range(n)]


def center_data(X, mu):
    """Subtract mean vector from every row."""
    m, n = mat_shape(X)
    return [[X[i][j] - mu[j] for j in range(n)] for i in range(m)]


def explained_variance_ratio(singular_values):
    """Variance explained by each principal component (proportional to sigma^2)."""
    variances = [s * s for s in singular_values]
    total     = sum(variances)
    return [v / total for v in variances]


def project(Xc, Vt, k):
    """
    Project centred data onto the first k principal components.
    Z = Xc @ Vk   where Vk = first k rows of V^T used as columns.
    """
    Vk = mat_transpose([Vt[i] for i in range(k)])
    Z  = mat_mul(Xc, Vk)
    return Z


def reconstruct_pca(Z, Vt, mu, k):
    """
    Reconstruct original-space data from projection Z.
    X_hat = Z @ Vk^T + mu
    """
    n_features = len(mu)
    Vk  = mat_transpose([Vt[i] for i in range(k)])
    VkT = mat_transpose(Vk)
    X_rec = mat_mul(Z, VkT)
    for i in range(len(X_rec)):
        for j in range(n_features):
            X_rec[i][j] += mu[j]
    return X_rec


def reconstruction_error(X_orig, X_rec):
    """Mean squared reconstruction error per sample."""
    m, n = mat_shape(X_orig)
    total = 0.0
    for i in range(m):
        for j in range(n):
            diff   = X_orig[i][j] - X_rec[i][j]
            total += diff * diff
    return total / m


# ---------------------------------------------------------------------------
# Section 4 – Dataset loader (Iris)
# ---------------------------------------------------------------------------

IRIS_URL  = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
IRIS_FILE = os.path.join(os.path.dirname(__file__), "iris.data")

FEATURE_NAMES = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
CLASS_MAP = {
    "Iris-setosa": 0,
    "Iris-versicolor": 1,
    "Iris-virginica": 2,
}


def load_iris():
    """Download iris.data if not present, then load into a 2-D list."""
    if not os.path.exists(IRIS_FILE):
        print("  Downloading Iris dataset ... ", end="", flush=True)
        urllib.request.urlretrieve(IRIS_URL, IRIS_FILE)
        print("done.")
    X, y = [], []
    with open(IRIS_FILE, newline="") as f:
        for row in csv.reader(f):
            if len(row) < 5:
                continue
            X.append([float(row[i]) for i in range(4)])
            y.append(CLASS_MAP.get(row[4], -1))
    return X, y


# ---------------------------------------------------------------------------
# Section 5 – Verification helpers (numpy / sklearn allowed here)
# ---------------------------------------------------------------------------

def verify_svd_numpy(A):
    try:
        import numpy as np
        An = np.array(A)
        _, Sn, _ = np.linalg.svd(An, full_matrices=False)
        return Sn.tolist()
    except ImportError:
        return None


def verify_pca_sklearn(X, k):
    try:
        import numpy as np
        from sklearn.decomposition import PCA
        pca = PCA(n_components=k)
        pca.fit_transform(np.array(X))
        return pca.explained_variance_ratio_.tolist()
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# Section 6 – Main driver
# ---------------------------------------------------------------------------

SEPARATOR = "=" * 70


def run_part_a():
    """Demonstrate SVD on a small example matrix."""
    print(f"\n{SEPARATOR}")
    print("  PART A - SVD IMPLEMENTATION")
    print(SEPARATOR)

    A = [
        [1.0,  2.0,  3.0,  4.0],
        [5.0,  6.0,  7.0,  8.0],
        [9.0, 10.0, 11.0, 12.0],
    ]
    m, n = mat_shape(A)
    print(f"\n  Matrix A  ({m} x {n}):")
    print_matrix(A, fmt=".2f", col_width=8)

    At  = mat_transpose(A)
    AtA = mat_mul(At, A)
    print_matrix(AtA, "Step 1 - A^T A", fmt=".4f", col_width=11)

    eigenvalues, _ = qr_eigen(AtA)
    eigenvalues_sorted = sorted(eigenvalues, reverse=True)
    print("\n  Step 2 - Eigenvalues of A^T A (sorted descending):")
    for i, lam in enumerate(eigenvalues_sorted):
        if lam > 1e-8:
            print(f"    lambda_{i+1} = {lam:14.6f}")

    U, S, Vt = svd(A)

    print("\n  Step 3 - Singular values sigma_i = sqrt(lambda_i):")
    for i, s in enumerate(S):
        print(f"    sigma_{i+1} = {s:14.6f}")

    r = len(S)
    print(f"\n  Matrices U ({m}x{r}), Sigma (diagonal), V^T ({r}x{n}):")
    print_matrix(U, "U (left singular vectors)", fmt=".6f", col_width=13)

    Sigma_diag = mat_zeros(r, r)
    for i in range(r):
        Sigma_diag[i][i] = S[i]
    print_matrix(Sigma_diag, "Sigma (singular-value diagonal)", fmt=".6f", col_width=13)
    print_matrix(Vt, "V^T (right singular vectors)", fmt=".6f", col_width=13)

    A_rec = reconstruct_from_svd(U, S, Vt)
    err   = frobenius_norm(mat_sub(A, A_rec))
    print_matrix(A_rec, "Step 7 - Reconstructed A = U Sigma V^T", fmt=".6f", col_width=13)
    print(f"\n  Reconstruction Error (Frobenius norm) : {err:.2e}")

    np_singular = verify_svd_numpy(A)
    if np_singular:
        print("\n  -- numpy.linalg.svd() verification --")
        print("  numpy singular values:", [f"{s:.6f}" for s in np_singular[:r]])
        print("  ours singular values :", [f"{s:.6f}" for s in S])


def run_part_b():
    """PCA on the Iris dataset."""
    print(f"\n{SEPARATOR}")
    print("  PART B - PCA USING SVD  (Iris Dataset)")
    print(SEPARATOR)

    print("\n  Loading Iris dataset ...")
    X, y = load_iris()
    m, n = mat_shape(X)
    print(f"  Samples: {m}   Features: {n}   Classes: 3")

    print(f"\n  Step 1 - Original dataset (first 5 rows of {m}):")
    header = "  " + "  ".join(f"{name:>14}" for name in FEATURE_NAMES)
    print(header)
    for i in range(5):
        row_str = "  ".join(f"{X[i][j]:>14.4f}" for j in range(n))
        print(f"  {row_str}")
    print("  ...")

    mu = compute_mean(X)
    print("\n  Step 2 - Mean vector mu:")
    for j, name in enumerate(FEATURE_NAMES):
        print(f"    {name:<15}: {mu[j]:.6f}")

    Xc = center_data(X, mu)
    print(f"\n  Step 3 - Centred data Xc = X - mu (first 5 rows):")
    print(header)
    for i in range(5):
        row_str = "  ".join(f"{Xc[i][j]:>14.6f}" for j in range(n))
        print(f"  {row_str}")
    print("  ...")

    print("\n  Step 4 - SVD of Xc = U Sigma V^T ...", end="", flush=True)
    U_pca, S_pca, Vt_pca = svd(Xc)
    print(" done.")

    print("\n  Step 5 - Principal Components (rows of V^T):")
    for i, pc in enumerate(Vt_pca):
        print(f"    PC{i+1}: [", "  ".join(f"{v:8.5f}" for v in pc), "]")

    evr = explained_variance_ratio(S_pca)
    cumulative = 0.0
    print("\n  Step 6 - Explained Variance Ratio:")
    print(f"  {'PC':<6} {'Singular Value':>16} {'Variance %':>12} {'Cumulative %':>14}")
    print(f"  {'-'*6}  {'-'*16}  {'-'*10}  {'-'*12}")
    for i, (s, ratio) in enumerate(zip(S_pca, evr)):
        cumulative += ratio
        print(f"  PC{i+1:<4}  {s:>16.6f}  {ratio*100:>11.4f}%  {cumulative*100:>12.4f}%")

    print(f"\n  Steps 7-8 - Projection & Reconstruction for k = 1 to {n}:")
    print(f"\n  {'k':<4} {'MSE Reconstruction Error':>24} {'Variance Retained':>18}")
    print(f"  {'-'*4}  {'-'*24}  {'-'*16}")

    results = {}
    cumvar = 0.0
    for k in range(1, n + 1):
        cumvar += evr[k - 1]
        Z     = project(Xc, Vt_pca, k)
        X_rec = reconstruct_pca(Z, Vt_pca, mu, k)
        mse   = reconstruction_error(X, X_rec)
        results[k] = {"Z": Z, "X_rec": X_rec, "mse": mse, "cumvar": cumvar}
        print(f"  k={k:<3}  {mse:>24.8f}  {cumvar*100:>16.4f}%")

    k_show = 2
    print(f"\n  -- Reduced representation Z (k={k_show}, first 10 samples) --")
    print("  " + "  ".join(f"{'PC'+str(i+1):>12}" for i in range(k_show)))
    Z2 = results[k_show]["Z"]
    for i in range(min(10, m)):
        print("  " + "  ".join(f"{Z2[i][j]:>12.6f}" for j in range(k_show)))
    print("  ...")

    print(f"\n  -- Reconstructed data X_hat (k={k_show}, first 5 rows) --")
    print(header)
    Xr2 = results[k_show]["X_rec"]
    for i in range(5):
        row_str = "  ".join(f"{Xr2[i][j]:>14.6f}" for j in range(n))
        print(f"  {row_str}")
    print("  ...")
    print(f"\n  Reconstruction MSE (k=2): {results[2]['mse']:.8f}")

    sk_evr = verify_pca_sklearn(X, n)
    if sk_evr:
        print("\n  -- sklearn PCA verification (explained_variance_ratio_) --")
        print("  sklearn :", [f"{v*100:.4f}%" for v in sk_evr])
        print("  ours    :", [f"{v*100:.4f}%" for v in evr])

    print(f"\n{SEPARATOR}")
    print("  RECOMMENDED EXTENSION: SVD vs Covariance-Matrix PCA")
    print(SEPARATOR)
    _compare_svd_vs_cov(Xc, mu, n)


def _compare_svd_vs_cov(Xc, mu, n_features):
    """
    Covariance-matrix PCA: C = Xc^T Xc / (m-1), then eigen-decompose C.
    Compare explained variances with SVD-based approach.
    """
    m = len(Xc)
    XcT = mat_transpose(Xc)
    C   = mat_mul(XcT, Xc)
    for i in range(n_features):
        for j in range(n_features):
            C[i][j] /= (m - 1)

    print_matrix(C, "Covariance Matrix C", fmt=".6f", col_width=12)

    eigenvalues_cov, _ = qr_eigen(C)
    cov_variances = sorted(eigenvalues_cov, reverse=True)
    total_cov     = sum(cov_variances)
    cov_evr       = [v / total_cov for v in cov_variances]

    print("\n  Covariance-PCA Eigenvalues (= variances of each PC):")
    for i, (ev, er) in enumerate(zip(cov_variances, cov_evr)):
        print(f"    PC{i+1}: eigenvalue = {ev:.6f}   ({er*100:.4f}%)")

    print("\n  Why SVD is preferred:")
    print("  +-----------------------------------------------------------+")
    print("  | 1. SVD avoids forming X^T X, which squares the condition  |")
    print("  |    number -> better numerical stability.                   |")
    print("  | 2. SVD works on the data matrix directly; no separate      |")
    print("  |    covariance-matrix build step needed.                    |")
    print("  | 3. For tall matrices SVD is more memory-efficient (thin).  |")
    print("  | 4. Both methods yield identical PCs when implemented       |")
    print("  |    correctly (up to sign).                                 |")
    print("  +-----------------------------------------------------------+")


def main():
    print(SEPARATOR)
    print("  Assignment 3 - PCA via SVD | Mathematical Foundations of ML")
    print(SEPARATOR)

    run_part_a()
    run_part_b()

    print(f"\n{SEPARATOR}")
    print("  Execution complete.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()

