import { apiFetch } from "./api";

export function register(data: {
  email: string;
  password: string;
  password2: string;
}) {
  return apiFetch("/api/auth/register/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function login(data: { email: string; password: string }) {
  const res = await apiFetch("/api/auth/login/", {
    method: "POST",
    body: JSON.stringify(data),
  });

  document.cookie = `token=${res.token}; path=/; SameSite=Lax`;
  return res;
}

export function logout() {
  document.cookie = "token=; path=/; Max-Age=0";
}

// export function handleSessionExpired() {
//   console.warn("Session expired — logging out");

//   localStorage.removeItem("access");
//   localStorage.removeItem("refresh");

//   window.location.href = "/login";
// }
