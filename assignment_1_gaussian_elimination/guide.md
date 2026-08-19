# Guide: Gaussian Elimination Method

## 1. Objective

This assignment focuses on solving a system of linear equations using the Gaussian elimination method. The method is widely used in numerical computing, engineering, and scientific applications for solving linear systems efficiently and accurately.

## 2. Mathematical Background

A system of linear equations can be written in matrix form as:

$$
A x = b
$$

where:

- $A$ is the coefficient matrix
- $x$ is the unknown variable vector
- $b$ is the constant vector

The goal is to transform the matrix into an upper triangular form and then apply back substitution to determine each variable.

## 3. Gaussian Elimination Process

The method follows these steps:

1. Write the augmented matrix.
2. Choose a pivot element.
3. Eliminate the values below the pivot using row operations.
4. Continue until the matrix is upper triangular.
5. Solve from the last row upward using back substitution.

## 4. Python Implementation

This project includes a Python program that:

- reads the number of variables
- accepts the augmented matrix input from the user
- applies Gaussian elimination
- prints the final solution values

The implementation is available in:

- [gaussian_elimination.py](gaussian_elimination.py)

## 5. Input Format

The program expects:

- first line: number of variables $n$
- next $n$ lines: each line contains $n$ coefficients and one constant term

Example input:

```text
3
2 1 -1 8
-3 -1 2 -11
-2 1 2 -3
```

This corresponds to:

- 2x + y - z = 8
- -3x - y + 2z = -11
- -2x + y + 2z = -3

## 6. How to Run

Open a terminal in this folder and run:

```bash
python gaussian_elimination.py
```

Then enter the equations exactly as shown in the required format.

### Sample execution

```text
Enter the number of variables (n): 3
Enter 3 equations, each with 3 coefficients and 1 constant value:
Equation 1: 2 1 -1 8
Equation 2: -3 -1 2 -11
Equation 3: -2 1 2 -3
```

## 7. Output

The solver prints the values for each variable.

Example output:

```text
Solution:
x1 = 2.0000
x2 = 3.0000
x3 = -1.0000
```

## 8. Practical Significance

Gaussian elimination is widely used in:

- engineering systems
- scientific calculations
- computer graphics
- machine learning and optimization
- numerical analysis

It is one of the most important methods for solving linear systems.

## 9. Conclusion

This assignment demonstrates the practical use of Gaussian elimination in Python. It bridges the gap between mathematical theory and computational problem solving, which is essential in modern technical education.
