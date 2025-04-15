import sys
from colorama import Cursor
from .interfaces import ProgressRenderer
from .color_manager import ColorManager

class VerticalRenderer(ProgressRenderer):
    def __init__(self, height: int = 10, spacing: int = 4):
        self.height = height
        self.spacing = spacing
        self._lines_used = 0

    def render(self, progress_data: list) -> None:
        sys.stdout.write(Cursor.UP(self._lines_used) + Cursor.POS(0))
        
        lines = []
        for task in progress_data:
            percent = (task["current"] / task["total"]) * 100
            filled = int(self.height * (percent / 100))
            
            bar = (
                task["colors"]["fore"] + 
                task["colors"]["style"] + 
                "▓" * filled + 
                "░" * (self.height - filled) + 
                ColorManager.RESET
            )
            
            status = f"{task['label']}: {percent:.1f}%"
            lines.append(f"{bar} {status}")
        
        self._lines_used = len(lines)
        print("\n".join(lines), end="", flush=True)

    def cleanup(self):
        print("\n" * self._lines_used)
