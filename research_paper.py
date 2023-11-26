import cv2
import numpy as np

def calculate_psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return round(psnr, 4)

def calculate_mse(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    return round(mse, 4)

# Example usage:
# Load the original and compressed images
original_image = cv2.imread('./pics/image7.jpg')
compressed_image = cv2.imread('final.png')

# Convert images to grayscale if they are in color
original_image_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
compressed_image_gray = cv2.cvtColor(compressed_image, cv2.COLOR_BGR2GRAY)

# Calculate PSNR and MSE
psnr_value = calculate_psnr(original_image_gray, compressed_image_gray)
mse_value = calculate_mse(original_image_gray, compressed_image_gray)

# Print the results
print(f"PSNR: {psnr_value} dB")
print(f"MSE: {mse_value}")
