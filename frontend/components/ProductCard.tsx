"use client";

import { useCart } from "../app/context/CartContext";

export default function ProductCard({ product }: { product: any }) {
  const { addToCart } = useCart();

  return (
    <div className="rounded-xl border bg-white shadow-sm hover:shadow transition">
      <div className="p-4 space-y-2">
        <h3 className="font-medium text-lg">{product.name}</h3>

        <div className="text-sm text-gray-500">
          {product.category_detail?.name || "Uncategorized"}
        </div>

        <div className="text-xl font-semibold">
          ${product.price}
        </div>

        {product.is_available ? (
          <button
            onClick={() => addToCart(product.id)}
            className="mt-3 w-full rounded-lg bg-blue-600 px-3 py-2 text-white hover:bg-blue-700"
          >
            Add to cart
          </button>
        ) : (
          <div className="mt-3 text-sm text-red-500">Out of stock</div>
        )}
      </div>
    </div>
  );
}
