"""Query Cala's knowledge search once per biography chapter and cache the answers.

Usage: python3 scripts/cala.py <drug_id> [brand] [--only key,key]
  python3 scripts/cala.py palbociclib Ibrance              # any drug: the CORE questions
  python3 scripts/cala.py trastuzumab_deruxtecan --only subtypes

Every drug is asked the CORE questions. Drugs listed in DRUGS add their own
questions, and one with the same key as a CORE question replaces it.
Responses are cached to data/raw/<drug>/<chapter>.json and never re-fetched
(delete a file to re-run that query). A review table of every claim and its
sources is written to data/claims_<drug>.md.
"""

import argparse
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
API = "https://api.cala.ai/v1/knowledge/search"

# One question per story beat (see CLAUDE.md). {drug} becomes "Brand (generic)".
# Keep each one simple: Cala answers "too complex" to compound questions.
CORE = {
    "origin": "How was {drug} discovered, and who developed it?",
    "problem": "What problem in treating breast cancer was {drug} designed to solve, and how does it work?",
    "near_death": "What setbacks or failures did {drug} face before it was approved?",
    "pivotal_trial": "What did the pivotal trial behind the first FDA approval of {drug} for breast cancer show?",
    "approval": "When did the FDA first approve {drug} for breast cancer?",
    # Decides the drug's rows on the Landscape (drugs.json "subtypes" and "subtype_approvals").
    "subtypes": "Which breast cancer subtypes (HR-positive, HER2-positive, HER2-low, triple-negative) is {drug} FDA-approved to treat, and when was each approved?",
    "later": "What later FDA approvals for breast cancer has {drug} received?",
    "today": "Where does {drug} stand today: generics or biosimilars, new forms, or new trials?",
}

DRUGS = {
    "trastuzumab": {
        "generic": "trastuzumab",
        "brand": "Herceptin",
        "extra": {
            "origin": "How was Herceptin (trastuzumab) discovered? What role did Dennis Slamon, Axel Ullrich and Genentech play in the 1980s HER2/neu research?",
            "problem": "Why was HER2-positive breast cancer considered especially aggressive before Herceptin, and why did the mouse antibody behind trastuzumab need to be humanized before it could be used in patients?",
            "near_death": "Did Genentech consider abandoning the Herceptin (trastuzumab) program during development?", # too complex for Cala
            "funding": "Who funded Dennis Slamon's HER2 breast cancer research at UCLA?",
            "advocates": "What role did breast cancer patient advocates play in the development of Herceptin?",
            "pivotal_trial": "What did the pivotal phase 3 trial of trastuzumab plus chemotherapy in HER2-positive metastatic breast cancer show? How many patients, what survival benefit, and what heart side effects were found?",
            "approval": "When did the FDA first approve trastuzumab (Herceptin) for breast cancer?",
            "adjuvant": "What did the adjuvant trastuzumab trials (HERA, NSABP B-31, NCCTG N9831) show for early-stage HER2-positive breast cancer, and when did the FDA approve Herceptin for early-stage disease?",
            "biosimilars": "When did the FDA approve the first trastuzumab biosimilar?",
            "subcutaneous": "What is Herceptin Hylecta and when was it approved?",
            "successors": "Which newer HER2-targeted breast cancer drugs built on trastuzumab?", # too complex for Cala
        },
    },
    "trastuzumab_deruxtecan": {
        "generic": "trastuzumab deruxtecan",
        "brand": "Enhertu",
        "extra": {
            "origin": "Who developed trastuzumab deruxtecan (Enhertu), and how is it built from the trastuzumab antibody?",
            "kadcyla": "How is trastuzumab deruxtecan (Enhertu) different from trastuzumab emtansine (Kadcyla)?",
            "deal": "What was the 2019 deal between AstraZeneca and Daiichi Sankyo for trastuzumab deruxtecan?",
            "approval": "When did the FDA first approve Enhertu (trastuzumab deruxtecan) for breast cancer?",
            "destiny_breast03": "What did the DESTINY-Breast03 trial show comparing trastuzumab deruxtecan with trastuzumab emtansine?",
            "her2_low": "What did the DESTINY-Breast04 trial show in HER2-low breast cancer, and when did the FDA approve Enhertu for HER2-low disease?",
            "lung": "What is the risk of interstitial lung disease with trastuzumab deruxtecan?",
            "tumor_agnostic": "When did the FDA approve trastuzumab deruxtecan for HER2-positive solid tumors of any type?",
            "ultralow": "What did the DESTINY-Breast06 trial show, and when did the FDA approve Enhertu for HER2-ultralow breast cancer?",
            "latest": "What are the latest results for trastuzumab deruxtecan in early-stage HER2-positive breast cancer, such as DESTINY-Breast05, DESTINY-Breast09 or DESTINY-Breast11?",
        },
    },
}


