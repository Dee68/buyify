export default function HomePage() {
  return (
    <main className="min-h-screen">
      <header className="flex items-center justify-between px-8 py-6 bg-white shadow-sm">
        <div className="text-xl font-bold tracking-tight">Buyify</div>
        <nav className="space-x-6 text-sm font-medium">
          <a href="#" className="hover:text-blue-600">Features</a>
          <a href="#" className="hover:text-blue-600">Pricing</a>
          <a href="/login" className="hover:text-blue-600">Login</a>
        </nav>
      </header>

      <section className="flex flex-col items-center justify-center text-center px-6 py-32 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
        <h1 className="text-5xl font-extrabold tracking-tight mb-6">
          Build your online store in minutes
        </h1>
        <p className="text-lg max-w-2xl mb-10 opacity-90">
          Buyify helps you launch, manage, and scale your e-commerce business with ease.
        </p>
        <div className="space-x-4">
          <button className="px-6 py-3 bg-white text-blue-700 font-semibold rounded-lg shadow hover:bg-gray-100">
            Get Started
          </button>
          <button className="px-6 py-3 border border-white text-white font-semibold rounded-lg hover:bg-white/10">
            View Demo
          </button>
        </div>
      </section>

      <section className="px-8 py-24 bg-gray-50">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          <Feature
            title="Fast Setup"
            description="Launch your store in under 10 minutes with guided onboarding."
          />
          <Feature
            title="Secure Payments"
            description="Integrated with Stripe, PayPal, and local payment providers."
          />
          <Feature
            title="Analytics"
            description="Track sales, users, and performance in real time."
          />
        </div>
      </section>
    </main>
  );
}

function Feature({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-8 text-center">
      <h3 className="text-lg font-semibold mb-3">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </div>
  );
}


