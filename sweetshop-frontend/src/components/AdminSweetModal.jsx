import { useState } from "react";

const AdminSweetModal = ({ sweet, onSave, onClose }) => {
  const [form, setForm] = useState(
    sweet || { name: "", price: "", stock: "", image: "" }
  );

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = () => onSave(form);

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h3>{sweet ? "Edit Sweet" : "Add Sweet"}</h3>

        <input name="name" placeholder="Name" value={form.name} onChange={handleChange} />
        <input name="price" placeholder="Price / kg" value={form.price} onChange={handleChange} />
        <input name="stock" placeholder="Stock" value={form.stock} onChange={handleChange} />
        <input name="image" placeholder="Image path (assets/...)" value={form.image} onChange={handleChange} />

        <button onClick={handleSubmit}>Save</button>
        <button onClick={onClose}>Cancel</button>
      </div>
    </div>
  );
};

export default AdminSweetModal;
