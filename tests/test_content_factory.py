import contextlib
import csv
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('factory', Path(__file__).resolve().parents[1] / 'scripts/content_factory.py')
f = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(f)


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for directory in ('00-console', '02-platform-guides', '03-drafts', '04-review', '05-visual-briefs'):
            shutil.copytree(f.ROOT / directory, self.root / directory)

    def tearDown(self):
        self.tmp.cleanup()

    def edit_row(self, **changes):
        rows = f.read_board(self.root)
        rows[0].update(changes)
        with (self.root / '00-console/content-board.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=f.FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_samples_and_generated_board(self):
        self.assertEqual([], f.check(self.root))
        self.assertEqual(f.render(self.root), (self.root / '00-console/content-board.html').read_text(encoding='utf-8'))

    def test_optional_owner_visual_and_notes(self):
        self.edit_row(owner='', visual_brief_id='', notes='')
        self.assertEqual([], f.check(self.root))
        self.edit_row(visual_brief_id='missing-sample-visual')
        self.assertIn('missing visual brief', '\n'.join(f.check(self.root)))
        self.edit_row(visual_brief_id='../unsafe')
        self.assertIn('invalid visual brief ID', '\n'.join(f.check(self.root)))
        self.edit_row(due='')
        with self.assertRaises(ValueError):
            f.read_board(self.root)

    def test_sample_pipeline_history_and_snapshot(self):
        rows = f.read_board(self.root)
        self.assertEqual(15, len(rows))
        self.assertEqual(f.STATUSES, {row['status'] for row in rows})
        for topic in ('sample-001', 'sample-002', 'sample-003'):
            self.assertEqual({'wechat', 'x', 'medium', 'linkedin', 'reddit'},
                             {row['platform'] for row in rows if row['topic_id'] == topic})
        skipped = next(row for row in rows if row['topic_id'] == 'sample-002' and row['platform'] == 'reddit')
        self.assertEqual('idea', skipped['status'])
        self.assertIn('NOT APPLICABLE', skipped['notes'])
        for topic, count in (('sample-001', 4), ('sample-002', 7)):
            _, body = f.parse_draft((self.root / '03-drafts' / topic / 'x.md').read_text())
            self.assertEqual(count, len(body.split('\n---\n')))
        published = [row for row in rows if row['status'] == 'published']
        self.assertEqual([('sample-001', 'x')], [(row['topic_id'], row['platform']) for row in published])
        meta, body = f.parse_draft((self.root / published[0]['file_path']).read_text())
        snapshot = (f.ROOT / '06-published/sample-record.md').read_text()
        self.assertIn('- version: ' + meta['version'], snapshot)
        self.assertEqual(body, snapshot.split('## Exact SAMPLE body snapshot — v3\n\n', 1)[1].strip())

    def test_transition_and_status_mismatch(self):
        self.edit_row(previous_status='idea', status='published')
        errors = '\n'.join(f.check(self.root))
        self.assertIn('invalid transition', errors)
        self.assertIn('metadata disagree', errors)
        self.edit_row(status='unknown')
        self.assertIn('invalid status', '\n'.join(f.check(self.root)))

    def test_required_front_matter_and_version(self):
        for text in ('body', '---\nplatform: x\n---\nbody', '---\ntopic_id: a\nplatform: x\nstatus: draft\nversion: 0\n---\nbody'):
            with self.assertRaises(ValueError):
                f.parse_draft(text)

    def test_length_language_and_tweets(self):
        rule = {'length_unit': 'chars', 'min_length': 1, 'max_length': 1000,
                'language': 'en', 'min_language_ratio': .8, 'tweet_max_chars': 280}
        self.assertEqual([], f.validate_body('a' * 280, rule))
        self.assertTrue(any('tweet' in e for e in f.validate_body('a' * 281, rule)))
        self.assertTrue(any('language' in e for e in f.validate_body('中文内容', rule)))
        self.assertTrue(any('length' in e for e in f.validate_body('', rule)))
        self.assertEqual([], f.validate_body('a' * 280 + '\n---\n' + 'b' * 280, rule))

    def test_duplicate_missing_and_unsafe_paths(self):
        self.edit_row(file_path='../outside.md')
        self.assertIn('unsafe relative path', '\n'.join(f.check(self.root)))
        with self.assertRaises(ValueError):
            f.local_path(self.root, '/tmp/example.md', '03-drafts')
        self.edit_row(file_path='03-drafts/missing.md')
        self.assertIn('missing draft', '\n'.join(f.check(self.root)))

    def test_escaped_html_and_staleness_cli(self):
        self.edit_row(owner='<script>alert("x")</script>')
        output = f.render(self.root)
        self.assertIn('&lt;script&gt;', output)
        original = f.ROOT
        try:
            f.ROOT = self.root
            # render's default root is bound at definition; explicitly exercise artifact logic using original data.
            (self.root / '00-console/content-board.html').write_text('stale', encoding='utf-8')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(1, f.main(['build', '--check']))
        finally:
            f.ROOT = original


if __name__ == '__main__':
    unittest.main()
