# Sidekick Python Library (`sidekick-py`)

[![PyPI version](https://badge.fury.io/py/sidekick-py.svg)](https://badge.fury.io/py/sidekick-py)

This library provides the Python interface for interacting with the [Sidekick Visual Coding Buddy](https://github.com/zhouer/Sidekick) frontend UI, typically running within VS Code. It allows your Python scripts to easily create, update, and interact with visual modules like grids (`Grid`), consoles (`Console`), variable visualizers (`Viz`), drawing canvases (`Canvas`), and UI controls (`Control`).

## Installation

Install the library using pip:

```bash
pip install sidekick-py
```

You will also need the [Sidekick VS Code extension](https://marketplace.visualstudio.com/items?itemName=sidekick-coding.sidekick-coding) installed and running in VS Code.

## Minimal Usage Example

**First, open the Sidekick panel** in VS Code (Press `Ctrl+Shift+P`, search for and run `Show Sidekick Panel`).

Then, save and run the following Python script:

```python
import sidekick

# 1. Create a default 16x16 Grid
grid = sidekick.Grid()

# 2. Define what happens when a cell is clicked
def handle_click(x, y):
    # Update the clicked cell in the Sidekick UI
    grid.set_color(x, y, 'red')
    print(f"Cell ({x}, {y}) clicked!") # Optional: Print to terminal

# 3. Register the click handler
grid.on_click(handle_click)

# 4. Keep the script running to listen for clicks!
#    Without this, the script would end, and clicks wouldn't be handled.
sidekick.run_forever()
```

After running the script, clicking the grid cells in the Sidekick panel will turn them red. Press `Ctrl+C` in the terminal to stop.

## Learn More

*   **Quick Start & Overview:** See the main [**Project README on GitHub**](https://github.com/zhouer/Sidekick) for a comprehensive guide.
*   **Full API Reference:** Explore detailed documentation for all modules, classes, and functions in the [**Python API Documentation**](https://zhouer.github.io/sidekick-py-docs/).
*   **Examples:** Check the `examples/` directory in the [GitHub repository](https://github.com/zhouer/Sidekick/tree/main/examples) for more usage scenarios.

This library simplifies the process by handling WebSocket communication and message formatting, allowing you to focus on controlling the visual elements from your Python code.
