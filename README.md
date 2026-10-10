# Drug Biographies

Sourced, illustrated stories of breast cancer drugs, plus a timeline of drugs approved and in clinical trials.

Built at the Creative Data Hackathon, October 2026.

## Setup

1. Clone the repo.
2. Add your API key to a `.env` file:
   ```
   CALA_API_KEY=your-key-here
   ```
3. Serve the folder locally and open it in a browser:
   ```bash
   python3 -m http.server 8000
   ```
   Open `localhost:8000` for the Landscape, or `localhost:8000/biography.html?drug=trastuzumab` for a biography. The pages load JSON files, so open them through the server, not by double-clicking.

## Add a drug

There is no build step. `biography.html` reads `biographies/<id>.json` when it opens, and `index.html` reads `drugs.json`. To add a drug, for example palbociclib (Ibrance):

1. **Ask Cala.** This asks one question per chapter (origin, setbacks, pivotal trial, approval, subtypes, later approvals, today) and saves each answer with its sources:
   ```bash
   python3 scripts/cala.py palbociclib Ibrance
   ```
   Answers go to `data/raw/palbociclib/<chapter>.json`, and a table of every claim and its source goes to `data/claims_palbociclib.md`. To ask one question again, delete its file and run with `--only <chapter>`. For hand-tuned questions, add the drug to `DRUGS` in `scripts/cala.py`.
2. **Write the biography.** Create `biographies/palbociclib.json` from the claims, following `biographies/trastuzumab.json`. Each chapter has a date, title, one-line summary, body paragraphs, a headline stat and a source. Use only claims with a source. Log anything you leave out in `data/gaps.md`.
3. **Add images (optional).** Put a Krea hero image at `assets/palbociclib/hero.jpg`, and chapter images at `assets/palbociclib/<chapter-id>.jpg`. Chapters without an image get a plate drawn in code. Set `"scene"` on a chapter to pick one (`aggressive`, `abandoned`, `patron`, `patients`, `approval`, `early`, `biosimilar`, `hylecta`, `family`).
4. **Put it on the Landscape.** Add a row to `drugs.json`, and copy it into the `inline-drugs` block in `index.html`, which the page uses when it can't load `drugs.json`. Add `"builds_on": ["<id>"]` to draw a link to a related drug.
5. **Link chapters across drugs (optional).** Add `"link": {"drug": "<id>", "label": "Read …'s biography"}` to a chapter.

## Reproducibility

- **Facts:** Cala writes each answer fresh, so asking the same question again can give different wording or claims. Every answer used here is saved in `data/raw/` and never fetched again, so the pages always rebuild from the same data.
- **Pages:** the biography JSON files hold exactly what is shown. Plates drawn in code use fixed seeds and look the same on every load.
- **Images:** Krea images can't be regenerated exactly. The ones used are saved in `assets/`.

## Disclaimer

For learning only. Not medical advice.