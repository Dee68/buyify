"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

const CartContext = createContext<any>(null);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cart, setCart] = useState(null);

  async function loadCart() {
    const res = await apiFetch("/cart/");
    if (!res) return;
    if (res.ok) {
      setCart(await res.json());
    }
  }

  async function addToCart(productId: number) {
    await apiFetch("/cart/add/", {
      method: "POST",
      body: JSON.stringify({ product_id: productId }),
    });
    loadCart();
  }

  async function removeFromCart(productId: number) {
    await apiFetch("/cart/remove/", {
      method: "POST",
      body: JSON.stringify({ product_id: productId }),
    });
    loadCart();
  }

  useEffect(() => {
    loadCart();
  }, []);

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
}

//export const useCart = () => useContext(CartContext);
export const useCart = () => {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used inside CartProvider");
  return ctx;
};
