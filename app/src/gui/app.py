"""Qt application bootstrap and GUI startup sequence."""

import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.core.config import APP_NAME, ORGANIZATION_NAME, RESTART_EXIT_CODE
from src.core.logging import logger
from src.core.paths import PYPROJECT_FILE_PATH
from src.core.releases import get_pyproject_version
from src.gui.utils.resources import ICON_FILE_PATH
from src.gui.windows.main_window import MainWindow

# --------------------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------------------
def run_gui() -> int:
    """Create the Qt application, wire the main window and its services, and run the event loop."""
    # Qt application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)
    _configure_window_icon(app)
    app.aboutToQuit.connect(_about_to_quit)
    # Application version
    version = get_pyproject_version(PYPROJECT_FILE_PATH)
    # Main window
    window = MainWindow(
        version=version,
        restart_callback=lambda: _restart(app),
        quit_callback=lambda: _quit(app),
    )
    # Startup tasks
    app.aboutToQuit.connect(window.shutdown)
    window.showMaximized()
    QTimer.singleShot(0, window.check_for_updates_on_startup)
    # Event loop
    return app.exec()

# --------------------------------------------------------------------------------------------------
# Appearance
# --------------------------------------------------------------------------------------------------
def _configure_window_icon(app: QApplication) -> None:
    """Apply the bundled application icon when it is available."""
    if not ICON_FILE_PATH.is_file():
        logger.warning(f"Application icon not found: {ICON_FILE_PATH}")
        return
    app.setWindowIcon(QIcon(str(ICON_FILE_PATH)))

# --------------------------------------------------------------------------------------------------
# Lifecycle
# --------------------------------------------------------------------------------------------------
def _restart(app: QApplication) -> None:
    """Request a launcher-level application restart."""
    logger.info("Restart requested")
    app.exit(RESTART_EXIT_CODE)
# --------------------------------------------------------------------------------------------------
def _quit(app: QApplication) -> None:
    """Quit the current application process."""
    logger.info("Quit requested")
    app.quit()
# --------------------------------------------------------------------------------------------------
def _about_to_quit() -> None:
    """Record application shutdown."""
    logger.info(f"Closing {APP_NAME}...")
