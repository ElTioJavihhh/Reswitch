import os

# --- Constantes de la Aplicación ---
APP_NAME = "Reswitch!"
APP_AUTHOR = "YourName" # Cambia esto a tu nombre o el de tu organización
APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)
SETTINGS_FILE = os.path.join(APP_DATA_DIR, 'settings.json')
LOG_FILE = os.path.join(APP_DATA_DIR, 'app.log')

# --- Constantes de la UI ---
ANIMATION_DURATION_MS = 250
ANIMATION_STEPS = 20
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 700

# --- Temas de la UI ---
THEMES = {
    "Light": {
        "accent": "#fbc02d",
        "accent_hover": "#e0a818",
        "text_on_accent": "#000000",
        "text": "#000000",
        "text_secondary": "gray50",
        "bg": "#ffffff",
        "bg_secondary": "#f0f0f0",
        "frame_bg": "#f9f9f9",
        "frame_border": "#e0e0e0",
        "hover": "#eeeeee",
        "button": "#e0e0e0",
        "button_hover": "#cccccc",
        "entry_border": "#cccccc",
        "error": "#D32F2F",
        "success": "#009688",
    },
    "Dark": {
        "accent": "#fbc02d",
        "accent_hover": "#e0a818",
        "text_on_accent": "#000000",
        "text": "#ffffff",
        "text_secondary": "gray65",
        "bg": "#1c1c1c",
        "bg_secondary": "#282828",
        "frame_bg": "#2b2b2b",
        "frame_border": "#3c3c3c",
        "hover": "#383838",
        "button": "#444444",
        "button_hover": "#555555",
        "entry_border": "#555555",
        "error": "#e74c3c",
        "success": "#2ecc71",
    }
}