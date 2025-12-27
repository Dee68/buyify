"use client";

import { ReactNode,useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth, AuthProvider } from "../../context/AuthContext";

export default function DashboardLayoutWrapper({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <DashboardLayout>{children}</DashboardLayout>
    </AuthProvider>
  );
}

function DashboardLayout({ children }: { children: ReactNode }) {
  const { user, logout, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user === null) {
      router.replace("/login");
    }
  }, [user, loading, router]);

  if (loading || user === null) {
    return (
      <div className="flex items-center justify-center h-screen w-screen">
        Loading...
      </div>
    );
  }
  function handleLogout() {
    logout();
    router.push("/");
  }

  return (
    <div className="fixed inset-0 flex bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r">
        <div className="px-6 py-6 text-xl font-bold">Buyify</div>
        <nav className="flex flex-col gap-1 px-4 text-sm">
          <NavLink href="/dashboard">Overview</NavLink>
          <NavLink href="/dashboard/categories">Categories</NavLink>
          <NavLink href="/dashboard/products">Products</NavLink>
          <NavLink href="/dashboard/orders">Orders</NavLink>
          <NavLink href="/dashboard/customers">Customers</NavLink>
          <NavLink href="/dashboard/settings">Settings</NavLink>
        </nav>
      </aside>

      {/* Main area */}
      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b bg-white px-8 py-4">
          <div className="text-sm text-gray-600">
            Welcome back, <span className="font-medium">{user?.email}</span>
          </div>
          <button
            onClick={handleLogout}
            className="text-sm text-red-600 hover:underline"
          >
            Logout
          </button>
        </header>

        <main className="flex-1 p-8">{children}</main>
      </div>
    </div>
  );
}

function NavLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <Link
      href={href}
      className="rounded-lg px-3 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition"
    >
      {children}
    </Link>
  );
}
