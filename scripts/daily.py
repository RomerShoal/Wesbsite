#!/usr/bin/env python3
"""Low-trust discovery feed for independent NESE websites.

Not a regulatory completeness guarantee. Official-page changes and press RSS items
are discovery leads requiring human review. Never infer legal deadlines from this feed.
"""
import datetime as dt, hashlib, json, pathlib, re, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
OUT = DATA / "daily.json"
STATE = DATA / "source_state.json"
now = dt.datetime.now(dt.timezone.utc)
existing = json.loads(STATE.read_text()) if STATE.exists() else {}
sources = {
    "NJDEP NESE": "https://dep.nj.gov/nese/",
    "Williams NESE application": "https://www.williams.com/nese-njdep-application/",
    "NJDEP bulletin": "https://dep.nj.gov/bulletin/",
    "NYSDEC notices": "https://dec.ny.gov/news/environmental-notice-bulletin",
    "USACE NY District": "https://www.nan.usace.army.mil/Missions/Regulatory/Regulatory-Public-Notices/",
}
req_headers = {"User-Agent": "NESEPublicResearchWatch/1.0 (public regulatory research)", "Accept": "text/html,application/rss+xml,*/*"}
def get(url):
    request = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(request, timeout=18) as response:
        return response.read(1_500_000).decode("utf-8", errors="replace")
items = []
availability = {}
for label, url in sources.items():
    try:
        content = get(url)
        text = re.sub(r"\s+", " ", re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.S|re.I))
        digest = hashlib.sha256(text.encode()).hexdigest()
        before = existing.get(url)
        if before and before != digest:
            items.append({"title": f"Official page content changed — {label}", "url":url, "date":now.date().isoformat(), "kind":"official-change","verification":"unverified"})
        existing[url] = digest
        availability[label] = "reachable"
    except Exception as e:
        availability[label] = "inaccessible: " + type(e).__name__

query = '(NESE OR "Northeast Supply Enhancement" OR "Raritan Bay Loop" OR Transco) (pipeline OR NJDEP OR FERC)'
rss = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=en-US&gl=US&ceid=US:en"
domains = {"nj.com","app.com","njspotlightnews.org","tworivertimes.com","northjersey.com","patch.com","newjerseymonitor.com","silive.com"}
try:
    tree = ET.fromstring(get(rss))
    for item in tree.findall("./channel/item"):
        title=(item.findtext("title") or "").strip()
        link=(item.findtext("link") or "").strip()
        published=(item.findtext("pubDate") or "").strip()
        if not title or not link: continue
        # RSS publisher may list an outlet after a hyphen; also retain relevant broader coverage.
        pub=(item.findtext("source") or "").lower()
        if any(d in pub for d in domains) or re.search(r"NESE|Raritan Bay Loop|Transco|Northeast Supply Enhancement",title,re.I):
            items.append({"title":title[:250],"url":link,"date":published,"kind":"press-lead","verification":"unverified"})
except Exception as e:
    availability["press-rss"] = "inaccessible: " + type(e).__name__
else:
    availability["press-rss"] = "reachable"

prior = json.loads(OUT.read_text()) if OUT.exists() else {}
seen_prior = {(i.get("kind"),i.get("url"),i.get("title")) for i in prior.get("items",[])}
unique = []
seen = set()
for item in items:
    key = (item["kind"],item["url"],item["title"])
    if key in seen or key in seen_prior: continue
    seen.add(key)
    unique.append(item)
report = {"checked_at":now.strftime("%Y-%m-%d %H:%M UTC"),"items":unique[:30],"source_access":availability,"evidence_policy":"Discovery signals are unverified; confirm original filings and dates."}
OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
STATE.write_text(json.dumps(existing,indent=2)+"\n")
print(json.dumps({"checked_at":report["checked_at"],"new_candidates":len(unique),"source_access":availability},indent=2))
