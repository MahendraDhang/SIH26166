from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import sys
import uuid
import importlib.util


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

# Project root:
# D:\SIH26166
# Render:
# /opt/render/project/src

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ============================================================
# BACKEND UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "Backend",
    "uploads"
)

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# ============================================================
# AI DIRECTORY
# ============================================================

AI_DIR = os.path.join(
    BASE_DIR,
    "AI"
)

if not os.path.exists(AI_DIR):
    raise RuntimeError(
        f"AI directory not found: {AI_DIR}"
    )


# ============================================================
# LOAD AI MAIN.PY
# ============================================================

MAIN_FILE = os.path.join(
    AI_DIR,
    "main.py"
)

if not os.path.exists(MAIN_FILE):
    raise RuntimeError(
        f"AI main.py not found: {MAIN_FILE}"
    )


spec = importlib.util.spec_from_file_location(
    "ai_main",
    MAIN_FILE
)

if spec is None or spec.loader is None:
    raise RuntimeError(
        "Could not load AI main.py"
    )


ai_main = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    ai_main
)


run_pipeline = ai_main.run_pipeline


# ============================================================
# UPLOAD ENDPOINT
# ============================================================

@router.post("/upload")
async def upload_images(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):

    # ========================================================
    # VALIDATE FILE TYPES
    # ========================================================

    allowed_types = {
        "image/jpeg",
        "image/png"
    }

    if image1.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Image 1 must be JPG, JPEG or PNG."
        )

    if image2.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Image 2 must be JPG, JPEG or PNG."
        )


    # ========================================================
    # GENERATE UNIQUE FILE NAMES
    # ========================================================

    file_id = str(
        uuid.uuid4()
    )

    ext1 = os.path.splitext(
        image1.filename or ""
    )[1].lower()

    ext2 = os.path.splitext(
        image2.filename or ""
    )[1].lower()


    if not ext1:
        ext1 = ".jpg"

    if not ext2:
        ext2 = ".jpg"


    image1_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}_image1{ext1}"
    )

    image2_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}_image2{ext2}"
    )


    # ========================================================
    # SAVE IMAGE 1
    # ========================================================

    try:

        image1_data = await image1.read()

        with open(
            image1_path,
            "wb"
        ) as f:

            f.write(
                image1_data
            )


        # ====================================================
        # SAVE IMAGE 2
        # ====================================================

        image2_data = await image2.read()

        with open(
            image2_path,
            "wb"
        ) as f:

            f.write(
                image2_data
            )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded images: {str(e)}"
        )


    # ========================================================
    # RUN AI PIPELINE
    # ========================================================

    try:

        result = run_pipeline(
            image1_path,
            image2_path
        )

    except ValueError as e:

        return {
            "status": "partial",
            "message": str(e),

            "image1_filename":
                image1.filename,

            "image2_filename":
                image2.filename
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"AI pipeline failed: {str(e)}"
        )


    # ========================================================
    # CONVERT RESULT PATHS TO API URLS
    # ========================================================

    def result_url(path):

        if not path:
            return None

        filename = os.path.basename(
            path
        )

        normalized = path.replace(
            "\\",
            "/"
        )


        if "/pipeline_matches/" in normalized:

            return (
                f"/results/"
                f"pipeline_matches/"
                f"{filename}"
            )


        if "/pipeline_homography/" in normalized:

            return (
                f"/results/"
                f"pipeline_homography/"
                f"{filename}"
            )


        if "/pipeline_reports/" in normalized:

            return (
                f"/results/"
                f"pipeline_reports/"
                f"{filename}"
            )


        if "/preprocessed/" in normalized:

            return (
                f"/results/"
                f"preprocessed/"
                f"{filename}"
            )


        return None


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    response = {
        "status":
            result.get(
                "status",
                "success"
            ),

        "message":
            result.get(
                "message",
                "Image analysis completed successfully."
            ),

        "image1_filename":
            image1.filename,

        "image2_filename":
            image2.filename,

        "image1_keypoints":
            result.get(
                "image1_keypoints",
                0
            ),

        "image2_keypoints":
            result.get(
                "image2_keypoints",
                0
            ),

        "candidate_matches":
            result.get(
                "candidate_matches",
                0
            ),

        "good_matches":
            result.get(
                "good_matches",
                0
            ),

        "inliers":
            result.get(
                "inliers",
                0
            ),

        "outliers":
            result.get(
                "outliers",
                0
            ),

        "inlier_ratio":
            result.get(
                "inlier_ratio",
                0.0
            ),

        "mean_reprojection_error":
            result.get(
                "mean_reprojection_error",
                0.0
            ),

        "min_reprojection_error":
            result.get(
                "min_reprojection_error",
                0.0
            ),

        "max_reprojection_error":
            result.get(
                "max_reprojection_error",
                0.0
            ),

        "matches_image":
            result_url(
                result.get(
                    "matches_image"
                )
            ),

        "inliers_image":
            result_url(
                result.get(
                    "inliers_image"
                )
            ),

        "aligned_image":
            result_url(
                result.get(
                    "aligned_image"
                )
            )
    }


    return response