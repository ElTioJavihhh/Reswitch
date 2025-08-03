import customtkinter as ctk
from customtkinter import filedialog
import win32api
import win32con
import win32gui
import win32ui
import psutil
import keyboard
import threading
import time
import json
import os
import sys
import winreg as reg
from PIL import Image, ImageDraw
import pystray
import ctypes
import traceback
import webbrowser

# --- Constantes y Configuración ---
APP_NAME = "Reswitch"

# --- FUNCIÓN DE RUTA PARA PYINSTALLER ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta a un recurso, funciona para desarrollo y para PyInstaller. """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- GESTOR DE IDIOMA ---
translations = {
    "en": {
        "nav_home": "Home",
        "nav_profiles": "Profiles",
        "nav_settings": "Settings",
        "nav_support": "❤️ Support",
        "home_title": "Game Profile Manager",
        "home_subtitle": "Manage your profiles and settings for an optimal gaming experience.",
        "quick_switch_title": "Quick Switch",
        "desktop_res_label": "Desktop Resolution",
        "game_res_label": "Game Resolution",
        "switch_button": "Switch Resolution",
        "profiles_title": "Game Profiles",
        "profiles_subtitle": "Manage your game profiles with custom resolution and settings.",
        "add_profile_button": "Add New Profile",
        "fullscreen_warning": "(!) For best results, use 'Fullscreen Windowed' or 'Borderless' mode in your games to avoid black screens.",
        "settings_title": "General Settings",
        "startup_options_label": "Startup Options",
        "start_with_windows": "Start with Windows",
        "minimize_to_tray": "Minimize to system tray on close",
        "hotkeys_label": "Keyboard Shortcuts",
        "desktop_hotkey": "Desktop Mode",
        "game_hotkey": "Game Mode",
        "language_label": "Language",
        "save_settings_button": "Save Changes",
        "status_ready": "Ready",
        "status_res_changed": "Resolution changed to {res}",
        "status_admin_needed": "Error: Administrator permissions needed",
        "status_res_unsupported": "Error: Resolution {res} not supported",
        "status_settings_saved": "Settings saved",
        "status_hotkey_error": "Error setting hotkeys: {e}",
        "status_startup_error": "Error modifying startup: {e}",
        "profile_editor_title": "Game Profile Editor",
        "executable_path_label": "Executable Path (.exe):",
        "game_resolution_label": "Resolution for this game:",
        "save_profile_button": "Save Profile",
        "select_executable_title": "Select Executable",
        "delete_button": "Delete",
        "edit_button": "Edit",
        "no_profiles_text": "No game profiles found. Add one to get started!",
        "admin_warning": "Run as Administrator for full functionality.",
        "tray_show": "Show",
        "tray_exit": "Exit",
        "list_header_game": "GAME",
        "list_header_resolution": "RESOLUTION",
    },
    "es": {
        "nav_home": "Inicio",
        "nav_profiles": "Perfiles",
        "nav_settings": "Ajustes",
        "nav_support": "❤️ Apoyar",
        "home_title": "Gestor de Perfiles de Juego",
        "home_subtitle": "Gestiona tus perfiles y configuraciones para una experiencia de juego óptima.",
        "quick_switch_title": "Cambio Rápido",
        "desktop_res_label": "Resolución Escritorio",
        "game_res_label": "Resolución Juego",
        "switch_button": "Cambiar Resolución",
        "profiles_title": "Perfiles de Juego",
        "profiles_subtitle": "Gestiona tus perfiles de juego con resoluciones y ajustes personalizados.",
        "add_profile_button": "Añadir Nuevo Perfil",
        "fullscreen_warning": "(!) Para mejores resultados, usa el modo 'Ventana sin Bordes' o 'Pantalla Completa en Ventana' en tus juegos para evitar pantallazos negros.",
        "settings_title": "Configuración General",
        "startup_options_label": "Opciones de Inicio",
        "start_with_windows": "Iniciar con Windows",
        "minimize_to_tray": "Minimizar a la bandeja del sistema al cerrar",
        "hotkeys_label": "Atajos de Teclado",
        "desktop_hotkey": "Modo Escritorio",
        "game_hotkey": "Modo Juego",
        "language_label": "Idioma",
        "save_settings_button": "Guardar Cambios",
        "status_ready": "Listo",
        "status_res_changed": "Resolución cambiada a {res}",
        "status_admin_needed": "Error: Se necesitan permisos de administrador",
        "status_res_unsupported": "Error: Resolución {res} no soportada",
        "status_settings_saved": "Ajustes guardados",
        "status_hotkey_error": "Error al configurar atajos: {e}",
        "status_startup_error": "Error al modificar inicio: {e}",
        "profile_editor_title": "Editor de Perfiles de Juego",
        "executable_path_label": "Ruta del ejecutable (.exe):",
        "game_resolution_label": "Resolución para este juego:",
        "save_profile_button": "Guardar Perfil",
        "select_executable_title": "Selecciona el ejecutable",
        "delete_button": "Eliminar",
        "edit_button": "Editar",
        "no_profiles_text": "No hay perfiles de juego. ¡Añade uno para empezar!",
        "admin_warning": "Ejecutar como Administrador para un funcionamiento completo.",
        "tray_show": "Mostrar",
        "tray_exit": "Salir",
        "list_header_game": "JUEGO",
        "list_header_resolution": "RESOLUCIÓN",
    },
    "zh": {
        "nav_home": "首页",
        "nav_profiles": "配置",
        "nav_settings": "设置",
        "nav_support": "❤️ 支持",
        "home_title": "游戏配置文件管理器",
        "home_subtitle": "管理您的配置文件和设置以获得最佳游戏体验。",
        "quick_switch_title": "快速切换",
        "desktop_res_label": "桌面分辨率",
        "game_res_label": "游戏分辨率",
        "switch_button": "切换分辨率",
        "profiles_title": "游戏配置",
        "profiles_subtitle": "使用自定义分辨率和设置管理您的游戏配置文件。",
        "add_profile_button": "添加新配置",
        "fullscreen_warning": "(!) 为了获得最佳效果，请在游戏中使用“无边框窗口”或“全屏窗口”模式以避免黑屏。",
        "settings_title": "通用设置",
        "startup_options_label": "启动选项",
        "start_with_windows": "开机自启",
        "minimize_to_tray": "关闭时最小化到系统托盘",
        "hotkeys_label": "键盘快捷键",
        "desktop_hotkey": "桌面模式",
        "game_hotkey": "游戏模式",
        "language_label": "语言",
        "save_settings_button": "保存更改",
        "status_ready": "准备就绪",
        "status_res_changed": "分辨率已更改为 {res}",
        "status_admin_needed": "错误：需要管理员权限",
        "status_res_unsupported": "错误：不支持分辨率 {res}",
        "status_settings_saved": "设置已保存",
        "status_hotkey_error": "设置快捷键时出错: {e}",
        "status_startup_error": "修改启动项时出错: {e}",
        "profile_editor_title": "游戏配置编辑器",
        "executable_path_label": "可执行文件路径 (.exe):",
        "game_resolution_label": "此游戏的分辨率:",
        "save_profile_button": "保存配置",
        "select_executable_title": "选择可执行文件",
        "delete_button": "删除",
        "edit_button": "编辑",
        "no_profiles_text": "未找到游戏配置。添加一个开始吧！",
        "admin_warning": "以管理员身份运行以获得全部功能。",
        "tray_show": "显示",
        "tray_exit": "退出",
        "list_header_game": "游戏",
        "list_header_resolution": "分辨率",
    }
}

