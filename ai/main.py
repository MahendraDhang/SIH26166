import cv2
import numpy as np
import os


# ============================================================
# BASE / RESULT DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RESULT_DIR = os.path.join(
    BASE_DIR,
    "Result"
)

PREPROCESSED_DIR = os.path.join(
    RESULT_DIR,
    "preprocessed"
)

MATCH_DIR = os.path.join(
    RESULT_DIR,
    "pipeline_matches"
)

HOMOGRAPHY_DIR = os.path.join(
    RESULT_DIR,
    "pipeline_homography"
)

REPORT_DIR = os.path.join(
    RESULT_DIR,
    "pipeline_reports"
)


# ============================================================
# CREATE RESULT DIRECTORIES
# ============================================================

os.makedirs(PREPROCESSED_DIR, exist_ok=True)
os.makedirs(MATCH_DIR, exist_ok=True)
os.makedirs(HOMOGRAPHY_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ============================================================
# IMAGE RESIZE FOR FAST PROCESSING
# ============================================================

MAX_PROCESS_SIZE = 1600


def resize_for_processing(image):
    """
    Resize image while preserving aspect ratio.
    Images smaller than MAX_PROCESS_SIZE are not enlarged.
    """

    height, width = image.shape[:2]

    max_dimension = max(
        height,
        width
    )

    if max_dimension <= MAX_PROCESS_SIZE:
        return image

    scale = (
        MAX_PROCESS_SIZE /
        max_dimension
    )

    new_width = int(
        width * scale
    )

    new_height = int(
        height * scale
    )

    return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline(image1_path, image2_path):

    # ========================================================
    # 1. LOAD IMAGES
    # ========================================================

    image1 = cv2.imread(
        image1_path
    )

    image2 = cv2.imread(
        image2_path
    )

    if image1 is None:
        raise ValueError(
            "Could not load Image 1"
        )

    if image2 is None:
        raise ValueError(
            "Could not load Image 2"
        )


    # ========================================================
    # 2. RESIZE FOR FAST PROCESSING
    # ========================================================

    image1 = resize_for_processing(
        image1
    )

    image2 = resize_for_processing(
        image2
    )


    # ========================================================
    # 3. PREPROCESSING
    # ========================================================

    gray1 = cv2.cvtColor(
        image1,
        cv2.COLOR_BGR2GRAY
    )

    gray2 = cv2.cvtColor(
        image2,
        cv2.COLOR_BGR2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    processed1 = clahe.apply(
        gray1
    )

    processed2 = clahe.apply(
        gray2
    )


    # ========================================================
    # 4. SAVE PREPROCESSED IMAGES
    # ========================================================

    preprocessed1_output = os.path.join(
        PREPROCESSED_DIR,
        "image1_preprocessed.jpg"
    )

    preprocessed2_output = os.path.join(
        PREPROCESSED_DIR,
        "image2_preprocessed.jpg"
    )

    cv2.imwrite(
        preprocessed1_output,
        processed1
    )

    cv2.imwrite(
        preprocessed2_output,
        processed2
    )


    # ========================================================
    # 5. SIFT FEATURE EXTRACTION
    # ========================================================

    sift = cv2.SIFT_create(
        nfeatures=5000,
        contrastThreshold=0.04,
        edgeThreshold=10,
        sigma=1.6
    )

    kp1, des1 = sift.detectAndCompute(
        processed1,
        None
    )

    kp2, des2 = sift.detectAndCompute(
        processed2,
        None
    )

    if des1 is None or des2 is None:
        raise ValueError(
            "Could not extract features from images"
        )


    # ========================================================
    # 6. BF MATCHING
    # ========================================================

    bf = cv2.BFMatcher(
        cv2.NORM_L2
    )

    matches = bf.knnMatch(
        des1,
        des2,
        k=2
    )


    # ========================================================
    # 7. LOWE RATIO TEST
    # ========================================================

    good_matches = []

    for pair in matches:

        if len(pair) == 2:

            m, n = pair

            if m.distance < 0.75 * n.distance:

                good_matches.append(
                    m
                )


    # ========================================================
    # 8. MATCH VISUALIZATION
    # ========================================================

    match_image = cv2.drawMatches(
        processed1,
        kp1,
        processed2,
        kp2,
        good_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    match_output = os.path.join(
        MATCH_DIR,
        "pipeline_good_matches.jpg"
    )

    cv2.imwrite(
        match_output,
        match_image
    )


    # ========================================================
    # 9. NOT ENOUGH MATCHES
    # ========================================================

    if len(good_matches) < 4:

        return {

            "status": "partial",

            "message":
                f"Feature matching completed, "
                f"but only {len(good_matches)} reliable "
                f"candidate matches were found. "
                f"At least 4 matches are required "
                f"for geometric verification.",

            "image1_keypoints":
                len(kp1),

            "image2_keypoints":
                len(kp2),

            "candidate_matches":
                len(matches),

            "good_matches":
                len(good_matches),

            "inliers":
                0,

            "outliers":
                len(good_matches),

            "inlier_ratio":
                0.0,

            "mean_reprojection_error":
                0.0,

            "min_reprojection_error":
                0.0,

            "max_reprojection_error":
                0.0,

            "matches_image":
                match_output,

            "inliers_image":
                None,

            "aligned_image":
                None
        }


    # ========================================================
    # 10. MATCH POINTS
    # ========================================================

    src_pts = np.float32([

        kp1[m.queryIdx].pt

        for m in good_matches

    ]).reshape(
        -1,
        1,
        2
    )

    dst_pts = np.float32([

        kp2[m.trainIdx].pt

        for m in good_matches

    ]).reshape(
        -1,
        1,
        2
    )


    # ========================================================
    # 11. HOMOGRAPHY + GEOMETRIC VERIFICATION
    # ========================================================

    H, mask = cv2.findHomography(
        src_pts,
        dst_pts,
        cv2.USAC_MAGSAC,
        3.0
    )

    if H is None or mask is None:

        return {

            "status": "partial",

            "message":
                "Feature matching completed, "
                "but geometric verification failed.",

            "image1_keypoints":
                len(kp1),

            "image2_keypoints":
                len(kp2),

            "candidate_matches":
                len(matches),

            "good_matches":
                len(good_matches),

            "inliers":
                0,

            "outliers":
                len(good_matches),

            "inlier_ratio":
                0.0,

            "mean_reprojection_error":
                0.0,

            "min_reprojection_error":
                0.0,

            "max_reprojection_error":
                0.0,

            "matches_image":
                match_output,

            "inliers_image":
                None,

            "aligned_image":
                None
        }


    mask = mask.ravel()


    # ========================================================
    # 12. INLIERS / OUTLIERS
    # ========================================================

    inliers = int(
        np.sum(mask)
    )

    outliers = (
        len(mask) - inliers
    )

    inlier_ratio = (
        inliers /
        len(good_matches)
    )


    # ========================================================
    # 13. INLIER VISUALIZATION
    # ========================================================

    inlier_matches = [

        match

        for i, match
        in enumerate(good_matches)

        if mask[i]

    ]

    inlier_image = cv2.drawMatches(
        processed1,
        kp1,
        processed2,
        kp2,
        inlier_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    inlier_output = os.path.join(
        HOMOGRAPHY_DIR,
        "pipeline_inliers.jpg"
    )

    cv2.imwrite(
        inlier_output,
        inlier_image
    )


    # ========================================================
    # 14. IMAGE ALIGNMENT
    # ========================================================

    height, width = processed2.shape[:2]

    aligned = cv2.warpPerspective(
        processed1,
        H,
        (
            width,
            height
        )
    )

    aligned_output = os.path.join(
        HOMOGRAPHY_DIR,
        "pipeline_aligned.jpg"
    )

    cv2.imwrite(
        aligned_output,
        aligned
    )


    # ========================================================
    # 15. REPROJECTION ERROR
    # ========================================================

    projected = cv2.perspectiveTransform(
        src_pts,
        H
    )

    errors = []

    for i in range(
        len(dst_pts)
    ):

        if mask[i]:

            error = np.linalg.norm(
                projected[i][0]
                -
                dst_pts[i][0]
            )

            errors.append(
                error
            )


    if errors:

        mean_error = float(
            np.mean(errors)
        )

        min_error = float(
            np.min(errors)
        )

        max_error = float(
            np.max(errors)
        )

    else:

        mean_error = 0.0
        min_error = 0.0
        max_error = 0.0


    # ========================================================
    # 16. FINAL RESULT
    # ========================================================

    return {

        "status":
            "success",

        "image1_keypoints":
            len(kp1),

        "image2_keypoints":
            len(kp2),

        "candidate_matches":
            len(matches),

        "good_matches":
            len(good_matches),

        "inliers":
            inliers,

        "outliers":
            outliers,

        "inlier_ratio":
            round(
                inlier_ratio,
                3
            ),

        "mean_reprojection_error":
            round(
                mean_error,
                3
            ),

        "min_reprojection_error":
            round(
                min_error,
                3
            ),

        "max_reprojection_error":
            round(
                max_error,
                3
            ),

        "matches_image":
            match_output,

        "inliers_image":
            inlier_output,

        "aligned_image":
            aligned_output
    }