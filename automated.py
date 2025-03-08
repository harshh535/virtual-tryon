import os
import argparse
import subprocess
import time
import shutil
from pathlib import Path
import cv2
import numpy as np

def remove_results_folder(results_folder):
    """Removes the results folder inside Streamlit's environment."""
    if os.path.exists(results_folder):
        shutil.rmtree(results_folder)
        print("🗑️ Removed old results/ folder to force fresh processing.")

def main(cloth_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(BASE_DIR, "results/")

    # ✅ Remove old results folder (only inside Streamlit environment)
    remove_results_folder(results_folder)

    # ✅ Ensure results folder exists
    os.makedirs(results_folder, exist_ok=True)

    # ✅ Run test.py to apply virtual try-on (Force fresh processing)
    print("🚀 Running test.py to apply virtual try-on...")
    process = subprocess.Popen(["python", "test.py", "--name", "virtual_tryon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()  # ✅ Wait for test.py to finish

    # ✅ Wait for new images to appear
    timeout = 60  # Maximum wait time in seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.exists(results_folder) and os.listdir(results_folder):
            print(f"✅ Virtual try-on process complete! Results saved in {results_folder}.")
            return  # ✅ Exit function when images are found
        time.sleep(2)  # Wait and retry

    print("⚠️ ERROR: No output images found after processing!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cloth_path", type=str, help="Path to the cloth image")
    args = parser.parse_args()
    main(args.cloth_path)

