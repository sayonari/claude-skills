#!/usr/bin/env python3
"""★教員確認HTML生成 — 採点後に必ず実施する工程.

AI が採点に迷った箇所・疑問に思った箇所・部分点の付け方を判断しかねた箇所を、
答案画像のキャプチャを埋め込んだ単一HTMLにして教員に提示し、判定を仰ぐ。

使い方:
  1) python3 make_review_html.py --init
       採点JSON の flags から確認候補を抽出し、review_cases.json の雛形を書き出す
  2) 雛形の各ケースに「AIの判読・根拠」「別の判断をした場合の影響（点数まで）」を AI が書き込む
  3) python3 make_review_html.py
       画像埋め込みHTMLを生成 → open で教員に提示
  4) 教員判定を review_cases.json の "verdict" に記入 → 再生成して記録として保存
     → apply_patch.py で採点JSONへ反映

review_cases.json の1件:
{
  "sheet": "1-44",            # 答案ID
  "item": "4b",               # 小問ID
  "crop": "q4",               # 埋め込む画像（crops/<sheet>/<crop>.jpg）
  "zoom": [800, 200, 1600, 700],   # 任意: その画像内をさらに切り出して拡大表示
  "category": "判読困難",      # 判読困難 / 基準外 / 別解 / 全体方針
  "title": "4(b) 左の子のラベルが「30」か「20」か",
  "ai_judgement": "「30」と判読し、木の形は正解と同一だがラベル不一致で0点",
  "alternative": "「20」なら全親子関係一致で +5点（87→92点）",
  "verdict": ""               # 教員判定（記入後に再生成して保存）
}
"""
import base64
import html
import io
import json
import os
import sys

import examlib as E

CASES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review_cases.json')
OUT_PATH = os.path.join(E.path('output'), '教員確認_採点の判断.html')
REVIEW_KEYWORDS = ('判読困難', '判読不能', '基準外', '裁量', '別解')

esc = html.escape