class LanguageManager:
    def __init__(self, language="en"):
        self.language = language
    def get(self, key, **kwargs):
        return translations.get(self.language, translations["en"]).get(key, key).format(**kwargs)
    def set(self, language):
        self.language = language

# --- Clases de Utilidad y Widgets Personalizados ---
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def get_icon_from_exe(exe_path, size=(32, 32)):
    try:
        large, small = win32gui.ExtractIconEx(resource_path(exe_path), 0)
        hicon = large[0] if large else (small[0] if small else None)
        if not hicon: raise ValueError("No icons found")
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap(); hbmp.CreateCompatibleBitmap(hdc, size[0], size[1])
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, hicon, size[0], size[1], 0, 0, 0x0003)
        bmp_info = hbmp.GetInfo()
        bmp_str = hbmp.GetBitmapBits(True)
        pil_img = Image.frombuffer('RGBA', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_str, 'raw', 'BGRA', 0, 1)
        win32gui.DestroyIcon(hicon); win32gui.DeleteObject(hbmp.GetHandle()); hdc.DeleteDC()
        return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
    except Exception:
        image = Image.new('RGBA', size, (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
        draw.ellipse((2, 10, 30, 28), fill='#cccccc', outline='#aaaaaa', width=1)
        draw.rectangle((6, 15, 12, 21), fill='#555555'); draw.rectangle((8, 13, 10, 23), fill='#555555')
        draw.ellipse((20, 14, 24, 18), fill='#ff5555'); draw.ellipse((24, 18, 28, 22), fill='#55ff55')
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)

class NavButton(ctk.CTkButton):
    def __init__(self, master, text_key, command, lang_manager):
        self.lang_manager = lang_manager
        self.text_key = text_key
        super().__init__(master, text=self.lang_manager.get(text_key), command=command,
                         height=40, corner_radius=8,
                         font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                         fg_color="transparent", text_color=("gray10", "gray90"),
                         hover_color=("gray75", "gray25"), anchor="w")
    def update_text(self):
        self.configure(text=self.lang_manager.get(self.text_key))

class ActionLabel(ctk.CTkLabel):
    def __init__(self, master, text_key, command, color, lang_manager):
        self.lang_manager = lang_manager
        self.text_key = text_key
        super().__init__(master, text=self.lang_manager.get(text_key), text_color=color, cursor="hand2",
                         font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
        self.bind("<Button-1>", lambda e: command())
    def update_text(self):
        self.configure(text=self.lang_manager.get(self.text_key))

class ResolutionSwitcherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("950x650") 
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.lang = LanguageManager()
        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_bold = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_title = ctk.CTkFont(family="Segoe UI", size=32, weight="bold")
        self.font_subtitle = ctk.CTkFont(family="Segoe UI", size=15, weight="normal")
        self.font_small = ctk.CTkFont(family="Segoe UI", size=12)
        self.font_italic = ctk.CTkFont(family="Segoe UI", size=14, slant="italic")

        self.original_resolution = self.get_current_resolution_str()
        self.supported_resolutions = self.get_supported_resolutions()
        self.game_profiles = []; self.config = {}
        self.process_checker_thread = None
        self.stop_thread = threading.Event(); self.tray_icon = None
        
        self.load_settings()
        self.create_widgets()
        self.update_ui_language()
        self.setup_hotkeys(); self.start_process_checker()
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self.show_frame("home")
        
        self.after(200, self.set_window_icon)

    def set_window_icon(self):
        try:
            hwnd = self.winfo_id()
            icon_path = resource_path("reswitch_icon.ico")
            h_icon = win32gui.LoadImage(0, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
            win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, h_icon)
            win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, h_icon)
        except Exception as e:
            print(f"Error setting window icon: {e}")

    # --- Lógica de Sistema (Backend) ---
    def load_settings(self):
        os.makedirs(APP_DATA_DIR, exist_ok=True)
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f: self.config = json.load(f)
                self.game_profiles = self.config.get("game_profiles", [])
            except (json.JSONDecodeError, IOError): self.config = {}
        self.lang.set(self.config.get("language", "en"))
        self.config.setdefault("desktop_res", self.original_resolution)
        self.config.setdefault("game_res", self.supported_resolutions[1] if len(self.supported_resolutions) > 1 else self.original_resolution)
        self.config.setdefault("start_with_windows", False); self.config.setdefault("minimize_to_tray", True)
        self.config.setdefault("hotkey_desktop", "ctrl+alt+1"); self.config.setdefault("hotkey_game", "ctrl+alt+2")
    
    def save_settings(self):
        os.makedirs(APP_DATA_DIR, exist_ok=True)
        self.config["game_profiles"] = self.game_profiles
        self.config["language"] = self.lang.language
        self.config["desktop_res"] = self.desktop_res_selector.get(); self.config["game_res"] = self.game_res_selector.get()
        self.config["start_with_windows"] = self.start_win_var.get(); self.config["minimize_to_tray"] = self.min_tray_var.get()
        self.config["hotkey_desktop"] = self.desktop_hotkey_entry.get(); self.config["hotkey_game"] = self.game_hotkey_entry.get()
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.update_status("status_settings_saved")
            self.setup_hotkeys(); self.apply_startup_setting()
        except Exception as e: self.update_status("status_startup_error", e=e)

    def get_current_resolution_str(self):
        settings = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        return f"{settings.PelsWidth}x{settings.PelsHeight}"

    def set_resolution(self, res_str):
        try:
            width, height = map(int, res_str.split('x'))
            devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
            devmode.PelsWidth = width; devmode.PelsHeight = height
            devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
            win32api.ChangeDisplaySettings(devmode, 0)
        except Exception:
            if not is_admin(): self.update_status("status_admin_needed")
            else: self.update_status("status_res_unsupported", res=res_str)

    def get_supported_resolutions(self):
        resolutions = set()
        i = 0
        while True:
            try:
                devmode = win32api.EnumDisplaySettings(None, i)
                resolutions.add(f"{devmode.PelsWidth}x{devmode.PelsHeight}")
                i += 1
            except win32api.error: break
        return sorted(list(resolutions), key=lambda r: (int(r.split('x')[0]), int(r.split('x')[1])), reverse=True)

    def setup_hotkeys(self):
        try:
            keyboard.unhook_all()
            desktop_hotkey = self.config.get("hotkey_desktop"); game_hotkey = self.config.get("hotkey_game")
            if desktop_hotkey: keyboard.add_hotkey(desktop_hotkey, lambda: self.set_resolution(self.config["desktop_res"]))
            if game_hotkey: keyboard.add_hotkey(game_hotkey, lambda: self.set_resolution(self.config["game_res"]))
        except Exception as e: self.update_status("status_hotkey_error", e=e)

    def check_for_game_process(self):
        game_is_running = False
        while not self.stop_thread.is_set():
            time.sleep(1)
            found_profile = None
            profile_executables = {os.path.basename(p['path']): p for p in self.game_profiles}
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in profile_executables:
                    found_profile = profile_executables[proc.info['name']]; break
            if found_profile:
                if not game_is_running:
                    game_is_running = True
                    self.original_resolution = self.get_current_resolution_str()
                target_res = found_profile['res']
                if self.get_current_resolution_str() != target_res: self.set_resolution(target_res)
            elif game_is_running:
                game_is_running = False
                self.set_resolution(self.original_resolution)

    def start_process_checker(self):
        self.stop_thread.clear()
        self.process_checker_thread = threading.Thread(target=self.check_for_game_process, daemon=True)
        self.process_checker_thread.start()

    # --- Creación de la Interfaz Gráfica (UI) ---
    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Barra de Navegación Izquierda ---
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, rowspan=2, sticky="nsw")
        self.nav_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.nav_frame, text=APP_NAME, font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = NavButton(self.nav_frame, text_key="nav_home", command=lambda: self.show_frame("home"), lang_manager=self.lang)
        self.home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.profiles_button = NavButton(self.nav_frame, text_key="nav_profiles", command=lambda: self.show_frame("profiles"), lang_manager=self.lang)
        self.profiles_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_button = NavButton(self.nav_frame, text_key="nav_settings", command=lambda: self.show_frame("settings"), lang_manager=self.lang)
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.support_button = NavButton(self.nav_frame, text_key="nav_support", command=self.open_support_link, lang_manager=self.lang)
        self.support_button.grid(row=5, column=0, padx=20, pady=20, sticky="sw")
        
        # --- Contenedor de Contenido Principal ---
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        self.status_bar = ctk.CTkLabel(self, text="", anchor="w", font=self.font_small)
        self.status_bar.grid(row=1, column=1, sticky="ew", padx=20, pady=5)

        self.frames = {}
        for F in ("home", "profiles", "settings"):
            frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_home_frame()
        self.create_profiles_frame()
        self.create_settings_frame()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        buttons = {"home": self.home_button, "profiles": self.profiles_button, "settings": self.settings_button}
        for name, button in buttons.items():
            if name == page_name:
                button.configure(fg_color=("gray70", "gray25"))
            else:
                button.configure(fg_color="transparent")

    def create_home_frame(self):
        frame = self.frames["home"]
        frame.grid_columnconfigure(0, weight=1)
        
        self.home_title_label = ctk.CTkLabel(frame, text="", font=self.font_title, anchor="w")
        self.home_title_label.grid(row=0, column=0, sticky="ew", pady=(10,0))
        self.home_subtitle_label = ctk.CTkLabel(frame, text="", font=self.font_subtitle, text_color="gray60", anchor="w")
        self.home_subtitle_label.grid(row=1, column=0, sticky="ew", pady=(0, 30))

        self.quick_switch_title_label = ctk.CTkLabel(frame, text="", font=self.font_bold, anchor="w")
        self.quick_switch_title_label.grid(row=2, column=0, sticky="ew", pady=(10,5))
        
        res_frame = ctk.CTkFrame(frame, corner_radius=10)
        res_frame.grid(row=3, column=0, sticky="ew")
        res_frame.grid_columnconfigure(1, weight=1)
        res_frame.grid_columnconfigure(3, weight=1)

        self.desktop_res_text_label = ctk.CTkLabel(res_frame, text="", font=self.font_main)
        self.desktop_res_text_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.desktop_res_selector = ctk.CTkOptionMenu(res_frame, values=self.supported_resolutions, height=35, font=self.font_main, dropdown_font=self.font_main)
        self.desktop_res_selector.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        
        self.game_res_text_label = ctk.CTkLabel(res_frame, text="", font=self.font_main)
        self.game_res_text_label.grid(row=0, column=2, padx=(30, 15), pady=15, sticky="w")
        self.game_res_selector = ctk.CTkOptionMenu(res_frame, values=self.supported_resolutions, height=35, font=self.font_main, dropdown_font=self.font_main)
        self.game_res_selector.grid(row=0, column=3, padx=15, pady=15, sticky="ew")
        
        self.switch_button = ctk.CTkButton(frame, text="", command=self.quick_switch, height=50, font=self.font_bold)
        self.switch_button.grid(row=4, column=0, sticky="ew", pady=(20,0))


    def create_profiles_frame(self):
        frame = self.frames["profiles"]
        frame.grid_columnconfigure(0, weight=1); frame.grid_rowconfigure(2, weight=1)

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(10,0))
        header_frame.grid_columnconfigure(0, weight=1)

        self.profiles_title_label = ctk.CTkLabel(header_frame, text="", font=self.font_title, anchor="w")
        self.profiles_title_label.grid(row=0, column=0, sticky="w")
        self.add_profile_button = ctk.CTkButton(header_frame, text="", command=self.open_profile_editor, height=40, font=self.font_bold)
        self.add_profile_button.grid(row=0, column=1, sticky="e")

        self.profiles_subtitle_label = ctk.CTkLabel(frame, text="", font=self.font_subtitle, text_color="gray60", anchor="w")
        self.profiles_subtitle_label.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        list_container = ctk.CTkFrame(frame, corner_radius=8)
        list_container.grid(row=2, column=0, sticky="nsew")
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(1, weight=1)

        self.list_header_frame = ctk.CTkFrame(list_container, fg_color="transparent", height=30)
        self.list_header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(5,0))
        self.list_header_game_label = ctk.CTkLabel(self.list_header_frame, text="", font=self.font_small, text_color="gray50")
        self.list_header_game_label.pack(side="left", padx=50)
        self.list_header_res_label = ctk.CTkLabel(self.list_header_frame, text="", font=self.font_small, text_color="gray50")
        self.list_header_res_label.pack(side="left", padx=20)

        self.profiles_list_frame = ctk.CTkScrollableFrame(list_container, fg_color="transparent")
        self.profiles_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.profiles_list_frame.grid_columnconfigure(0, weight=1)

        self.fullscreen_warning_label = ctk.CTkLabel(frame, text="", font=self.font_small, text_color="gray60", anchor="w")
        self.fullscreen_warning_label.grid(row=3, column=0, sticky="ew", pady=(10,0))

    def create_settings_frame(self):
        frame = self.frames["settings"]
        frame.grid_columnconfigure(0, weight=1)
        self.settings_title_label = ctk.CTkLabel(frame, text="", font=self.font_title, anchor="w")
        self.settings_title_label.grid(row=0, column=0, sticky="ew", pady=(10, 20))

        startup_frame = ctk.CTkFrame(frame); startup_frame.grid(row=1, column=0, sticky="ew", pady=10)
        self.startup_options_label = ctk.CTkLabel(startup_frame, text="", font=self.font_bold)
        self.startup_options_label.pack(padx=15, pady=(10,5), anchor="w")
        self.start_win_var = ctk.BooleanVar()
        self.start_win_check = ctk.CTkCheckBox(startup_frame, text="", variable=self.start_win_var, font=self.font_main)
        self.start_win_check.pack(padx=15, pady=15, anchor="w")

        hotkey_frame = ctk.CTkFrame(frame); hotkey_frame.grid(row=2, column=0, sticky="ew", pady=10)
        hotkey_frame.grid_columnconfigure(1, weight=1)
        self.hotkeys_text_label = ctk.CTkLabel(hotkey_frame, text="", font=self.font_bold)
        self.hotkeys_text_label.grid(row=0, column=0, columnspan=2, pady=(10,15), padx=15, sticky="w")
        self.desktop_hotkey_text_label = ctk.CTkLabel(hotkey_frame, text="", font=self.font_main)
        self.desktop_hotkey_text_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.desktop_hotkey_entry = ctk.CTkEntry(hotkey_frame, font=self.font_main); self.desktop_hotkey_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")
        self.game_hotkey_text_label = ctk.CTkLabel(hotkey_frame, text="", font=self.font_main)
        self.game_hotkey_text_label.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.game_hotkey_entry = ctk.CTkEntry(hotkey_frame, font=self.font_main); self.game_hotkey_entry.grid(row=2, column=1, padx=15, pady=10, sticky="ew")

        lang_frame = ctk.CTkFrame(frame); lang_frame.grid(row=3, column=0, sticky="ew", pady=10)
        self.language_text_label = ctk.CTkLabel(lang_frame, text="", font=self.font_bold)
        self.language_text_label.pack(padx=15, pady=(10,5), anchor="w")
        self.language_selector = ctk.CTkOptionMenu(lang_frame, values=["English", "Español", "中文"], command=self.change_language, font=self.font_main, dropdown_font=self.font_main, height=35)
        self.language_selector.pack(fill="x", padx=15, pady=10)

        self.save_settings_button = ctk.CTkButton(frame, text="", command=self.save_settings, height=40, font=self.font_bold)
        self.save_settings_button.grid(row=4, column=0, sticky="e", pady=20)

    # --- Lógica de la Interfaz (UI) ---
    def change_language(self, choice):
        lang_map = {"English": "en", "Español": "es", "中文": "zh"}
        self.lang.set(lang_map[choice])
        self.update_ui_language()

    def update_ui_language(self):
        lang_map_rev = {"en": "English", "es": "Español", "zh": "中文"}
        self.language_selector.set(lang_map_rev[self.lang.language])

        # Nav
        self.home_button.update_text()
        self.profiles_button.update_text()
        self.settings_button.update_text()
        self.support_button.update_text()

        # Home
        self.home_title_label.configure(text=self.lang.get("home_title"))
        self.home_subtitle_label.configure(text=self.lang.get("home_subtitle"))
        self.quick_switch_title_label.configure(text=self.lang.get("quick_switch_title"))
        self.desktop_res_text_label.configure(text=self.lang.get("desktop_res_label"))
        self.game_res_text_label.configure(text=self.lang.get("game_res_label"))
        self.switch_button.configure(text=self.lang.get("switch_button"))
        
        # Profiles
        self.profiles_title_label.configure(text=self.lang.get("profiles_title"))
        self.profiles_subtitle_label.configure(text=self.lang.get("profiles_subtitle"))
        self.fullscreen_warning_label.configure(text=self.lang.get("fullscreen_warning"))
        self.add_profile_button.configure(text=self.lang.get("add_profile_button"))
        self.list_header_game_label.configure(text=self.lang.get("list_header_game"))
        self.list_header_res_label.configure(text=self.lang.get("list_header_resolution"))
        self.refresh_profiles_list()

        # Settings
        self.settings_title_label.configure(text=self.lang.get("settings_title"))
        self.startup_options_label.configure(text=self.lang.get("startup_options_label"))
        self.start_win_check.configure(text=self.lang.get("start_with_windows"))
        self.hotkeys_text_label.configure(text=self.lang.get("hotkeys_label"))
        self.desktop_hotkey_text_label.configure(text=self.lang.get("desktop_hotkey"))
        self.game_hotkey_text_label.configure(text=self.lang.get("game_hotkey"))
        self.language_text_label.configure(text=self.lang.get("language_label"))
        self.save_settings_button.configure(text=self.lang.get("save_settings_button"))

        # General
        self.update_status("status_ready")
        self.desktop_res_selector.set(self.config.get("desktop_res"))
        self.game_res_selector.set(self.config.get("game_res"))
        self.start_win_var.set(self.config.get("start_with_windows"))
        self.desktop_hotkey_entry.delete(0, 'end'); self.desktop_hotkey_entry.insert(0, self.config.get("hotkey_desktop"))
        self.game_hotkey_entry.delete(0, 'end'); self.game_hotkey_entry.insert(0, self.config.get("hotkey_game"))

    def refresh_profiles_list(self):
        for widget in self.profiles_list_frame.winfo_children(): widget.destroy()
        if not self.game_profiles:
            ctk.CTkLabel(self.profiles_list_frame, text=self.lang.get("no_profiles_text"), font=self.font_italic, text_color="gray50").pack(pady=50, padx=10)
            return
        
        for profile in self.game_profiles:
            p_frame = ctk.CTkFrame(self.profiles_list_frame, fg_color=("gray85", "gray18"), height=50)
            p_frame.pack(fill="x", padx=5, pady=4)
            p_frame.grid_columnconfigure(1, weight=1)

            icon = get_icon_from_exe(profile['path'])
            ctk.CTkLabel(p_frame, text="", image=icon).grid(row=0, column=0, padx=10, pady=10)
            game_name = os.path.basename(profile['path']).replace('.exe', '')
            ctk.CTkLabel(p_frame, text=game_name, font=self.font_bold).grid(row=0, column=1, sticky="w", padx=10)
            ctk.CTkLabel(p_frame, text=profile['res'], font=self.font_main).grid(row=0, column=2, padx=40)

            actions_frame = ctk.CTkFrame(p_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=3, padx=10)
            ActionLabel(actions_frame, text_key="edit_button", command=lambda p=profile: self.open_profile_editor(p), color="#3498db", lang_manager=self.lang).pack(side="left", padx=5)
            ActionLabel(actions_frame, text_key="delete_button", command=lambda p=profile: self.delete_profile(p), color="#e74c3c", lang_manager=self.lang).pack(side="left", padx=5)

    def open_profile_editor(self, profile_to_edit=None):
        editor = ctk.CTkToplevel(self); editor.transient(self); editor.grab_set()
        editor.title(self.lang.get("profile_editor_title")); editor.geometry("450x250")
        
        ctk.CTkLabel(editor, text=self.lang.get("executable_path_label"), font=self.font_main).pack(padx=20, pady=(15,0), anchor="w")
        path_frame = ctk.CTkFrame(editor, fg_color="transparent"); path_frame.pack(fill="x", padx=20)
        path_entry = ctk.CTkEntry(path_frame, width=330, font=self.font_main); path_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(path_frame, text="...", width=30, font=self.font_main, command=lambda: path_entry.insert(0, filedialog.askopenfilename(title=self.lang.get("select_executable_title"), filetypes=[("Executable", "*.exe")]))).pack(side="right", padx=(5,0))

        ctk.CTkLabel(editor, text=self.lang.get("game_resolution_label"), font=self.font_main).pack(padx=20, pady=(15,0), anchor="w")
        res_selector = ctk.CTkOptionMenu(editor, values=self.supported_resolutions, font=self.font_main); res_selector.pack(fill="x", padx=20, pady=5)
        
        if profile_to_edit:
            path_entry.insert(0, profile_to_edit["path"])
            res_selector.set(profile_to_edit["res"])

        def save_profile():
            path = path_entry.get(); res = res_selector.get()
            if path and res:
                if profile_to_edit:
                    profile_to_edit["path"] = path; profile_to_edit["res"] = res
                else:
                    self.game_profiles.append({"path": path, "res": res})
                self.save_settings(); self.refresh_profiles_list(); editor.destroy()
        
        ctk.CTkButton(editor, text=self.lang.get("save_profile_button"), command=save_profile, height=40, font=self.font_bold).pack(pady=20, padx=20, fill="x")

    def delete_profile(self, profile_to_delete): self.game_profiles.remove(profile_to_delete); self.save_settings(); self.refresh_profiles_list()
    
    def update_status(self, key, **kwargs):
        message = self.lang.get(key, **kwargs)
        is_error = "Error" in key
        colors = {"success": "#2CC963", "error": "#E53935", "info": "#DCE4EE"}
        level = "error" if is_error else ("success" if "saved" in key else "info")
        self.status_bar.configure(text=f"{self.lang.get('status_ready')}: {message}", text_color=colors[level])

    def quick_switch(self):
        current_res = self.get_current_resolution_str()
        desktop_res = self.desktop_res_selector.get(); game_res = self.game_res_selector.get()
        if current_res == desktop_res: self.set_resolution(game_res)
        else: self.set_resolution(desktop_res)
    
    def open_support_link(self):
        """Abre el enlace de donación en el navegador web del usuario."""
        webbrowser.open("https://buymeacoffee.com/javihhh")

    def apply_startup_setting(self):
        key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(__file__)
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
            if self.config.get("start_with_windows"): reg.SetValueEx(key, APP_NAME, 0, reg.REG_SZ, f'"{exe_path}"')
            else:
                try: reg.DeleteValue(key, APP_NAME)
                except FileNotFoundError: pass
            reg.CloseKey(key)
        except Exception as e: self.update_status("status_startup_error", e=e)

    def ask_on_close(self):
        """Muestra un diálogo personalizado al intentar cerrar la ventana."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.lang.get("close_dialog_title"))
        
        # Centrar el diálogo en la ventana principal
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_w = self.winfo_width()
        main_h = self.winfo_height()
        dialog_w = 400
        dialog_h = 150
        dialog.geometry(f"{dialog_w}x{dialog_h}+{main_x + (main_w - dialog_w) // 2}+{main_y + (main_h - dialog_h) // 2}")
        
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        label = ctk.CTkLabel(dialog, text=self.lang.get("close_dialog_text"), font=self.font_main)
        label.pack(pady=20, padx=20)

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        minimize_button = ctk.CTkButton(button_frame, text=self.lang.get("close_dialog_minimize_button"), command=lambda: [self.iconify(), dialog.destroy()], width=150)
        minimize_button.grid(row=0, column=0, padx=10)

        exit_button = ctk.CTkButton(button_frame, text=self.lang.get("close_dialog_exit_button"), command=self.quit_app, fg_color="#D32F2F", hover_color="#B71C1C", width=150)
        exit_button.grid(row=0, column=1, padx=10)

    def quit_app(self):
        self.stop_thread.set()
        self.quit()

if __name__ == "__main__":
    # --- Bloque de Arranque a Prueba de Fallos ---
    def show_error_and_exit(e):
        """Muestra un error en una ventana emergente simple antes de cerrar."""
        error_message = f"A critical error occurred and the application must close.\n\nError: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        ctypes.windll.user32.MessageBoxW(None, error_message, "Application Startup Error", 0x10) # MB_OK | MB_ICONERROR
        sys.exit(1)

    try:
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0) 
        else:
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)
            except AttributeError:
                pass
            app = ResolutionSwitcherApp()
            app.mainloop()
    except Exception as e:
        show_error_and_exit(e)
