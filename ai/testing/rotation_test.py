import cv2
import numpy as np
import os


# ============================================================
# INPUT
# ============================================================

image_path = r"D:\SIH26166\Data\samples\image1.jpg"

output_dir = r"D:\SIH26166\Result\invariance\rotation"

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
# ROTATION ANGLES
# ============================================================

angles = [
    -90,
    -45,
    -30,
    -15,
    0,
    15,
    30,
    45,
    90
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
# TEST EACH ROTATION
# ============================================================

for angle in angles:

    print("\n" + "-" * 50)
    print("Testing rotation:", angle, "degrees")

    height, width = image.shape[:2]

    center = (
        width // 2,
        height // 2
    )

    # Rotation matrix
    matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    # Rotate image
    rotated = cv2.warpAffine(
        image,
        matrix,
        (width, height)
    )

    # Save rotated image
    rotated_path = os.path.join(
        output_dir,
        f"rotation_{angle}.jpg"
    )

    cv2.imwrite(
        rotated_path,
        rotated
    )

    # ========================================================
    # SIFT ON ROTATED IMAGE
    # ========================================================

    gray_rotated = cv2.cvtColor(
        rotated,
        cv2.COLOR_BGR2GRAY
    )

    kp_rotated, des_rotated = sift.detectAndCompute(
        gray_rotated,
        None
    )

    print(
        "Rotated keypoints:",
        len(kp_rotated)
    )

    if des_rotated is None:

        print("❌ No descriptors found")
        continue


    # ========================================================
    # BF MATCHING
    # ========================================================

    bf = cv2.BFMatcher(
        cv2.NORM_L2
    )

    matches = bf.knnMatch(
        des_original,
        des_rotated,
        k=2
    )

    # Lowe Ratio Test
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
    # HOMOGRAPHY + RANSAC
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
        kp_rotated[m.trainIdx].pt
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
        inliers / len(good_matches)
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
        rotated,
        kp_rotated,
        inlier_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )


    result_path = os.path.join(
        output_dir,
        f"rotation_{angle}_matches.jpg"
    )


    cv2.imwrite(
        result_path,
        result
    )


    print(
        "💾 Result saved:",
        result_path
    )


print("\n" + "=" * 50)
print("ROTATION INVARIANCE TEST COMPLETED")
print("=" * 50)