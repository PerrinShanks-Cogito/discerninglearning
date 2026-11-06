#!/usr/bin/env python3
"""Refresh the NHS cost landmark numbers from NHS England's National Cost Collection.

Finds the latest "National Cost Collection Data Publication" through NHS England's
WordPress API, downloads the cost index (NCCI) files, which give cost and activity
for every trust by department and service,
and writes national averages and one trust's figures to _data/landmark_ncc.json,
which the Landmark Numbers page reads.

Runs in the "Refresh landmark numbers" GitHub Action (NHS England blocks many
other hosts). Run locally with:  python scripts/landmark_numbers/update_ncc.py
"""
import argparse
import datetime as dt
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

API = "https://www.england.nhs.uk/wp-json/wp/v2/"
OUT = Path(__file__).resolve().parents[2] / "_data" / "landmark_ncc.json"
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "Mozilla/5.0 (Discerning Learning landmark numbers)"

# Each landmark: departments (and optionally service codes) from the NCCI
# department and service file, summed as total cost / total activity.
METRICS = [
    {"key": "ae_major", "label": "A&E attendance at a major (type 1) emergency department",
     "unit": "attendance", "departments": ["EC"], "services": ["01EC"],
     "use": "Pricing avoided A&E attendances"},
    {"key": "ae_all", "label": "Any emergency care attendance (incl. urgent treatment centres)",
     "unit": "attendance", "departments": ["EC"],
     "use": "Same-day and urgent care pathways"},
    {"key": "op_consultant", "label": "Outpatient appointment, consultant-led",
     "unit": "appointment", "departments": ["CL"],
     "use": "Pricing avoided or virtual follow-ups"},
    {"key": "op_non_consultant", "label": "Outpatient appointment, nurse or therapist-led",
     "unit": "appointment", "departments": ["NCL"],
     "use": "Shifting follow-ups to other professions"},
    {"key": "op_procedure", "label": "Outpatient procedure",
     "unit": "procedure", "departments": ["OPROC"],
     "use": "Moving procedures out of theatres"},
    {"key": "day_case", "label": "Day case",
     "unit": "case", "departments": ["DC"],
     "use": "Converting inpatient stays to day cases"},
    {"key": "elective", "label": "Planned (elective) inpatient stay",
     "unit": "stay", "departments": ["EL"],
     "use": "Elective recovery and cancelled operations"},
    {"key": "non_elective", "label": "Emergency (non-elective) inpatient stay",
     "unit": "stay", "departments": ["NEL", "NES"],
     "use": "Pricing avoided emergency admissions"},
    {"key": "non_elective_short", "label": "Emergency stay of 0 or 1 nights",
     "unit": "stay", "departments": ["NES"],
     "use": "Same-day emergency care (SDEC) cases"},
    {"key": "critical_care_adult", "label": "Adult critical care bed day",
     "unit": "bed day", "departments": ["ACC"],
     "use": "Avoided or shortened ICU stays"},
]


def get(url, **kw):
    r = SESSION.get(url, timeout=kw.pop("timeout", 120), **kw)
    r.raise_for_status()
    return r


def latest_publication():
    """Return (title, year label, document JSON) for the newest data publication."""
    hits = get(API + "search", params={"search": "National Cost Collection Data Publication",
                                       "per_page": 50}).json()
    pubs = []
    for h in hits:
        m = re.match(r"(\d{4})/(\d{2}) National Cost Collection Data Publication", h.get("title", ""))
        if m and h.get("subtype") == "document":
            pubs.append((int(m.group(1)), h))
    if not pubs:
        sys.exit("No National Cost Collection data publications found")
    year, hit = max(pubs, key=lambda p: p[0])
    doc = get(hit["_links"]["self"][0]["href"]).json()
    return f"{year}/{str(year + 1)[-2:]}", doc


def file_urls(doc):
    urls = set(u.replace("\\/", "/") for u in re.findall(r'https?:\\?/\\?/[^"\s<>]+\.zip', json.dumps(doc)))
    for a in doc.get("_links", {}).get("wp:attachment", []):
        for m in get(a["href"], params={"per_page": 100}).json():
            if m.get("source_url", "").endswith(".zip"):
                urls.add(m["source_url"])
    return sorted(urls)


def dashboards(doc):
    """Power BI dashboards linked from the publication page, keyed by their link text."""
    found = {}
    for value in (doc.get("custom_fields") or {}).values():
        if isinstance(value, str):
            for href, label in re.findall(r'href="(https://app\.powerbi\.com/[^"]+)"[^>]*>([^<]+)</a>', value):
                found[label.strip()] = href
    return found


def pick(urls, pattern, exclude=r"unsuppressed|HCD"):
    found = [u for u in urls if re.search(pattern, u, re.I) and not re.search(exclude, u, re.I)]
    if not found:
        sys.exit(f"No file matching {pattern} in {urls}")
    return found[0]


def read_zip(url):
    return zipfile.ZipFile(io.BytesIO(get(url, timeout=900).content))


def col(df, *names):
    for n in names:
        for c in df.columns:
            if c.strip().lower() == n.lower():
                return c
    sys.exit(f"Missing column {names} in {list(df.columns)}")


def money(series):
    return pd.to_numeric(series.astype(str).str.replace(r"[£,Â\s]", "", regex=True), errors="coerce")


