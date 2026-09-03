import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">

      <NavLink to="/" className="navbar-logo">
        <span className="satellite-icon">🛰️</span>

        <div>
          <h2>Chandrayaan-2</h2>
          <p>Image Correspondence</p>
        </div>
      </NavLink>

      <div className="navbar-links">

        <NavLink to="/">Home</NavLink>

        <NavLink to="/analysis">Analysis</NavLink>

        <NavLink to="/about">About</NavLink>

      </div>

      <div className="system-status">
        <span className="status-dot"></span>
        System Ready
      </div>

    </nav>
  );
}

export default Navbar;