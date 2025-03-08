import streamlit as st
import os
import subprocess
import time

# Get base directory for local storage (not GitHub)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_virtual_tryon(cloth_path):
    """Runs the virtual try-on backend script and waits for results."""
    process = subprocess.Popen(["python", "automated.py", cloth_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()  # Ensure the process completes before fetching results

def get_result_images(results_folder, timeout=30):
    """Waits for new images to appear in results folder and returns them."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.exists(results_folder):
            images = [os.path.join(results_folder, img) for img in os.listdir(results_folder) if img.endswith(('.jpg', '.png'))]
            if images:
                return images  # Return fresh images
        time.sleep(2)  # Wait and retry

    st.warning("⚠️ No new output images found within timeout period.")
    return []

# Streamlit UI
st.title("👕 Virtual Try-On System")
st.write("Upload a clothing image and see it applied on all models!")

# File uploader
uploaded_file = st.file_uploader("Choose a clothing image", type=["jpg", "png"])

if uploaded_file is not None:
    cloth_folder = os.path.join(BASE_DIR, "datasets/test/cloth/")
    results_folder = os.path.join(BASE_DIR, "results/")
    os.makedirs(cloth_folder, exist_ok=True)
    os.makedirs(results_folder, exist_ok=True)

    cloth_path = os.path.join(cloth_folder, uploaded_file.name)
    with open(cloth_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Image saved: {uploaded_file.name}")

    if st.button("Run Virtual Try-On"):
        with st.spinner("Processing... Please wait ⏳"):
            run_virtual_tryon(cloth_path)  # Wait for processing to complete
            result_images = get_result_images(results_folder)  # Fetch fresh images

        if result_images:
            st.success("🎉 Processing complete! Check the results below.")
            for img_path in result_images:
                st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
                with open(img_path, "rb") as file:
                    st.download_button(label="Download", data=file, file_name=os.path.basename(img_path), mime="image/jpeg")
            st.rerun()  # Force UI to refresh for new images
        else:
            st.warning("⚠️ No output images found. Please check if the try-on process completed successfully.")

        
