#!/usr/bin/env python3
"""採点JSON・本人特定・自由記述OCR・AI返信を統合して 採点結果_集約.json を作る。

キーは学籍番号。以後の帳票はすべてこの集約ファイルを入力にする。
※ verify_scores.py をエラー0件で通してから実行すること。

入力:
  sheet_map.json   [{"sheet": "1-01", "sid": "B990001", "name": "見本 太郎"}, ...]
  comments_all.json [{"sheet": "1-01", "to_teacher": "…", "to_ai": "…"}, ...]  （任意）
  ai_replies.json  {"1-01": "AIからの返信文", ...}                            （任意）
"""
import json
import os

import examlib as E


def load_optional(p, default):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def main():
    sheet_map = {r['sheet']: r for r in json.load(open(E.path('sheet_map'), encoding='utf-8'))}
    comments = {r['sheet']: r for r in load_optional(E.path('comments'), [])}
    replies = load_optional(E.path('ai_replies'), {})

    agg = {}
    warn = []
    for _fname, rec in E.load_batches():
        sheet = rec['sheet']
        if sheet not in sheet_map:
            warn.append(f'{sheet}: sheet_map に対応する本人特定結果がありません')
            continue
        official = sheet_map[sheet]
        sid = official['sid']
        com = comments.get(sheet, {})
        agg[sid.lstrip('B')] = {
            'sheet': sheet,
            'official_sid': sid,
            'official_name': official['name'],
            'scores': rec['scores'],
            'total': rec['total'],
            'summary': rec.get('summary', ''),
            'flags': rec.get('flags', []),
            'to_teacher': com.get('to_teacher'),
            'to_ai': com.get('to_ai'),
            'ai_reply': replies.get(sheet),
        }
        # 取り違えの最終防波堤: 採点recの学籍番号と本人特定結果の食い違いを検出
        rec_sid = str(rec.get('student_id', '')).lstrip('B')
        if rec_sid and rec_sid != sid.lstrip('B'):
            warn.append(f'{sheet}: 採点JSONのID {rec_sid} ≠ 本人特定 {sid} → 画像で確認すること')

    out = E.path('aggregate')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(agg, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(agg)}名分を保存: {out}')
    for w in warn:
        print(' !!', w)

    noreply = [v['sheet'] for v in agg.values() if v.get('to_ai') and not v.get('ai_reply')]
    if noreply:
        print('AI返信未作成:', ' '.join(sorted(noreply)))


if __name__ == '__main__':
    main()
