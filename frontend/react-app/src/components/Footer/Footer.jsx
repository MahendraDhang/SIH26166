import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-left">
        <div className="footer-logo">
          🛰️ <span>SIH26166</span>
        </div>

        <p>
          Multi-Modal Image Correspondence using Chandrayaan-2
          Optical Images
        </p>
      </div>

      <div className="footer-center">
        <span>OHRC</span>
        <span>TMC</span>
        <span>IIRS</span>
      </div>

      <div className="footer-right">
        <p>Space Technology</p>
        <p>© 2026 SIH26166</p>
      </div>
    </footer>
  );
}

export default Footer;