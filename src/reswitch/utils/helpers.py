import sys
import os
import math
import ctypes
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk
import win32gui
import win32ui
import win32con
import win32api
import logging

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
        # Note: ExtractIconEx returns a list of handles
        large_icons, small_icons = win32gui.ExtractIconEx(exe_path, 0, 1)

        # We prefer large icons
        target_icons = large_icons if large_icons else small_icons
        
        if not target_icons:
            logger.warning(f"No icons found in '{exe_path}'.")
            return create_placeholder_icon(size=size)

        h_icon = target_icons[0]

        # Get icon info
        icon_info = win32gui.GetIconInfo(h_icon)

        # Get the icon's bitmap handle
        h_bitmap = icon_info[4]

        # Create a device context
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        h_mem_dc = hdc.CreateCompatibleDC()
        h_mem_dc.SelectObject(h_bitmap)

        # Get bitmap dimensions
        bmp_info = win32gui.GetBitmapBits(h_bitmap, False)
        bmp_header = BITMAPINFOHEADER()
        ctypes.memmove(ctypes.pointer(bmp_header), bmp_info, ctypes.sizeof(bmp_header))

        # Create a PIL image from the bitmap
        bmp_str = h_mem_dc.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (bmp_header.biWidth, bmp_header.biHeight),
            bmp_str, 'raw', 'BGRA', 0, 1
        )

        # Clean up handles
        win32gui.DestroyIcon(h_icon)
        for icon in large_icons:
            if icon != h_icon: win32gui.DestroyIcon(icon)
        for icon in small_icons:
            if icon != h_icon: win32gui.DestroyIcon(icon)
        win32gui.DeleteObject(icon_info[3]) # hbmMask
        win32gui.DeleteObject(icon_info[4]) # hbmColor
        hdc.DeleteDC()
        h_mem_dc.DeleteDC()

        logger.debug(f"Successfully extracted icon from '{exe_path}'.")
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

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', ctypes.wintypes.DWORD),
        ('biWidth', ctypes.wintypes.LONG),
        ('biHeight', ctypes.wintypes.LONG),
        ('biPlanes', ctypes.wintypes.WORD),
        ('biBitCount', ctypes.wintypes.WORD),
        ('biCompression', ctypes.wintypes.DWORD),
        ('biSizeImage', ctypes.wintypes.DWORD),
        ('biXPelsPerMeter', ctypes.wintypes.LONG),
        ('biYPelsPerMeter', ctypes.wintypes.LONG),
        ('biClrUsed', ctypes.wintypes.DWORD),
        ('biClrImportant', ctypes.wintypes.DWORD)
    ]