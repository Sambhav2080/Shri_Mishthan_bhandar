import "../styles/sweets.css";

export default function SweetCard({ image, name, price }) {
  return (
    <div className="sweet-card">
      <img src={image} alt={name} />
      <h3>{name}</h3>
      <p>₹ {price}</p>
      <button>Add to Cart</button>
    </div>
  );
}
