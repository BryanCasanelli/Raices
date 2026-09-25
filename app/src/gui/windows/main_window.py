"""Main application window and top-level actions."""

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QCursor, QKeySequence
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from src.core.config import APP_DESCRIPTION, APP_NAME
from src.gui.windows.release_update_window import ReleaseUpdateWindow

# --------------------------------------------------------------------------------------------------
# Window constants
# --------------------------------------------------------------------------------------------------
INITIAL_WINDOW_SIZE = (1_400, 860)

# --------------------------------------------------------------------------------------------------
# Application keymap
# --------------------------------------------------------------------------------------------------
# Ctrl maps to Command and Meta maps to Control on macOS, so both variants are registered
RESTART_SHORTCUTS = ("Ctrl+R", "Meta+R")
QUIT_SHORTCUTS = ("Ctrl+Q", "Meta+Q")

# --------------------------------------------------------------------------------------------------
# Main window
# --------------------------------------------------------------------------------------------------
class MainWindow(QMainWindow):
    """Main application window and top-level actions."""

    def __init__(
        self,
        version: str,
        quit_callback: Callable[[], None],
        restart_callback: Callable[[], None] | None = None,
    ) -> None:
        super().__init__()
        # Application callbacks
        self._quit_callback = quit_callback
        self._restart_callback = restart_callback
        # Auxiliary windows
        self._release_update_window: ReleaseUpdateWindow | None = None
        # Runtime state
        self._version = version
        # Window configuration
        self.setWindowTitle(APP_NAME)
        self.resize(*INITIAL_WINDOW_SIZE)
        # Interface setup
        self._build_content()
        self._build_menu_bar()
        self._build_status_bar()

    # ----------------------------------------------------------------------------------------------
    # Actions
    # ----------------------------------------------------------------------------------------------
    def _build_actions(self) -> None:
        # Lifecycle actions
        self.restart_action = self._create_action("Restart", self._handle_restart_triggered, RESTART_SHORTCUTS)
        self.quit_action = self._create_action("Quit", self._handle_quit_triggered, QUIT_SHORTCUTS)
        # Help actions
        self.check_for_updates_action = self._create_action(
            "Check for Updates...", self._open_release_update_window
        )

    def _create_action(
        self,
        text: str,
        handler: Callable[[], None],
        shortcuts: tuple[str, ...] = (),
    ) -> QAction:
        """Create a menu action and register its application-wide key sequences."""
        action = QAction(text, self)
        self._apply_shortcuts(action, shortcuts)
        action.triggered.connect(handler)
        return action

    def _apply_shortcuts(self, action: QAction, shortcuts: tuple[str, ...]) -> None:
        if not shortcuts:
            return
        action.setShortcuts([QKeySequence(sequence) for sequence in shortcuts])
        action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)

    # ----------------------------------------------------------------------------------------------
    # Interface
    # ----------------------------------------------------------------------------------------------
    def _build_content(self) -> None:
        # Placeholder until the family tree views exist
        placeholder_label = QLabel(APP_DESCRIPTION, self)
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(placeholder_label)

    def _build_menu_bar(self) -> None:
        # Menu actions
        self._build_actions()
        menu_bar = self.menuBar()
        # File menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.restart_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.check_for_updates_action)

    def _build_status_bar(self) -> None:
        self._version_label = QLabel(f"{APP_NAME} {self._version}", self)
        self.statusBar().addPermanentWidget(self._version_label)

    # ----------------------------------------------------------------------------------------------
    # Windows and lifecycle
    # ----------------------------------------------------------------------------------------------
    def center_on_screen(self) -> None:
        """Center the window on the screen containing the mouse cursor."""
        # Target screen
        screen = QApplication.screenAt(QCursor.pos()) or QApplication.primaryScreen()
        if screen is None:
            return
        # Centered position
        window_frame = self.frameGeometry()
        window_frame.moveCenter(screen.availableGeometry().center())
        self.move(window_frame.topLeft())

    def check_for_updates_on_startup(self) -> None:
        """Check for a new release without showing current-version or error dialogs."""
        self._get_release_update_window().check_for_updates_on_startup()

    def shutdown(self) -> None:
        """Stop background work before the process tears down."""

    def closeEvent(self, event: QCloseEvent) -> None:
        """Route window-manager closes through the application quit path."""
        event.ignore()
        self._quit_callback()

    def _handle_restart_triggered(self) -> None:
        if self._restart_callback is None:
            return
        self._restart_callback()

    def _handle_quit_triggered(self) -> None:
        self._quit_callback()

    def _open_release_update_window(self) -> None:
        self._get_release_update_window().check_for_updates()

    def _get_release_update_window(self) -> ReleaseUpdateWindow:
        # Lazy initialization
        if self._release_update_window is None:
            self._release_update_window = ReleaseUpdateWindow(
                restart_callback=self._restart_callback,
                parent=self,
            )
        return self._release_update_window
