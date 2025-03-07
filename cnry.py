import cloudinary
import cloudinary.uploader
import os

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dvfdf9uqh",
    api_key="328511124772772",
    api_secret="KtfBQEGsdeCbZcdBkRBMCSs7BPI",  # Replace with your actual API secret
    secure=True
)

# Define the local folder path
folder_path = "C:/Users/MSI/Desktop/clothes wala/Virtual-Try-On/datasets/test/cloth"

# Define the Cloudinary folder name
cloudinary_folder = "virtual_tryon/cloth"  # Change this to your preferred folder

# Upload all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path):  # Ensure it's a file
        upload_result = cloudinary.uploader.upload(
            file_path,
            folder=cloudinary_folder  # ✅ Ensures file is placed inside the correct folder
        )

        print(f"✅ Uploaded {filename} -> {upload_result['secure_url']}")

