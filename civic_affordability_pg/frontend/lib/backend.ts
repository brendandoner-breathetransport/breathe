export function buildBackendUrl(path: string, searchParams?: URLSearchParams): string {
  const backendBaseUrl = process.env.BACKEND_API_BASE_URL;
  if (!backendBaseUrl) {
    throw new Error("Missing BACKEND_API_BASE_URL environment variable");
  }
  const base = backendBaseUrl.endsWith("/") ? backendBaseUrl.slice(0, -1) : backendBaseUrl;
  const url = new URL(`${base}${path}`);
  if (searchParams) {
    searchParams.forEach((value, key) => url.searchParams.set(key, value));
  }
  return url.toString();
}

export function toCsv(rows: Array<Record<string, unknown>>): string {
  if (!rows.length) return "";
  const headers = Object.keys(rows[0]);
  const esc = (value: unknown) => {
    const raw = value == null ? "" : String(value);
    if (raw.includes(",") || raw.includes('"') || raw.includes("\n")) {
      return `"${raw.replace(/"/g, '""')}"`;
    }
    return raw;
  };

  const lines = [headers.join(",")];
  for (const row of rows) {
    lines.push(headers.map((h) => esc(row[h])).join(","));
  }
  return lines.join("\n");
}
