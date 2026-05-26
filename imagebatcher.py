import threading
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps

SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
print_lock = threading.Lock()


def resolve_path(path_str):
    """Resolve a user-provided path string to an existing Path.

    Tries the string as given, then common fallbacks:
    - relative to cwd
    - relative to the script's folder
    - relative to the script's parent (sibling folders)
    - relative to the user's home
    Returns a Path (may not exist if no candidate exists).
    """
    p = Path(path_str)
    # absolute or already exists
    if p.is_absolute() and p.exists():
        return p

    candidates = [
        p,
        Path.cwd() / p,
        Path(__file__).resolve().parent / p,
        Path(__file__).resolve().parent.parent / p,
        Path.home() / p,
    ]

    for c in candidates:
        try:
            if c.exists():
                return c
        except Exception:
            continue

    # fallback: return the path as given (relative to cwd)
    return Path(path_str)

def apply_filter(img, name):
    # filters
    filters = {
        "blur":      lambda i: i.filter(ImageFilter.GaussianBlur(radius=3)),
        "sharpen":   lambda i: i.filter(ImageFilter.SHARPEN),
        "grayscale": lambda i: ImageOps.grayscale(i).convert("RGB"),
        "contour":   lambda i: i.filter(ImageFilter.CONTOUR),
        "none":      lambda i: i,
    }
    return filters.get(name, filters["none"])(img)

def process_image(input_path, output_dir, filter_name, max_w, max_h, quality):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            img = apply_filter(img, filter_name)
            img.thumbnail((max_w, max_h), Image.LANCZOS)
            out = output_dir / (input_path.stem + "_processed.jpg")
            img.save(out, format="JPEG", quality=quality)
        with print_lock:
            print(f"  ✓  {input_path.name}")
    except Exception as e:
        with print_lock:
            # erorr
            print(f"  ✗  {input_path.name}: {e}")

def batch_process(input_dir, output_dir, filter_name, max_w, max_h, quality):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # scan
    images = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in SUPPORTED]
    if not images:
        print("No images found.")
        return

    print(f"\nProcessing {len(images)} image(s) with filter: {filter_name}\n")
    threads = [threading.Thread(target=process_image, args=(f, out, filter_name, max_w, max_h, quality)) for f in images]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"\nDone! Saved to: {out.resolve()}")

def main():
    input_dir_str   = input("Input folder  : ").strip() or "input_images"
    output_dir_str  = input("Output folder : ").strip() or "output_images"
    print("Filters: blur, sharpen, grayscale, contour, none")
    filter_name = input("Filter        : ").strip() or "none"
    try:
        max_w   = int(input("Max width  [1920]: ").strip() or 1920)
        max_h   = int(input("Max height [1080]: ").strip() or 1080)
        quality = int(input("Quality  [85]: ").strip() or 85)
    except ValueError:
        # defaults
        max_w, max_h, quality = 1920, 1080, 85

    # resolve paths: try cwd, script folder, script parent (for sibling folders), and home
    input_dir = resolve_path(input_dir_str)
    output_dir = resolve_path(output_dir_str)
    if str(input_dir_str) != str(input_dir):
        print(f"Resolved input folder to: {input_dir.resolve()}")
    if str(output_dir_str) != str(output_dir):
        print(f"Resolved output folder to: {output_dir.resolve()}")

    batch_process(input_dir, output_dir, filter_name, max_w, max_h, quality)

if __name__ == "__main__":
    main()