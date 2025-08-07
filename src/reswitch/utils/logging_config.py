import logging
import logging.config
import os
from reswitch.config import LOG_FILE, APP_DATA_DIR

def setup_logging():
    """
    Configura el sistema de logging para la aplicación.
    Utiliza dictConfig para una configuración flexible.
    Crea un log que rota por tamaño y escribe en un archivo en APPDATA.
    """
    os.makedirs(APP_DATA_DIR, exist_ok=True)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detailed',
                'filename': LOG_FILE,
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 3,
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            '': {  # Logger raíz
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'pystray': { # Silenciar un poco el log de pystray si es necesario
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': False,
            },
             'PIL': { # Silenciar logs de Pillow
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': False,
            }
        }
    }

    logging.config.dictConfig(logging_config)
    logging.info("Sistema de logging configurado correctamente.")