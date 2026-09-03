import cv2
import os


# Preprocessed images
image1_path = r"D:\SIH26166\result\preprocessed\image1_preprocessed.jpg"
image2_path = r"D:\SIH26166\result\preprocessed\image2_preprocessed.jpg"

# Output
output_dir = r"D:\SIH26166\result\matches_preprocessed"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(
    output_dir,
    "bf_preprocessed_matches.jpg"
)


# Read images
img1 = cv2.imread(image1_path)
img2 = cv2.imread(image2_path)

if img1 is None or img2 is None:
    print("❌ Images not found")
    exit()

print("✅ Both preprocessed images loaded")


# Convert to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


# SIFT
sift = cv2.SIFT_create()

kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

print("Image 1 keypoints:", len(kp1))
print("Image 2 keypoints:", len(kp2))


# BF Matcher
bf = cv2.BFMatcher(cv2.NORM_L2)

matches = bf.knnMatch(
    des1,
    des2,
    k=2
)

print("Total candidate matches:", len(matches))


# Lowe's Ratio Test
good_matches = []

for m, n in matches:

    if m.distance < 0.75 * n.distance:
        good_matches.append(m)


print("Good matches:", len(good_matches))


# Draw matches
matched_image = cv2.drawMatches(
    img1,
    kp1,
    img2,
    kp2,
    good_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)


# Save
cv2.imwrite(
    output_path,
    matched_image
)

print("✅ Match result saved:")
print(output_path)