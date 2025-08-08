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

logger = logging.getLogger(__name__)

def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta a un recurso. Esta es la versión definitiva y robusta.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        logger.debug(f"Running in PyInstaller bundle, _MEIPASS: {base_path}")
    except AttributeError:
        # Not in a PyInstaller bundle
        base_path = os.path.abspath(".")
        logger.debug(f"Running in development, base_path: {base_path}")
        final_path = os.path.join(base_path, 'src', 'assets', relative_path)
        logger.debug(f"Resource path in dev: {final_path}")
        return final_path

    final_path = os.path.join(base_path, 'assets', relative_path)
    logger.debug(f"Resource path in bundle: {final_path}")
    return final_path

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
    logger.debug(f"Attempting to get icon for exe: '{exe_path}'")
    if not exe_path or not os.path.exists(exe_path):
        logger.warning(f"Exe path does not exist or is empty: '{exe_path}'. Returning placeholder.")
        return create_placeholder_icon(size=size)
    try:
        ico_data = winshell.get_icon(exe_path, winshell.IconSize.large)
        
        if not ico_data:
            logger.warning(f"winshell.get_icon returned no data for '{exe_path}'. Returning placeholder.")
            return create_placeholder_icon(size=size)

        logger.debug(f"Successfully got icon data for '{exe_path}'. Creating CTkImage.")
        with BytesIO(ico_data) as bio:
            img = Image.open(bio)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    except Exception as e:
        logger.error(f"Error extracting icon from '{exe_path}': {e}", exc_info=True)
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