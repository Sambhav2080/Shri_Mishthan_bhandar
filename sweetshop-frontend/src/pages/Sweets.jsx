import { useEffect, useState } from "react";
import { addToCart } from "../services/cartService";
import { fetchProducts } from "../services/productservice";

export default function Sweets() {
  const [sweets, setSweets] = useState([]);

  useEffect(() => {
    fetchProducts().then(setSweets);
  }, []);

  const handleAdd = async (id) => {
    const token = localStorage.getItem("token");
    await addToCart(id, 1, token);
    alert("Added to cart");
  };

  return (
    <div className="sweets-section">
      <h2>Available Sweets</h2>

      <div className="sweets-grid">
        {sweets.map((s) => (
          <div key={s.id} className="sweet-card">
            <h3>{s.name}</h3>
            <p>₹ {s.price}</p>
            <p>Stock: {s.stock}</p>
            <button onClick={() => handleAdd(s.id)}>Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
}
