const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request<T>(
  path: string,
  init: globalThis.RequestInit = {},
): Promise<T> {
  const headers = new Headers(init.headers ?? {});

  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    ...init,
    headers,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Request failed");
  }

  return response.json() as Promise<T>;
}

export const apiRequest = request;
export const apiFetch = request;