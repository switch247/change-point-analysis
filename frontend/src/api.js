export async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json();
}
