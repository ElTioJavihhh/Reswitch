from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class GameProfile:
    """Representa el perfil de un juego con su configuración específica."""
    path: str
    res: str
    monitor: str
    name: Optional[str] = None
    icon: Optional[object] = None # Puede ser un CTkImage

@dataclass
class AppSettings:
    """Almacena toda la configuración de la aplicación."""
    language: str = "en"
    appearance_mode: str = "System"
    target_monitor: Optional[str] = None
    desktop_res: Optional[str] = None
    game_res: Optional[str] = None
    start_with_windows: bool = False
    hotkey_desktop: str = "ctrl+alt+1"
    hotkey_game: str = "ctrl+alt+2"
    tray_notification_shown: bool = False
    game_profiles: List[GameProfile] = field(default_factory=list)