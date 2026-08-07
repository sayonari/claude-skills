#!/usr/bin/env python3
"""答案スキャンへの赤入れ（大問ごとの ◯△✕ ＋ 得点、表面右上に合計点）.

全員同一レイアウトであることが前提。座標は 300dpi 基準で exam_config.json の annotate に定義する。

使い方:
  python3 annotate_answers.py            # 全員
  python3 annotate_answers.py 990001     # 学籍番号（数字部分）を指定
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

import examlib as E

OUTDIR = os.path.join(E.path('output'), '赤入れ答案')
RED = (200, 30, 30)
CFG_A = E.CFG['annotate']
FONT_PATH = CFG_A.get('font_path', '/System/Library/Fonts/Hiragino Sans GB.ttc')


def font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def draw_symbol(d, x, y, kind, r=42, w=7):
    """kind: 'o'=満点, 't'=部分点, 'x'=0点"""
    if kind == 'o':
        d.ellipse([x - r, y - r, x + r, y + r], outline=RED, width=w)
    elif kind == 't':
        d.polygon([(x, y - r), (x - r, y + r * 0.85), (x + r, y + r * 0.85)],
                  outline=RED, width=w)
    else:
        d.line([x - r, y - r, x + r, y + r], fill=RED, width=w)
        d.line([x - r, y + r, x + r, y - r], fill=RED, width=w)


def mark_kind(got, full):
    return 'o' if got >= full else ('x' if got == 0 else 't')


def annotate(sid, rec):
    q_items = E.question_items()
    q_max = E.question_max()
    sheet = rec['sheet']
    book, i = sheet.split('-')
    n = E.CFG['scan']['books'][book]
    pages = [
        (os.path.join(E.path('pages'), f'{book}_front', f'p-{int(i):02d}.jpg'),
         CFG_A['front_marks'], True),
        (os.path.join(E.path('pages'), f'{book}_back', f'p-{n + 1 - int(i):02d}.jpg'),
         CFG_A['back_marks'], False),
    ]
    os.makedirs(OUTDIR, exist_ok=True)
    name = f'{sid}_{rec["official_name"].replace(" ", "_")}'
    for src, marks, is_front in pages:
        if not os.path.exists(src):
            print(f'  !! 画像なし: {src}')
            continue
        im = Image.open(src).convert('RGB')
        d = ImageDraw.Draw(im)
        for q, (x, y) in marks.items():
            if q not in q_items:
                print(f'  !! annotate の "{q}" が items の大問名と一致しません（設定を確認）')
                continue
            got = sum(rec['scores'][k][0] for k in q_items[q] if k in rec['scores'])
            draw_symbol(d, x, y, mark_kind(got, q_max[q]))
            d.text((x + 60, y - 30), f'{got}/{q_max[q]}', fill=RED, font=font(46))
        if is_front:
            tx, ty = CFG_A.get('total_pos', [2150, 250])
            d.text((tx, ty), f'{rec["total"]}', fill=RED, font=font(110))
            d.text((tx + 5, ty + 120), f'/ {E.CFG["full_marks"]}', fill=RED, font=font(44))
        suffix = '表' if is_front else '裏'
        im.save(os.path.join(OUTDIR, f'{name}_{suffix}.jpg'), quality=88)


def main():
    agg = E.load_aggregate()
    targets = sys.argv[1:]
    n = 0
    for sid, rec in sorted(agg.items()):
        if targets and sid not in targets:
            continue
        annotate(sid, rec)
        n += 1
    print(f'{n}名分の赤入れ答案を生成: {OUTDIR}')


if __name__ == '__main__':
    main()
