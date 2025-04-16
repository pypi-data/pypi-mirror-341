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

[![ProgressVertical](https://img.shields.io/badge/ProgressVertical-%200.1.7-0073B7?style=for-the-badge&logo=python)](https://pypi.org/project/progressvertical/)
