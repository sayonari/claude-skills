---
name: field_literature_survey
description: 論文を執筆する前に、対象分野の代表的国際会議・ジャーナル（Interspeech, ICASSP, IEEE/ACM TASLP, Speech Communication, ACL, NAACL 等）の過去N年分の論文を多数精査し、文体・語彙・記述内容・図表のクセを学習・整理するスキル。「別分野の人が書いた論文」のような原稿になることを防ぐため、論文執筆プロジェクトの早い段階で実行する準備作業。paper_writing スキルと併用する。
---

# 分野文献調査スキル（Claude 用）

論文執筆プロジェクトを始める前、もしくは大幅な改稿前に、**対象分野の代表的会議・ジャーナルの論文群を多数精査**し、文体・語彙・記述内容・図表のクセを学習・整理するための skill。

**位置づけ**：`paper_writing` skill は「論文執筆の汎用ルール」を提供する。本 skill は「**分野特有のクセ**」を学習する作業をカバーする。両者は併用する。

---

## いつ使うか（トリガー）

- **新規論文執筆プロジェクトの Phase A の早い段階**（投稿先決定後、執筆開始前）
- 既に書いた原稿が「分野のクセに合っていない／別分野の人が書いたように見える」と指摘された時
- 査読で「論文のスタイルが本会議の標準と異なる」と指摘された時
- 投稿先を変更した時（例：Interspeech → IEEE/ACM TASLP）

---

## 何を作るか（成果物）

調査結果を以下の構造でプロジェクトに保存：

```
_AI用_関連各種データ/分野文献調査/
├── field_style_notes.md          # 総合ノート（最重要）
├── vocabulary.md                 # 語彙・専門用語のクセ
├── phrasing.md                   # 典型表現・文構造の集約
├── section_patterns.md           # セクション構成の典型パターン
├── figure_table_patterns.md      # 図表のクセ
├── references_studied.md         # 精査した論文の一覧（出典・URL・DOI）
└── corpus/                       # 精査した論文の PDF / テキスト抜粋
    ├── interspeech_2024_XXX.pdf
    ├── interspeech_2024_XXX_abstract_intro.txt
    └── ...
```

ノートは継続的に育てる。同じ分野で複数論文を書く場合、過去の調査結果を再利用する。

---

## 標準ワークフロー

### Step 1. 対象スコープの確定（ユーザー合意）

以下をユーザーと合意：

| 項目 | 例 |
|---|---|
| 投稿先 | Speech Communication |
| 関連会議・ジャーナル | Interspeech, ICASSP, IEEE/ACM TASLP, Computer Speech and Language, SLT, ASRU |
| 対象年度 | 過去5年（推奨）／過去3年（短縮版） |
| キーワード | turn-taking, end-of-utterance, voice activity projection, response timing |
| 精査本数 | 50〜100本（推奨）／20〜30本（短縮版） |
| 重視する観点 | 文体／語彙／構成／図表／統計提示／その他 |

### Step 2. 文献リストの構築

参照ソース：

| ソース | URL | 範囲 |
|---|---|---|
| ISCA Archive | `https://www.isca-archive.org/` | Interspeech, Odyssey, SLT, etc. |
| IEEE Xplore | `https://ieeexplore.ieee.org/` | ICASSP, TASLP, SLT, ASRU |
| ACL Anthology | `https://aclanthology.org/` | ACL, NAACL, EMNLP, EACL |
| Elsevier ScienceDirect | `https://www.sciencedirect.com/` | Speech Communication, Computer Speech and Language |
| DBLP | `https://dblp.org/` | クロス検索 |
| Google Scholar / Semantic Scholar | 引用数・関連度ベースの検索 |

検索方針：
- `キーワード AND 会議名 AND 年度`
- 各会議×年度ごとに5〜20本リストアップ
- 以下を優先：
  1. **引用数の多い論文**（その分野の standard）
  2. **自分の研究の参考文献に多く出てくる著者**の論文（投稿先のコミュニティ）
  3. **best paper / outstanding paper award** 受賞論文
  4. **直近の関連サーベイ論文**（典型表現の参考）

### Step 3. 各論文の取得

