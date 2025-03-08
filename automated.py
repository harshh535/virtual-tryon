import os
import argparse
import subprocess
import time
import shutil
from pathlib import Path

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

    # ✅ Run test.py to apply virtual try-on
    print("🚀 Running test.py to apply virtual try-on...")
    process = subprocess.Popen(["python", "test.py", "--name", "virtual_tryon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()  # ✅ Ensure test.py completes

    # ✅ Check if new images are created
    timeout = 60  # Maximum wait time in seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.exists(results_folder) and len(os.listdir(results_folder)) > 0:
            print(f"✅ New images found in {results_folder}. Ready to display.")
            return
        time.sleep(2)  # Wait and retry

    print("⚠️ ERROR: No new images were generated!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cloth_path", type=str, help="Path to the cloth image")
    args = parser.parse_args()
    main(args.cloth_path)
