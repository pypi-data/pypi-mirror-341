from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager

ColorManager.init_colorama()
renderer = VerticalProgressRenderer(height=15)
manager = ProgressManager(renderer)
print("progress")

iterable = [1, 2, 3, 4, 5,'bebel',True,[1,2,3,4,5]]

for i in manager.track(iterable, label="1", fore_color="blue"):__import__('time').sleep(0.6)


for e in manager.track(iterable, label="2", fore_color="red"):__import__('time').sleep(0.4)


for f in manager.track(iterable, label="3", fore_color="blue"):__import__('time').sleep(0.5)
for g in manager.track(iterable, label="4", fore_color="yellow"):__import__('time').sleep(0.9)


for item in manager.track(range(100), label="title", fore_color="green"):
  if(item == 35):
   break

print("======================================")
