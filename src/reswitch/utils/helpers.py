import sys
import os
import math
import ctypes
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk
import win32api
import win32gui
import win32con
from win32com.shell import shell, shellcon
import logging

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
        flags = shellcon.SHGFI_ICON | shellcon.SHGFI_LARGEICON
        _ , info = shell.SHGetFileInfo(exe_path, 0, flags)
        hIcon = info[0]
        if not hIcon: return create_placeholder_icon(size=size)

        icon_info = win32gui.GetIconInfo(hIcon)
        hbmColor = icon_info[4]
        bmp = win32gui.GetObject(hbmColor)
        
        bmp_info_header = BITMAPINFOHEADER()
        bmp_info_header.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        hdc = win32gui.GetDC(0)
        win32gui.GetDIBits(hdc, hbmColor, 0, 0, None, ctypes.byref(bmp_info_header), win32con.DIB_RGB_COLORS)
        win32gui.ReleaseDC(None, hdc)
        
        bits = win32gui.GetBitmapBits(hbmColor, True)
        img = Image.frombuffer("RGBA", (bmp.bmWidth, bmp.bmHeight), bits, "raw", "BGRA", 0, 1)

        win32gui.DestroyIcon(hIcon)
        win32gui.DeleteObject(icon_info[3])
        win32gui.DeleteObject(icon_info[4])
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except Exception:
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
    _fields_ = [('biSize', ctypes.wintypes.DWORD), ('biWidth', ctypes.wintypes.LONG), ('biHeight', ctypes.wintypes.LONG), ('biPlanes', ctypes.wintypes.WORD), ('biBitCount', ctypes.wintypes.WORD), ('biCompression', ctypes.wintypes.DWORD), ('biSizeImage', ctypes.wintypes.DWORD), ('biXPelsPerMeter', ctypes.wintypes.LONG), ('biYPelsPerMeter', ctypes.wintypes.LONG), ('biClrUsed', ctypes.wintypes.DWORD), ('biClrImportant', ctypes.wintypes.DWORD)]
class BITMAPINFO(ctypes.Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', ctypes.wintypes.DWORD * 1)]