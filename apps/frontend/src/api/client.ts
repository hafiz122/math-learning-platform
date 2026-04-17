const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request<T>(
  path: string,
  init: globalThis.RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Request failed");
  }

  return response.json() as Promise<T>;
}

export const apiRequest = request;
export const apiFetch = request;