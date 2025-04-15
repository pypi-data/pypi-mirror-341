import sys
from colorama import Cursor

class VerticalRenderer:
    def __init__(self, height: int = 10):
        self.height = height
        self._lines_used = 0
    
    def render(self, progress_data):
        sys.stdout.write(Cursor.UP(self._lines_used) + Cursor.POS(0))
        
        output_lines = []
        for task in progress_data:
            percent = min(100, (task["progress"] / task["total"]) * 100)
            filled = int(self.height * (percent / 100))
            
            bar = (
                task["colors"]["fore"] + 
                task["colors"]["style"] + 
                "▓" * filled + 
                "░" * (self.height - filled) + 
                ColorManager.RESET
            )
            
            # Linha de status
            status_line = f"{task['label']}: {task['progress']}/{task['total']} ({percent:.1f}%)"
            output_lines.append(f"{bar} {status_line}")
        
        # Exibe tudo de uma vez
        output = "\n".join(output_lines)
        self._lines_used = len(output_lines)
        print(output, end="", flush=True)
    
    def cleanup(self):
        print("\n" * self._lines_used)
