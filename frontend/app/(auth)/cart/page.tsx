"use client";

import { useCart } from "../../context/CartContext";

export default function CartPage() {
  const { cart, removeFromCart } = useCart();

  if (!cart) return <p>Your cart is empty.</p>

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-semibold mb-6">Your Cart</h1>

      {cart.items.map((item: any) => (
        <div key={item.id} className="flex justify-between border-b py-4">
          <div>
            {item.product.name} × {item.quantity}
          </div>
          <button
            onClick={() => removeFromCart(item.product.id)}
            className="text-red-600"
          >
            Remove
          </button>
        </div>
      ))}
    </div>
  );
}
