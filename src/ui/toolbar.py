"""Toolbar UI component for PureDoc"""

from typing import Callable, TypeAlias, Any, Awaitable
from pathlib import Path

import flet as ft

from src.ui.theme import Theme
from src.utils.file_picker import FilePickerHandler

ToolbarCallback: TypeAlias = Callable[[Any], None | Awaitable[None]]

class Toolbar:
    """Application toolbar with import, template, preview and export buttons"""

    def __init__(
        self,
        page: ft.Page,
        file_picker: FilePickerHandler,
        on_import: ToolbarCallback | None = None,
        on_template: ToolbarCallback | None = None,
        on_preview: ToolbarCallback | None = None,
        on_export: ToolbarCallback | None = None,
        on_settings_change: ToolbarCallback | None = None,
    ):
        """Initialize toolbar

        Args:
            page: Flet Page object
            file_picker: File picker handler instance
            on_import: Callback when import button is clicked
            on_template: Callback when template button is clicked
            on_preview: Callback when preview button is clicked
            on_export: Callback when export button is clicked
            on_settings_change: Callback when any setting checkbox/dropdown changes
        """
        self.page = page
        self.file_picker = file_picker
        self._on_import = on_import
        self._on_template = on_template
        self._on_preview = on_preview
        self._on_export = on_export
        self._on_settings_change = on_settings_change

        # UI Components
        self._checkbox_ignore_bullets = ft.Checkbox(
            label="忽略 Bullet (•)",
            value=True,
            **Theme.get_checkbox_style(),
        )
        self._checkbox_ignore_bullets.on_change = self._handle_setting_change

        self._checkbox_preserve_num = ft.Checkbox(
            label="保留数字列表",
            value=True,
            **Theme.get_checkbox_style(),
        )
        self._checkbox_preserve_num.on_change = self._handle_setting_change

        self._dropdown_style: ft.Dropdown = ft.Dropdown(
            width=180,
            options=[
                ft.dropdown.Option("text", text="转为纯文本 (1.)"),
                ft.dropdown.Option("list", text="Word 自动列表"),
            ],
            value="text",
            on_text_change=self._handle_setting_change,
            **Theme.get_dropdown_style(),
        )


        # Template selector display
        self._template_display = ft.Button(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.DESCRIPTION, size=18, color=Theme.TEXT_SECONDARY),
                    ft.Text("模板: 默认", size=13, color=Theme.TEXT_SECONDARY),
                ],
                spacing=8,
            ),
            style=Theme.get_button_style(is_filled=True),
            on_click=self._on_template,
            tooltip="点击选择 Word 模板",
        )

        self._component = self._build()

    def _build(self) -> ft.Row:
        """Build toolbar component

        Returns:
            Flet Row component
        """
        # Import button
        btn_import = ft.IconButton(
            icon=ft.Icons.FILE_UPLOAD,
            icon_size=22,
            tooltip="导入 Markdown",
            icon_color=Theme.TEXT_PRIMARY,
            style=Theme.get_button_style(),
            on_click=self._on_import,
        )

        # Preview button
        btn_preview = ft.IconButton(
            icon=ft.Icons.VISIBILITY,
            icon_size=22,
            tooltip="Word 原生预览",
            icon_color=Theme.PRIMARY,
            style=Theme.get_button_style(),
            on_click=self._on_preview,
        )

        # Export button
        btn_export = ft.IconButton(
            icon=ft.Icons.SAVE,
            icon_size=22,
            tooltip="导出 Word",
            icon_color=Theme.SUCCESS,
            style=Theme.get_button_style(),
            on_click=self._on_export,
        )

        # Toolbar layout
        return ft.Row(
            controls=[
                # Left section: Import and template
                btn_import,
                ft.Container(width=8),
                self._template_display,
                ft.VerticalDivider(width=1, color=Theme.DIVIDER),
                ft.Container(width=8),
                # Middle section: Settings
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                "选项:",
                                size=13,
                                weight=ft.FontWeight.W_500,
                                color=Theme.TEXT_SECONDARY,
                            ),
                            self._checkbox_ignore_bullets,
                            ft.Container(width=8),
                            self._checkbox_preserve_num,
                            ft.Container(width=8),
                            self._dropdown_style,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.Padding.symmetric(horizontal=8),
                ),
                ft.VerticalDivider(width=1, color=Theme.DIVIDER),
                # Spacer
                ft.Container(expand=True),
                # Right section: Preview and export
                btn_preview,
                ft.Container(width=8),
                btn_export,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _handle_setting_change(self, event) -> None:
        """Handle setting change
        Args:
            event: Flet control event
        """
        if self._on_settings_change:
            self._on_settings_change(None)

    @property
    def ignore_bullets(self) -> bool:
        """Get ignore bullets setting"""
        return self._checkbox_ignore_bullets.value or False

    @property
    def preserve_numbered_lists(self) -> bool:
        """Get preserve numbered lists setting"""
        return self._checkbox_preserve_num.value or False

    @property
    def numbered_list_style(self) -> str:
        """Get numbered list style setting"""
        return self._dropdown_style.value or "转为纯文本 (1.)"

    def set_template_name(self, name: str) -> None:
        """Update template display name

        Args:
            name: Template name to display
        """
        if name:
            display_text = f"模板: {Path(name).name}"
            color = Theme.PRIMARY
        else:
            display_text = "模板: 默认"
            color = Theme.TEXT_SECONDARY

        self._template_display.content = ft.Row(
            [
                ft.Icon(ft.Icons.DESCRIPTION, size=18, color=color),
                ft.Text(display_text, size=13, color=color),
            ],
            spacing=8,
        )
        self._template_display.update()

    @property
    def component(self) -> ft.Row:
        """Get the toolbar component"""
        return self._component
