# scripts/ — 採点スクリプト雛形

**そのままでは動かない。** テストごとに `exam_config.json` を作り、座標・小問ID・配点を書き換えて使う。
科目のプロジェクトへコピーして改変するのが前提（このスキル内のファイルは編集しない）。

## セットアップ

```bash
cp -r <このスキル>/scripts <科目プロジェクト>/AI作業場/scripts
cd <科目プロジェクト>/AI作業場/scripts
cp exam_config.example.json exam_config.json
# exam_config.json を編集（course / exam_name / full_marks / scan / crop / items / annotate）
python3 examlib.py        # 設定の自己検査（配点合計・クロップ座標）
```

必要なパッケージ: `pillow`（必須）、`openpyxl`（Excel出力を使う場合）

## 実行順

| # | コマンド | 内容 |
|---|---|---|
| 1 | `pdftoppm -jpeg -r 300 scan/1_表面.pdf .output/採点/pages/1_front/p` | ページ画像化（冊ごと・表裏ごと） |
| 2 | `python3 crop_answers.py` | 大問クロップ生成（autocontrast付き） |
| 3 | （エージェントで本人特定OCR） | → `sheet_map.json` |
| 4 | （エージェントで並列採点） | → `採点JSON/batch*.json` |
| 5 | `python3 verify_scores.py --fix` | **機械検証（必須）**。教員確認すべき flags も一覧表示 |
| 6 | `python3 aggregate.py` | 集約 → `採点結果_集約.json` |
| 7 | `python3 make_review_html.py --init` → 内容を記入 → `python3 make_review_html.py` | **★教員確認HTML（必須工程）** |
| 8 | `patch.json` を書いて `python3 apply_patch.py --dry` → `python3 apply_patch.py` | 教員判定・方針変更の反映 |
| 9 | 5〜6 を再実行 | 再検証・再集約 |
| 10 | `python3 annotate_answers.py` | 赤入れ答案 |
| 11 | `python3 make_student_pdfs.py` | 個人成績PDF（Chromeヘッドレス） |
| 12 | `python3 make_summary.py` | サマリHTML・Excel・コメント返信用Excel |
| 13 | `appsscript_return_template.gs` | Classroom/Drive 返却（**冒頭の教訓コメントを必ず読む**） |

## ファイル

| ファイル | 内容 |
|---|---|
| `exam_config.example.json` | 設定ファイルの雛形。**ここを書き換えるのが作業の中心** |
| `examlib.py` | 設定読込・パス解決・答案ID列挙・配点導出の共通ライブラリ |
| `crop_answers.py` | 大問クロップ生成（表裏ペアリング込み） |
| `verify_scores.py` | 小問網羅・上限・合計・全件網羅の機械検証 |
| `aggregate.py` | 採点JSON・本人特定・コメント・AI返信の集約 |
| `make_review_html.py` | **★教員確認HTML（画像埋め込み）の生成** |
| `apply_patch.py` | 採点JSONへのパッチ適用（理由を転記文とflagsに残す） |
| `annotate_answers.py` | 赤入れ答案の生成 |
| `make_student_pdfs.py` | 個人成績PDFの生成 |
| `make_summary.py` | 教員用サマリHTML・Excel |
| `appsscript_return_template.gs` | 返却用 Apps Script（事故防止の教訓コメント入り） |

## 原則

- **採点JSONは原本。** 手で書き換えず、必ず `apply_patch.py` で理由付きで変更する。
- **合計はスクリプトで再計算する。** AIの合計計算ミスは実測1/131件。
- **迷った採点は教員確認HTMLへ。** AIの裁量で部分点を付けない。
