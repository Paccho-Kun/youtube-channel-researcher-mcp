# youtube-channel-researcher-mcp

YouTube Channel Researcher の MCPサーバー + Vercelデプロイ。
ビジネスロジック（`channel_researcher.py`）は [youtube-channel-researcher](https://github.com/Paccho-Kun/youtube-channel-researcher) を git submodule として参照する薄いラッパー。

## セットアップ

```bash
# クローン（submodule含む）
gh repo clone Paccho-Kun/youtube-channel-researcher-mcp
cd youtube-channel-researcher-mcp
git submodule update --init

# 依存パッケージ
pip install -r requirements.txt

# APIキー設定
export YOUTUBE_API_KEY='your-api-key'
```

## 使い方

### ローカルMCPサーバー（stdio）

```bash
python mcp_server.py
```

`~/.claude.json` に追加:

```json
"youtube-channel-researcher": {
  "type": "stdio",
  "command": "python3",
  "args": ["/home/yujikato/projects/youtube-channel-researcher-mcp/mcp_server.py"],
  "env": { "YOUTUBE_API_KEY": "your-api-key" }
}
```

### Vercelホスト版（リモートMCPサーバー）

デプロイ済み: `https://youtube-channel-researcher.vercel.app/api/mcp`

Claude.ai Settings > MCP Servers > URLを追加して接続。

#### セルフデプロイ

```bash
vercel link
vercel env add YOUTUBE_API_KEY production
vercel deploy --prod
# 以降は git push で自動デプロイ
```

#### APIキーのローテーション

```bash
vercel env ls
vercel env rm YOUTUBE_API_KEY production
vercel env add YOUTUBE_API_KEY production
vercel deploy --prod
```

## MCPツール一覧（8ツール）

| ツール | 用途 | コスト |
|:--|:--|--:|
| `youtube_discover_channels` | 3層検索でチャンネル発掘 | 700-1,000 |
| `youtube_analyze_channel` | チャンネル深掘り分析（PR適性スコア） | 4 |
| `youtube_search_channels` | キーワードでチャンネル検索 | 100 |
| `youtube_channel_details` | チャンネル詳細取得（最大50件バッチ） | 1 |
| `youtube_recent_videos` | 最新動画一覧 | 100 |
| `youtube_search_videos` | 動画検索→投稿者チャンネル逆引き | 100 |
| `youtube_video_statistics` | 再生回数・高評価数取得（50本バッチ） | 1 |
| `steam_app_tags` | Steam AppIDからタグ情報取得 | 0 |

## アーキテクチャ

```
api/mcp.py                          ← Vercel Function エントリポイント
  └→ mcp_server.py                  ← FastMCP サーバー（8ツール定義）
       └→ youtube-channel-researcher/scripts/channel_researcher.py  ← ビジネスロジック（submodule）
```

薄いラッパー戦略: MCP層はツール定義と引数の橋渡しのみ。ビジネスロジックには一切触れない。

## ファイル構成

```
├── README.md
├── CHANGELOG.md
├── .gitignore
├── .gitmodules
├── mcp_server.py                   # MCPサーバー（ローカルstdio版）
├── api/
│   └── mcp.py                      # Vercel Function（リモートHTTP版）
├── vercel.json                     # Vercel設定
├── requirements.txt                # Python依存パッケージ
└── youtube-channel-researcher/     # git submodule（スキル本体）
    └── scripts/
        └── channel_researcher.py
```

## 関連リポジトリ

| リポジトリ | 役割 |
|:--|:--|
| [youtube-channel-researcher](https://github.com/Paccho-Kun/youtube-channel-researcher) | スキル本体（ビジネスロジック） |
| [youtube-video-triage](https://github.com/Paccho-Kun/youtube-video-triage) | パイプライン下流（動画トリアージ） |
