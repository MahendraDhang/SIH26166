import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadImages } from "../../services/api";
import "./ImageUploader.css";

function ImageUploader() {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Handle image selection
  const handleImage = (file, setImage) => {
    if (!file) return;

    // Validate image type
    const allowedTypes = [
      "image/jpeg",
      "image/png",
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Please select a JPG, JPEG or PNG image.");
      return;
    }

    setImage({
      file: file,
      preview: URL.createObjectURL(file),
    });

    setError("");
  };

  // Analyze images
  const handleAnalyze = async () => {
    if (!image1 || !image2) {
      setError("Please upload both images first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await uploadImages(
        image1.file,
        image2.file
      );

      console.log("Backend Response:", result);

      // Navigate to analysis page
      navigate("/analysis", {
        state: {
          result: result,
          image1: image1.preview,
          image2: image2.preview,
        },
      });

    } catch (err) {
      console.error("Analysis Error:", err);

      setError(
        err.message || "Image analysis failed."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="image-uploader">

      {/* IMAGE 1 */}

      <div className="upload-box">

        <div className="upload-heading">
          <span>IMAGE 01</span>
          <h3>Reference Image</h3>
        </div>

        <label className="drop-area">

          {image1 ? (
            <img
              src={image1.preview}
              alt="Reference"
            />
          ) : (
            <>
              <div className="upload-symbol">
                ↑
              </div>

              <strong>
                Upload Reference Image
              </strong>

              <p>
                JPG, JPEG or PNG
              </p>
            </>
          )}

          <input
            type="file"
            accept="image/jpeg,image/png"
            onChange={(e) =>
              handleImage(
                e.target.files[0],
                setImage1
              )
            }
          />

        </label>

        {image1 && (
          <div className="selected-file">
            ✓ {image1.file.name}
          </div>
        )}

      </div>


      {/*  IMAGE 2  */}

      <div className="upload-box">

        <div className="upload-heading">
          <span>IMAGE 02</span>
          <h3>Target Image</h3>
        </div>

        <label className="drop-area">

          {image2 ? (
            <img
              src={image2.preview}
              alt="Target"
            />
          ) : (
            <>
              <div className="upload-symbol">
                ↑
              </div>

              <strong>
                Upload Target Image
              </strong>

              <p>
                JPG, JPEG or PNG
              </p>
            </>
          )}

          <input
            type="file"
            accept="image/jpeg,image/png"
            onChange={(e) =>
              handleImage(
                e.target.files[0],
                setImage2
              )
            }
          />

        </label>

        {image2 && (
          <div className="selected-file">
            ✓ {image2.file.name}
          </div>
        )}

      </div>


      {/*ERROR */}

      {error && (
        <div className="upload-error">
          ⚠ {error}
        </div>
      )}


      {/* ANALYZE BUTTON  */}

      <button
        className="analyze-button"
        onClick={handleAnalyze}
        disabled={loading}
      >

        {loading ? (
          <>
            Analyzing...
          </>
        ) : (
          <>
            Analyze Images →
          </>
        )}

      </button>

    </div>
  );
}

export default ImageUploader;