- PDF を取得可能なら `corpus/` に保存
  - `WebFetch` で abstract / intro まで取れる場合あり
  - フルテキストは IEEE Xplore など API/DOI 経由
- ダウンロード不可・有料の場合は、abstract と introduction のみ Web fetch で取得し、`*_abstract_intro.txt` として保存
- 著者・年・タイトル・DOI・URL を `references_studied.md` に記録

**ファイル命名規約（推奨）**：
```
{venue}_{year}_{first_author_last}_{short_title_slug}.pdf
例: interspeech_2024_smith_endpointing_for_streaming_asr.pdf
```

### Step 4. 観察項目（精査チェックリスト）

各論文ごとに以下を観察し、`field_style_notes.md` 等に転記する。

#### A. タイトル

- 形式：動詞型 / 名詞句型 / "Toward X" 型 / 質問型
- 語数（平均何語か）
- 「タスク名 + アプローチ + データ」の語順
- 副題（コロン区切り）の有無

#### B. Abstract

- 構造（典型的な5要素：背景／課題／提案／結果／意義）の文数配分
- 数値を入れる位置（最後／最初／全体に散らす／無し）
- "We propose / present / introduce / describe" の使い分け
- 平均語数

#### C. Introduction

- 「分野の重要性」を述べる典型1段落の構造
- 既存手法の列挙パターン（手法名 → 限界 → 提案へ繋ぐ）
- contributions リストの形式（itemize / 散文 / 番号付き）
- 段落数の典型（3〜5段落？）
- 最後の段落は「論文の構成」を述べるか？

#### D. Related Work

- 単独 section vs Intro に統合
- グルーピングの仕方（手法ベース／タスクベース／データベース／時系列）
- 引用密度（1段落あたり何件か）
- 「本研究との違い」を明示する慣習があるか

#### E. Method / Approach

- 数式の使い方（密度、ナンバリング、let-style 定義）
- 図の入れ方（system overview を最初に置くか）
- "we use", "we adopt", "following [X]" のパターン
- pseudo code / algorithm の使用頻度

#### F. Experiments

- データセット記述の典型構造（出典・サイズ・分割・言語）
- 比較対象（自分の手法以外に必ず置くべき baseline）
- 評価指標の標準（accuracy / F1 / EER / MAE / WER / BLEU 等）
- 実装詳細（hyperparameters）の記述位置（本文 / appendix）

#### G. Results

- 表の形式（行・列の配置、bold / underline / arrow の使い方）
- 「X% improvement over baseline」型 vs 「absolute numbers」型
- 統計的有意性をどう示すか（CI / p-value / bootstrap / 何もなし）
- ablation の位置（独立 subsection / Results 末尾）

#### H. Discussion

- limitations を独立節として書くか（特にジャーナルは独立）
- error analysis の典型構造
- qualitative example の入れ方（特に NLP/対話系）

#### I. Conclusion

- 文数（多くは3〜5文）
- "Future work" の書き方（具体的 vs 抽象的）

#### J. References

- 平均何件か（会議論文：30件前後、ジャーナル：50件以上）
- 自己引用・指導教員引用の比率
- citation style（plain / harvard / numeric）

#### K. 図表

- system architecture 図の典型形式（モジュール図 / データフロー図）
- confusion matrix の標準形式
- caption の長さ（1文 / 複数文）
- 表の置き方（[t]/[h] の使い分け）

#### L. 専門用語・略語

- よく使われる略語（VAP, TRP, IPU, EOU, EOT, ASR, SLU, VAD, …）
- 略語を初出で定義する慣習があるか
- 動詞表現の使い分け（"predict" / "estimate" / "detect" / "forecast" / "model"）
- 名詞表現の使い分け（"utterance" / "segment" / "turn" / "IPU"）

#### M. 文体の特徴

- 一人称（we）の使用頻度
- 受動態 vs 能動態の比率
- 文の平均長
- 段落の平均長

#### N. 「分野の暗黙の常識」

- データセットを必ず挙げる慣習（CEJC, CSJ, LibriSpeech, etc.）
- 計算リソース記述（GPU 型番、学習時間）の慣習
- reproducibility（コード公開）の言及位置
- ethics statement の有無（特に対話系）

