# Feature Specification: Voice profiles on Cowork and cloud hosts

**Feature Branch**: `spec/039-cloud-voice-profiles`

**Created**: 2026-11-26

**Status**: Draft

**Input**: Fio, 26/11/2026, "Làm spec 039". This is the second direction he named for the next version: manage and use each user's writing voice better on Claude Cowork and cloud hosts, with no local scripts. Spec 038 deferred the split of `references/voice-profile.md` to this spec.

## Clarifications

### Session 2026-11-26

- Q: Which hosts are in scope? → A: Both (Fio: "Cả hai"). Local Cowork with an attached project folder saves full profiles and the registry in that folder. Cloud Cowork and claude.ai Chat keep the compact memory copy and add an optional full copy in Google Drive when that connector is on.
- Q: Where in a Cowork project folder? → A: A hidden folder, `.vietnamizer/` (Fio: "Thư mục ẩn .vietnamizer/").
- Q: Who verifies on Cowork? → A: The agent, through Fio's "Finos" Chrome on claude.ai (Fio: "Mở Chrome Finos mà test"). Chrome reaches cloud Cowork and Chat on the web. It does not reach the local Cowork desktop app, so local Cowork is verified on Claude Code with a folder that stands in for a project, plus whatever the web shows of a local project.

## Background: what the skill assumes today

Since spec 032, the skill sorts hosts into two kinds:

- **Hosts that write files.** Profiles go to a Markdown file, Orrery or Obsidian, and the registry is fixed at `~/.agents/vietnamizer/registry.md`.
- **Chat hosts with no local files.** These are claude.ai web, Desktop, Mobile and "Cowork chạy trên cloud". Here a compact copy of about 1,200 characters goes into the Chat's memory. It holds no evidence excerpts, rating history or open points, and Chat may rewrite it.

Research on 26/11/2026, from Anthropic help and docs pages, shows a different picture:

- **Cowork on the desktop** reads and writes files in the folders the user attaches. A Cowork project holds local folders and its own memory, and files persist across sessions.
- **Cloud Cowork** keeps only the files it hands back. It shares account memory with Chat.
- **claude.ai Projects** have per-project memory.
- **Connectors.** The Google Drive connector can create files in the user's own Drive, with an approval prompt for each action by default.
- **Claude Code cloud sessions** start from a fresh VM. Only the repository persists.
- **Agent Skills spec.** It has no storage feature.

So the skill under-serves local Cowork. It treats Cowork as a host without files and saves only the compact copy, though the project folder could keep the full profile. On cloud hosts, the full profile with its evidence and open points is lost unless the user keeps it by hand.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Keep a full profile in a Cowork project (Priority: P1)

A user works in a Cowork project on their computer with a folder attached. They ask Vietnamizer to learn their voice and save it. The full profile, the same file as on Claude Code, is saved in `.vietnamizer/` inside that folder, with a registry beside it. In a later session of the same project, "theo giọng của tôi" applies it.

**Why this priority**: This is the biggest gap. The host can keep files, and the skill throws away most of the profile.

**Independent Test**: In a folder that stands in for a project, on Claude Code, and on Cowork where the web shows it:
1. Learn a profile.
2. Save it to the project folder.
3. Start a new session and call it by name and by "theo giọng của tôi".

Check the files written, the registry row, and that nothing else was read.

**Acceptance Scenarios**:

1. **Given** a session with an attached project folder the agent can write, **When** the user asks to save a learned profile, **Then** the agent offers "this project's folder (`.vietnamizer/`)" among the stores, shows the exact path, and writes only after the user's yes.
2. **Given** a saved project profile, **When** the user calls it in a new session of the same project, **Then** the agent reads `.vietnamizer/registry.md` and exactly that profile, and applies it.
3. **Given** a project folder without `.vietnamizer/`, **When** the user asks to save, **Then** the question says the folder will be created, and that yes is the consent to create exactly that folder.

---

### User Story 2 - Keep a full copy on cloud hosts (Priority: P2)

A user on cloud Cowork or claude.ai Chat saves a profile. Besides the compact memory copy, they may keep the full profile as a Markdown file in their Google Drive when the Drive connector is on. A later call may read it back from Drive.

**Why this priority**: It gives cloud users the full profile, evidence and open points included, with a store they own. It depends on a connector being on, so it is second.

**Independent Test**: On claude.ai, through Chrome, with the Drive connector on:
1. Save a profile to Drive.
2. Check that the file exists in Drive with the full content.
3. In a new chat, call the profile and see it applied.

With the connector off, check that Drive is never offered.

**Acceptance Scenarios**:

1. **Given** a cloud host with the Drive connector available, **When** the user saves a profile, **Then** the stores offered include "Google Drive", with the file name and folder. The agent creates the file only after the user's yes and the host's own approval.
2. **Given** a cloud host without a Drive connector, **When** the user saves, **Then** Drive is not offered and the compact memory copy works as in 0.16.2.
3. **Given** a profile saved in Drive and noted in the compact memory copy, **When** the user calls it, **Then** the agent reads exactly that Drive file and no other.

---

### User Story 3 - Read only what the task needs (Priority: P3)

The profile route reads `references/voice-profile.md` (41 KB) for every profile task. Spec 038 measured this route at 82 KB. After this spec, applying a saved profile reads only the part about applying, not the parts about learning or saving.

