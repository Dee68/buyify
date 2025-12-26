export async function fetchProfile() {
  const token = document.cookie
    .split("; ")
    .find(row => row.startsWith("token="))
    ?.split("=")[1];

  const res = await fetch("http://localhost:8000/api/auth/profile/", {
    headers: {
      Authorization: `Token ${token}`,
    },
  });

  if (!res.ok) throw new Error("Not authenticated");

  return res.json();
}
