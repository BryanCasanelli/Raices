"""Bundled GUI asset paths."""

from pathlib import Path

from src.core.paths import SRC_DIR

# --------------------------------------------------------------------------------------------------
# Directories
# --------------------------------------------------------------------------------------------------
ASSETS_DIR: Path = SRC_DIR / "assets"
ICONS_DIR: Path = ASSETS_DIR / "icons"
LOGOS_DIR: Path = ASSETS_DIR / "logos"

# --------------------------------------------------------------------------------------------------
# Files
# --------------------------------------------------------------------------------------------------
ICON_FILE_PATH: Path = ASSETS_DIR / "icon.png"
