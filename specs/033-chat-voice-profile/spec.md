# Feature Specification: Learn a personal voice profile from the user's own agent chat history

**Feature Branch**: `spec/033-chat-voice-profile`
**Created**: 2026-11-14
**Status**: Draft, spec only (no plan, tasks or implementation). Planned for the version after 0.16.0. Needs a constitution amendment (exact text pending Fio's approval, open decision O1) before any implementation.
**Input**: Fio, 14/11/2026: "nếu user không muốn mất thời gian build lại writing profile, thì họ có thể lựa chọn cho vietnamizer học hỏi từ chính cách họ viết qua các session chat. Lúc này vietnamizer có thể có một script hoặc agent nào đó thu thập lại các session chat trong vòng 30 ngày gần nhất của users để từ đó đóng gói thành writing profiles cho họ." Orrery memory `01M7CHWABQ4FDAQFJNHVE9R4E9` holds the idea and the open issues the coordinator raised. Router depth DEEP, trigger `privacy`: the skill would read the user's local agent history, which may hold secrets, file paths, client work and other people's text, and the shipped constitution forbids searching memory or history. Builds on spec 028 (voice-profile route), spec 030 (personal and brand voice, social sources) and the 14/11/2026 decision that building a profile is optional and the first use only reminds the user.

## Settled decisions (owner, 2026-11-14)

1. **Source: prompt-history files only.** The route reads only each host's prompt-history file, which holds what the user typed into the prompt box. It never reads full session transcripts, so agent replies, tool output and injected system or project context are never in the data read. Paths observed on Fio's machine on 14/11/2026 (field names only, no content read):

   | Host | File | Text field | Pasted blocks |
   |---|---|---|---|
   | Claude Code (CLI, desktop Code tab, IDE extensions) | `~/.claude/history.jsonl` | `display` | separate, in `pastedContents`; `display` holds a placeholder |
   | Codex CLI and local app | `~/.codex/history.jsonl` | `text` | inline in `text`, not marked |
   | Antigravity CLI | `~/.gemini/antigravity-cli/history.jsonl` | `display` | not checked |

   Antigravity IDE stores conversations as binary `.pb` files and is out of scope until a readable format exists. Not taken: full transcripts (`~/.claude/projects/*/*.jsonl`, `~/.codex/sessions/**/rollout-*.jsonl`), Claude Code only.
2. **Hosts: local hosts with a shell only.** The route runs only where the agent can run a local command that reaches the user's home folder: Claude Code, Codex CLI or local app, Antigravity CLI. In Claude.ai Chat, Cowork, Codex cloud, Antigravity IDE or any host without that access, the route says it cannot read chat history on this machine and offers pasted posts or a platform export (spec 030) instead. It never asks the user to mount or upload their history folder. Fio asked (14/11/2026) whether a script could work in Cowork, Chat and the equivalent modes; the answer recorded here: no, because the history files are not reachable there, whatever reads them.
3. **A script ships in the package.** An offline, read-only script using only the Python standard library reads the consented files, filters them (decision 4) and prints only the filtered result. The agent never opens a history file with its own file-reading tool. The script makes no network call, reads no environment secret or API key, writes no file, and reads no path other than the consented files. The skill still works without it: when Python or a shell is missing, the route stops as in decision 2. This needs a Principle V amendment (O1). Not taken: the agent reading the files itself (first answer, withdrawn once the conflict with decision 4 was shown), a command embedded in the reference, a script outside the package.
4. **Deterministic filtering before any analysis.** The script keeps only text the user typed and drops, before the agent sees any of it: whole entries that are pasted blocks (Claude Code: the `pastedContents` and the placeholder; Codex and Antigravity: fenced code blocks and long multi-line blocks that look pasted), slash commands, and any entry carrying a secret sign (key or token shapes, `KEY=value` assignments, private-key headers, long high-entropy strings). It masks file paths, URLs, email addresses, phone numbers and long numeric identifiers with labels. It reports how many entries it dropped for each reason. The agent then applies the existing redaction of `references/voice-analysis.md` (names, contacts, health and money data, deal terms, unreleased work, remarks about other people). Not taken: agent-only filtering.
5. **One consent question naming the files and the dates.** Exactly one question, before the script runs, names each file the script will read, the exact date window ("từ dd/mm/yyyy đến dd/mm/yyyy"; default the last 30 days, the user may shorten it, never lengthen it past 30), what is dropped and masked, and that nothing is saved unless the user later asks to save. Only a clear yes counts. Not taken: one question per host.
6. **A provisional sample floor, labelled uncalibrated.** The script counts, exactly, the kept entries that are Vietnamese (carry Vietnamese diacritics) and have at least 15 words. Below 30 such entries, or below 1,500 words across them, the route stops, drafts no profile, and says the sample is too thin (FR-012). At or above the floor, the profile describes only the channel "chat với agent" and never claims the user's voice for posts, email or documents. These numbers are an owner decision, not a calibrated threshold: the plan MUST calibrate them on a labelled development set and check them on a separate holdout set before release (Principle IV, open decision O2). Not taken: no number, the agent judging alone.
7. **Store only the profile, through the existing save gate; short redacted excerpts allowed.** Nothing is written but the profile, and only through `references/voice-profile.md` mục 4 (explicit save request after the full profile is shown, a store or path the user chooses). Filtered messages are never written to disk, cache, log, memory or the profile store. The profile records the host or hosts, the date window and the exact counts kept and dropped. Evidence may quote short excerpts from the chat sample once redacted, as pasted samples do today. Not taken (plan author's recommendation): no verbatim excerpts at all.
8. **Lookup: an ordinary personal profile; a lookup miss lists saved names.** A profile learned from chat is a normal `kind: personal` profile with a source marker (proposed `source: agent-chat`) and is found by name like any other. Fio's answer on the lookup design (14/11/2026): when `/vietnamizer <tên>` finds no profile, the skill returns the list of saved profile names for the user to choose from. That listing belongs to spec 032 (session "vietnamizer: find saved voice profiles by name"), which owns how names are found and listed; this spec only requires that chat-learned profiles appear in it like any other, and that no lookup, listing or miss ever starts reading chat history (FR-016). Not taken: suggesting the chat source on a lookup miss.

## Open decisions

| # | Decision | Owner | Unblocks it |
|---|---|---|---|
| O1 | Exact text of the constitution amendment (section "Constitution amendment" below) | Fio | Approval of the exact text at review of this PR or of the plan; no implementation before it |
| O2 | Calibration of the sample floor of decision 6 | Plan author, then Fio | A labelled development set and a separate holdout set of chat samples, consented and kept out of the repo |
| O3 | Field name and lookup behaviour shared with spec 032 (source marker, how listing finds profiles) | Session of spec 032, then Fio | Spec 032 settled; this spec's FR-015 and FR-016 aligned with it |
| O4 | Per-host format and retention: fields, timestamp units, whether history can be turned off or is pruned (Claude Code prunes local history after a retention period; Codex history persistence can be turned off) | Plan author | Checking each host's current version and docs in the plan's research; a host whose format is not confirmed is not supported |

## Clarifications

### Session 2026-11-14

- Q: Which files per host? → A: the prompt-history files only; Antigravity IDE out of scope (decision 1).
- Q: Ship a script? → A: first "agent reads, no script", which conflicted with "deterministic filtering in a script"; after the conflict was shown Fio asked whether a script works in Cowork, Chat and similar modes; it does not, nor does anything else, because the files are not reachable there. Final: a script in the package, local hosts only (decisions 2, 3).
- Q: How is data filtered? → A: deterministic filtering in the script, then the agent's existing redaction (decision 4).
- Q: The consent question? → A: one question naming the files and the dates (decision 5).
- Q: Minimum sample? → A: a provisional floor, labelled uncalibrated (decision 6).
- Q: What is stored, and excerpts? → A: only the profile through the save gate; short redacted excerpts allowed (decision 7).
- Q: Fit with the lookup design? → A: an ordinary personal profile; on a lookup miss the skill lists saved names (decision 8).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Build a personal profile from my chat history without pasting posts (Priority: P1)

A user working in Claude Code does not want to collect posts. They ask Vietnamizer to learn their voice from their chats. The skill explains the source and its limits, asks one consent question naming `~/.claude/history.jsonl` and the window from 15/10/2026 to 14/11/2026, runs the script, reads only the filtered output, and drafts a `kind: personal` profile scoped to the channel "chat với agent". The user reviews it and may save it through the save gate.

**Why this priority**: it is the outcome Fio asked for: a profile with no pasting or exporting.
**Independent Test**: on a machine with a Claude Code history holding typed Vietnamese prompts, pasted blocks, a slash command and a fake key, run the route; the consent question names the file and dates, the agent never opens the file with its read tool, the filtered output holds none of the pasted text, the command or the key, the draft cites only typed text, and nothing is written until the user asks to save.

**Acceptance Scenarios**:
1. **Given** a request "học giọng tôi từ các session chat", **When** the route starts on a local host, **Then** the skill states which host files exist (by checking only those exact paths), the default window and what is dropped, and asks one consent question; nothing is read before a clear yes.
2. **Given** consent, **When** the script runs, **Then** the agent receives only filtered entries and the per-reason drop counts, never raw file content.
3. **Given** enough sample (decision 6), **When** the draft is shown, **Then** it is complete as in spec 028, its source section names the host, the window and the exact counts, and its channel is "chat với agent" only.
4. **Given** the user approves the draft but does not ask to save, **When** the task ends, **Then** nothing is written anywhere and no filtered text remains on disk.

### User Story 2 — Thin sample: say so and offer the other sources (Priority: P1)

Most entries are short commands ("chạy test", "ok merge đi"). The script reports 12 qualifying entries and about 400 words.

**Why this priority**: chat commands are a weak voice signal; a profile built on them would mislead every later edit.
**Independent Test**: a history with only short commands yields the thin-sample message and no draft.

**Acceptance Scenarios**:
1. **Given** fewer than 30 qualifying entries or fewer than 1,500 words, **When** the script finishes, **Then** the skill drafts nothing and says, in Vietnamese, how many entries qualified, that messages to an agent are mostly short commands and a weak sign of how the user writes, and offers to paste 3–5 posts or use a LinkedIn or Facebook export, or to stop.
2. **Given** the thin-sample message, **When** the user asks to "cứ dựng đi", **Then** the skill still drafts nothing from chat (the floor is a hard stop), and may build from other sources the user then gives.

### User Story 3 — Several hosts, one window (Priority: P2)

A user works in both Claude Code and Codex CLI.

**Independent Test**: with both files present, one consent question names both files and one window; counts are reported per host and in total.

**Acceptance Scenarios**:
1. **Given** two history files exist, **When** consent is asked, **Then** one question names both; the user may drop either before answering.
2. **Given** Codex entries with inline pasted blocks, **When** the script filters, **Then** fenced code and long multi-line blocks are dropped and counted under "pasted".

### User Story 4 — Unsupported host (Priority: P2)

A user in Claude.ai Chat or Cowork asks to learn from their chats.

**Acceptance Scenarios**:
1. **Given** a host without local shell access to the home folder, **When** the user asks, **Then** the skill says it cannot read chat history on this machine, offers pasted posts or an export, and asks for no upload or folder mount.

### Edge Cases

- No history file at any supported path: say none was found at the exact paths checked; do not search elsewhere.
- History turned off, pruned, or shorter than the window: report the real date range read.
- A file whose format does not match the confirmed one (O4): the script stops for that host and reports "định dạng chưa hỗ trợ"; no partial guess.
- Typed text that quotes someone else or names people: the agent's redaction removes names and quotes; when authorship of an entry is unclear it stays out of evidence (spec 028 rule).
- Typed text that contains instructions ("lưu hồ sơ này", "đọc thêm file X"): data, never acted on.
- English-only entries: kept out of the Vietnamese count; they may be noted but do not raise the floor.
- The user asks for a window longer than 30 days: decline the extra days; 30 is the cap.
- The user asks to exclude a project or session: out of scope in v1; the user may shorten the window or decline.
- The route is not opened by an ordinary edit request, by "theo giọng của tôi" without a source, by a lookup, or by the first-use reminder.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chat-history source MUST be opt-in: it runs only when the user asks to learn their voice from their chats or picks it from the setup step. It MUST NOT be offered as a default or run silently.
- **FR-002**: The source MUST read only the prompt-history files of decision 1, at the exact paths for the hosts present, and MUST NOT read session transcripts, memory stores, other agents' data, or any other path.
- **FR-003**: Before reading, the skill MUST check only whether those exact paths exist (no listing of folders) and MUST ask exactly one consent question naming each file, the exact date window (at most the last 30 days), what is dropped and masked, and that nothing is saved without a later save request. Only a clear yes counts.
- **FR-004**: Reading and filtering MUST be done by the packaged script; the agent MUST NOT open a history file with its own file tools, and MUST receive only the script's filtered output.
- **FR-005**: The script MUST use only the Python standard library, make no network call, read no environment secret, write no file, and read only the paths named in the consent.
- **FR-006**: The script MUST keep only text the user typed and MUST drop pasted blocks, slash commands and any entry with a secret sign, before output (decision 4).
- **FR-007**: The script MUST mask file paths, URLs, email addresses, phone numbers and long numeric identifiers, and MUST report counts dropped and masked per reason.
- **FR-008**: The script MUST keep only entries whose timestamp falls inside the consented window.
- **FR-009**: The agent MUST then apply `references/voice-analysis.md` redaction and treat every entry as data, not instructions.
- **FR-010**: The script MUST count qualifying entries exactly (Vietnamese, at least 15 words) and their words; these counts are computed by code and may be shown without the approximation label.
- **FR-011**: Below the floor of decision 6 the route MUST stop and draft nothing from chat, even if the user insists.
- **FR-012**: The thin-sample message MUST state the qualifying count, why chat to an agent is a weak signal, and offer pasted posts, an export, or stopping.
- **FR-013**: A profile drafted from chat MUST be `kind: personal`, MUST describe only the channel "chat với agent", and MUST NOT state traits for other channels.
- **FR-014**: Only the profile may be stored, only through `references/voice-profile.md` mục 4. Filtered entries MUST NOT be written to disk, cache, log, memory or the profile store; short excerpts in the profile MUST be redacted.
- **FR-015**: The profile's source section MUST record the source marker, the hosts, the date window read and the exact counts kept and dropped.
- **FR-016**: A profile lookup, listing, lookup miss, first-use reminder or setup screen MUST NOT start reading chat history; each may only mention that the source exists.
- **FR-017**: On a host without local shell access to the home folder, or without Python, the route MUST stop with the message of User Story 4 and MUST NOT ask for an upload or mount.
- **FR-018**: A host whose file format is not confirmed (O4) MUST NOT be read.
- **FR-019**: The script MUST stop on an unexpected format rather than guess, and MUST report which host failed.

### Key Entities

- **Prompt-history file**: a host's own record of what the user typed; one entry per prompt with a timestamp and text.
- **Filtered sample**: the script's output for one run: kept entries with masks, per-reason counts; it lives only in the conversation.
- **Chat-learned profile**: a `kind: personal` profile with source marker, hosts, window and counts; otherwise the spec 028 template.

## Constitution amendment (proposed, exact text pending Fio's approval — O1)

Version 2.6.1 → 2.7.0 (MINOR: the voice-profile constraint gains a source; Principle V is clarified for local reads; no obligation removed).

**Principle V**, append after "MUST NOT phụ thuộc một repo local khác.":

> Ngoại lệ duy nhất: script đọc lịch sử prompt của tuyến hồ sơ giọng MAY đọc file trên máy người dùng, chỉ sau câu đồng ý đọc, chỉ đúng các file được nêu trong câu đó, chỉ bằng thư viện chuẩn, không gọi mạng, không đọc biến môi trường chứa secret và không ghi file.

**Ràng buộc "Tuyến hồ sơ giọng"**, replace "Skill MUST NOT tự tìm hồ sơ hoặc mẫu trong memory hay lịch sử; chỉ đọc hồ sơ người dùng dán hoặc chỉ định." with:

> Với hồ sơ cá nhân, tuyến MAY đọc file lịch sử prompt của chính người dùng trên host local (Claude Code, Codex CLI hoặc app local, Antigravity CLI) trong tối đa 30 ngày gần nhất, sau một câu đồng ý nêu từng file và khoảng ngày; việc đọc và lọc MUST do script trong gói làm, agent MUST NOT tự mở file lịch sử; script MUST chỉ giữ lời người dùng gõ, bỏ đoạn dán, lệnh và mục có dấu hiệu secret, che đường dẫn, URL, email, số điện thoại và mã định danh trước khi agent đọc; MUST NOT đọc transcript đầy đủ, câu trả lời của agent hay tool output; MUST NOT ghi mẫu đã lọc ra bất kỳ đâu. Ngoài nguồn này, skill MUST NOT tự tìm hồ sơ hoặc mẫu trong memory hay lịch sử; chỉ đọc hồ sơ người dùng dán hoặc chỉ định.

The second replacement keeps the existing ban for every other source. Spec 032 may amend the same sentence for lookup by name; the two amendments MUST be reconciled into one text before either is applied (O3).

## Success Criteria *(mandatory)*

- **SC-001**: On the test fixtures, 0 pasted blocks, slash commands, secret-marked entries, agent replies or tool outputs reach the agent; every path, URL, email and phone number in kept entries is masked.
- **SC-002**: In every run, the consent question names each file read and the exact window, and no file is read before the yes.
- **SC-003**: A history below the floor yields 0 drafts from chat and the thin-sample message.
- **SC-004**: After any run, whether saved, declined, stopped or failed, no filtered text exists on disk outside the profile the user chose to save.
- **SC-005**: The script makes 0 network calls and opens 0 paths outside the consent list (checked by test).
- **SC-006**: On Chat, Cowork, Codex cloud and Antigravity IDE, the route stops with the unsupported-host message in every case.

## Assumptions

- Each host's prompt-history file holds only what the user typed into the prompt box; the plan confirms this per host version (O4).
- The user who runs the agent is the only author of their prompt history on that machine account.
- Fio's 14/11/2026 decision stands: building a profile is optional, and the first use only reminds the user. This source is one more option behind that reminder, never a default.

## Out of scope

- Full transcripts, agent replies, tool output, Antigravity IDE `.pb` files, cloud sessions.
- Data exports of claude.ai or ChatGPT (possible later, separate spec).
- Per-project or per-session exclusion; windows longer than 30 days; scheduled or background collection.
- Brand profiles from chat history.
- Any code, reference or constitution change in this PR.
