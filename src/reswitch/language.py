# --- Gestor de Idioma ---
# (Este es tu código original, que es bastante bueno. Lo movemos a su propio módulo)
translations = {
    "en": {
        "nav_home": "Home", "nav_profiles": "Profiles", "nav_settings": "Settings", "nav_support": "❤️ Support",
        "home_title": "Game Profile Manager", "home_subtitle": "Manage your profiles and settings for an optimal gaming experience.",
        "quick_switch_title": "Quick Switch", "desktop_res_label": "Desktop Resolution", "game_res_label": "Game Resolution",
        "switch_button": "Switch Resolution", "profiles_title": "Game Profiles",
        "add_profile_button": "Add New Profile", "fullscreen_warning": "For best results, use 'Borderless' or 'Fullscreen Windowed' mode in your games to avoid black screens.",
        "settings_title": "General Settings", "startup_options_label": "Startup Options", "start_with_windows": "Start with Windows",
        "hotkeys_label": "Keyboard Shortcuts", "desktop_hotkey": "Desktop Mode", "game_hotkey": "Game Mode",
        "language_label": "Language", "save_settings_button": "Save Changes", "status_ready": "Ready",
        "status_res_changed": "Resolution changed to {res} on {monitor}", "status_admin_needed": "Error: Administrator permissions needed",
        "status_res_unsupported": "Error: Resolution {res} not supported", "status_settings_saved": "Settings saved",
        "status_hotkey_error": "Error setting hotkeys: {e}", "status_startup_error": "Error modifying startup: {e}",
        "profile_editor_title": "Game Profile Editor", "executable_path_label": "Executable Path (.exe):",
        "game_resolution_label": "Resolution for this game:", "save_profile_button": "Save Profile", "select_executable_title": "Select Executable",
        "delete_button": "Delete", "edit_button": "Edit", "no_profiles_text": "No profiles yet!", "no_profiles_subtext": "Add a profile or scan for games to get started.",
        "list_header_game": "GAME", "list_header_resolution": "RESOLUTION",
        "appearance_label": "Appearance", "appearance_mode_label": "Theme", "monitor_label": "Target Monitor",
        "theme_light": "Light", "theme_dark": "Dark", "theme_system": "System",
        "monitor_profile_label": "Monitor for this game:", "hotkey_capture_title": "Set Hotkey", "hotkey_capture_text": "Press the desired key combination...",
        "tray_show": "Show Reswitch!", "tray_exit": "Exit", "tray_desktop_mode": "Switch to Desktop Mode", "tray_game_mode": "Switch to Game Mode",
        "scan_games_button": "Scan for Games", "game_scanner_title": "Game Scanner", "scanner_status_scanning": "Scanning for games, please wait...",
        "scanner_status_found": "Found {count} new games. Select which ones to add:", "scanner_add_selected_button": "Add Selected Profiles",
        "scanner_no_new_games": "No new games found or all are already in your profiles.",
        "tray_notice_title": "Reswitch! is running", "tray_notice_text": "Reswitch! will continue to run in the system tray. You can open it again from there.", "tray_notice_button": "Got it"
    },
    "es": {
        "nav_home": "Inicio", "nav_profiles": "Perfiles", "nav_settings": "Ajustes", "nav_support": "❤️ Apoyar",
        "home_title": "Gestor de Perfiles de Juego", "home_subtitle": "Gestiona tus perfiles y configuraciones para una experiencia de juego óptima.",
        "quick_switch_title": "Cambio Rápido", "desktop_res_label": "Resolución Escritorio", "game_res_label": "Resolución Juego",
        "switch_button": "Cambiar Resolución", "profiles_title": "Perfiles de Juego",
        "add_profile_button": "Añadir Nuevo Perfil", "fullscreen_warning": "Para mejores resultados, usa el modo 'Ventana sin Bordes' o 'Pantalla Completa en Ventana' en tus juegos para evitar pantallazos negros.",
        "settings_title": "Configuración General", "startup_options_label": "Opciones de Inicio", "start_with_windows": "Iniciar con Windows",
        "hotkeys_label": "Atajos de Teclado", "desktop_hotkey": "Modo Escritorio", "game_hotkey": "Modo Juego",
        "language_label": "Idioma", "save_settings_button": "Guardar Cambios", "status_ready": "Listo",
        "status_res_changed": "Resolución cambiada a {res} en {monitor}", "status_admin_needed": "Error: Se necesitan permisos de administrador",
        "status_res_unsupported": "Error: Resolución {res} no soportada", "status_settings_saved": "Ajustes guardados",
        "status_hotkey_error": "Error al configurar atajos: {e}", "status_startup_error": "Error al modificar inicio: {e}",
        "profile_editor_title": "Editor de Perfiles de Juego", "executable_path_label": "Ruta del ejecutable (.exe):",
        "game_resolution_label": "Resolución para este juego:", "save_profile_button": "Guardar Perfil", "select_executable_title": "Selecciona el ejecutable",
        "delete_button": "Eliminar", "edit_button": "Editar", "no_profiles_text": "¡Aún no hay perfiles!", "no_profiles_subtext": "Añade un perfil o busca juegos para empezar.",
        "list_header_game": "JUEGO", "list_header_resolution": "RESOLUCIÓN",
        "appearance_label": "Apariencia", "appearance_mode_label": "Tema", "monitor_label": "Monitor de Destino",
        "theme_light": "Claro", "theme_dark": "Oscuro", "theme_system": "Sistema",
        "monitor_profile_label": "Monitor para este juego:", "hotkey_capture_title": "Definir Atajo", "hotkey_capture_text": "Presiona la combinación de teclas deseada...",
        "tray_show": "Mostrar Reswitch!", "tray_exit": "Salir", "tray_desktop_mode": "Cambiar a Modo Escritorio", "tray_game_mode": "Cambiar a Modo Juego",
        "scan_games_button": "Buscar Juegos", "game_scanner_title": "Buscador de Juegos", "scanner_status_scanning": "Buscando juegos, por favor espera...",
        "scanner_status_found": "Se encontraron {count} juegos nuevos. Selecciona cuáles añadir:", "scanner_add_selected_button": "Añadir Perfiles Seleccionados",
        "scanner_no_new_games": "No se encontraron juegos nuevos o ya están todos en tus perfiles.",
        "tray_notice_title": "Reswitch! se está ejecutando", "tray_notice_text": "Reswitch! continuará ejecutándose en la bandeja del sistema. Puedes abrirlo de nuevo desde allí.", "tray_notice_button": "Entendido"
    },
    "zh": { # Omitido por brevedad
    }
}

class LanguageManager:
    def __init__(self, language: str = "en"):
        self.language = language

    def get(self, key: str, **kwargs) -> str:
        """Obtiene una cadena de traducción para la clave dada."""
        return translations.get(self.language, translations["en"]).get(key, key).format(**kwargs)

    def set_language(self, language: str):
        """Establece el idioma actual."""
        self.language = language