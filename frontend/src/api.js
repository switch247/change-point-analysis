const rawBaseUrl = import.meta.env.VITE_API_BASE || "http://localhost:4000";
const baseUrl = rawBaseUrl.replace(/\/$/, "");

export async function fetchJson(path) {
  const url = path.startsWith("http") ? path : `${baseUrl}${path}`;
  const response = await fetch(url);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json();
}
