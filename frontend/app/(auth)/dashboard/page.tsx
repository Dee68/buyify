"use client";

import { useAuth } from "../../context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();

  // user is guaranteed to exist, because layout handles redirect
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        <p className="text-gray-600 text-sm">
          Overview of your store performance.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard title="Revenue" value="$12,450" delta="+12%" />
        <StatCard title="Orders" value="248" delta="+8%" />
        <StatCard title="Customers" value="1,024" delta="+5%" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Panel title="Recent Orders">
          <p className="text-sm text-gray-500">No recent orders yet.</p>
        </Panel>
        <Panel title="Top Products">
          <p className="text-sm text-gray-500">No products sold yet.</p>
        </Panel>
      </div>
    </div>
  );
}

function StatCard({ title, value, delta }: { title: string; value: string; delta: string }) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <div className="text-sm text-gray-500">{title}</div>
      <div className="mt-2 text-2xl font-semibold">{value}</div>
      <div className="mt-1 text-xs text-green-600">{delta} this month</div>
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <h3 className="text-sm font-medium mb-4">{title}</h3>
      {children}
    </div>
  );
}

