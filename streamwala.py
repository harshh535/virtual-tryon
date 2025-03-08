import streamlit as st
import os
import subprocess
import time

# Get base directory (ensures compatibility for local & cloud deployment)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_virtual_tryon(cloth_path):
    """Runs the virtual try-on backend script using the system Python."""
    subprocess.run(["python", "automated.py", cloth_path])  # Uses system Python

def get_result_images(results_folder):
    """Fetches processed images from the results folder."""
    if not os.path.exists(results_folder):
        st.warning("⚠️ Results folder not found!")
        return []

    files = os.listdir(results_folder)
    if not files:
        st.warning("⚠️ No images found in the results folder!")
    
    return [
        os.path.join(results_folder, img)
        for img in files
        if img.endswith(('.jpg', '.png'))
    ]

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
            run_virtual_tryon(cloth_path)
            time.sleep(5)  # Allow script to process files

        st.success("🎉 Processing complete! Check the results below.")

        # Display generated images
        result_images = get_result_images(results_folder)

        if result_images:
            for img_path in result_images:
                st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
                with open(img_path, "rb") as file:
                    st.download_button(label="Download", data=file, file_name=os.path.basename(img_path), mime="image/jpeg")
        else:
            st.warning("⚠️ No output images found. Please check if the try-on process completed successfully.")
