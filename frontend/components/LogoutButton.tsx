"use client";

import { logout } from "@/lib/auth";

export default function LogoutButton() {
  return (
    <button
      onClick={() => {
        logout();
        window.location.href = "/";
      }}
      className="text-sm text-red-600"
    >
      Logout
    </button>
  );
}
