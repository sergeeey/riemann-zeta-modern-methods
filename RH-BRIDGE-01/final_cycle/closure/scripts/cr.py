"""Crossref bibliographic lookup: python cr.py "query" ...  -> top 3 per query (title, year, container, DOI, authors)"""

import json, sys, urllib.parse, urllib.request

for q in sys.argv[1:]:
    url = (
        "https://api.crossref.org/works?query.bibliographic="
        + urllib.parse.quote(q)
        + "&rows=3&select=title,DOI,issued,container-title,author,volume,page"
    )
    try:
        with urllib.request.urlopen(
            urllib.request.Request(
                url, headers={"User-Agent": "research-script (mailto:none@example.org)"}
            ),
            timeout=60,
        ) as r:
            d = json.load(r)
    except Exception as e:
        print(f"## {q}\n  ERROR {e}")
        continue
    print(f"## {q}")
    for it in d["message"]["items"]:
        au = ", ".join((a.get("family", "?")) for a in it.get("author", [])[:3])
        yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        print(
            f"  {yr} | {it.get('title', ['?'])[0][:110]} | {(it.get('container-title') or ['?'])[0]} {it.get('volume', '')} {it.get('page', '')} | {it['DOI']} | {au}"
        )
