import os
import winreg
from typing import Dict
import logging

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)

class GogProvider(BaseProvider):
    """Encuentra juegos de GOG consultando el registro de Windows."""

    # --- CORRECCIÓN: Se añade la propiedad 'name' que faltaba ---
    @property
    def name(self) -> str:
        return "GOG"

    REG_PATH = r"SOFTWARE\WOW6432Node\GOG.com\Games"

    def get_installed_games(self) -> Dict[str, str]:
        """Escanea el registro en busca de juegos instalados por GOG Galaxy."""
        games = {}
        try:
            main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.REG_PATH, 0, winreg.KEY_READ)
            logger.debug(f"Clave de registro de GOG encontrada en: HKLM\\{self.REG_PATH}")
        except FileNotFoundError:
            logger.info("Proveedor de GOG: No se encontró la clave de registro principal.")
            return {}
        except Exception as e:
            logger.error(f"Error al abrir la clave de registro de GOG: {e}")
            return {}

        try:
            i = 0
            while True:
                try:
                    game_id = winreg.EnumKey(main_key, i)
                    game_key_path = os.path.join(self.REG_PATH, game_id).replace("/", "\\")
                    
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, game_key_path, 0, winreg.KEY_READ) as game_key:
                        game_name, _ = winreg.QueryValueEx(game_key, "gameName")
                        install_path, _ = winreg.QueryValueEx(game_key, "path")
                        exe_name, _ = winreg.QueryValueEx(game_key, "exe")
                        
                        full_exe_path = os.path.join(install_path, exe_name)
                        
                        if game_name and os.path.exists(full_exe_path):
                            logger.info(f"Juego de GOG detectado: '{game_name}' en '{full_exe_path}'")
                            games[game_name] = full_exe_path
                except OSError:
                    break
                finally:
                    i += 1
        finally:
            winreg.CloseKey(main_key)
            
        return games