### Step 5. クロスチェック（会議間の差異）

会議ごとの差分を比較し、`field_style_notes.md` に「**[会議名] の特徴**」セクションを設ける：

- **Interspeech**：4ページ＋参考文献、acoustic 寄り、図を多用
- **ICASSP**：4ページ、信号処理寄り、数式重視
- **IEEE/ACM TASLP**：ジャーナル、密度高、評価が詳細
- **Speech Communication**：ジャーナル、対話系・知覚系も含む幅広い
- **ACL / EMNLP**：NLP 寄り、言語データ重視
- など

### Step 6. ノートの構造化（成果物の生成）

`field_style_notes.md` の推奨構造：

```markdown
# 分野文献調査ノート

## メタ情報
- 投稿先：[Speech Communication]
- 関連会議：[Interspeech, ICASSP, IEEE/ACM TASLP, ...]
- 対象年度：[2020-2024]
- 精査本数：[N 本]
- 調査日：[YYYY-MM-DD]
- 調査者：[西村 / Claude]

## 1. タイトル
[クセ・典型パターン]
[Good examples（出典付き）]

## 2. Abstract
[クセ・典型パターン]
[Good examples（出典付き）]

## 3. Introduction
...

## ... （A-N の各観点）

## X. 会議別の特徴
### Interspeech
...
### ICASSP
...

## Y. 用語辞書（vocabulary.md と連携）
| 概念 | 典型語彙 | 例文（出典付き） |
|---|---|---|
| 発話末予測 | end-of-utterance prediction / turn-end prediction / EOU prediction | [Smith et al., 2023] "We propose an EOU prediction model that..." |
| ... | ... | ... |

## Z. 典型表現テンプレ（phrasing.md と連携）
### Intro 冒頭の典型表現
- "X is a fundamental task in spoken dialog systems."
- "Recent advances in Y have ..."
- "Despite progress in Z, ..."

### contributions リストの典型表現
- "We make the following contributions:"
- "Our contributions are threefold:"
- ...

## AA. 引用すべき定番文献（references_studied.md と連携）
| 概念 | 定番引用 |
|---|---|
| 一般のturn-taking心理学 | Stivers et al. 2009 |
| 日本語応答時間 | Kitaoka et al. 2005 |
| VAP | Ekstedt and Skantze 2022 |
| ... | ... |
```

### Step 7. 論文執筆中の活用

`paper_writing` skill の各 Phase で本 skill の成果物を参照する：

| Phase | 参照タイミング |
|---|---|
| Phase A（プロジェクト立ち上げ） | 投稿先決定後、本 skill を起動 |
| Phase C（本文執筆）開始時 | `field_style_notes.md` を全読 |
| Phase C 各セクション執筆時 | 該当セクションのノートを再読 |
| Phase D（検証） | 「会議別の特徴」と現原稿の整合チェック |
| Phase E（投稿準備） | 引用すべき定番文献の漏れチェック |
| 査読対応時 | 「分野標準ではどうか」を確認 |

---

## 注意事項

### 時間コスト
- 50本精査でも数日〜1週間かかる
- 投稿締切が迫っている時は無理に全部やらず、**まず10〜20本に絞る**（abstract+intro のみ精読）
- 継続調査として「投稿後も少しずつ追加」する運用が現実的

### 著作権・倫理
- PDF を copy する場合、調査用の **fair use / private use 範囲** を守る
- 観察に徹し、他論文の文言を **直接コピーしない**（盗用）
- ノートに引用するときは必ず出典（著者・年・タイトル・該当ページ）を併記

### 信頼性
- AI が「クセを抽出した」と言っても、**人間（指導教員・査読者）の感覚と照合**する
- 自動抽出だけでなく、ユーザーが「これは確かにそう」と感じるかをチェック
- ノートには **必ず元論文の出典**を残し、追跡可能にする

### 抽出の偏り
- 引用数の多い論文ばかり見ると「定着した型」しか拾えない
- 新規性の高い投稿が増えた近年（直近1〜2年）の論文も含める

---

## 関連スキル

