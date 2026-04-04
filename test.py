import cv2
import numpy as np
from skimage.metrics import structural_similarity

print("OpenCV Version:", cv2.__version__)
print("NumPy Version:", np.__version__)

img1 = np.zeros((300, 300), dtype="uint8")
img2 = np.zeros((300, 300), dtype="uint8")

cv2.rectangle(img2, (100, 100), (200, 200), 255, -1)

score, diff = structural_similarity(img1, img2, full=True)

print("SSIM Score:", score)
print("Everything is working correctly.")
