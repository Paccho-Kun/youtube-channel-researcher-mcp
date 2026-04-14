# Changelog

## [1.0.0] - 2026-04-14

### 追加
- youtube-channel-researcher リポジトリから MCP/Vercel 関連ファイルを分離して独立リポジトリ化
- `mcp_server.py` — FastMCP サーバー（8ツール）
- `api/mcp.py` — Vercel Function エントリポイント
- `vercel.json` — Vercel設定
- youtube-channel-researcher を git submodule として参照

### 背景
スキルリポジトリの標準パターン準拠のため、ビジネスロジック（スキル）と
MCPアクセス層（サーバー + デプロイ）を分離。薄いラッパー戦略に基づき、
MCP層はツール定義と引数の橋渡しのみを担当する。
