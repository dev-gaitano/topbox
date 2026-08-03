const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USERNAME_KEY = "username";

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

function readJwtPayload(token: string): Record<string, unknown> | null {
  try {
    const part = token.split(".")[1];
    if (!part) return null;
    const normalized = part.replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized.padEnd(
      normalized.length + ((4 - (normalized.length % 4)) % 4),
      "=",
    );
    return JSON.parse(atob(padded)) as Record<string, unknown>;
  } catch {
    return null;
  }
}

export function getUsername(): string | null {
  const stored = localStorage.getItem(USERNAME_KEY);
  if (stored) return stored;

  const token = getAccessToken();
  if (!token) return null;
  const payload = readJwtPayload(token);
  const username = payload?.username;
  return typeof username === "string" && username ? username : null;
}

export function setAuthSession(data: {
  accessToken: string;
  refreshToken: string;
  username?: string;
}): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, data.accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, data.refreshToken);
  if (data.username) {
    localStorage.setItem(USERNAME_KEY, data.username);
  }
}

/** @deprecated Prefer setAuthSession */
export function setAuthTokens(accessToken: string, refreshToken: string): void {
  setAuthSession({ accessToken, refreshToken });
}

export function setUsername(username: string): void {
  localStorage.setItem(USERNAME_KEY, username);
}

export function authHeaders(
  extra: Record<string, string> = {},
): Record<string, string> {
  const token = getAccessToken();
  return {
    ...extra,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}
