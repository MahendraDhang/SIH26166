import cv2
import os


def preprocess_image(image_path, output_path):
    # Read image
    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not found:", image_path)
        return False

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Slight noise reduction
    enhanced = cv2.GaussianBlur(
        enhanced,
        (3, 3),
        0
    )

    # Create output directory
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    # Save result
    cv2.imwrite(output_path, enhanced)

    print("✅ Preprocessed image saved:")
    print(output_path)

    return True


if __name__ == "__main__":

    image1 = r"D:\SIH26166\data\samples\image1.jpg"
    image2 = r"D:\SIH26166\data\samples\image2.png"

    output1 = r"D:\SIH26166\result\preprocessed\image1_preprocessed.jpg"
    output2 = r"D:\SIH26166\result\preprocessed\image2_preprocessed.jpg"

    preprocess_image(image1, output1)
    preprocess_image(image2, output2)