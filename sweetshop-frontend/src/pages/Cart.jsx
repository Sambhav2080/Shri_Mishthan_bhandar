import { checkoutCart } from "../services/cartService";

export default function Cart() {
  const handleCheckout = async () => {
    const token = localStorage.getItem("token");
    const res = await checkoutCart(token);
    alert(res.data.message);
  };

  return (
    <div style={{ padding: "50px" }}>
      <h2>Your Cart</h2>
      <button onClick={handleCheckout}>
        Checkout (Cash on Delivery)
      </button>
    </div>
  );
}
