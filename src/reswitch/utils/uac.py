import ctypes
import sys
import os
import logging

logger = logging.getLogger(__name__)

def is_running_as_admin() -> bool:
    """
    Comprueba de forma fiable si el script se está ejecutando con privilegios de administrador.
    IsUserAnAdmin() no es fiable en sistemas con UAC. CheckTokenMembership es el método correcto.
    """
    if os.name!= 'nt':
        # En sistemas no-Windows, se comprueba si el UID es 0 (root).
        return os.geteuid() == 0

    try:
        import win32security
        admin_sid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid, None)
        is_admin = win32security.CheckTokenMembership(None, admin_sid)
        logger.debug(f"Comprobación de admin con CheckTokenMembership: {'Sí' if is_admin else 'No'}")
        return is_admin
    except (ImportError, AttributeError) as e:
        logger.warning(f"pywin32 no está instalado o falta un componente. Volviendo a IsUserAnAdmin. Error: {e}")
        # Fallback al método menos fiable si pywin32 no está disponible.
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()!= 0
        except Exception as ex:
            logger.error(f"No se pudo comprobar el estado de administrador: {ex}")
            return False

def request_elevation():
    """
    Relanza el script actual solicitando privilegios de administrador a través de UAC.
    El script original debe salir después de llamar a esta función.
    """
    if os.name!= 'nt':
        logger.error("La solicitud de elevación de privilegios solo es compatible con Windows.")
        return

    try:
        # Usamos ShellExecuteW para solicitar la elevación con el verbo "runas".
        result = ctypes.windll.shell32.ShellExecuteW(
            None,           # hwnd
            "runas",        # lpOperation: "runas" activa el diálogo de UAC
            sys.executable, # lpFile: el ejecutable de Python
            " ".join(sys.argv), # lpParameters: los mismos argumentos con los que se llamó al script
            None,           # lpDirectory
            1               # nShowCmd: SW_SHOWNORMAL
        )
        
        # Un resultado > 32 indica éxito.
        if result <= 32:
            logger.error(f"Falló la solicitud de elevación de privilegios. Código de error de ShellExecuteW: {result}")
            raise ctypes.WinError()
        else:
            logger.info("Solicitud de elevación enviada correctamente. El proceso actual saldrá.")

    except Exception as e:
        logger.critical(f"Error crítico al intentar elevar privilegios: {e}", exc_info=True)
        # Mostrar un mensaje de error al usuario si falla la elevación
        ctypes.windll.user32.MessageBoxW(
            None,
            "No se pudieron obtener los permisos de administrador necesarios para continuar. La aplicación se cerrará.",
            "Error de Permisos",
            0x10 # MB_ICONERROR
        )
        sys.exit(1)