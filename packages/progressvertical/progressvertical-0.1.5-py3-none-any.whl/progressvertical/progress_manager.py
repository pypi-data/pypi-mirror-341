from .color_manager import ColorManager

class ProgressManager:
    
    def __init__(self, renderer):
        self.stages = []
        self.renderer = renderer
    
    def add_task(self, label: str, total: int = 100, **color_kwargs):
        self.stages.append({
            "label": label,
            "total": total,
            "progress": 0,
            "complete": False,
            "colors": {
                "fore": ColorManager.get_color("fore", color_kwargs.get("fore_color", "")),
                "back": ColorManager.get_color("back", color_kwargs.get("back_color", "")),
                "style": ColorManager.get_color("style", color_kwargs.get("style", ""))
            }
        })
    
    def update(self, task_idx: int, increment: int = 1):
        task = self.stages[task_idx]
        task["progress"] += increment
        task["complete"] = (task["progress"] >= task["total"])
        self.renderer.render(self.stages)
    
    def start(self):
        self.renderer.render(self.stages)
    
    def end(self):
        self.renderer.cleanup()
