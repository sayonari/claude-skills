---
name: paper_writing
description: 音声言語情報処理系の国際会議論文・ジャーナル論文（Speech Communication、IEEE/ACM Trans.、Computer Speech and Language、Interspeech、ICASSP等）の執筆・推敲・査読対応に用いる汎用スキル。ハルシネーション防止、参考文献検証、数値トレーサビリティ、読者層に合わせた英語表現、セクション構造、LaTeX/compile.sh運用などをカバー。論文執筆プロジェクトでは必ず参照すること。
---

# 論文執筆スキル（Claude 用）

音声言語情報処理系の国際会議論文・ジャーナル論文（Speech Communication、IEEE/ACM Trans., Computer Speech and Language、Interspeech、ICASSP 等）を執筆する際に用いる**汎用ルール**をまとめたスキルファイル。

**使い方**：論文執筆・推敲・査読対応時に必ず参照すること。プロジェクト固有の詳細（ファイル名・cite_key・章番号等）は含めず、**どの論文執筆作業にも適用できる**形で記述する。

---

## 0. 表記の大原則

- 日本語原稿の**句読点は必ず「，．」（全角カンマ・ピリオド）**。「、。」は使わない（引用など原文保持箇所を除く）

## 1. 全体方針

### 1.1 完全新規作成 vs 修正
- 既存原稿があっても、品質を確保するなら完全新規作成が有効
- 参照元（修士論文、国際会議原稿、既存原稿）からデータ・数値は引用するが、文章は一から書く

### 1.2 実験制約への対応
- 「再実験不可」の制約下でも以下は可能:
  - 既存混同行列からの派生指標算出（MAE, RMSE, within-one-bin accuracy）
  - 理論的ベースラインの計算（duration-prior baseline等、Pythonスクリプトで算出）
  - Bootstrap CI（既存混同行列または予測結果からリサンプリング）
  - **McNemar検定／paired CI**（※ サンプルごとのペア予測結果ファイルが残っている場合のみ実施可。**混同行列だけでは原理的に計算不可能**。ファイル不在で実施したと記述するとハルシネーション → §8.4.X 参照）
  - 既存データの再集計・再解釈

---

## 1.5 標準ワークフロー【論文執筆のend-to-end手順】

論文執筆プロジェクトを立ち上げてから投稿完了までの**標準的な進行順**。各ステップで参照すべき詳細ルールは後述の該当節にリンクする。

AI・ユーザーの役割分担を明記する。AI は「情報を整理・提示」し、**重要な判断はユーザーが承認**する。

### Phase A. プロジェクト立ち上げ

**A-1. プロジェクトフォルダ作成**（AI 実行）
- `/make_project` を実行し、「論文執筆プロジェクトですか？」に Y と回答
- 標準フォルダ（`latex原稿/`, `_ref/`, `_AI用_関連各種データ/`, `参考文献確認作業/`, `論文修正作業用スクリプト/`, `_過去のもの/`）が自動生成される（§8.7）
- `CLAUDE.md` に `/paper_writing` スキル参照が自動挿入される

**A-2. 情報源の配置**（ユーザー実行）
- `_ref/` 配下に以下を配置：
  - 修士論文／博士論文（本研究の土台）
  - 過去の関連**国際会議発表原稿**（英語・同じ研究ラインの既発表）
  - 過去の関連**国内学会発表原稿**（日本語・同じ研究ラインの既発表）
  - 既存投稿稿（あれば）
  - 関連する実験データ・混同行列・予測結果ファイル等
- これらが**全ての数値・事実の情報源**となる（§8.4.Y）
- 原則として `_ref/` は読み取り専用で扱う（AI は書き換えない）

**A-3. 情報源のスキャンと執筆方針ヒアリング**（AI 実行）
- AI が `_ref/` 全ファイルを `pdftotext` 等で読み、以下を整理してユーザーに提示：
  - 本論文で扱える主題・新規性の候補
  - 使える実験結果・数値・混同行列
  - 著者候補・所属
  - 想定される貢献点（contributions）
- ユーザーに以下を確認：
  1. 「投稿先ジャーナル／会議はどこを想定していますか？」
  2. 「本論文での新規性・主要な主張は何ですか？」
  3. 「筆頭著者・共著者・所属をお教えください」
  4. 「タイトルの候補はありますか？」
  5. 「目標分量（pages）・投稿締切はいつですか？」

**A-4. 投稿先テンプレートの取得と配置**（AI 実行）
- 投稿先公式サイトまたは CTAN から LaTeX テンプレートを入手して `latex原稿/` に配置（§6.5 参照）
- documentclass を確認 → `compile.sh` を §6.3 の該当バージョンに差し替え
- 投稿規定（author guidelines）を読み、以下を把握：
  - ページ数・字数制限
  - 必要な追加ファイル（Highlights、Cover Letter、Graphical Abstract 等）
  - 文献スタイル（Harvard / numbered）
  - 図表フォーマット（カラー可否、解像度）
- **修正履歴マーキング機構を組み込む**（§6.6）：`main.tex` プリアンブルに `\rev{}` `\revdel{}` マクロと `\ifshowrevs` トグルを追加（共著者・指導教員レビュー時に修正箇所を赤文字表示するため）

**A-5. 分野文献調査の実施**（AI 実行 → ユーザー確認）【強く推奨】
- **`field_literature_survey` skill を起動**して、投稿先・関連会議の過去5年分の論文を多数精査
  - スコープ（投稿先・関連会議・年度・キーワード・本数）をユーザーと合意
  - 文献を収集し、観察項目（タイトル／Abstract／Intro／Method／Results／Discussion／用語／文体／図表）ごとにノート化
  - 成果物：`_AI用_関連各種データ/分野文献調査/field_style_notes.md` ほか
- **目的**：「別分野の人が書いた論文」のような原稿になることを防ぎ、投稿先コミュニティに馴染んだ文体・語彙・構成を獲得する
- 投稿締切が迫っている場合は短縮版（20本程度、abstract+intro のみ）で良い
- 本フェーズの成果物は Phase C 以降で常時参照する
- 詳細は `field_literature_survey` skill を参照

### Phase B. 情報整理・検証準備

**B-1. 情報源の数値・事実の抽出とトレーサビリティ構築**（AI 実行 → ユーザー確認）
- `_ref/` 内の全数値・主張を抽出し、`_AI用_関連各種データ/表・数値の参照元情報.md` に記入（§8.8.1）
- 各値を (A) 直記載 / (B) 派生計算 / (C) 要 Python 検証 / (X) 未裏付け に分類
- ユーザーに確認：「この値の一覧で漏れ・誤りはありますか？」

**B-2. 関連研究の候補収集とハルシネーション検証**（AI 実行 → ユーザー確認）
- 本論文の位置づけに必要な先行研究を列挙（§3.1, §3.2）
- 各文献について（§3.1.3）：
  - タイトル・著者・DOI・年・掲載誌を `参考文献確認作業/参考文献チェック.xlsx` に記入
  - PDF を `参考文献確認作業/PDFs/[cite_key]_[1stAuthor姓]_[Venue][Year].pdf` にダウンロード
  - 取得できない文献は `user_download/` 経由でユーザーに依頼（§3.1.6）
- ユーザー確認依頼：「この先行研究リストで漏れはありますか？／必須で入れるべき文献はありますか？」

**B-3. 比較表（Related Work Table）の設計**（AI 実行 → ユーザー確認）
- 本論文の位置づけを一目で示す比較表を設計（§3.2.1）
- 列候補：Study / Task / Output / Features / Horizon / Online / Language 等
- 各セルを `参考文献チェック.xlsx` の Sheet 2 で**個別に検証**（§3.2.3）
- モデル名とタスク名の混同に注意（§3.2.3）

**B-4. 専門用語の統一**（AI 実行 → ユーザー確認）
- `_AI用_関連各種データ/専門用語.md` に日英対訳・表記ゆれ・初出管理を整理（§9.2）
- 初出時にフルスペルアウトすべき略語をリスト化
- 類似用語（utterance / speech / turn / dialog 等）の使い分けルールを記録
- ユーザー確認依頼：「用語の訳・表記で違和感のあるものはありますか？」

### Phase C. 本文執筆（§2 執筆順序に従う）

**C-1〜C-11. 章単位の執筆**（AI 実行 → ユーザー章ごとレビュー）
- §2 の推奨順序（Task/Data → Method → Experiments → Results → Related Work → Online Prototype → Discussion → Introduction → Conclusion → Abstract → Appendix）に沿って章ごとに書く
- **各章完成ごと**にユーザーにレビュー依頼（査読サブエージェントに頼らず、ユーザー主導レビューを推奨。§5 参照）
- 表現の選択が分かれる箇所は**候補1／候補2**で提示（§8.10）
- 構造ルール：subsection 2〜4個、subsubsection 非推奨、`\textbf{項目名.}` 段落頭ラベル禁止（§8.6）
- 英語表現：専門用語は残し、**論文以外で多用される形式的・文語的語彙**は平易な代替に（§8.5）
- **抽象的・曖昧記述の禁止**（§8.5.5）：`the same quantity` / `conversion pipeline` / `affects timing quality` のような抽象語でぼかさず、「何が」「何を」「どのくらい」を明示
- **分野文献調査ノートを参照**（Phase A-5 の成果物）：投稿先コミュニティの文体・語彙・構成・典型表現を確認しながら書く
- em-dash（`---`）禁止、代替手法（カンマ、括弧、コロン等）を使用（§8.6.5）
- 各数値は §8.8.1 の分類に従い、X（未裏付け）は絶対に書かない
- 引用は本文中 `\citep{}`、表内 `\cite{}`（§3.2.5）
- **レビュー対応中の修正は `\rev{}` で囲む**（§6.6）：共著者・指導教員からの指摘に基づく追記・修正テキストは必ず `\rev{...}` でラップ（赤文字表示）。レビュアーが変更箇所を一目で確認できるようにする

### Phase D. 検証・最終化

**D-1. 数値検証スクリプトの作成**（AI 実行）
- Python 検証が必要な値（C 分類）は `_AI用_関連各種データ/数値計算検証/` に配置（§8.8.2）
- ランダム性を含む計算は 10 seed 以上で安定性確認（§8.8.3）
- スクリプト + `計算過程の説明.md` を**永続保存**（投稿後の再検証に使う）

**D-2. ハルシネーション最終除去**（AI 実行 → ユーザー確認）
- `_ref` 裏付けのない数値・統計値・先行研究言及を削除または置換（§8.4.Y, §8.4.X, §3.1.7）
- 削除した値の近接記述（差分値・相対評価・因果説明）も**連動して修正**
- 削除したものの一度復活させる場合は **再ハルシネーション防止**手順（§8.8.4）を徹底

**D-3. コンパイル**（AI 実行）
- `latex原稿/compile.sh` を実行（§6.3）
- エラーは `main.log` の**最初のエラー**から解消（後続は連鎖であることが多い）
- **必ず `compile.sh` 経由**。`pdflatex` や `latexmk` を直接呼ばない
- 警告（Warning）も可能な限り解消（hyperref 重複定義、undefined references 等）

**D-4. `.tex` ソース通読**（AI + ユーザー共同）
- 章ごとにユーザーが通読・修正指示（§9.5）
- 一括置換の副作用（collocation 破壊、表内 `\cite` の変換事故 等）をチェック
- 語の重複、英語として不自然な組み合わせを洗い出す

**D-5. PDF通読**（ユーザー主導、AI は補助）
- コンパイル後 PDF を1ページ目から末尾まで通読（§9.5.X）
- レイアウト崩れ・ページ跨ぎ・連番不整合・Highlightsページ余白を検出
- 印刷時の読みやすさ（色依存の図等）も確認

### Phase E. 投稿準備

**E-1. 著者情報・メタデータの記述**（AI 実行 → ユーザー確認）
- CRediT authorship contribution statement（§8.9）
- Data availability statement（データ公開範囲・入手方法）
- Declaration of competing interest
- Acknowledgments（科研費番号・プロジェクト資金等）
- Highlights（Elsevier 系で必須、3〜5項目、各85字以内）
- Keywords（5〜7語、分野が分かるように）

**E-2. 補助ファイル最終整備**
- `参考文献リスト.md`（指導教員確認用、§9.1）
- `図表作成依頼.md`（未完成の図表がある場合、§9.3）
- 全ての補助ファイルを `_AI用_関連各種データ/` 配下に集約

**E-3. 投稿パッケージ作成**（AI 実行 → ユーザー最終確認）
- **修正履歴マーキングの無効化【必須】**（§6.6.5）：
  1. `main.tex` プリアンブルの `\showrevstrue` を `\showrevsfalse` に書き換え
  2. `./compile.sh` で再コンパイル、PDF を目視で赤文字が消えているか確認
  3. `grep -rn '\\rev{\|\\revdel{' latex原稿/sections/` で残存件数を記録、スポット確認
  4. （推奨）保険的削除を別ブランチで実行：`perl -i -pe 's/\\rev\{([^{}]*)\}/$1/g; s/\\revdel\{[^{}]*\}//g'`
- 投稿先の指定フォーマットに従う：
  - Elsevier Editorial System: `main.pdf` + ソース一式（`.tex`, `.bib`, 図ファイル）
  - IEEE Manuscript Central: zip で一式
  - ACL / Interspeech: 事前に pdf-only か ソース込みか確認
  - arXiv 同時公開の場合は別途 arXiv 用パッケージ
