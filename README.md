# Code to Video

A utility that converts markdown files with code blocks into MP4 videos showing the code being typed out with proper syntax highlighting.

## Features

- 📝 Parse markdown files and extract code blocks
- 🎨 Syntax highlighting for multiple programming languages
- 🎬 Generate MP4 videos with typing animations
- ⚡ Configurable typing speed and styling
- 🎯 Support for multiple code blocks in sequence

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python code_to_video.py input.md output.mp4
```

### List Available Themes

```bash
python code_to_video.py --list-themes
```

### Advanced Usage

```bash
python code_to_video.py input.md output.mp4 \
  --typing-speed 50 \
  --font-size 20 \
  --width 1280 \
  --height 720 \
  --theme monokai
```

## Options

- `--typing-speed`: Base characters per second (default: 30)
- `--font-size`: Font size in pixels (default: 16)
- `--width`: Video width (default: 1024)
- `--height`: Video height (default: 768)
- `--theme`: Color theme - see available themes with `--list-themes` (default: 'dark')
- `--pause-duration`: Pause between code blocks in seconds (default: 2.0)
- `--non-realistic`: Disable realistic typing (keyboard difficulty and patterns)
- `--randomness`: Amount of random variation in timing (0.0=none, 1.0=normal, 2.0=high, default: 1.0)
- `--list-themes`: Show all available themes and exit

## Themes

The utility supports multiple color themes for syntax highlighting. Available themes include:

- **dark**: Default dark theme with modern colors
- **light**: Clean light theme for bright environments
- **monokai**: Popular dark theme inspired by Sublime Text's Monokai
- **dracula**: Dark theme with purple accents and vibrant colors
- **github**: Light theme inspired by GitHub's code highlighting
- **solarized-dark**: Solarized dark color scheme
- **nord**: Arctic, north-bluish color palette

You can create custom themes by adding JSON files to the `themes/` directory. See `themes/README.md` for details.

## Realistic Typing

By default, the utility uses **realistic typing** with **randomness** to create natural, human-like animations. These are now separate controls:

### Realism (Keyboard Ergonomics & Patterns)

- **Keyboard Ergonomics**: Home row keys (ASDF, JKL;) are typed faster than numbers or special characters
- **Character Difficulty**: Keys farther from home position take longer to type
- **Special Characters**: Symbols requiring shift are slower than regular letters
- **Programming Patterns**: Common code patterns like `()`, `{}`, `def` are typed faster due to muscle memory
- **Smart Pauses**: Longer pauses after punctuation, newlines, and complex characters

### Randomness (Natural Variation)

- **Timing Variation**: Random fluctuations in keystroke timing
- **Human Inconsistency**: Simulates natural human typing inconsistency
- **Configurable**: Control how much variation you want

### Examples

```bash
# Default: Realistic + normal randomness
python code_to_video.py example.md output.mp4

# Realistic typing, no randomness (consistent delays for same characters)
python code_to_video.py example.md output.mp4 --randomness 0

# Realistic typing with high randomness
python code_to_video.py example.md output.mp4 --randomness 2

# Classic uniform typing (no realism, no randomness)
python code_to_video.py example.md output.mp4 --non-realistic --randomness 0

# Uniform base speed with randomness applied
python code_to_video.py example.md output.mp4 --non-realistic --randomness 2
```

### Randomness Levels

- `0.0`: No variation (perfectly consistent)
- `0.5`: Subtle variation
- `1.0`: Normal human-like variation (default)
- `1.5`: Noticeable variation
- `2.0`: High variation (very human-like)

### Typing Modes

| Mode | Description | Command |
|------|-------------|---------|
| **Realistic + Random** | Default - keyboard difficulty + natural variation | *(default)* |
| **Realistic Only** | Keyboard difficulty, no randomness | `--randomness 0` |
| **Random Only** | Uniform base + random variation | `--non-realistic` |
| **Classic Uniform** | Like old behavior - perfectly uniform | `--non-realistic --randomness 0` |

## Example Input

Create a markdown file like this:

````markdown
# My Code Examples

Here's a Python example:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == '__main__':
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
```

And here's some JavaScript:

```javascript
const factorial = (n) => {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
};

console.log(factorial(5)); // 120
```

````

The utility will create a video showing each code block being typed out with appropriate syntax highlighting.
