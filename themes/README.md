# Themes

This directory contains color theme files for the code-to-video utility. Themes control the appearance of syntax highlighting, background colors, and cursor colors in generated videos.

## Available Themes

### Dark Themes

- **dark**: Default dark theme with modern colors
- **monokai**: Popular dark theme inspired by Sublime Text's Monokai
- **dracula**: Dark theme with purple accents and vibrant colors
- **solarized-dark**: Solarized dark color scheme with carefully chosen colors
- **nord**: Arctic, north-bluish color palette

### Light Themes

- **light**: Clean light theme for bright environments  
- **github**: Light theme inspired by GitHub's code highlighting

## Using Themes

### List Available Themes

```bash
python code_to_video.py --list-themes
```

### Generate Video with Specific Theme

```bash
python code_to_video.py input.md output.mp4 --theme monokai
```

## Creating Custom Themes

Themes are defined as JSON files in this directory. Each theme file should have the following structure:

```json
{
  "name": "Theme Name",
  "description": "Brief description of the theme",
  "background": [R, G, B],
  "cursor": [R, G, B],
  "colors": {
    "keyword": [R, G, B],
    "string": [R, G, B],
    "comment": [R, G, B],
    "number": [R, G, B],
    "function": [R, G, B],
    "class": [R, G, B],
    "operator": [R, G, B],
    "default": [R, G, B]
  }
}
```

### Color Categories

- **keyword**: Language keywords (if, for, def, function, etc.)
- **string**: String literals and text
- **comment**: Code comments
- **number**: Numeric literals
- **function**: Function names and calls
- **class**: Class names and types
- **operator**: Operators and punctuation (+, -, =, {, }, etc.)
- **default**: Default text color for everything else

### RGB Values

All colors are specified as RGB arrays with values from 0-255:

- `[255, 0, 0]` = Red
- `[0, 255, 0]` = Green  
- `[0, 0, 255]` = Blue
- `[255, 255, 255]` = White
- `[0, 0, 0]` = Black

### Example Custom Theme

Create a file called `my-theme.json`:

```json
{
  "name": "My Custom Theme",
  "description": "A custom theme with my favorite colors",
  "background": [30, 30, 40],
  "cursor": [255, 255, 0],
  "colors": {
    "keyword": [255, 100, 100],
    "string": [100, 255, 100],
    "comment": [150, 150, 150],
    "number": [255, 200, 100],
    "function": [100, 200, 255],
    "class": [255, 255, 100],
    "operator": [200, 100, 255],
    "default": [220, 220, 220]
  }
}
```

Then use it with:

```bash
python code_to_video.py input.md output.mp4 --theme my-theme
```

## Tips for Creating Themes

1. **Contrast**: Ensure good contrast between text and background
2. **Accessibility**: Consider color-blind users when choosing colors
3. **Hierarchy**: Use different colors to create visual hierarchy (comments dimmer than keywords)
4. **Consistency**: Keep related elements (like different operators) using similar colors
5. **Testing**: Generate test videos to see how your theme looks in practice

## Fallback Behavior

If a theme file cannot be loaded or a theme is not found, the utility will:

1. Print a warning message
2. Fall back to the default 'dark' theme
3. Continue processing

This ensures videos can always be generated even with theme issues.
