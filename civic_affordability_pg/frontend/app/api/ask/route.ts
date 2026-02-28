import { NextRequest, NextResponse } from "next/server";

import { buildBackendUrl } from "@/lib/backend";

export async function POST(req: NextRequest) {
  const body = await req.json();

  const upstream = await fetch(buildBackendUrl("/api/ask"), {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store"
  });

  const payload = await upstream.json();
  return NextResponse.json(payload, { status: upstream.status });
}
