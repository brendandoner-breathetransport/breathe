import Link from "next/link";

export default function HomePage() {
  return (
    <main className="grid" style={{ gap: "1rem" }}>
      <h1>Civic Affordability Intelligence</h1>
      <p className="muted">MVP scope: Colorado annual affordability indices + direct ballot policy events.</p>
      <div className="card">
        <h2 style={{ marginBottom: "0.75rem" }}>Dashboard</h2>
        <Link className="btn" href="/state/co">Open Colorado Dashboard</Link>
      </div>
      <div className="card">
        <h2 style={{ marginBottom: "0.75rem" }}>Voter Tools</h2>
        <Link className="btn" href="/vote/co/polling-location">Find Colorado Polling Location</Link>
      </div>
    </main>
  );
}
