# En: src/reswitch/utils/helpers.py

import os
import sys
import math
import ctypes
from ctypes import wintypes
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk
import win32api
import win32gui
import win32con

def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta a un recurso. Funciona tanto en desarrollo
    como en un ejecutable de PyInstaller.
    """
    try:
        # PyInstaller crea una carpeta temporal y almacena su ruta en _MEIPASS.
        base_path = sys._MEIPASS
    except AttributeError:
        # Si no se está ejecutando desde PyInstaller, la base es el directorio del proyecto.
        # Asumimos que los assets están en src/reswitch/assets
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))
    
    return os.path.join(base_path, relative_path)

def calculate_aspect_ratio(width: int, height: int) -> str:
    """Calcula el aspect ratio de una resolución (ej. 16:9)."""
    if width == 0 or height == 0:
        return ""
    gcd = math.gcd(width, height)
    return f"({width // gcd}:{height // gcd})"

def set_dpi_awareness():
    """Configura la aplicación para que sea consciente de los DPI en Windows."""
    try:
        # Windows 8.1 y superior
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except AttributeError:
        try:
            # Windows Vista y superior
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            # Versiones más antiguas de Windows no lo soportan
            pass

# --- FUNCIÓN NUEVA AÑADIDA ---
def get_icon_from_exe(exe_path: str, size: Tuple[int, int] = (32, 32)) -> ctk.CTkImage:
    """ Extrae el icono de un archivo .exe y lo devuelve como un CTkImage. """
    if not exe_path or not os.path.exists(exe_path):
        return create_placeholder_icon("generic", size)

    try:
        large, small = win32gui.ExtractIconEx(exe_path, 0, 1)
        
        # Priorizar icono grande, si no, el pequeño
        icon_handle = large[0] if large else (small[0] if small else None)
        
        if not icon_handle:
            for i in large: win32gui.DestroyIcon(i)
            for i in small: win32gui.DestroyIcon(i)
            return create_placeholder_icon("generic", size)

        # Convertir HICON a CTkImage
        icon_info = win32gui.GetIconInfo(icon_handle)
        hbmp = icon_info[4] # HBITMAP de color
        
        bmp_info_header = BITMAPINFOHEADER()
        bmp_info_header.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        
        hdc = win32gui.GetDC(0)
        win32gui.GetDIBits(hdc, hbmp, 0, 0, None, ctypes.byref(bmp_info_header), win32con.DIB_RGB_COLORS)
        
        bmp_info_header.biHeight = abs(bmp_info_header.biHeight)
        bmp_info_header.biCompression = win32con.BI_RGB
        
        w, h = bmp_info_header.biWidth, bmp_info_header.biHeight
        
        bits = ctypes.create_string_buffer(w * h * 4)
        win32gui.GetDIBits(hdc, hbmp, 0, h, bits, ctypes.byref(bmp_info_header), win32con.DIB_RGB_COLORS)
        
        img = Image.frombuffer("RGBA", (w, h), bits.raw, "raw", "BGRA", 0, 1)

        # Limpieza de recursos
        win32gui.DeleteObject(hbmp)
        win32gui.DeleteObject(icon_info[3])
        win32gui.ReleaseDC(None, hdc)
        for i in large: win32gui.DestroyIcon(i)
        for i in small: win32gui.DestroyIcon(i)
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    except Exception:
        return create_placeholder_icon("generic", size)

# --- FUNCIÓN ORIGINAL MODIFICADA PARA MEJOR VISUALIZACIÓN ---
def create_placeholder_icon(icon_type: str = "generic", size: Tuple[int, int] = (32, 32)) -> ctk.CTkImage:
    """Crea un icono de marcador de posición si no se puede cargar el del juego."""
    image = Image.new('RGBA', size, (0, 0, 0, 0)) # Transparente
    draw = ImageDraw.Draw(image)
    
    # Dibuja un fondo redondeado
    draw.rounded_rectangle((0, 0, size[0]-1, size[1]-1), radius=4, fill="#4a4a4a")

    try:
        font = ImageFont.truetype("seguisb.ttf", size[0] // 2)
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((size[0]/2, size[1]/2), "?", fill="#ffffff", anchor="ms", font=font)
        
    return ctk.CTkImage(light_image=image, dark_image=image, size=size)

# --- DEFINICIONES NECESARIAS PARA ctypes (AÑADIDAS) ---
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD)
    ]