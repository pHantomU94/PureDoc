"""File picker handlers for PureDoc"""

import flet as ft


class FilePickerHandler:
    """Handles file selection dialogs"""

    def __init__(self, page: ft.Page):
        """Initialize file picker handler

        Args:
            page: Flet Page object
        """
        self.page = page

        # File picker for opening files
        self.file_picker = ft.FilePicker()

        # Save file picker
        self.save_picker = ft.FilePicker()
