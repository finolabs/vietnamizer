# Quickstart: verify spec 039

1. **Contract tests:** run `python3 -m unittest tests.test_skill_contract`, plus `python3 scripts/route_budget.py`.
2. **Project store on Claude Code:**
   - Create a stand-in project folder outside any Git work tree.
   - Start `claude` there with the candidate plugin.
   - Run PJ01–PJ04: save; call by name in a new session; call with "theo giọng của tôi"; the creation question.
   - Check the files in `.vietnamizer/`.
3. **Cloud through Chrome (Finos)** on claude.ai, with test profiles only:
   - With the Drive connector on: PJ05–PJ06 (save to Drive; call back in a new chat).
   - With Drive off: PJ07 (the 0.16.2 compact flow).
   - Check the Drive file by name only.
4. **Guard:** PJ08, a project folder inside a Git work tree, where nothing is written.
5. **Report:** per case, pass or fail, the files written and read, and what was not run (local Cowork desktop).
