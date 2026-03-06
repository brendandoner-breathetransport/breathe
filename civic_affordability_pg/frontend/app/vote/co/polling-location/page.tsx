"use client";

import { FormEvent, useState } from "react";

type PollingLocation = {
  location_type: string;
  name: string;
  address: string;
  hours?: string | null;
  notes?: string | null;
  source_name?: string;
  source_url?: string;
  maps_url?: string | null;
};

type PollingResponse = {
  status: "ok" | "no_match" | "unavailable" | "error";
  message: string;
  request_address: string;
  election?: {
    id?: string;
    name?: string;
    date?: string;
  };
  result_count?: number;
  locations?: PollingLocation[];
  citations?: Array<{ source_name: string; publisher: string; source_url: string }>;
  official_fallback_url: string;
  retrieved_at_utc: string;
  provider_detail?: string;
};

export default function ColoradoPollingLocationPage() {
  const [street, setStreet] = useState("");
  const [city, setCity] = useState("");
  const [zip, setZip] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PollingResponse | null>(null);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/vote/co/polling-location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ street, city, zip, state_abbrev: "CO" })
      });
      const payload = await res.json();
      setResult(payload);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="grid" style={{ gap: "1rem" }}>
      <h1>Colorado Polling Location Finder</h1>
      <p className="muted">Enter your Colorado voting address to find polling location details with official source links.</p>

      <form className="card grid" style={{ gap: "0.6rem" }} onSubmit={onSubmit}>
        <label>
          Street address
          <input value={street} onChange={(e) => setStreet(e.target.value)} required placeholder="123 Main St" />
        </label>
        <label>
          City
          <input value={city} onChange={(e) => setCity(e.target.value)} required placeholder="Denver" />
        </label>
        <label>
          ZIP
          <input value={zip} onChange={(e) => setZip(e.target.value)} required placeholder="80202" />
        </label>
        <button type="submit" disabled={loading}>{loading ? "Looking up..." : "Find Polling Location"}</button>
      </form>

      {result ? (
        <div className="card grid" style={{ gap: "0.6rem" }}>
          <h2 style={{ marginBottom: "0.2rem" }}>{result.status === "ok" ? "Polling Locations" : "Lookup Result"}</h2>
          <p className="muted">{result.message}</p>
          <p className="small muted">Address: {result.request_address}</p>
          {result.election?.name ? (
            <p className="small muted">Election: {result.election.name} ({result.election.date})</p>
          ) : null}

          {result.locations?.length ? (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Name</th>
                    <th>Address</th>
                    <th>Hours</th>
                    <th>Map</th>
                  </tr>
                </thead>
                <tbody>
                  {result.locations.map((loc, idx) => (
                    <tr key={`${loc.location_type}-${idx}`}>
                      <td>{loc.location_type}</td>
                      <td>{loc.name}</td>
                      <td>{loc.address}</td>
                      <td>{loc.hours || "-"}</td>
                      <td>{loc.maps_url ? <a href={loc.maps_url} target="_blank" rel="noreferrer">Directions</a> : "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null}

          <div>
            <p className="small muted"><strong>Official fallback:</strong> <a href={result.official_fallback_url} target="_blank" rel="noreferrer">Colorado Secretary of State lookup</a></p>
            {result.citations?.length ? (
              <div className="small muted">
                <strong>Sources:</strong>
                {result.citations.map((c, i) => (
                  <div key={`source-${i}`}>
                    [{i + 1}] <a href={c.source_url} target="_blank" rel="noreferrer">{c.source_name}</a> ({c.publisher})
                  </div>
                ))}
              </div>
            ) : null}
            <p className="small muted">Retrieved: {new Date(result.retrieved_at_utc).toLocaleString()}</p>
          </div>
        </div>
      ) : null}
    </main>
  );
}
