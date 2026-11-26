# Research: Voice profiles on Cowork and cloud hosts

Sources are Anthropic help and docs pages fetched 26/11/2026 by a research subagent. Every claim has a URL in the session record. These are the findings that shape the plan:

## R1. Local Cowork keeps files in attached folders

- Claude reads and writes only files in the folders the user connected. A Cowork project holds local folders and a project memory store. Files Claude creates land in the project's folders.
- Projects stay on the computer and are not synced. Archiving deletes the project's memory, not the folders.
- **Decision:** treat a session with an attached, writable folder as a file host, and offer `.vietnamizer/` there (Fio: hidden folder). Do not write Cowork's own project memory: that is the host's store, not ours.

## R2. Cloud Cowork and Chat

- Cloud Cowork keeps only the files it delivers. It shares account memory with Chat.
- claude.ai Projects have per-project memory.
- Project knowledge is added by the user by hand. Nothing documents Claude writing to it.
- **Decision:** keep the 0.16.2 compact memory copy, and add a full copy in Drive when the connector is visible.

## R3. The Google Drive connector

- The connector can search, read and create files. By default it asks for approval on each action. Team and Enterprise owners must enable it.
- **Decision:** offer Drive only when the agent sees Drive create and read tools. Write one file per profile in a `Vietnamizer` folder. Name the file in the compact copy so the next call reads exactly that file.

## R4. Claude Code cloud sessions

- Each session is a fresh VM. Only the repository persists, through a commit.
- **Decision:** out of scope. The 0.16.2 rule (no registry inside a Git work tree) already keeps profiles out of repositories.

## R5. Agent Skills spec

- The spec has no storage feature.
- **Decision:** stores stay host features that the skill uses through the tools it sees, so no Principle V change.

## R6. The voice-profile reference split

- The file is 41,016 bytes, and the voice-profile route measures 82 KB (spec 038 budget).
- **Decision:** a short index plus parts by task: learn and consent; draft and present; save and the registry, including the project and Drive stores; apply and call, including the Chat compact copy; update, rate and A/B; and the reminder.
- Apply reads the index and the apply part only.
