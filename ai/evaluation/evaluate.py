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

print("✅ Images loaded")



# SIFT Feature Detection

sift = cv2.SIFT_create()

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

print("Image 1 keypoints:", len(keypoints1))
print("Image 2 keypoints:", len(keypoints2))



# BFMatcher

bf = cv2.BFMatcher(cv2.NORM_L2)

matches = bf.knnMatch(
    descriptors1,
    descriptors2,
    k=2
)


# Lowe Ratio Test

good_matches = []

for pair in matches:

    if len(pair) == 2:

        m, n = pair

        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

print("Good matches:", len(good_matches))



# Check minimum matches

if len(good_matches) < 4:

    print("❌ Not enough matches for evaluation")
    exit()


# Get matching points

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



# Inliers / Outliers

mask = mask.ravel()

inliers = int(np.sum(mask))
outliers = len(mask) - inliers

inlier_ratio = inliers / len(good_matches)



# Reprojection Error

projected_points = cv2.perspectiveTransform(
    src_points,
    H
)

errors = []

for i in range(len(dst_points)):

    if mask[i]:

        error = np.linalg.norm(
            projected_points[i][0] -
            dst_points[i][0]
        )

        errors.append(error)


if len(errors) > 0:

    mean_error = float(np.mean(errors))
    max_error = float(np.max(errors))
    min_error = float(np.min(errors))

else:

    mean_error = 0
    max_error = 0
    min_error = 0



# Print Evaluation

print("\n" + "=" * 45)
print("        IMAGE CORRESPONDENCE EVALUATION")
print("=" * 45)

print("Image 1 Keypoints     :", len(keypoints1))
print("Image 2 Keypoints     :", len(keypoints2))

print("Good Matches          :", len(good_matches))

print("Inliers               :", inliers)
print("Outliers              :", outliers)

print("Inlier Ratio          :", round(inlier_ratio, 3))

print("Mean Reprojection Err :", round(mean_error, 3), "pixels")
print("Min Reprojection Err  :", round(min_error, 3), "pixels")
print("Max Reprojection Err  :", round(max_error, 3), "pixels")

print("=" * 45)



# Save Report

result_dir = r"D:\SIH26166\Result\reports"

os.makedirs(result_dir, exist_ok=True)

report_path = os.path.join(
    result_dir,
    "evaluation_report.txt"
)

with open(report_path, "w") as file:

    file.write("IMAGE CORRESPONDENCE EVALUATION\n")
    file.write("=" * 45 + "\n")

    file.write(
        f"Image 1 Keypoints: {len(keypoints1)}\n"
    )

    file.write(
        f"Image 2 Keypoints: {len(keypoints2)}\n"
    )

    file.write(
        f"Good Matches: {len(good_matches)}\n"
    )

    file.write(
        f"Inliers: {inliers}\n"
    )

    file.write(
        f"Outliers: {outliers}\n"
    )

    file.write(
        f"Inlier Ratio: {inlier_ratio:.3f}\n"
    )

    file.write(
        f"Mean Reprojection Error: {mean_error:.3f} pixels\n"
    )

    file.write(
        f"Min Reprojection Error: {min_error:.3f} pixels\n"
    )

    file.write(
        f"Max Reprojection Error: {max_error:.3f} pixels\n"
    )

print("\n💾 Report saved at:")
print(report_path)