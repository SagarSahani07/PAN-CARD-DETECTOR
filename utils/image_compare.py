import cv2
import os
from skimage.metrics import structural_similarity

def compare_images(original_path, tampered_path):
    # Read images
    original = cv2.imread(original_path)
    tampered = cv2.imread(tampered_path)

    if original is None or tampered is None:
        return {
            "similarity_score": 0,
            "status": "Error Reading Images",
            "original_result": "",
            "tampered_result": "",
            "difference_result": ""
        }

    # Resize images to same size
    width = 700
    height = 500

    original = cv2.resize(original, (width, height))
    tampered = cv2.resize(tampered, (width, height))

    # Convert to grayscale
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    tampered_gray = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(original_gray, tampered_gray, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold difference image
    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]

    # Find contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    tampered_regions = 0

    # Draw bounding boxes on changed areas
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 40:
            tampered_regions += 1

            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(
                original,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            cv2.rectangle(
                tampered,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

    # Create output folder if not exists
    output_folder = "static/output"
    os.makedirs(output_folder, exist_ok=True)

    # Output image paths
    original_result_path = os.path.join(output_folder, "original_result.jpg")
    tampered_result_path = os.path.join(output_folder, "tampered_result.jpg")
    difference_result_path = os.path.join(output_folder, "difference_result.jpg")

    # Save processed images
    cv2.imwrite(original_result_path, original)
    cv2.imwrite(tampered_result_path, tampered)
    cv2.imwrite(difference_result_path, thresh)

    # Convert score to percentage
    similarity_percentage = round(score * 100, 2)

    # Detection logic
    if similarity_percentage >= 98:
        status = "No Tampering Detected"
    elif similarity_percentage >= 90:
        status = "Minor Changes Detected"
    else:
        status = "PAN Card May Be Tampered"

    return {
        "similarity_score": similarity_percentage,
        "status": status,
        "original_result": original_result_path,
        "tampered_result": tampered_result_path,
        "difference_result": difference_result_path,
        "tampered_regions": tampered_regions
    }
