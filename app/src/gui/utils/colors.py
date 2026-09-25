"""Theme detection helpers for the application palette."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# --------------------------------------------------------------------------------------------------
# Theme
# --------------------------------------------------------------------------------------------------
def is_dark_mode() -> bool:
    """Return whether the application uses a dark color scheme."""
    return QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark
