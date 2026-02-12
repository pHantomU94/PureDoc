"""PureDoc - Markdown to Word Converter

A lightweight cross-platform tool for converting Markdown documents
to clean, perfectly formatted Microsoft Word files.
"""

import flet as ft

from src.ui.theme import Theme
from src.ui.main_page import MainPage
from src import __version__

def main(page: ft.Page):
    """Main application entry point"""
    page.title = "PureDoc - Markdown to Word - (v" + __version__ + ")"  
    # page.padding = 20
    page.window.min_width = 800
    page.window.maximized = True
    page.window.min_height = 600
    Theme.apply_to_page(page)
    main_page = MainPage(page)


    def on_close(event):
        main_page.cleanup()
        page.on_close = on_close


if __name__ == "__main__":
    try:
        ft.run(main, assets_dir='assets')
    except Exception as e:
        print(f"启动失败: {e}")
