"use client";

import { useEffect, useMemo, useState } from "react";

type AffordabilityRow = {
  year: number;
  income_index: number;
  housing_index: number;
  healthcare_index: number;
  childcare_index: number;
  income_cpi_2023_index: number;
  healthcare_cpi_2023_index: number;
  childcare_cpi_2023_index: number;
};

type PolicyRow = {
  year: number;
  short_label: string;
  summary: string;
  category: string;
};

type AskPayload = {
  category: string;
  summary: string;
  row_count: number;
  rows: Array<Record<string, unknown>>;
  approved_marts: string[];
};

const seriesMeta = [
  { key: "income_index", label: "Income", color: "#0e7a4e" },
  { key: "housing_index", label: "Housing", color: "#b91c1c" },
  { key: "healthcare_index", label: "Healthcare", color: "#1d4ed8" },
  { key: "childcare_index", label: "Childcare", color: "#a16207" }
] as const;

export default function AffordabilityDashboard() {
  const [stateAbbrev, setStateAbbrev] = useState("CO");
  const [showPolicyMarkers, setShowPolicyMarkers] = useState(true);
  const [indexMode, setIndexMode] = useState<"nominal" | "inflation_adjusted">("nominal");
  const [affordability, setAffordability] = useState<AffordabilityRow[]>([]);
  const [policy, setPolicy] = useState<PolicyRow[]>([]);
  const [question, setQuestion] = useState("What was the largest affordability gap year?");
  const [askResult, setAskResult] = useState<AskPayload | null>(null);
  const [loadingAsk, setLoadingAsk] = useState(false);

  useEffect(() => {
    const run = async () => {
      const [affRes, polRes] = await Promise.all([
        fetch(`/api/affordability?state_abbrev=${stateAbbrev}`, { cache: "no-store" }),
        fetch(`/api/policy?state_abbrev=${stateAbbrev}`, { cache: "no-store" })
      ]);
      const affJson = await affRes.json();
      const polJson = await polRes.json();
      setAffordability(
        (affJson.rows ?? []).map((row: Record<string, unknown>) => ({
          year: Number(row.year),
          income_index: Number(row.income_index),
          housing_index: Number(row.housing_index),
          healthcare_index: Number(row.healthcare_index),
          childcare_index: Number(row.childcare_index),
          income_cpi_2023_index: Number(row.income_cpi_2023_index),
          healthcare_cpi_2023_index: Number(row.healthcare_cpi_2023_index),
          childcare_cpi_2023_index: Number(row.childcare_cpi_2023_index)
        }))
      );
      setPolicy(polJson.rows ?? []);
    };
    run();
  }, [stateAbbrev]);

  const latest = affordability[affordability.length - 1];
  const metricKeys =
    indexMode === "inflation_adjusted"
      ? {
          income: "income_cpi_2023_index",
          healthcare: "healthcare_cpi_2023_index",
          childcare: "childcare_cpi_2023_index"
        }
      : {
          income: "income_index",
          healthcare: "healthcare_index",
          childcare: "childcare_index"
        };
  const incomeVal = latest ? Number(latest[metricKeys.income as keyof AffordabilityRow]) : null;
  const housingVal = latest ? Number(latest.housing_index) : null;
  const healthcareVal = latest ? Number(latest[metricKeys.healthcare as keyof AffordabilityRow]) : null;
  const childcareVal = latest ? Number(latest[metricKeys.childcare as keyof AffordabilityRow]) : null;
  const costPressureVal =
    incomeVal != null && housingVal != null && healthcareVal != null && childcareVal != null
      ? (housingVal + healthcareVal + childcareVal) / 3
      : null;
  const affordabilityGapVal =
    costPressureVal != null && incomeVal != null ? costPressureVal - incomeVal : null;

  const chartLines = useMemo(() => {
    if (!affordability.length) return "";
    const width = 1040;
    const height = 360;
    const padL = 42;
    const padR = 20;
    const padT = 20;
    const padB = 36;
    const minY = 90;
    const maxY =
      Math.max(
        ...affordability.flatMap((r) => [
          Number(r[metricKeys.income as keyof AffordabilityRow]),
          r.housing_index,
          Number(r[metricKeys.healthcare as keyof AffordabilityRow]),
          Number(r[metricKeys.childcare as keyof AffordabilityRow])
        ])
      ) + 15;
    const years = affordability.map((r) => r.year);
    const minX = Math.min(...years);
    const maxX = Math.max(...years);

    const x = (year: number) => padL + ((year - minX) / Math.max(1, maxX - minX)) * (width - padL - padR);
    const y = (val: number) => height - padB - ((val - minY) / Math.max(1, maxY - minY)) * (height - padT - padB);

    const paths = seriesMeta.map((s) => {
      const d = affordability
        .map((r, i) => {
          const value =
            s.key === "income_index"
              ? Number(r[metricKeys.income as keyof AffordabilityRow])
              : s.key === "healthcare_index"
              ? Number(r[metricKeys.healthcare as keyof AffordabilityRow])
              : s.key === "childcare_index"
              ? Number(r[metricKeys.childcare as keyof AffordabilityRow])
              : Number(r[s.key]);
          return `${i === 0 ? "M" : "L"} ${x(r.year).toFixed(1)} ${y(value).toFixed(1)}`;
        })
        .join(" ");
      return `<path d=\"${d}\" fill=\"none\" stroke=\"${s.color}\" stroke-width=\"3\" />`;
    });

    const markerLines = showPolicyMarkers
      ? policy
          .map((p, i) => {
            const px = x(p.year).toFixed(1);
            const textY = (padT + 12 + (i % 2) * 14).toFixed(1);
            return `<line x1=\"${px}\" y1=\"${padT}\" x2=\"${px}\" y2=\"${height - padB}\" stroke=\"#777\" stroke-dasharray=\"4 4\" stroke-width=\"1\" />\n<text x=\"${(Number(px) + 3).toFixed(1)}\" y=\"${textY}\" font-size=\"10\" fill=\"#333\">${i + 1}</text>`;
          })
          .join("\n")
      : "";

    return `<svg class=\"chart\" viewBox=\"0 0 ${width} ${height}\" preserveAspectRatio=\"none\">\n<line x1=\"${padL}\" y1=\"${height - padB}\" x2=\"${width - padR}\" y2=\"${height - padB}\" stroke=\"#c9d2ca\"/>\n<line x1=\"${padL}\" y1=\"${padT}\" x2=\"${padL}\" y2=\"${height - padB}\" stroke=\"#c9d2ca\"/>\n${markerLines}\n${paths.join("\n")}\n</svg>`;
  }, [affordability, policy, showPolicyMarkers, metricKeys]);

  const onAsk = async () => {
    setLoadingAsk(true);
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, state_abbrev: stateAbbrev })
      });
      const json = await res.json();
      setAskResult(json);
    } finally {
      setLoadingAsk(false);
    }
  };

  return (
    <main className="grid" style={{ gap: "1rem" }}>
      <h1>Civic Affordability Intelligence</h1>
      <p className="muted">Base year index = 2003 (100). State scope is Colorado for MVP.</p>

      <div className="card controls">
        <label>
          State:&nbsp;
          <select value={stateAbbrev} onChange={(e) => setStateAbbrev(e.target.value)}>
            <option value="CO">Colorado</option>
          </select>
        </label>
        <label>
          Index Mode:&nbsp;
          <select value={indexMode} onChange={(e) => setIndexMode(e.target.value as "nominal" | "inflation_adjusted")}>
            <option value="nominal">Nominal</option>
            <option value="inflation_adjusted">Inflation-adjusted (CPI 2023)</option>
          </select>
        </label>
        <label>
          <input
            type="checkbox"
            checked={showPolicyMarkers}
            onChange={(e) => setShowPolicyMarkers(e.target.checked)}
          />
          &nbsp;Show policy markers
        </label>
        <a className="btn" href={`/api/affordability?state_abbrev=${stateAbbrev}&format=csv`}>Download Affordability CSV</a>
        <a className="btn" href={`/api/policy?state_abbrev=${stateAbbrev}&format=csv`}>Download Policy CSV</a>
      </div>

      <div className="grid summary-grid">
        <div className="card"><div className="small muted">Income Index</div><h3>{incomeVal?.toFixed?.(1) ?? "-"}</h3></div>
        <div className="card"><div className="small muted">Housing Index</div><h3>{latest?.housing_index?.toFixed?.(1) ?? "-"}</h3></div>
        <div className="card"><div className="small muted">Healthcare Index</div><h3>{healthcareVal?.toFixed?.(1) ?? "-"}</h3></div>
        <div className="card"><div className="small muted">Childcare Index</div><h3>{childcareVal?.toFixed?.(1) ?? "-"}</h3></div>
        <div className="card"><div className="small muted">Cost Pressure</div><h3>{costPressureVal?.toFixed?.(1) ?? "-"}</h3></div>
        <div className="card"><div className="small muted">Affordability Gap</div><h3>{affordabilityGapVal?.toFixed?.(1) ?? "-"}</h3></div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: "0.5rem" }}>Indexed Trend Chart</h2>
        <p className="small muted" style={{ marginTop: 0 }}>
          {indexMode === "inflation_adjusted" ? "Using inflation-adjusted income/healthcare/childcare indexes (CPI 2023)." : "Using nominal indexes."}
        </p>
        <div className="series">
          {seriesMeta.map((s) => (
            <span key={s.key} className="legend-item"><span className="dot" style={{ background: s.color }} />{s.label}</span>
          ))}
        </div>
        <div dangerouslySetInnerHTML={{ __html: chartLines }} />
        {showPolicyMarkers && (
          <div className="small muted" style={{ marginTop: "0.6rem" }}>
            {policy.map((p, i) => (
              <div key={`${p.year}-${p.short_label}`}>{i + 1}. {p.year} - {p.short_label}</div>
            ))}
          </div>
        )}
      </div>

      <div className="grid two-col">
        <div className="card">
          <h2 style={{ marginBottom: "0.75rem" }}>Ask the Data</h2>
          <p className="muted small">Template-based SQL only. Approved marts only. 50 rows max.</p>
          <div className="controls">
            <input value={question} onChange={(e) => setQuestion(e.target.value)} type="text" />
            <button onClick={onAsk} disabled={loadingAsk}>{loadingAsk ? "Running..." : "Ask"}</button>
          </div>
          {askResult && (
            <div style={{ marginTop: "0.8rem" }}>
              <p><strong>{askResult.summary}</strong> <span className="badge">{askResult.category}</span></p>
              <p className="small muted">Rows: {askResult.row_count}</p>
              <p className="small muted">Allowed marts: {askResult.approved_marts?.join(", ")}</p>
            </div>
          )}
        </div>

        <div className="card table-wrap">
          <h3 style={{ marginBottom: "0.5rem" }}>Policy Events</h3>
          <table>
            <thead>
              <tr>
                <th>Year</th>
                <th>Label</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody>
              {policy.map((p) => (
                <tr key={`${p.year}-${p.short_label}`}>
                  <td>{p.year}</td>
                  <td>{p.short_label}</td>
                  <td>{p.category}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
