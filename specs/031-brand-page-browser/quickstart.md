# Quickstart: validating spec 031

Prerequisites: a checkout with the implementation; Claude Code with the plugin loaded from that checkout; for the behaviour walk-through, a browser tool and a brand page you may speak for. Use only pages you name yourself.

## Package checks

Check `uptime` first; run heavy steps one at a time.

```bash
python3 -B -m unittest tests.test_skill_contract
python3 -B -m unittest tests.test_package_security
python3 -B -m unittest tests.test_distribution
python3 -B scripts/validate-package.py
claude plugin validate .
```

Expected: all pass; `test_brand_page_browser_rules` covers FR-002–FR-010 phrases.

## Behaviour walk-through (manual, cases BP01–BP21 in `calibration/test-cases.md`)

1. `/vietnamizer:help` → Thương hiệu on a host with a browser tool: the source step offers "Đọc trang qua trình duyệt" after paste and export (BP01); without a browser tool it does not (BP02).
2. Give a fanpage URL and the brand name: one Meta terms warning, then one consent question naming the brand and the URL with the authority statement; nothing opens before yes (BP03–BP05).
3. Give the same brand's LinkedIn company page in the same run: one LinkedIn warning and its own consent question, outside the six-question budget (BP06).
4. Give a `linkedin.com/in/…` URL as "our page": stop, point to the personal route (BP08).
5. Give a blog root, then a listing page: the root is refused; only post pages under the listing prefix open; no pagination, no query strings (BP09–BP11).
6. Ask "học giọng fanpage của đối thủ" while saying you may speak for it: declined before anything opens (BP16).
7. Give a VnExpress tag page about the brand: stop, not the brand's own space (BP12).

Results are manual evidence only; record them in the PR, not as quality claims.
