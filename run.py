# En: run.py (en la raíz del proyecto)

import sys
import os

# Esto añade la carpeta 'src' al path de Python para que pueda encontrar tu paquete 'reswitch'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Ahora podemos importar y ejecutar el punto de entrada de forma segura
from reswitch.__main__ import entry_point

if __name__ == '__main__':
    entry_point()