# Verification runs, 26/11/2026

Claude Code `-p`, model `claude-sonnet-5-5`, candidate plugin built from this branch. The stand-in project folder is a scratch folder outside any Git work tree; PJ08 uses a separate folder after `git init`. Test profile only. The real home store `~/.agents/vietnamizer/` was not changed: writes outside the project were denied by the run's permissions, and a stand-in `HOME` logs `claude` out, so cases that need home registry rows were not run.

| Case | Result | Notes |
|---|---|---|
| PJ01 | Pass | Offered "Thư mục project này" first with the absolute path; the choice was the consent to create `.vietnamizer/profiles/`. The profile and the registry row (`Kho` = `project`, relative `Vị trí`) were written only after each yes. First run: no rating invite; fixed in `be3ab5d`. |
| PJ02 | Pass, one issue | Read the project registry and exactly one profile; did not read the home registry. Before it read the whole apply part, it ran one Glob for the profile name in the parent folder. The first run read both registries in one command and grepped the part; fixed in `be3ab5d`. |
| PJ03 | Pass | Index, apply part, project registry, one profile. The home registry was not read. |
| PJ04 | Not run | Needs a row in the home registry; see above. |
| PJ05–PJ07 | Not run | The Finos Chrome was not connected to the session, and claude.ai needs the candidate skill uploaded to the account first. |
| PJ08 | Pass | Saw the Git work tree, did not offer the project store, created nothing. Stopped before the next turn, which would have written to the real home store. |

Local Cowork desktop was not run: Chrome cannot drive it.

Route bytes for applying a saved profile: index plus apply part, 16,341 bytes, against 41,016 in 0.16.2 (−60%, SC-004).
