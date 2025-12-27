"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Category = {
  id: number;
  name: string;
};

export default function NewCategoryPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [parentId, setParentId] = useState<string>("");
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      const res = await apiFetch("/categories/");
      const data = await res.json();
      setCategories(data.results || data);
    }
    load();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    const payload: any = { name };
    if (parentId) payload.parent = Number(parentId);

    const res = await apiFetch("/categories/", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      router.push("/dashboard/categories");
    } else {
      const err = await res.json();
      alert(JSON.stringify(err));
    }

    setLoading(false);
  }

  return (
    <div className="max-w-md space-y-6">
      <h1 className="text-2xl font-semibold">New Category</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Parent */}
        <div>
          <label className="block text-sm font-medium">Parent Category</label>
          <select
            value={parentId}
            onChange={(e) => setParentId(e.target.value)}
            className="mt-1 block w-full rounded-lg border px-3 py-2 text-sm"
          >
            <option value="">None (Top-level)</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        {/* Name */}
        <div>
          <label className="block text-sm font-medium">Name</label>
          <input
            className="mt-1 w-full rounded-lg border px-3 py-2"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <button
          disabled={loading}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Saving..." : "Create Category"}
        </button>
      </form>
    </div>
  );
}
