const API = "http://localhost:8000/api";

async function refreshToken() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return null;

  const res = await fetch(`${API}/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (!res.ok) {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    return null;
  }

  const data = await res.json();
  localStorage.setItem("access", data.access);
  return data.access;
}

export async function apiFetch(url: string, options: RequestInit = {}) {
  let access = localStorage.getItem("access");

  const res = await fetch(`${API}${url}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: access ? `Bearer ${access}` : "",
      "Content-Type": "application/json",
    },
  });

  if (res.status !== 401) return res;

  // Try refresh once
  const newAccess = await refreshToken();
  if (!newAccess) {
    return null;
  }//throw new Error("Session expired");

  return fetch(`${API}${url}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${newAccess}`,
      "Content-Type": "application/json",
    },
  });
}
