# 音声分野コーパス実測スタイルデータ（paper_writing 参照ファイル）

- 出典: ICASSP 2001–2026 全年度（45,571本・114.0M語）＋ Interspeech 2007–2025 全年度（17,406本・52.9M語）、計62,977本・166.9M語の実測
- ベースライン（「人間の適正頻度」）= ChatGPT登場以前の 2015–2022 コア（19,925本・56.8M語）
- 分析実施: 2026-07-02、生成スクリプト・全データは
  `/Volumes/ROBOCO_SAN/AItask/音声系英語論文執筆スキル作成/`（scripts/ と analysis/）にあり再生成可能
- 単位表記: /M = per million words。1論文 ≒ 2,700語（4ページ）なので、10/M ≒ 「37本に1回」

## 1. 定量スタイル基準（人間の相場）

| 指標 | 人間の相場（26年間安定） | AI初稿の傾向 | ルール |
|---|---|---|---|
| 文長 | 平均24.5語・中央値21語・90%タイル42語 | 平均23〜29語（長め・均質） | 中央値21語を意識。40語超の文を連発しない |
| セミコロン | 0.03〜0.05回/文（約30文に1回） | 多用しがち（旧世代） | 文接続はピリオドで切る |
| em-dash（—） | 0.4回/論文＝137/M | 挿入句を—で包む癖（現世代も残存） | 使わない（§8.6.5参照）。カンマ・括弧へ |
| 箇条書き（•等） | 0.9回/論文未満 | 本文を箇条書きで進めがち | 本文は散文で書く |
| 修辞疑問文（?） | 0.23/M（≒稀） | Introで多用する例あり | 原則使わない |
| 段落 | 長さ不均一（100〜250語が混在） | 約100〜130語×4〜5個の均質段落 | 内容駆動で長短を混ぜる |
| 三点列挙 | 控えめ | (i)(ii)(iii)・First/Second/Thirdを多用 | パラレリズムの整いすぎに注意 |

LLM混入の実測: em-dashは2001–2024年の24年間92〜149/Mで安定→2025年に**ICASSP 514/M・Interspeech 489/M**へ爆発（人間論文へのAI混入）。この数字が「—を使うとAI臭い」の根拠。

## 2. 語彙: BAN（人間はそもそも使わない。baseline < 3/M）

使ったら即AI臭。すべて2024年以降に急増した実績あり（括弧内はbaseline→2024-26実測/M）:

- **underscore / underscores / underscoring**（0.7→19〜30、×26〜82）
- **pivotal**（1.6→24）, **nuanced**（1.2→19）, **intricate / intricacies**（2.7→36）
- **delve / delves / delving**（0.7→6）, **meticulous / meticulously**（0.3→9）
- **showcase系 showcasing/showcases**（1.2→18）, **seamless**（2.4→14）
- **realm**（1.7→9）, **harness系**（1.8→8）, **garnered**（0.7→10）
- **bolster系, foster系(fosters/fostering), empower系, elucidate系**（いずれも≦1→2〜4）
- **multifaceted, groundbreaking, cutting-edge, tapestry**（≒0）

BANフレーズ: has garnered / in the realm of / paving the way / plays a crucial role /
plays a vital role / sheds light on / a plethora of / myriad / rapidly evolving / ever-evolving

## 3. 語彙: LIMIT（人間も使うが適正頻度あり。超えるとAI臭）

| 語 | 人間の適正頻度 | LLM後の異常値 | 目安 |
|---|---|---|---|
| notably | 24/M | 149/M | 1論文0〜1回 |
| crucial | 63/M | 205/M | 1論文0〜1回 |
| comprehensively | 4.5/M | 31/M | ほぼ使わない |
| seamlessly | 3.4/M | 22/M | ほぼ使わない |
| innovative | 7/M | 41/M | 自称に使わない |
| holistic | 8/M | 26/M | ほぼ使わない |
| crucially | 3.7/M | 14/M | ほぼ使わない |

