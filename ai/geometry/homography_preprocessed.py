import cv2
import numpy as np
import os


# INPUT FILES


image1_path = r"D:\SIH26166\data\samples\image1.jpg"
image2_path = r"D:\SIH26166\data\samples\image2.png"

matches_path = r"D:\SIH26166\result\matches\bf_preprocessed_matches.jpg"


# LOAD IMAGES


img1 = cv2.imread(image1_path)
img2 = cv2.imread(image2_path)

if img1 is None or img2 is None:
    print("❌ Error: Images could not be loaded")
    exit()

print("🟢 Both images loaded")


# LOAD SIFT KEYPOINTS


sift = cv2.SIFT_create()

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

print("Image 1 keypoints:", len(kp1))
print("Image 2 keypoints:", len(kp2))


# MATCH FEATURES


bf = cv2.BFMatcher(cv2.NORM_L2)

matches = bf.knnMatch(des1, des2, k=2)

good_matches = []

for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

print("Good matches:", len(good_matches))


# CHECK ENOUGH MATCHES


if len(good_matches) < 4:
    print("❌ Not enough matches for Homography")
    exit()


# GET MATCH POINTS


src_pts = np.float32(
    [kp1[m.queryIdx].pt for m in good_matches]
).reshape(-1, 1, 2)

dst_pts = np.float32(
    [kp2[m.trainIdx].pt for m in good_matches]
).reshape(-1, 1, 2)


# HOMOGRAPHY USING RANSAC


H, mask = cv2.findHomography(
    src_pts,
    dst_pts,
    cv2.RANSAC,
    5.0
)

if H is None:
    print("❌ Homography could not be calculated")
    exit()

print("\n✅ Homography calculated!")
print("\nHomography Matrix:")
print(H)


# INLIERS / OUTLIERS


inliers = int(np.sum(mask))
outliers = len(good_matches) - inliers

inlier_ratio = inliers / len(good_matches)

print("\nTotal good matches:", len(good_matches))
print("Inliers:", inliers)
print("Outliers:", outliers)
print("Inlier Ratio:", round(inlier_ratio, 3))


# DRAW INLIER MATCHES


matches_mask = mask.ravel().tolist()

inlier_matches = []

for i, m in enumerate(good_matches):
    if matches_mask[i]:
        inlier_matches.append(m)

match_image = cv2.drawMatches(
    img1,
    kp1,
    img2,
    kp2,
    inlier_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)


# SAVE RESULT


output_dir = r"D:\SIH26166\result\homography_preprocessed"

os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(
    output_dir,
    "homography_preprocessed_inliers.jpg"
)

cv2.imwrite(output_path, match_image)

print("\n📁 Result saved at:")
print(output_path)
