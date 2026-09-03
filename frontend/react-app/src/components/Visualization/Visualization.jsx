import "./Visualization.css";

const API_URL = "http://127.0.0.1:8000";

function Visualization({ result, image1, image2 }) {
  const matchesImage = result?.matches_image
    ? `${API_URL}/results/pipeline_matches/pipeline_good_matches.jpg`
    : null;

  const inliersImage = result?.inliers_image
    ? `${API_URL}/results/pipeline_homography/pipeline_inliers.jpg`
    : null;

  const alignedImage = result?.aligned_image
    ? `${API_URL}/results/pipeline_homography/pipeline_aligned.jpg`
    : null;

  return (
    <section className="visualization-section">

      {/* INPUT IMAGES */}
      <div className="visualization-block">
        <div className="visualization-heading">
          <span>01</span>
          <div>
            <h3>Input Images</h3>
            <p>Uploaded Chandrayaan-2 optical images</p>
          </div>
        </div>

        <div className="input-images-grid">

          <div className="image-card">
            <div className="image-card-header">
              <span>IMAGE 1</span>
            </div>

            {image1 ? (
              <img
                src={image1}
                alt="Input Image 1"
                className="visualization-image"
              />
            ) : (
              <div className="image-placeholder">
                No Image Available
              </div>
            )}
          </div>

          <div className="image-card">
            <div className="image-card-header">
              <span>IMAGE 2</span>
            </div>

            {image2 ? (
              <img
                src={image2}
                alt="Input Image 2"
                className="visualization-image"
              />
            ) : (
              <div className="image-placeholder">
                No Image Available
              </div>
            )}
          </div>

        </div>
      </div>


      {/* FEATURE MATCHING */}
      <div className="visualization-block">

        <div className="visualization-heading">
          <span>02</span>
          <div>
            <h3>Feature Matching</h3>
            <p>SIFT features matched using BFMatcher</p>
          </div>
        </div>

        <div className="result-image-card">

          {matchesImage ? (
            <img
              src={matchesImage}
              alt="Feature Matching Result"
              className="large-result-image"
            />
          ) : (
            <div className="image-placeholder">
              Matching result unavailable
            </div>
          )}

          <div className="result-info">

            <div>
              <span>METHOD</span>
              <strong>SIFT + BFMatcher</strong>
            </div>

            <div>
              <span>CANDIDATE MATCHES</span>
              <strong>{result?.candidate_matches ?? "--"}</strong>
            </div>

            <div>
              <span>GOOD MATCHES</span>
              <strong>{result?.good_matches ?? "--"}</strong>
            </div>

          </div>
        </div>
      </div>


      {/* RANSAC */}
      <div className="visualization-block">

        <div className="visualization-heading">
          <span>03</span>
          <div>
            <h3>Geometric Verification</h3>
            <p>RANSAC-based homography verification</p>
          </div>
        </div>

        <div className="result-image-card">

          {inliersImage ? (
            <img
              src={inliersImage}
              alt="RANSAC Inlier Matches"
              className="large-result-image"
            />
          ) : (
            <div className="image-placeholder">
              RANSAC result unavailable
            </div>
          )}

          <div className="result-info">

            <div>
              <span>VERIFICATION</span>
              <strong>RANSAC</strong>
            </div>

            <div>
              <span>INLIERS</span>
              <strong>{result?.inliers ?? "--"}</strong>
            </div>

            <div>
              <span>OUTLIERS</span>
              <strong>{result?.outliers ?? "--"}</strong>
            </div>

            <div>
              <span>INLIER RATIO</span>
              <strong>
                {result?.inlier_ratio != null
                  ? `${Math.round(result.inlier_ratio * 100)}%`
                  : "--"}
              </strong>
            </div>

          </div>
        </div>
      </div>


      {/* ALIGNED IMAGE */}
      <div className="visualization-block">

        <div className="visualization-heading">
          <span>04</span>
          <div>
            <h3>Image Alignment</h3>
            <p>Homography transformation result</p>
          </div>
        </div>

        <div className="result-image-card">

          {alignedImage ? (
            <img
              src={alignedImage}
              alt="Aligned Image"
              className="large-result-image"
            />
          ) : (
            <div className="image-placeholder">
              Aligned image unavailable
            </div>
          )}

          <div className="alignment-status">
            <span className="status-dot"></span>
            <div>
              <strong>Homography Computed</strong>
              <p>
                {result?.inliers
                  ? `${result.inliers} verified correspondence points`
                  : "Verification unavailable"}
              </p>
            </div>
          </div>

        </div>
      </div>


      {/* TECHNICAL SUMMARY */}
      <div className="technical-summary">

        <div className="summary-title">
          <span>TECHNICAL SUMMARY</span>
        </div>

        <div className="summary-grid">

          <div>
            <span>FEATURE DETECTOR</span>
            <strong>SIFT</strong>
          </div>

          <div>
            <span>MATCHER</span>
            <strong>BFMatcher</strong>
          </div>

          <div>
            <span>VERIFICATION</span>
            <strong>RANSAC</strong>
          </div>

          <div>
            <span>TRANSFORMATION</span>
            <strong>Homography</strong>
          </div>

          <div>
            <span>MEAN ERROR</span>
            <strong>
              {result?.mean_reprojection_error ?? "--"} px
            </strong>
          </div>

          <div>
            <span>MAX ERROR</span>
            <strong>
              {result?.max_reprojection_error ?? "--"} px
            </strong>
          </div>

        </div>
      </div>

    </section>
  );
}

export default Visualization;