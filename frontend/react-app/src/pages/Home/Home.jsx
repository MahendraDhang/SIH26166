import ImageUploader from "../../components/ImageUploader/ImageUploader";
import "./Home.css";

function Home() {
  return (
    <main className="home">

      {/* ================= HERO ================= */}
      <section className="home-hero">

        <div className="hero-content">

          <div className="hero-tag">
            <span className="status-dot"></span>
            SIH26166 • SPACE TECHNOLOGY
          </div>

          <p className="hero-eyebrow">
            CHANDRAYAAN-2 • OPTICAL IMAGE ANALYSIS
          </p>

          <h1>
            Multi-Modal
            <br />
            <span>Image Correspondence</span>
          </h1>

          <p className="hero-description">
            A computer vision based system for identifying reliable
            correspondences between Chandrayaan-2 optical images
            under changes in scale, viewing conditions and illumination.
          </p>

          {/* Mission Cards */}
          <div className="mission-info">

            <div className="mission-card">
              <div className="mission-icon">◉</div>
              <div>
                <strong>OHRC</strong>
                <small>Orbiter High Resolution Camera</small>
              </div>
            </div>

            <div className="mission-card">
              <div className="mission-icon">◇</div>
              <div>
                <strong>TMC</strong>
                <small>Terrain Mapping Camera</small>
              </div>
            </div>

            <div className="mission-card">
              <div className="mission-icon">◈</div>
              <div>
                <strong>IIRS</strong>
                <small>Imaging Infrared Spectrometer</small>
              </div>
            </div>

          </div>
        </div>

        {/* Right visual */}
        <div className="space-visual">

          <div className="orbit orbit-one"></div>
          <div className="orbit orbit-two"></div>
          <div className="orbit orbit-three"></div>

          <div className="moon">
            <div className="moon-crater crater-one"></div>
            <div className="moon-crater crater-two"></div>
            <div className="moon-crater crater-three"></div>
            <div className="moon-crater crater-four"></div>
          </div>

          <div className="satellite">
            <span></span>
          </div>

        </div>

      </section>


      {/* ================= ANALYSIS INTRO ================= */}
      <section className="analysis-intro">

        <div className="section-heading">
          <div className="section-number">01</div>

          <div>
            <p className="section-label">CORRESPONDENCE ANALYSIS</p>

            <h2>
              Compare two Chandrayaan-2
              <span> optical images</span>
            </h2>

            <p className="section-description">
              Upload a reference image and a target image to detect
              feature correspondences and geometrically verify the matches.
            </p>
          </div>
        </div>

        {/* Process flow */}
        <div className="process-flow">

          <div className="process-step">
            <span>01</span>
            <strong>Input Images</strong>
            <small>Reference + Target</small>
          </div>

          <div className="process-line"></div>

          <div className="process-step">
            <span>02</span>
            <strong>Feature Extraction</strong>
            <small>SIFT Features</small>
          </div>

          <div className="process-line"></div>

          <div className="process-step">
            <span>03</span>
            <strong>Feature Matching</strong>
            <small>BFMatcher</small>
          </div>

          <div className="process-line"></div>

          <div className="process-step">
            <span>04</span>
            <strong>Verification</strong>
            <small>RANSAC / Homography</small>
          </div>

        </div>

      </section>


      {/* ================= UPLOAD ================= */}
      <section className="upload-section">

        <div className="upload-header">

          <div>
            <p className="section-label">IMAGE INPUT</p>

            <h2>Upload Images</h2>

            <p>
              Select two optical images for correspondence analysis.
            </p>
          </div>

          <div className="supported-format">
            <span>SUPPORTED</span>
            <strong>JPG • JPEG • PNG</strong>
          </div>

        </div>

        <ImageUploader />

      </section>


      {/* ================= TECHNOLOGY ================= */}
      <section className="technology-section">

        <div className="section-heading centered">

          <div className="section-number">02</div>

          <div>
            <p className="section-label">COMPUTER VISION PIPELINE</p>

            <h2>
              Technology behind the
              <span> analysis</span>
            </h2>
          </div>

        </div>

        <div className="technology-grid">

          <div className="technology-card">
            <span className="tech-number">01</span>
            <strong>SIFT</strong>
            <p>Scale-invariant feature detection and description.</p>
          </div>

          <div className="technology-card">
            <span className="tech-number">02</span>
            <strong>BFMatcher</strong>
            <p>Descriptor matching between the input images.</p>
          </div>

          <div className="technology-card">
            <span className="tech-number">03</span>
            <strong>RANSAC</strong>
            <p>Geometric verification of reliable correspondences.</p>
          </div>

          <div className="technology-card">
            <span className="tech-number">04</span>
            <strong>Homography</strong>
            <p>Image alignment and correspondence visualization.</p>
          </div>

        </div>

      </section>

    </main>
  );
}

export default Home;