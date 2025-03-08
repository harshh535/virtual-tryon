import streamlit as st
import os
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set paths
UPLOAD_FOLDER = "cloth/"
RESULTS_FOLDER = "results/"
AUTOMATED_SCRIPT = "automated.py"  # Only calling this

# Ensure required folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Streamlit UI
st.set_page_config(page_title="Virtual Try-On System", layout="wide")

st.title("👕 Virtual Try-On System")
st.write("Upload a clothing image and see it applied on all models!")

# File uploader
uploaded_file = st.file_uploader("Choose a clothing image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Image saved: {uploaded_file.name}")

# Button to run the virtual try-on process
if st.button("Run Virtual Try-On"):
    st.info("⏳ Running the virtual try-on process (automated.py)... Please wait.")

    # Run automated.py (which internally runs test.py)
    auto_result = subprocess.run(["python", AUTOMATED_SCRIPT], capture_output=True, text=True)

    st.text(auto_result.stdout)
    if auto_result.stderr:
        st.error("❌ Error in automated.py")
        st.text(auto_result.stderr)
        st.stop()  # Stop execution if error occurs

    # Wait for results to be generated
    time.sleep(5)

    # Check if images exist in results folder
    if os.path.exists(RESULTS_FOLDER) and os.listdir(RESULTS_FOLDER):
        st.success("🎉 Virtual try-on completed! Here are the results:")
        
        # Display images
        for image_file in os.listdir(RESULTS_FOLDER):
            image_path = os.path.join(RESULTS_FOLDER, image_file)
            st.image(image_path, caption=image_file, use_container_width=True)
    else:
        st.warning("⚠️ No output images found. Please check if the try-on process completed successfully.")

# Button to check files in results folder
if st.button("Check Results Folder"):
    if os.path.exists(RESULTS_FOLDER):
        files = os.listdir(RESULTS_FOLDER)
        if files:
            st.write("✅ Found the following output images:")
            for file in files:
                st.write(file)
        else:
            st.write("⚠️ No images found in results/.")
    else:
        st.write("⚠️ results/ folder does not exist.")
