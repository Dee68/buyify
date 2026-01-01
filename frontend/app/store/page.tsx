"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import ProductCard from "@/components/ProductCard";
import { logout } from "@/lib/auth";
import router from "next/router";

export default function StorePage() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const res = await apiFetch("/products/");
      const data = await res.json();
      setProducts(data.results || data);
      setLoading(false);
      if (!res) {
        logout();
        router.replace("/login");
        return;
      }
    }
    load();
  }, []);

  if (loading) return <div className="p-8">Loading products...</div>;

  return (
    <div className="max-w-7xl mx-auto px-8 py-12">
      <h1 className="text-3xl font-semibold mb-8">Store</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}
