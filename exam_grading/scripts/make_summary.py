#!/usr/bin/env python3
"""教員用の採点サマリ（HTML）と採点結果Excelを生成する.

出力:
  .output/採点サマリレポート.html   統計・分布・大問別得点率・要確認一覧・インジェクション一覧・AI返信一覧
  .output/<テスト名>採点結果.xlsx   成績一覧 / 統計 / flags一覧（openpyxl があるとき）
  .output/学生コメント_返信用.xlsx  「教員に一言」への返信記入用（openpyxl があるとき）
"""
import html
import os
import statistics as st

import examlib as E

OUT = E.path('output')
esc = html.escape
REVIEW_KEYWORDS = ('判読困難', '判読不能', '基準外', '裁量', '別解')


def histogram(totals, width=10):
    full = E.CFG['full_marks']
    bins = {}
    for t in totals:
        lo = min(int(t) // width * width, full - width if full % width == 0 else full)
        bins[lo] = bins.get(lo, 0) + 1
    return [(lo, bins.get(lo, 0)) for lo in range(0, full, width)]


def main():
    agg = E.load_aggregate()
    mp, q_items, q_max = E.max_points(), E.question_items(), E.question_max()
    totals = [v['total'] for v in agg.values()]
    n = len(totals)
    if n == 0:
        print('集約データが空です')
        return

    stats = {
        '人数': n,
        '平均': round(st.mean(totals), 1),
        '中央値': st.median(totals),
        '標準偏差': round(st.pstdev(totals), 1),
        '最高': max(totals),
        '最低': min(totals),
        '満点者': sum(1 for t in totals if t >= E.CFG['full_marks']),
        '60点未満': sum(1 for t in totals if t < 60),
    }

    # 大問別得点率
    qrate = {}
    for q, keys in q_items.items():
        got = sum(v['scores'][k][0] for v in agg.values() for k in keys if k in v['scores'])
        qrate[q] = round(100 * got / (q_max[q] * n), 1)

    # flags 分類
    review, injection = [], []
    for sid, v in sorted(agg.items()):
        for fl in v.get('flags', []):
            s = str(fl)
            row = (v['official_sid'], v['official_name'], s)
            if '指示文' in s:
                injection.append(row)
            elif any(k in s for k in REVIEW_KEYWORDS):
                review.append(row)

    def table(rows, headers):
        h = ''.join(f'<th>{esc(x)}</th>' for x in headers)
        b = ''.join('<tr>' + ''.join(f'<td>{esc(str(c))}</td>' for c in r) + '</tr>' for r in rows)
        return f'<table><tr>{h}</tr>{b}</table>'

    bars = ''
    for lo, c in histogram(totals):
        w = int(320 * c / max(1, max(x[1] for x in histogram(totals))))
        bars += (f'<div class="bar"><span class="lab">{lo}〜{lo+9}</span>'
                 f'<span class="fill" style="width:{w}px"></span><span>{c}</span></div>')

    doc = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<title>{esc(E.CFG['exam_name'])} 採点サマリ</title><style>
body{{font-family:"Hiragino Kaku Gothic ProN",sans-serif;color:#22304a;background:#f4f1e8;
      margin:0;line-height:1.7}}
.wrap{{max-width:1000px;margin:0 auto;padding:28px 32px 64px}}
h1{{font-size:21px;border-bottom:3px double #22304a;padding-bottom:8px}}
h2{{font-size:15px;margin:26px 0 8px;border-left:6px solid #c73e3a;padding-left:10px}}
table{{border-collapse:collapse;background:#fff;font-size:13px;width:100%}}
th,td{{border:1px solid #d8cfba;padding:4px 10px;text-align:left}}
th{{background:#ece5d3}}
.stats{{display:flex;flex-wrap:wrap;gap:10px}}
.stat{{background:#fff;border:1px solid #d8cfba;border-radius:6px;padding:8px 16px;min-width:100px}}
.stat b{{display:block;font-size:20px}}
.bar{{display:flex;align-items:center;gap:8px;font-size:12px;margin:2px 0}}
.bar .lab{{width:70px;text-align:right;color:#76674d}}
.bar .fill{{height:14px;background:#c73e3a;border-radius:2px}}
.note{{background:#f8f1dd;border:1px solid #b08c3d;border-radius:6px;padding:10px 14px;font-size:13px}}
</style></head><body><div class="wrap">
<h1>{esc(E.CFG['course'])} {esc(E.CFG['exam_name'])} 採点サマリ</h1>
<div class="stats">{''.join(f'<div class="stat">{esc(k)}<b>{v}</b></div>' for k, v in stats.items())}</div>
<h2>得点分布</h2>{bars}
<h2>大問別得点率</h2>
{table([(q, f'{r}%', f'満点{q_max[q]}') for q, r in qrate.items()], ['大問', '得点率', '配点'])}
<h2>教員確認が必要な項目（{len(review)}件）</h2>
<div class="note">これらは <b>make_review_html.py で画像付きHTMLにして教員判定を仰ぐこと</b>（必須工程）。</div>
{table(review, ['学籍番号', '氏名', '内容']) if review else '<p>なし</p>'}
<h2>採点AIへの指示文（プロンプトインジェクション）検出（{len(injection)}件）</h2>
<div class="note">いずれも無視して採点基準どおりに採点済み。処分対象ではなく、返信でユーモアを返すと好評。</div>
{table(injection, ['学籍番号', '氏名', '内容']) if injection else '<p>なし</p>'}
</div></body></html>"""

    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, '採点サマリレポート.html')
    open(p, 'w', encoding='utf-8').write(doc)
    print('保存:', p)

    try:
        from openpyxl import Workbook
    except ImportError:
        print('openpyxl が無いため Excel はスキップしました（pip install openpyxl）')
        return

    wb = Workbook()
    ws = wb.active
    ws.title = '成績一覧'
    keys = list(mp)
    ws.append(['学籍番号', '氏名', '合計'] + keys + ['講評', 'flags'])
    for sid, v in sorted(agg.items(), key=lambda x: x[1]['official_sid']):
        ws.append([v['official_sid'], v['official_name'], v['total']]
                  + [v['scores'].get(k, ['', ''])[0] for k in keys]
                  + [v.get('summary', ''), ' / '.join(map(str, v.get('flags', [])))])
    ws2 = wb.create_sheet('統計')
    for k, v in stats.items():
        ws2.append([k, v])
    ws2.append([])
    ws2.append(['大問', '得点率(%)', '配点'])
    for q, r in qrate.items():
        ws2.append([q, r, q_max[q]])
    xp = os.path.join(OUT, f'{E.CFG["exam_name"]}採点結果.xlsx')
    wb.save(xp)
    print('保存:', xp)

    wb2 = Workbook()
    ws3 = wb2.active
    ws3.title = '教員への一言'
    ws3.append(['学籍番号', '氏名', '合計', '教員への一言', '先生の返信（ここに記入）'])
    for sid, v in sorted(agg.items(), key=lambda x: x[1]['official_sid']):
        if v.get('to_teacher'):
            ws3.append([v['official_sid'], v['official_name'], v['total'], v['to_teacher'], ''])
    cp = os.path.join(OUT, '学生コメント_返信用.xlsx')
    wb2.save(cp)
    print('保存:', cp)


if __name__ == '__main__':
    main()
