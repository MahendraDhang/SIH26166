import cv2
import os

# Image paths
image1_path = r"D:\SIH26166\Data\samples\image1.jpg"
image2_path = r"D:\SIH26166\Data\samples\image2.png"

# Read images
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

if image1 is None or image2 is None:
    print("❌ Could not load images")
    exit()

print("✅ Both images loaded")

# Convert to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Create SIFT
sift = cv2.SIFT_create()

# Detect features
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

print("Image 1 keypoints:", len(keypoints1))
print("Image 2 keypoints:", len(keypoints2))

# Create BFMatcher
bf = cv2.BFMatcher(cv2.NORM_L2)

# Find 2 nearest matches for each descriptor
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

print("Total candidate matches:", len(matches))

# Lowe's Ratio Test
good_matches = []

for pair in matches:
    if len(pair) == 2:
        m, n = pair

        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

print("Good matches:", len(good_matches))

# Draw good matches
matched_image = cv2.drawMatches(
    image1,
    keypoints1,
    image2,
    keypoints2,
    good_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

# Create result folder
result_dir = r"D:\SIH26166\Result\matches"
os.makedirs(result_dir, exist_ok=True)

# Save result
output_path = os.path.join(result_dir, "bf_good_matches.jpg")

cv2.imwrite(output_path, matched_image)

print("💾 Match result saved at:")
print(output_path)