- Cover Letter（必要な場合）
- 添付ファイルチェックリストを確認
- 最終版 PDF をバックアップ（`_過去のもの/submission_v1/`）

### Phase F. 投稿後対応（参考）

**F-1. 査読対応**
- 査読コメントに対して Response Letter を作成（`§4 査読対応パターン`）
- 変更箇所を原稿内で色付け／下線等でハイライト → **§6.6 の `\rev{}` 機構を再有効化**（`\showrevstrue`）して修正箇所を赤文字表示。査読者・編集者が変更箇所を即座に確認できる
- 最終版（acceptance 後の camera-ready）提出時には再度 `\showrevsfalse` に切替
- Major Revision / Minor Revision に応じて計画的に対応

**F-2. 知見の蓄積**
- プロジェクトの `KNOWLEDGE.md` / `MEMORY.md` に「今回の教訓」を記録
- 汎用化できる知見は **本スキルファイル自体を更新**（AIに依頼、ユーザー確認）

---

## 2. 執筆順序

### 推奨順序
1. **Task Definition / Data** — 事実ベースで最も書きやすい
2. **Method** — 技術的詳細
3. **Experiments** — 実験設定
4. **Results** — 最大ボリューム、数値の正確性が最重要
5. **Related Work** — 文献調査完了後に書く
6. **Online Prototype / Demo** — 定性的記述
7. **Discussion** — 査読対応の核。限界を正直に認めつつ建設的に
8. **Introduction** — 全体を把握してから書く
9. **Conclusion** — Introと対応させる
10. **Abstract** — 最後に書く（全数値の整合性チェック）
11. **Appendix** — 補足情報

---

## 3. 先行研究・参考文献

### 3.1 ハルシネーション防止【最重要】

**AIによる参考文献の捏造・不正確記載は研究倫理上の重大問題**。特にAIが執筆した論文原稿では、存在しない論文や事実と異なる記述が混入するリスクが高い。**投稿前に必ず全文献を検証する**。

#### 3.1.1 検証の原則
- 全ての参考文献について、**オフィシャルサイト（出版社・学会・arXiv等）に直接アクセス**して実在確認
- **DOI・URL・タイトル・著者・年・掲載誌・ページが全て一致**することを確認
- **PDFが取得できる場合は必ずダウンロード**し、本文での引用記述がPDFの実内容と合致するか確認
- **PDFが取得できない場合はせめてアブストラクトを読み、本文の記述と矛盾しないか確認**

#### 3.1.2 検証作業の専用フォルダ構成

プロジェクトルートに `参考文献確認作業/` フォルダを作成し、以下を格納：

```
参考文献確認作業/
├── 参考文献チェック.xlsx    ← 全検証結果を記入
└── PDFs/                      ← ダウンロードしたPDFを保存
    ├── [cite_key]_[venue][year].pdf
    ├── [cite_key]_[venue][year].pdf
    └── ...
```

**PDFファイル名の命名規則**：
- `[cite_key]_[1stAuthor姓]_[venue略称][year].pdf` の形式
- 例：`turngpt_Ekstedt_EMNLP2020.pdf`、`vap1_Ekstedt_Interspeech2022.pdf`、`syokiapproch_Raux_SIGDIAL2008.pdf`
- cite_key だけだと内容が分かりにくいため、**1st author の姓 + venue (会議/ジャーナル名の略称) + 年** を含める
- venue 略称の例：Interspeech, ICASSP, EMNLP, NeurIPS, LREC, SIGDIAL, TASLP, CSL（Computer Speech & Language）, IWSDS, NLP（言語処理学会） など
- 1st author は姓のみ（英字1語）、スペースやハイフンがある場合は除去

#### 3.1.3 参考文献チェックExcelの構成

| 列 | 内容 |
|---|---|
| ID | 通し番号 |
| cite_key | `\cite{}` のキー |
| Title | bib記載タイトル |
| Authors | bib記載著者 |
| Year | bib記載年 |
| Venue | 会議名/ジャーナル名（+ 巻号・ページ） |
| DOI/URL (bib) | bibのDOIまたはURL |
| 引用箇所 | 本文中の「ファイル名:行番号」（複数） |
| 本文での記述 | 引用されている行の実内容 |
| オフィシャルURL | 検証で確認した正式URL |
| PDFダウンロード可否 | Yes / No / 部分アクセスのみ |
| PDFファイル名 | ダウンロード成功時のファイル名 |
| 整合性 | 本文記述が文献と合致するか（OK / NG / 要確認） |
| ハルシネーション疑い | 疑いがある場合に具体的に記録 |
| メモ | その他の注意事項 |

**重要**：Excelには**実際に引用されている文献のみ**含める。bibに残っている未引用文献は除外する（refs.bibから削除するかどうかは別判断）。

#### 3.1.4 検証スクリプトの自動化

検証作業を効率化するため、以下の自動化スクリプトを作成する：
- `refs.bib` を正規表現でパースし、各文献のフィールドを抽出
- `main.tex` および各 section ファイルから `\cite[a-z]*{key}` を全検索
- **実際に引用されている文献のみ** Excel に出力（bibに残っている未引用文献は除外）
- 引用箇所（ファイル名:行番号）と該当行の内容を自動収集

これにより、初期Excelは**自動生成**でき、手動作業は「各行の検証結果を埋める」のみ。未引用文献が bib に残っていることは珍しくないが、検証対象は本文で実際に引用されているものに限定する。

**Related Work Table 専用シートを併設する**：

比較表（Related Work Table / Table 1）は、文献単体の検証とは別に**Excel 内の独立シート**として個別検証するのが効果的。

```
参考文献チェック.xlsx
├── Sheet 1: 全文献検証（タイトル・著者・DOI・整合性）
└── Sheet 2: Table 1 検証（各セル＝Task / Output / Features / Horizon / Online / Language 単位の検証）
```

Sheet 2 の構成例：

| cite_key | Task（本文表） | Task（元論文） | 一致 | Output（本文表） | Output（元論文） | 一致 | ... |
|---|---|---|---|---|---|---|---|
| turngpt | Turn-shift prediction | Turn-taking prediction | △ → 本文修正 | ... | ... | ... | ... |

**なぜ別シートか**：
- 比較表の誤記は査読で最も目立つ（§3.2.2）
- 列単位（Task/Output/Features/Horizon/Online/Language）で個別に検証する必要がある
- 全文献シートに列を足すと横に伸びすぎて可読性が落ちる

#### 3.1.5 検証プロセス

1. Excel を起動
2. 1文献ずつ DOI/URL をブラウザで開く
3. オフィシャルサイトでタイトル・著者・年を照合
4. PDFをダウンロードし `参考文献確認作業/PDFs/[cite_key]_[1stAuthor姓]_[venue略][year].pdf` に保存
5. 「本文での記述」列と PDF内容を照合
6. 整合性・ハルシネーション疑いを記入
7. **記述が不正確な場合は本文を修正**

#### 3.1.6 PDFダウンロード失敗時の対応フロー

AIが `curl` や `WebFetch` で PDF を取得できないケースは頻発する（主な要因）：
- ペイウォール（IEEE Xplore, Elsevier ScienceDirect, PNAS 等の購読制ジャーナル）
- ボット対策（MDPI, Cloudflare, ReCAPTCHA 等）
- ログイン必須（ResearchGate, Academia.edu, 一部の学会サイト）
- 大学アクセス権限が必要なリポジトリ

この場合は以下の流れで**ユーザーに手動ダウンロードを依頼**する：

**手順**：

1. **まず AI が可能な限りダウンロードを試みる**（arXiv, ACL Anthology, ISCA Archive, 著者ページなど複数ソース試行）
2. **それでも失敗した文献をまとめ、以下のフォーマットでユーザーに提示**：

```
■ ダウンロードできなかった文献一覧：

| cite_key | 論文タイトル | オフィシャルURL | 失敗理由 |
|---|---|---|---|
| xxx | Paper Title | https://... | ペイウォール |
| yyy | Another Paper | https://... | MDPIボット対策 |

ユーザーの環境からご確認ください。ダウンロード後は、
`参考文献確認作業/PDFs/user_download/` フォルダにそのまま入れてください。
ファイル名は AI が内容を確認して規約通りにリネームします。
```

3. **`参考文献確認作業/PDFs/user_download/` フォルダをあらかじめ作成**しておく（`mkdir -p`）
4. ユーザーがPDFを配置したら、AI が：
   - ファイル内容を `Read` で確認（タイトル・著者が bib と一致するか）
   - 命名規則 `[cite_key]_[1stAuthor姓]_[venue略][year].pdf` に沿って**リネーム**
   - 元の `user_download/` から `PDFs/` 直下へ移動
   - 作業後 `user_download/` フォルダを削除（空になったら）
   - Excel の該当行に「Yes (user提供)」等を記入

**重要**：ユーザーに依頼する際は：
- ダウンロードできなかった一覧を**網羅的に**提示（後からバラバラに出さない）
- **ファイル名は AI が内容を見て変更すること**を明示（ユーザーに命名規則を強制しない）
- 配置フォルダのパスを明記
- 一件ずつ処理するのではなく、**複数件まとめて**依頼することでユーザーの手間を減らす

#### 3.2.1 引用選定の三原則【絶対原則】

**論文に引用する文献は、以下の3条件を全て満たすもののみに限定する。**

1. **それなりに有名であること**（引用数がそれなりにある／同コミュニティで反復言及されている）
2. **PDFがダウンロード可能であること**（AIが自力で、あるいはユーザー取得後に、一次情報の本体にアクセスできる）
3. **内容が確認できていること**（Abstract だけでなく結論部含めて精読済み、本文の引用記述と照合済み）

**1〜3のいずれか1つでも満たさない文献は、原則として引用しない。**

##### なぜこの原則が必要か

過去セッションで以下のハルシネーションが発生した：
- PDFが取れなかった Morais 2023 に対し、Abstract にない「wav2vec 2.0, HuBERT, WavLM」という具体モデル名を AI が**勝手に外挿して記載**
- PDFが取れなかった Maynard 1986 に対し、原典未確認のまま「roughly twice as frequently」という**具体数値**を記載（他論文で二次引用される定説ではあるが、原典で数値を確認できていない）
- Razavi 2019 の「semantic and timing features are the strongest individual predictors」は、実際の論文では **真逆**（lexical と syntactic が最強）。**Abstract の浅い読み取りから勝手にストーリー化**

これらは全て**「なんとなく有名な文献だから引用した」「Abstract だけ読んで要約した」「WebSearch の一文から外挿した」**パターン。

##### 運用方法

**執筆時の判断フロー：**

```
[引用したい文献 X]
  ↓
① 実在するか？（DBLP / Google Scholar / 公式ページで確認）
  No → 引用しない（捏造疑い）
  ↓ Yes
② 引用数やコミュニティ内の位置付けは？
  不明・ほぼゼロ → 代替文献を探す（§3.1.6 の手順で web 検索）
  ↓ 有名
③ PDFがダウンロードできるか？（AI 自力 + ユーザー依頼）
  No → 引用を**削除**するか、代替文献を探す
  ↓ Yes
④ 内容を実際に読んで確認したか？（Abstract 止まりはNG、結論部・関連する章まで読む）
  No → 読んでから引用
  ↓ Yes
⑤ 本文の引用記述と実論文の内容が**完全一致**するか？
  No → 本文を修正、または引用を削除
  ↓ Yes
[引用OK]
```

**PDFが取れなかった場合の対応（優先順）：**

1. **大学アクセス・著者ページ・arXiv・ACL Anthology・ISCA Archive・ResearchGate・Semantic Scholar・CORE・SemanticScholar のPDFリンクなど、あらゆる代替ソースで再試行**
2. それでもダメならユーザーに手動取得を依頼（§3.1.6）
3. ユーザーも取れない場合：
   - **当該主張を削除**、または
   - **同じ内容をカバーする別の PDF 取得可能文献を web 検索して代替**、または
   - **定性的・汎用的な記述に弱めて特定の数値・具体主張を避ける**

##### 「ハルシネーションが疑われる主張」の判定チェックリスト

執筆した任意の `\citet{X}` または `\citep{X}` について、以下を全て肯定できなければハルシネーションの疑いあり：

- [ ] X のPDF本体が `参考文献確認作業/PDFs/` にある
- [ ] X の本体を読み、本文の引用記述に対応する箇所（数値・結論・手法名）を**引用符付きで引ける**
- [ ] 引用された部分は**Abstract ではなく本文**にある（Abstract だけの要約はしばしば不正確）
- [ ] 具体的な数値（%, ms, 倍率等）を記述している場合、その値が**原典と一致**
- [ ] 著者・年・会議・ページが bibtex と一致

##### HuggingFace モデルカードや公式Webページの扱い

- HF モデルカードや公式プロジェクトページは、**そのページ自体が一次情報**なので、WebFetch で内容を確認できれば引用OK
- ただし引用時は `@misc` で HF URL を明記
- WebFetch で取得できない場合（401等）は、ユーザーにブラウザからアクセスしてもらい、記載内容を教えてもらうか、他の公式情報源を探す

##### 著者自己引用（first/co-author の過去研究）

