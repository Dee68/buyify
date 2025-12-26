"use client";

import { useAuth } from "../../context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function ProfilePage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) router.push("/login");
  }, [loading, user]);

  if (loading) return <p className="p-8">Loading...</p>;
  if (!user) return null;

  return (
    <div className="max-w-md mx-auto mt-20 space-y-4">
      <h1 className="text-xl font-bold">Profile</h1>
      <p>Email: {user.email}</p>
      <button onClick={logout} className="bg-red-600 text-white px-4 py-2 rounded">
        Logout
      </button>
    </div>
  );
}
