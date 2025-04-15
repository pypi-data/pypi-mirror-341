**ProgressVertical** is a Python library for displaying vertical progress bars for command-line interface (CLI) applications.  
Designed with a focus on usability and customization, allowing the creation of multi-stage progress animations with configurable colors, styles, and durations, inspired by another library [_progressbar_](https://pypi.org/project/progressbar/).

## The differential of ProgressVertical

| ProgressVertical              | ProgressBar2                                                |
| ---------------------------- | ----------------------------------------------------------- |
| Multiple parallel stages with compact visualization.     | Single or sequential linear progress. |
| Independent logic for each bar.                          | Single progress with sub-bar support  |
| Monitors multiple tasks in parallel                      | Traditional linear progress with built-in metrics  |

Processes are batch-based, allowing monitoring of tasks in parallel without depending on others, reducing overhead.

## Installation:

```pip
pip install progressvertical

```
### Usage Example

```python
from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager

ColorManager.init_colorama()  # Initializes Colorama

renderer = VerticalProgressRenderer(height=10, spacing=6)
manager = ProgressManager(renderer)

manager.add_stage("Processing", 2.0, fore_color="green", style="bright")
manager.add_stage("Validation", 3.0, fore_color="yellow", back_color="blue")
manager.add_stage("Finalization", 1.5, fore_color="red", style="dim")

manager.start_animation(update_interval=0.1)
```

[![ProgressVertical](https://img.shields.io/badge/ProgressVertical-%200.1.5-0073B7?style=for-the-badge&logo=python)](https://pypi.org/project/progressvertical/)
