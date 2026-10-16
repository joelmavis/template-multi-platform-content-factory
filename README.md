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

## How to use / 使用方法

Paste an English prompt below into an AI agent in PuppyOne; each is a separate task using this repository's fictional samples. 中文简版附在每条提示后。Keep work offline, use role placeholders, and retain 示例/SAMPLE labels; sample history is never real approval. After edits, run `python3 scripts/content_factory.py check`, `python3 scripts/content_factory.py build --check`, and `python3 -m unittest discover tests`; if the CSV changes, first regenerate HTML with `python3 scripts/content_factory.py build`.

### Split one topic into five platform versions / 一题五版

Use one shared brief to develop five distinct audience angles and drafts.

```text
Read AGENTS.md, README.md, 99-system-rules, 01-topics/sample-003.md,
02-platform-guides, and 00-console/content-board.csv. Use the single shared
brief to revise the five existing files in 03-drafts/sample-003: wechat.md
in Simplified Chinese, and x.md, medium.md, linkedin.md, and reddit.md in
English. Give each audience a distinct hook, structure, and CTA; follow
platform-rules.json in 02-platform-guides. Retain SAMPLE labels, flag
unsupported claims, and increment versions for substantive revisions.
Keep existing statuses and align board metadata; identify any reviewed
version needing fresh human review in 04-review/sample-003-review.md.
Run the README validation commands, rebuilding HTML if the CSV changes.
Leave approval and publication to humans.
```

中文简版：根据 sample-003 的同一选题简报改写五个平台版本，区分受众、语言与结构，更新版本并保持元数据一致，提交人工复审。

### Rewrite only one platform version / 只改一个平台

Improve the LinkedIn adaptation with a specific professional decision and question.

```text
Read AGENTS.md, 99-system-rules, 01-topics/sample-003.md,
02-platform-guides/linkedin.md, 02-platform-guides/platform-rules.json,
04-review/sample-003-review.md, and 03-drafts/sample-003/linkedin.md.
Rewrite only this LinkedIn draft: add a concrete fictional condition for
reopening an archived draft and end with one relevant question. Keep it
English and within the local word limits. Increment its version, retain
draft status and the SAMPLE label, and flag claims needing human review.
Leave the shared brief and other four drafts unchanged. Run the README
validation commands and summarize the revision for the human reviewer.
```

中文简版：只改 sample-003 的 LinkedIn 草稿，补充重新开启旧稿的具体条件与结尾问题，递增版本并保留草稿状态。

### Review and send back a draft / 审稿并建议退回

Prepare actionable return feedback for a human reviewer to decide and apply.

```text
Read AGENTS.md, 99-system-rules, 01-topics/sample-003.md,
03-drafts/sample-003/medium.md, 02-platform-guides/medium.md,
02-platform-guides/platform-rules.json, 04-review/review-checklist-template.md,
and 04-review/sample-003-review.md. Review the current Medium version for
claims, audience fit, structure, and the missing archive-versus-reopen
example. Append clearly labeled AI-proposed feedback to the existing review
record, naming the version, concrete requested edits, a responsible role
placeholder, and a proposed next review date. Recommend return if warranted;
leave the human decision pending and do not change statuses. Explain that
if the human returns it, they must set the matching CSV and draft status to
returned and CSV previous_status to review, then rebuild the board and run
the README validation commands. Do not rewrite the draft during this review.
```

中文简版：审核 sample-003 的 Medium 稿，记录版本、退回理由、修改要求、责任角色和建议复审日期，由人工决定并执行退回。

### Create a visual brief for one version / 编写单版视觉简报

Turn one Medium draft into a concrete image specification for a designer.

```text
Read AGENTS.md, 99-system-rules, 03-drafts/sample-003/medium.md,
02-platform-guides/medium.md, 05-visual-briefs/visual-brief-template.md,
and 05-visual-briefs/size-cheat-sheet.md. Refine the existing
05-visual-briefs/sample-003-medium.md for this draft: specify a 1600 x 900
layout, safe margins, exact on-image copy, style, alt text, role owner,
and deadline consistent with 00-console/content-board.csv. Use an original
fictional diagram and identify rights and crop checks for human review.
Keep the brief requested, retain the SAMPLE label and matching visual ID,
and do not imply artwork delivery or human approval. Run the README
validation commands. Produce a brief, not an image.
```

中文简版：完善 sample-003 Medium 视觉简报，写清尺寸、构图、文案、替代文本、责任角色与截止日期，保留待制作和待人工审核状态。

### Record after publishing / 发布后归档

Prepare an exact publication record after a human supplies the publication facts.

```text
Read AGENTS.md, 99-system-rules, 06-published/published-record-template.md,
06-published/sample-record.md, 00-console/publish-log.md,
00-console/content-board.csv, and 04-review. Prepare a publication-record
proposal in your response using the existing template. Ask me for the human
approval reference, exact approved draft and version, exact published body,
publisher role, date, destination, and visual details if missing. Never infer
actual publication from sample records. Include the exact body snapshot and
a proposed log entry, using placeholders and example.com for fictional data.
Leave files and statuses unchanged: a human must verify the facts, save the
record in 06-published, update the log, and apply final -> published in the
CSV and draft with previous_status final. Provide the existing build and
validation commands from README for the human to run afterward. Do not
publish or mark content approved or published yourself.
```

中文简版：根据人工提供的发布事实准备精确正文快照、归档记录和日志条目，缺失信息先询问，由人工保存并更新已发布状态。

### Add a new platform rule / 新增平台规则

Add a local editorial rule for an existing platform while keeping its guide and validation limits consistent.

```text
Read AGENTS.md, 99-system-rules, 02-platform-guides/linkedin.md,
02-platform-guides/platform-rules.json, scripts/content_factory.py, and
tests/test_content_factory.py. Add a local LinkedIn editorial rule requiring
a concrete decision or next action before the closing question, and tighten
its maximum length from 400 to 350 words in both the guide and JSON. Keep
the five existing platform keys; this task adds a rule, not a sixth platform.
Explain that the semantic rule needs human review while the existing checker
enforces the length limit. Check all existing LinkedIn drafts and report
any violations without silently rewriting them. Record the maintenance
change in 99-system-rules/changelog.md and run the README validation commands;
do not claim these local defaults are official destination policies.
```

中文简版：为现有 LinkedIn 平台增加具体行动要求，并将指南和 JSON 的上限同步为 350 词；检查现有稿件，语义要求交由人工审核。

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
