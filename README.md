# Claude Skills（sayonari / 西村良太）

Claude Code で使用する個人スキル集．`~/.claude/skills/` に配置され，各スキルは `SKILL.md` を持つ．Claude はタスク内容に応じてこれらを自動参照する（または `/スキル名` で明示起動）．

## 導入方法

```bash
git clone https://github.com/sayonari/claude-skills.git ~/.claude/skills
```

既に `~/.claude/skills/` がある場合は，必要なスキルのフォルダだけをコピーしてもよい．各スキルは独立して動く（paper_writing と paper_review，field_literature_survey は互いを参照する）．

## スキル一覧

| スキル | 用途 | 主な内容 |
|---|---|---|
| [kakenhi_writing](kakenhi_writing/SKILL.md) | **科研費研究計画調書の執筆・推敲** | JSPS審査制度と評定要素の原文／「減点理由を書かせない」防御戦略（定型所見リストへの1対1対応）／審査員の定量データ（評点3=採択率5%，当落ライン4,3,3）／書き方の定石（概要10行・問いの疑問文化・準備状況の確度グラデーション）／種目別ポイント（基盤B・挑戦的萌芽）／分担者設計／採択調書7本精読による共通構造チェックリスト／不採択が続く場合の診断と改訂戦略／図の設計とLaTeX固定ページ枠の実務．2026-08にJSPS一次資料・書き方解説13情報源・公開採択調書・KAKEN採択課題275件超・審査員証言17情報源の網羅調査から構築 |
| [paper_writing](paper_writing/SKILL.md) | **音声言語情報処理系の論文執筆**（Speech Communication, IEEE/ACM Trans., Interspeech, ICASSP等） | 標準ワークフロー（プロジェクト立ち上げ→情報整理→執筆→検証→投稿）／ハルシネーション防止（参考文献の三原則・数値トレーサビリティA/B/C/X分類）／読者層に合わせた英語表現の平易化辞書／AI臭排除（em-dash禁止・BAN語・コーパス実測基準）／セクション構造ルール／compile.sh運用／修正履歴マーキング（\rev{}） |
| [paper_review](paper_review/SKILL.md) | **論文査読**（他者論文の査読委員査読＋執筆中原稿の自己査読） | 査読前ヒアリング／機密保持／3観点並行チェック（技術内容・参考文献検証・語彙表現）／査読コメント作成．paper_writing と対で使用 |
| [field_literature_survey](field_literature_survey/SKILL.md) | **分野文体調査**（論文執筆の準備作業） | 対象分野の代表的会議・ジャーナルの過去N年分の論文を多数精査し，文体・語彙・図表のクセを学習．「別分野の人が書いた論文」化を防ぐ．paper_writing の Phase A-5 で使用 |
| [exam_grading](exam_grading/SKILL.md) | **筆記試験のAI採点**（中間・期末・小テスト／科目非依存） | 作問設計→スキャン→本人特定→採点基準の明文化→並列AI採点→機械検証→**★教員確認HTML（答案画像付き）**→返却→疑義申告対応の全工程／部分点の刻み方・連鎖切り・別解の扱い／学生のプロンプトインジェクション対策／Drive共有事故の再発防止／スクリプト雛形一式（クロップ・検証・集約・確認HTML・赤入れ・成績PDF・Apps Script）．単体配布版: [sayonari/exam-grading-skill](https://github.com/sayonari/exam-grading-skill) |
| [dialysis_conference_travel](dialysis_conference_travel/SKILL.md) | **国際会議・出張と維持血液透析の両立**（判断アルゴリズム） | 参加日程の設計／旅行透析の病院調整（直接連絡のみ・第一波3件）／透析間隔ルール（中3日を作らない・中2日連続を避ける）／透析日程優先の航空券・宿選定／大学の出張手続き／英文医療書類／間隔検算スクリプト `scripts/check_intervals.py`．個人の医療値・会員情報は `~/.claude/profiles/` に分離する4層構造 |
| [make_project](make_project/SKILL.md) | **新規プロジェクトの初期構築**（`/make_project`） | `.agent/`（handoff・memory・scripts）・`.spec/`（SPEC/PLAN/TODO/KNOWLEDGE）・`CLAUDE.md`/`AGENTS.md`・Git初期化の定型セットアップ／既存プロジェクトの更新モード／Google Drive アーカイブ先の決定と `sync_to_drive.sh` の自動作成 |
| [frontend-design](frontend-design/SKILL.md) | **Webフロントエンドのデザイン**（Anthropic 公式配布・Apache-2.0） | 高品質なWebコンポーネント・ページの制作．ジェネリックなAI美学を避けたUI設計 |

## 共通ルール（西村研の運用．他所で使う場合は適宜読み替える）

- **ユーザーへの情報提示・確認は .md でなく HTML で行う**（`open` でブラウザ表示）．コピペが崩れる場合のみ .md を併用し，その旨を HTML 側に記載する
- 科研費・論文の LaTeX コンパイルは必ず各フォルダの `compile.sh` を使用（latexmk/platex 直接実行禁止）
- 日本語文書の句読点は「，．」に統一

## 運用

- このリポジトリは `~/.claude/skills/` 自体を Git 管理したもの（[sayonari/claude-skills](https://github.com/sayonari/claude-skills)）
- スキルを更新したらコミット・プッシュする（Claude が作業の区切りで自動実施）
- プロジェクト固有の知見は各プロジェクトの `.spec/KNOWLEDGE.md` に，汎用化できた知見のみスキルへ昇格させる
- 論文系3スキル＋make_project の写しは [sayonari/claude-paper-writing-skills](https://github.com/sayonari/claude-paper-writing-skills) にも置いている（このリポジトリが正本）

### exam_grading の単体配布版

`exam_grading` は public リポジトリ [sayonari/exam-grading-skill](https://github.com/sayonari/exam-grading-skill) にも単体で置いている．
実体はこのリポジトリの `exam_grading/` で，**git subtree で切り出して公開側へ push する**（二重管理しない）．

```bash
cd ~/.claude/skills
git add -A && git commit -m "exam_grading: 更新内容"
git push                                                # 本体
git subtree push --prefix=exam_grading exam-grading main  # 単体配布版へ反映
```

（初回のみ `git remote add exam-grading https://github.com/sayonari/exam-grading-skill.git`）
公開版には**学生の個人情報を一切含めない**．サンプルの学籍番号は架空の `B990001` 系を使う．

## ライセンス

MIT（`LICENSE`）．ただし `frontend-design/` は Anthropic 配布物で Apache-2.0（`frontend-design/LICENSE.txt`）．
