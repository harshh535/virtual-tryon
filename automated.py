import os
import argparse
import subprocess
import time
import shutil
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def remove_results_folder(results_folder):
    """Removes the results folder to force fresh processing."""
    if os.path.exists(results_folder):
        shutil.rmtree(results_folder)
        print("🗑️ Removed old results/ folder to force fresh processing.")

def ensure_directory_exists(folder_path):
    """Ensures the given directory exists."""
    os.makedirs(folder_path, exist_ok=True)

def generate_cloth_mask(cloth_image_path, cloth_mask_path):
    """Generates the cloth mask dynamically if it does not exist."""
    if not os.path.exists(cloth_mask_path):
        print("🎭 Cloth mask missing! Generating...")
        process = subprocess.Popen(["python", "generate_mask.py", "--input", cloth_image_path, "--output", cloth_mask_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

        if os.path.exists(cloth_mask_path):
            print(f"✅ Cloth mask generated at: {cloth_mask_path}")
            display_image(cloth_mask_path, title="Generated Cloth Mask")  # ✅ Display cloth mask
        else:
            print("❌ ERROR: Cloth mask generation failed!")

def display_image(image_path, title="Image"):
    """Displays an image using OpenCV & Matplotlib."""
    if os.path.exists(image_path):
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to correct color format
        
        plt.figure(figsize=(5, 5))
        plt.imshow(img)
        plt.axis("off")
        plt.title(title)
        plt.show()
    else:
        print(f"⚠️ ERROR: Image not found at {image_path}")

def run_virtual_tryon():
    """Runs test.py to apply virtual try-on."""
    print("🚀 Running test.py to apply virtual try-on...")
    process = subprocess.Popen(["python", "test.py", "--name", "virtual_tryon"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

def wait_for_results(results_folder, timeout=60):
    """Waits for new results to appear, with a timeout."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(results_folder) and len(os.listdir(results_folder)) > 0:
            print(f"✅ New images found in {results_folder}. Ready to display.")
            return True
        time.sleep(2)  # Wait and retry
    print("⚠️ ERROR: No new images were generated!")
    return False

def main(cloth_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(BASE_DIR, "results/")
    cloth_mask_folder = os.path.join(BASE_DIR, "datasets/test/cloth-mask/")
    
    # ✅ Remove old results folder
    remove_results_folder(results_folder)

    # ✅ Ensure necessary directories exist
    ensure_directory_exists(results_folder)
    ensure_directory_exists(cloth_mask_folder)

    # ✅ Generate cloth mask dynamically if missing
    cloth_filename = os.path.basename(cloth_path)
    cloth_mask_path = os.path.join(cloth_mask_folder, cloth_filename)
    generate_cloth_mask(cloth_path, cloth_mask_path)

    # ✅ Run virtual try-on
    run_virtual_tryon()

    # ✅ Wait for output images
    wait_for_results(results_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cloth_path", type=str, help="Path to the cloth image")
    args = parser.parse_args()
    main(args.cloth_path)
