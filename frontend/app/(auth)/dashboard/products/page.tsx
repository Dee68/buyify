"use client";

import { useEffect, useState } from "react";
import { useAuth } from "../../../context/AuthContext";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";


type Product = {
  id: number;
  name: string;
  price: string;
  stock: number;
};

export default function ProductsPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  
 useEffect(() => {
  async function load() {
    const res = await apiFetch("/products/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`,
      },
    });
    try {
    const data = await res.json();

    // Handle paginated and non-paginated responses
    if (Array.isArray(data)) {
      setProducts(data);
    } else if (Array.isArray(data.results)) {
      setProducts(data.results);
    } else {
      console.error("Unexpected products response:", data);
      setProducts([]);
    }
    } catch{
        alert("Session expired. Please login again.");
        router.replace("/login");
    }
    setLoading(false);
  }

  load();
}, []);


  if (!user) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
  <h1 className="text-2xl font-semibold">Products</h1>
  <Link
    href="/dashboard/products/new"
    className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
  >
    + New Product
  </Link>
</div>


      <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-4 py-3 text-left font-medium text-gray-600">Name</th>
              <th className="px-4 py-3 text-left font-medium text-gray-600">Price</th>
              <th className="px-4 py-3 text-left font-medium text-gray-600">Stock</th>
              <th className="px-4 py-3 text-right font-medium text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={4} className="px-4 py-6 text-center text-gray-500">
                  Loading products…
                </td>
              </tr>
            ) : products.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-6 text-center text-gray-500">
                  No products yet.
                </td>
              </tr>
            ) : (
              products.map((p) => (
                <tr key={p.id} className="border-b last:border-0">
                  <td className="px-4 py-3">{p.name}</td>
                  <td className="px-4 py-3">${p.price}</td>
                  <td className="px-4 py-3">{p.stock ?? "-"}</td>
                  <td className="px-4 py-3 text-right">
                    <button className="text-blue-600 hover:underline text-sm">
                      Edit
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
