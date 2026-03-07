# Civic Affordability User Flow

This document captures:
- the **current implemented flow** (based on existing routes/components)
- a **proposed improved flow** using proven UX patterns (fast first value, guided actions, clear recovery states)

## 1) Current Implemented Flow

```mermaid
flowchart TD
    A[Landing Page /] --> B{Choose Path}
    B -->|Open Colorado Dashboard| C[/state/co Dashboard/]
    B -->|Find Polling Location| D[/vote/co/polling-location/]

    C --> C1[Load Affordability + Policy APIs]
    C1 --> C2[Render Chart + Summary Cards]
    C2 --> C3{User Action}
    C3 -->|Download CSV| C4[GET /api/affordability?format=csv]
    C3 -->|Ask Question| C5[POST /api/ask]
    C5 --> C6[Template + Guardrails]
    C6 --> C7[Return Text + Data + Citations]

    D --> D1[Enter Address + State Inputs]
    D1 --> D2[POST /api/vote/co/polling-location]
    D2 --> D3{Provider Result}
    D3 -->|Found| D4[Show polling/early/dropoff locations]
    D3 -->|Not Found| D5[Show official state fallback guidance]
```

## 2) Improved Flow (Recommended)

```mermaid
flowchart TD
    A[Landing Page /] --> A1[Primary CTA: Find Polling Location]
    A --> A2[Secondary CTA: Explore Colorado Affordability]

    A2 --> B[/state/co Dashboard/]
    B --> B1[Immediate Default Insight Card: Since 2003 change]
    B1 --> B2[Trend Chart with labeled axes + policy markers]
    B2 --> B3{Next Intent}
    B3 -->|Understand why| B4[Policy context panel with short summaries]
    B3 -->|Ask question| B5[Ask the Data input with examples]
    B5 --> B6[Guarded API query]
    B6 --> B7[Plain-language answer + source citations]
    B7 --> B8{Helpful?}
    B8 -->|Yes| B9[Follow-up question chips]
    B8 -->|No| B10[Suggested rephrase prompts]

    A1 --> C[/vote/co/polling-location/]
    C --> C1[Address + state entry]
    C1 --> C2[Provider lookup chain]
    C2 --> C3{Resolved?}
    C3 -->|Yes| C4[Show location + hours + source]
    C3 -->|Partial| C5[Show best-match + clarification step]
    C3 -->|No| C6[Official state lookup link + what to try next]
    C4 --> C7[Optional: Save/share result]
```

## 3) Why This Improved Flow Performs Better

- Reduces time-to-value with a default insight card before users need to ask.
- Uses clear branching for success, partial, and failure states in polling lookup.
- Adds guided follow-ups in Ask flow to reduce dead-end responses.
- Keeps outputs human-readable (plain language + source citations) for trust.
- Preserves your existing architecture and routes; this is mostly UX/interaction polish.
