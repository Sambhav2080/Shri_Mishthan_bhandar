import { createContext, useEffect, useState } from "react";
import { ADMIN_EMAILS } from "../config/admin";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  const isAdmin = user && ADMIN_EMAILS.includes(user.email);

  // Load auth state on refresh
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (storedToken) setToken(storedToken);

    if (storedUser && storedUser !== "undefined") {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem("user");
      }
    }
  }, []);

  // LOGIN
  const login = (loginData) => {
    const userObj = { email: loginData.email };

    localStorage.setItem("token", loginData.access_token);
    localStorage.setItem("user", JSON.stringify(userObj));

    setToken(loginData.access_token);
    setUser(userObj);
  };

  // LOGOUT
  const logout = () => {
    localStorage.clear();
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, isAdmin, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