**Why this priority**: It cuts the read cost of the most common profile task. It needs no new store, so it can land last or alone.

**Independent Test**: The route budget check (`scripts/route_budget.py`) shows a lower total for the apply task. The contract tests still find every rule in exactly one file.

**Acceptance Scenarios**:

1. **Given** a request to apply a saved profile, **When** the agent runs, **Then** it reads the index and the apply part, and no other part of the voice-profile reference.
2. **Given** the split, **When** the contract tests run, **Then** every pinned rule is found in exactly one file.

### Edge Cases

- **Project folder is read-only, or the attached folder is a Git work tree.** The registry rules of 0.16.2 apply: a registry inside a Git work tree, behind a symlink, or inside instruction or memory files is neither read nor written. Spec 039 does not create `.vietnamizer/` inside a repository unless the user names it.
- **Two copies exist**, one in the project and one in `~/.agents/vietnamizer/`, or one in Drive and one in memory. A call reads one profile only: the registry of the current project first, then the home registry, and on cloud the Drive file the memory line names. The agent never merges copies.
- **Drive approval is declined or fails.** Say it was not saved, and keep the compact copy flow.
- **Cloud Cowork task with memory turned off.** No memory copy; offer Drive if available; otherwise show the profile for the user to keep.
- **Scheduled tasks**, which can read memory but not write it. No save is offered.
- **The user deletes `.vietnamizer/` or the Drive file.** A later call reports that the profile is not found. The agent does not search elsewhere.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skill MUST tell a host with an attached, writable project folder (local Cowork, Claude Code in a project) apart from a host with no local files. It decides from the tools and folders the agent actually sees, never from the product name alone. It no longer lists "Cowork chạy trên cloud" as the only Cowork case.
- **FR-002**: On a host with a writable project folder, saving a profile MUST offer the store "this project (`.vietnamizer/`)". Files go to `.vietnamizer/profiles/<slug>.md` and `.vietnamizer/registry.md`, in the same format as the home registry and profile.
- **FR-003**: A call MUST read the project registry first when present, else the home registry. It reads exactly one profile and searches no other store on a miss.
- **FR-004**: On a cloud host with the Google Drive connector available, saving MUST offer "Google Drive". The file goes to a `Vietnamizer` folder the user can change, and holds the full profile. The compact memory copy MAY name that file, so a later call can find it. Nothing is written without the user's yes and the host's own approval.
- **FR-005**: Without a writable folder or a Drive connector, the 0.16.2 compact memory flow MUST be unchanged.
- **FR-006**: The skill MUST NOT create `.vietnamizer/` inside a Git work tree, behind a symlink, or in an instruction or memory location unless the user names that place. All 0.16.2 consent, scope and privacy rules stay.
- **FR-007**: `references/voice-profile.md` MUST be split by task: learn, save and registry, apply, update and rate. A short index names the parts. Every rule keeps exactly one owner, and every pinned phrase stays findable.
- **FR-008**: The constitution's "Tuyến hồ sơ giọng" constraint MUST be amended first. Today it fixes the registry at `~/.agents/vietnamizer/registry.md` and lists cloud Cowork as a Chat host. The amendment adds the project registry and the Drive store. Fio approves the exact text (MINOR bump, 2.9.0 → 2.10.0).
- **FR-009**: `PRIVACY.md`, `references/help.md`, README and `docs/style-and-voice.md` MUST describe the new stores. They also say that a project store stays on the user's computer and a Drive file lives in the user's own Drive.
- **FR-010**: Verification:
  - Contract tests for every new rule.
  - Agent runs on Claude Code with a folder that stands in for a project.
  - Runs on claude.ai through Fio's "Finos" Chrome for cloud Cowork or Chat, with Drive and without.
  - Local Cowork can be checked in Chrome only as far as the web shows it. The report says what was not checked.

### Key Entities

- **Project store**: `.vietnamizer/` in an attached project folder, holding `registry.md` and `profiles/<slug>.md`.
- **Drive store**: a Markdown profile file in the user's Google Drive, named in the compact memory copy.
- **Home store**: the 0.16.2 `~/.agents/vietnamizer/` store, unchanged.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a project-folder session, a saved profile is applied by name and by "theo giọng của tôi" in a new session, with the full profile, not the compact copy, in every verification run.
- **SC-002**: On claude.ai with Drive on, a profile saved to Drive is read back in full in a new chat. With Drive off, the flow equals 0.16.2.
- **SC-003**: No verification run reads or writes a store the user did not choose, or reads more than one profile per call.
- **SC-004**: Applying a saved profile reads at least 50% fewer bytes of the voice-profile reference than 0.16.2, by the route budget check.
- **SC-005**: Every contract test passes, and every pinned phrase is found in exactly one file.

## Assumptions

- The Drive connector's tool names and approval behavior come from the host. The skill uses whatever create and read tools the agent sees, and offers Drive only when it sees them.
- Cloud Cowork tasks share account memory with Chat, so the compact copy works there as on Chat.
- Local Cowork sessions do not use account memory. Project memory is Cowork's own, and the skill does not write to it.
- This spec does not touch the editing routes, so the spec 038 gate pool does not apply.
- Release, version and catalog pin follow `versioning`, on Fio's go.
