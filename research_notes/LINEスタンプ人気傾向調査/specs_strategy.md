# 個人クリエイターがLINEスタンプを出す場合の制作仕様・収益構造・売れるための戦略

調査上の制約: creator.line.me を含む多くのドメインへの WebFetch が DNS エラーで失敗した。以下は WebSearch の要約結果ベースで、公式ガイドライン本文は直接確認できていない。数値は「二次情報」「年」を併記。制作前に公式で再確認が必要。

## 1. 現行スタンプ仕様・枚数・画像サイズ・価格・審査期間・レベニューシェア・2025〜2026の変更点

### Takeaway
静止画スタンプは8/16/24/32/40個から選べ、画像は最大370x320px・PNG透過・メイン240x240・タブ96x74(二次情報)。販売価格はクリエイターが選ぶ方式から変わり、2026年7月1日に静止画クリエイターズスタンプの最低価格が120円→190円に改定された。取り分は約35%(2015年以降の制度、現行値は未確認)。

### Cited Findings
- 静止画の個数は2016年10月6日から、従来の40個固定に加え8/16/24/32/40個から選択可能になった — [ASCII 2016](https://weekly.ascii.jp/elem/000/001/252/1252008/)
- 画像規格: スタンプ画像は横最大370px x 縦最大320px、メイン画像240x240px(1個)、トークルームタブ画像96x74px(1個) — [CrowdWorks解説](https://crowdworks.jp/times/know-how/5213/)、[AppBank](https://www.appbank.net/?p=1235796)(いずれも二次情報、年は不明確)
- 形式はPNG(背景透過)、画像のpx数は偶数、1個1MB以下との要約あり — [Libecity記事](https://library.libecity.com/articles/01KQH5RBH1H00HP9AVYZHX2AWR)(二次情報)
- 審査はイラストの上手さではなくガイドライン適合性を見る — [CrowdWorks](https://crowdworks.jp/times/know-how/5213/)
- 審査期間: 2015年時点で、審査体制増員後に平均5日程度(リジェクト期間除く)との報告 — [ASCII/Impress系記事(2015)](https://ascii.jp/elem/000/001/252/1252008/2/)。古い数値で現行は未確認
- 審査通過率: 2014年時点で申請作品の約8分の1しか公開されなかったとの報道 — [ITmedia 2014](https://www.itmedia.co.jp/news/article/1406/11/1140611018/)(古い。現行は低下していると思われるが数値は未確認)
- 分配率: 2015年2月1日申請分以降、ストア手数料(App Store/Google Play等30%)を除いた額の50%、すなわち売上総額の35%がクリエイター取り分 — [gori.me 2015](https://gori.me/line/line-news/67901)。2026年の解説でも「約35%、250円なら1個約87円」とされる(二次情報、後述)
- 価格改定(重要): 2026年7月1日(水)10:00から、LINEクリエイターズスタンプ(静止画のみ)がLINE STORE価格で120円〜→190円〜、アプリ内は50コイン〜→70コイン〜。アニメ・メッセージ等の静止画以外のスタンプ、絵文字(アニメ)、着せかえは対象外 — [Jetstream 2026-06-01](https://jetstream.blog/2026/06/01/line-stickers-emoji-price-increase-jul-1-2026/)、[Pricey](https://pricey.jp/web/articles/4768)、[個人X投稿](https://x.com/ku3uyo/status/2071520540448420149)
- 2025年5月29日、クリエイターズ絵文字(静止画)の最低価格が120円→170円に値上げ(スタンプは対象外)。2026年改定で絵文字も170円→190円との記述あり — [Jetstream/Pricey検索要約](https://pricey.jp/web/articles/4768)
- 価格の歴史: 2015年時点は120/240/360/480/600円等から選択可能、2015年12月から価格変更機能の導入が報じられた — [Appllio 2015](https://appllio.com/20151202-7797-line-creators-market-animation-stamp-kisekae)
- アニメスタンプ(個人ブログ要約): 8個または16個、APNG、フレーム5〜20枚推奨、キャンバス320x270px — [Classmethod](https://dev.classmethod.jp/articles/line-animated_sticker/)(年・公式整合は未確認、要確認)
- 生成AI: 公式の2025年ルール変更は確認できず。二次情報では、AI利用自体は禁止されず第三者権利侵害の有無が審査対象、AIツールの商用利用規約確認が必要 — [aipicks](https://aipicks.jp/mag/ai-line-stamp-creation-rules-2026)(非公式)
- 税務: 分配金は源泉徴収の対象になる前提で、確定申告は入金年ではなく売上発生年基準との説明 — [税理士ドットコム](https://www.zeiri4.com/c_5/q_147534/)。源泉税率は情報が食い違い未確定。最低支払額は約1,000円とのブログ情報(二次情報)

### Inferences
- 2026年7月以降は静止画の価格下限が上がるため、同じ販売数でも取り分(価格x35%想定)は増える可能性があるが、購入率が下がる懸念もある(推測。実績データなし)。
- 190円x35%なら1個約66円(算術上の推定。現行の取り分率が35%のままという前提)。
- 静止画以外(アニメ等)は据え置きで、価格差の縮小により静止画の優位性が下がる可能性(推測)。

### Gaps
- 公式ガイドライン(creator.line.meの現行仕様、メッセージスタンプ/ポップアップ/ビッグスタンプ/アニメの現行値)を直接取得できなかった。
- 現行の審査期間・審査通過率の公式値。
- 現行の源泉徴収税率と最低支払額の公式値、2026年改定後の分配率変更の有無。

## 2. 個人クリエイターの売上実態

### Takeaway
公式が出す数字は上位層(上位10名平均など)のみで、平均・中央値の公式データは見つからなかった。副業系ブログは「大多数は月数百円〜数千円、上位約10%に集中」と述べるが根拠は示されておらず推定扱い。

### Cited Findings
- 2014年6月、開始1か月で上位10名の平均売上470万円 — [Appllio 2014](https://appllio.com/20140611-5341-line-creators-market-stamp-revenue)(黎明期で現在の参考にならない)
- 2021年5月: 登録クリエイター390万人超、累計販売総額1,000億円超、売上上位10名平均11億8,262万円、1億円超クリエイター154名 — [LINEヤフー 2021プレス](https://www.lycorp.co.jp/news/archive/L/ja/ja20210506_A.pdf)(検索要約経由)。全体の中央値・分布は未公表
- 2024年11月の例: 小学生の作品が7人に購入、手数料後の手元収益は265円 — [Libecity記事要約](https://library.libecity.com/articles/01JDCD9A44B7VZBFX917RC6FWQ)(個人例、単発)
- 2026年版の副業ブログ: 「平均的なクリエイターの月収は数百円〜数千円」「上位10%に集中」「戦略次第で月3〜10万円」。また筆者は28セット販売で月2〜6万円と記述 — [atsoho.com](https://atsoho.com/blog/line-stamp-income-reality)(根拠不明の商業ブログ、割り引いて扱う)
- 参入者増により1スタンプあたりの平均収益は2014〜2016年より低下したとの見方 — [atsoho.com](https://atsoho.com/blog/sticker-line-fukugyo)(推測的記述)

### Inferences
- 分布は極端なべき乗型で、新規個人の期待値は低い(上位層公式値と個人例の乖離からの推測)。
- 一次情報としての「平均/中央値」は存在せず、レポートでは「公開統計なし」と明記すべき。

### Gaps
- note等の個人の詳細な収益公開記事(セット数x売上x期間)は検索で十分に特定できず、2024〜2026年の信頼できる複数事例は未収集。
- 全体に対する収益化できている割合の一次データ。

## 3. 売れるための戦略

### Takeaway
各ブログが一致して挙げるのは、(1) SNS等での自力告知、(2) 検索に載るタイトル・説明文のキーワード、(3) ニッチな利用シーン、(4) シリーズ化・複数セット、(5) 季節ネタ。いずれも定量的な効果検証は見当たらない。

### Cited Findings
- アプリ内検索だけでは新作は発見されにくく、「知られていない」ことが主因との指摘 — [Libecity](https://library.libecity.com/articles/01KQHKZMPQAJ0ARK2QF875TK6J)(ブログ意見)
- 36セット作ってもSNS告知ゼロで売れなかったとの体験談。告知投稿を自動化して継続 — [体験記(検索要約)](https://atsoho.com/blog/sticker-line-fukugyo)
- スタンプショップの探索導線はキーワード、カテゴリー、イベント、新着、ランキング — [find-model insta-lab](https://find-model.jp/insta-lab/line-stamp/)
- 説明文・タグに「猫 かわいい ゆるい 日常 あいさつ」のように検索語を入れる — [Libecity](https://library.libecity.com/articles/01KQHKZMPQAJ0ARK2QF875TK6J)
- ニッチ化: 「かわいい猫」「ゆるい犬」は飽和、テレワーク・推し活・育児あるある等を狙う — [find-model](https://find-model.jp/insta-lab/line-stamp/)(2026年解説)
- シリーズ化で既存ファンが購入しやすい、年始あいさつ等の季節需要 — [Libecity](https://library.libecity.com/articles/01KQHKZMPQAJ0ARK2QF875TK6J)
- 当初価格は最低価格設定が多い(120円)。購入ハードルを下げる戦略とされる — 同上
- 発売直後のランキング入り戦略(初動集中)、コラボ、LINE VOOM/LINEギフト/LINE公式アカウント導線に関する信頼できる具体情報は今回の検索では得られなかった。

### Inferences
- ランキングはアプリ内の主要発見導線であるため、発売日に知人・フォロワーの購入を集中させるのが定石とされるが、本調査ではその裏付けは未取得(推測)。
- 値上げ前後(2026年7月)は「価格改定前にお迎えを」といった告知がクリエイター側でも使われている(例: [X投稿](https://x.com/ku3uyo/status/2071520540448420149))。

### Gaps
- 初動ランキングのアルゴリズム・必要販売数、タイトル/タグSEOの公式仕様。
- コラボ事例、季節ネタの売上効果の定量データ。

## 4. 失敗パターン(売れない原因)

### Takeaway
多数のブログが指摘するのは、告知不足、飽和ジャンル、ニッチ不在、審査落ち(著作権・類似)。

### Cited Findings
- 告知ゼロ・知られていない — [Libecity](https://library.libecity.com/articles/01KQHKZMPQAJ0ARK2QF875TK6J)
- 飽和ジャンル(汎用の猫・犬)で差別化なし、新規の自然発見確率は低下 — [find-model](https://find-model.jp/insta-lab/line-stamp/)
- 審査落ち例: 有名キャラ類似(著作権)、ロゴ写り込み、AIツールの商用不可 — [aipicks](https://aipicks.jp/mag/ai-line-stamp-creation-rules-2026)、[CrowdWorks](https://crowdworks.jp/times/know-how/10546/)
- 二次創作は不可 — [ITmedia 2014](https://www.itmedia.co.jp/news/article/1404/17/1140417122/)

### Inferences
- 「使いどころのない汎用絵柄」「会話で使える文言の欠如」が売れない構造要因と思われるが、直接の検証データはなし(推測)。

### Gaps
- 失敗の頻度順などの統計。

## 5. LINE VOOM/LINEギフト/LINE公式アカウント等の販促導線

### Takeaway
今回の検索では、これらを個人スタンプ販促に使う公式手段や事例は確認できなかった。

### Cited Findings
- 該当する信頼できる出典は取得できなかった。

### Inferences
- LINEギフト(スタンプのプレゼント購入)は購入導線として機能しうるが、販促の効果や仕様は未確認(推測)。

### Gaps
- LINE VOOM・LINEギフト・公式アカウント経由の導線の公式仕様と事例。2026年のLINE Creators Magazine等の公式記事を要確認。
