"""
Vercel Function entrypoint for YouTube Channel Researcher MCP Server.

Vercel routes /api/mcp to this file.
Streamable HTTP + stateless mode for serverless environment.
"""

import sys
import os

# プロジェクトルートと scripts/ をパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "scripts"))

from mcp_server import mcp

# Vercel Python runtime は 'app' 変数をASGIアプリとして検出する
app = mcp.http_app(
    path="/api/mcp",
    transport="streamable-http",
    stateless_http=True,
)