WATCH（増加傾向・多用注意）: additionally（116/M→309/M）, paradigm, essential, vital, landscape, showcase

問題なし（頻度を守れば普通の語）: significantly(337/M), overall, moreover(266/M), furthermore(253/M), consequently, state-of-the-art(360〜458/M。むしろ分野常用語)

## 4. 人間マーカー表現【積極的に使う】

実論文で常用されるが**AIが自発的にほぼ使わない**表現（AI生成実験で出現ゼロ、かつLLM混入後のコーパスで減少中）。適度に使うと人間らしくなる:

- **Note that ...**（注意喚起の第一選択）
- **It can be seen that ...** / **We can see that ...**（図表・結果への言及）
- **in order to ...**（442/M。AIは省略しがち）
- **On the other hand, ...**（154/M。LLM後×0.3に減少＝人間マーカー）
- **In other words, ...**（62/M。LLM後×0.2に減少）
- **It should be noted that ...**（20/M。控えめに）
- **At the same time, ...** / **In addition to ...**（additionally 単語より句形が人間的）

## 5. 分野の定型表現（使ってよい・使うべき）

- In this paper, we propose ...（149/M・最頻の提案導入。1論文1回）
- In this work/study, we ... / In this section, we ...
- The rest of the paper is organized as follows.（Introduction末尾の定型）
- To the best of our knowledge, ...（新規性主張。49/M）
- as shown in Fig. N（ICASSP系は "Fig."、ISCA系は "Figure" 優勢）/ are shown in Table N
- Experimental results show that ... / The results show that ...
- the proposed method / outperforms / achieves ... improvement / baseline(s)
- can be written/expressed as（数式導入）/ where X is the ...（変数説明）/ is defined as
- This work was supported (in part) by ...（謝辞定型）
- 初出略語はフルスペル＋略語: automatic speech recognition (ASR), word error rate (WER)

## 6. 会議別の章立て・作法

| | ICASSP（IEEE系） | Interspeech（ISCA系） |
|---|---|---|
| 見出し体裁 | `1. INTRODUCTION`（全大文字） | `1. Introduction`（Title Case） |
| 典型構成 | INTRO →(RELATED WORK)→ PROPOSED METHOD → EXPERIMENTS → CONCLUSION | Intro → Method(s) → Results → Discussion → Conclusions |
| 結論見出し | **CONCLUSION** 優勢（2.2倍） | **CONCLUSIONS** 優勢（1.4倍） |
| Discussion節 | 稀 | 頻出（実験系文化） |
| 謝辞 | 番号なしが多い | 番号付きセクションが多い |
| 図参照 | Fig. N | Figure N |

## 6.5 推敲時のgrepセルフチェック【活用形もれ対策】

BAN語・BANフレーズは活用形・挿入語ですり抜ける（実例: "shed **some** light on"）。完成原稿に対して語幹ベースで確認する:

```bash
grep -inE 'underscor|pivotal|nuanc|intricac|delv(e|ing)|meticulous|showcas|seamless|\brealm|harness|garner|bolster|multifacet|groundbreak|cutting-edge|shed.{0,10}light|pav.{0,8}way|crucial role|vital role|plethora|myriad|garner' sections/*.tex
grep -cE '—|---' sections/*.tex          # em-dash はゼロであること
grep -inE '\?\s' sections/*.tex          # 修辞疑問の確認
```

## 7. 運用メモ

- このデータの主根拠は2015–2022コーパス（LLM混入なし）。2023年以降の「人間論文」は既にAI混入があるため頻度基準に使わない
- AI典型語の流行は動く（例: delve/realm/pivotalは2024年ピーク→有名になりすぎて2025-26年は減少、代わりにunderscoring/notably/comprehensivelyが上昇中）。リストは定期的に再生成すること（scripts/build_avoid_list.py）
- 世間の「AI語リスト」を鵜呑みにしない: sheds light on / a plethora of / myriad はLLM後も増えていない（単に誰も使わない語）
