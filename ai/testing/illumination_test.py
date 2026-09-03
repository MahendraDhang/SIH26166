import cv2
import numpy as np
import os


# INPUT


image_path = r"D:\SIH26166\Data\samples\image1.jpg"

output_dir = r"D:\SIH26166\Result\invariance\illumination"

os.makedirs(output_dir, exist_ok=True)



# LOAD IMAGE


image = cv2.imread(image_path)

if image is None:
    print("❌ Image could not be loaded")
    exit()

print("✅ Original image loaded")



# ILLUMINATION CONDITIONS
# alpha = contrast
# beta  = brightness
#
# output = alpha * image + beta


conditions = {
    "very_dark": (0.5, -50),
    "dark": (0.7, -30),
    "slightly_dark": (0.85, -15),
    "original": (1.0, 0),
    "bright": (1.2, 25),
    "very_bright": (1.5, 50)
}



# SIFT


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



# TEST EACH ILLUMINATION CONDITION


for name, (alpha, beta) in conditions.items():

    print("\n" + "-" * 55)
    print("Testing:", name)
    print("Contrast:", alpha, "| Brightness:", beta)


   
    # CHANGE ILLUMINATION
    

    modified = cv2.convertScaleAbs(
        image,
        alpha=alpha,
        beta=beta
    )


    # Save modified image
    modified_path = os.path.join(
        output_dir,
        f"{name}.jpg"
    )

    cv2.imwrite(
        modified_path,
        modified
    )


 
    # SIFT ON MODIFIED IMAGE
    

    gray_modified = cv2.cvtColor(
        modified,
        cv2.COLOR_BGR2GRAY
    )

    kp_modified, des_modified = sift.detectAndCompute(
        gray_modified,
        None
    )

    print(
        "Modified keypoints:",
        len(kp_modified)
    )


    if des_modified is None:

        print("❌ No descriptors found")
        continue


  
    # BF MATCHING
    

    bf = cv2.BFMatcher(
        cv2.NORM_L2
    )

    matches = bf.knnMatch(
        des_original,
        des_modified,
        k=2
    )


   
    # LOWE RATIO TEST
    

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


    
    # HOMOGRAPHY + RANSAC
   

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
        kp_modified[m.trainIdx].pt
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


   
    # METRICS
    

    inliers = int(np.sum(mask))

    outliers = len(mask) - inliers

    inlier_ratio = (
        inliers /
        len(good_matches)
    )


    print("Inliers:", inliers)
    print("Outliers:", outliers)

    print(
        "Inlier Ratio:",
        round(inlier_ratio, 3)
    )


  
    # REPROJECTION ERROR


    projected = cv2.perspectiveTransform(
        src_pts,
        H
    )


    errors = []

    for i in range(len(dst_pts)):

        if mask[i]:

            error = np.linalg.norm(
                projected[i][0] -
                dst_pts[i][0]
            )

            errors.append(error)


    if errors:

        mean_error = float(
            np.mean(errors)
        )

        print(
            "Mean Reprojection Error:",
            round(mean_error, 3),
            "pixels"
        )


    
    # DRAW INLIERS

    inlier_matches = []

    for i, match in enumerate(good_matches):

        if mask[i]:

            inlier_matches.append(match)


    result = cv2.drawMatches(
        image,
        kp_original,
        modified,
        kp_modified,
        inlier_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )


    result_path = os.path.join(
        output_dir,
        f"{name}_matches.jpg"
    )


    cv2.imwrite(
        result_path,
        result
    )


    print(
        "💾 Result saved:",
        result_path
    )



# COMPLETE


print("\n" + "=" * 55)
print("ILLUMINATION INVARIANCE TEST COMPLETED")
print("=" * 55)