#!/usr/bin/env python3
"""答案の大問クロップ生成（「大問クロップ + autocontrast」方式）.

前提:
  - pdftoppm でページ画像を作ってあること
      pdftoppm -jpeg -r 300 "scan/1_表面.pdf" ".output/採点/pages/1_front/p"
  - 表は正順・裏は逆順（片面一括スキャンの標準的な挙動）

使い方:
  python3 crop_answers.py            # 全答案
  python3 crop_answers.py 1-01 2-05  # 指定答案のみ

要設定: exam_config.json の crop / scan
"""
import os
import sys

from PIL import Image, ImageOps

import examlib as E

PAGES = E.path('pages')
CROPS = E.path('crops')


def crop_sheet(sheet_id, front_page, back_page, book, only=None):
    out = os.path.join(CROPS, sheet_id)
    os.makedirs(out, exist_ok=True)
    targets = [
        (os.path.join(PAGES, f'{book}_front', f'p-{front_page:02d}.jpg'), E.CFG['crop']['front']),
        (os.path.join(PAGES, f'{book}_back', f'p-{back_page:02d}.jpg'), E.CFG['crop']['back']),
    ]
    for src, regions in targets:
        if not os.path.exists(src):
            print(f'  !! 画像がありません: {src}')
            continue
        im = Image.open(src)
        for name, box in regions.items():
            if name.startswith('_') or (only and name not in only):
                continue
            # autocontrast は薄い鉛筆書きの可読性を大きく上げる（必須）
            ImageOps.autocontrast(im.crop(tuple(box))).save(
                os.path.join(out, f'{name}.jpg'), quality=90)


def main():
    errs = E.check_config()
    if errs:
        print('設定エラー:', *errs, sep='\n - ')
        return 1
    targets = set(sys.argv[1:]) or None
    n = 0
    for sheet_id, fp, bp, book in E.sheets():
        if targets and sheet_id not in targets:
            continue
        crop_sheet(sheet_id, fp, bp, book)
        n += 1
        print(sheet_id, 'done')
    print(f'{n}枚のクロップを生成: {CROPS}')
    print('※ 数枚を目視し、大問が切れていないか・表裏が一致しているか必ず確認すること')
    return 0


if __name__ == '__main__':
    sys.exit(main())
