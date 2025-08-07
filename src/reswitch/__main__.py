# En: src/reswitch/__main__.py

import sys
import ctypes
import traceback
from .ui.app import ResolutionSwitcherApp
from .utils import uac, logging_config
from .config import APP_NAME

def main_app_logic():
    """
    Punto de entrada principal de la aplicación.
    Configura el logging y lanza la GUI.
    """
    logging_config.setup_logging()
    
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)
    except AttributeError:
        pass

    app = ResolutionSwitcherApp()
    app.mainloop()

def show_error_and_exit(title: str, message: str):
    """Muestra un cuadro de diálogo de error y cierra la aplicación."""
    ctypes.windll.user32.MessageBoxW(None, message, title, 0x10)
    sys.exit(1)

def entry_point():
    """
    Punto de entrada que gestiona los permisos antes de lanzar la app.
    """
    try:
        if not uac.is_running_as_admin():
            print("Se necesitan privilegios de administrador. Intentando relanzar...")
            uac.request_elevation()
            sys.exit(0)
        else:
            main_app_logic()
    except Exception as e:
        error_message = f"Ha ocurrido un error crítico irrecuperable.\n\nError: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        show_error_and_exit(f"{APP_NAME} - Error Crítico", error_message)

if __name__ == "__main__":
    entry_point()