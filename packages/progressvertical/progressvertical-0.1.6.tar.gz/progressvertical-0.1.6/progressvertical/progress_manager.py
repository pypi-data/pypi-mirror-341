from .color_manager import ColorManager
from .interfaces import ProgressRenderer

class ProgressVertical:
    def __init__(self, renderer: ProgressRenderer):
        self.stages = []
        self.renderer = renderer

    def add_stage(self, label: str, total: int = 100, **color_kwargs):
        self.stages.append({
            "label": label,
            "total": total,
            "current": 0,
            "complete": False,
            "colors": {
                "fore": ColorManager.get_color("fore", color_kwargs.get("fore_color")),
                "back": ColorManager.get_color("back", color_kwargs.get("back_color")),
                "style": ColorManager.get_color("style", color_kwargs.get("style"))
            }
        })

    def update(self, stage_idx: int, value: int):
        stage = self.stages[stage_idx]
        stage["current"] = value
        stage["complete"] = (value >= stage["total"])
        self.renderer.render(self.stages)

    def start(self):
        self.renderer.render(self.stages)

    def end(self):
        self.renderer.cleanup()
