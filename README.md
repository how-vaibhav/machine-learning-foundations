# MFML | Mathematical Foundations for Machine Learning

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-coursework-2E7D32)
![Focus](https://img.shields.io/badge/focus-numerical%20methods%20%7C%20computer%20vision-6A1B9A)

> A focused coursework repository connecting mathematical theory with practical Python implementations.

## About This Repository

This repository contains two independent assignments from a mathematical foundations of machine learning workflow:

- **Numerical computation:** solving systems of linear equations with Gaussian elimination.
- **Computer vision:** expanding image data with linear and affine transformations.

Each assignment is self-contained with its own implementation, guide, and outputs. The structure is designed for clear learning, reproducible execution, and professional academic submission.

## Learning Map

```mermaid
flowchart LR
	A[MFML Coursework] --> B[Assignment 1\nGaussian Elimination]
	A --> C[Assignment 2\nAffine Image Augmentation]
	B --> D[User enters\naugmented matrix]
	D --> E[Row reduction]
	E --> F[Linear system solution]
	C --> G[User selects\ninput image]
	G --> H[Affine transformations]
	H --> I[Separate run folder\nand comparison montage]
```

## Assignments

### 01 | Gaussian Elimination

📐 **Purpose:** solve a system of linear equations from user-provided input.

**Implementation:** [gaussian_elimination.py](assignment_1_gaussian_elimination/gaussian_elimination.py)  
**Guide:** [guide.md](assignment_1_gaussian_elimination/guide.md)

```mermaid
flowchart TD
	A[Read number of variables] --> B[Read augmented matrix]
	B --> C[Select pivot]
	C --> D[Apply row operations]
	D --> E{All pivots processed?}
	E -- No --> C
	E -- Yes --> F[Back substitution]
	F --> G[Print x1, x2, ..., xn]
```

### 02 | Affine Image Augmentation

🖼️ **Purpose:** create realistic variations of an image for data augmentation.

**Implementation:** [image_augmentation_assignment.py](assignment_2_image_augmentation/image_augmentation_assignment.py)  
**Guide:** [guide.md](assignment_2_image_augmentation/guide.md)  
**Outputs:** [augmented_outputs](assignment_2_image_augmentation/augmented_outputs)

```mermaid
flowchart LR
	A[Input image] --> B[Rotation]
	A --> C[Scaling]
	A --> D[Translation]
	A --> E[Shearing]
	A --> F[Horizontal flip]
	B --> G[Augmented image set]
	C --> G
	D --> G
	E --> G
	F --> G
	G --> H[Montage and run-specific outputs]
```

## Repository Layout

```text
MFML/
├── README.md
├── Profile.jpg
├── assignment_1_gaussian_elimination/
│   ├── gaussian_elimination.py
│   └── guide.md
└── assignment_2_image_augmentation/
	├── image_augmentation_assignment.py
	├── guide.md
	└── augmented_outputs/
		├── run_001/
		├── run_002/
		└── run_003/
```

## Quick Start

### Requirements

- Python 3.13 or a compatible Python 3 version
- Pillow for Assignment 2

Install the image-processing dependency in the project virtual environment:

```powershell
\.venv\Scripts\python.exe -m pip install pillow
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

## Concepts Demonstrated

| Area              | Concepts                                                      |
| ----------------- | ------------------------------------------------------------- |
| Linear algebra    | Augmented matrices, row operations, pivots, back substitution |
| Numerical methods | Algorithmic solving of linear systems                         |
| Computer vision   | Image transformation and augmentation                         |
| Software practice | Modular scripts, repeatable execution, documentation          |

## Academic Purpose

The project demonstrates how abstract mathematical concepts become practical programs:

1. A mathematical model is defined.
2. The algorithm is implemented in Python.
3. User input or image data is processed.
4. Results are generated and documented.

This makes the repository useful as both a coursework submission and a compact reference for foundational machine learning concepts.

## Author

Prepared for coursework and practical assignment submission.
