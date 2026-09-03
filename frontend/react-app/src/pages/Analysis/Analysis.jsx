import { useLocation } from "react-router-dom";

import ResultCards from "../../components/ResultCards/ResultCards";
import Visualization from "../../components/Visualization/Visualization";

import "./Analysis.css";

function Analysis() {
  const location = useLocation();

  const result = location.state?.result || null;
  const image1 = location.state?.image1 || null;
  const image2 = location.state?.image2 || null;

  return (
    <main className="analysis-page">

      {/* ================= HEADER ================= */}
      <section className="analysis-header">

        <div className="analysis-header-content">

          <div className="analysis-tag">
            <span className="analysis-dot"></span>
            SIH26166 • CORRESPONDENCE ANALYSIS
          </div>

          <p className="analysis-eyebrow">
            CHANDRAYAAN-2 • COMPUTER VISION PIPELINE
          </p>

          <h1>
            Correspondence
            <span> Analysis</span>
          </h1>

          <p className="analysis-description">
            Feature matching, geometric verification and image alignment
            results for Chandrayaan-2 optical imagery.
          </p>

        </div>

        <div className={`analysis-status ${result ? "complete" : ""}`}>
          <span></span>
          {result ? "Analysis Complete" : "Waiting for Analysis"}
        </div>

      </section>


      {/* ================= PIPELINE ================= */}
      <section className="pipeline-overview">

        <div className="pipeline-card active">
          <span>01</span>
          <strong>Input Images</strong>
          <small>Reference + Target</small>
        </div>

        <div className="pipeline-connector"></div>

        <div className="pipeline-card">
          <span>02</span>
          <strong>Feature Matching</strong>
          <small>SIFT + BFMatcher</small>
        </div>

        <div className="pipeline-connector"></div>

        <div className="pipeline-card">
          <span>03</span>
          <strong>Geometric Verification</strong>
          <small>RANSAC / Homography</small>
        </div>

        <div className="pipeline-connector"></div>

        <div className="pipeline-card">
          <span>04</span>
          <strong>Visual Result</strong>
          <small>Verified Correspondence</small>
        </div>

      </section>


      {/* ================= RESULTS ================= */}
      <section className="results-container">

        {/* Performance Metrics */}
        <div className="results-title">

          <div className="results-number">01</div>

          <div>
            <p className="results-label">
              PERFORMANCE METRICS
            </p>

            <h2>
              Correspondence <span>Performance</span>
            </h2>

            <p className="results-description">
              Quantitative evaluation of detected image correspondences
              and geometric consistency.
            </p>
          </div>

        </div>

        <div className="results-wrapper">
          <ResultCards result={result} />
        </div>


        {/* Visualization */}
        <div className="results-title visualization-title">

          <div className="results-number">02</div>

          <div>
            <p className="results-label">
              CORRESPONDENCE VISUALIZATION
            </p>

            <h2>
              Feature Match <span>Visualization</span>
            </h2>

            <p className="results-description">
              Visual representation of candidate matches, verified
              correspondences and image alignment.
            </p>
          </div>

        </div>

        <div className="visualization-wrapper">
          <Visualization
            result={result}
            image1={image1}
            image2={image2}
          />
        </div>


        {/* Technical Information */}
        <section className="technical-section">

          <div className="technical-header">
            <p className="results-label">
              03 • TECHNICAL PIPELINE
            </p>

            <h2>
              Analysis <span>Methodology</span>
            </h2>
          </div>

          <div className="technical-grid">

            <div className="technical-card">
              <span>01</span>
              <strong>Pre-processing</strong>
              <p>
                Contrast enhancement using CLAHE before feature extraction.
              </p>
            </div>

            <div className="technical-card">
              <span>02</span>
              <strong>Feature Extraction</strong>
              <p>
                SIFT detects scale-invariant keypoints and generates descriptors.
              </p>
            </div>

            <div className="technical-card">
              <span>03</span>
              <strong>Feature Matching</strong>
              <p>
                BFMatcher compares descriptors using distance-based matching.
              </p>
            </div>

            <div className="technical-card">
              <span>04</span>
              <strong>Geometric Verification</strong>
              <p>
                RANSAC and homography identify geometrically consistent matches.
              </p>
            </div>

          </div>

        </section>

      </section>

    </main>
  );
}

export default Analysis;