# Raices

Raices is a desktop application to model, visualize, and export your family tree.

## Run the application

The launchers install `uv`, Python 3.12, and the project dependencies into the repository on first use. Internet access is required for the initial setup.

### Linux

```bash
cd /path/to/Raices
bash Linux_Raices.sh
# Or
./Linux_Raices.sh
```

### macOS

```bash
cd /path/to/Raices
bash Mac_Raices.command
# Or
./Mac_Raices.command
```

If macOS blocks a downloaded launcher, enable it with:

```bash
cd /path/to/Raices
xattr -dr com.apple.quarantine .
chmod +x Mac_Raices.command
```

### Windows

Double-click `Windows_Raices.bat`, or run it from Command Prompt (CMD):

```bat
cd /d "C:\path\to\Raices"
Windows_Raices.bat
```

## Keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl+R` / `Cmd+R` | Restart the application |
| `Ctrl+Q` / `Cmd+Q` | Quit the application |

## Project structure

```
app/
  main.py              Entry point: core services, then the GUI
  pyproject.toml       Project metadata and dependencies
  releases.json        Published release history
  scripts/             Developer command-line utilities
  src/
    assets/            Bundled icons and images
    core/              Application core, free of any Qt dependency
      config.py        Application metadata and release configuration
      logging.py       Console and rotating-file logging
      paths.py         Centralized filesystem paths
      releases.py      Release packaging and GitHub-based updates
      tmp.py           Application-owned temporary files
    gui/
      app.py           Qt bootstrap
      utils/           Theme, resources, release notes, update checks
      widgets/         Reusable widgets
      windows/         Main window and dialogs
```

The `core` package never imports Qt, so it stays usable from scripts. The `gui` package owns every widget and every Qt call.

## Developers

### Developer execution

With `uv` already installed:

```bash
cd /path/to/Raices/app
uv run python main.py
```

### Releases and updates

Updates are distributed through GitHub Releases. To publish a release, run the platform launcher with the `release` argument. The workflow requires Git, push access to the repository, and the GitHub CLI (`gh`).

```bash
./Linux_Raices.sh release
./Mac_Raices.command release
```

On Windows:

```bat
Windows_Raices.bat release
```

In-app updates are disabled automatically when the project is a Git checkout. Use `git pull` instead.
