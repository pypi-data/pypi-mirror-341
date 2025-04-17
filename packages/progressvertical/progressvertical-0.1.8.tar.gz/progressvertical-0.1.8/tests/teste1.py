from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager
import time

ColorManager.init_colorama()
renderer = VerticalProgressRenderer(height=5)
manager = ProgressManager(renderer)
print("progresso")
lista = [1, 2, 3, 4, 5]

for numero in manager.track(lista, label="Números", fore_color="green"):
    print(f"Processando: {numero}")

print("Processo concluído!")