- 著者ご本人が執筆する場合、自己引用の内容正確性は**著者自身が最終責任**を負う
- AI はbib情報（タイトル・年・会議）の妥当性までは確認できるが、内容の要約は著者ご本人の確認が必須
- **「著者確認要」フラグを立てて UNVERIFIED_CLAIMS.md 等に記録**し、レビュー後に確認してもらう

##### 引用件数が少なくて記述が薄い・主張が弱いと感じた場合

これは **「もっと引用しなければ」ではなく「もっと強い根拠を探す」機会** として対応する：

1. **Web検索（WebSearch / Google Scholar）で、同じ主張を支える新しい文献を探す**
2. 候補文献が見つかったら、§3.1.7.1 の三原則を適用してフィルタ
3. 通った文献をPDFダウンロード・精読 → bib追加 → 本文に組み込む

**禁止**：「有名そうだから」「執筆中の他の論文でよく見るから」という理由で、自力で内容確認していない文献を引用に加えないこと。

#### 3.1.7 特に注意すべきハルシネーションパターン

| パターン | 検出方法 |
|---|---|
| 架空の論文（存在しない著者・タイトル） | DOI/URL アクセスで 404 になる |
| 実在するが別の論文（タイトル混同） | タイトル・著者を原本と照合 |
| 実在するが記述内容が違う | 本文の引用記述をPDFで確認 |
| 年・会議名の誤り | bibのフィールドをオフィシャルページで照合 |
| 未実施の統計検定（McNemar p値等） | 元データ・予測ファイルの存在を確認 |
| 数値の捏造・丸め誤り | 修論・初期原稿との照合 |
| **PDF未取得のまま具体数値を書く** | **引用選定の三原則（§3.1.7.1）適用** |
| **Abstract から勝手にストーリー外挿** | **結論部まで読了してから執筆** |
| **「コミュニティ定説」として一次未確認の数値を書く** | **原典で数値を確認できないなら定性記述に留める** |

### 3.2 比較表（Related Work Table）の検証【超重要】

#### 3.2.1 基本方針
- 先行研究を一覧にする比較表は査読者に好評
- 列: Study / Task / Output type / Features / Horizon / Online / Language
- 自分の研究が「どの軸で新しいか」を一目で示す

#### 3.2.2 検証の厳格さ
**比較表は引用文献の著者自身が読む可能性が最も高いセクション**。誤記載があると直接的なクレームにつながる。ハルシネーションが混入しやすい箇所でもあるため、**通常の文献検証よりもさらに厳格に確認**する。

#### 3.2.3 各列の確認ポイント

| 列 | 典型的な誤り | 確認方法 |
|---|---|---|
| Task | **モデル名をタスク名として記載**（例：TurnGPTはモデル名、タスクはturn-taking） | 元論文のタイトルとアブストラクトで「何を予測しているか」を確認 |
| Output | 連続値/離散/確率 の誤り | 元論文の Methodology で出力形式を確認 |
| Features | 特徴量の誤記載（例：Audio (CPC) なのに単に Audio と書く） | 元論文の Feature extraction 節を確認 |
| Horizon | 予測範囲の誤り（例：VAPは ~2s ahead） | 元論文の evaluation 節を確認 |
| Online | リアルタイム対応の有無 | 元論文にオンライン評価/デモの記述があるか |
| Language | 対象言語の誤り | 元論文のデータセット記述を確認 |

#### 3.2.4 比較表のセル内引用は `\cite{}` を使う
- 通常本文は `\citep{}` （Harvard style で `(Author, Year)` として表示）
- **表のセル内は `\cite{}`** を使うのが慣例（表示が簡潔、スペース節約）
- 一括置換で `\cite{}` を全て `\citep{}` に変換する場合、**表内だけは `\cite{}` に戻す**必要がある

### 3.2.5 `\cite{}` と `\citep{}` の使い分け【厳守】

Elsevier `elsarticle` + Harvard style (`elsarticle-harv.bst`) を使うジャーナル（Speech Communication等）での使い分け：

| 場面 | 使用コマンド | 表示例 |
|---|---|---|
| 本文中の括弧つき引用 | `\citep{}` | `(Author, 2020)` |
| 本文中に著者名を文の一部として書く | `\citet{}` | `Author (2020) show ...` |
| 表のセル内（著者名を主語的に表示） | `\cite{}` | `Author (2020)` |

**よくある間違い**：
- 本文で `\cite{}` を使う → 表示が不統一になる（`Author (2020)` が文中に露出）
- **モデル名・システム名の直後の引用も `\citep{}` を使う**（例：`[ModelName]~\citep{xxx}`）。モデル名を文中で述べるときも、引用自体は Harvard style の括弧付きで
- 表内で `\citep{}` を使う → 冗長な括弧表示になることがある

**修正作業で注意**：
- sed等で一括置換する場合、表内の `\cite{}` まで変換してしまうミスに注意
- 変換後に必ず表を目視確認

**一括置換 sed の事故パターンと対処**：

| 事故 | 発生箇所 | 対処 |
|---|---|---|
| `\cite{` → `\citep{` 一括適用で表内も変換 | Related Work Table 等 | 変換後に `grep -n '\\citep{' 表.tex` で確認し、表内は `\cite{}` に戻す |
| 語彙置換が collocation を破壊（例：`consistent` → `steady` で `consistent with` が `steady with` に） | 本文全般 | 置換前に対象語の全出現を `grep -n` で列挙し、熟語/固定句を除外してから置換 |
| 固有名詞の一部マッチ（例：`wav2vec` を含む URL、`\label{}` 内） | refs.bib, label | `\b` 境界指定または対象ファイル限定で置換 |

**推奨ワークフロー**：
1. `grep -n '置換前' sections/*.tex` で全出現を表示
2. 除外すべきケースをリストアップ
3. 1 箇所ずつ Edit で置換（sed での一括置換は副作用が大きい）
4. どうしても一括が必要な場合は、置換後に全ファイル diff を目視



### 3.3 `\ref{}` とappendix参照の注意

Elsevier `elsarticle` クラス等では `\appendix` 後の `\ref{app:X}` は**自動的に "Appendix" プレフィックスを付与**する。

- **誤**：`(Appendix~\ref{app:X})` → コンパイル後「Appendix Appendix A」と重複
- **正**：`(\ref{app:X})` → コンパイル後「Appendix A」

クラスファイルの挙動を確認してから書く。

### 3.4 ハルシネーション検出で特に注意すべきチェック

比較表や先行研究言及で起きやすい典型パターン：

1. **AI が追加した統計値（p値、paired CI 等）**：元データ（予測ファイル等）が存在しない場合、AI が「このくらいの差なら有意だろう」と推論して捏造している可能性。削除するか、Bootstrap CI 幅との比較等の検証可能な表現に置換
2. **比較表の "Task" 列にモデル名が記載**：典型的な混同。TurnGPT、VAP等の固有名はモデル/システム名であり、Task（タスク）は "turn-taking prediction" 等の一般名詞
3. **比較表のセル内で `\cite{}` と `\citep{}` が混在**：表内は `\cite{}`、本文は `\citep{}` に統一
4. **本文でモデル名が登場するのに `\cite{}` が付いていない**：`[ModelName]~\citep{xxx}` の形式で必ず引用
5. **先行研究の特徴（入力、出力、対象言語、オンライン可否）の誤記載**：元論文のアブストラクトで最低確認
6. **数値の丸めエラー、桁ズレ、単位誤り**：修論・初期原稿と Abstract/Intro/Results/Conclusion で同じ数値になっているか相互チェック

---

## 4. 査読対応パターン

### 4.1 よくある査読指摘と対応策

| 指摘カテゴリ | 対応パターン |
|-------------|-------------|
| 統計的信頼性不足 | Bootstrap CI (1000 resamples) + McNemar検定 |
| ベースライン不在 | パラメータフリー統計ベースライン（survival analysis等） |
| 交絡の指摘 | 複数の傍証（3 lines of evidence）で間接的に対処 + 正直に限界認定 |
| アーキテクチャ選択根拠 | 3つの理由（タスク適合性、先行研究実績、計算コスト）+ future workでの代替案明示 |
| 指標の工学的意味 | 人間のターン交替研究（Stivers et al.等）との対応付け |
| オンライン評価不足 | pseudo-online分析の位置づけ明確化 + acknowledged limitationとして記述 |
| 単一ラン結果 | bootstrap CIで対応 + seed varianceの限界を明示 |

### 4.2 正直さの戦略
- 限界は隠さず正直に議論する（科学的誠実さとして査読者に評価される）
- 「cannot do X → leave for future work」ではなく「X is important → we provide indirect evidence from Y and Z → a definitive answer requires controlled experiment W」のパターン
- acknowledged limitationとして記述すれば、追加実験要求を回避できることが多い

---

## 5. 査読サブエージェント運用（オプション）

**より本格的な自己査読は `paper_review` スキルを使う【推奨】**：本節の3名体制よりも強力な「3観点並行査読（技術内容・参考文献検証・語彙表現）」を `paper_review` スキル（`skills/paper_review/SKILL.md`）として独立させている。各章完成時は軽量版（技術＋語彙）、投稿前はフル版（3観点＋マージ＋評点案）を自原稿に適用すると、実際の査読に近いチェックを投稿前に受けられる。詳細は `paper_review` §6（自己査読モード）参照。

**位置づけ**：査読サブエージェントは、原稿が概ね完成した段階で一通り機械的な指摘を得るのに有効。ただし、章ごとにユーザーが直接確認する運用（ユーザー主導）のほうが速く、かつ誤ったAI判断の混入を防げるケースが多い。プロジェクトの規模・期限・ユーザーの関与度で使い分ける。

- **向く状況**：原稿が長い／査読期限前に自己チェックしたい／ユーザーの時間が取れない
- **向かない状況**：章ごとに細かく方針相談しながら書く／AIの判断を毎回人間が検証する運用

### 5.1 3名体制
- 査読者A: 音声言語処理専門家（技術的正確性・新規性）
- 査読者B: 対話システム専門家（実用性・応用可能性）
- 査読者C: 機械学習専門家（実験設計・統計的妥当性）

### 5.2 査読サイクル
- R1: 初稿査読 → Major/Minor指摘を収集
- R2: R1指摘対応後の再査読 → Minor指摘の確認
- R3: R2指摘対応後の最終確認 → Accept判定

### 5.3 査読指示のポイント
- 前回の査読結果ファイルパスを明示
- 指摘事項のリストを具体的に提示
- Accept / Minor / Major の判定を求める
- 「残った問題があれば具体的に指摘」を明記

---

## 6. LaTeX執筆テクニック

### 6.1 テンプレート
- Elsevier: elsarticle.cls + elsarticle-num.bst
- `\documentclass[preprint,12pt]{elsarticle}` + numbered style

### 6.2 セクション分割
- `sections/*.tex` に分割し `main.tex` から `\input` で読み込み
- コンパイルは必ず `compile.sh` を使用

### 6.3 compile.sh 標準テンプレ【Elsevier + dvipdfmx】

Elsevier `elsarticle` で `\documentclass[...,dvipdfmx]{elsarticle}` を指定した場合、**`pdflatex` は直接使えない**。`LaTeX3 Error: Backend request inconsistent with engine: using 'pdftex'` のようなエラーになる。

解決策：**`platex / uplatex + dvipdfmx` パイプライン**を使う（VSCode LaTeX Workshop も内部でこのパイプラインを使っている）。

#### 標準テンプレート（`latex原稿/compile.sh`）

```bash
#!/bin/bash
# Usage: ./compile.sh
cd "$(dirname "$0")"

# 中間ファイル掃除（重複定義エラー防止）
rm -f main.aux main.bbl main.blg main.log main.out main.toc \
      main.dvi main.pdf main.fls main.fdb_latexmk main.synctex.gz

# uplatex 優先、なければ platex にフォールバック
if command -v uplatex >/dev/null 2>&1; then
    LATEX_CMD="uplatex"
    BIBTEX_CMD="upbibtex"
else
    LATEX_CMD="platex"
    BIBTEX_CMD="pbibtex"
fi

echo "Using: $LATEX_CMD + dvipdfmx"

latexmk \
    -e "\$latex = '$LATEX_CMD -interaction=nonstopmode -halt-on-error -synctex=1 %O %S';" \
    -e "\$bibtex = '$BIBTEX_CMD %O %B';" \
    -e '$dvipdf = q/dvipdfmx %O -o %D %S/;' \
    -pdfdvi \
    main.tex

EXIT_CODE=$?
echo ""
echo "=== Compile finished ==="
if [ -f main.pdf ]; then
    echo "Output: main.pdf (succeeded)"
else
    echo "Error: main.pdf was not produced. See main.log."
    exit $EXIT_CODE
fi
```

#### ジャーナル別 documentclass とコンパイル経路

| documentclass | 典型ジャーナル | コンパイル経路 |
|---|---|---|
| `\documentclass[...,dvipdfmx]{elsarticle}` | Speech Communication, Computer Speech and Language | **platex/uplatex + dvipdfmx**（上記） |
| `\documentclass[...]{elsarticle}` （dvipdfmx なし、欧文のみ） | Elsevier欧文系 | `pdflatex` 直接 |
| `\documentclass{IEEEtran}` | IEEE系（TASLP 等） | `pdflatex` 直接 |
| `\documentclass{acmart}` | ACM系 | `pdflatex` 直接 |
| `\documentclass{sn-jnl}` | Springer Nature | `pdflatex` 直接 |
| `\documentclass{interspeech}` / ICASSP / IWSDS等 | 各学会テンプレ | 原則 `pdflatex` 直接（個別確認） |

