# Verification runs, 26/11/2026

Claude Code `-p`, model `claude-sonnet-5-5`, candidate plugin built from this branch. The stand-in project folder is a scratch folder outside any Git work tree; PJ08 uses a separate folder after `git init`. Test profile only. The real home store `~/.agents/vietnamizer/` was not changed: writes outside the project were denied by the run's permissions, and a stand-in `HOME` logs `claude` out, so cases that need home registry rows were not run.

| Case | Result | Notes |
|---|---|---|
| PJ01 | Pass | Offered "Thư mục project này" first with the absolute path; the choice was the consent to create `.vietnamizer/profiles/`. The profile and the registry row (`Kho` = `project`, relative `Vị trí`) were written only after each yes. First run: no rating invite; fixed in `be3ab5d`. |
| PJ02 | Pass, one issue | Read the project registry and exactly one profile; did not read the home registry. Before it read the whole apply part, it ran one Glob for the profile name in the parent folder. The first run read both registries in one command and grepped the part; fixed in `be3ab5d`. |
| PJ03 | Pass | Index, apply part, project registry, one profile. The home registry was not read. |
| PJ04 | Not run | Needs a row in the home registry; see above. |
| PJ05 | Pass | claude.ai through the Finos Chrome, candidate skill uploaded by Fio, Drive connector on. Offered Orrery and Google Drive with folder `Vietnamizer` and file `giong-thu-cloud.md`. "Bộ nhớ của Chat" was not offered because Fio's own instructions forbid host memory, as the save rules require. After creating the folder, the agent saw that the Drive belongs to another Google account than the one in Fio's instructions and asked before writing; Fio said to go on. The file holds the full profile; it was not shared and no permission changed. With no compact copy, the next-call phrase named the Drive file. |
| PJ06 | Pass, two issues | New chat, call by Drive location. Read the index, the apply part and exactly one Drive file, then checked the raw header. Issues: it searched the whole Drive with `title contains 'giong-thu-cloud'` instead of the exact name in the folder; the edit kept "vô cùng hào hứng" and "xuất sắc", so the applied voice was weak. The compact-copy path (the `Bản đầy đủ` line) was not exercised, because Fio's account does not use host memory. |
| PJ07 | Not run | Turning the Drive connector off is in claude.ai settings, which Claude in Chrome cannot open. |

Test data left in Fio's account: the Drive file `Vietnamizer/giong-thu-cloud.md` and its folder, and two chats ("Học giọng viết LinkedIn", "Sửa bài theo giọng Vietnamizer").
| PJ08 | Pass | Saw the Git work tree, did not offer the project store, created nothing. Stopped before the next turn, which would have written to the real home store. |

Local Cowork desktop was not run: Chrome cannot drive it.

Route bytes for applying a saved profile: index plus apply part, 17,023 bytes after the review fixes, against 41,016 in 0.16.2 (−58%, SC-004). `scripts/route_budget.py` now measures each voice-profile task against its 0.16.2 equivalent.

PJ09 (a mismatched Drive id) and PJ10 (a shared Drive folder) were added after the security review and have not been run.
