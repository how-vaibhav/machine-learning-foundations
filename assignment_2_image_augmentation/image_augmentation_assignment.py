from pathlib import Path
import math
import sys

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

DEFAULT_INPUT_PATH = BASE_DIR / "Profile.jpg"
if not DEFAULT_INPUT_PATH.exists():
    DEFAULT_INPUT_PATH = ROOT_DIR / "Profile.jpg"

OUTPUTS_BASE_DIR = BASE_DIR / "augmented_outputs"


def get_next_output_dir() -> Path:
    run_number = 1
    while True:
        output_dir = OUTPUTS_BASE_DIR / f"run_{run_number:03d}"
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
            return output_dir
        run_number += 1


def get_input_path() -> Path:
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1]).expanduser()
        if not input_path.is_absolute():
            input_path = Path.cwd() / input_path
    else:
        input_path = DEFAULT_INPUT_PATH

    if not input_path.exists():
        raise FileNotFoundError(f"Input image was not found: {input_path}")
    return input_path


def save_image(image: Image.Image, output_dir: Path, name: str) -> Path:
    path = output_dir / name
    image.save(path)
    print(f"Saved: {path}")
    return path


def apply_translation(image: Image.Image, dx: int, dy: int, bg_color=(255, 255, 255)) -> Image.Image:
    canvas = Image.new("RGB", image.size, bg_color)
    canvas.paste(image, (dx, dy))
    return canvas


def apply_rotation(image: Image.Image, angle_deg: float, bg_color=(255, 255, 255)) -> Image.Image:
    return image.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=bg_color)


def apply_scale(image: Image.Image, scale_factor: float, bg_color=(255, 255, 255)) -> Image.Image:
    w, h = image.size
    new_size = (max(1, int(w * scale_factor)), max(1, int(h * scale_factor)))
    scaled = image.resize(new_size, Image.Resampling.BICUBIC)
    canvas = Image.new("RGB", (w, h), bg_color)
    x_offset = (w - scaled.width) // 2
    y_offset = (h - scaled.height) // 2
    canvas.paste(scaled, (x_offset, y_offset))
    return canvas


def apply_shear_x(image: Image.Image, shear_deg: float, bg_color=(255, 255, 255)) -> Image.Image:
    w, h = image.size
    shear_rad = math.radians(shear_deg)
    shear_factor = math.tan(shear_rad)
    matrix = (1, shear_factor, 0, 0, 1, 0)
    return image.transform((w, h), Image.AFFINE, matrix, resample=Image.Resampling.BICUBIC, fillcolor=bg_color)


def create_montage(images, grid_cols=3):
    sample_images = list(images)
    if not sample_images:
        raise ValueError("No images were provided for montage creation.")

    width, height = sample_images[0].size
    rows = math.ceil(len(sample_images) / grid_cols)
    montage = Image.new("RGB", (width * grid_cols, height * rows), (255, 255, 255))

    for index, image in enumerate(sample_images):
        row = index // grid_cols
        col = index % grid_cols
        x = col * width
        y = row * height
        montage.paste(image, (x, y))

    return montage


def main():
    input_path = get_input_path()
    output_dir = get_next_output_dir()
    original = Image.open(input_path).convert("RGB")

    augmentations = {
        "original": original,
        "rotation_15_deg": apply_rotation(original, 15),
        "scale_1_10x": apply_scale(original, 1.10),
        "translation_30_15": apply_translation(original, 30, 15),
        "shear_12_deg": apply_shear_x(original, 12),
        "horizontal_flip": ImageOps.mirror(original),
        "best_affine_combo": apply_translation(
            apply_scale(
                apply_rotation(original, -8),
                1.08,
            ),
            15,
            10,
        ),
    }

    for name, image in augmentations.items():
        save_image(image, output_dir, f"{name}.jpg")

    montage = create_montage(list(augmentations.values()), grid_cols=3)
    montage_path = save_image(montage, output_dir, "affine_augmentation_montage.jpg")

    print("\nAssignment complete.")
    print(f"Input image: {input_path}")
    print(f"Results folder: {output_dir}")
    print("Suggested best augmentation set:")
    print("1. small rotation (-8 to +15 degrees)")
    print("2. mild scaling (1.08x)")
    print("3. slight translation (15 px, 10 px)")
    print("4. horizontal flip for robustness")
    print("5. small shear (up to 12 degrees)")
    print(f"\nMontage saved at: {montage_path}")


if __name__ == "__main__":
    main()