#### 運用ルール
- **必ず `compile.sh` を介してコンパイル**する（`latexmk` や `platex` を直接呼ばない）
- VSCode の場合は `settings.json` で同等パイプラインを recipe として設定、もしくは **`compile.sh` を LaTeX Workshop の build recipe として登録**する
- コンパイル失敗時は `main.log` の最初のエラーに着目（後続エラーは連鎖であることが多い）

### 6.4 数値の整合性チェック
- Abstract, Introduction, Results, Conclusion間で同一数値が一致するか確認
- 表番号・図番号の参照が正しいか確認
- `\ref` の未解決がないか確認

### 6.5 投稿先テンプレートの入手と配置【Phase A-4 詳細】

#### 6.5.1 投稿先ごとの入手経路

| 投稿先分類 | 具体例 | 入手元 | 配置方法 |
|---|---|---|---|
| Elsevier系 | Speech Communication, Computer Speech and Language, Journal of Phonetics | CTAN（elsarticle）または [Elsevier author resources](https://www.elsevier.com/authors) | CTAN 版で OK（TeX Live なら標準搭載）。サンプル `.tex` はダウンロード推奨 |
| IEEE系 | TASLP, SPL, Proc. ICASSP | [IEEE Author Portal](https://template-selector.ieee.org/) | zip ダウンロード → 展開 → `latex原稿/` 配下 |
| ACM系 | ACM Trans., Proc. CHI | CTAN（acmart）または [ACM公式テンプレ](https://www.acm.org/publications/proceedings-template) | CTAN 版 + 公式サンプル |
| Springer Nature | SN journals | [Springer Nature LaTeX template](https://www.springernature.com/gp/authors/campaigns/latex-author-support) | zip 展開 |
| 音声言語情報処理の会議 | Interspeech, ICASSP, ACL, EMNLP, EACL, NAACL | 学会公式配布（年度ごとに更新） | 当年版を必ず使用。前年と異なる場合あり |
| 国内学会 | 言語処理学会 (NLP), 情報処理学会, 日本音響学会 | 学会公式配布 | 和文スタイル（`jarticle` / `jsarticle`）の場合あり、compile.sh 要調整 |

#### 6.5.2 テンプレート展開後の処理

1. **サンプル保存**：展開した原テンプレ一式（サンプル `.tex`, `.bib`, 図等）を `latex原稿/templates_sample/` に退避
2. **作業用ファイル作成**：`latex原稿/main.tex` はサンプルをコピーして自分用に改変
3. **documentclass 確認**：
   - `\documentclass[...,dvipdfmx]{elsarticle}` 等の dvipdfmx 指定 → §6.3 標準テンプレ使用（uplatex+dvipdfmx）
   - `\documentclass{IEEEtran}` 等 → `pdflatex` 直接の compile.sh に差し替え
4. **文献スタイル確認**：`\bibliographystyle{}` を投稿先ガイドに合わせる
   - Elsevier Harvard: `elsarticle-harv`
   - Elsevier numbered: `elsarticle-num`
   - IEEE: `IEEEtran`
   - ACM: `ACM-Reference-Format`
5. **必要パッケージの整理**：`\usepackage{}` に本論文で使うパッケージを列挙
6. **初回コンパイル試験**：`./compile.sh` を実行し、テンプレが動作することを確認してから執筆開始

#### 6.5.3 投稿規定の読解

テンプレに付属する author guidelines（README / `guide-for-authors.pdf` 等）を読み、以下を把握：

- **ページ数・字数制限**（Elsevier は通常ページ制限なしだが、Letter/Short形式は厳格）
- **図表カウント方法**（本文内 vs 別ファイル）
- **Highlights / Graphical Abstract の要否**
- **Cover Letter の要否・様式**
- **著者情報の書式**（ORCID、responsible author 指定方法）
- **投稿時の追加アンケート**（ethics declaration、preprint policy 同意 等）

これらは初稿執筆中に発覚すると手戻りが大きいため、**Phase A-4 の時点で確認**する。

### 6.6 修正履歴のマーキング（共著者・指導教員レビュー用）【重要】

#### 6.6.1 目的と背景

論文修正中、共著者・指導教員（特に紙PDFに赤字でコメントを返してくる方）にドラフトを提出するとき、**修正・追記された箇所が一目で分かる状態**にしておくとレビュー効率が大きく上がる。

- レビュアー側の利点：「どこが変わったか探す」作業が不要、自分の指摘が正しく反映されているか即座に確認できる
- 執筆側の利点：レビュー指摘 → 該当箇所修正 → 再提出のサイクルを高速化できる

ただし**最終投稿時は色マークを完全に消す必要がある**（学会・ジャーナルの本投稿原稿に色が付いていてはいけない）。色マーク機構は「ON/OFF が1行で切替可能」「削除漏れが grep で検出可能」な設計にする。

#### 6.6.2 標準マクロ（プリアンブルに追加）

`main.tex` のプリアンブルに以下を追加：

```latex
% =====================================================================
% 修正箇所マークアップ用マクロ（共著者・指導教員チェック用）
%   - \rev{...}        : 追記・修正したテキストを赤文字で表示
%   - \revdel{...}     : 削除したテキストを赤色＋取消線で表示（履歴用）
%
%   【最終投稿時の手順】
%     1) 下記 \showrevstrue を \showrevsfalse に書き換える
%        → \rev は色なしで中身だけ出力、\revdel は空に展開（テキスト消失）
%     2) grep -rn '\\rev{\|\\revdel{' latex原稿/sections/ で残存確認
% =====================================================================
\usepackage{xcolor}
\usepackage{ulem}  % \sout 取消線（\revdel 用）
\normalem          % \emph がイタリックのままになるよう設定
\newif\ifshowrevs
\showrevstrue      % ← 最終投稿時は \showrevsfalse に変更
\ifshowrevs
  \newcommand{\rev}[1]{\textcolor{red}{#1}}
  \newcommand{\revdel}[1]{\textcolor{red}{\sout{#1}}}
\else
  \newcommand{\rev}[1]{#1}
  \newcommand{\revdel}[1]{}
\fi
```

**設計のポイント**：
- `\showrevsfalse` 切替時、`\rev{...}` は **identity 展開**（中身だけ残す） → テキスト消失のリスクなし
- `\revdel{...}` は空に展開 → 「削除した古いテキスト」が最終原稿に出ない
- `xcolor` + `ulem` は uplatex + 二段組 + 日本語混在でも安定動作
- `\normalem` は `ulem` の `\emph` 上書き（取消線化）を抑制する必須行

#### 6.6.3 本文中の使い方ルール

論文修正運用中は、**追記・修正したテキストを必ず `\rev{...}` で囲む**：

```latex
% 例1：追記（短い句の挿入）
best five-bin classification accuracy \rev{(0.2\,s per bin)} over the last 1\,s

% 例2：文の置き換え（新しい文を丸ごとくくる）
\rev{In contrast, recovering this remaining-time value from a binary endpoint flag
requires an additional mapping, and a poorly designed mapping degrades the dialog
system's response-timing precision.}

% 例3：単語レベルの置き換え（新だけマーク、旧は通常削除）
producing \rev{listener's next} activity patterns rather than \rev{direct timing}.

% 例4：削除部分も履歴として見せたい場合（オプション）
\revdel{a direct timing quantity}\rev{direct timing}
```

**判断基準**：
- 小さな追加・置き換え → `\rev{}` のみで十分（旧テキストは通常削除）
- レビュアーが「何を消したか」を確認したい場面のみ `\revdel{}` 併用
- 段落丸ごとの書き換えは段落全体を `\rev{}` でくくる
- 数式・参照（`\ref`, `\cite`）も `\rev{}` で囲んで問題ない

#### 6.6.4 修正案まとめ md との連携

各修正箇所について、**修正案まとめ md（例：`_共著者チェック/指摘_修正案まとめ_<日付>.md`）の「対応ファイル」欄に `\rev{}` でくくった旨を明記**する：

```markdown
- **対応ファイル**：`latex原稿/sections/1_introduction.tex`（line 16、`\rev{}` でラップ済）
```

→ あとで「どの修正が `\rev{}` 状態か」を md で追跡できる。

#### 6.6.5 最終投稿時の手順【必須】

1. **トグル切替**：`main.tex` プリアンブルの `\showrevstrue` → `\showrevsfalse` に書き換え
2. **コンパイル確認**：`./compile.sh` で正常終了することを確認、PDF を目視で赤文字が消えているかチェック
3. **残存確認 grep**：
   ```bash
   grep -rn '\\rev{\|\\revdel{' latex原稿/sections/
   ```
   → ヒット件数を記録、抜き打ちでいくつかの行をスポット確認
4. **保険的削除（任意・推奨）**：将来の編集事故を防ぐため、最終投稿用ブランチでは `\rev{}` 自体を本文から除去できる：
   ```bash
   # \rev{...} を中身だけに展開／\revdel{...} を完全削除（単純な1階層のみ。ネスト非対応）
   find latex原稿/sections -name '*.tex' -exec \
     perl -i -pe 's/\\rev\{([^{}]*)\}/$1/g; s/\\revdel\{[^{}]*\}//g' {} \;
   ```
   ※実行前に必ず git でブランチ分離・commit 済みにすること。ネスト（`\rev{\rev{...}}`）や複数行わたりの `\rev{}` は別途処理が必要。
5. **再コンパイル＆PDF最終確認**：投稿用 PDF を生成、念のため別の人にも見てもらう

#### 6.6.6 運用上の注意

- **マクロ未定義エラー対策**：他の共著者が `compile.sh` を回したとき `\rev` 未定義にならないよう、マクロ定義はリポジトリ管理下の `main.tex` に常駐させる
- **過去の修正をいつ消すか**：レビュー1巡完了＆全指摘反映後、次のレビューサイクル開始前に「前ラウンドの `\rev{}` を全部解除（中身だけに置換）」してから新規修正に `\rev{}` を付け直すと、レビュアーが「今回の修正」だけを見やすい
- **複数ラウンドの色分け（高度）**：レビュアー別・ラウンド別に色を分けたい場合は `\revA{}` `\revB{}` 等のマクロを追加し、それぞれ別色を割り当てる。ただし `\showrevsfalse` 切替で全マクロが identity になるよう統一すること
- **数式中での使用**：`\rev{\sum_{i=1}^N x_i}` のように数式環境内でも使えるが、`\textcolor` が数式モードで挙動が異なる場合がある。失敗時は `\mathcolor` 系パッケージ（`mathcolor` 等）を検討

---

## 7. Discussion 節の構成パターン

効果的な Discussion の構成例（音声言語情報処理系ジャーナル向け）：
1. **Why does X help?** — 提案手法が効果を発揮する要因の分析
2. **Positioning relative to Y** — 既存の代替手法と直接比較しなかった理由、補完関係の整理
3. **Design parameter Z** — 主要な設計パラメータ（bin幅、window長等）の根拠
4. **Task formulation choice** — 定式化（分類 vs 回帰等）の選択根拠
5. **Model architecture choice** — アーキテクチャ選択の根拠と限界

**Limitations（§ Limitations and Ethics として独立させることを推奨）**：
- Prediction/estimation limits — 手法内在の予測限界
- Evaluation assumptions — 評価前提（VAD, transcript boundary等）の限界
- Interactivity / dialog context — モデル化していない要素
- Data scope and generalization — 言語・ドメイン・スタイル一般化可能性
- Ethical considerations and data availability — 倫理・データ公開・再現性

**原則**：Discussion と Limitations は性質が異なるため、**セクションタイトルを "Discussion and Limitations" と混載せず、別セクションに分ける**（§8.6 参照）。

---

## 8. 英語品質チェックリスト

- [ ] 受動態の過用を避け、能動態を適切に混ぜる
- [ ] 1文が25語以下を目安（分野実測: 平均24.5語・中央値21語。40語超を連発しない）
- [ ] 段落はtopic sentence firstで書く
- [ ] 段落の長さが機械的に均質になっていないか（AI初稿は約100〜130語×N個の均質段落になりがち。内容駆動で長短を混ぜる）
- [ ] 「however」「moreover」等の接続語を適切に使用
- [ ] 数値には `\,` で適切なスペースを入れる（例: 38.2\,\%）
- [ ] 表のキャプションは表の上、図のキャプションは図の下
- [ ] 初出の略語は必ずフルスペルアウト
- [ ] **BAN語・LIMIT語チェック**（`speech_style_data.md` §2–3）: underscore系/pivotal/nuanced/intricate/delve系/seamless/realm等はゼロに。notably/crucialは1論文0〜1回
- [ ] **人間マーカー表現を適度に使ったか**（`speech_style_data.md` §4）: Note that / It can be seen that / in order to / On the other hand / In other words
- [ ] セミコロンによる文接続は約30文に1回まで（分野実測 0.03〜0.05回/文）
- [ ] 修辞疑問文（...?）を本文で使っていないか（分野実測 0.23/M、ほぼゼロ）
- [ ] (i)(ii)(iii)・First/Second/Third型の三点列挙が多すぎないか（整いすぎたパラレリズムはAI臭）

---

## 8.4.Y 情報源の原則と _ref との照合【最重要】

### 情報源の大原則

論文の**全ての数値・事実は、以下のいずれかに由来しなければならない**：

1. **_ref 配下にある既存の関連資料**（修論、過去の国際会議・国内学会発表論文、既存原稿）
2. **_ref 配下の資料から機械的・数学的に派生計算できる値**（混同行列からの MAE/RMSE、発話数合計、accuracy の分散解析に基づく CI など）
3. **外部の公開論文**（bibに含まれる文献）の、**当該論文を実際に確認した上での引用**

**これ以外の情報（例：AI が文脈から推測して補完した値、過去にどこにも記載がない新規の数値）は、全てハルシネーションである**。

### 数値ハルシネーションの典型例

AI が論文推敲中に**勝手に追加しがちな数値**：
- 「duration-prior baseline は 26.6%」のような**新規ベースラインの数値**（元論文に該当実験なし）
- 「mean duration 4.3s, median 3.0s」のような**統計要約値**（元論文に記載なし、派生計算で再現不可）
- 「wav2vec forward pass 0.15s, LSTM 0.05s」のような**内訳レイテンシ**（元論文に時間計測結果なし）
- 「within-one-bin accuracy +11.7 points gain」のような**差分値**（被減数・減数の一方が不明）
- McNemar p 値、paired CI（§8.4.X 参照）

### 検証プロトコル

1. **_ref 配下の全ファイル（.tex, .md, .pdf）で、当該数値を grep / pdftotext で全文検索**
2. 見つかれば「判定 A（一致）」または「判定 B（派生計算で一致）」と記録
3. 見つからなければ：
   - (a) 当該数値を**削除**
   - (b) 関連する主張・表現も**元論文が裏付ける範囲に限定**して書き直す
4. 削除後に**前後の文脈に矛盾・不自然さがないか確認**し、必要に応じて接続語・段落構造を調整

### 数値削除時の文章修正の原則

**原則**：削除した数値の代わりに、**具体的でない別のハルシネーション**を入れないこと。

- 悪い例：`"26.6%"` → `"approximately 30%"`（新たなハルシネーション）
- 良い例：`"26.6%"` → **該当記述を丸ごと削除**
- 悪い例：`"mean 4.3s"` → `"mean around 4s"`（推測で補完）
- 良い例：`"mean 4.3s"` → **数値を削除し、定性的主張のみ残す**（例：「utterance lengths span a wide range」）

**文脈調整の実例**：

- 「Three pieces of evidence suggest..." の 1 つ目が削除された場合：
  - 「Three」→「Two」に変更
  - 残りの 2 つ目・3 つ目を「First,... Second,...」にリナンバリング
- 「duration-prior baseline 26.6%」への言及が abstract / intro / conclusion / discussion で重複している場合：
  - **全てを一括削除**（一つ残すと整合性崩壊）
- 「baseline から X point gap」の記述：
  - baseline 数値が削除されるなら、gap も削除
  - gap を絶対値でなく方向性で記述（"substantially above chance" 等、chance level 20% のような既知値との比較に置き換え）

### 再発防止のための執筆ワークフロー

1. **初稿時**：AI に「元原稿にある数値のみを使って本文を書く。新しい数値は一切追加しない」と明示指示
2. **推敲時**：追加された数値があれば、**_ref 検索** → 裏付けがなければ即削除
3. **最終確認**：全数値について「_ref 照合結果」を表にまとめた確認ファイル（`表・数値の参照元情報.md` 等）を作成
4. **ハルシネーション発見時**：数値単体だけでなく、**それに依拠する全ての記述（差分値・相対評価・因果説明）を含めて削除**

### _ref 検索時の注意点【重要】

**検索が「見つからない」ことは「存在しない」を意味しない**。検索漏れが発生した実例：
- ある数値を「一括削除」する前に、`_ref` の **全ての資料**（複数の国際会議論文・国内学会発表論文・修論）を**PDFの本文レベル**で検索する
- PDF検索は `pdftotext` 等で本文抽出後、**日本語・英語・数値表記の揺れ**（例：「0.2秒」「0.2 s」「200ms」「200 ms」「5Hz」「5 Hz」「200 ミリ秒」）を全てカバーする
- 数値が**等価な別表現**で書かれている可能性をチェック（例：`5 Hz` = `0.2 s update cycle` = `inference every 200 ms`）
- **同じ値でも異なる文脈・異なる言語で記述されている場合がある**（日本語原稿では「約 0.2 秒かかる」と書かれていて、英語 journal で「0.2 s per cycle」と表現される、等）

**推奨手順**：
1. 数値の**全ての等価表現**をリストアップ（例：`5 Hz`, `0.2 s`, `200 ms`, `0.2 秒`, `5 回/秒`, `5 times per second`）
2. `_ref` の**全ファイル**（`.tex`, `.pdf`, `.md`）で各表現を順次検索
3. いずれかが見つかれば、その元となる値（例：SPEASIP で「0.2 秒」と記載）を**確認済**として数値を復活・採用
4. 全て見つからない場合のみハルシネーション確定

**一度削除した値でも、より徹底的な検索で裏付けが見つかる場合がある**。削除後の値についても、後で再検索して「本当にハルシネーションだったか」を二度目の確認すること。

### 対応時に注意すべきデリケートな側面

- **削除しすぎないこと**：派生計算が可能な値（混同行列からの MAE/RMSE 等）まで削除する必要はない。**計算根拠を明記**して残す
- **査読対応時の留意**：削除した数値について査読者が「元の数値はどこから？」と質問する可能性は低いが、聞かれた場合は「再確認の結果、原典で裏付けられなかったため削除」と正直に答える
- **次の論文へのフィードバック**：今回のような事例が発生したら、**該当する新規実験を修論とは別に実施**し、正式な数値として取得することが理想

---

## 8.4.X 研究倫理：統計値を捏造・推測で生成しない【絶対遵守】

### 背景

AI が論文を推敲すると、**元データを見ずに「このくらいの差なら有意だろう」と推論**して、根拠のない統計値を記述することがある。典型例：
- McNemar検定のp値（`McNemar $p < 0.001$`）を、paired な予測結果ファイルが存在しないのに記述
- paired confidence interval（`CI [0.7\%, 1.3\%]`）を、paired データにアクセスせず記述
- 「statistically significant」の断定を、実際の検定なしに記述

**AI による統計値の捏造は、査読で発覚すれば retraction（撤回）のリスクがある重大な研究倫理違反**。混同行列だけでは計算不可能な統計量（McNemar検定・paired CI等）は、元の予測ファイルへのアクセスがなければ原理的に計算できないことを AI は忘れがちであり、特に注意を要する。

### 厳格ルール

**以下の統計値は、AIが元データを見て計算した場合のみ記述可能。それ以外は絶対に書かない。**

| 統計値 | 必要なデータ |
|---|---|
| McNemar検定のp値 | 各サンプルについて両モデル(A, B)の予測結果のペア |
| 2モデル差のpaired confidence interval | 同上 |
| t検定・paired t検定のp値 | 各サンプルの値 |
| bootstrap CI（単一モデルのaccuracy等） | 各サンプルの正解/不正解ラベル（混同行列から再現可） |
| effect size (Cohen's d等) | 各サンプルの値 |
| 有意性を示す記述（`p < 0.001`, `statistically significant`等） | 該当検定の実計算結果 |

### 元データがない場合の代替表現（研究倫理上安全）

| 避ける（要データ） | 代替（データ不要で安全） |
|---|---|
| `McNemar $p < 0.001$` | `the N pp gain is larger than the 95\% bootstrap CI width` |
| `statistically significant (p < 0.001)` | `beyond sampling variability` / `larger than the CI width` |
| `paired CI [0.7\%, 1.3\%]` | 削除（numerical differenceのみ残す） |

### AI（Claude等）の振る舞いルール

1. **論文中の統計値を「補強」「強化」のためにAIの判断で追加してはいけない**
2. **"このくらいの差ならp<0.001だろう"という推測は研究不正**
3. **既存原稿に統計値がある場合、元データの存在を必ず確認してから引用**
4. **不明な場合はユーザーに確認する**：「この統計値の元データはどこにありますか？」
5. **bootstrap CIのみであっても、ペア比較のCIは元データが必要と認識する**

### チェックリスト（執筆時・査読時）

- [ ] 論文中のp値は、該当する実計算結果ファイルが存在するか？
- [ ] confidence intervalは単一分布のCIか、paired差のCIか？後者は元データ必須
- [ ] `statistically significant`の記述には、対応する検定結果があるか？
- [ ] 修論や過去原稿になかった統計値が、journal原稿で新規追加されていないか？

---

## 8.5 読者層に合わせた英語表現の平易化【重要】

### 8.5.1 想定読者と表現選択の原則

音声言語情報処理系ジャーナル・国際会議論文の想定読者は、主に **音声言語情報処理系の工学者**。
彼らは：
- 当該分野の専門用語（VAP, IPU, CTC, hidden states, wav2vec, SSL, MFCC 等）には**馴染み深い**
- **論文を読むことで英語を学んでいるため、論文で頻繁に登場する表現には馴染みがある**（"We propose", "outperforms", "baseline" 等）
- しかし、**論文以外（一般的な会話・本・ニュース等）で用いられる表現には疎い**。なぜなら、論文からしか英語を学習していないから
- そのため、**論文以外の文脈でよく使われるが、技術系論文ではあまり使わない形式的・文語的な語彙**（"warrant", "exhibit", "synthesize", "alleviate", "underscore" など、ジャーナリズムや人文系文書で多用される単語）は、読解の負担になる

執筆時の鉄則：
- **専門用語は専門用語のまま**使う（無理に平易化しない。工学者にとっては易しい）
- **論文以外で多用される形式的・文語的な語彙**（ジャーナリズム、人文系文書等で多用される英語）は、**技術系論文でよく使われる平易な代替表現**に置き換える
- 冗長な言い回しは避ける

### 8.5.2 避けるべき一般語・一般表現と推奨置き換え

対象：**論文以外（ニュース、書籍、一般会話）で多用されるが、技術系論文では代替表現のほうが自然な語彙**。工学者は論文でしか英語を学ばないため、こうした語彙への馴染みが薄い。

#### A. 形式的・文語的な動詞 → 平易な動詞へ

| 避ける | 推奨 |
|---|---|
| warrant | require / need |
| exhibit | show / have |
| synthesize | summarize / bring together |
| constitute | count as / be |
| yield | produce / give |
| comprise / comprising | consist of |
| incentivize | push toward / encourage |
| underscore | highlight / emphasize |
| leverage | use / make use of |
| alleviate | reduce / ease |
| disentangle | separate from |
| sidestep | avoid |
| convey | express / show |
| deserve attention | be worth noting |
| favor (動詞) | be better suited to |
| isolate (the contribution) | separate out |
| replicate | reproduce / mimic |

#### B. 形式的な名詞・形容詞・副詞 → 平易な語へ

| 避ける | 推奨 |
|---|---|
| remarkable | very high / striking |
| auxiliary | additional / supporting |
| modestly | slightly |
| comprehensive | broad / thorough |
| fundamental | basic / essential |
| implicit | indirect |
| anticipatory | predictive / look-ahead |
| transient | short-lived / brief |
| non-trivial | not simple / substantial |
| definitive | conclusive |
| favorable | advantageous |
| actionable | usable / easier to act on |
| inherently | by nature |
| moderate (size) | medium |
| diagnostics (名詞複数) | breakdowns |
| a diagnostic (名詞) | an analysis / a check |
| diagnostic analysis (形容詞用法) | per-bin analysis / detailed analysis |
| retain (動詞：保持する) | keep |
| retain (動詞：選別して残す) | keep |
| are retained (受動態) | remain |
| consistent with（「合致する」熟語） | in line with / matching / as expected given **※ "steady with" への置換は誤り（"steady with" は英語として成立しない）** |
| consistent（時間的に安定・ブレない） | steady / stable |
| consistently（時間的に安定・着実に） | steadily |
| consistently outperforms / consistently X（「全条件で常に」の意） | **副詞削除** or always / in every setting / in every comparison **※ "steadily outperforms" は誤訳的（"steadily" は時間的推移の意味）** |
| plateau（動詞：頭打ちになる） | stop improving / level off |
| plateau（名詞：頭打ち状態） | lack of further improvement / flat region |
| skewed（形容詞：分布が歪んでいる） | long-tailed / 文で具体的に説明（"most X are Y while some are Z"） |
| truncate（動詞：切り詰める） | cut off |
| truncating（動名詞） | cutting off |
| truncation（名詞） | 文を動詞形に書き換え（"that ... cut off"）を推奨 |
| short-horizon（予測範囲） | near-future / short-range |
| prediction horizon | prediction range |
| shortest-horizon class | class closest to the endpoint |
| longest-horizon class | class farthest from the endpoint |
| mid-horizon classes | middle classes |
| longer horizons（残り時間が長い） | longer remaining times |
| far-horizon bins | bins farther from the endpoint |
| near-horizon classes | classes close to the endpoint |
| Extended-horizon classification | Extended-range classification |
| dip（名詞：グラフの一時的な下降） | brief drop / temporary drop |
| dips（複数） | brief drops |

#### C. 接続表現・談話マーカー

| 避ける（重い） | 推奨（軽い） |
|---|---|
| Nevertheless | However / Still / But |
| By contrast | On the other hand / In contrast |
| Furthermore | In addition / Also |
| Crucially | Importantly |
| Three lines of evidence suggest | Three pieces of evidence suggest |

#### D. 慣用的・冗長な言い回し

| 避ける | 推奨 |
|---|---|
| to assess practical feasibility | to check whether it works in practice |
| for a balance between A and B | as a trade-off between A and B |
| introduces a minimum N-cycle response delay | adds at least N cycles of delay |
| does not directly translate into | does not directly cause |
| offsetting the processing cost | canceling out the processing cost |
| fall back to | revert to |
| via pluggable control modules | through plug-in control modules |
| any post-processing pipeline | any extra post-processing |
| comfortably supports | easily supports |
| acts as a natural buffer | serves as a buffer |
| an important avenue for future work | an important direction for future work |
| have functional counterparts in | have functionally similar markers in |
| support reproducibility | enable reproducibility |
| The paper proceeds through ... | The rest of the paper covers ... |
| addresses this gap | fills this gap |
| introducing unavoidable latency | adding unavoidable latency |
| temporal interplay between A and B | timing interaction between A and B |

### 8.5.3 執筆時のフロー

1. **第一稿執筆時**：上記表のリストを参照し、最初から平易な表現で書く
2. **査読サブエージェント運用前**：自己チェックで上記表の「避ける」語を grep し、置き換える
3. **査読対応時**：査読者の指摘以外でも、上記表の「避ける」語を見つけたら平易化する

### 8.5.4 平易化しない例外

以下は「専門用語」または「定着した慣用句」として、無理に平易化しない：
- 専門用語そのもの（utterance, dialog, turn-taking, backchannel, etc.）
- 統計・機械学習用語（hidden states, logits, classification, regression, etc.）
- 評価指標名（MAE, RMSE, accuracy, F1, etc.）
- 論文構造の慣用句（"In this paper", "We propose", "Future work", etc.）

### 8.5.5pre 文頭表現の読みやすさ（"Because" 始まりを避ける）【推敲時チェック】

理由・目的を述べる文を **`Because ...,` で始めると、主節に到達するまで読み手が宙づりになり読みにくい**（特に従属節が長い場合）。技術論文では文頭の従属節を避け、以下のような言い回しに変えると流れが良くなる：

- **目的**：`Because we want to avoid redundancy, the table lists ...` → **`To avoid redundancy, the table lists ...`**
- **理由（後置）**：`Because A, B` → **`B because A`**（主節を先に出す）／ **`B; A causes this`**
- **理由（言い換え）**：`Because of X` → **`Owing to X` / `Given X` / `Since X`**（ただし `Since` は時間と紛れる文脈では避ける）
- **根拠の明示**：`Because the data is limited, ...` → **`The limited data means that ...` / `With only limited data, ...`**

原則：**文頭は主語・主節・目的不定詞（To ...）から始める**ことを優先し、長い従属節を頭に置かない。推敲時は `grep -n "^Because\|\. Because\| Because " sections/*.tex` 相当で文頭・文中の `Because` を洗い出し、読みにくければ上記へ置換する。
（実例：表1の選定基準説明で `Because several approaches share ...,` → `To avoid redundancy among approaches that share ...,` に変更し可読性が向上。2026-06-28 西村確認）

---

## 8.5.5 抽象的・曖昧記述の禁止【重要】

### 8.5.5.1 問題意識

論文中で抽象語（"the same quantity", "conversion pipeline", "design choices", "the resulting quality", "affects timing precision" 等）でぼかすと、読者は **何を指しているか分からず**、文の主張が伝わらない。査読者からも「具体的に何を意味するのか」と指摘される。

**原則**：抽象語・婉曲表現でぼかさず、**「何が」「何を」「どのくらい」**を明示する。比喩的な"pipeline" / "step" / "procedure" 等を使う時は **必ず具体例を併記**する。

### 8.5.5.2 典型的なアンチパターンと修正

#### A. 曖昧な指示語・抽象語は具体名に置き換える

| 避ける | 推奨 |
|---|---|
| the same quantity / the same value | this remaining-time value / the predicted seconds |
| conversion pipeline / conversion step / conversion procedure | mapping / threshold / integration（具体名） |
| design choices / certain factors | thresholding choice / integration step / window size |
| timing quality / output quality（何のか不明） | the dialog system's response-timing precision / classification accuracy |
| the system / the model（文脈で何か曖昧な時） | the dialog manager / the time-to-end estimator |
| something like X / a kind of X | X（具体名）、または明示的に「we use X (defined as ...)」 |

#### B. 曖昧な動詞を具体的な動詞に

| 避ける | 推奨 |
|---|---|
| affects X | degrades X / improves X by N pp / biases X toward Y |
| involves Y | requires N steps / includes thresholding |
| supports Z | directly drives Z / computes input for Z |
| is challenging | requires hand-tuning of two thresholds / incurs N ms latency |
| has an impact on | reduces / increases / changes by N% |

#### C. 「変換」「ステップ」「パイプライン」等の抽象語を残す場合の最低条件

「conversion」「mapping」「step」「procedure」「pipeline」を使うこと自体は禁止しないが、**必ず例示を添える**：

❌ `requires a conversion pipeline whose design choices affect timing quality`
✅ `requires an additional mapping (e.g., thresholding the flag, or integrating predicted activities over time), and a poorly designed mapping degrades the dialog system's response-timing precision`

#### D. 数値・名前・操作で具体化する

| 抽象 | 具体 |
|---|---|
| improves performance significantly | improves five-bin accuracy by 1.9 pp (37.0\% vs.\ 35.1\%) |
| affects timing quality | degrades the dialog system's response-timing precision |
| performs better | outperforms the MFCC baseline by 7.9 pp on macro-F1 |
| takes a long time | runs at 5 Hz on a consumer GPU (200 ms per update) |

#### E. 「精度／性能／品質／影響」が出たら必ず3点セットを示す

文中に「精度（accuracy / precision）」「性能（performance）」「品質（quality）」「影響（impact / effect）」が出てきたら、以下を明示：

1. **何の** 精度／性能／品質か（分類精度／応答タイミング精度／予測精度）
2. **どの値が** どうなのか（38.2\%、+1.9 pp、−50 ms）
3. **どのくらいの幅で** 信頼できるか（CI 95\% [+1.5, +2.3] pp、bootstrap N=1000）

### 8.5.5.3 推敲時のチェック（grep セルフレビュー）

執筆完了後、以下の語を grep し、**それぞれ「何を意味するか」が文脈だけで明確か**を確認。曖昧なら置換／例示追加：

```bash
# 抽象語の自己レビュー
grep -nE "same quantity|same value|conversion|pipeline|procedure|step|mapping" sections/*.tex
grep -nE "quality|precision|accuracy|performance" sections/*.tex
grep -nE "affects|involves|supports|is challenging|has an impact" sections/*.tex
grep -nE "certain|various|several|some |a number of" sections/*.tex
grep -nE "directly|effectively|appropriately|adequately" sections/*.tex
```

各ヒット箇所について自問：
- これは何の精度・品質か？（「response-timing の」か「classification の」か）
- 「影響する」のはどの方向か？（degrade か improve か）
- 「いくつかの」って具体的に何個か？

### 8.5.5.4 文意の自己テスト

書いた文を **1日後または別の人視点** で読み直し、「これは何のこと？」と聞かれて10秒で答えられるか確認。答えに詰まったら抽象語が残っている証拠。

### 8.5.5.5 例外：本当に一般論を述べる場合

「affects」「various」「several」が **本当に一般論として正しい場合** はあり得る。ただし、文意全体で「具体例は本文後半／別 section にある」ことが読者に伝わるように：

✅ `Various factors affect turn-taking timing in natural dialog; in this study, we focus on three: speaker overlap, sentence-final particles, and silence duration.` （直後に列挙して回収）
❌ `Various factors affect timing quality.`（回収なし）

---

## 8.6 セクション構造・ネスト階層の設計【重要】

### 8.6.1 問題意識：AI論文的スタイルを避ける

AIが初稿を書くと、以下のような「AI論文的／Markdown的」な構造になりがち：
- 細かい subsection が乱立（1セクションあたり5個以上）
- subsection 内にさらに subsubsection
- さらに `\textbf{項目名.}` で段落頭をラベル化（4階層目のネスト）
- 短い情報を itemize / enumerate で箇条書き化
- 「情報の塊」ごとに見出しを付けるため、連続する散文として読めない

これは**伝統的な工学系ジャーナル（Speech Communication, IEEE/ACM Trans., Computer Speech and Language, etc.）のスタイルとは乖離**している。査読者にもAI生成と見なされやすい。

### 8.6.2 推奨する構造基準

**セクション階層**：
- section（章）→ 必須
- subsection → 1セクションあたり **2〜4個** が目安（多くても5）
- subsubsection → **原則使わない**。どうしても必要なら1セクションに1-2個まで
- `\textbf{...}` による段落頭ラベル → 原則使わない。自然文の冒頭に溶け込ませる

**1セクションの分量の目安**：
- 極端に短い節（10-20行）なら subsection を設けず、連続した散文にする
- 長い節（100行超）でも、意味のまとまりで2-4個に束ねる

**箇条書き（itemize / enumerate）の使用基準**：
- 箇条書きが適切なケース：
  - Contributions（論文の貢献リスト）
  - アルゴリズムの明確な手順列挙（例：サンプリング戦略の1/2/3/4ステップ）
  - 列挙数が5個以上で散文化すると読みにくい場合
- 避けるべきケース：
  - 2-3項目の特徴列挙（散文で書ける）
  - 評価指標の羅列（散文で書ける）
  - モデルのバリアント説明（散文で書ける）

### 8.6.3 段落構造の原則

- **各段落は1つのトピックセンテンスで始まる**：「何の話をするか」を冒頭で示す
- subsection タイトルに相当する内容は、段落冒頭の文に自然に織り込む
  - 悪い例：`\textbf{Audio channel.} We use the close-talk wearable microphone...`
  - 良い例：`For the audio channel, we use the close-talk wearable microphone...`
  - 悪い例：`\subsection{CEJC}\nThe Corpus of Everyday Japanese Conversation...`
  - 良い例：（subsection廃止）`The Corpus of Everyday Japanese Conversation (CEJC) is our primary dataset...`

### 8.6.4 執筆時のチェックリスト

- [ ] 1つの section に subsection が5個以上ある → 統合できないか検討
- [ ] subsubsection を使っている → 本当に必要か再考
- [ ] `\textbf{...}` で段落頭をラベル化している → 自然文に書き換え
- [ ] itemize/enumerate が3個以上ある → 散文化できる箇所がないか検討
- [ ] 各段落の最初の文を読むと話の流れが追える → トピックセンテンス原則
- [ ] section → subsection → subsubsection → textbf の4階層ネストになっていないか

### 8.6.5 em-dash（`---`）は使わない

**ルール**：em-dash（`---` → 印刷時の「—」）は使用しない。

**理由**：音声言語情報処理系の工学系ジャーナル（Speech Communication、IEEE/ACM Trans.、Computer Speech and Language 等）では em-dash による挿入句・説明はほとんど使われない。英米の文芸・社会科学系では頻出するが、工学系の読者には違和感がある。

**コーパス実測根拠（2026-07追加）**：ICASSP+Interspeech 約52,000本の実測で、人間の論文のem-dash使用は**0.4回/論文（137/百万語）で2001年から2024年まで24年間安定**。2025年に両会議とも一斉に3〜5倍化（ICASSP 514/M、Interspeech 489/M）しており、これは人間の論文へのLLM混入と解釈される。つまり「—の多用＝AI臭」はデータで確定済み。AI生成実験でも、スタイル指示なしのAIは第1文から `X — explanation — is ...` 型の挿入を書いた（詳細: `speech_style_data.md`）。

**代替手法**（状況に応じて使い分け）：

| em-dash の用法 | 推奨代替 | 例 |
|---|---|---|
| 同格・言い換え | カンマ（`, ..., `）または括弧（`(...)`） | 旧: `the output---a scalar---is...` → 新: `the output, a scalar, is...` または `the output (a scalar) is...` |
| 挿入句・補足説明 | 括弧（`(...)`）または関係詞節（`, which ..., `） | 旧: `X advantage---which uses Y---is...` → 新: `X advantage, which uses Y, is...` |
| 例示（内部にカンマあり） | 括弧（`(such as A, B, and C)` / `(e.g., A, B)`） | 旧: `listener behavior---backchannels, nods---and...` → 新: `listener behavior (such as backchannels and nods) and ...` |
| 数値・具体値の補足 | 括弧（`(N points below ...)`） | 旧: `26.6\%\ accuracy---11.6 points below---showing...` → 新: `26.6\%\ accuracy (11.6 points below), showing...` |
| 2つのトピックの対比 | セミコロン（`; `）または文分割（`. `） | 旧: `seconds---directly interpretable---while...` → 新: `seconds, which is directly interpretable. Deriving... requires...` |
| 項目リストの説明導入 | コロン（`: `） | 旧: `\textbf{Feature type}---MFCC, CNN...` → 新: `\textbf{Feature type}: MFCC, CNN...` |

**en-dash（`--`）は通常通り使用可**：
- 数値範囲（`1--10\,s`）
- 複合語・2者接続（`human--agent studies`, `acoustic--linguistic patterns`）
- en-dash は em-dash とは別物であり、工学系でも標準的。

**特に注意：`A---B---C` の左右対称な挿入はAI執筆臭が最も強い**。文の途中に `---...---` で補足節を挟む構文（例：`X is evaluated under identical conditions---the same model and the same test set---and ...`）は、工学系ジャーナルではまず使われず、AIが書いた印象を強く与える。**コロンで導入して文を組み替える**か、**短い文に分割する**のが自然：
- 旧: `All encoders are evaluated under identical conditions---the same time-to-end model and the same held-out test set---and their CER is measured on a common test set, so ...`
- 新: `All encoders are evaluated under identical conditions: each is plugged into the same time-to-end model and tested on the same held-out test set, and its CER is measured on a common test set. The comparison therefore reflects only ...`
- 原則：挿入句を `---` で「挟む」のではなく、**コロンで「開いて」並列に展開**するか、**ピリオドで切って次文にする**。（2026-06-28 西村確認）

### 8.6.6 AI 初稿で起きがちなアンチパターン

AI が論文を執筆・推敲すると、以下の過剰分割が高頻度で発生する。初稿時点でチェックし、最初から避ける：

- 1セクション内に **5個以上の subsection**（情報を細かく分けすぎ）
- 20-40行程度の短いセクションに subsection が複数（分割する必要なし、連続散文で十分）
- **subsubsection の多用**（2階層で十分な情報を3階層に分けている）
- `\textbf{項目名.}` による段落頭ラベルが5個以上並ぶ（section → sub → subsub → textbf の4階層ネストに相当）
- 2-3項目の列挙で itemize/enumerate を使う（散文化可能）
- **"Discussion and Limitations" のように2つの性質が混在するセクションタイトル**（最初から2セクションに分けるべき）

**再発防止の原則**：
1. 初稿時から「subsection 2-4個 / subsubsection 不使用 / textbf段落頭 不使用」を徹底する
2. タイトルが "A and B" の形式で2つの概念を含む場合、セクションを2つに分けることを検討
3. 情報の塊ごとに見出しを付けたくなっても、**まずは連続する散文で書く**ことを優先
4. 査読サブエージェントに「構造がAI論文的でないか」の観点でチェックさせる

### 8.6.7 コーパス実測に基づく語彙・文体基準【2026-07追加・データ根拠付き】

ICASSP 2001–2026＋Interspeech 2007–2025 の全proceedings（約52,000本・7,600万語）を統計分析し、
「音声分野の人間の論文の実測値」と「LLM後（2024–2026）に急増したAI由来表現」を分離した。
**詳細データは同フォルダの `speech_style_data.md` を必ず参照**すること。要点:

1. **BAN語**（人間の使用頻度が3/百万語未満。使ったら即AI臭）:
   underscore系 / pivotal / nuanced / intricate / delve系 / meticulous系 / showcase系 /
   seamless / realm / harness系 / garnered / bolster系 / multifaceted / cutting-edge 等
   ＋フレーズ: in the realm of / paving the way / plays a crucial role / has garnered 等
2. **LIMIT語**（人間も使うが適正頻度あり）: notably・crucial は1論文0〜1回。
   comprehensively / seamlessly / innovative / holistic はほぼ使わない
3. **人間マーカー表現を意図的に使う**（AIは自発的に使わない）:
   Note that / It can be seen that / in order to / On the other hand / In other words
   ——現世代AIはBAN語をすでに回避するため、「避ける」だけでは不十分。「人間の定型を使う」が本命
4. **定量基準**: 文長中央値21語 / セミコロン30文に1回 / 修辞疑問なし / 本文箇条書きなし /
   段落は長短不均一に / 三点列挙の多用禁止
5. **会議別作法**: ICASSPは `CONCLUSION`・`Fig. N`、Interspeechは `Conclusions`・`Figure N`・
   Discussion節あり・番号付きAcknowledgements（詳細は `speech_style_data.md` §6）

---

## 8.7 論文プロジェクトの標準フォルダ構成【推奨】

### 8.7.1 標準レイアウト

新規論文プロジェクトを立ち上げる際は、以下の構成を推奨する：

```
プロジェクトルート/
├── latex原稿/                       ← LaTeX ソース・コンパイル対象
│   ├── main.tex
│   ├── compile.sh                   ← §6.3 標準テンプレ
│   ├── refs.bib
│   └── sections/                    ← 章ごとにファイル分割
│       ├── 0_abstract.tex
│       ├── 1_introduction.tex
│       └── ...
│
├── _ref/                            ← 【情報源】修論・過去原稿・関連発表
│   ├── master_thesis/
│   ├── 過去_国際会議発表/
│   ├── 過去_国内学会発表/
│   └── 既存ジャーナル投稿稿/
│
├── _AI用_関連各種データ/            ← AIと人間の共有作業スペース
│   ├── paper_writing.md             ← 本スキル（または ~/.claude/skills/ 側）
│   ├── 表・数値の参照元情報.md      ← 値のトレーサビリティ（§8.8.1）
│   └── 数値計算検証/                ← Python検証スクリプト（§8.8.2）
│       ├── 01_compute_*.py
│       ├── 02_verify_stability.py
│       └── 計算過程の説明.md
│
├── 参考文献確認作業/                ← 文献ハルシネーション検証（§3.1.2）
│   ├── 参考文献チェック.xlsx
│   └── PDFs/
│       ├── [cite_key]_[1stAuthor姓]_[Venue][Year].pdf
│       └── user_download/           ← AIが取得できない分のユーザー配置場（§3.1.6）
│
├── 論文修正作業用スクリプト/        ← 一括置換・Excel生成等のad-hocスクリプト
│   ├── generate_*.py
│   └── apply_*.py
│
├── _過去のもの/                     ← 過去バージョン・不要になった資料
│
└── CLAUDE.md / AGENTS.md / .agent/  ← プロジェクト全体ルール（make_project 由来）
```

### 8.7.2 各フォルダの役割

| フォルダ | 役割 | 永続性 |
|---|---|---|
| `latex原稿/` | 投稿対象の原稿一式 | 投稿まで保持、提出後はアーカイブ |
| `_ref/` | **全ての数値・事実の情報源**。修論・過去論文原稿・関連発表を集約 | 最重要、常時参照 |
| `_AI用_関連各種データ/` | AIが作業で参照／生成する補助資料（トレーサビリティ、検証スクリプト等） | 投稿後も残す（再現性担保） |
| `参考文献確認作業/` | refs.bib の検証証跡（Excel と PDF） | 投稿後も残す |
| `論文修正作業用スクリプト/` | 一括置換などの ad-hoc スクリプト | 本番では不要だが、再現性のため残す |
| `_過去のもの/` | 廃棄候補だが念のため保持 | 投稿後に削除検討 |

### 8.7.3 原則
- **`_ref/` は原則読み取り専用**（情報源なので書き換えない）
- **`_AI用_関連各種データ/` は AI と人間の共同作業スペース**。AI が生成した検証結果も人間が確認した結果もここに集約
- **ad-hoc スクリプトは `論文修正作業用スクリプト/` に集約**して `latex原稿/` を汚さない
- **バックアップは `_過去のもの/` に集約**（原稿ディレクトリに `main_backup_*.tex` を置かない）

---

## 8.8 数値検証スクリプト運用【ハルシネーション防止の実務】

### 8.8.1 値の4分類（情報源トレーサビリティ）

論文中の**全ての数値**を以下に分類し、`表・数値の参照元情報.md` 等で管理する：

| 分類 | 根拠 | 採用判断 | 記録必須事項 |
|---|---|---|---|
| **A** | `_ref` の PDF/原稿に**直接記載**されている値 | 採用 | 出典ファイル名・ページ/セクション |
| **B** | `_ref` 記載の値から**機械的に派生計算**可能（混同行列→MAE, 発話数合計等） | 採用 | 元の値＋計算式 |
| **C** | `_ref` の**生データ**（予測ファイル・混同行列等）から **Python で再計算**したもの | 採用（§8.8.3 安定性検証後） | スクリプトファイル名＋実行結果ログ |
| **X** | 上記いずれでもない／出典不明 | **削除**（§8.4.Y） | 削除理由＋文脈調整内容 |

### 8.8.2 Python 検証スクリプトの標準構成

`_AI用_関連各種データ/数値計算検証/` 配下に以下を配置：

```
数値計算検証/
├── 01_compute_<指標名1>.py          ← 1スクリプト = 1指標群
├── 02_compute_<指標名2>.py
├── 03_verify_stability.py           ← 複数seedの分散確認
└── 計算過程の説明.md                 ← 入力／前提／出力／採用判断
```

各スクリプトの書き方：
- **冒頭に前提条件を定数化**（bin 幅、閾値、seed 等）
- **入力**は `_ref/` 配下の原データ（absolute path またはプロジェクトルートからの相対）
- **出力**は stdout に数値と採用判断を JSON 形式で
- **依存を最小化**（1 スクリプトは単一の関心事のみ）

`計算過程の説明.md` には以下を記録：
- 何を計算したか（目的）
- どの `_ref` ファイル由来のデータを使ったか
- 計算式の導出根拠
- 10 seed での結果分布
- **最終的に論文に採用したか／不採用の理由**

### 8.8.3 数値安定性の検証プロトコル（ランダム性を含む計算）

Bootstrap、サブサンプリング等のランダム性を含む計算は：

1. **10 seed 以上**で実行
2. 最大値 − 最小値が**論文の有効桁の半分以下**なら採用
3. それを超える場合：
   - より小さい有効桁で記述（`38.24%` → `38.2%` → `38%`）
   - または**定性記述に置換**（"substantially above chance" 等）
4. **seed 固定・スクリプト保存**により、査読対応時に再実行可能にする

採用判断の例：
| 指標 | 10 seed 範囲 | 論文記載 | 判断 |
|---|---|---|---|
| Accuracy | 38.20%〜38.25% | `38.2\%` | 採用 |
| MAE | 280.3ms〜282.1ms | `280.6\,\text{ms}` | 採用（有効桁内） |
| 稀な指標 | 12.1%〜14.8% | 文で定性記述 | 不採用（幅が広すぎる） |

### 8.8.4 一度削除した値を復活させる場合の注意【再ハルシネーション防止】

`X` 判定で削除した値が、その後の検索で `_ref` 直記載（A）や Python 検証（C）で裏付けが取れた場合、復活させることがある。このとき以下に厳重注意：

1. **復活値単体**だけでなく、**周辺の記述**（「約 N ポイント改善」等の**差分値**、「X は Y より良い」等の**比較記述**）も正しいか再検証
2. 近接する**他のハルシネーション値**が「連動して」復活していないか再チェック（AI が「値 A が戻ったので値 B も戻そう」と勝手に補完する）
3. 復活位置の**前後数段落**を読み、削除時の文脈調整が取り残しになっていないか確認
4. 復活後、再度**全文検索で当該値の全出現箇所**を洗い出し、一貫した表記になっているか確認（Abstract / Intro / Results / Conclusion）

**原則**：「値が正しい」と「周辺記述が正しい」は別問題。個別確認を徹底する。

---

## 8.9 CRediT authorship contribution statement の記述原則

### 8.9.1 基本原則

CRediT (Contributor Roles Taxonomy) は**当該論文における寄与**を記述するもの。**研究室全体の役職**や**プロジェクト全体のマネジメント**とは切り分けて考える。

### 8.9.2 よくある困惑と整理

**困惑例**：指導教員が研究室・プロジェクト全体を統括しているが、この論文自体の投稿プロセスは筆頭著者が主導した場合、`Project administration` は誰か？

**原則**：
- **本論文の執筆プロジェクト**そのもの（方針決定、セクション分担、投稿プロセス管理）を主導した人
- 資金獲得・研究の初期着想・分野全体の指導は **Funding acquisition / Conceptualization / Supervision** 側に分ける
- 論文単位で見れば、筆頭著者・指導教員の役割は重複しないことが多い

### 8.9.3 役割の使い分け早見表

| 役割 | 対象 | 典型的な担当 |
|---|---|---|
| Conceptualization | 研究アイディアの着想 | 指導教員 or 筆頭著者 |
| Methodology | 研究手法の設計 | 筆頭著者（＋共著者） |
| Software | コード実装 | 実作業者（修士院生等） |
| Validation | 再現性・再計算の確認 | 共著者 |
| Formal analysis | 統計・数理的扱い | 実作業者 |
| Investigation | 実験実施 | 実作業者 |
| Resources | 計算機・データ提供 | 指導教員／機関 |
| Data curation | データ整備・アノテーション管理 | 実作業者 |
| Writing - original draft | 初稿執筆 | 筆頭著者 |
| Writing - review \& editing | 推敲・査読対応 | 全員 |
| Visualization | 図表作成 | 実作業者 |
| Supervision | 研究指導 | 指導教員 |
| Project administration | **本論文執筆プロジェクト**の管理 | 筆頭著者 or 責任著者 |
| Funding acquisition | 資金獲得 | 指導教員 |

### 8.9.4 記述例（Elsevier elsarticle）

```latex
\section*{CRediT authorship contribution statement}
\textbf{First Author}: Methodology, Project administration, Supervision, Writing -- original draft, Writing -- review \& editing.
\textbf{Second Author}: Data curation, Formal analysis, Investigation, Methodology, Software, Visualization, Writing -- review \& editing.
\textbf{Third Author}: Supervision, Writing -- review \& editing.
\textbf{Fourth Author}: Conceptualization, Funding acquisition, Resources, Supervision, Writing -- review \& editing.
```

### 8.9.5 原則
- **複数人に同じ役割を割り当て可**（Supervision, Writing - review \& editing は特に）
- **役割名は CRediT 公式リスト（14項目）に合わせる**（勝手に作らない）
- **Writing は `Writing -- original draft` と `Writing -- review \& editing` の 2 種類**。ハイフンは en-dash（`--`）

---

## 8.10 修正案の複数候補提示形式【AI→ユーザー対話】

### 8.10.1 原則

AIが修正を提案する際、**選択が分かれうる変更**は候補 1／候補 2 の形式でユーザーに提示する。即時実行ではなく、**ユーザーに選択させる**。

### 8.10.2 標準フォーマット

```
### 修正対象：[セクション名／行番号]

**現状**：
> ...原文の該当箇所を引用...

**候補 1**：[置換後の簡潔な説明]
> ...置換後の文...
- **長所**: [この案のメリット]
- **短所**: [この案のデメリット・トレードオフ]

**候補 2**：[置換後の別案]
> ...置換後の文...
- **長所**: [別の視点のメリット]
- **短所**: [別のデメリット]

どちらで進めますか？（もしくは別案があれば指示ください）
```

### 8.10.3 候補提示を使う場面・使わない場面

| 場面 | 候補提示 |
|---|---|
| 明白な誤り（タイポ、数値バグ、リンク切れ） | 不要、即修正 |
| 表現の好み（語彙、語順、詳しさ） | **必要** |
| 構造変更（章の統合・分割、節の並び替え） | **必要**（影響範囲が広い） |
| ハルシネーション値の削除 | **必要**（関連する他の記述への影響確認のため） |
| 英訳・和訳の揺れ | **必要** |
| 書式統一（`\cite` → `\citep` 等） | 方針確認は必要、実行は一括可 |

### 8.10.4 候補数の目安
- **候補 2 個が標準**（比較しやすい）
- 3 個以上は選択コストが上がるので、AI 側で絞って提示
- 候補間の差分を明確に（「やや柔らかく／固い」等、軸がはっきりしているほうが選びやすい）

---

## 9. 補助ファイル

論文執筆と並行して作成・メンテナンスする補助ファイル。**全て `_AI用_関連各種データ/` 配下に配置**する（§8.7 参照）。

### 9.1 参考文献リスト.md【指導教員確認用】

**用途**：`refs.bib` に追加した文献を、短縮形式で一覧化して**指導教員・共著者に確認依頼**する。Excelより読みやすく、差分レビューしやすい。

**フォーマット例**：
```markdown
# 参考文献リスト

## 追加済み（先生確認待ち）
- [turngpt] Ekstedt et al., "TurnGPT: A Transformer-based Language Model for Predicting Turn-taking in Spoken Dialog", EMNLP 2020
  → 発話交替予測の Transformer 系先駆け。§2 関連研究で言及
- [vap1] Ekstedt & Skantze, "Voice Activity Projection: Self-supervised Learning of Turn-taking Events", Interspeech 2022
  → 現在の turn-taking モデルの主流。§2 比較表に含める

## 確認済み・採用
- [wav2vec2] Baevski et al., "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations", NeurIPS 2020
  → 本研究のエンコーダ基盤。§4 で詳述
```

**運用**：
- 新規追加時はまず「追加済み・確認待ち」に書き、確認後「確認済み・採用」に移動
- 除外した文献（検討したが採用しない）は `## 却下` セクションに理由とともに残す

### 9.2 専門用語.md【日英対訳・表記ゆれ統一】

**用途**：
- 論文全体で**専門用語の英訳を統一**
- **初出時のフルスペルアウト**管理（略語は必ず初出でフル展開）
- **類似用語の使い分け**ルール記録
- **固有モデル名・システム名**の表記統一

**フォーマット例**：

| 日本語 | 採用英訳 | 初出箇所 | 略語フルスペル | 備考 |
|---|---|---|---|---|
| 発話 | utterance | §1 p.1 | — | `speech` は使わない |
| 発話終端 | utterance end | §1 p.1 | — | `utterance boundary` と混在させない |
| ターン交替 | turn-taking | §1 p.1 | — | `turn-change` は非標準 |
| 音響特徴量 | acoustic features | §4.2 | — | `audio features` と混在させない |
| 隠れ状態 | hidden states | §4.3 | — | `hidden representations` と使い分けない |
| 自動音声認識 | ASR | §2 | Automatic Speech Recognition | 初出 §2 でフルスペル |
| 音声区間検出 | VAD | §3 | Voice Activity Detection | 初出 §3 でフルスペル |
| Voice Activity Projection | VAP | §2 | Voice Activity Projection | モデル名、初出でフル |
| 日本語日常会話コーパス | CEJC | §3 | Corpus of Everyday Japanese Conversation | 初出 §3 でフル |

**チェックポイント（AI が自動チェックする）**：
- 同じ日本語概念に対して**2種類以上の英訳**を使っていないか（例：`turn-taking` と `turn-change` の混在）
- 略語の**初出展開**が全て揃っているか（`ASR`, `VAD`, `CEJC` 等）
- 固有のモデル名・システム名（`TurnGPT`, `VAP`, `wav2vec 2.0` 等）の大文字小文字・数字表記が統一されているか
- 複合語のハイフネーション（`turn-taking` vs `turn taking`、`self-supervised` vs `self supervised`）が統一されているか

**運用**：
- 執筆中、新語が出たら即座に追記（後回しにすると混乱の元）
- 推敲時に全文 grep で一貫性を検証
- 査読対応時、査読者が用語に言及した場合はここに反映

### 9.3 図表作成依頼.md【未完成図表のトラッキング】

**用途**：図表の未完成部分・差し替え依頼を記録。指導教員・共著者との分担が明確になる。

**フォーマット例**：
```markdown
# 図表作成依頼

## 未完成・差し替え待ち
- [ ] Fig. 3: システム全体図の再作成（現状は手書きスキャン） → 依頼先：[共著者名] / 締切：2026-05-01
- [ ] Table 2: 実験結果の数値が最新版ではない → 依頼先：筆者本人（Python再計算） / 締切：2026-04-25

## 作業中
- [~] Fig. 5: 混同行列のヒートマップ生成 → 筆者本人、2026-04-22 着手

## 完了済み
- [x] Fig. 1: Architecture overview — 2026-04-15 完了
- [x] Table 1: Related Work comparison — 2026-04-18 完了
```

### 9.4 表・数値の参照元情報.md【ハルシネーション防止の中核】

詳細は **§8.8.1** 参照。論文中の全数値を A/B/C/X に分類してトレーサビリティを担保する。

### 9.5 数値計算検証/（フォルダ）

`_AI用_関連各種データ/数値計算検証/` に Python 検証スクリプトを配置。詳細は **§8.8.2** 参照。

### 9.6 補助ファイルの運用原則

- **全て `_AI用_関連各種データ/` に集約**（ルートを汚さない）
- **最新状態を保つ**（古くなったら即更新、古い情報を残したまま放置しない）
- **投稿後も削除しない**（再現性・査読対応・次論文への再利用のため）
- 共著者・指導教員との**共有はこのフォルダ単位**で行う

---

## 9.5 最終通読（Final Read-Through）【必須】

### なぜ必要か
複数回の査読・推敲・置換を経た原稿には、以下の問題が残存する可能性が高い：
- 置換の副作用（文法が破綻、語の重複、"a not simple X" のような不自然表現）
- 章間の整合性ズレ（§3 と §5 で同じ情報が重複、数値の不一致）
- セクションをまたぐ参照の破綻（`\ref{}` が別の節番号を指す）
- 構造変更に伴う記述の流れの不自然さ
- 変更した表現が前後の文脈と合わない

### タイミング
- 全ての内容変更・構造改革・置換作業が完了した後、提出前の**最終ステップ**として必ず実施
- 査読サブエージェントによる機械的チェックとは別に、**人間の目で頭から末尾まで読む**
- 章単位のチェックではなく、**通しで読む**ことで章間の流れを評価

### チェックポイント
- [ ] Abstract から Conclusion まで通読し、論理の流れが自然か
- [ ] 同じ情報が複数章で冗長に書かれていないか（Data description と Experimental setup 等、記述が重複しがちな章）
- [ ] 語の重複（"shows ... shows"、"practical practicality" のように動詞/名詞が同一単語で連続する）
- [ ] 一括置換で発生した不自然表現（"steady with" のような英語として成立しない組み合わせ、"about balanced" のような collocation 違反、"got by" のような informal 表現の混入）
- [ ] 数値の一貫性（Abstract、Introduction、Results、Conclusion で同じ数値が使われているか）
- [ ] 図表参照の連番（`Fig. 1`, `Fig. 2`, ... が飛んでいないか。削除した図の参照が残っていないか）
- [ ] 参照セクション名が本文と一致しているか（Section タイトルを変更した場合、参照側も更新されているか）
- [ ] 各章の冒頭段落が次章への導入・前章からの接続として機能しているか
- [ ] モデル名・手法名の初出時に必ず `\citep{}` が付与されているか

### AI支援の活用方法
- AI に「この論文を頭から読んで、不自然な表現や論理の飛躍がないか報告してください」と依頼
- ただし、AI は「文法的に正しい」ものを見逃しやすいので、最終判断は人間が行う
- 章ごとに分割して読んでもらうと見落としが少ない

### 9.5.X PDF版での最終通読【ソース通読とは別に必須】

`.tex` ソースの通読で論理・文面をチェックしたら、**コンパイル後の PDF を1ページ目から末尾まで通読**する。ソース通読では検出できない問題が PDF でのみ顕在化する。

#### PDF でのみ見える問題

| 問題 | 具体例 |
|---|---|
| レイアウト崩れ | 表の列ずれ、図のはみ出し、キャプションの位置ずれ |
| ページ跨ぎ | 表・図が2ページに分断、段落冒頭がページ末に孤立 |
| 改行破綻 | DOI/URL の不適切な改行、長い単語のハイフネーション失敗 |
| 余白バランス | Highlights ページに大きな空白、Abstract が1ページ目末に押し出される |
| 連番不整合 | Figure 5 の次に Figure 7（Figure 6 が未参照／削除の残骸） |
| 参考文献末尾 | リスト末尾まで正しくレンダリングされているか |
| Appendix 連番 | A.1, A.2, ... が正しく振られているか |
| ヘッダー／フッター | 著者名・タイトルの誤記、ページ番号の欠落 |

#### PDF 通読チェックリスト
- [ ] 表紙（著者・所属・連絡先）の表示OK
- [ ] Abstract / Highlights / Keywords ページの余白が自然
- [ ] 全ての Figure/Table が本文言及位置の近くにある（遠く離れていない）
- [ ] 数式の改行・字下げが崩れていない
- [ ] 参考文献リストが末尾まで途切れずにレンダリング
- [ ] Appendix のセクション番号・連番が正しい
- [ ] 全ページ通しで**目視通読**（13ページ程度なら30分以内）
- [ ] 印刷時に読みやすいか（色依存の図になっていないか）

#### AI 支援の限界
- AI は PDF を画像として読めるが、**レイアウトの微妙な崩れやキャプション位置ずれは見逃しやすい**
- **最終 PDF 通読は人間が必ず行う**。AI による通読は補助として使う（章ごとに「何か気になる点は」と聞く程度）

---

## 10. 重要な教訓

1. **数値は常に検算する**: 分布・混同行列からの派生計算（平均、MAE、within-one-bin accuracy等）は必ずPythonスクリプトで検証し、本文・Abstract・Conclusion で同一の値が使われるか確認する
2. **査読者の「任意」指摘も対応する**: 査読サイクルで全ての指摘に対応すれば、Accept に到達しやすい
3. **パラメータフリーの理論的ベースラインは強力**: 追加実験なしで「モデルの付加価値」を定量的に示せる（例：タスクに応じた統計ベースライン、duration-prior、chance level）
4. **Bootstrap CIは単一ランの限界を補う**: ただし seed variance は別途必要であることを明記
5. **比較表（Related Work Table）は論文の位置づけを明確にする**: 査読者から高評価されやすいが、記載内容のハルシネーション検出を徹底（§3.2 参照）
6. **AI による統計値の捏造に注意**: McNemar/paired CI 等は元データなしでは計算不可能。AI が初稿に追加した統計値は必ず検証（§8.4.X 参照）

---

## 付記：ユーザーへの情報提示ルール（2026-08-05）
ユーザーに情報提示・確認（レビュー依頼・候補提示・チェックリスト等）を行う際は、.md でなく **HTML で提示**する（`open` でブラウザ表示）。コピペが崩れる場合のみ .md を併用し、その旨を HTML に記載する。
