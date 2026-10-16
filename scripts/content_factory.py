#!/usr/bin/env python3
"""Offline content checks and deterministic HTML board generation (Python 3.9+)."""
import argparse
import csv
import datetime
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'idea', 'draft', 'review', 'returned', 'final', 'published'}
TRANSITIONS = {'idea': {'draft'}, 'draft': {'review'}, 'review': {'final', 'returned'},
               'returned': {'draft'}, 'final': {'published', 'returned'}, 'published': set()}
FIELDS = ['topic_id', 'platform', 'status', 'previous_status', 'owner', 'due',
          'file_path', 'visual_brief_id', 'review_path', 'notes']
OPTIONAL_FIELDS = {'owner', 'visual_brief_id', 'notes'}


def local_path(root, name, directory):
    """Reject absolute paths, traversal, and symlinks escaping a designated folder."""
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('unsafe relative path: ' + name)
    resolved = (root / path).resolve()
    try:
        resolved.relative_to((root / directory).resolve())
    except ValueError:
        raise ValueError('path outside ' + directory + ': ' + name)
    return resolved


def read_board(root):
    with (root / '00-console/content-board.csv').open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('CSV header must be: ' + ','.join(FIELDS))
        rows = list(reader)
    for row in rows:
        if None in row or any(not isinstance(row.get(key), str) or (key not in OPTIONAL_FIELDS and not row[key].strip()) for key in FIELDS):
            raise ValueError('CSV rows must contain exactly the required fields; only owner, visual_brief_id, and notes may be empty')
    return rows


def parse_draft(text):
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('missing opening front matter delimiter')
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise ValueError('missing closing front matter delimiter')
    meta = {}
    for line in lines[1:end]:
        key, sep, value = line.partition(':')
        if not sep or not key.strip() or not value.strip() or key.strip() in meta:
            raise ValueError('invalid or duplicate front matter field')
        meta[key.strip()] = value.strip()
    for key in ('topic_id', 'platform', 'status', 'version'):
        if key not in meta:
            raise ValueError('missing front matter: ' + key)
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['topic_id']):
        raise ValueError('invalid topic_id')
    if meta['status'] not in STATUSES:
        raise ValueError('invalid draft status')
    if not re.fullmatch(r'[1-9][0-9]*', meta['version']):
        raise ValueError('version must be a positive integer')
    return meta, '\n'.join(lines[end + 1:]).strip()


def validate_body(body, rule):
    errors = []
    length = len(body) if rule['length_unit'] == 'chars' else len(body.split())
    if not rule['min_length'] <= length <= rule['max_length']:
        errors.append('body length {} outside {}–{} {}'.format(length, rule['min_length'], rule['max_length'], rule['length_unit']))
    letters = [c for c in body if c.isalpha()]
    if rule['language'] == 'zh-Hans':
        matching = sum('\u4e00' <= c <= '\u9fff' for c in letters)
    else:
        matching = sum(c.isascii() for c in letters)
    if not letters or matching / len(letters) < rule['min_language_ratio']:
        errors.append('language heuristic failed for ' + rule['language'])
    if 'tweet_max_chars' in rule:
        tweets = re.split(r'(?m)^---\s*$', body)
        for index, tweet in enumerate(tweets, 1):
            if not tweet.strip() or len(tweet.strip()) > rule['tweet_max_chars']:
                errors.append('tweet {} is empty or exceeds {} characters'.format(index, rule['tweet_max_chars']))
    return errors


