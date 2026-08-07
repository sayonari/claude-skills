#!/usr/bin/env python3
"""採点JSONの機械検証（必須工程）.

検証項目:
  - 小問キーの網羅（欠落・未知キー）
  - 配点上限・下限
  - 合計点の再計算（サブエージェントの合計ミスは実測 1/131 件で発生する）
  - 全答案の網羅・重複
  - 教員確認に回すべき flags の集計

使い方:
  python3 verify_scores.py          # 検証のみ
  python3 verify_scores.py --fix    # total を再計算値で上書き保存
"""
import sys

import examlib as E

REVIEW_KEYWORDS = ('判読困難', '判読不能', '基準外', '裁量', '別解', '指示文')


def main():
    MAX = E.max_points()
    errors = []
    records = E.load_batches()
    if not records:
        print('採点JSONが1件もありません:', E.path('batches'))
        return 1

    seen = {}
    review = []
    for fname, rec in records:
        sheet = rec.get('sheet')
        sid = rec.get('student_id', '')
        if sheet in seen:
            errors.append(f'{fname}: {sheet} 重複（既出: {seen[sheet]}）')
        seen[sheet] = fname

        scores = rec.get('scores', {})
        missing = set(MAX) - set(scores)
        extra = set(scores) - set(MAX)
        if missing:
            errors.append(f'{sheet} {sid}: 小問欠落 {sorted(missing)}')
        if extra:
            errors.append(f'{sheet} {sid}: 未知の小問 {sorted(extra)}')

        total = 0
        for q, v in scores.items():
            if q not in MAX:
                continue
            if not (isinstance(v, (list, tuple)) and len(v) >= 2):
                errors.append(f'{sheet} {sid}: {q} の形式が [点数, 転記文] でない')
                continue
            pts = v[0]
            if not (isinstance(pts, (int, float)) and 0 <= pts <= MAX[q]):
                errors.append(f'{sheet} {sid}: {q}={pts} が範囲外(0..{MAX[q]})')
            else:
                total += pts
            if not str(v[1]).strip():
                errors.append(f'{sheet} {sid}: {q} の転記文が空（疑義対応の根拠になるため必須）')
        if total != rec.get('total'):
            errors.append(f'{sheet} {sid}: total不一致 申告{rec.get("total")} 実{total}')
            rec['total'] = total

        for fl in rec.get('flags', []):
            if any(k in str(fl) for k in REVIEW_KEYWORDS):
                review.append((sheet, sid, fl))

    absent = set(E.all_sheet_ids()) - set(seen)
    if absent:
        errors.append(f'未採点の答案: {sorted(absent)}')

    print(f'{len(records)}件読込 / エラー {len(errors)}件')
    for e in errors:
        print(' -', e)

    print(f'\n■ 教員に確認・報告すべき flags: {len(review)}件')
    for sheet, sid, fl in review:
        print(f' - {sheet} {sid}: {fl}')
    if review:
        print('→ make_review_html.py で画像付きHTMLを作り、教員判定を仰ぐこと（必須工程）')

    if '--fix' in sys.argv:
        by_file = {}
        for fname, rec in records:
            by_file.setdefault(fname, []).append(rec)
        for fname, recs in by_file.items():
            E.save_batch(fname, recs)
        print('\ntotal を再計算値で保存しました')

    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
