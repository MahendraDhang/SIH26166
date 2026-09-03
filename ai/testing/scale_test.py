import cv2
import numpy as np
import os


# ============================================================
# INPUT
# ============================================================

image_path = r"D:\SIH26166\Data\samples\image1.jpg"

output_dir = r"D:\SIH26166\Result\invariance\scale"

os.makedirs(output_dir, exist_ok=True)


# ============================================================
# LOAD IMAGE
# ============================================================

image = cv2.imread(image_path)

if image is None:
    print("❌ Image could not be loaded")
    exit()

print("✅ Original image loaded")


# ============================================================
# CREATE SCALED IMAGES
# ============================================================

scales = [
    0.5,
    0.75,
    1.0,
    1.5,
    2.0
]


# ============================================================
# SIFT
# ============================================================

sift = cv2.SIFT_create()


# Original image features

gray_original = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

kp_original, des_original = sift.detectAndCompute(
    gray_original,
    None
)

print("\nOriginal keypoints:", len(kp_original))


# ============================================================
# TEST EACH SCALE
# ============================================================

for scale in scales:

    print("\n" + "-" * 45)
    print("Testing scale:", scale)

    # Resize
    height, width = image.shape[:2]

    new_width = int(width * scale)
    new_height = int(height * scale)

    scaled_image = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR
    )

    # Save scaled image
    scaled_path = os.path.join(
        output_dir,
        f"scale_{scale}.jpg"
    )

    cv2.imwrite(
        scaled_path,
        scaled_image
    )

    # Grayscale
    gray_scaled = cv2.cvtColor(
        scaled_image,
        cv2.COLOR_BGR2GRAY
    )

    # SIFT
    kp_scaled, des_scaled = sift.detectAndCompute(
        gray_scaled,
        None
    )

    print(
        "Scaled keypoints:",
        len(kp_scaled)
    )

    if des_scaled is None:

        print("❌ No descriptors")
        continue

    # ========================================================
    # BF MATCHING
    # ========================================================

    bf = cv2.BFMatcher(
        cv2.NORM_L2
    )

    matches = bf.knnMatch(
        des_original,
        des_scaled,
        k=2
    )

    # Ratio test
    good_matches = []

    for pair in matches:

        if len(pair) == 2:

            m, n = pair

            if m.distance < 0.75 * n.distance:

                good_matches.append(m)

    print(
        "Good matches:",
        len(good_matches)
    )

    # ========================================================
    # RANSAC
    # ========================================================

    if len(good_matches) < 4:

        print(
            "⚠️ Not enough matches for Homography"
        )

        continue

    src_pts = np.float32([
        kp_original[m.queryIdx].pt
        for m in good_matches
    ]).reshape(-1, 1, 2)

    dst_pts = np.float32([
        kp_scaled[m.trainIdx].pt
        for m in good_matches
    ]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(
        src_pts,
        dst_pts,
        cv2.RANSAC,
        5.0
    )

    if H is None:

        print("❌ Homography failed")
        continue

    mask = mask.ravel()

    inliers = int(np.sum(mask))

    outliers = len(mask) - inliers

    inlier_ratio = (
        inliers /
        len(good_matches)
    )

    print("Inliers:", inliers)
    print("Outliers:", outliers)

    print(
        "Inlier Ratio:",
        round(inlier_ratio, 3)
    )

    # ========================================================
    # DRAW INLIERS
    # ========================================================

    inlier_matches = []

    for i, match in enumerate(good_matches):

        if mask[i]:

            inlier_matches.append(match)

    result = cv2.drawMatches(
        image,
        kp_original,
        scaled_image,
        kp_scaled,
        inlier_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    result_path = os.path.join(
        output_dir,
        f"scale_{scale}_matches.jpg"
    )

    cv2.imwrite(
        result_path,
        result
    )

    print(
        "💾 Result saved:",
        result_path
    )


print("\n" + "=" * 45)
print("SCALE INVARIANCE TEST COMPLETED")
print("=" * 45)