# ---------------------------------------------------------------- init
def init_cases():
    """flags から確認候補を抽出して review_cases.json の雛形を作る。"""
    items = E.items()
    cases = []
    for _f, rec in E.load_batches():
        for fl in rec.get('flags', []):
            s = str(fl)
            if not any(k in s for k in REVIEW_KEYWORDS):
                continue
            # flags 中に小問IDらしき文字列があれば拾う
            item = next((k for k in items if k in s), '')
            cases.append({
                'sheet': rec['sheet'],
                'item': item,
                'crop': f'q{item[0]}' if item else 'q1',
                'category': next((k for k in REVIEW_KEYWORDS if k in s), '要確認'),
                'title': f'{item}: <確認したい論点を1行で>',
                'ai_judgement': s,
                'alternative': '<別の判断をした場合の影響を点数まで書く>',
                'verdict': '',
            })
    cases.sort(key=lambda c: (c['sheet'], c['item']))
    json.dump(cases, open(CASES_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(cases)}件の候補を書き出しました: {CASES_PATH}')
    print('各ケースの title / ai_judgement / alternative を埋めてから本スクリプトを実行してください。')
    print('※ 迷った箇所は全て出すこと。裁量で決めて黙って済ませない。')


# ---------------------------------------------------------------- render
def img64(sheet, crop, zoom=None, scale=1):
    p = os.path.join(E.path('crops'), sheet, f'{crop}.jpg')
    if not os.path.exists(p):
        return None
    if zoom or scale != 1:
        from PIL import Image
        im = Image.open(p)
        if zoom:
            im = im.crop(tuple(zoom))
        if scale != 1:
            im = im.resize((int(im.width * scale), int(im.height * scale)))
        buf = io.BytesIO()
        im.save(buf, format='JPEG', quality=92)
        return base64.b64encode(buf.getvalue()).decode()
    return base64.b64encode(open(p, 'rb').read()).decode()


CSS = """
body{font-family:"Hiragino Kaku Gothic ProN",sans-serif;color:#22304a;margin:0;
     background:#f4f1e8;line-height:1.7}
.wrap{max-width:1150px;margin:0 auto;padding:28px 32px 64px}
h1{font-size:21px;border-bottom:3px double #22304a;padding-bottom:8px}
h2{font-size:15px;margin:0 0 8px;border-left:6px solid #c73e3a;padding-left:10px}
.case{background:#fff;border:1px solid #d8cfba;border-radius:8px;padding:16px 20px;margin:22px 0}
.cat{display:inline-block;font-size:11px;background:#22304a;color:#fff;border-radius:3px;
     padding:1px 8px;margin-right:6px;vertical-align:2px}
.meta{border-collapse:collapse;margin-bottom:10px;font-size:13px;width:100%}
.meta th,.meta td{border:1px solid #d8cfba;padding:4px 10px;text-align:left}
.meta th{background:#ece5d3;white-space:nowrap;width:130px}
.meta .alt{background:#fdf3ec;color:#8c3d10;font-weight:600}
.meta .vd{background:#eaf2f8;color:#1e3d52;font-weight:600}
.meta .small{font-size:11px;color:#5a5344}
img{max-width:100%;border:1px solid #d8cfba;margin-top:4px}
.note{background:#f8f1dd;border:1px solid #b08c3d;border-radius:6px;padding:10px 14px;font-size:13px}
.policy{background:#eef3ea;border:1px solid #6f8b5c;border-radius:6px;padding:12px 16px;
        font-size:13px;margin-top:26px}
footer{color:#8a8270;font-size:12px;margin-top:24px}
"""


def render(cases, policy_notes):
    agg = E.load_aggregate()
    by_sheet = {v['sheet']: v for v in agg.values()}
    mp = E.max_points()
    body = ''
    for i, c in enumerate(cases, 1):
        s = by_sheet.get(c['sheet'], {})
        item = c.get('item', '')
        pt, note = s.get('scores', {}).get(item, ['—', '—'])[:2] if item else ('—', '—')
        rows = [
            ('現在の採点',
             f'{esc(item)}: <b>{pt}点</b>'
             + (f' / 満点{mp.get(item, "?")}点' if item in mp else '')
             + f'（合計 {s.get("total", "—")}点）', ''),
            ('AIの判読・根拠', esc(c.get('ai_judgement', '')), ''),
            ('別の判断なら', esc(c.get('alternative', '')), 'alt'),
            ('採点への転記', esc(str(note)), 'small'),
        ]
        if c.get('verdict'):
            rows.append(('教員判定', esc(c['verdict']), 'vd'))
        else:
            rows.append(('教員判定', '（　　　　　　　　　　　　　　　　　　　）', 'vd'))
        tr = ''.join(
            f'<tr><th class="{cls}">{k}</th><td class="{cls}">{v}</td></tr>'
            for k, v, cls in rows)

        imgs = ''
        b64 = img64(c['sheet'], c.get('crop', 'q1'))
        if b64:
            imgs += f'<img src="data:image/jpeg;base64,{b64}" alt="{c["sheet"]} {item}">'
        if c.get('zoom'):
            z = img64(c['sheet'], c.get('crop', 'q1'), zoom=c['zoom'], scale=2)
            if z:
                imgs += f'<img src="data:image/jpeg;base64,{z}" alt="拡大">'
        if not imgs:
            imgs = '<p style="color:#c73e3a">※ 画像が見つかりません（crops を確認）</p>'

        body += f"""
<div class="case">
<h2><span class="cat">{esc(c.get('category', '要確認'))}</span>
{i}. {esc(s.get('official_sid', ''))} {esc(s.get('official_name', ''))}
（{esc(c['sheet'])}）— {esc(c.get('title', ''))}</h2>
<table class="meta">{tr}</table>
{imgs}
</div>"""

    policy = ''
    if policy_notes:
        policy = ('<div class="policy"><b>全体方針の確認事項（一括判断をお願いします）</b><ul>'
                  + ''.join(f'<li>{esc(p)}</li>' for p in policy_notes) + '</ul></div>')

    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<title>{esc(E.CFG['exam_name'])} 採点の教員確認（{len(cases)}件）</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>{esc(E.CFG['course'])} {esc(E.CFG['exam_name'])} — 採点の教員確認（{len(cases)}件）</h1>
<div class="note">
AIが判読・部分点の判断に迷った箇所です。<b>画像を見て判定をお願いします（1件30秒程度）。</b>
判定いただければ、点数変更・帳票とPDFの再生成まで自動で反映します。<br>
画像はブラウザのズーム（⌘＋）で拡大できます。<b>基準外の裁量部分点はAI側では付けていません</b>
（付与するか否かの方針を決めていただければ一括適用します）。
</div>
{body}
{policy}
<footer>生成: {esc(E.CFG.get('exam_date', ''))} / AI採点 — 判定後はこのファイルに判定結果を追記して記録として保存すること</footer>
</div></body></html>"""


def main():
    if '--init' in sys.argv:
        init_cases()
        return 0
    if not os.path.exists(CASES_PATH):
        print(f'{CASES_PATH} がありません。まず --init を実行してください。')
        return 1
    data = json.load(open(CASES_PATH, encoding='utf-8'))
    cases = data['cases'] if isinstance(data, dict) else data
    policy_notes = data.get('policy_notes', []) if isinstance(data, dict) else []
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    open(OUT_PATH, 'w', encoding='utf-8').write(render(cases, policy_notes))
    print(f'保存: {OUT_PATH} ({os.path.getsize(OUT_PATH)//1024}KB, {len(cases)}件)')
    print(f'教員に提示: open "{OUT_PATH}"')
    return 0


if __name__ == '__main__':
    sys.exit(main())
