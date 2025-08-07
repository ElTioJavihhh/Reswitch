import os
import json
from typing import Dict, Optional
import logging

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)

class EpicProvider(BaseProvider):
    """Encuentra juegos de Epic Games analizando los manifiestos en ProgramData."""

    # --- CORRECCIÓN: Se añade la propiedad 'name' que faltaba ---
    @property
    def name(self) -> str:
        return "Epic Games"

    MANIFESTS_PATH = os.path.join(os.getenv('ProgramData', 'C:\\ProgramData'), 'Epic', 'EpicGamesLauncher', 'Data', 'Manifests')

    def get_installed_games(self) -> Dict[str, str]:
        """Escanea el directorio de manifiestos de Epic Games."""
        games = {}
        if not os.path.isdir(self.MANIFESTS_PATH):
            logger.info("Proveedor de Epic: El directorio de manifiestos no existe.")
            return {}

        logger.debug(f"Escaneando manifiestos de Epic en: {self.MANIFESTS_PATH}")
        for item_file in os.listdir(self.MANIFESTS_PATH):
            if item_file.endswith('.item'):
                manifest_path = os.path.join(self.MANIFESTS_PATH, item_file)
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    game_name = data.get('DisplayName')
                    install_location = data.get('InstallLocation')
                    executable = data.get('LaunchExecutable')

                    if game_name and install_location and executable:
                        exe_path = os.path.join(install_location, executable)
                        if os.path.exists(exe_path):
                            logger.info(f"Juego de Epic detectado: '{game_name}' en '{exe_path}'")
                            games[game_name] = exe_path
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    logger.error(f"Error al parsear el manifiesto de Epic {manifest_path}: {e}")
        
        return games