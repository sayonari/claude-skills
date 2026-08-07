#!/usr/bin/env python3
"""共通ライブラリ: exam_config.json の読み込みとパス解決.

各スクリプトはこれを import して設定を取る。
使う前に exam_config.example.json をコピーして exam_config.json を作り、テストに合わせて書き換えること。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, 'exam_config.json')


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise SystemExit(
            f'設定ファイルがありません: {CONFIG_PATH}\n'
            f'exam_config.example.json をコピーして作成し、テストに合わせて書き換えてください。')
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)


CFG = load_config()


def path(key):
    """設定の paths.<key> を絶対パスで返す。"""
    return os.path.abspath(os.path.join(HERE, CFG['paths'][key]))


def items():
    """小問ID -> 定義 の dict（_comment を除く）。"""
    return {k: v for k, v in CFG['items'].items() if not k.startswith('_')}


def max_points():
    """小問ID -> 配点。"""
    return {k: v['max'] for k, v in items().items()}


def question_items():
    """大問名 -> [小問ID, ...]（config の記載順を保つ）。"""
    out = {}
    for k, v in items().items():
        out.setdefault(v['q'], []).append(k)
    return out


def question_max():
    """大問名 -> 満点。"""
    mp = max_points()
    return {q: sum(mp[k] for k in ks) for q, ks in question_items().items()}


def sheets():
    """(sheet_id, 表ページ番号, 裏ページ番号, 冊) を順に返す。

    片面一括スキャンの前提: 表は正順・裏は逆順（表 i ↔ 裏 N+1-i、p-01 始まり）。
    """
    for book, n in CFG['scan']['books'].items():
        for i in range(1, n + 1):
            yield (f'{book}-{i:02d}', i, n + 1 - i, book)


def all_sheet_ids():
    return [s[0] for s in sheets()]


def load_batches():
    """採点JSON を全部読んで [(ファイル名, レコード), ...] を返す。"""
    import glob
    recs = []
    for f in sorted(glob.glob(os.path.join(path('batches'), 'batch*.json'))):
        with open(f, encoding='utf-8') as fp:
            for rec in json.load(fp):
                recs.append((os.path.basename(f), rec))
    return recs


def save_batch(filename, records):
    with open(os.path.join(path('batches'), filename), 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=1)


def load_aggregate():
    with open(path('aggregate'), encoding='utf-8') as f:
        return json.load(f)


def check_config():
    """設定の自己検査（配点合計・クロップ座標）。"""
    errs = []
    total = sum(max_points().values())
    if total != CFG['full_marks']:
        errs.append(f'配点合計 {total} が full_marks {CFG["full_marks"]} と不一致')
    w, h = CFG['scan']['page_size_px']
    for side in ('front', 'back'):
        for name, box in CFG['crop'].get(side, {}).items():
            if name.startswith('_'):
                continue
            l, t, r, b = box
            if not (0 <= l < r <= w and 0 <= t < b <= h):
                errs.append(f'crop.{side}.{name} の座標がページ範囲外: {box}')
    return errs


if __name__ == '__main__':
    errs = check_config()
    print(f'{CFG["course"]} / {CFG["exam_name"]}')
    print(f'小問 {len(items())}個 / 合計 {sum(max_points().values())}点 / 答案 {len(all_sheet_ids())}枚')
    if errs:
        print('設定エラー:')
        for e in errs:
            print(' -', e)
    else:
        print('設定OK')