def check(root=ROOT):
    errors = []
    rules = json.loads((root / '02-platform-guides/platform-rules.json').read_text(encoding='utf-8'))['platforms']
    rows = read_board(root)
    drafts = {}
    for path in sorted((root / '03-drafts').rglob('*.md')):
        label = str(path.relative_to(root))
        try:
            local_path(root, label, '03-drafts')
            meta, body = parse_draft(path.read_text(encoding='utf-8'))
            if meta['platform'] not in rules:
                raise ValueError('unknown platform')
            expected = '03-drafts/{}/{}.md'.format(meta['topic_id'], meta['platform'])
            if label != expected:
                raise ValueError('draft path must be ' + expected)
            drafts[label] = meta
            errors.extend(label + ': ' + issue for issue in validate_body(body, rules[meta['platform']]))
        except (ValueError, OSError) as exc:
            errors.append(label + ': ' + str(exc))
    seen = set()
    referenced = set()
    for index, row in enumerate(rows, 2):
        label = 'CSV row {}'.format(index)
        key = (row['topic_id'], row['platform'])
        if key in seen:
            errors.append(label + ': duplicate topic/platform')
        seen.add(key)
        previous, current = row['previous_status'], row['status']
        if previous not in STATUSES or current not in STATUSES:
            errors.append(label + ': invalid status')
        elif previous != current and current not in TRANSITIONS[previous]:
            errors.append(label + ': invalid transition ' + previous + ' -> ' + current)
        try:
            datetime.date.fromisoformat(row['due'])
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', row['due']):
                raise ValueError('due must use YYYY-MM-DD')
            path = local_path(root, row['file_path'], '03-drafts')
            if not path.is_file():
                raise ValueError('missing draft')
            review = local_path(root, row['review_path'], '04-review')
            if not review.is_file():
                raise ValueError('missing review record')
            if row['visual_brief_id'] and not re.fullmatch(r'[a-z0-9-]+', row['visual_brief_id']):
                raise ValueError('invalid visual brief ID')
            if row['visual_brief_id'] and not (root / '05-visual-briefs' / (row['visual_brief_id'] + '.md')).is_file():
                raise ValueError('missing visual brief')
            meta = drafts.get(row['file_path'])
            if meta is None:
                raise ValueError('draft could not be validated')
            if any(meta[k] != row[k] for k in ('topic_id', 'platform', 'status')):
                raise ValueError('CSV and draft metadata disagree')
            referenced.add(row['file_path'])
        except (ValueError, OSError) as exc:
            errors.append(label + ': ' + str(exc))
    errors.extend(path + ': draft missing from board' for path in sorted(set(drafts) - referenced))
    return errors


def render(root=ROOT):
    rows = read_board(root)
    esc = html.escape
    parts = ['<!doctype html>', '<html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<title>Multi-Platform Content Factory</title>',
             '<style>body{font:16px system-ui;margin:2rem;color:#182638;background:#f6f8fa}table{border-collapse:collapse;background:white}th,td{padding:.7rem;border:1px solid #ccd3dc;text-align:left}a{color:#164f9c}.board{overflow-x:auto}caption{text-align:left;padding:.7rem}</style>',
             '</head><body><h1>Multi-Platform Content Factory</h1>',
             '<p>Public template. All examples are fictional.</p>',
             '<p>Generated from content-board.csv. Human approval and manual publication required.</p>',
             '<div class="board"><table><caption>Editorial board</caption><thead><tr>']
    parts.extend('<th scope="col">' + esc(field.replace('_', ' ')) + '</th>' for field in FIELDS)
    parts.append('</tr></thead><tbody>')
    for row in rows:
        parts.append('<tr>')
        for field in FIELDS:
            value = row[field]
            if field in ('file_path', 'review_path'):
                local_path(root, value, '03-drafts' if field == 'file_path' else '04-review')
                from urllib.parse import quote
                cell = '<a href="../{}">{}</a>'.format(esc(quote(value, safe='/'), quote=True), esc(value))
            else:
                cell = esc(value)
            parts.append('<td>' + cell + '</td>')
        parts.append('</tr>')
    parts.append('</tbody></table></div></body></html>')
    return '\n'.join(parts) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', choices=['build', 'check'], default='build')
    parser.add_argument('--check', action='store_true', help='check generated HTML staleness without writing')
    args = parser.parse_args(argv)
    try:
        if args.command == 'check':
            errors = check()
            if errors:
                print('\n'.join(errors), file=sys.stderr)
                return 1
            print('Content checks passed.')
        if args.command == 'build' or args.check:
            target = ROOT / '00-console/content-board.html'
            expected = render()
            if args.check:
                if not target.exists() or target.read_text(encoding='utf-8') != expected:
                    print('HTML is stale; run build.', file=sys.stderr)
                    return 1
                print('HTML is current.')
            else:
                target.write_text(expected, encoding='utf-8')
                print('Built 00-console/content-board.html')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
