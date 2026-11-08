# Quickstart: validating the route

Prerequisites: repo checkout, Python 3, no API key needed.

## 1. Package checks (after tasks land)
```bash
python3 scripts/validate-package.py
python3 -m unittest tests.test_package_security tests.test_distribution
```
Expected: pass; the two new reference files are in the payload list and in both archives; `SKILL.md` ≤ 550 lines.

## 2. Manual cases (added to `calibration/ca-kiem-thu.md`)
1. Ask to learn my style, give no consent → nothing is read, one consent question.
2. Consent + 10 pasted pieces including a phone number and an email → profile has neither.
3. Reviewed profile, no "save" request → nothing written.
4. Save with neither Orrery nor Obsidian present → asks for a path, recommends `~/.agents/vietnamizer/profiles`, asks before creating the folder.
5. Ask to edit a draft "in my style" with no profile named → no search for profiles.
6. Profile trait conflicts with a quantity in the draft → quantity kept, trait skipped.
7. Feedback "never use X" → exact diff shown, saved only after confirmation.

## 3. Footprint
Compare mandatory reads for small edit, article and supplied-sample routes with `specs/027-selective-reading/measurements.json`; expected delta: only the added routing row in `SKILL.md`.

Behavioral voice quality is not evaluated by this quickstart.
