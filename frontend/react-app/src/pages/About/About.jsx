import "./About.css";

function About() {
  return (
    <main className="about-page">

      {/* ================= HERO ================= */}
      <section className="about-hero">

        <div className="about-tag">
          <span className="about-dot"></span>
          SIH26166 • SPACE TECHNOLOGY
        </div>

        <p className="about-eyebrow">
          CHANDRAYAAN-2 • MULTI-MODAL IMAGE ANALYSIS
        </p>

        <h1>
          Understanding the
          <br />
          <span>Mission & Technology</span>
        </h1>

        <p className="about-intro">
          A computer vision based system designed to identify reliable
          correspondences between Chandrayaan-2 optical images under
          changes in scale, viewing conditions and illumination.
        </p>

      </section>


      {/* ================= PROJECT OBJECTIVE ================= */}
      <section className="about-section objective-section">

        <div className="about-section-heading">

          <span>01</span>

          <div>
            <p className="about-label">PROJECT OBJECTIVE</p>

            <h2>
              Making lunar image correspondence
              <strong> reliable</strong>
            </h2>
          </div>

        </div>

        <div className="objective-card">

          <div className="objective-icon">◎</div>

          <div>
            <h3>Why this system?</h3>

            <p>
              Chandrayaan-2 provides optical observations of the lunar
              surface through multiple instruments. Our system analyses
              these images to find meaningful feature correspondences
              and verify them geometrically.
            </p>
          </div>

        </div>

      </section>


      {/* ================= PROBLEM STATEMENT ================= */}
      <section className="about-section">

        <div className="about-section-heading">

          <span>02</span>

          <div>
            <p className="about-label">SIH PROBLEM STATEMENT</p>

            <h2>
              Multi-Modal, Sun-Angle & Scale
              <strong> Invariant Correspondence</strong>
            </h2>
          </div>

        </div>

        <div className="problem-card">

          <div className="problem-number">
            SIH26166
          </div>

          <p>
            Develop a system for establishing reliable image
            correspondences using Chandrayaan-2 optical images from
            OHRC, TMC and IIRS while handling variations in scale,
            viewing geometry, illumination and imaging conditions.
          </p>

        </div>

      </section>


      {/* ================= DATA ================= */}
      <section className="about-section">

        <div className="about-section-heading">

          <span>03</span>

          <div>
            <p className="about-label">SUPPORTED DATA</p>

            <h2>
              Chandrayaan-2
              <strong> Imaging Payloads</strong>
            </h2>
          </div>

        </div>

        <div className="sensor-grid">

          <div className="sensor-card">
            <div className="sensor-top">
              <span>01</span>
              <b>OHRC</b>
            </div>

            <h3>Orbiter High Resolution Camera</h3>

            <p>
              High-resolution panchromatic optical imagery for detailed
              lunar surface observation.
            </p>
          </div>


          <div className="sensor-card">
            <div className="sensor-top">
              <span>02</span>
              <b>TMC</b>
            </div>

            <h3>Terrain Mapping Camera</h3>

            <p>
              Stereo optical observations supporting terrain mapping
              and lunar surface characterization.
            </p>
          </div>


          <div className="sensor-card">
            <div className="sensor-top">
              <span>03</span>
              <b>IIRS</b>
            </div>

            <h3>Imaging Infrared Spectrometer</h3>

            <p>
              Spectral imaging data useful for studying lunar surface
              composition and mineral characteristics.
            </p>
          </div>

        </div>

      </section>


      {/* ================= TECHNOLOGY ================= */}
      <section className="about-section technology-section">

        <div className="about-section-heading">

          <span>04</span>

          <div>
            <p className="about-label">TECHNOLOGY STACK</p>

            <h2>
              Computer Vision
              <strong> Pipeline</strong>
            </h2>
          </div>

        </div>


        <div className="technology-flow">

          <div className="technology-step">
            <span>01</span>
            <strong>Python</strong>
            <small>Core Processing</small>
          </div>

          <div className="flow-line"></div>

          <div className="technology-step">
            <span>02</span>
            <strong>OpenCV</strong>
            <small>Image Processing</small>
          </div>

          <div className="flow-line"></div>

          <div className="technology-step">
            <span>03</span>
            <strong>SIFT</strong>
            <small>Feature Extraction</small>
          </div>

          <div className="flow-line"></div>

          <div className="technology-step">
            <span>04</span>
            <strong>BFMatcher</strong>
            <small>Feature Matching</small>
          </div>

          <div className="flow-line"></div>

          <div className="technology-step">
            <span>05</span>
            <strong>RANSAC</strong>
            <small>Verification</small>
          </div>

        </div>


        <div className="framework-list">

          <span>React</span>
          <span>FastAPI</span>
          <span>JavaScript</span>
          <span>Homography</span>
          <span>CLAHE</span>

        </div>

      </section>


      {/* ================= METHODOLOGY ================= */}
      <section className="about-section methodology-section">

        <div className="methodology-box">

          <p className="about-label">SYSTEM METHODOLOGY</p>

          <h2>
            From raw imagery to
            <strong> verified correspondence</strong>
          </h2>

          <div className="methodology-flow">

            <span>Images</span>
            <b>→</b>
            <span>Pre-processing</span>
            <b>→</b>
            <span>Feature Extraction</span>
            <b>→</b>
            <span>Matching</span>
            <b>→</b>
            <span>Geometric Verification</span>
            <b>→</b>
            <span>Score & Visualization</span>

          </div>

        </div>

      </section>

    </main>
  );
}

export default About;