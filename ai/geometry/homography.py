import cv2
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

# Convert to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# SIFT
sift = cv2.SIFT_create()

keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

print("Image 1 keypoints:", len(keypoints1))
print("Image 2 keypoints:", len(keypoints2))

# BF Matcher
bf = cv2.BFMatcher(cv2.NORM_L2)

matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# Lowe Ratio Test
good_matches = []

for pair in matches:
    if len(pair) == 2:
        m, n = pair

        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

print("Good matches:", len(good_matches))

# Need at least 4 points for homography
if len(good_matches) < 4:
    print("❌ Not enough matches for homography")
    exit()

# Get matching coordinates
src_points = []
dst_points = []

for match in good_matches:
    src_points.append(keypoints1[match.queryIdx].pt)
    dst_points.append(keypoints2[match.trainIdx].pt)

src_points = __import__("numpy").float32(src_points).reshape(-1, 1, 2)
dst_points = __import__("numpy").float32(dst_points).reshape(-1, 1, 2)

# RANSAC Homography
H, mask = cv2.findHomography(
    src_points,
    dst_points,
    cv2.RANSAC,
    5.0
)

if H is None:
    print("❌ Homography could not be calculated")
    exit()

print("\n✅ Homography calculated!")
print("\nHomography Matrix:")
print(H)

# Inliers and outliers
inlier_mask = mask.ravel().tolist()

inliers = sum(inlier_mask)
outliers = len(inlier_mask) - inliers

print("\nTotal good matches:", len(good_matches))
print("✅ Inliers:", inliers)
print("❌ Outliers:", outliers)

inlier_ratio = inliers / len(good_matches)

print("📊 Inlier Ratio:", round(inlier_ratio, 3))

# Draw only inlier matches
inlier_matches = []

for i, match in enumerate(good_matches):
    if inlier_mask[i]:
        inlier_matches.append(match)

result = cv2.drawMatches(
    image1,
    keypoints1,
    image2,
    keypoints2,
    inlier_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

# Create output folder
result_dir = r"D:\SIH26166\Result\homography"
os.makedirs(result_dir, exist_ok=True)

output_path = os.path.join(
    result_dir,
    "homography_inliers.jpg"
)

cv2.imwrite(output_path, result)

print("\n💾 Result saved at:")
print(output_path)