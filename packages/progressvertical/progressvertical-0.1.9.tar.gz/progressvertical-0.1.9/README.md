**ProgressVertical** is a Python library for displaying vertical progress bars for command-line interface (CLI) applications.  
Designed with a focus on usability and customization, allowing the creation of multi-stage progress animations with configurable colors, styles, and durations, inspired by another library [_progressbar_](https://pypi.org/project/progressbar/).



## Installation:

```pip
pip install progressvertical

```
### Usage Example

```python
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

```
## Example 1

```python
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
```


## Example 2
```python
from progressvertical import ProgressManager, VerticalProgressRenderer, ColorManager

ColorManager.init_colorama()
renderer = VerticalProgressRenderer(height=26)
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
```
[![ProgressVertical](https://img.shields.io/badge/ProgressVertical-%200.1.8-0073B7?style=for-the-badge&logo=python)](https://pypi.org/project/progressvertical/)
