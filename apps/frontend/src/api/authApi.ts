import { apiFetch } from "./client";

export type AuthMe = {
  authenticated: boolean;
  display_name?: string | null;
  customer_name?: string | null;
  expires_at?: string | null;
  max_devices?: number | null;
  devices_used?: number | null;
};

export async function loginWithCode(payload: {
  code: string;
  display_name?: string;
  device_name?: string;
}) {
  return apiFetch<AuthMe>("/api/v1/auth/login-with-code", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getAuthMe() {
  return apiFetch<AuthMe>("/api/v1/auth/me");
}

export async function logoutAuth() {
  return apiFetch<{ ok: boolean }>("/api/v1/auth/logout", {
    method: "POST",
  });
}