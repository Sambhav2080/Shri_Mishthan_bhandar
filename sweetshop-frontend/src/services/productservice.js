import baseURL from ".\api";
import axios from "axios";

export const fetchProducts = async () => {
  const res = await axios.get(`${baseURL}/sweets`);
  return res.data;
};

export const purchaseProduct = async (id, amount, token) => {
  return axios.post(
    `${baseURL}/sweets/${id}/purchase`,
    { amount },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};
