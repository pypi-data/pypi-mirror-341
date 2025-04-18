#!/usr/bin/env python3
"""
Main entry point for swipe_verse application.
This is a standalone script that will be installed as the 'swipe-verse' command.
"""
import argparse
import sys

import flet as ft

def main() -> int:
    """Entry point for the Swipe Verse game application."""
    parser = argparse.ArgumentParser(
        description="Swipe Verse - A multiverse card-based decision game"
    )
    parser.add_argument("--config", type=str, help="Path to game configuration file")
    parser.add_argument(
        "--game",
        choices=["kingdom", "business", "science", "space", "tutorial"],
        default="kingdom",
        help="Game scenario to launch with",
    )
    parser.add_argument("--assets", type=str, help="Path to custom assets directory")
    parser.add_argument(
        "--port", type=int, default=0, help="Port number for web view (0 = auto)"
    )

    args = parser.parse_args()

    # Use the Flet UI
    from swipe_verse.ui.app import SwipeVerseApp

    def launch_ui(page: ft.Page) -> None:
        # Initialize settings
        config_path = args.config
        if not config_path and args.game:
            from pathlib import Path

            config_dir = Path(__file__).parent / "scenarios"
            config_path = str(config_dir / f"{args.game}_game.json")

        assets_path = args.assets if args.assets else None

        # Create and add the app to the page
        app = SwipeVerseApp(page=page, config_path=config_path, assets_path=assets_path)
        page.add(app)

    # Launch the app with Flet
    ft.app(target=launch_ui, port=args.port)

    return 0

if __name__ == "__main__":
    sys.exit(main())