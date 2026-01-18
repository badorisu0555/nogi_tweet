<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>乃木坂46 Xトレンド分析アプリ 設計書</title>
    <style>
        :root {
            --primary-color: #7d4b99; /* 乃木坂46のイメージカラー */
            --bg-color: #f8f9fa;
            --text-color: #333;
            --code-bg: #2d2d2d;
            --card-bg: #ffffff;
            --border-color: #dee2e6;
        }

        body {
            font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: var(--card-bg);
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        h1 {
            color: var(--primary-color);
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 10px;
            text-align: center;
        }

        h2 {
            color: var(--primary-color);
            border-left: 5px solid var(--primary-color);
            padding-left: 15px;
            margin-top: 40px;
            background: rgba(125, 75, 153, 0.05);
            padding-top: 5px;
            padding-bottom: 5px;
        }

        h3 {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 5px;
        }

        ul {
            padding-left: 20px;
        }

        li {
            margin-bottom: 8px;
        }

        pre {
            background-color: var(--code-bg);
            color: #ccc;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.4;
        }

        .diagram-container {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 8px;
            border: 1px dashed #999;
            margin: 20px 0;
        }

        .method-card {
            border: 1px solid var(--border-color);
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .tag {
            display: inline-block;
            background: var(--primary-color);
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-bottom: 5px;
        }

        blockquote {
            border-left: 4px solid #ccc;
            margin: 0;
            padding-left: 15px;
            color: #666;
            font-style: italic;
        }

        a {
            color: var(--primary-color);
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 0.8em;
            color: #999;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>乃木坂46 Xトレンド分析アプリ 設計書</h1>

    <h2># 目的</h2>
    <p>乃木坂メンバーやグループの話題は日々入れ替わっているが、それを毎日Xなどで調べてみるのは手間がかかる。</p>
    <p>そこで、X上で乃木坂関連で話題になっている事柄を自動で調査・カテゴライズ・まとめをしてくれると便利だと感じた。そこでX上での乃木坂の話題を整理して、見やすくまとめてくれるアプリケーションの開発を行う。</p>

    <h2># 要求</h2>
    <ul>
        <li>Xから乃木坂に関連するツイートを収集する</li>
        <li>ツイートをカテゴライズする</li>
        <li>カテゴライズしたツイートの概要をまとめる
            <ul>
                <li>タイトル</li>
                <li>ツイート数</li>
                <li>総PV数</li>
                <li>総お気に入り数</li>
                <li>ツイート例3つ</li>
            </ul>
        </li>
        <li>その結果を総PV数が多い順に並び替えて上位5カテゴリを表示</li>
    </ul>

    <h2># 要件</h2>
    <ul>
        <li>ユーザーが集計するツイート数の合計と、カテゴリを設定できる</li>
        <li>Xのツイートを集められるAPIを使って、以下のフィルタリングでツイートを集める
            <ul>
                <li>キーワード：「乃木坂46」（任意で設定できる）</li>
                <li>収集ツイート数：人気順で並び替えをしたうえで、上位任意の数のツイートを収集</li>
            </ul>
        </li>
        <li>レスポンスとして以下を返してもらい、Dataframe型に整理
            <ul>
                <li>text：ツイート本文</li>
            </ul>
        </li>
        <li>上記のツイートについてBedrockを使って、カテゴリ分けをする
            <ul>
                <li>LLMモデル：Claude 3.5</li>
                <li>レスポンスは構造化されたJSON形式で出力させ、プログラム側で処理可能にする。</li>
            </ul>
        </li>
        <li>タイトル、ツイート数、総PV数、総お気に入り数、ツイート事例をまとめて出力させる</li>
    </ul>

    <h2># 設計概要</h2>
    <div class="diagram-container">
<pre>
ユーザー (APIクライアント)
  │
  │ キーワード, 取得件数, (任意)カテゴリ定義
  ▼
[データ収集モジュール] (tweet_api.py)
  │  使用API: X (twitterapi.io)
  │  フィルタ: 人気順 (Top), Query指定
  │
  │ 生ツイートデータ (JSON: id, text, viewCount, likeCount, url)
  ▼
[前処理モジュール] (preprocessing.py)
  │  テキスト正規化: URL除去, 絵文字削除, 改行の平滑化
  │  データ変換: 効率化のため不要な列を削り JSON/DataFrame化
  │
  ▼
[LLM分類・構造化モジュール] (tweet_categorize.py)
  │  使用モデル: AWS Bedrock (Claude 3.5 Sonnet)
  │  プロンプト: 「以下のツイートを分類し、JSON形式で返せ」
  │  ┌──────────────────────────────────────────────────┐
  │  │ 入力: 前処理済みツイートリスト + 分類カテゴリ案    │
  │  │ 出力: カテゴリ付与済みの構造化データ (JSON)       │
  │  └──────────────────────────────────────────────────┘
  ▼
[集計・選定モジュール] (Python / Pandas)
  │  - カテゴリごとの統計計算 (ツイート数, 総PV, 総いいね)
  │  - 各カテゴリの代表ツイート例(3件)の抽出
  │  - ソート処理: 総PV数(viewCount)の降順
  │  - 上位5カテゴリのフィルタリング
  ▼
[出力モジュール] (FastAPI / DataFrame)
  │  JSONResponse または DataFrame 形式での結果返却
  │  ┌──────────────────────────────────────────────┐
  │  │ 1. タイトル (LLMが命名)                       │
  │  │ 2. ツイート数                                 │
  │  │ 3. 総PV数 (ソートキー)                         │
  │  │ 4. 総お気に入り数                             │
  │  │ 5. 代表ツイート3件 (本文・URL等)              │
  └──────────────────────────────────────────────┘
</pre>
    </div>

    <h2># 備考</h2>
    <blockquote>
        1日当たり「乃木坂」のキーワードを含んだツイートは約 5500件
    </blockquote>

    <h2># 自然言語カテゴライズ手法（比較）</h2>
    
    <div class="method-card">
        <span class="tag">手法 ①</span> <strong>sentence-transformers × BERTopic</strong>
        <ul>
            <li>埋め込み：高精度、文脈理解◎</li>
            <li>クラスタリング：HDBSCANを内部利用 + トピックラベル自動生成機能あり</li>
            <li>メリット：一番手軽、実用例も豊富</li>
            <li>👉 <b>デファクト標準、まずはこれ</b></li>
        </ul>
    </div>

    <div class="method-card">
        <span class="tag">手法 ②</span> <strong>sentence-transformers × HDBSCAN</strong>
        <ul>
            <li>メリット：シンプルに設計できる</li>
            <li>デメリット：トピック名は自分で生成（TF-IDFなどと組み合わせ要）</li>
            <li>👉 自分で「カテゴリ名の抽出」をカスタムしたい人向け</li>
        </ul>
    </div>

    <div class="method-card">
        <span class="tag">手法 ⑤</span> <strong>Bedrock Embedding × BERTopic</strong>
        <ul>
            <li>メリット：運用がAWS完結、スケーラブル</li>
            <li>👉 商用アプリとしてAWS環境に載せたい場合に最適</li>
        </ul>
    </div>

    <h2># 参考リンク</h2>
    <ul>
        <li><a href="https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search" target="_blank">TwitterAPI.io 詳細検索リファレンス</a></li>
        <li><a href="https://sbert.net/docs/sentence_transformer/usage/usage.html" target="_blank">sentence-bert リファレンス</a></li>
        <li><a href="https://japan-cyber.com/archives/3044" target="_blank">GETとPOSTの使い分け</a></li>
    </ul>

    <div class="footer">
        &copy; 2024 Nogizaka46 Tweet Analyzer Project
    </div>
</div>

</body>
</html>