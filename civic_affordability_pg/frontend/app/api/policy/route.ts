import { NextRequest, NextResponse } from "next/server";

import { buildBackendUrl, toCsv } from "@/lib/backend";

export async function GET(req: NextRequest) {
  const state = (req.nextUrl.searchParams.get("state_abbrev") || "CO").toUpperCase();
  const format = (req.nextUrl.searchParams.get("format") || "json").toLowerCase();

  const upstreamUrl = buildBackendUrl("/api/policy", new URLSearchParams({ state_abbrev: state }));
  const upstream = await fetch(upstreamUrl, { cache: "no-store" });

  if (!upstream.ok) {
    return NextResponse.json({ error: "Backend policy request failed" }, { status: upstream.status });
  }

  const payload = await upstream.json();

  if (format === "csv") {
    const csv = toCsv(payload.rows ?? []);
    return new NextResponse(csv, {
      status: 200,
      headers: {
        "content-type": "text/csv; charset=utf-8",
        "content-disposition": `attachment; filename=policy_${state.toLowerCase()}.csv`
      }
    });
  }

  return NextResponse.json(payload);
}
