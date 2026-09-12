#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""透析間隔検算スクリプト

使い方:
    python3 check_intervals.py <透析カレンダー.md>            # 全件
    python3 check_intervals.py <file> --from 2026-10-10 --to 2026-11-01

入力：`## セッション一覧` 見出し以下の Markdown 表。1行が1セッションで，先頭セルに ISO 日付を含むこと。
      日付セルが `~` の行は「通常の月水金透析が続く区間」の区切りで，間隔の連鎖をリセットする。
      2列目=場所，3列目=時刻（HH:MM-HH:MM，オーバーナイトは終了が翌日扱い），4列目=状態。
      「-」で始まる区切り行，ヘッダ行，日付を含まない行は無視する。

判定：
  ✗ 中3日以上        … 絶対に作らない（SKILL.md §2-A-1）
  ⚠ 中2日が2回連続   … 避ける。出発前の土曜に国内で1回追加する（§2-A-2）
  ℹ 実間隔 24h 未満  … 連日扱い。意図したものか確認
"""
import sys, re, datetime

WD = "月火水木金土日"

def parse(path):
    """`## セッション一覧` 見出し以下の表だけを読む。
    日付セルが `~` の行は「区間の区切り」（通常の月水金透析が続く区間）として
    間隔の連鎖をリセットする。"""
    rows = []
    inside = False
    for raw in open(path, encoding="utf-8"):
        if raw.startswith("## "):
            inside = raw.startswith("## セッション一覧")
            continue
        if not inside or not raw.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if cells and cells[0].startswith("~"):
            rows.append(dict(brk=True))
            continue
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", cells[0] if cells else "")
        if not m:
            continue
        d = datetime.date(*map(int, m.groups()))
        place = cells[1] if len(cells) > 1 else "?"
        tm = cells[2] if len(cells) > 2 else ""
        state = cells[3] if len(cells) > 3 else ""
        t = re.search(r"(\d{1,2}):(\d{2})\s*[-\u2013~]\s*(\d{1,2}):(\d{2})", tm)
        start = end = None
        if t:
            sh, sm, eh, em = map(int, t.groups())
            start = datetime.datetime.combine(d, datetime.time(sh, sm))
            end = datetime.datetime.combine(d, datetime.time(eh, em))
            if end <= start:                      # オーバーナイト
                end += datetime.timedelta(days=1)
        rows.append(dict(brk=False, date=d, place=place, time=tm, state=state,
                         start=start, end=end))
    return rows


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    path = sys.argv[1]
    lo = hi = None
    if "--from" in sys.argv:
        lo = datetime.date.fromisoformat(sys.argv[sys.argv.index("--from") + 1])
    if "--to" in sys.argv:
        hi = datetime.date.fromisoformat(sys.argv[sys.argv.index("--to") + 1])

    rows = parse(path)
    if lo: rows = [r for r in rows if r.get("brk") or r["date"] >= lo]
    if hi: rows = [r for r in rows if r.get("brk") or r["date"] <= hi]
    if not [r for r in rows if not r.get("brk")]:
        print("セッションが1件も読み取れませんでした。`## セッション一覧` の表の1列目に YYYY-MM-DD を入れてください。")
        sys.exit(1)

    print("| 日付 | 場所 | 時刻 | 状態 | 間隔 | 実時間 | 判定 |")
    print("|---|---|---|---|---|---|---|")
    problems, missing = [], []
    prev = None        # 直前のセッション
    prev_gap = None    # 直前の間隔（中N日）
    prev2 = None       # 2つ前のセッション
    for r in rows:
        if r.get("brk"):
            print("| ~ | *（通常の月水金オーバーナイトが続く区間・検算対象外）* | | | | | |")
            prev = prev2 = prev_gap = None
            continue
        if not r["start"]:
            missing.append(r)
        gap = hours = ""
        verdict = ""
        n = None
        if prev is None:
            gap = "—"
        else:
            n = (r["date"] - prev["date"]).days - 1
            gap = "連日" if n == 0 else ("同日" if n < 0 else "中%d日" % n)
            if prev["end"] and r["start"]:
                h = (r["start"] - prev["end"]).total_seconds() / 3600
                hours = "%.0fh" % h
                if 0 <= h < 24:
                    verdict += "ℹ24h未満 "
            if n >= 3:
                verdict += "✗中3日以上 "
                problems.append("✗ %s → %s が中%d日。中3日以上は不可（SKILL.md §2-A-1）"
                                % (prev["date"], r["date"], n))
            if n == 2 and prev_gap == 2:
                verdict += "⚠中2日2連続 "
                problems.append(
                    "⚠ %s → %s → %s が中2日の2連続。出発前の土曜に国内で1回追加して受ける"
                    "（金・土の連日になるが国内なら追加費用なし・毒素もよく抜ける／SKILL.md §2-A-2）"
                    % (prev2["date"], prev["date"], r["date"]))
        print("| %s(%s) | %s | %s | %s | %s | %s | %s |"
              % (r["date"], WD[r["date"].weekday()], r["place"], r["time"] or "—",
                 r["state"] or "—", gap, hours or "—", verdict.strip() or "✅"))
        prev2, prev, prev_gap = prev, r, n

    print()
    if problems:
        print("## 要対応")
        for p in problems:
            print("- " + p)
    else:
        print("## 要対応：なし（中3日以上なし・中2日の2連続なし）")

    if missing:
        print("\n## 時刻未定（実時間を検算できていないセッション）")
        for r in missing:
            print("- %s(%s) %s %s" % (r["date"], WD[r["date"].weekday()], r["place"], r["state"]))


if __name__ == "__main__":
    main()
