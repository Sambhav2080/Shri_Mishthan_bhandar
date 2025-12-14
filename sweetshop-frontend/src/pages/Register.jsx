import { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../services/authService";

const Register = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await authService.register(form);
      setSuccess(true);
    } catch (err) {
  if (err.response?.data?.detail) {
    setError(
      typeof err.response.data.detail === "string"
        ? err.response.data.detail
        : "Invalid input. Please check details."
    );
  }
    else {
        setError("Registration failed. Try again.");
      }
    }
  };

  return (
    <div style={styles.container}>
      <h2>Register</h2>

      {!success ? (
        <form onSubmit={handleRegister} style={styles.form}>
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={form.name}
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />

          <button type="submit">Register</button>

          {error && <p style={styles.error}>{error}</p>}
        </form>
      ) : (
        <div style={styles.successBox}>
          <p style={styles.success}>Registered successfully 🎉</p>
          <button onClick={() => navigate("/login")}>
            Go to Login Page
          </button>
        </div>
      )}
    </div>
  );
};

export default Register;

/* ---------- Minimal Inline Styles ---------- */

const styles = {
  container: {
    maxWidth: "400px",
    margin: "60px auto",
    padding: "20px",
    textAlign: "center",
    border: "1px solid #ddd",
    borderRadius: "8px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  error: {
    color: "red",
    fontSize: "14px",
  },
  successBox: {
    marginTop: "20px",
  },
  success: {
    color: "green",
    fontSize: "16px",
    marginBottom: "12px",
  },
};
