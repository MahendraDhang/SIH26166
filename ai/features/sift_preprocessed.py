import cv2
import os

# Preprocessed image paths
image1_path = r"D:\SIH26166\result\preprocessed\image1_preprocessed.jpg"
image2_path = r"D:\SIH26166\result\preprocessed\image2_preprocessed.jpg"

# Output directory
output_dir = r"D:\SIH26166\result\keypoints_preprocessed"
os.makedirs(output_dir, exist_ok=True)


def extract_sift(image_path, output_name):

    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not found:", image_path)
        return

    # SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors
    keypoints, descriptors = sift.detectAndCompute(image, None)

    print("\nImage:", os.path.basename(image_path))
    print("🔹 Keypoints detected:", len(keypoints))

    if descriptors is not None:
        print("🔹 Descriptor shape:", descriptors.shape)

    # Draw keypoints
    result = cv2.drawKeypoints(
        image,
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    output_path = os.path.join(output_dir, output_name)

    cv2.imwrite(output_path, result)

    print("💾 Result saved:", output_path)


# Process both images
extract_sift(
    image1_path,
    "image1_preprocessed_sift.jpg"
)

extract_sift(
    image2_path,
    "image2_preprocessed_sift.jpg"
)