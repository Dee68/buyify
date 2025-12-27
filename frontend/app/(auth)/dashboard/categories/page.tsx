"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Category = {
  id: number;
  name: string;
};

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    const res = await apiFetch("/categories/");
    const data = await res.json();
    setCategories(data.results || data);
    setLoading(false);
  }

  async function remove(id: number) {
    if (!confirm("Delete this category?")) return;
    await apiFetch(`/categories/${id}/`, { method: "DELETE" });
    load();
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Categories</h1>
        <Link
          href="/dashboard/categories/new"
          className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 text-sm"
        >
          New Category
        </Link>
      </div>

      <div className="rounded-xl border bg-white">
        {loading ? (
          <p className="p-6 text-gray-500 text-sm">Loading...</p>
        ) : categories.length === 0 ? (
          <p className="p-6 text-gray-500 text-sm">No categories yet.</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left">Name</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((c) => (
                <tr key={c.id} className="border-b last:border-0">
                  <td className="px-4 py-3">{c.name}</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => remove(c.id)}
                      className="text-red-600 hover:underline text-xs"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
