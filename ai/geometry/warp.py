import cv2
import numpy as np
import os

# Image paths
image1_path = r"D:\SIH26166\Data\samples\image1.jpg"
image2_path = r"D:\SIH26166\Data\samples\image2.png"

# Read images
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

if image1 is None or image2 is None:
    print("❌ Images could not be loaded")
    exit()

print("✅ Both images loaded")


# SIFT

sift = cv2.SIFT_create()

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

print("Image 1 keypoints:", len(keypoints1))
print("Image 2 keypoints:", len(keypoints2))


# BFMatcher

bf = cv2.BFMatcher(cv2.NORM_L2)

matches = bf.knnMatch(descriptors1, descriptors2, k=2)

good_matches = []

for pair in matches:
    if len(pair) == 2:
        m, n = pair

        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

print("Good matches:", len(good_matches))


# Matching points

src_points = np.float32([
    keypoints1[m.queryIdx].pt
    for m in good_matches
]).reshape(-1, 1, 2)

dst_points = np.float32([
    keypoints2[m.trainIdx].pt
    for m in good_matches
]).reshape(-1, 1, 2)


# Homography + RANSAC

H, mask = cv2.findHomography(
    src_points,
    dst_points,
    cv2.RANSAC,
    5.0
)

if H is None:
    print("❌ Homography calculation failed")
    exit()

print("✅ Homography calculated")


# Warp Image 1 → Image 2

height, width = image2.shape[:2]

aligned_image = cv2.warpPerspective(
    image1,
    H,
    (width, height)
)


# Save result

result_dir = r"D:\SIH26166\Result\homography"
os.makedirs(result_dir, exist_ok=True)

output_path = os.path.join(
    result_dir,
    "aligned_image.jpg"
)

cv2.imwrite(output_path, aligned_image)

print("💾 Aligned image saved at:")
print(output_path)