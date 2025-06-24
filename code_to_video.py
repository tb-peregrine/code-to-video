#!/usr/bin/env python3
"""
Code to Video - Convert markdown code blocks to typing animation videos
"""

import json
import os
import re
import time
from typing import List, Tuple, Dict, Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pygments.lexers import get_lexer_by_name
import click


class Theme:
    """Represents a color theme for syntax highlighting"""
    def __init__(self, name: str, description: str, background: List[int], 
                 cursor: List[int], colors: Dict[str, List[int]]):
        self.name = name
        self.description = description
        self.background = tuple(background)
        self.cursor = tuple(cursor)
        self.colors = {k: tuple(v) for k, v in colors.items()}


class ThemeManager:
    """Manages loading and accessing themes"""
    
    def __init__(self, themes_dir: str = "themes"):
        self.themes_dir = themes_dir
        self._themes: Dict[str, Theme] = {}
        self._load_themes()
    
    def _load_themes(self):
        """Load all theme files from the themes directory"""
        if not os.path.exists(self.themes_dir):
            print(f"Warning: Themes directory '{self.themes_dir}' not found")
            self._load_default_themes()
            return
        
        for filename in os.listdir(self.themes_dir):
            if filename.endswith('.json'):
                theme_name = filename[:-5]  # Remove .json extension
                theme_path = os.path.join(self.themes_dir, filename)
                
                try:
                    with open(theme_path, 'r') as f:
                        theme_data = json.load(f)
                    
                    theme = Theme(
                        name=theme_data['name'],
                        description=theme_data['description'],
                        background=theme_data['background'],
                        cursor=theme_data['cursor'],
                        colors=theme_data['colors']
                    )
                    
                    self._themes[theme_name] = theme
                    
                except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
                    print(f"Warning: Could not load theme '{filename}': {e}")
        
        # If no themes were loaded, load defaults
        if not self._themes:
            self._load_default_themes()
    
    def _load_default_themes(self):
        """Load built-in default themes as fallback"""
        # Default dark theme
        dark_theme = Theme(
            name="Dark",
            description="Default dark theme",
            background=[40, 44, 52],
            cursor=[255, 255, 255],
            colors={
                'keyword': [198, 120, 221],
                'string': [152, 195, 121],  
                'comment': [92, 99, 112],
                'number': [209, 154, 102],
                'function': [97, 175, 239],
                'class': [229, 192, 123],
                'operator': [86, 182, 194],
                'default': [171, 178, 191]
            }
        )
        
        # Default light theme
        light_theme = Theme(
            name="Light",
            description="Default light theme",
            background=[255, 255, 255],
            cursor=[0, 0, 0],
            colors={
                'keyword': [128, 0, 128],
                'string': [0, 128, 0],
                'comment': [128, 128, 128],
                'number': [255, 140, 0],
                'function': [0, 0, 255],
                'class': [184, 134, 11],
                'operator': [0, 139, 139],
                'default': [0, 0, 0]
            }
        )
        
        self._themes['dark'] = dark_theme
        self._themes['light'] = light_theme
    
    def get_theme(self, theme_name: str) -> Theme:
        """Get a theme by name"""
        if theme_name in self._themes:
            return self._themes[theme_name]
        
        print(f"Warning: Theme '{theme_name}' not found, using 'dark' as fallback")
        return self._themes.get('dark', list(self._themes.values())[0])
    
    def list_themes(self) -> List[str]:
        """Get list of available theme names"""
        return list(self._themes.keys())
    
    def get_theme_info(self) -> List[Tuple[str, str]]:
        """Get list of (theme_name, description) tuples"""
        return [(name, theme.description) for name, theme in self._themes.items()]


class CodeBlock:
    """Represents a code block from markdown"""

    def __init__(self, language: str, code: str):
        self.language = language.lower() if language else 'text'
        self.code = code.strip()
        self.lines = code.strip().split('\n')


class VideoConfig:
    """Configuration for video generation"""

    def __init__(self,
                 width: int = 1024,
                 height: int = 768,
                 fps: int = 30,
                 typing_speed: int = 30,  # characters per second
                 font_size: int = 16,
                 theme: str = 'dark',
                 pause_duration: float = 2.0):
        self.width = width
        self.height = height
        self.fps = fps
        self.typing_speed = typing_speed
        self.font_size = font_size
        self.theme_name = theme
        self.pause_duration = pause_duration
        
        # Load theme configuration
        theme_manager = ThemeManager()
        self.theme = theme_manager.get_theme(theme)
        self.bg_color = self.theme.background
        self.cursor_color = self.theme.cursor


