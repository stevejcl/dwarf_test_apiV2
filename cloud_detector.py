import cv2
import numpy as np
import os

def detect_cloud_photo_histogram_and_stars(img_path1, img_path2, hist_thresh=0.2, star_min_area=2, star_max_area=30, debug=True):
    """
    Compare two images using histogram correlation and star count to detect clouds.

    Args:
        img_path1 (str): Path to the first image (previous).
        img_path2 (str): Path to the second image (latest).
        hist_thresh (float): Threshold below which histogram correlation indicates clouds.
        star_min_area (int): Minimum area of a blob to consider as a star.
        star_max_area (int): Maximum area of a blob to consider as a star.
        debug (bool): If True, shows extra info and saves debug images.

    Returns:
        bool: True if cloud is likely detected, False otherwise.
    """
    if not os.path.exists(img_path1) or not os.path.exists(img_path2):
        print(f"❌ One or both image paths do not exist:\n  - {img_path1}\n  - {img_path2}")
        return False

    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        print("❌ Could not read one or both images.")
        return False

    # Resize if needed
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Histogram comparison
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # Star detection using blob detector
    def count_stars(img):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = star_min_area
        params.maxArea = star_max_area
        params.filterByCircularity = False
        params.filterByInertia = False
        params.filterByConvexity = False
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(img)
        return len(keypoints)

    stars_img1 = count_stars(img1)
    stars_img2 = count_stars(img2)

    if debug:
        print(f"📊 Histogram correlation: {correlation:.4f}")
        print(f"✨ Stars in previous image: {stars_img1}")
        print(f"✨ Stars in latest image:   {stars_img2}")

    cloud_detected = False
    if correlation < hist_thresh:
        print("☁️ Histogram suggests cloud presence.")
        cloud_detected = True
    elif stars_img2 < stars_img1 * 0.5:
        print("☁️ Star count dropped significantly — likely clouds.")
        cloud_detected = True
    else:
        print("✅ Histogram and star count indicate clear sky.")

    return cloud_detected
