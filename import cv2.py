import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
def generate_cloth_mask(input_path, output_path="C:\\Users\\MSI\\Desktop\\clothes wala\\Virtual-Try-On\\datasets\\test\\cloth-mask\\cloth-mask.jpg"):
    if not os.path.exists(input_path):
        print(f"Error: File not found - {input_path}")
        return
    
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Unable to read the image at {input_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphological closing (reduce kernel size)
    kernel = np.ones((15, 15), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty mask
    mask = np.zeros_like(gray)

    # **FIX:** Keep all contours above a threshold size
    min_area = 5000  # Adjust as needed
    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            cv2.drawContours(mask, [cnt], -1, 255, thickness=cv2.FILLED)

    # Save the final mask
    cv2.imwrite(output_path, mask)

    # Show results
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(thresh, cmap="gray")
    plt.title("Binary Thresholding")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(mask, cmap="gray")
    plt.title("Final Cloth Mask (Fixed)")
    plt.axis("off")

    plt.show()

    print(f"✅ Cloth mask saved at: {output_path}")

# Example usage
image_path = "C:/Users/MSI/Desktop/clothes wala/Virtual-Try-On/datasets/test/cloth/cloth.jpg"
generate_cloth_mask(image_path)
