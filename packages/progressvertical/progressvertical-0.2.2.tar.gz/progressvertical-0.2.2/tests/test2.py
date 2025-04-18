from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager

ColorManager.init_colorama()
renderer = VerticalProgressRenderer(height=5,spacing=5)
manager = ProgressManager(renderer)

name_list = ["Mel", "Bianca", "Melissa","Piqueno","Netuno","Merenga"]
numbers_list = [10, 20, 30, 40, 50]
color_list = ["vermelho", "verde", "azul", "amarelo"]
print("starting")

for name in manager.track(name_list, label="Names", fore_color="ciano"): __import__('time').sleep(0.4)
for number in manager.track(numbers_list, label="Number", fore_color="verde"): __import__('time').sleep(0.3)
for color in manager.track(color_list, label="Color", fore_color="magenta"): __import__('time').sleep(0.2)
print("finished")

