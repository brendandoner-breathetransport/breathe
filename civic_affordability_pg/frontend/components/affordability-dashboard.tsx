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

type ExpenseShareRow = {
  year: number;
  healthcare_share_pct_of_monthly_income: number;
  childcare_share_pct_of_monthly_income: number;
  known_expense_share_pct_of_monthly_income: number;
  healthcare_share_cpi_2023_pct_of_monthly_income: number;
  childcare_share_cpi_2023_pct_of_monthly_income: number;
  known_expense_share_cpi_2023_pct_of_monthly_income: number;
  estimated_home_price: number;
  estimated_loan_amount: number;
  estimated_monthly_mortgage_payment: number;
  estimated_mortgage_share_pct_of_monthly_income: number;
  estimated_mortgage_share_cpi_2023_pct_of_monthly_income: number;
};

type AskPayload = {
  category: string;
  summary: string;
  answer_text: string;
  query_template: string;
  query_sql: string;
  query_params: Record<string, unknown>;
  confidence: "low" | "medium" | "high";
  warnings: string[];
  row_count: number;
  table_rows: Array<Record<string, unknown>>;
  table_columns: string[];
  approved_marts: string[];
  citations: Array<{
    dataset: string;
    metric_columns: string[];
    state: string;
    year_range: string;
    row_count_used: number;
    method_note: string;
    external_sources: Array<{
      domain: string;
      source_name: string;
      publisher: string;
      source_url: string;
    }>;
  }>;
  grounding: {
    state: string;
    rows_used: number;
    year_min: number | null;
    year_max: number | null;
  };
  question_guide: {
    supported_categories: string[];
    example_prompts: string[];
  };
};

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  text: string;
  payload?: AskPayload;
  createdAt: string;
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
  const [expenseShare, setExpenseShare] = useState<ExpenseShareRow[]>([]);
  const [question, setQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      text: "Ask about affordability trends, year comparisons, component differences, or policy impact.",
      createdAt: new Date().toISOString()
    }
  ]);
  const [selectedResult, setSelectedResult] = useState<AskPayload | null>(null);
  const [loadingAsk, setLoadingAsk] = useState(false);
  const [showQueryDetails, setShowQueryDetails] = useState(false);

  const suggestionPrompts = [
    "What was the largest affordability gap year?",
    "Compare before and after 2010 and 2023.",
    "How did policy impact in 2020?",
    "Give me a trend summary."
  ];

  useEffect(() => {
    const run = async () => {
      const [affRes, polRes, expenseRes] = await Promise.all([
        fetch(`/api/affordability?state_abbrev=${stateAbbrev}`, { cache: "no-store" }),
        fetch(`/api/policy?state_abbrev=${stateAbbrev}`, { cache: "no-store" }),
        fetch(`/api/expense-share?state_abbrev=${stateAbbrev}`, { cache: "no-store" })
      ]);
      const affJson = await affRes.json();
      const polJson = await polRes.json();
      const expenseJson = await expenseRes.json();
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
      setExpenseShare(
        (expenseJson.rows ?? []).map((row: Record<string, unknown>) => ({
          year: Number(row.year),
          healthcare_share_pct_of_monthly_income: Number(row.healthcare_share_pct_of_monthly_income),
          childcare_share_pct_of_monthly_income: Number(row.childcare_share_pct_of_monthly_income),
          known_expense_share_pct_of_monthly_income: Number(row.known_expense_share_pct_of_monthly_income),
          healthcare_share_cpi_2023_pct_of_monthly_income: Number(row.healthcare_share_cpi_2023_pct_of_monthly_income),
          childcare_share_cpi_2023_pct_of_monthly_income: Number(row.childcare_share_cpi_2023_pct_of_monthly_income),
          known_expense_share_cpi_2023_pct_of_monthly_income: Number(row.known_expense_share_cpi_2023_pct_of_monthly_income),
          estimated_home_price: Number(row.estimated_home_price),
          estimated_loan_amount: Number(row.estimated_loan_amount),
          estimated_monthly_mortgage_payment: Number(row.estimated_monthly_mortgage_payment),
          estimated_mortgage_share_pct_of_monthly_income: Number(row.estimated_mortgage_share_pct_of_monthly_income),
          estimated_mortgage_share_cpi_2023_pct_of_monthly_income: Number(row.estimated_mortgage_share_cpi_2023_pct_of_monthly_income)
        }))
      );
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
  const latestExpenseShare = expenseShare[expenseShare.length - 1];
  const healthcareShareVal = latestExpenseShare
    ? Number(
        indexMode === "inflation_adjusted"
          ? latestExpenseShare.healthcare_share_cpi_2023_pct_of_monthly_income
          : latestExpenseShare.healthcare_share_pct_of_monthly_income
      )
    : null;
  const childcareShareVal = latestExpenseShare
    ? Number(
        indexMode === "inflation_adjusted"
          ? latestExpenseShare.childcare_share_cpi_2023_pct_of_monthly_income
          : latestExpenseShare.childcare_share_pct_of_monthly_income
      )
    : null;
  const knownExpenseShareVal = latestExpenseShare
    ? Number(
        indexMode === "inflation_adjusted"
          ? latestExpenseShare.known_expense_share_cpi_2023_pct_of_monthly_income
          : latestExpenseShare.known_expense_share_pct_of_monthly_income
      )
    : null;
  const mortgageShareVal = latestExpenseShare
    ? Number(
        indexMode === "inflation_adjusted"
          ? latestExpenseShare.estimated_mortgage_share_cpi_2023_pct_of_monthly_income
          : latestExpenseShare.estimated_mortgage_share_pct_of_monthly_income
      )
    : null;

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
    if (!question.trim()) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `u-${Date.now()}`,
      role: "user",
      text: question.trim(),
      createdAt: new Date().toISOString()
    };
    setChatMessages((prev) => [...prev, userMessage]);
    setLoadingAsk(true);
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question.trim(), state_abbrev: stateAbbrev })
      });
      const json = await res.json();
      if (!res.ok) {
        const detail = json?.detail || "Ask API request failed";
        throw new Error(`${detail}`);
      }
      const payload = json as AskPayload;
      const assistantMessage: ChatMessage = {
        id: `a-${Date.now()}`,
        role: "assistant",
        text: payload.answer_text,
        payload,
        createdAt: new Date().toISOString()
      };
      setChatMessages((prev) => [...prev, assistantMessage]);
      setSelectedResult(payload);
      setQuestion("");
    } catch (error) {
      const assistantMessage: ChatMessage = {
        id: `e-${Date.now()}`,
        role: "assistant",
        text: `I hit an error: ${error instanceof Error ? error.message : "unknown error"}`,
        createdAt: new Date().toISOString()
      };
      setChatMessages((prev) => [...prev, assistantMessage]);
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
        <a className="btn" href={`/api/expense-share?state_abbrev=${stateAbbrev}&format=csv`}>Download Expense Share CSV</a>
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

      <div className="card">
        <h2 style={{ marginBottom: "0.5rem" }}>Marked Expenses as % of Monthly Income</h2>
        <p className="small muted" style={{ marginTop: 0 }}>
          Combined known expenses now include healthcare, childcare, and estimated mortgage share.
        </p>
        <div className="grid summary-grid">
          <div className="card"><div className="small muted">Healthcare %</div><h3>{healthcareShareVal?.toFixed?.(1) ?? "-"}%</h3></div>
          <div className="card"><div className="small muted">Childcare %</div><h3>{childcareShareVal?.toFixed?.(1) ?? "-"}%</h3></div>
          <div className="card"><div className="small muted">Estimated Mortgage %</div><h3>{mortgageShareVal?.toFixed?.(1) ?? "-"}%</h3></div>
          <div className="card"><div className="small muted">Known Expenses (Total) %</div><h3>{knownExpenseShareVal?.toFixed?.(1) ?? "-"}%</h3></div>
        </div>
      </div>

      <div className="grid two-col">
        <div className="card">
          <h2 style={{ marginBottom: "0.75rem" }}>Ask the Data</h2>
          <p className="muted small">Template-routed queries only. Approved marts only. 50 rows max.</p>
          <div className="controls" style={{ marginBottom: "0.75rem" }}>
            {suggestionPrompts.map((prompt) => (
              <button
                key={prompt}
                className="btn"
                style={{ background: "#2f3a46", fontSize: "0.8rem", padding: "0.4rem 0.55rem" }}
                onClick={() => setQuestion(prompt)}
                type="button"
              >
                {prompt}
              </button>
            ))}
          </div>
          <div
            style={{
              border: "1px solid #d9e0d8",
              borderRadius: "10px",
              padding: "0.65rem",
              maxHeight: "300px",
              overflowY: "auto",
              display: "grid",
              gap: "0.55rem",
              marginBottom: "0.7rem"
            }}
          >
            {chatMessages.map((message) => (
              <div
                key={message.id}
                style={{
                  justifySelf: message.role === "user" ? "end" : "start",
                  background: message.role === "user" ? "#111827" : "#f6f7f9",
                  color: message.role === "user" ? "#ffffff" : "#1f2937",
                  borderRadius: "12px",
                  padding: "0.55rem 0.7rem",
                  maxWidth: "90%"
                }}
              >
                <div style={{ fontSize: "0.9rem" }}>{message.text}</div>
                {message.payload && (
                  <div className="small" style={{ marginTop: "0.35rem", opacity: 0.85 }}>
                    {message.payload.category} · confidence {message.payload.confidence}
                  </div>
                )}
                {message.payload?.grounding && message.payload.grounding.year_min != null ? (
                  <div className="small" style={{ marginTop: "0.2rem", opacity: 0.85 }}>
                    Grounding: {message.payload.grounding.state}, {message.payload.grounding.rows_used} row(s),{" "}
                    {message.payload.grounding.year_min}-{message.payload.grounding.year_max}
                  </div>
                ) : null}
                {message.payload?.citations?.length ? (
                  <div className="small" style={{ marginTop: "0.2rem", opacity: 0.85 }}>
                    Sources: {(message.payload.citations[0].external_sources ?? []).map((s) => s.publisher).join(", ")}
                  </div>
                ) : null}
              </div>
            ))}
            {loadingAsk && (
              <div style={{ justifySelf: "start", background: "#f6f7f9", borderRadius: "12px", padding: "0.55rem 0.7rem" }}>
                Thinking...
              </div>
            )}
          </div>
          <div className="controls">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loadingAsk) {
                  onAsk();
                }
              }}
              type="text"
              placeholder="Ask about trends, comparisons, or policy impact..."
            />
            <button onClick={onAsk} disabled={loadingAsk}>{loadingAsk ? "Running..." : "Ask"}</button>
          </div>
          {selectedResult && (
            <div style={{ marginTop: "0.8rem" }}>
              <p><strong>{selectedResult.summary}</strong> <span className="badge">{selectedResult.category}</span></p>
              <p className="small muted">Rows: {selectedResult.row_count} · Template: {selectedResult.query_template}</p>
              <p className="small muted">Allowed marts: {selectedResult.approved_marts?.join(", ")}</p>
              {selectedResult.grounding?.year_min != null ? (
                <p className="small muted">
                  Grounded on {selectedResult.grounding.rows_used} row(s) in {selectedResult.grounding.state} for years{" "}
                  {selectedResult.grounding.year_min}-{selectedResult.grounding.year_max}.
                </p>
              ) : null}
              {selectedResult.warnings?.length ? (
                <p className="small" style={{ color: "#9a3412" }}>{selectedResult.warnings.join(" ")}</p>
              ) : null}
              {selectedResult.citations?.length ? (
                <div style={{ marginTop: "0.55rem" }}>
                  <p className="small muted" style={{ marginBottom: "0.35rem" }}><strong>Sources</strong></p>
                  {selectedResult.citations.map((citation, idx) => (
                    <div key={`citation-${idx}`} className="small muted" style={{ marginBottom: "0.55rem" }}>
                      <div>[{idx + 1}] Metrics: {citation.metric_columns.join(", ")}</div>
                      <div>Coverage: {citation.state} | years {citation.year_range} | rows {citation.row_count_used}</div>
                      <div>Method: {citation.method_note}</div>
                      {(citation.external_sources ?? []).map((source, sourceIdx) => (
                        <div key={`citation-${idx}-src-${sourceIdx}`}>
                          {source.domain}:{" "}
                          <a href={source.source_url} target="_blank" rel="noreferrer">
                            {source.source_name}
                          </a>{" "}
                          ({source.publisher})
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              ) : null}
              <button
                type="button"
                className="btn"
                style={{ marginTop: "0.4rem", background: "#374151" }}
                onClick={() => setShowQueryDetails((v) => !v)}
              >
                {showQueryDetails ? "Hide query details" : "Show query details"}
              </button>
              {showQueryDetails ? (
                <pre className="small" style={{ marginTop: "0.55rem", whiteSpace: "pre-wrap" }}>
                  SQL: {selectedResult.query_sql}
                  {"\n"}
                  Params: {JSON.stringify(selectedResult.query_params)}
                </pre>
              ) : null}
            </div>
          )}
        </div>

        <div className="card table-wrap">
          <h3 style={{ marginBottom: "0.5rem" }}>{selectedResult ? "Latest Ask Table" : "Policy Events"}</h3>
          <table>
            <thead>
              {selectedResult?.table_rows?.length ? (
                <tr>
                  {Object.keys(selectedResult.table_rows[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              ) : (
                <tr>
                  <th>Year</th>
                  <th>Label</th>
                  <th>Category</th>
                </tr>
              )}
            </thead>
            <tbody>
              {selectedResult?.table_rows?.length
                ? selectedResult.table_rows.slice(0, 20).map((row, idx) => (
                    <tr key={`ask-row-${idx}`}>
                      {Object.keys(selectedResult.table_rows[0]).map((key) => (
                        <td key={`${idx}-${key}`}>{String(row[key] ?? "")}</td>
                      ))}
                    </tr>
                  ))
                : policy.map((p) => (
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
