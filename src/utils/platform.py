"""Platform-specific utilities for PureDoc"""

import os
import sys
import subprocess
import time
from pathlib import Path


class PlatformUtils:
    """Platform-specific utility functions"""

    @staticmethod
    def is_macos() -> bool:
        """Check if running on macOS"""
        return sys.platform == "darwin"

    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows"""
        return sys.platform == "win32"

    @staticmethod
    def is_linux() -> bool:
        """Check if running on Linux"""
        return sys.platform.startswith("linux")

    @staticmethod
    def open_file(file_path: str) -> None:
        """Open a file with the default application

        Args:
            file_path: Path to the file to open
        """
        path = str(file_path)
        if PlatformUtils.is_macos():
            subprocess.call(["open", path])
        elif PlatformUtils.is_windows():
            os.startfile(path)  # type: ignore
        else:  # Linux
            subprocess.call(["xdg-open", path])

    @staticmethod
    def open_quicklook_preview(file_path: str) -> None:
        """Open file in QuickLook (macOS only)

        Args:
            file_path: Path to the file to preview
        """
        if not PlatformUtils.is_macos():
            # Fallback to regular open on other platforms
            PlatformUtils.open_file(file_path)
            return

        temp_docx = os.path.abspath(file_path)

        try:
            # Start qlmanage
            ql_process = subprocess.Popen(
                ["qlmanage", "-p", temp_docx],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )

            # Wait a bit for the window to appear
            time.sleep(0.2)

            # Bring QuickLook window to front using AppleScript
            applescript = '''
            tell application "System Events"
                set frontmost of (every process whose name is "qlmanage") to true
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript])

        except Exception:
            # Fallback to regular open if QuickLook fails
            PlatformUtils.open_file(file_path)

    @staticmethod
    def get_desktop_path() -> Path:
        """Get the user's desktop directory path

        Returns:
            Path to desktop directory
        """
        return Path.home() / "Desktop"

    @staticmethod
    def get_documents_path() -> Path:
        """Get the user's documents directory path

        Returns:
            Path to documents directory
        """
        if PlatformUtils.is_windows():
            # Windows
            try:
                from win32com.shell import shell, shellcon
                return Path(shell.SHGetFolderPath(0, shellcon.CSIDL_MYDOCUMENTS, 0, 0))
            except ImportError:
                # Fallback to default path
                return Path.home() / "Documents"
        elif PlatformUtils.is_macos():
            # macOS
            return Path.home() / "Documents"
        else:
            # Linux
            # Try XDG standard, fallback to ~/Documents
            docs = os.environ.get("XDG_DOCUMENTS_DIR", "")
            if docs:
                return Path(docs)
            return Path.home() / "Documents"

    @staticmethod
    def get_app_support_path(app_name: str = "PureDoc") -> Path:
        """Get the application support directory for storing config/data

        Args:
            app_name: Name of the application

        Returns:
            Path to application support directory
        """
        if PlatformUtils.is_windows():
            # Windows: %APPDATA%
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif PlatformUtils.is_macos():
            # macOS: ~/Library/Application Support
            base = Path.home() / "Library" / "Application Support"
        else:
            # Linux: ~/.local/share or ~/.config
            xdg_data = os.environ.get("XDG_DATA_HOME")
            if xdg_data:
                base = Path(xdg_data)
            else:
                base = Path.home() / ".local" / "share"

        app_path = base / app_name
        app_path.mkdir(parents=True, exist_ok=True)
        return app_path

    @staticmethod
    def get_config_path(app_name: str = "PureDoc") -> Path:
        """Get the config directory path

        Args:
            app_name: Name of the application

        Returns:
            Path to config directory
        """
        if PlatformUtils.is_windows():
            # Windows: same as app data
            return PlatformUtils.get_app_support_path(app_name)
        elif PlatformUtils.is_macos():
            # macOS: ~/Library/Preferences
            base = Path.home() / "Library" / "Preferences"
        else:
            # Linux: ~/.config
            base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

        config_path = base / app_name
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path
