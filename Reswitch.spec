# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# --- Recopilación de archivos de datos ---
# Copia los assets y el icono.
datas = [('src/assets', 'assets')]

# --- Configuración del Análisis ---
# Aquí le decimos a PyInstaller dónde encontrar todo.
a = Analysis(
    ['run.py'],
    # Indica a PyInstaller que la carpeta 'src' contiene código fuente.
    pathex=[os.path.abspath('src')],
    binaries=[],
    datas=datas,
    # Lista de módulos que PyInstaller podría no encontrar por sí solo.
    hiddenimports=[
        'pystray._win32',
        'win32timezone',
        'darkdetect',
        'winshell'  # Importante mantenerlo aquí.
    ],
    # Ruta a la carpeta que contiene nuestros hooks personalizados.
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- Configuración del Ejecutable ---
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='Reswitch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False para una aplicación GUI (sin ventana de consola)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/reswitch_icon.ico',
)

# --- Creación del Directorio Final ---
# Agrupa el .exe y todas sus dependencias en una sola carpeta.
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Reswitch',
)
