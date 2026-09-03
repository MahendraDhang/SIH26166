from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import sys
import uuid


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


# ============================================================
# BASE PATHS
# ============================================================

# Project root:
# D:\SIH26166
# Render par automatically Linux path banega
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ============================================================
# UPLOAD DIRECTORY
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

if AI_DIR not in sys.path:
    sys.path.append(AI_DIR)


from main import run_pipeline


# ============================================================
# UPLOAD + AI ANALYSIS
# ============================================================

@router.post("/upload")
async def upload_images(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):

    image1_path = None
    image2_path = None

    try:

        # ----------------------------------------------------
        # Validate file type
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # Validate filename
        # ----------------------------------------------------

        if not image1.filename:
            raise HTTPException(
                status_code=400,
                detail="Image 1 filename is missing."
            )

        if not image2.filename:
            raise HTTPException(
                status_code=400,
                detail="Image 2 filename is missing."
            )


        # ----------------------------------------------------
        # Save uploaded images
        # ----------------------------------------------------

        image1_name = (
            f"{uuid.uuid4()}_{image1.filename}"
        )

        image2_name = (
            f"{uuid.uuid4()}_{image2.filename}"
        )

        image1_path = os.path.join(
            UPLOAD_DIR,
            image1_name
        )

        image2_path = os.path.join(
            UPLOAD_DIR,
            image2_name
        )


        image1_data = await image1.read()
        image2_data = await image2.read()


        # ----------------------------------------------------
        # Validate empty files
        # ----------------------------------------------------

        if not image1_data:
            raise HTTPException(
                status_code=400,
                detail="Image 1 is empty."
            )

        if not image2_data:
            raise HTTPException(
                status_code=400,
                detail="Image 2 is empty."
            )


        # ----------------------------------------------------
        # Write files
        # ----------------------------------------------------

        with open(
            image1_path,
            "wb"
        ) as file:

            file.write(
                image1_data
            )


        with open(
            image2_path,
            "wb"
        ) as file:

            file.write(
                image2_data
            )


        # ----------------------------------------------------
        # RUN AI PIPELINE
        # ----------------------------------------------------

        try:

            result = run_pipeline(
                image1_path,
                image2_path
            )

        except ValueError as e:

            raise HTTPException(
                status_code=422,
                detail=(
                    f"Image analysis failed: {str(e)}"
                )
            )

        except Exception as e:

            print(
                "AI PIPELINE ERROR:",
                str(e)
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "AI analysis failed. "
                    "Please try different images."
                )
            )


        # ----------------------------------------------------
        # Convert result paths to browser URLs
        # ----------------------------------------------------

        result["matches_image"] = (
            "/results/pipeline_matches/"
            "pipeline_good_matches.jpg"
        )

        result["inliers_image"] = (
            "/results/pipeline_homography/"
            "pipeline_inliers.jpg"
        )

        result["aligned_image"] = (
            "/results/pipeline_homography/"
            "pipeline_aligned.jpg"
        )


        # ----------------------------------------------------
        # Original filenames
        # ----------------------------------------------------

        result["image1"] = (
            image1.filename
        )

        result["image2"] = (
            image2.filename
        )


        # ----------------------------------------------------
        # Analysis message
        # ----------------------------------------------------

        if result.get("status") == "partial":

            result["message"] = (
                result.get(
                    "message",
                    "Feature matching completed "
                    "but geometric verification "
                    "was not successful."
                )
            )

        else:

            result["message"] = (
                "Image correspondence analysis "
                "completed successfully."
            )


        return result


    # ========================================================
    # HTTP ERRORS
    # ========================================================

    except HTTPException:

        raise


    # ========================================================
    # UNEXPECTED ERRORS
    # ========================================================

    except Exception as e:

        print(
            "UPLOAD ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Something went wrong while "
                "processing the images."
            )
        )


    # ========================================================
    # CLEANUP
    # ========================================================

    finally:

        # Uploaded files are currently kept
        # for debugging purposes.

        pass