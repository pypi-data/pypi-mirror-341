from progressvertical import ProgressManager, VerticalProgressRenderer, ForLoopTracker

# Exemplo básico
renderer = VerticalProgressRenderer(height=10)
manager = ProgressManager(renderer)
tracker = ForLoopTracker(manager)

for item in tracker.track(range(100), label="Processando", fore_color="green"):
    __import__('time').sleep(0.3)
