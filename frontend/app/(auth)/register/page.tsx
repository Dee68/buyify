"use client";

import { useState } from "react";
import { register } from "@/lib/auth";

export default function RegisterPage() {
  const [form, setForm] = useState({ email: "", password: "", password2: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      await register(form);
      setSuccess("Account created successfully. You can now log in.");
      setForm({ email: "", password: "", password2: "" });
    } catch (err: any) {
      setError(JSON.stringify(err));
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 p-6 border rounded">
      <h1 className="text-2xl mb-4">Register</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })}
          className="w-full p-2 border rounded"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })}
          className="w-full p-2 border rounded"
          required
        />

        <input
          type="password"
          placeholder="Confirm Password"
          value={form.password2}
          onChange={e => setForm({ ...form, password2: e.target.value })}
          className="w-full p-2 border rounded"
          required
        />

        <button className="w-full bg-black text-white p-2 rounded">
          Register
        </button>
      </form>

      {error && <p className="text-red-600 mt-4">{error}</p>}
      {success && <p className="text-green-600 mt-4">{success}</p>}
    </div>
  );
}
