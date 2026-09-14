# Assignment 3 – PCA via SVD: Guide

## Overview

This assignment implements **Principal Component Analysis (PCA)** using
**Singular Value Decomposition (SVD)** entirely from scratch in Python.

All core mathematical steps are hand-coded.  
`numpy.linalg.svd()` and `sklearn.decomposition.PCA` appear **only** in the
verification section at the end.

---

## Mathematical Background

### Part A – SVD

Given matrix **A** (m × n):

```
A = U Σ Vᵀ
```

| Symbol | Meaning |
|--------|---------|
| **U** | m × r matrix of left singular vectors |
| **Σ** | r × r diagonal matrix of singular values σᵢ |
| **Vᵀ** | r × n matrix whose rows are right singular vectors |

**Steps implemented:**

1. Compute **AᵀA** (n × n symmetric positive semi-definite).  
2. Eigendecompose **AᵀA** using the **QR algorithm** (iterative Gram-Schmidt).  
3. Singular values: `σᵢ = √λᵢ` (only positive eigenvalues kept).  
4. Right singular vectors **vᵢ** = normalised eigenvectors of **AᵀA**.  
5. Left singular vectors: `uᵢ = A vᵢ / σᵢ`.  
6. Assemble **U**, **Σ**, **Vᵀ**.  
7. Verify: reconstruct **A** and measure Frobenius-norm error.

---

### Part B – PCA

Given dataset **X** (150 × 4, Iris):

1. **Mean** `μ = mean(X, axis=0)`.  
2. **Centre** `Xc = X − μ`.  
3. **SVD** `Xc = U Σ Vᵀ`.  
4. **Principal components** = rows of **Vᵀ** (columns of **V**).  
5. **Explained variance ratio** `= σᵢ² / Σ σⱼ²`.  
6. **Project** `Z = Xc Vk` (k = chosen number of PCs).  
7. **Reconstruct** `X̂ = Z Vkᵀ + μ`.  
8. **Reconstruction error** (MSE) for k = 1, 2, 3, 4.

---

### Extension – SVD vs Covariance-Matrix PCA

| Method | Formula | Notes |
|--------|---------|-------|
| **SVD** | direct on **Xc** | numerically stable |
| **Covariance PCA** | eigendecomp of **C = XcᵀXc / (m−1)** | squares condition number |

SVD is preferred because it avoids the intermediate squaring step,
preserving numerical precision especially when features have very
different scales.

---

## How to Run

```powershell
# From the repository root
cd assignment_3_pca_svd
python pca_svd.py
```

The script will:
- Auto-download `iris.data` on first run (requires internet).
- Print all required outputs to the terminal.

---

## Expected Outputs

1. Original matrix A (Part A demo)  
2. AᵀA  
3. Eigenvalues  
4. Singular values  
5. U, Σ, Vᵀ  
6. Reconstruction of A + Frobenius error  
7. Iris dataset (first rows)  
8. Mean vector μ  
9. Centred matrix Xc (first rows)  
10. Principal components  
11. Explained variance ratio table  
12. Projection Z for k = 1 … 4  
13. Reconstructed Iris data  
14. MSE reconstruction error per k  
15. Sklearn/numpy verification comparison  
16. Covariance-matrix comparison  

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `math`, `csv`, `os`, `urllib` | stdlib — always available |
| `numpy` | **verification only** |
| `scikit-learn` | **verification only** |

Install verification libraries (optional):

```powershell
..\.venv\Scripts\python.exe -m pip install numpy scikit-learn
```