def questions_for(drug, brand=None):
    """The drug's own questions in its story order, then any CORE ones it doesn't replace."""
    info = DRUGS.get(drug, {})
    generic = info.get("generic", drug.replace("_", " "))
    brand = brand or info.get("brand")
    name = f"{brand} ({generic})" if brand else generic
    queries = dict(info.get("extra", {}))
    for chapter, question in CORE.items():
        queries.setdefault(chapter, question.format(drug=name))
    return queries


def load_key():
    key = os.environ.get("CALA_API_KEY")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("CALA_API_KEY="):
                key = line.split("=", 1)[1].strip().strip("\"'")
    if not key:
        sys.exit("CALA_API_KEY missing: add it to .env")
    return key


def search(key, question):
    req = urllib.request.Request(
        API,
        data=json.dumps({"input": question}).encode(),
        headers={"X-API-KEY": key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.load(resp)


def fetch(key, drug, chapter, question):
    path = RAW / drug / f"{chapter}.json"
    if path.exists():
        return chapter, "cached"
    try:
        data = search(key, question)
    except Exception as e:  # keep going; one failed chapter shouldn't stop the rest
        return chapter, f"FAILED: {e}"
    if not data.get("explainability"):  # e.g. "too complex"; don't cache, rephrase the query
        return chapter, f"EMPTY: {data.get('content', '')[:80]}"
    data["_query"] = question
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return chapter, "fetched"


def sources_by_id(data):
    out = {}
    for ctx in data.get("context", []):
        out[ctx["id"]] = [
            (o["document"].get("name") or o["source"].get("name"), o["document"].get("url"))
            for o in ctx.get("origins", [])
        ]
    return out


def write_review(drug, chapters):
    lines = [f"# Claims for {drug}", "", "Generated by scripts/cala.py from cached Cala responses. Pick claims for chapters; prefer strong sources.", ""]
    for chapter in chapters:
        path = RAW / drug / f"{chapter}.json"
        if not path.exists():
            lines += [f"## {chapter}", "", "_No response (see gaps.md)._", ""]
            continue
        data = json.loads(path.read_text())
        srcs = sources_by_id(data)
        lines += [f"## {chapter}", ""]
        for i, claim in enumerate(data.get("explainability", []), 1):
            lines.append(f"{i}. {claim['content']}")
            seen = set()
            for ref in claim.get("references", []):
                for name, url in srcs.get(ref, []):
                    if url and url not in seen:
                        seen.add(url)
                        lines.append(f"   - [{urlparse(url).netloc}]({url}) {name}")
        lines.append("")
    out = ROOT / "data" / f"claims_{drug}.md"
    out.write_text("\n".join(lines))
    return out


def main():
    ap = argparse.ArgumentParser(description="Ask Cala one question per biography chapter for a drug.")
    ap.add_argument("drug", nargs="?", default="trastuzumab", help="drug id, e.g. palbociclib")
    ap.add_argument("brand", nargs="?", help="brand name for a drug not in DRUGS, e.g. Ibrance")
    ap.add_argument("--only", help="comma-separated chapters to ask, e.g. subtypes")
    args = ap.parse_args()

    queries = questions_for(args.drug, args.brand)
    asked = queries
    if args.only:
        wanted = args.only.split(",")
        unknown = [c for c in wanted if c not in queries]
        if unknown:
            sys.exit(f"unknown chapter(s) {', '.join(unknown)}; choose from: {', '.join(queries)}")
        asked = {c: queries[c] for c in wanted}

    key = load_key()
    (RAW / args.drug).mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        for chapter, status in pool.map(lambda kv: fetch(key, args.drug, *kv), asked.items()):
            print(f"{chapter:16} {status}")
    # Review every chapter that has an answer, plus any asked this run that came back empty.
    shown = [c for c in queries if c in asked or (RAW / args.drug / f"{c}.json").exists()]
    print("review table:", write_review(args.drug, shown))


if __name__ == "__main__":
    main()
