from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager

ColorManager.init_colorama()
renderer = VerticalProgressRenderer(height=5,spacing=5)
manager = ProgressManager(renderer)

lista_nomes = ["Mel", "Bianca", "Melissa","Piqueno"]
lista_numeros = [10, 20, 30, 40, 50]
lista_cores = ["vermelho", "verde", "azul", "amarelo"]
print("iniciado processo")

for nome in manager.track(lista_nomes, label="Nomes", fore_color="ciano"):
    __import__('time').sleep(0.4)
    for numero in manager.track(lista_numeros, label="Números", fore_color="verde"):
        __import__('time').sleep(0.3)
        for cor in manager.track(lista_cores, label="Cores", fore_color="magenta"):
            __import__('time').sleep(0.2)
print("finalizado")
