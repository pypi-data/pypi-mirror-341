import time
from math import ceil
from .color_manager import ColorManager
from .interfaces import ProgressRenderer

class ProgressManager:

    def __init__(self, renderer: ProgressRenderer):
        self.stages = []
        self.renderer = renderer

    def add_stage(
        self,
        label: str,
        duration: float = 1.0,
        fore_color: str = None,
        back_color: str = None,
        style: str = None,
    ):
        self.stages.append({
            'label': label,
            'duration': duration,
            'progress': 0,
            'complete': False,
            'fore_color': ColorManager.get_fore_color(fore_color),
            'back_color': ColorManager.get_back_color(back_color),
            'style': ColorManager.get_style(style),
        })

    def start_animation(self, update_interval=0.1):
        try:
            while not all(stage['complete'] for stage in self.stages):
                self._update_progress()
                self.renderer.render(self.stages)
                time.sleep(update_interval)
        except KeyboardInterrupt:
            print("\nProgresso interrompido pelo usuário!")

    def _update_progress(self):
        for stage in self.stages:
            if not stage['complete']:
                stage['progress'] += 1
                if stage['progress'] >= self.renderer.height:
                    stage['complete'] = True
                    stage['progress'] = self.renderer.height
