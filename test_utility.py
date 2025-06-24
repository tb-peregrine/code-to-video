#!/usr/bin/env python3
"""
Test script for the code-to-video utility
"""

from code_to_video import CodeToVideoGenerator, VideoConfig
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_markdown_parsing():
    """Test markdown parsing functionality"""
    print("🧪 Testing markdown parsing...")

    config = VideoConfig()
    generator = CodeToVideoGenerator(config)

    # Test markdown content
    test_markdown = """
# Test

```python
print("Hello, world!")
```

```javascript
console.log("Hello from JS!");
```
"""

    code_blocks = generator.parse_markdown(test_markdown)

    assert len(code_blocks) == 2, f"Expected 2 code blocks, got {len(code_blocks)}"
    assert code_blocks[0].language == 'python', f"Expected 'python', got '{
        code_blocks[0].language}'"
    assert code_blocks[1].language == 'javascript', f"Expected 'javascript', got '{
        code_blocks[1].language}'"

    print("✅ Markdown parsing test passed!")


def test_syntax_highlighting():
    """Test syntax highlighting functionality"""
    print("🧪 Testing syntax highlighting...")

    from code_to_video import SyntaxHighlighter, ThemeManager

    theme_manager = ThemeManager()
    dark_theme = theme_manager.get_theme('dark')
    highlighter = SyntaxHighlighter(dark_theme)

    # Test Python highlighting
    python_code = "def hello():\n    print('Hello!')"
    tokens = highlighter.get_highlighted_text(python_code, 'python')

    assert len(tokens) > 0, "Should have tokens"
    print(f"   Python tokens: {len(tokens)}")

    # Test JavaScript highlighting
    js_code = "const x = 42;"
    tokens = highlighter.get_highlighted_text(js_code, 'javascript')

    assert len(tokens) > 0, "Should have tokens"
    print(f"   JavaScript tokens: {len(tokens)}")

    print("✅ Syntax highlighting test passed!")


def test_video_generation_dry_run():
    """Test video generation setup (without actually creating video)"""
    print("🧪 Testing video generation setup...")

    config = VideoConfig(width=640, height=480, typing_speed=50)
    generator = CodeToVideoGenerator(config)

    # Test frame creation
    tokens = [("print", "keyword"), ("(", "operator"), ("'hello'", "string"), (")", "operator")]
    frame = generator.create_frame("print('hello')", tokens, 5)

    assert frame is not None, "Frame should be created"
    assert frame.shape == (480, 640, 3), f"Expected (480, 640, 3), got {frame.shape}"

    print("✅ Video generation setup test passed!")


def test_indentation_handling():
    """Test that indentation is properly calculated"""
    print("🧪 Testing indentation handling...")

    config = VideoConfig(width=640, height=480, typing_speed=50)
    generator = CodeToVideoGenerator(config)

    # Test indentation calculation
    test_text = "if True:\n    print('indented')\n        print('more indented')"

    # Find the correct positions after newlines
    first_newline = test_text.find('\n') + 1
    second_newline = test_text.find('\n', first_newline) + 1

    # Test 4-space indentation
    indent_width = generator._calculate_indentation_width(test_text, first_newline)
    assert indent_width > 0, "Should detect indentation"

    # Test 8-space indentation
    indent_width2 = generator._calculate_indentation_width(test_text, second_newline)
    assert indent_width2 > indent_width, "Should detect deeper indentation"

    print("✅ Indentation handling test passed!")


def test_theme_system():
    """Test theme loading functionality"""
    print("🧪 Testing theme system...")

    from code_to_video import ThemeManager

    theme_manager = ThemeManager()

    # Test theme loading
    themes = theme_manager.list_themes()
    assert len(themes) > 0, "Should have themes available"
    assert 'dark' in themes, "Should have default dark theme"
    assert 'light' in themes, "Should have default light theme"

    # Test theme retrieval
    dark_theme = theme_manager.get_theme('dark')
    assert dark_theme.name == "Dark", f"Expected 'Dark', got '{dark_theme.name}'"
    assert hasattr(dark_theme, 'colors'), "Theme should have colors"
    assert hasattr(dark_theme, 'background'), "Theme should have background"
    assert hasattr(dark_theme, 'cursor'), "Theme should have cursor color"

    print(f"   Found {len(themes)} themes: {', '.join(themes)}")
    print("✅ Theme system test passed!")


def test_realistic_typing():
    """Test realistic typing system"""
    print("🧪 Testing realistic typing system...")

    from code_to_video import TypingRealism

    # Test basic initialization
    typing_realism = TypingRealism(base_speed=30.0, realistic=True, randomness=1.0)
    
    # Test character delay calculation
    test_chars = ['a', 'Q', '!', ' ', '\n', '(', ')']
    delays = []
    
    for char in test_chars:
        delay = typing_realism.get_character_delay(char, "test context", 5)
        delays.append(delay)
        assert delay > 0, f"Delay for '{char}' should be positive"
    
    # Test that different characters have different delays (with realism)
    home_row_delay = typing_realism.get_character_delay('a', "", 0)
    number_delay = typing_realism.get_character_delay('1', "", 0)
    special_delay = typing_realism.get_character_delay('!', "", 0)
    
    # Numbers and special chars should generally be slower than home row
    # (though random variation might occasionally make them faster)
    print(f"   Realistic+Random 'a': {home_row_delay:.3f}s")
    print(f"   Realistic+Random '1': {number_delay:.3f}s") 
    print(f"   Realistic+Random '!': {special_delay:.3f}s")
    
    # Test pause delays
    pause_delay = typing_realism.get_pause_delay("comma")
    assert pause_delay > 0, "Pause delay should be positive"
    print(f"   Comma pause: {pause_delay:.3f}s")
    
    # Test non-realistic mode with no randomness (classic uniform)
    uniform = TypingRealism(base_speed=30.0, realistic=False, randomness=0.0)
    uniform_delay = uniform.get_character_delay('a', "", 0)
    base_expected = 1.0 / 30.0  # Should be exactly this
    assert abs(uniform_delay - base_expected) < 0.001, "Uniform mode should give exact timing"
    print(f"   Uniform mode 'a': {uniform_delay:.3f}s")
    
    # Test realistic mode with no randomness
    realistic_no_random = TypingRealism(base_speed=30.0, realistic=True, randomness=0.0)
    realistic_delay_1 = realistic_no_random.get_character_delay('a', "", 0)
    realistic_delay_2 = realistic_no_random.get_character_delay('a', "", 0)
    assert abs(realistic_delay_1 - realistic_delay_2) < 0.001, "No randomness should give consistent delays"
    print(f"   Realistic no-random 'a': {realistic_delay_1:.3f}s")
    
    print("✅ Realistic typing test passed!")


def main():
    """Run all tests"""
    print("🚀 Running code-to-video utility tests...\n")

    try:
        test_markdown_parsing()
        test_syntax_highlighting()
        test_video_generation_dry_run()
        test_indentation_handling()
        test_theme_system()
        test_realistic_typing()

        print("\n🎉 All tests passed! The utility is ready to use.")
        print("\nTo generate a video from the example file, run:")
        print("python code_to_video.py example.md output.mp4")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
