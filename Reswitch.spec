# -*- mode: python ; coding: utf-8 -*-

# Este archivo.spec le da a PyInstaller un control mucho más fino sobre la compilación.
# Es la forma recomendada para proyectos complejos.

block_cipher = None

# --- Recopilación de archivos de datos ---
# Copia el icono a la raíz del bundle, donde la función resource_path lo buscará.
datas = [('src/assets', 'assets')]

a = Analysis(
    ['run.py'],
    binaries=[],     # <--- CORREGIDO
    datas=datas,
    hiddenimports=[
        'pystray._win32',
        'win32timezone', # A menudo necesario para que pywin32 funcione correctamente
        'darkdetect'     # A menudo necesario para que customtkinter detecte el tema del sistema
    ],
    hookspath=[],    # <--- CORREGIDO
    hooksconfig={},
    runtime_hooks=[],# <--- CORREGIDO
    excludes=[],     # <--- CORREGIDO
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- Configuración del ejecutable ---
exe = EXE(
    pyz,
    a.scripts,
    # <--- CORREGIDO (se eliminó la coma extra)
    exclude_binaries=True,
    name='Reswitch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprime los binarios. Requiere que UPX esté instalado y en el PATH del sistema.
    console=False, # False para una aplicación de GUI (sin ventana de consola)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/reswitch_icon.ico', # <--- RUTA CORREGIDA
)

# --- Creación del directorio final ---
# Agrupa el.exe y todas sus dependencias en una sola carpeta.
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[], # <--- CORREGIDO
    name='Reswitch', # Nombre de la carpeta de salida en el directorio 'dist'
)