# En: src/reswitch/core/engine.py

import logging
from typing import List, Dict, Type

from ..providers.base_provider import BaseProvider
from ..providers.steam_provider import SteamProvider
# --- CORRECCIÓN: Se usa "GogProvider" en lugar de "GOGProvider" ---
from ..providers.gog_provider import GogProvider
from ..providers.epic_provider import EpicProvider

logger = logging.getLogger(__name__)

class GameScannerEngine:
    """
    Motor encargado de escanear el sistema en busca de juegos
    utilizando diferentes proveedores (Steam, GOG, etc.).
    """
    def __init__(self):
        self.providers: List[BaseProvider] = [
            SteamProvider(),
            # --- CORRECCIÓN: Se usa "GogProvider()" en lugar de "GOGProvider()" ---
            GogProvider(),
            EpicProvider()
        ]
        logger.info(f"Motor de escaneo inicializado con {len(self.providers)} proveedores.")

    def scan_all(self) -> Dict[str, str]:
        """
        Escanea todos los juegos de todos los proveedores.
        Devuelve un diccionario con {nombre_juego: ruta_ejecutable}.
        """
        all_games = {}
        logger.info("Iniciando escaneo de juegos...")
        for provider in self.providers:
            try:
                logger.info(f"Escaneando con el proveedor: {provider.name}")
                games = provider.get_installed_games()
                all_games.update(games)
                logger.info(f"Se encontraron {len(games)} juegos con {provider.name}.")
            except Exception as e:
                logger.error(f"Error al escanear con el proveedor {provider.name}: {e}", exc_info=True)
        
        logger.info(f"Escaneo completado. Se encontraron un total de {len(all_games)} juegos.")
        return all_games