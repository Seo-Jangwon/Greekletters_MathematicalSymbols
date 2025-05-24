# Greek letters & Mathematical Symbols

## Download
[GreekLetters & MathSymbols 1.2.0](https://github.com/Seo-Jangwon/Greekletters_MathematicalSymbols/releases/download/v2.0.0/GreekLetters.MathSymbols.1.2.0.exe)

[GreekLetters & MathSymbols 2.0.0](https://github.com/Seo-Jangwon/Greekletters_MathematicalSymbols/releases/download/v2.0.0/GreekLetters.MathSymbols.2.0.0.exe)


## What's New in v2.0.0?
### Custom Symbol Categories
- **JSON-based Customization**: Create your own symbol categories using simple JSON files
- **Built-in Category Management**: Add, edit, and manage custom categories directly from the app
- **Automatic File Generation**: Pre-loaded with common symbol categories (Math, Physics, Chemistry, etc.)
- **Hot Reload**: Changes to JSON files are reflected immediately with the reload button
- **Custom Colors**: Each category can have its own border color for visual organization
- **Flexible Ordering**: Control the display order of categories with simple numbering

### Enhanced User Interface
- **Organized Categories**: Clear separation between "Basic" (Greek letters) and "Custom" categories
- **Visual Improvements**: Added section labels and dividers for better organization
- **Three-Button Control Panel**: 
  - **Add**: Creates new category templates automatically
  - **Edit**: Opens custom symbols folder for direct file editing
  - **Reload**: Refreshes categories without restarting the app

### Easy Customization Workflow
1. **Click "Add"** → Automatic template creation with examples
2. **Click "Edit"** → Opens folder with JSON files and documentation
3. **Edit JSON files** → Add your symbols with LaTeX codes and descriptions
4. **Click "Reload"** → See changes instantly

### Technical Improvements
- **Error Handling**: Invalid JSON files are ignored with clear error messages
- **File Validation**: Automatic structure checking ensures stability
- **Documentation**: Built-in README.md with examples and color codes

## What's New in v1.2.0?
- Added favorites feature
- Removed problematic responsive design
- Previous state is now saved

## Features in v2.0.0

### Functionality
- **Greek Letters & Mathematical Symbols**: Easy access to lowercase/uppercase Greek letters and comprehensive mathematical symbols
- **Dual Output Modes**: Switch between regular symbol output and LaTeX code output
- **One-Click Copy**: Click any symbol to instantly copy to clipboard with status feedback

### Symbol Organization
- **Basic Categories**: Greek letters (lowercase/uppercase) always available
- **Custom Categories**: Unlimited user-defined categories via JSON files
- **Pre-loaded Symbols**: Math/Engineering, Physics, Chemistry, Script Letters, Set Theory, Logic, Probability, Calculus, AI/ML, and Definitions/Relationships
- **Color-Coded Categories**: Each category can have custom border colors

### User Experience
- **Favorites System**: Save frequently used symbols with drag-and-drop functionality for easy management
- **Recent History**: Automatically tracks recently used symbols for quick access
- **Drag & Drop Interface**: Drag symbols from recent list to favorites, reorder favorites by dragging
- **Persistent Settings**: All preferences, favorites, recent history, and custom categories are automatically saved and restored

### Customization
- **Custom Symbol Categories**: Create unlimited categories using JSON files
- **Easy Category Management**: Built-in tools for adding, editing, and reloading categories
- **Flexible Symbol Definitions**: Each symbol includes display form, LaTeX code, and description
- **Visual Organization**: Custom colors and ordering for personalized workflow

### Interface & Themes
- **Dual Theme Support**: Light and dark mode themes with Tokyo Night color scheme
- **Always on Top Option**: Keep the application visible above other windows

## Features in v1.2.0
- **Greek Letters & Mathematical Symbols**: Easy access to lowercase/uppercase Greek letters and comprehensive mathematical symbols
- **Dual Output Modes**: Switch between regular symbol output and LaTeX code output
- **Categories**: Organized into 12 categories including Greek letters, script letters, math/engineering symbols, vector/matrix operations, set theory, logic, probability, physics, calculus, AI/ML, and definitions/relationships
- **Favorites System**: Save frequently used symbols with drag-and-drop functionality for easy management
- **Recent History**: Automatically tracks recently used symbols for quick access
- **Dual Theme Support**: Light and dark mode themes with Tokyo Night color scheme
- **Always on Top Option**: Keep the application visible above other windows
- **Persistent Settings**: All preferences, favorites, and recent history are automatically saved and restored
- **Drag & Drop Interface**: Drag symbols from recent list to favorites, reorder favorites by dragging
- **One-Click Copy**: Click any symbol to instantly copy to clipboard with status feedback


## Custom Categories Guide in v2.0.0

### JSON Structure
```json
{
  "category_info": {
    "name": "My Physics Symbols",
    "description": "Quantum mechanics and thermodynamics",
    "order": 100,
    "color": "#7aa2f7"
  },
  "symbols": [
    {
      "symbol": "ħ",
      "latex": "\\hbar",
      "name": "reduced Planck constant"
    },
    {
      "symbol": "⟨ψ|φ⟩",
      "latex": "\\langle \\psi | \\phi \\rangle",
      "name": "inner product"
    }
  ]
}
```

### How to Add Custom Categories
1. **Click "Add"** button → Creates template file automatically
2. **Click "Edit"** button → Opens custom symbols folder
3. **Modify JSON files** → Edit templates or create new ones
4. **Click "Reload"** → Apply changes without restarting

## Images

![image](https://github.com/user-attachments/assets/0c5848cf-cbd0-497e-b92e-d695e4b0ad3d)


## contributor
[BongSangKim](https://github.com/BongSangKim)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Requirements
- Python 3.6+
- PyQt5
