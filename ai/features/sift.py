import cv2
import os


def detect_sift(image_path, output_name=None):
    # Read image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not found or could not be read: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors
    keypoints, descriptors = sift.detectAndCompute(gray, None)

    print("Keypoints detected:", len(keypoints))

    if descriptors is not None:
        print("Descriptor shape:", descriptors.shape)
    else:
        print("No descriptors found.")

    # Draw keypoints on image
    result = cv2.drawKeypoints(
        image,
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    # Save output if output name is provided
    if output_name:
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", output_name)
        cv2.imwrite(output_path, result)
        print("Result saved:", output_path)

    return keypoints, descriptors