- **`paper_writing`**：論文執筆の汎用ルール。本 skill の成果物（`field_style_notes.md` 等）を参照しながら使う。
- **`make_project`**：プロジェクト初期構築。本 skill 用のフォルダ（`_AI用_関連各種データ/分野文献調査/`）はここで作成しておくと良い。

---

## 補助ツール（推奨実装パターン）

### 文献メタデータ収集の自動化

ユーザー環境で以下のような Python スクリプトを用意すると効率化：

```python
# 例：ISCA Archive から Interspeech 2024 の論文リストを取得
import requests
from bs4 import BeautifulSoup

url = "https://www.isca-archive.org/interspeech_2024/"
# ... タイトル・著者・PDF URL を抽出
# references_studied.md の表に整形して出力
```

### PDF からの本文抽出

```bash
pdftotext -layout paper.pdf paper.txt
```

抽出後、abstract と introduction のみを切り出して `corpus/*_abstract_intro.txt` として保存。

### 観察項目の半自動化

```python
# 例：abstract の平均語数を計算
import statistics
abstracts = [...]
word_counts = [len(a.split()) for a in abstracts]
print(f"Avg: {statistics.mean(word_counts):.1f}, Std: {statistics.stdev(word_counts):.1f}")
```

これらの補助スクリプトは `_AI用_関連各種データ/分野文献調査/scripts/` 配下に置くと再利用しやすい。

---

## 実装済み大規模パイプライン【2026-07実施・再利用可能】

本 skill の方法論を大規模実装した実績がある。**新たに調査する前に、まずこの成果物を確認・再利用すること**。

### 場所
`/Volumes/ROBOCO_SAN/AItask/音声系英語論文執筆スキル作成/`

- `_ref/papers/`：ICASSP 2001–2026＋Interspeech 2007–2025 の全proceedings（約82GB。研究室NASのアーカイブと同期済み）
- `corpus/`：全PDFのテキスト抽出済みコーパス（約52,000本・7,600万語）
- `analysis/`：年次別統計・トレンド・確定リスト（avoid_list.md / use_list.md / ai_vs_human/ 等）
- `scripts/`：再実行可能なパイプライン一式
  - `download_isca.sh <year>`：ISCA ArchiveからInterspeech proceedingsを丁寧に収集
  - `sync_nas.sh` / `backup_to_nas.sh`：研究室NASとの同期（SSH経由rsync。SMBの10倍以上速い）
  - `extract_text.sh <会議> <年>`：pdftotextによる一括テキスト化
  - `analyze_corpus.py`：語彙/n-gram/記号/文長/章立て/AI典型語の統計
  - `trend_report.py`：年次推移テーブル生成
  - `build_avoid_list.py`：BAN/LIMIT/WATCH の自動分類（baseline×急増率）
  - `compare_style.py`：AI生成テキストと実論文のスタイル指標比較

### 方法論上の重要な知見（この skill の手順に対する改訂）

1. **3層コーパス設計を標準とする**：
   - 第1層（コア）2015–2022 = ChatGPT以前の「純粋な人間文体」。頻度基準はここから作る
   - 第2層 2023以降 = 人間論文に既にLLM混入がある。**文体の見本にしてはならない**。
     逆に「急増語の検出器」として使う（例: em-dashは24年間137/M前後で安定→2025年に500/M弱へ爆発）
   - 第3層 過去の飛び石 = 核となる定番表現と流行語の区別に使う
2. **AI生成との直接差分が有効**：同テーマでスタイル指示なしのAIにセクションを書かせ、実論文と
   指標比較（compare_style.py）。現世代AIは有名なAI語を既に回避するため、語彙ではなく
   **構造（文長・段落均質性・修辞疑問・三点列挙・人間マーカー欠落）**に差が出る
3. **成果はデータごと `paper_writing` に反映済み**：`~/.claude/skills/paper_writing/speech_style_data.md`
   に確定リストあり。定期的（年1回程度、新年度proceedings追加時）に再生成して更新すること

---

## まとめ

本 skill は **「論文を書く前に分野のクセを学ぶ」** ための準備作業を体系化したもの。一度作ったノートは継続的に育て、同じ分野で複数論文を書く際に再利用する。`paper_writing` の汎用ルールと併せて、**「分野に馴染んだ、しっかり伝わる論文」** を書くための土台を作る。
