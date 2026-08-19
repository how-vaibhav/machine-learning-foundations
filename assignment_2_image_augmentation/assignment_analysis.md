# Guide: Image Data Augmentation Using Affine Transformations

## 1. Objective

The aim of this assignment is to apply data augmentation to a personal image using linear and affine transformations. This helps us understand how synthetic variations in an image can improve model robustness and increase dataset diversity.

## 2. Why Data Augmentation is Important

Machine learning models often perform better when trained on varied examples. In image-related tasks, small changes in position, scale, or orientation should not drastically alter the identity of the object.

Affine transformations are especially useful because they allow us to simulate realistic changes without destroying the structure of the image.

## 3. Affine Transformation Concept

Affine transformation has the general form:

$$
\begin{bmatrix}
 x' \\
 y'
\end{bmatrix}
=
\begin{bmatrix}
 a & b & t_x \\
 c & d & t_y
\end{bmatrix}
\begin{bmatrix}
 x \\
 y \\
 1
\end{bmatrix}
$$

This includes:

- rotation
- scaling
- shearing
- translation

These operations help create different versions of the same image while preserving geometric consistency.

## 4. Transformations Applied

The implementation uses several augmentation techniques on the uploaded face image:

1. Rotation
   - simulates head movement
   - useful for pose variation

2. Scaling
   - simulates zoom-in or zoom-out effects
   - helps the model learn size invariance

3. Translation
   - shifts the subject within the frame
   - useful for alignment variations

4. Shear
   - adds mild distortion
   - helps simulate perspective-like changes

5. Horizontal flip
   - creates mirror-image data
   - useful for real-world variation

## 5. Best Augmentation Strategy

For face images, the most realistic and effective approach is to use mild transformations rather than extreme warping.

Recommended range:

- rotation: 5° to 15°
- scale factor: 1.05x to 1.10x
- translation: 10 to 30 pixels
- shear: small values below 15°
- horizontal flip: optional but useful

This keeps the person recognizable while still creating a useful augmented dataset.

## 6. File and Execution Details

The script for this assignment is:

- [image_augmentation_assignment.py](image_augmentation_assignment.py)

This script:

- loads the image from the folder
- applies several affine transformations
- saves the transformed outputs in the `augmented_outputs` folder
- creates a final montage for comparison

## 7. How to Run

Open a terminal in this assignment folder and run:

```bash
python image_augmentation_assignment.py
```

The script will generate several modified versions of the original photo and save them automatically.

## 8. Output Generated

The outputs include:

- original image
- rotated image
- scaled image
- translated image
- sheared image
- flipped image
- best combined affine result
- montage of all transformed images

## 9. Conclusion

Affine transformations are a practical and effective way to augment image data. They preserve the structure of the subject while introducing realistic variation, which makes them valuable for training more robust machine learning models.

In this assignment, the best results were obtained by using a balanced combination of small rotation, scaling, and translation instead of extreme distortion.
