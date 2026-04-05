import cv2
import os
import time
import numpy as np
from PIL import Image, ImageOps
from skimage.metrics import structural_similarity


def compare_images(original_path, tampered_path):
    # Create output folder
    output_folder = 'static/output'
    os.makedirs(output_folder, exist_ok=True)

    timestamp = str(int(time.time()))

    # Open images with proper EXIF orientation
    original = ImageOps.exif_transpose(Image.open(original_path)).convert("RGB")
    tampered = ImageOps.exif_transpose(Image.open(tampered_path)).convert("RGB")

    print("Original Size Before Resize:", original.size)
    print("Tampered Size Before Resize:", tampered.size)

    # Crop whitespace if present
    original = original.crop(original.getbbox())
    tampered = tampered.crop(tampered.getbbox())

    # Resize both images to same minimum dimensions
    width = min(original.size[0], tampered.size[0])
    height = min(original.size[1], tampered.size[1])

    original = original.resize((width, height))
    tampered = tampered.resize((width, height))

    print("Original Size After Resize:", original.size)
    print("Tampered Size After Resize:", tampered.size)

    # Convert PIL images directly to OpenCV format
    original_cv = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
    tampered_cv = cv2.cvtColor(np.array(tampered), cv2.COLOR_RGB2BGR)

    print("Original Shape:", original_cv.shape)
    print("Tampered Shape:", tampered_cv.shape)

    # Convert to grayscale
    original_gray = cv2.cvtColor(original_cv, cv2.COLOR_BGR2GRAY)
    tampered_gray = cv2.cvtColor(tampered_cv, cv2.COLOR_BGR2GRAY)

    # Reduce noise slightly
    original_gray = cv2.GaussianBlur(original_gray, (5, 5), 0)
    tampered_gray = cv2.GaussianBlur(tampered_gray, (5, 5), 0)

    # Compute similarity
    score, diff = structural_similarity(original_gray, tampered_gray, full=True)

    similarity_percentage = max(round(score * 100, 2), 1)

    print("SSIM Raw Score:", score)
    print("Similarity Percentage:", similarity_percentage)

    # Convert diff image
    diff = (diff * 255).astype("uint8")

    # Threshold
    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]

    # Find contours
    contours, _ = cv2.findContours(
        thresh.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    tampered_regions = 0

    # Draw rectangles around changed regions
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 10:
            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(original_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(tampered_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)

            tampered_regions += 1

    print("Tampered Regions:", tampered_regions)

    # Detection status
    if similarity_percentage >= 90:
        status = "No Tampering Detected"
    elif similarity_percentage >= 60:
        status = "Minor Changes Detected"
    else:
        status = "PAN Card May Be Tampered"

    # Output image paths
    original_result_path = os.path.join(output_folder, f"original_result_{timestamp}.jpg")
    tampered_result_path = os.path.join(output_folder, f"tampered_result_{timestamp}.jpg")
    difference_result_path = os.path.join(output_folder, f"difference_result_{timestamp}.jpg")

    # Save result images
    cv2.imwrite(original_result_path, original_cv)
    cv2.imwrite(tampered_result_path, tampered_cv)
    cv2.imwrite(difference_result_path, thresh)

    return {
        'similarity_score': similarity_percentage,
        'status': status,
        'tampered_regions': tampered_regions,
        'original_result': original_result_path.replace("static/", ""),
        'tampered_result': tampered_result_path.replace("static/", ""),
        'difference_result': difference_result_path.replace("static/", "")
    }