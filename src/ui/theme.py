"""UI Theme configuration - Typora-inspired color scheme"""

import flet as ft


class Theme:
    """Typora-inspired UI theme colors and styles"""

    # Color palette
    PRIMARY = "#4A90E2"          # Main blue for active states
    PRIMARY_LIGHT = "#7BB3E9"     # Lighter blue for hover
    BACKGROUND = "#FAFAFA"       # Main background color
    SURFACE = "#FFFFFF"          # Card/container background
    BORDER = "#E8E8E8"           # Border color
    BORDER_LIGHT = "#F0F0F0"     # Lighter border
    DIVIDER = "#EEEEEE"          # Divider line

    TEXT_PRIMARY = "#333333"     # Main text color
    TEXT_SECONDARY = "#666666"   # Secondary text color
    TEXT_DISABLED = "#999999"    # Disabled text
    TEXT_HINT = "#BBBBBB"        # Hint text

    SUCCESS = "#52C41A"          # Success color
    ERROR = "#FF4D4F"            # Error color
    WARNING = "#FAAD14"         # Warning color

    # Common styles
    @staticmethod
    def get_button_style(
        is_filled: bool = False,
        primary: bool = False
    ) -> ft.ButtonStyle:
        """Get button style

        Args:
            is_filled: Whether button has filled background
            primary: Whether button is primary action

        Returns:
            ButtonStyle object
        """
        if primary:
            return ft.ButtonStyle(
                bgcolor=Theme.PRIMARY,
                color=Theme.SURFACE,
                overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                shape=ft.RoundedRectangleBorder(radius=6),
            )
        elif is_filled:
            return ft.ButtonStyle(
                bgcolor=Theme.SURFACE,
                color=Theme.TEXT_PRIMARY,
                overlay_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                side=ft.BorderSide(color=Theme.BORDER, width=1),
                shape=ft.RoundedRectangleBorder(radius=6),
            )
        else:
            return ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                color=Theme.TEXT_PRIMARY,
                overlay_color=ft.Colors.with_opacity(0.05, Theme.PRIMARY),
                shape=ft.RoundedRectangleBorder(radius=6),
            )

    @staticmethod
    def get_container_style(
        has_border: bool = True,
        radius: int = 8
    ) -> dict:
        """Get container style

        Args:
            has_border: Whether to add border
            radius: Border radius

        Returns:
            Dictionary of container properties
        """
        result = {
            "bgcolor": Theme.SURFACE,
            "border_radius": radius,
        }

        if has_border:
            result["border"] = ft.Border.all(1, Theme.BORDER)

        return result

    @staticmethod
    def get_text_field_style() -> dict:
        """Get text field style

        Returns:
            Dictionary of text field properties
        """
        return {
            "border_color": Theme.BORDER,
            "focused_border_color": Theme.PRIMARY,
            "border_radius": 8,
            "text_size": 14,
            "content_padding": ft.Padding.all(16),
        }

    @staticmethod
    def get_checkbox_style() -> dict:
        """Get checkbox style

        Returns:
            Dictionary of checkbox properties
        """
        return {
            "fill_color": {
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, Theme.PRIMARY),
                ft.ControlState.SELECTED: Theme.PRIMARY,
            },
            "check_color": Theme.SURFACE,
        }

    @staticmethod
    def get_dropdown_style() -> dict:
        """Get dropdown style

        Returns:
            Dictionary of dropdown properties
        """
        return {
            "border_color": Theme.BORDER,
            "focused_border_color": Theme.PRIMARY,
            "border_radius": 6,
            "text_size": 13,
            "fill_color": Theme.SURFACE,
        }

    @staticmethod
    def apply_to_page(page: ft.Page) -> None:
        """Apply theme to Flet page

        Args:
            page: Flet Page object
        """
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = Theme.BACKGROUND
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=Theme.PRIMARY,
                on_primary=Theme.SURFACE,
                surface=Theme.SURFACE,
                on_surface=Theme.TEXT_PRIMARY,
            )
        )
