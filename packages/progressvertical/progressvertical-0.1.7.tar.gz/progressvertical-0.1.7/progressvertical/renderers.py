import sys
from .color_manager import ColorManager

class VerticalProgressRenderer:
    def __init__(self, height=10, spacing=3):
        self.height = height
        self.spacing = spacing
        self.bar_width = 3
        self._first_render = True

    def _move_cursor_up(self, lines):
        """Move o cursor para cima sem limpar o conteúdo"""
        sys.stdout.write(f"\033[{lines}A")

    def render(self, progress_data):
        if self._first_render:
            print("\n" * (self.height + 3))
            self._move_cursor_up(self.height + 3)
            self._first_render = False
        else:
            self._move_cursor_up(self.height + 3)
        
        sys.stdout.write("\033[J") 
        
        for line in range(self.height, 0, -1):
            line_str = ""
            for i, data in enumerate(progress_data):
                prefix = " " * (self.spacing if i > 0 else 1)
                block = '▓▓▓' if line <= data['progress'] else '   '
                color = f"{data.get('fore_color','')}{data.get('back_color','')}{data.get('style','')}"
                line_str += f"{prefix}{color}{block}{ColorManager.RESET}"
            print(line_str)
        
        labels_line = ""
        for i, data in enumerate(progress_data):
            prefix = " " * (self.spacing if i > 0 else 1)
            labels_line += f"{prefix}{data['label'].center(self.bar_width)}"
        print(labels_line)
        
        percent_line = ""
        for i, data in enumerate(progress_data):
            prefix = " " * (self.spacing if i > 0 else 1)
            pct = min(100, (data['progress']/self.height)*100)
            color = f"{data.get('fore_color','')}{data.get('style','')}"
            percent_line += f"{prefix}{color}{pct:3.0f}%{ColorManager.RESET}"
        print(percent_line)
        
        sys.stdout.flush()
