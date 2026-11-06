#!/usr/bin/env python3
"""Refresh the NHS performance landmark numbers from NHS England's public data gateway.

For one trust (Guy's and St Thomas', RJ1, by default) this reads the headline
waiting-time measures, the trust's rank, the national average and the last 12
months of both, and writes them to _data/landmark_performance.json for the
"How the NHS is performing" page.

Runs in the "Refresh landmark numbers" GitHub Action (the gateway is blocked from
some networks). Run locally with:  python scripts/landmark_numbers/update_performance.py
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

import requests

BASE = "https://data.england.nhs.uk"
OUT = Path(__file__).resolve().parents[2] / "_data" / "landmark_performance.json"
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "Mozilla/5.0 (Discerning Learning landmark numbers)"

# Gateway metric codes, in plain English, with the long-standing NHS standard.
METRICS = [
    {"code": "ae_4_hour", "group": "Urgent and emergency care",
     "label": "A&E patients seen within 4 hours", "standard": "95%", "better": "higher"},
    {"code": "ae_12_hour", "group": "Urgent and emergency care",
     "label": "A&E patients in the department for 12 hours or more", "standard": "No standard",
     "better": "lower"},
    {"code": "within_18_weeks", "group": "Planned care",
     "label": "Waiting under 18 weeks for planned treatment", "standard": "92%", "better": "higher"},
    {"code": "52_plus_weeks", "group": "Planned care",
     "label": "Waiting over a year for planned treatment", "standard": "None waiting", "better": "lower"},
    {"code": "cancer_faster_diagnostic", "group": "Cancer",
     "label": "Cancer diagnosed or ruled out within 28 days", "standard": "75%", "better": "higher"},
    {"code": "cancer_31_day", "group": "Cancer",
     "label": "Cancer treatment within 31 days of the decision to treat", "standard": "96%",
     "better": "higher"},
    {"code": "cancer_62_day", "group": "Cancer",
     "label": "Cancer treatment within 62 days of an urgent referral", "standard": "85%",
     "better": "higher"},
    {"code": "diagnostics_6_weeks", "group": "Diagnostics",
     "label": "Waiting 6 weeks or more for a diagnostic test", "standard": "1%", "better": "lower"},
]


def page_summary(slug):
    """Current value, rank and national average for each metric, from the trust's page."""
    t = SESSION.get(f"{BASE}/providers/{slug}", timeout=60)
    t.raise_for_status()
    codes = list(dict.fromkeys(re.findall(r'name="metricCode" value="([^"]+)"', t.text)))
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                         re.sub(r"(?s)<(script|style).*?</\1>", "", t.text))))
    found = re.findall(r"Current Performance ([\d.]+)% Rank: (\d+) of (\d+) National Average ([\d.]+)%", text)
    if len(found) != len(codes):
        sys.exit(f"Page layout changed: {len(codes)} metrics but {len(found)} summaries")
    return {c: {"rank": int(r), "ranked": int(n)} for c, (_, r, n, _) in zip(codes, found)}


def series(code, provider):
    r = SESSION.post(f"{BASE}/api/export/json", timeout=60,
                     data={"metricCode": code, "providerCode": provider, "includeNational": "true"})
    r.raise_for_status()
    rows = sorted(r.json()["rows"], key=lambda x: x["date"])
    return [{"month": x["date"][:7],
             "trust": None if x["provider_value"] is None else round(x["provider_value"] * 100, 1),
             "national": None if x["national_value"] is None else round(x["national_value"] * 100, 1)}
            for x in rows]


def spark(values, lo, hi, width=120, height=32):
    """SVG polyline points for a small trend line."""
    pts = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(pts) < 2 or hi == lo:
        return ""
    step = width / (len(values) - 1)
    return " ".join(f"{i * step:.1f},{height - (v - lo) / (hi - lo) * height:.1f}" for i, v in pts)


def month_name(ym):
    return dt.datetime.strptime(ym, "%Y-%m").strftime("%B %Y")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="RJ1")
    ap.add_argument("--slug", default="guy-s-and-st-thomas-nhs-foundation-trust")
    ap.add_argument("--provider-name", default="Guy's and St Thomas'")
    args = ap.parse_args()

    ranks = page_summary(args.slug)
    rows = []
    for m in METRICS:
        s = series(m["code"], args.provider)
        if not s or s[-1]["trust"] is None:
            sys.exit(f"No data for {m['code']}")
        latest = s[-1]
        vals = [v for x in s for v in (x["trust"], x["national"]) if v is not None]
        lo, hi = min(vals), max(vals)
        pad = max((hi - lo) * 0.1, 0.5)
        rows.append({**m,
                     "month": latest["month"], "month_text": month_name(latest["month"]),
                     "trust": latest["trust"], "national": latest["national"],
                     "rank": ranks.get(m["code"], {}).get("rank"),
                     "ranked": ranks.get(m["code"], {}).get("ranked"),
                     "series": s,
                     "trend_from": month_name(s[0]["month"]),
                     "spark_trust": spark([x["trust"] for x in s], lo - pad, hi + pad),
                     "spark_national": spark([x["national"] for x in s], lo - pad, hi + pad)})
        print(f"{m['code']}: {args.provider} {latest['trust']}% vs England {latest['national']}% "
              f"({latest['month']}), rank {rows[-1]['rank']} of {rows[-1]['ranked']}")

    data = {
        "provider_code": args.provider,
        "provider_name": args.provider_name,
        "source_page": f"{BASE}/providers/{args.slug}",
        "latest_month_text": max((r["month"] for r in rows)),
        "metrics": rows,
    }
    data["latest_month_text"] = month_name(data["latest_month_text"])

    today = dt.date.today().isoformat()
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    figures = lambda x: {k: v for k, v in x.items() if k not in ("last_checked", "last_updated")}
    changed = figures(old) != data
    data["last_updated"] = today if changed or "last_updated" not in old else old["last_updated"]
    data["last_checked"] = today
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("PERFORMANCE", "CHANGED" if changed else "UNCHANGED", "- latest", data["latest_month_text"])


if __name__ == "__main__":
    main()
