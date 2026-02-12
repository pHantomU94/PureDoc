"""Core conversion logic for PureDoc"""

import os
import subprocess
from typing import Callable
from pathlib import Path
import pypandoc


class ConversionError(Exception):
    """Custom exception for conversion errors"""
    pass


class Converter:
    """Handles Markdown to Word conversion using Pandoc"""

    def __init__(
        self,
        lua_filter_path: str,
        template_path: str | None = None,
        ignore_bullets: bool = True
    ):
        """Initialize converter

        Args:
            lua_filter_path: Path to Lua filter script
            template_path: Path to Word template (optional)
            ignore_bullets: Whether to ignore bullet points
        """


        self.lua_filter_path = lua_filter_path
        self.template_path = template_path
        self.ignore_bullets = ignore_bullets

    def get_pandoc_args(self, is_export: bool = False) -> list[str]:
        """Generate Pandoc arguments

        Args:
            is_export: Whether this is for export (includes template) or preview

        Returns:
            List of Pandoc arguments
        """
        args = ['--from=markdown+hard_line_breaks']

        # Add ignore bullets metadata
        if self.ignore_bullets:
            args.append("--metadata=ignore_bullets=true")

        # Add template for export
        if is_export and self.template_path and os.path.exists(self.template_path):
            args.append(f'--reference-doc={self.template_path}')

        # Add Lua filter
        if os.path.exists(self.lua_filter_path):
            args.append(f'--lua-filter={self.lua_filter_path}')

        args.append('--wrap=none')
        return args

    def convert_text(
        self,
        md_text: str,
        output_format: str = 'markdown',
        is_export: bool = False
    ) -> str:
        """Convert markdown text to specified format

        Args:
            md_text: Input markdown text
            output_format: Target format (default: markdown for preview)
            is_export: Whether this is for export

        Returns:
            Converted text

        Raises:
            ConversionError: If conversion fails
        """
        if not md_text:
            return ""

        try:
            result = pypandoc.convert_text(
                md_text,
                output_format,
                format='markdown+hard_line_breaks',
                extra_args=self.get_pandoc_args(is_export=is_export)
            )
            return result
        except Exception as e:
            raise ConversionError(f"Preview conversion failed: {e}")

    def convert_to_word(
        self,
        md_text: str,
        output_path: str,
        progress_callback: Callable[[int], None] | None = None
    ) -> None:
        """Convert markdown text to Word document

        Args:
            md_text: Input markdown text
            output_path: Output file path (.docx)
            progress_callback: Optional callback for progress updates (0-100)

        Raises:
            ConversionError: If conversion fails
        """
        if not md_text:
            raise ConversionError("Input text is empty")

        try:
            if progress_callback:
                progress_callback(10)

            # Generate default template if needed
            if self.template_path and not os.path.exists(self.template_path):
                try:
                    subprocess.run(
                        ['pandoc', '-o', str(self.template_path),
                         '--print-default-data-file', 'reference.docx'],
                        check=True,
                        capture_output=True
                    )
                except Exception:
                    pass  # Use Pandoc's built-in default

            if progress_callback:
                progress_callback(30)

            # Convert to Word
            pypandoc.convert_text(
                md_text,
                'docx',
                format='markdown+hard_line_breaks',
                outputfile=output_path,
                extra_args=self.get_pandoc_args(is_export=True)
            )

            if progress_callback:
                progress_callback(100)

        except Exception as e:
            raise ConversionError(f"Word export failed: {e}")

    def convert_file_to_word(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Callable[[int], None] | None = None
    ) -> None:
        """Convert a markdown file to Word document

        Args:
            input_path: Input markdown file path
            output_path: Output file path (.docx)
            progress_callback: Optional callback for progress updates (0-100)

        Raises:
            ConversionError: If conversion fails
        """
        if not os.path.exists(input_path):
            raise ConversionError(f"Input file not found: {input_path}")

        try:
            if progress_callback:
                progress_callback(10)

            # Generate default template if needed
            if self.template_path and not os.path.exists(self.template_path):
                try:
                    subprocess.run(
                        ['pandoc', '-o', str(self.template_path),
                         '--print-default-data-file', 'reference.docx'],
                        check=True,
                        capture_output=True
                    )
                except Exception:
                    pass

            if progress_callback:
                progress_callback(30)

            # Convert file to Word
            pypandoc.convert_file(
                input_path,
                'docx',
                outputfile=output_path,
                extra_args=self.get_pandoc_args(is_export=True)
            )

            if progress_callback:
                progress_callback(100)

        except Exception as e:
            raise ConversionError(f"File conversion failed: {e}")

    def set_template_path(self, path: str) -> None:
        """Set the Word template path

        Args:
            path: Path to template file (.docx)
        """
        self.template_path = path

    def set_ignore_bullets(self, ignore: bool) -> None:
        """Set whether to ignore bullet points

        Args:
            ignore: True to ignore bullets, False to keep them
        """
        self.ignore_bullets = ignore
