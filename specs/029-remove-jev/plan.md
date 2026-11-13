# Plan: Remove Jev

Path: Spec Kit, tasks path (cross-cutting: package, tests, docs, constitution), DEEP/contract.

Order (each step is one atomic commit; the tree validates at each step where feasible):
1. Spec 029 (this folder).
2. Remove `jev/`, `references/typesafe-advisor.md`, registry generator, Jev tests and Jev-only benchmarks/eval; fix `validate-package.py`, `package-skill.sh`, `package-plugin.py`, `tests/test_distribution.py`, `tests/test_package_security.py`.
3. SKILL.md evaluator section, `.plugin-skills`, references mentions, agents/openai.yaml, plugin manifests text.
4. Docs: README, PRIVACY, AGENTS, CONTRIBUTING, SECURITY, TERMS, docs/*, constitution V, historical notes.
5. Changelog and version (MINOR) per `versioning`.

Proof: `python3 scripts/validate-package.py`, build the three archives, targeted tests of changed code and traced consumers (voice tests, structure tests that did not depend on jev), grep for `jev|typesafe|TYPESAFE_API_KEY` outside history. Reviews: posted code + security review before any PR.
