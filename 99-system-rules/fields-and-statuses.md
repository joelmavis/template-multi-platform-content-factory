# Fields and statuses

Canonical status flow: 选题 idea → 草稿 draft → 审核 review → 定稿 final → 已发布 published.

退回 returned is available from review or final; returned → draft starts revision. No other status jumps are allowed. A same-status pair is allowed for an unchanged row. Published is terminal; corrections start a new version in a new topic ID and link to the original record.

Editors (human or AI working under direction) may prepare idea/draft and submit draft → review. A human reviewer may move review → returned/final or final → returned. Only a human publisher may move final → published after actual publication. AI never approves final content or publishes. An editor may move returned → draft after recording the requested changes.

CSV fields: `topic_id` (stable lowercase ID), `platform` (wechat/x/medium/linkedin/reddit), `status`, `previous_status` (immediately prior status, or current status for no change), `owner` (role placeholder), `due` (ISO date), `file_path` (relative Markdown path under 03-drafts), `visual_brief_id` (matching brief filename stem), `review_path` (review record), `notes` (context and scheduling exceptions). One row per topic/platform; all columns are required. `owner` may be blank for unassigned work, `visual_brief_id` may be blank for text-only or not-yet-requested artwork, and `notes` is optional free text. Other values remain required. `notes` records scheduling exceptions such as SKIPPED / NOT APPLICABLE; these are not new workflow statuses. Retain idea status for a deferred angle. Draft front matter requires `topic_id`, `platform`, `status`, and positive integer `version`. Board and draft status must agree.

The checker validates declared transitions and metadata consistency, not identity, authorization, historical truth, or publication. Human decision records remain required. For a new idea row use idea → idea. Update previous_status on every transition, and keep decision details in review records.

Sample fixtures may illustrate final/published history when visibly labeled 示例/SAMPLE and explicitly fictional. They never constitute actual human approval or publication. All five audience adaptations are retained per topic, including provisional idea copy.
