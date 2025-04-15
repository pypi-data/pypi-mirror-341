import sys
from .interfaces import ProgressRenderer
from .color_manager import ColorManager

class VerticalProgressRenderer(ProgressRenderer):

    def __init__(self, height=10, spacing=6):
        self.height = height
        self.spacing = spacing
        self.bar_width = 3
        self._prepare_display_area()

    def _prepare_display_area(self):
        print("\n" * (self.height + 3), end='')
        sys.stdout.write(f"\033[{self.height + 3}F")
        sys.stdout.flush()

    def render(self, progress_data: list) -> None:
        sys.stdout.write(f"\033[{self.height + 3}H\033[J")

        for line in range(self.height, 0, -1):
            for idx, data in enumerate(progress_data):
                space = ' ' * (self.spacing if idx > 0 else 2)
                filled = line <= data['progress']
                color = data.get('fore_color', '') + data.get('back_color', '') + data.get('style', '')
                block = color + '▓▓▓' + ColorManager.RESET if filled else '   '
                sys.stdout.write(space + block)
            sys.stdout.write('\n')

        labels = []
        for idx, data in enumerate(progress_data):
            total_space = self.bar_width + (self.spacing if idx > 0 else 2)
            labels.append(data['label'].center(total_space))
        print(''.join(labels))

        percentages = []
        for idx, data in enumerate(progress_data):
            total_space = self.bar_width + (self.spacing if idx > 0 else 2)
            pct = min(100, (data['progress'] / self.height) * 100)
            color = data.get('fore_color', '') + data.get('style', '')
            percentages.append(color + f"{pct:>3.0f}%".center(total_space) + ColorManager.RESET)
        print(''.join(percentages))
        sys.stdout.flush()
