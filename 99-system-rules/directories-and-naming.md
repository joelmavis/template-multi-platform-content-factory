# Directories and naming

Use numbered directories as described in README. Topic IDs use lowercase letters, numbers, and hyphens, for example sample-001. Store drafts as `03-drafts/<topic_id>/<platform>.md`. Store shared briefs as `01-topics/<topic_id>.md`, visual briefs as `05-visual-briefs/<topic_id>-<platform>.md`, and review records in `04-review`.

Use UTF-8 and relative POSIX paths; do not traverse outside the workspace. Keep the documented CSV header stable, including the notes column. Edit CSV as source and regenerate HTML; never hand-edit the generated board. Increment version for substantive revisions and identify the reviewed version. Keep templates outside 03-drafts. X tweets are separated by a standalone --- line after the closing front-matter delimiter.
