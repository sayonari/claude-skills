#!/usr/bin/env python3
"""採点JSONへのパッチ適用（教員判定の反映・方針変更の一括適用）.

**採点JSONを手で書き換えてはいけない。** 必ずこのスクリプトで、理由付きで適用する。
変更は転記文と flags に残り、疑義申告時の説明根拠になる。

使い方:
  1) patch.json を書く（下記フォーマット）
  2) python3 apply_patch.py --dry    # 変更内容の確認だけ
  3) python3 apply_patch.py          # 適用
  4) python3 verify_scores.py --fix && python3 aggregate.py  で再検証・再集約

patch.json:
{
  "label": "v3 教員判定（2026-08-05）",
  "changes": [
    {"sheet": "1-44", "item": "4b", "new": 2,
     "reason": "教員判定: 形は正解のため特別点2点"},
    {"sheet": "2-04", "item": "6c", "new": 4,
     "reason": "教員判定: SUBAで正解"},
    {"sheet": "1-22", "item": "4a", "new": 0,
     "reason": "方針: 採点基準に明記のない裁量部分点を取消"}
  ]
}
"""
import json
import os
import sys

import examlib as E

PATCH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch.json')


def main():
    if not os.path.exists(PATCH_PATH):
        print(f'{PATCH_PATH} がありません。docstring のフォーマットで作成してください。')
        return 1
    patch = json.load(open(PATCH_PATH, encoding='utf-8'))
    label = patch.get('label', 'patch')
    changes = patch['changes']
    dry = '--dry' in sys.argv
    MAX = E.max_points()

    by_file = {}
    for fname, rec in E.load_batches():
        by_file.setdefault(fname, []).append(rec)

    sheet_to = {rec['sheet']: (fname, rec) for fname, recs in by_file.items() for rec in recs}

    applied, skipped = [], []
    dirty_files = set()
    for c in changes:
        sheet, item, new = c['sheet'], c['item'], c['new']
        if sheet not in sheet_to:
            skipped.append(f'{sheet}: 採点JSONに存在しません')
            continue
        fname, rec = sheet_to[sheet]
        if item not in rec['scores']:
            skipped.append(f'{sheet} {item}: 小問が存在しません')
            continue
        if item in MAX and not (0 <= new <= MAX[item]):
            skipped.append(f'{sheet} {item}: {new}点は配点範囲外(0..{MAX[item]})')
            continue
        old = rec['scores'][item][0]
        if old == new:
            skipped.append(f'{sheet} {item}: 変更なし（{old}点のまま）')
            continue
        if not dry:
            rec['scores'][item][1] = str(rec['scores'][item][1]) + \
                f'【{label}: {old}点→{new}点。{c["reason"]}】'
            rec['scores'][item][0] = new
            rec.setdefault('flags', []).append(f'{label}: {item} {old}→{new}点（{c["reason"]}）')
            rec['total'] = rec['total'] - old + new
            dirty_files.add(fname)
        applied.append((sheet, item, old, new, rec['total'], c['reason']))

    for sheet, item, old, new, total, reason in applied:
        print(f'{sheet} {item}: {old}→{new}点（新合計 {total}）  {reason}')
    for s in skipped:
        print(' !!', s)
    print(f'\n{"[DRY RUN] " if dry else ""}適用 {len(applied)}件 / スキップ {len(skipped)}件')

    if not dry:
        for fname in dirty_files:
            E.save_batch(fname, by_file[fname])
        print(f'{len(dirty_files)}ファイルを保存しました')
        print('次: python3 verify_scores.py --fix && python3 aggregate.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
