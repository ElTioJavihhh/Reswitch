import sys
import os
import math
import ctypes
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk
import winshell
import logging
from io import BytesIO

def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta a un recurso. Esta es la versión definitiva y robusta.
    """
    try:
        # Ruta cuando está empaquetado con PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Ruta en desarrollo (la raíz del proyecto)
        base_path = os.path.abspath(".")
        # La carpeta de assets está dentro de 'src' en desarrollo
        return os.path.join(base_path, 'src', 'assets', relative_path)
    
    # En producción, PyInstaller pone los assets en una carpeta al lado del exe
    return os.path.join(base_path, 'assets', relative_path)

def calculate_aspect_ratio(width: int, height: int) -> str:
    if width == 0 or height == 0: return ""
    gcd = math.gcd(width, height)
    return f"({width // gcd}:{height // gcd})"

def set_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except AttributeError:
        try: ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError: pass

def get_icon_from_exe(exe_path: str, size: Tuple[int, int] = (32, 32)) -> ctk.CTkImage:
    if not exe_path or not os.path.exists(exe_path):
        return create_placeholder_icon(size=size)
    try:
        ico_data = winshell.get_icon(exe_path, winshell.IconSize.large)
        
        if not ico_data:
            return create_placeholder_icon(size=size)

        with BytesIO(ico_data) as bio:
            img = Image.open(bio)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    except Exception as e:
        logging.error(f"Error extracting icon from {exe_path}: {e}")
        return create_placeholder_icon(size=size)

def create_placeholder_icon(size: Tuple[int, int] = (32, 32)) -> ctk.CTkImage:
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius=4, fill="#4a4a4a")
    try:
        font_path = resource_path("seguisb.ttf") # Busca la fuente en los assets
        font = ImageFont.truetype(font_path, size[0] // 2)
    except IOError:
        font = ImageFont.load_default()
    draw.text((size[0]/2, size[1]/2), "?", fill="#ffffff", anchor="ms", font=font)
    return ctk.CTkImage(light_image=image, dark_image=image, size=size)