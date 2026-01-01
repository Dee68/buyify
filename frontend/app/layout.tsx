import "../app/globals.css"
import { AuthProvider } from "./context/AuthContext";
// import { CartProvider } from "./context/CartContext";
// import Navbar from "@/components/Navbar";

export const metadata = {
  title: "Buyify",
  description: "Modern e-commerce platform",
};



export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900">
        <AuthProvider>
         
        {children}
  
        </AuthProvider>
      </body>
    </html>
  );
}

