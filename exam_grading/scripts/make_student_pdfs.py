#!/usr/bin/env python3
"""学生個人用の成績PDF（成績票 ＋ 赤入れ答案）を生成する.

HTMLを組み立て、Chromeヘッドレスで1つのPDFに印刷する。
先に annotate_answers.py で赤入れ答案を作っておくこと。

使い方:
  python3 make_student_pdfs.py           # 全員
  python3 make_student_pdfs.py 990001    # 指定学生のみ
"""
import html
import os
import subprocess
import sys
import tempfile

import examlib as E

PDF_DIR = os.path.join(E.path('output'), '個人成績PDF')
ANN_DIR = os.path.join(E.path('output'), '赤入れ答案')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

esc = html.escape

CSS = """
@page{size:A4;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Hiragino Kaku Gothic ProN",sans-serif;color:#22304a;line-height:1.6;font-size:10.5pt}
.sheet{padding:13mm 14mm;page-break-after:always}
header{border-bottom:2.5px double #22304a;padding-bottom:4mm;display:flex;
       justify-content:space-between;align-items:flex-end;gap:6mm}
.course{font-size:8.5pt;letter-spacing:.12em;color:#76674d;font-weight:700}
h1{font-size:16.5pt;font-weight:800;margin-top:1mm}
.who{font-size:11pt;margin-top:1.5mm}.who b{font-size:13pt}
.who .id{font-family:ui-monospace,monospace;color:#76674d;margin-right:4mm}
.total{border:2.5px solid #c73e3a;color:#c73e3a;text-align:center;padding:2mm 6mm;
       border-radius:2mm;min-width:34mm}
.total .lab{font-size:7.5pt;font-weight:700;letter-spacing:.1em}
.total .num{font-size:26pt;font-weight:800;line-height:1.1}
.total .num small{font-size:10pt}
h2{font-size:11.5pt;font-weight:800;margin:6mm 0 2mm;page-break-after:avoid}
table{width:100%;border-collapse:collapse}
.qsum td,.qsum th{border:1px solid #d8cfba;text-align:center;padding:1.2mm 0;font-size:9.5pt}
.qsum th{background:#fbf8f0;font-weight:700}
.qsum .full{color:#2c5444;font-weight:700}.qsum .zero{color:#c73e3a;font-weight:700}
.detail td,.detail th{border-bottom:1px solid #d8cfba;padding:1.1mm 1.8mm;font-size:8.2pt;
                      vertical-align:top;text-align:left}
.detail th{border-bottom:1.8px solid #22304a}
.detail .k{font-family:ui-monospace,monospace;white-space:nowrap;font-weight:600}
.detail .s{font-family:ui-monospace,monospace;text-align:center;font-weight:700;white-space:nowrap}
.box{border:1px solid #d8cfba;background:#fbf8f0;padding:2.5mm 3.5mm;font-size:9pt}
.aibox{border:1.2px solid #3d6b8c;background:#eaf2f8;color:#1e3d52;padding:2.5mm 3.5mm;
       font-size:9pt;border-radius:1mm}
.notice{border:1.2px solid #b08c3d;background:#f8f1dd;color:#6a5420;padding:2mm 3.5mm;
        font-size:8.2pt;margin-top:4mm;border-radius:1mm}
.ans{page-break-before:always}
.ans img{width:100%;display:block}
"""

# 返却告知の必須文（AIの読み間違いを前提に、照合と申告を促す）
NOTICE = ('この採点はAIによる速報です。<b>AIは手書きの読み間違いをすることがあります。</b>'
          '必ずご自身の答案（次ページ以降の画像）と照合し、疑義があれば期限までに申告してください。')


def render(sid, rec, mp, q_items, q_max):
    rows = ''
    for q, keys in q_items.items():
        got = sum(rec['scores'][k][0] for k in keys if k in rec['scores'])
        cls = 'full' if got >= q_max[q] else ('zero' if got == 0 else '')
        rows += f'<td class="{cls}">{got}/{q_max[q]}</td>'
    head = ''.join(f'<th>{esc(q)}</th>' for q in q_items)

    det = ''
    for k, v in rec['scores'].items():
        pt, note = v[0], v[1]
        cls = 'full' if pt >= mp.get(k, 0) else ('zero' if pt == 0 else '')
        det += (f'<tr><td class="k">{esc(k)}</td>'
                f'<td class="s {cls}">{pt}/{mp.get(k, "?")}</td>'
                f'<td>{esc(str(note))}</td></tr>')

    ai = ''
    if rec.get('to_ai') or rec.get('ai_reply'):
        ai = (f'<h2>採点AIから</h2><div class="aibox">'
              f'<div style="font-size:8.2pt;color:#5a7d96">あなたの一言: {esc(str(rec.get("to_ai") or ""))}</div>'
              f'{esc(str(rec.get("ai_reply") or ""))}</div>')

    imgs = ''
    base = f'{sid}_{rec["official_name"].replace(" ", "_")}'
    for suffix in ('表', '裏'):
        p = os.path.join(ANN_DIR, f'{base}_{suffix}.jpg')
        if os.path.exists(p):
            imgs += f'<div class="sheet ans"><img src="file://{p}"></div>'

    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="sheet">
<header><div>
  <div class="course">{esc(E.CFG['course'])}</div>
  <h1>{esc(E.CFG['exam_name'])} 採点結果</h1>
  <div class="who"><span class="id">{esc(rec['official_sid'])}</span><b>{esc(rec['official_name'])}</b></div>
</div><div class="total"><div class="lab">TOTAL</div>
  <div class="num">{rec['total']}<small>/{E.CFG['full_marks']}</small></div></div>
</header>
<h2>大問別</h2><table class="qsum"><tr>{head}</tr><tr>{rows}</tr></table>
<h2>小問別の採点と読み取り内容</h2>
<table class="detail"><tr><th>小問</th><th>点</th><th>あなたの解答としてAIが読み取った内容</th></tr>{det}</table>
<h2>講評</h2><div class="box">{esc(rec.get('summary', ''))}</div>
{ai}
<div class="notice">{NOTICE}</div>
</div>{imgs}</body></html>"""


def main():
    agg = E.load_aggregate()
    mp = E.max_points()
    q_items, q_max = E.question_items(), E.question_max()
    os.makedirs(PDF_DIR, exist_ok=True)
    targets = sys.argv[1:]
    n = 0
    for sid, rec in sorted(agg.items()):
        if targets and sid not in targets:
            continue
        doc = render(sid, rec, mp, q_items, q_max)
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as tf:
            tf.write(doc)
            tmp = tf.name
        out = os.path.join(PDF_DIR, f'{sid}_{rec["official_name"].replace(" ", "_")}.pdf')
        subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={out}', f'file://{tmp}'],
                       check=True, capture_output=True)
        os.unlink(tmp)
        n += 1
    print(f'{n}件の成績PDFを生成: {PDF_DIR}')


if __name__ == '__main__':
    main()
