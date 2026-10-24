# MFML | Mathematical Foundations for Machine Learning

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-coursework-2E7D32)
![Focus](https://img.shields.io/badge/focus-numerical%20methods%20%7C%20computer%20vision-6A1B9A)

> A focused coursework repository connecting mathematical theory with practical Python implementations.

## About This Repository

This repository contains three independent assignments from a mathematical foundations of machine learning workflow:

- **Numerical computation:** solving systems of linear equations with Gaussian elimination.
- **Computer vision:** expanding image data with linear and affine transformations.
- **Dimensionality reduction:** implementing SVD from scratch and applying it for PCA on the Iris dataset.

Each assignment is self-contained with its own implementation, guide, and outputs. The structure is designed for clear learning, reproducible execution, and professional academic submission.

## Learning Map

![Learning Map](Flow%20Chart/1.png)

## Assignments

### 01 | Gaussian Elimination

**Purpose:** solve a system of linear equations from user-provided input.

**Implementation:** [gaussian_elimination.py](assignment_1_gaussian_elimination/gaussian_elimination.py)  
**Guide:** [guide.md](assignment_1_gaussian_elimination/guide.md)

![Gaussian Elimination Process](Flow%20Chart/2.png)

### 02 | Affine Image Augmentation

**Purpose:** create realistic variations of an image for data augmentation.

**Implementation:** [image_augmentation_assignment.py](assignment_2_image_augmentation/image_augmentation_assignment.py)  
**Guide:** [guide.md](assignment_2_image_augmentation/guide.md)  
**Outputs:** [augmented_outputs](assignment_2_image_augmentation/augmented_outputs)

![Affine Image Augmentation Workflow](Flow%20Chart/3.png)

### 03 | PCA via Singular Value Decomposition

**Purpose:** implement SVD from mathematical first principles and use it to perform PCA on the Iris dataset.

**Implementation:** [pca_svd.py](assignment_3_pca_svd/pca_svd.py)  
**Guide:** [guide.md](assignment_3_pca_svd/guide.md)

**What is implemented from scratch (no sklearn/numpy.linalg.svd for core logic):**
- QR algorithm with Gram-Schmidt orthogonalisation for eigendecomposition
- Full SVD: **A = U Σ Vᵀ**
- PCA: centring → SVD → projection → reconstruction
- Explained variance ratio table
- Comparison: SVD-based PCA vs covariance-matrix PCA
- Verification block using `numpy.linalg.svd` and `sklearn.decomposition.PCA`

![PCA](Flow%20Chart/PCA.png)

## Repository Layout

```text
MFML/
├── README.md
├── LICENSE
├── Profile.jpg
├── Flow Chart/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   └── PCA.png
├── assignment_1_gaussian_elimination/
│   ├── gaussian_elimination.py
│   └── guide.md
├── assignment_2_image_augmentation/
│   ├── image_augmentation_assignment.py
│   ├── guide.md
│   └── augmented_outputs/
│       ├── run_001/
│       ├── run_002/
│       └── run_003/
└── assignment_3_pca_svd/
    ├── pca_svd.py
    ├── guide.md
    └── iris.data          ← downloaded automatically on first run
```

## Quick Start

### Requirements

- Python 3.13 or a compatible Python 3 version
- Pillow for Assignment 2
- numpy + scikit-learn for Assignment 3 verification (optional)

Install dependencies in the project virtual environment:

```powershell
.venv\Scripts\python.exe -m pip install pillow numpy scikit-learn
```

### Run Assignment 1

```powershell
cd assignment_1_gaussian_elimination
python gaussian_elimination.py
```

Enter the number of variables, followed by one augmented-matrix row per equation.

### Run Assignment 2

```powershell
cd assignment_2_image_augmentation
python image_augmentation_assignment.py "..\Profile.jpg"
```

Every execution creates a new numbered folder inside `augmented_outputs`, so results from previous images are preserved:

```text
augmented_outputs/run_001/
augmented_outputs/run_002/
augmented_outputs/run_003/
```

To process another image, replace `"..\Profile.jpg"` with its path.

### Run Assignment 3

```powershell
cd assignment_3_pca_svd
python pca_svd.py
```

`iris.data` is downloaded automatically on the first run (requires internet).  
All outputs — matrices, eigenvalues, principal components, variance tables,  
projections, reconstructions, and errors — are printed to the terminal.

## Concepts Demonstrated

| Area                    | Concepts                                                                  |
| ----------------------- | ------------------------------------------------------------------------- |
| Linear algebra          | Augmented matrices, row operations, pivots, back substitution             |
| Numerical methods       | Algorithmic solving of linear systems                                     |
| Computer vision         | Image transformation and augmentation                                     |
| Matrix decomposition    | SVD from scratch: eigendecomposition via QR algorithm, U, Σ, Vᵀ          |
| Dimensionality reduction| PCA via SVD: projection, reconstruction, explained variance               |
| Software practice       | Modular scripts, repeatable execution, documentation                      |

## Academic Purpose

The project demonstrates how abstract mathematical concepts become practical programs:

1. A mathematical model is defined.
2. The algorithm is implemented in Python.
3. User input or image data is processed.
4. Results are generated and documented.

This makes the repository useful as both a coursework submission and a compact reference for foundational machine learning concepts.

### Assignment 3 Highlights

- **No black-box ML functions** used for the core logic.
- The QR algorithm (Gram-Schmidt) computes eigenvalues/eigenvectors from scratch.
- SVD is derived step-by-step: AᵀA → eigendecomp → σᵢ = √λᵢ → uᵢ = Avᵢ/σᵢ.
- PCA pipeline: centre → SVD → project → reconstruct → measure error.
- Reconstruction errors drop as k increases (k=4 gives MSE ≈ 0).
- PC1 + PC2 together capture **97.76 %** of the variance in the Iris dataset.

## Author

Prepared for coursework and practical assignment submission.
