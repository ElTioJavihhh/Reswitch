import os
import re
import winreg
from typing import Dict, List, Optional
import logging

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)

class SteamProvider(BaseProvider):
    """Encuentra juegos de Steam analizando los archivos de manifiesto."""

    @property
    def name(self) -> str:
        return "Steam"

    def _find_steam_path(self) -> Optional[str]:
        # ... (código sin cambios)
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            winreg.CloseKey(key)
            return steam_path.replace("/", "\\")
        except Exception:
            return None

    def _parse_library_folders(self, vdf_path: str) -> List[str]:
        # ... (código sin cambios)
        libraries = []
        if not os.path.exists(vdf_path): return []
        try:
            with open(vdf_path, 'r', encoding='utf-8') as f: content = f.read()
            matches = re.findall(r'"path"\s+"([^"]+)"', content)
            for path in matches: libraries.append(os.path.normpath(path.replace('\\\\', '\\')))
        except Exception as e: logger.error(f"Error al parsear {vdf_path}: {e}")
        return libraries

    def _find_main_executable(self, game_path: str) -> Optional[str]:
        """Intenta encontrar el ejecutable principal en la carpeta de un juego."""
        if not os.path.isdir(game_path):
            return None
        
        all_exes = [os.path.join(root, file) for root, _, files in os.walk(game_path) for file in files if file.lower().endswith('.exe')]
        if not all_exes:
            return None

        # --- CORRECCIÓN: Se añaden más términos a la lista de ignorados ---
        ignore_list = [
            'crash', 'report', 'launcher', 'setup', 'redist', 'dx', 'vcredist',
            'dotnet', 'unins', 'vconsole', 'activationui'
        ]
        
        filtered_exes = [exe for exe in all_exes if not any(sub in os.path.basename(exe).lower() for sub in ignore_list)]
        
        exes_to_check = filtered_exes if filtered_exes else all_exes
        if not exes_to_check:
            return None

        try:
            # La heurística más común es asumir que el .exe más grande es el juego.
            return max(exes_to_check, key=os.path.getsize)
        except (IOError, FileNotFoundError):
            return None

    def get_installed_games(self) -> Dict[str, str]:
        # ... (código sin cambios)
        games = {}
        steam_path = self._find_steam_path()
        if not steam_path: return {}
        library_folders_vdf = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
        libraries = self._parse_library_folders(library_folders_vdf)
        libraries.append(steam_path)
        for library in set(libraries):
            steamapps_path = os.path.join(library, 'steamapps')
            if not os.path.isdir(steamapps_path): continue
            for item in os.listdir(steamapps_path):
                if item.startswith('appmanifest_') and item.endswith('.acf'):
                    try:
                        acf_path = os.path.join(steamapps_path, item)
                        with open(acf_path, 'r', encoding='utf-8') as f: content = f.read()
                        name_match = re.search(r'"name"\s+"([^"]+)"', content)
                        installdir_match = re.search(r'"installdir"\s+"([^"]+)"', content)
                        if name_match and installdir_match:
                            name = name_match.group(1)
                            installdir = installdir_match.group(1)
                            game_path = os.path.join(steamapps_path, 'common', installdir)
                            if exe_path := self._find_main_executable(game_path):
                                games[name] = exe_path
                    except Exception as e: logger.error(f"Error procesando el archivo ACF {item}: {e}")
        return games