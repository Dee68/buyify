"use client";
import { useAuth } from "../app/context/AuthContext";
import Link from "next/link";

export default function HomePage() {
  const { user, loading, logout } = useAuth();

  if (loading) return null;
  return (
      <header className="flex items-center justify-between px-8 py-6 bg-white shadow-sm">
        <div className="text-xl font-bold tracking-tight">Buyify</div>

        <nav className="space-x-6 text-sm font-medium">
          <Link href="#" className="hover:text-blue-600">Features</Link>
          <Link href="#" className="hover:text-blue-600">Pricing</Link>

          {!user ? (
          <>
            <Link href="/login">Login</Link>
            <Link href="/register">Register</Link>
          </>
        ) : (
          <>
            <Link href="/dashboard" >Dashboard</Link>
            <Link href="/profile">Profile</Link>
            <button onClick={logout} className="text-red-600">
              Logout
            </button>
          </>
        )}
        </nav>
      </header>
  );
}