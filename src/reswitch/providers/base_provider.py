from abc import ABC, abstractmethod
from typing import Dict

class BaseProvider(ABC):
    """Clase base abstracta para todos los proveedores de juegos."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre del proveedor (ej. 'Steam')."""
        pass

    # --- CORRECCIÓN: El método abstracto debe llamarse 'get_installed_games' ---
    @abstractmethod
    def get_installed_games(self) -> Dict[str, str]:
        """
        Busca y devuelve un diccionario de juegos instalados.
        Formato: { 'Nombre del Juego': 'ruta/al/ejecutable.exe' }
        """
        pass