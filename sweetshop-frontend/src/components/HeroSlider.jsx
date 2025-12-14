import gajjak from "../assets/hero/gajjak.jpeg";
import jalebi from "../assets/hero/jalebi.jpeg";
import mallpua from "../assets/hero/mallpua.jpeg";
import samosa from "../assets/hero/samosa.jpeg";

import { useEffect, useState } from "react";
import "../styles/hero.css";

const images = [
  mallpua, gajjak, jalebi, samosa
];

export default function HeroSlider() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % images.length);
    }, 3500);
    return () => clearInterval(timer);
  }, []);

  return (
    <div
      className="hero"
      style={{ backgroundImage: `url(${images[index]})` }}
    >
      <div className="hero-overlay">
        <h1>Fresh & Authentic Indian Sweets</h1>
        <p>Made with love & tradition</p>
      </div>
    </div>
  );
}
