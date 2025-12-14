
import barfi from "../assets/sweets/barfi.jpeg";
import gulabjamun from "../assets/sweets/gulabjamun.jpeg";
import laddu from "../assets/sweets/laddu.jpeg";
import HeroSlider from "../components/HeroSlider";
import SweetCard from "../components/SweetCard";
import "../styles/sweets.css";

export default function Home() {
  return (
    <>
      <HeroSlider />

      <section className="sweets-section">
        <h2>Our Popular Sweets</h2>

        <div className="sweets-grid">
          <SweetCard image={laddu} name="Motichoor Laddu" price={300} />
          <SweetCard image={barfi} name="Milk Barfi" price={420} />
          <SweetCard image={gulabjamun} name="Gulab JAmun" price={300} />
      </div>
      </section>
    </>
  );
}