class SyntaxHighlighter:
    """Handles syntax highlighting for different languages"""

    def __init__(self, theme: Theme):
        self.theme = theme
        self.colors = theme.colors

    def get_highlighted_text(self, code: str, language: str) -> List[Tuple[str, str]]:
        """
        Returns a list of (text, token_type) tuples for syntax highlighting
        """
        try:
            if language == 'text' or not language:
                return [(code, 'default')]

            lexer = get_lexer_by_name(language, stripall=True)
            tokens = list(lexer.get_tokens(code))

            result = []
            for token_type, text in tokens:
                token_name = str(token_type).split('.')[-1].lower()

                # Map token types to our color categories
                if 'keyword' in token_name:
                    color_key = 'keyword'
                elif 'string' in token_name or 'literal' in token_name:
                    color_key = 'string' if 'string' in token_name else 'number'
                elif 'comment' in token_name:
                    color_key = 'comment'
                elif 'name' in token_name:
                    if 'function' in token_name:
                        color_key = 'function'
                    elif 'class' in token_name:
                        color_key = 'class'
                    else:
                        color_key = 'default'
                elif 'operator' in token_name or 'punctuation' in token_name:
                    color_key = 'operator'
                else:
                    color_key = 'default'

                result.append((text, color_key))

            return result

        except Exception as e:
            print(f"Warning: Could not highlight {language} code, using plain text: {e}")
            return [(code, 'default')]


