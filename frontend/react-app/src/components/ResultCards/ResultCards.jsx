import "./ResultCards.css";

function ResultCards({ result }) {
  const inlierRatio = result?.inlier_ratio ?? null;

  let matchQuality = "--";
  let qualityMessage = "Waiting for analysis";

  if (inlierRatio !== null) {
    if (inlierRatio >= 0.7) {
      matchQuality = "HIGH";
      qualityMessage = "Strong correspondence detected";
    } else if (inlierRatio >= 0.4) {
      matchQuality = "MEDIUM";
      qualityMessage = "Moderate correspondence detected";
    } else {
      matchQuality = "LOW";
      qualityMessage = "Limited reliable correspondence";
    }
  }

  const confidence =
    inlierRatio !== null
      ? `${(inlierRatio * 100).toFixed(0)}%`
      : "--";

  const metrics = [
    {
      label: "IMAGE 1 KEYPOINTS",
      value: result?.image1_keypoints ?? "--",
      description: "SIFT features",
    },
    {
      label: "IMAGE 2 KEYPOINTS",
      value: result?.image2_keypoints ?? "--",
      description: "SIFT features",
    },
    {
      label: "GOOD MATCHES",
      value: result?.good_matches ?? "--",
      description: "Lowe ratio test",
    },
    {
      label: "INLIERS",
      value: result?.inliers ?? "--",
      description: "RANSAC verified",
    },
    {
      label: "OUTLIERS",
      value: result?.outliers ?? "--",
      description: "Rejected matches",
    },
    {
      label: "INLIER RATIO",
      value:
        result?.inlier_ratio !== undefined
          ? `${(result.inlier_ratio * 100).toFixed(0)}%`
          : "--",
      description: "Geometric consistency",
    },
    {
      label: "MEAN ERROR",
      value:
        result?.mean_reprojection_error !== undefined
          ? Number(result.mean_reprojection_error).toFixed(3)
          : "--",
      description: "Reprojection error (px)",
    },
    {
      label: "MAX ERROR",
      value:
        result?.max_reprojection_error !== undefined
          ? Number(result.max_reprojection_error).toFixed(3)
          : "--",
      description: "Reprojection error (px)",
    },
  ];

  return (
    <div className="result-cards">

      {/* MATCH QUALITY */}
      <div className="match-quality-card">

        <div className="quality-left">
          <span>MATCH QUALITY</span>
          <strong className={`quality-${matchQuality.toLowerCase()}`}>
  {matchQuality}
</strong>
          <small>{qualityMessage}</small>
        </div>

        <div className="confidence-box">
          <span>CONFIDENCE</span>
          <strong>{confidence}</strong>
        </div>

      </div>

      {/* PERFORMANCE METRICS */}
      {metrics.map((metric) => (
        <div className="result-card" key={metric.label}>

          <span>{metric.label}</span>

          <strong>{metric.value}</strong>

          <small>{metric.description}</small>

        </div>
      ))}

    </div>
  );
}

export default ResultCards;