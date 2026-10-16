# Multi-Platform Content Factory

Public template. All examples are fictional.

Turn one topic into five platform-specific versions: 公众号 in Simplified Chinese, an English X thread, an English Medium article, an English LinkedIn post, and a community-native English Reddit discussion.

## Quick start

1. Copy this workspace and replace placeholders such as `{{YOUR_BRAND}}` and `{{YOUR_PRODUCT}}`.
2. Copy the topic brief in `01-topics`, assign a unique topic ID, and agree on audience, claims, and purpose.
3. Create five drafts using the sample folder and platform guides. Add their relative paths to the board CSV.
4. Run `python3 scripts/content_factory.py check` and `python3 scripts/content_factory.py build`.
5. Open `00-console/content-board.html`, complete human review, and record approved publication manually.

Requires Python 3.9+; no dependencies or network access. Run tests with `python3 -m unittest discover tests`. Use `python3 scripts/content_factory.py build --check` to detect stale HTML without writing it. `python3 scripts/content_factory.py --check` is an alias.

## Workspace guide

| Directory | Purpose |
| --- | --- |
| `00-console` | CSV source of truth, generated board, editorial tasks, publication log |
| `01-topics` | Shared topic briefs and evidence |
| `02-platform-guides` | Editorial guidance and machine-readable local limits |
| `03-drafts` | One topic folder, one Markdown file per platform |
| `04-review` | Human review checklist and decision records |
| `05-visual-briefs` | Image briefs and size planning |
| `06-published` | Approved publication snapshots and records |
| `90-archive` | Retired material with context |
| `99-system-rules` | Fields, workflow, naming, collaboration, maintenance |
| `scripts` | Offline standard-library validation and board generation |
| `tests` | Unit tests for workflow and validation |

## Daily workflow

1. Review the board and editorial tasks; assign owners and dates.
2. Adapt the topic for each audience instead of copying the same text everywhere.
3. Check claims, permissions, language, visuals, and community fit; capture human decisions in `04-review`.
4. Update both draft and board status. When changing status, set `previous_status` to the prior status and record the decision in review notes.
5. A human approves final copy and publishes manually. Record the exact version and destination in the publication log, then rebuild the board.

## Using with an AI assistant

Ask the assistant to read `AGENTS.md`, the topic brief, and the relevant platform guide. Request drafts and visual briefs with unsupported claims flagged for review. AI may prepare content and run checks; only a human may approve final content or publish. Never give the assistant publishing credentials.

Limits in this template are conservative editorial defaults, not a live description of platform policies. Verify actual destination requirements manually before publication. Automated language checks are heuristics and do not replace an editor. Templates are excluded from draft validation; the sample drafts are validated. Transition checks validate the declared previous/current pair, not historical changes to the CSV.

## Fictional pipeline samples

示例/SAMPLE: three shared briefs and fifteen audience drafts illustrate uneven work in progress, using 2026-10-16 as the scenario date. Dates vary; some tasks are overdue, two owners are unassigned, and versions range from v1 to v3. The board includes idea, draft, review, returned (退回), final, and published states. Final/published rows illustrate fictional history only; no real approval or publication occurred.

Blank owners mean unassigned. Blank visual IDs mean no artwork is currently requested; existing briefs span requested, in-progress, delivered, and needs-revision. Notes flag sample-002 Reddit as skipped / not applicable for scheduling while retaining its provisional idea adaptation. Review records contain concrete open issues and return reasons. The sole simulated publication, sample-001 X v3, has a matching log entry and exact body snapshot. Replace these samples before real use.

## License

CC0 1.0 Universal; see `LICENSE`. Public template. All examples are fictional.
