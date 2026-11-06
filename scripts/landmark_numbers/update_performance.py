#!/usr/bin/env python3
"""Refresh the NHS performance landmark numbers from NHS England's public data gateway.

For one trust (Guy's and St Thomas', RJ1, by default) this reads the headline
waiting-time measures, the trust's national rank, the national average and the
last 12 months of both. It also reads the same measures for the ten Shelford Group
teaching hospitals so the trust can be compared with its peers. Everything is
written to _data/landmark_performance.json for the "How the NHS is performing" page.

Runs in the "Refresh landmark numbers" GitHub Action (the gateway is blocked from
some networks). Run locally with:  python scripts/landmark_numbers/update_performance.py
"""
import argparse
import datetime as dt
import html
import json
import re
import statistics
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
     "label": "A&E patients seen within 4 hours", "short": "A&E 4 hours",
     "standard": "95%", "better": "higher"},
    {"code": "ae_12_hour", "group": "Urgent and emergency care",
     "label": "A&E patients in the department for 12 hours or more", "short": "A&E 12+ hours",
     "standard": "No standard", "better": "lower"},
    {"code": "within_18_weeks", "group": "Planned care",
     "label": "Waiting under 18 weeks for planned treatment", "short": "Under 18 weeks",
     "standard": "92%", "better": "higher"},
    {"code": "52_plus_weeks", "group": "Planned care",
     "label": "Waiting over a year for planned treatment", "short": "Over 52 weeks",
     "standard": "None waiting", "better": "lower"},
    {"code": "cancer_faster_diagnostic", "group": "Cancer",
     "label": "Cancer diagnosed or ruled out within 28 days", "short": "Cancer 28 days",
     "standard": "75%", "better": "higher"},
    {"code": "cancer_31_day", "group": "Cancer",
     "label": "Cancer treatment within 31 days of the decision to treat", "short": "Cancer 31 days",
     "standard": "96%", "better": "higher"},
    {"code": "cancer_62_day", "group": "Cancer",
     "label": "Cancer treatment within 62 days of an urgent referral", "short": "Cancer 62 days",
     "standard": "85%", "better": "higher"},
    {"code": "diagnostics_6_weeks", "group": "Diagnostics",
     "label": "Waiting 6 weeks or more for a diagnostic test", "short": "Tests 6+ weeks",
     "standard": "1%", "better": "lower"},
]

# The Shelford Group: ten large NHS teaching hospital trusts (shelfordgroup.org/members).
SHELFORD = {
    "RGT": "Cambridge University Hospitals",
    "RJ1": "Guy's and St Thomas'",
    "RYJ": "Imperial College Healthcare",
    "RJZ": "King's College Hospital",
    "R0A": "Manchester University",
    "RTD": "Newcastle upon Tyne Hospitals",
    "RTH": "Oxford University Hospitals",
    "RHQ": "Sheffield Teaching Hospitals",
    "RRV": "University College London Hospitals",
    "RRK": "University Hospitals Birmingham",
}


def page_summary(slug):
    """Rank among all ranked trusts for each metric, from the trust's gateway page."""
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
    """Last 12 months for one trust and the national average, as percentages."""
    r = SESSION.post(f"{BASE}/api/export/json", timeout=60,
                     data={"metricCode": code, "providerCode": provider, "includeNational": "true"})
    r.raise_for_status()
    pct = lambda v: None if v is None else round(v * 100, 1)
    return [{"month": x["date"][:7], "trust": pct(x["provider_value"]), "national": pct(x["national_value"])}
            for x in sorted(r.json()["rows"], key=lambda x: x["date"])]


def spark(values, lo, hi, width=120, height=32):
    """SVG polyline points for a small trend line."""
    pts = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(pts) < 2 or hi == lo:
        return ""
    step = width / (len(values) - 1)
    return " ".join(f"{i * step:.1f},{height - (v - lo) / (hi - lo) * height:.1f}" for i, v in pts)


def month_name(ym):
    return dt.datetime.strptime(ym, "%Y-%m").strftime("%B %Y")


def shelford(metric, month, provider):
    """Each Shelford trust's value for the same month, best first, with positions."""
    peers = []
    for code, name in SHELFORD.items():
        try:
            row = next((x for x in series(metric["code"], code) if x["month"] == month), None)
        except requests.RequestException as e:
            print(f"  {code} {metric['code']}: {e}")
            row = None
        if row and row["trust"] is not None:
            peers.append({"code": code, "name": name, "value": row["trust"], "is_trust": code == provider})
    peers.sort(key=lambda p: (p["value"] if metric["better"] == "lower" else -p["value"], not p["is_trust"]))
    for p in peers:
        # Ties share a position: 1 + the number of trusts strictly better.
        better = [q for q in peers if (q["value"] > p["value"] if metric["better"] == "higher"
                                       else q["value"] < p["value"])]
        p["position"] = len(better) + 1
        p["tied"] = sum(q["value"] == p["value"] for q in peers) > 1
    return peers


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
        peers = shelford(m, latest["month"], args.provider)
        if len(peers) < 8:
            sys.exit(f"Only {len(peers)} Shelford trusts have {m['code']} data for {latest['month']}")
        values = [p["value"] for p in peers]
        me = next((p for p in peers if p["is_trust"]), None)

        trend = [v for x in s for v in (x["trust"], x["national"]) if v is not None]
        lo, hi = min(trend), max(trend)
        pad = max((hi - lo) * 0.1, 0.5)
        # Positions (0-100) on a strip covering all ten trusts and England.
        strip = values + [latest["national"]]
        s_lo, s_hi = min(strip), max(strip)
        span = (s_hi - s_lo) or 1
        for p in peers:
            p["x"] = round((p["value"] - s_lo) / span * 100, 1)

        rows.append({**m,
                     "month": latest["month"], "month_text": month_name(latest["month"]),
                     "trust": latest["trust"], "national": latest["national"],
                     "rank": ranks.get(m["code"], {}).get("rank"),
                     "ranked": ranks.get(m["code"], {}).get("ranked"),
                     "shelford_median": round(statistics.median(values), 1),
                     "shelford_position": me["position"] if me else None,
                     "shelford_tied": me["tied"] if me else False,
                     "shelford_count": len(peers),
                     "shelford_min": s_lo, "shelford_max": s_hi,
                     "national_x": round((latest["national"] - s_lo) / span * 100, 1),
                     "shelford": peers,
                     "series": s,
                     "trend_from": month_name(s[0]["month"]),
                     "spark_trust": spark([x["trust"] for x in s], lo - pad, hi + pad),
                     "spark_national": spark([x["national"] for x in s], lo - pad, hi + pad)})
        r = rows[-1]
        print(f"{m['code']} ({latest['month']}): {args.provider} {r['trust']}%, England {r['national']}%, "
              f"Shelford median {r['shelford_median']}%; rank {r['rank']} of {r['ranked']}, "
              f"Shelford {r['shelford_position']} of {r['shelford_count']}")

    data = {
        "provider_code": args.provider,
        "provider_name": args.provider_name,
        "source_page": f"{BASE}/providers/{args.slug}",
        "shelford_source": "https://shelfordgroup.org/members/",
        "latest_month_text": month_name(max(r["month"] for r in rows)),
        "metrics": rows,
    }

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