def department_costs(z):
    """Cost and activity by provider, department and service (the NCCI detail file).

    Cells with very small activity are suppressed ("*") for confidentiality; they are
    left out of both cost and activity so each unit cost stays like-for-like.
    """
    name = next(n for n in z.namelist() if re.search(r"Department and Service Unadjusted\.csv$", n, re.I))
    df = pd.read_csv(z.open(name), encoding="utf-8-sig", dtype=str)
    out = pd.DataFrame({
        "provider": df[col(df, "Provider")].str.split(" - ").str[0].str.strip(),
        "department": df[col(df, "Department")].str.split(" - ").str[0].str.strip(),
        "service": df[col(df, "Service")].str.split(" - ").str[0].str.strip(),
        "activity": money(df[col(df, "Activity")]),
        "cost": money(df[col(df, "Actual Cost")]),
    })
    total_cost = out.cost.sum()
    trust_cost = out.groupby("provider").cost.sum()
    return out.dropna(subset=["activity", "cost"]), total_cost, trust_cost


def ncci(z, provider):
    name = next(n for n in z.namelist() if re.search(r"Mapping Pot MFF Adjusted\.xlsx$", n, re.I))
    raw = pd.read_excel(io.BytesIO(z.read(name)), header=None)
    pots = raw.iloc[0].tolist()
    row = raw[raw[0].astype(str).str.startswith(provider + " ")]
    if row.empty:
        return None, []
    row = row.iloc[0]
    areas = []
    for i, label in enumerate(pots[1:], start=1):
        v = pd.to_numeric(row[i], errors="coerce")
        if pd.notna(v):
            areas.append({"area": re.sub(r"^\d+_[^ ]+ - ", "", str(label)).replace(" And ", " and "), "index": round(float(v))})
    total = next((a["index"] for a in areas if a["area"] == "Total"), None)
    return total, [a for a in areas if a["area"] != "Total"]


def remember(x):
    """Round to two significant figures for the 'remember it as' column."""
    if x >= 10000:
        return f"£{round(x, -3):,.0f}"
    digits = len(str(int(x))) - 2
    return f"£{round(x, -digits):,.0f}"


def count(n):
    """Readable activity count, e.g. 17.2 million or 124,000."""
    if n >= 1e6:
        return f"{n / 1e6:.1f} million"
    return f"{round(n, -(len(str(int(n))) - 3)):,.0f}" if n >= 1000 else str(int(n))


def unit_costs(d, provider):
    rows = []
    for m in METRICS:
        sel = d[d.department.isin(m["departments"])]
        if "services" in m:
            sel = sel[sel.service.isin(m["services"])]
        nat = sel.cost.sum() / sel.activity.sum()
        p = sel[sel.provider == provider]
        trust = p.cost.sum() / p.activity.sum() if p.activity.sum() > 0 else None
        rows.append({
            "key": m["key"], "label": m["label"], "unit": m["unit"], "use": m["use"],
            "national": round(float(nat), 2), "national_remember": remember(nat),
            "national_activity": int(sel.activity.sum()),
            "national_activity_text": count(sel.activity.sum()),
            "trust": round(float(trust), 2) if trust else None,
            "trust_remember": remember(trust) if trust else None,
            "trust_activity": int(p.activity.sum()),
            "trust_activity_text": count(p.activity.sum()),
            "difference_pct": int(round((trust / nat - 1) * 100)) if trust else None,
        })
    return rows


def sanity(d, rows):
    problems = []
    if d.provider.nunique() < 100:
        problems.append(f"only {d.provider.nunique()} providers")
    for r in rows:
        if not 10 < r["national"] < 50000:
            problems.append(f"{r['key']} national cost {r['national']} looks wrong")
    if problems:
        sys.exit("Sanity check failed: " + "; ".join(problems))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="RJ1")
    ap.add_argument("--provider-name", default="Guy's and St Thomas'")
    args = ap.parse_args()

    year, doc = latest_publication()
    urls = file_urls(doc)
    ncci_url = pick(urls, r"NCCI")
    print("Edition", year, "\n ", ncci_url)

    z = read_zip(ncci_url)
    d, total_cost, trust_cost = department_costs(z)
    rows = unit_costs(d, args.provider)
    sanity(d, rows)
    ncci_total, ncci_areas = ncci(z, args.provider)

    data = {
        "edition": year,
        "costs_financial_year": year,
        "published": doc.get("date", "")[:10],
        "source_page": doc.get("link"),
        "source_files": [ncci_url],
        "dashboards": dashboards(doc),
        "provider_code": args.provider,
        "provider_name": args.provider_name,
        "providers_in_collection": int(d.provider.nunique()),
        "national_total_cost_bn": round(total_cost / 1e9, 1),
        "trust_total_cost_bn": round(trust_cost.get(args.provider, 0) / 1e9, 2),
        "ncci_total": ncci_total,
        "ncci_areas": ncci_areas,
        "unit_costs": rows,
    }

    today = dt.date.today().isoformat()
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    figures = lambda x: {k: v for k, v in x.items() if k not in ("last_checked", "last_updated")}
    changed = figures(old) != data
    data["last_updated"] = today if changed or "last_updated" not in old else old["last_updated"]
    data["last_checked"] = today
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("CHANGED" if changed else "UNCHANGED", "- edition", year)
    for r in rows:
        print(f"  {r['label']}: national £{r['national']:,.0f}, {args.provider} "
              f"£{(r['trust'] or 0):,.0f} ({r['difference_pct']:+}%)" if r["trust"] else r["label"])


if __name__ == "__main__":
    main()
