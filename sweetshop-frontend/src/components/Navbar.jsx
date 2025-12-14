import { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/navbar.css";

const Navbar = () => {
  const { user, logout, isAdmin } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <h2 className="logo">Shri Mishthan Bhandar</h2>

      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/about">About Us</Link></li>
        <li><Link to="/sweets">Sweets</Link></li>
        <li><Link to="/cart">Cart</Link></li>

        {!user ? (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        ) : (
          <>
            {isAdmin && (
              <li><Link to="/admin/sweets">Admin Panel</Link></li>
            )}

            <li style={{ color: "white" }}>
              Welcome {user.email}
            </li>

            <li>
              <button onClick={logout} className="logout-btn">
                Logout
              </button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;


const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    padding: "12px 20px",
    background: "#222",
    color: "white",
  },
  links: {
    display: "flex",
    gap: "15px",
  },
};
