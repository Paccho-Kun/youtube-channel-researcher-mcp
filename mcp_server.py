"""
YouTube Channel Researcher MCP Server

YouTube Data API v3 を使ったチャンネル調査ツールをMCPサーバーとして公開する。
Claude.ai / Claude Code / Claude Desktop から利用可能。

起動方法:
  python mcp_server.py

環境変数:
  YOUTUBE_API_KEY — YouTube Data API v3 のAPIキー（必須）
"""

from __future__ import annotations

import sys
import os

# submodule 内の scripts/ をパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "youtube-channel-researcher", "scripts"))

from fastmcp import FastMCP

from channel_researcher import (
    search_channels,
    get_channel_details,
    get_recent_videos,
    get_video_statistics,
    search_videos_by_keyword,
    discover,
    get_steam_app_tags,
    analyze_channel,
)

mcp = FastMCP(
    "youtube-channel-researcher",
    instructions=(
        "YouTube Data API v3 を使ってYouTubeチャンネルを検索・評価するツール群です。"
        "ゲームタイトルのレビューキー送付先候補となるYouTuberを発掘するのに使います。"
    ),
)


@mcp.tool()
def youtube_search_channels(query: str, max_results: int = 10) -> list[dict]:
    """キーワードでYouTubeチャンネルを検索する

    Args:
        query: 検索キーワード（例: "Steam インディーゲーム 紹介"）
        max_results: 最大取得件数（1-50、デフォルト10）

    Returns:
        チャンネル情報のリスト（channel_id, title, description）
    """
    return search_channels(query, max_results=max_results)


@mcp.tool()
def youtube_channel_details(channel_ids: list[str]) -> list[dict]:
    """チャンネルIDから詳細情報を取得する

    登録者数、動画数、総再生数、説明文、カスタムURL等を返す。
    最大50件まで一括取得可能。

    Args:
        channel_ids: チャンネルIDのリスト（例: ["UCxxxxxxxx", "UCyyyyyyyy"]）

    Returns:
        チャンネル詳細情報のリスト
    """
    return get_channel_details(channel_ids)


@mcp.tool()
def youtube_recent_videos(channel_id: str, max_results: int = 10) -> list[dict]:
    """チャンネルの最新動画を取得する

    Args:
        channel_id: チャンネルID（例: "UCxxxxxxxxxxxxxxxxxxxxxxxx"）
        max_results: 最大取得件数（1-50、デフォルト10）

    Returns:
        動画情報のリスト（video_id, title, url, published_at）
    """
    return get_recent_videos(channel_id, max_results=max_results)


@mcp.tool()
def youtube_search_videos(query: str, max_results: int = 15) -> list[dict]:
    """キーワードで動画を検索し、投稿者チャンネル情報も返す

    特定のゲームタイトルを取り上げているYouTuberを見つけるのに有効。

    Args:
        query: 検索キーワード（例: "Gothic 1 Remake 実況"）
        max_results: 最大取得件数（1-50、デフォルト15）

    Returns:
        動画情報のリスト（video_id, title, channel_id, channel_title, url）
    """
    return search_videos_by_keyword(query, max_results=max_results)


@mcp.tool()
def youtube_video_statistics(video_ids: list[str]) -> dict:
    """動画IDから再生回数・高評価数・コメント数を取得する

    最大50件ずつバッチ処理。1ユニット/リクエストでコスパが良い。

    Args:
        video_ids: 動画IDのリスト（例: ["dQw4w9WgXcQ", "abc123"]）

    Returns:
        video_id → {view_count, like_count, comment_count} のマッピング
    """
    return get_video_statistics(video_ids)


@mcp.tool()
def youtube_discover_channels(
    title: str = "",
    related: list[str] | None = None,
    genre: list[str] | None = None,
    steam_app_id: str | None = None,
    max_per_layer: int = 10,
    use_cache: bool = True,
) -> dict:
    """3層検索でゲームタイトルに親和性の高いYouTubeチャンネルを発掘する

    Layer 1（タイトル直接検索）: 既にそのゲームをカバーしている人
    Layer 2（関連タイトル検索）: 同ジャンル・同パブリッシャーのゲーム動画を出している人
    Layer 3（ジャンルキーワード検索）: 広い候補プール

    steam_app_idを指定すると、SteamのユーザータグからLayer 3のキーワードを自動生成する。

    Args:
        title: 対象ゲームタイトル（例: "Gothic 1 Remake"）。steam_app_id指定時は省略可
        related: 関連タイトルのリスト（例: ["Elex 2", "Risen", "Kingdom Come Deliverance"]）
        genre: ジャンルキーワードのリスト（例: ["オープンワールド RPG レビュー"]）。steam_app_id指定時は自動生成
        steam_app_id: Steam AppID（例: "1297900"）。指定するとSteamタグからgenreを自動生成
        max_per_layer: 各検索クエリごとの最大動画数（デフォルト10）
        use_cache: キャッシュを使用するか（デフォルトTrue）

    Returns:
        発掘結果（title, channels, quota_used, steam_info等）
        channelsは登録者数・レイヤー情報・マッチ動画付き
    """
    if not title and not steam_app_id:
        return {"error": "title または steam_app_id のどちらかを指定してください"}

    return discover(
        title=title,
        related=related,
        genre=genre,
        steam_app_id=steam_app_id,
        max_per_layer=max_per_layer,
        use_cache=use_cache,
    )


@mcp.tool()
def steam_app_tags(app_id: str) -> dict:
    """Steam AppIDからゲームのタグ・ジャンル情報を取得する

    ゲームのユーザータグ（RPG、オープンワールド、ダークファンタジー等）、
    ジャンル、開発元、パブリッシャーを返す。
    discoverのsteam_app_idオプションの内部で使用されるが、単体でも利用可能。

    Args:
        app_id: Steam AppID（例: "1297900"）

    Returns:
        ゲーム情報（name, tags, genres, developers, publishers）
    """
    return get_steam_app_tags(app_id)


@mcp.tool()
def youtube_analyze_channel(channel_id: str, max_videos: int = 20, max_comments: int = 50) -> dict:
    """チャンネルを深掘り分析する（PR適性評価）

    直近動画の再生回数・エンゲージメント率、ゲーム系コンテンツ比率、
    投稿頻度、コメント欄の雰囲気、案件受付情報を分析し、
    PR適性スコア（100点満点）を算出する。

    わずか4ユニット/チャンネルで包括的な分析が可能。

    Args:
        channel_id: チャンネルID（例: "UCxxxxxxxxxxxxxxxxxxxxxxxx"）
        max_videos: 分析する直近動画数（デフォルト20）
        max_comments: 取得するコメント数（デフォルト50）

    Returns:
        分析結果（channel, videos, analysis, comments, business_contact, PR適性スコア）
    """
    return analyze_channel(channel_id, max_videos=max_videos, max_comments=max_comments)


if __name__ == "__main__":
    mcp.run()