class CodeToVideoGenerator:
    """Main class for generating videos from code blocks"""

    def __init__(self, config: VideoConfig):
        self.config = config
        self.highlighter = SyntaxHighlighter(config.theme)

        # Try to load a monospace font
        self.font = self._load_font()

    def _load_font(self):
        """Load a suitable monospace font"""
        font_paths = [
            '/System/Library/Fonts/Monaco.ttf',  # macOS
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',  # Linux
            'C:/Windows/Fonts/consola.ttf',  # Windows
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, self.config.font_size)
            except (OSError, IOError):
                continue

        # Fallback to default font
        try:
            return ImageFont.load_default()
        except BaseException:
            return None

    def parse_markdown(self, markdown_content: str) -> List[CodeBlock]:
        """Extract code blocks from markdown content"""
        code_blocks = []

        # Pattern to match fenced code blocks
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, markdown_content, re.DOTALL)

        for language, code in matches:
            if code.strip():  # Skip empty code blocks
                code_blocks.append(CodeBlock(language, code))

        return code_blocks

    def _calculate_indentation_width(self, text: str, start_pos: int) -> int:
        """Calculate the visual width of indentation after a newline"""
        if start_pos >= len(text):
            return 0

        indent_width = 0
        pos = start_pos

        while pos < len(text) and text[pos] in ' \t':
            if text[pos] == '\t':
                # Tab is typically 4 or 8 spaces, let's use 4
                indent_width += 4
            else:
                # Regular space
                indent_width += 1
            pos += 1

        # Convert to pixel width (approximate)
        if self.font:
            # Use a space character to estimate character width
            space_bbox = self.font.getbbox(' ')
            char_width = space_bbox[2] - space_bbox[0]
            return int(indent_width * char_width)

        return indent_width * 8  # Fallback estimate

    def create_frame(self, text_content: str, highlighted_tokens: List[Tuple[str, str]],
                     current_pos: int) -> np.ndarray:
        """Create a single frame of the video"""
        # Create PIL image
        img = Image.new('RGB', (self.config.width, self.config.height), self.config.bg_color)
        draw = ImageDraw.Draw(img)

        # Starting position
        x, y = 20, 20
        line_height = self.config.font_size + 4
        left_margin = 20

        # Draw the text up to current position
        char_count = 0
        for token_text, token_type in highlighted_tokens:
            if char_count >= current_pos:
                break

            # Process each character individually to properly handle newlines
            remaining_chars = current_pos - char_count
            chars_to_process = min(len(token_text), remaining_chars)

            if chars_to_process <= 0:
                break

            text_to_process = token_text[:chars_to_process]
            color = self.highlighter.colors.get(token_type, self.highlighter.colors['default'])

            # Process character by character to handle newlines properly
            current_line = ""
            for i, char in enumerate(text_to_process):
                if char == '\n':
                    # Draw the current line if it has content
                    if current_line and self.font:
                        draw.text((x, y), current_line, font=self.font, fill=color)
                    # Move to next line
                    y += line_height

                    # Calculate indentation for the next line
                    next_char_pos = char_count + i + 1
                    indent_width = self._calculate_indentation_width(text_content, next_char_pos)
                    x = left_margin + indent_width

                    current_line = ""
                else:
                    current_line += char

            # Draw any remaining text on the current line
            if current_line and self.font:
                draw.text((x, y), current_line, font=self.font, fill=color)
                bbox = draw.textbbox((x, y), current_line, font=self.font)
                x = bbox[2]

            char_count += chars_to_process

            if char_count >= current_pos:
                break

        # Add cursor
        if current_pos < len(text_content):
            cursor_color = self.config.cursor_color
            draw.rectangle([x, y, x + 2, y + self.config.font_size], fill=cursor_color)

        # Convert PIL image to OpenCV format
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return cv_img

    def generate_video(self, code_blocks: List[CodeBlock], output_path: str):
        """Generate the complete video"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.config.fps,
                              (self.config.width, self.config.height))

        try:
            for i, block in enumerate(code_blocks):
                print(f"Processing code block {i + 1}/{len(code_blocks)} ({block.language})")

                # Get syntax highlighted tokens
                highlighted_tokens = self.highlighter.get_highlighted_text(
                    block.code, block.language)

                # Calculate frames needed for typing
                total_chars = len(block.code)
                chars_per_frame = self.config.typing_speed / self.config.fps
                total_frames = int(total_chars / chars_per_frame) + 1

                # Generate frames for typing animation
                for frame_num in range(total_frames):
                    current_pos = min(int(frame_num * chars_per_frame), total_chars)
                    frame = self.create_frame(block.code, highlighted_tokens, current_pos)
                    out.write(frame)

                # Hold the final frame
                final_frame = self.create_frame(block.code, highlighted_tokens, total_chars)
                for _ in range(int(self.config.fps * self.config.pause_duration)):
                    out.write(final_frame)

                # Clear screen between blocks (except for the last one)
                if i < len(code_blocks) - 1:
                    clear_frame = np.full((self.config.height, self.config.width, 3),
                                          self.config.bg_color, dtype=np.uint8)
                    clear_frame = cv2.cvtColor(clear_frame, cv2.COLOR_RGB2BGR)
                    for _ in range(int(self.config.fps * 0.5)):  # Half second clear
                        out.write(clear_frame)

        finally:
            out.release()
            cv2.destroyAllWindows()


def get_available_themes():
    """Get list of available themes for CLI validation"""
    theme_manager = ThemeManager()
    return theme_manager.list_themes()


@click.command()
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.argument('output_file', type=click.Path(), required=False)
@click.option('--typing-speed', default=30, help='Characters typed per second')
@click.option('--font-size', default=16, help='Font size in pixels')
@click.option('--width', default=1024, help='Video width')
@click.option('--height', default=768, help='Video height')
@click.option('--theme', default='dark', type=click.Choice(get_available_themes(), case_sensitive=False),
              help='Color theme')
@click.option('--pause-duration', default=2.0, help='Pause between code blocks in seconds')
@click.option('--list-themes', is_flag=True, help='List available themes and exit')
def main(input_file, output_file, typing_speed, font_size, width, height, theme, pause_duration, list_themes):
    """Convert markdown code blocks to a typing animation video."""

    # Handle list themes option
    if list_themes:
        theme_manager = ThemeManager()
        print("🎨 Available Themes:")
        print()
        for theme_name, description in theme_manager.get_theme_info():
            print(f"  {theme_name:<15} - {description}")
        return

    # Validate required arguments when not listing themes
    if not input_file or not output_file:
        click.echo("Error: INPUT_FILE and OUTPUT_FILE are required when not using --list-themes")
        click.echo("Try 'code_to_video.py --help' for help.")
        return

    print("🎬 Code to Video Generator")
    print(f"📝 Input: {input_file}")
    print(f"🎥 Output: {output_file}")
    print(f"🎨 Theme: {theme}")

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Create configuration
    config = VideoConfig(
        width=width,
        height=height,
        typing_speed=typing_speed,
        font_size=font_size,
                         theme=theme,
        pause_duration=pause_duration
    )

    # Create generator
    generator = CodeToVideoGenerator(config)

    # Parse markdown
    code_blocks = generator.parse_markdown(markdown_content)

    if not code_blocks:
        print("❌ No code blocks found in the markdown file!")
        return

    print(f"📋 Found {len(code_blocks)} code block(s)")
    for i, block in enumerate(code_blocks):
        lines = len(block.lines)
        chars = len(block.code)
        print(f"  {i + 1}. {block.language} ({lines} lines, {chars} characters)")

    # Generate video
    print("🎬 Generating video...")
    start_time = time.time()

    generator.generate_video(code_blocks, output_file)

    end_time = time.time()
    print(f"✅ Video generated successfully in {end_time - start_time:.2f} seconds!")
    print(f"📁 Output saved to: {output_file}")


if __name__ == '__main__':
    main()
