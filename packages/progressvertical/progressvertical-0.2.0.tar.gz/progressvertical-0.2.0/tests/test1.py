from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager
import time

ColorManager.init_colorama()
renderer = VerticalProgressRenderer(height=5)
manager = ProgressManager(renderer)

list = [1, 2, 3, 4, 5]

for number in manager.track(list, label="Number", fore_color="green"):
    print(f"Number: {number}")

