"""Main page UI component for PureDoc"""

from typing import Callable
from pathlib import Path

import flet as ft

from src.ui.theme import Theme
from src.ui.toolbar import Toolbar
from src.utils.file_picker import FilePickerHandler
from src.utils import get_download_path, get_resource_path
from src.core.converter import Converter
from src.utils.platform import PlatformUtils

import os

class MainPage:
    """Main application page"""

    def __init__(self, page: ft.Page):
        """Initialize main page

        Args:
            page: Flet Page object
        """
        self.page = page
        
        # # Initialize converter
        self.converter = Converter(
            lua_filter_path=get_resource_path('scripts/bullet_process.lua'),
            template_path=get_resource_path('template/template.docx'),
            ignore_bullets=True,
        )

        # Temporary file for preview
        self._temp_preview_file = None

        # File picker handler
        self.file_picker = FilePickerHandler(page)

        # Setup file picker result handlers
        #self.file_picker.file_picker.on_result = self._on_file_picker_result
        #self.file_picker.save_picker.on_result = self._on_save_picker_result

        # Add file pickers to page overlay
        # self.page.overlay.append(self.file_picker.file_picker)
        # self.page.overlay.append(self.file_picker.save_picker)

        # Build UI components
        self._build_ui()

    def _build_ui(self) -> None:
        """Build all UI components"""
        # Toolbar
        self.toolbar = Toolbar(
            page=self.page,
            file_picker=self.file_picker,
            on_import=self._handle_import,
            on_template=self._handle_template_select,
            on_preview=self._handle_preview,
            on_export=self._handle_export,
            on_settings_change=self._handle_settings_change,
        )

        # Input text field
        self.txt_input = ft.TextField(
            multiline=True,
            expand=True,
            border=ft.InputBorder.NONE,
            hint_text="粘贴 Markdown 内容到这里，或点击导入按钮导入文件...",
            **Theme.get_text_field_style(),
            on_change=self._handle_input_change,
        )

        # Markdown preview
        self.markdown_view = ft.Markdown(
            value="预览区域",
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            on_tap_link=self._handle_link_tap,
        )

        self.preview_container = ft.Container(
            content=ft.Column(
                [self.markdown_view],
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            **Theme.get_container_style(has_border=True),
            padding=ft.Padding.all(24),
            expand=True,
        )

        # Main layout
        self.split_view = ft.Row(
            controls=[
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "原始内容",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=Theme.TEXT_SECONDARY,
                            ),
                            padding=ft.Padding.only(bottom=12),
                        ),
                        ft.Container(
                            content=self.txt_input,
                            **Theme.get_container_style(has_border=True),
                            padding=ft.Padding.all(8),
                            expand=True,
                        ),
                    ],
                    expand=1,
                ),
                ft.VerticalDivider(width=1, color=Theme.DIVIDER),
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "转换后预览",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=Theme.TEXT_SECONDARY,
                            ),
                            padding=ft.Padding.only(bottom=12),
                        ),
                        self.preview_container,
                    ],
                    expand=1,
                ),
            ],
            expand=True,
        )

        # Add all components to page
        self.page.add(self.toolbar.component, ft.Divider(height=1, color=Theme.DIVIDER), self.split_view)
        # Load initial settings
        self._load_settings()

    def _load_settings(self) -> None:
        """Load settings from config into UI"""
        self._checkbox_ignore_bullets = self.toolbar._checkbox_ignore_bullets
        self._checkbox_preserve_num = self.toolbar._checkbox_preserve_num
        self._dropdown_style = self.toolbar._dropdown_style

        self._checkbox_ignore_bullets.value = True
        self._checkbox_preserve_num.value = True
        self._dropdown_style.value = "text"

        # Update converter
        self.converter.set_ignore_bullets(self._checkbox_ignore_bullets.value)

        # Update template display
        template_path = get_resource_path('template/template.docx')
        if template_path and Path(template_path).exists():
            self.toolbar.set_template_name(template_path)
        else:
            self.toolbar.set_template_name("")

    def _handle_input_change(self, event) -> None:
        """Handle input text change

        Args:
            event: Flet control event
        """
        raw_content = self.txt_input.value
        if not raw_content:
            self.markdown_view.value = ""
        else:
            try:
                processed_md = self.converter.convert_text(
                    raw_content,
                    output_format='markdown',
                    is_export=False,
                )
                self.markdown_view.value = processed_md
            except Exception as e:
                self.markdown_view.value = f"**预览错误**: {e}"
        self.markdown_view.update()

    def _handle_settings_change(self, e: ft.ControlEvent | None = None) -> None:
        """Handle settings change"""
        # Update converter
        self.converter.set_ignore_bullets(self.toolbar.ignore_bullets)

        # Refresh preview
        self._handle_input_change(None)

    async def _handle_import(self, event) -> None:
        """Handle import button click

        Args:
            event: Flet control event
        """
        export_dir = get_download_path()
        files = await self.file_picker.file_picker.pick_files(
            allowed_extensions=["md", "markdown"],
            dialog_title="选择 Markdown 文件",
            initial_directory=export_dir,
        )
        self._on_file_picker_result(files)
        # refresh preview
        self._handle_input_change(None)

    def _on_file_picker_result(self, files: list[ft.FilePickerFile]) -> None:
        """Handle file picker result

        Args:
            event: File picker result event
        """
        if not files:
            return 
        
        file_path = files[0].path
        if file_path:
            # Handle based on file extension
            if file_path.lower().endswith(('.md', '.markdown')):
                self._on_file_imported(file_path)
            elif file_path.lower().endswith('.docx'):
                self._on_template_selected(file_path)            

    def _on_file_imported(self, file_path: str) -> None:
        """Handle imported markdown file

        Args:
            file_path: Path to imported file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.txt_input.value = content
            self.txt_input.update()
            self._show_message(f"已导入: {Path(file_path).name}")
        except Exception as e:
            self._show_message(f"导入失败: {e}", is_error=True)

    async def _handle_template_select(self, event) -> None:
        """Handle template button click

        Args:
            event: Flet control event
        """
        files = await self.file_picker.file_picker.pick_files(
            allowed_extensions=["docx"],
            dialog_title="选择 Word 模板文件",
        )
        self._on_file_picker_result(files)

    def _on_template_selected(self, file_path: str) -> None:
        """Handle selected template file

        Args:
            file_path: Path to selected template
        """
        try:
            self.converter.set_template_path(file_path)
            self.toolbar.set_template_name(file_path)
            self._show_message(f"模板已设置: {Path(file_path).name}")
        except Exception as e:
            self._show_message(f"设置模板失败: {e}", is_error=True)

    def _handle_preview(self, event) -> None:
        """Handle preview button click

        Args:
            event: Flet control event
        """
        if not self.txt_input.value:
            self._show_message("内容为空！", is_error=True)
            return

        import tempfile
        import os

        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
                self._temp_preview_file = f.name

            # Convert to temporary Word file
            self.converter.convert_to_word(
                self.txt_input.value,
                self._temp_preview_file,
            )

            # Open in QuickLook (macOS) or default viewer
            PlatformUtils.open_quicklook_preview(self._temp_preview_file)

            self._show_message("已打开原生预览")

        except Exception as e:
            self._show_message(f"预览失败: {e}", is_error=True)

    async def _handle_export(self, event) -> None:
        """Handle export button click

        Args:
            event: Flet control event
        """
        if not self.txt_input.value:
            self._show_message("内容为空！", is_error=True)
            return
        # Get save path
        save_path = await ft.FilePicker().save_file(
            allowed_extensions=["docx"], 
            file_name="Document.docx"
        )
        if save_path:
            output_path = Path(save_path)

        else:
            self._show_message(f"导出失败: 未选择保存路径", is_error=True)
            return
        try:
            self.converter.convert_to_word(
                self.txt_input.value,
                str(output_path),
            )

            # Open exported file
            PlatformUtils.open_file(str(output_path))

            self._show_message(f"成功导出: {output_path.name}")

        except Exception as e:
            self._show_message(f"导出失败: {e}", is_error=True)

    async def _handle_link_tap(self, event) -> None:
        """Handle link tap in markdown preview

        Args:
            event: Flet control event
        """
        if event.data:
            await self.page.launch_url(str(event.data))

    def _show_message(self, message: str, is_error: bool = False) -> None:
        """Show a snackbar message

        Args:
            message: Message to display
            is_error: Whether this is an error message
        """
        color = Theme.ERROR if is_error else Theme.SUCCESS
        icon_name = ft.Icons.ERROR_OUTLINE if is_error else ft.Icons.CHECK_CIRCLE

        snack = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(icon_name, color=color, size=20),
                    ft.Container(width=8),
                    ft.Text(message, size=14, color=color),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=Theme.SURFACE,
            duration=3000,
            open=True,
        )

        try:
            self.page.overlay.append(snack)
            self.page.update()
        except Exception:
            print(f">> {message}")

    def cleanup(self) -> None:
        """Clean up resources"""

        # Remove temp preview file
        if self._temp_preview_file and Path(self._temp_preview_file).exists():
            try:
                os.unlink(self._temp_preview_file)
            except Exception:
                pass
