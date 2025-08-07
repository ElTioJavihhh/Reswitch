import customtkinter as ctk
import win32api
import win32con
import psutil
import keyboard
import threading
import time
import json
import os
import sys
import winreg as reg
from PIL import Image, ImageTk
import webbrowser
import pystray
import logging
from typing import Optional, Dict, Any, List
from dataclasses import asdict

# --- CORRECCIÓN: Importaciones relativas corregidas ---
from ..config import (
    APP_NAME, SETTINGS_FILE, APP_DATA_DIR, THEMES, WINDOW_WIDTH,
    WINDOW_HEIGHT
)
from ..language import LanguageManager
from ..utils import helpers
from . import views, widgets
from ..core.engine import GameScannerEngine
from ..core.models import GameProfile

logger = logging.getLogger(__name__)

class ResolutionSwitcherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        logger.info(f"Iniciando {APP_NAME}...")
        
        helpers.set_dpi_awareness()
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.lang = LanguageManager()
        self.engine = GameScannerEngine()
        self.theme = THEMES["Light"]
        self.icon_path = helpers.resource_path("reswitch_icon.ico")
        
        # --- CORRECCIÓN: Carga el icono una sola vez y lo guarda como un objeto ---
        if os.path.exists(self.icon_path):
            self.app_icon = ImageTk.PhotoImage(Image.open(self.icon_path))
        else:
            self.app_icon = None
        
        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_bold = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_title = ctk.CTkFont(family="Segoe UI", size=32, weight="bold")
        self.font_subtitle = ctk.CTkFont(family="Segoe UI", size=15)
        self.font_small = ctk.CTkFont(family="Segoe UI", size=12)

        # El resto del código de __init__ se mantiene igual
        self.monitors, self.monitor_names, self.supported_resolutions_cache = self._get_available_monitors(), [], {}; self.monitor_names = list(self.monitors.keys())
        self.original_resolution: Optional[str] = None; self.game_profiles: List[GameProfile] = []; self.config: Dict[str, Any] = {}
        self.process_checker_thread: Optional[threading.Thread] = None; self.stop_thread = threading.Event(); self.tray_icon: Optional[pystray.Icon] = None; self.tray_thread: Optional[threading.Thread] = None; self.current_frame_name: Optional[str] = None
        self.load_settings(); self.apply_theme(); self._create_widgets(); self.update_ui_language()
        self.setup_hotkeys(); self.start_process_checker(); self.protocol("WM_DELETE_WINDOW", self.hide_to_tray); self.set_window_icon()
        self.show_frame("home"); logger.info("Aplicación inicializada correctamente.")

    def set_window_icon(self):
        try:
            if os.path.exists(self.icon_path):
                self.iconbitmap(self.icon_path)
        except Exception as e:
            logger.error(f"Error al establecer el icono de la ventana: {e}")

    def load_settings(self):
        os.makedirs(APP_DATA_DIR, exist_ok=True)
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f: self.config = json.load(f)
        except (json.JSONDecodeError, IOError, FileNotFoundError): self.config = {}
        
        self.lang.set_language(self.config.get("language", "en"))
        ctk.set_appearance_mode(self.config.get("appearance_mode", "System"))
        
        default_monitor = self.monitor_names[0] if self.monitor_names else "Principal"
        self.config.setdefault("target_monitor", default_monitor)
        
        self.original_resolution = self._get_current_resolution_str(self.config["target_monitor"])
        current_monitor_res = self._get_supported_resolutions(self.config["target_monitor"])
        
        self.config.setdefault("desktop_res", self.original_resolution)
        self.config.setdefault("game_res", current_monitor_res[1] if len(current_monitor_res) > 1 else self.original_resolution)
        self.config.setdefault("start_with_windows", False)
        self.config.setdefault("hotkey_desktop", "ctrl+alt+1")
        self.config.setdefault("hotkey_game", "ctrl+alt+2")
        self.config.setdefault("tray_notification_shown", False)
        self.game_profiles = [GameProfile(**p) for p in self.config.get("game_profiles", [])]

    def save_settings(self):
        if "settings" not in self.frames or "home" not in self.frames: return

        settings_view = self.frames["settings"]
        home_view = self.frames["home"]
        
        appearance_map_rev = {v: k for k, v in self._get_translated_appearance_map().items()}
        self.config["appearance_mode"] = appearance_map_rev.get(settings_view.appearance_mode_selector.get(), "System")
        self.config["game_profiles"] = [asdict(p) for p in self.game_profiles]
        self.config["language"] = self.lang.language
        self.config["target_monitor"] = settings_view.monitor_selector.get()
        self.config["desktop_res"] = home_view.desktop_res_selector.get()
        self.config["game_res"] = home_view.game_res_selector.get()
        self.config["start_with_windows"] = bool(settings_view.start_win_var.get())
        self.config["hotkey_desktop"] = settings_view.desktop_hotkey_entry.cget("text")
        self.config["hotkey_game"] = settings_view.game_hotkey_entry.cget("text")
        
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.update_status("status_settings_saved")
            self.setup_hotkeys()
            self.apply_startup_setting()
        except Exception as e: self.update_status("status_startup_error", e=e)

    def _create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, rowspan=2, sticky="nsw")
        self.nav_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = ctk.CTkLabel(self.nav_frame, text=APP_NAME, font=self.font_bold)
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        self.nav_buttons = { "home": widgets.NavButton(self.nav_frame, "nav_home", lambda: self.show_frame("home"), self.lang, self.theme), "profiles": widgets.NavButton(self.nav_frame, "nav_profiles", lambda: self.show_frame("profiles"), self.lang, self.theme), "settings": widgets.NavButton(self.nav_frame, "nav_settings", lambda: self.show_frame("settings"), self.lang, self.theme) }
        self.nav_buttons["home"].grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons["profiles"].grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons["settings"].grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.support_button = widgets.NavButton(self.nav_frame, "nav_support", self.open_support_link, self.lang, self.theme)
        self.support_button.grid(row=6, column=0, padx=20, pady=20, sticky="sw")
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.status_bar = ctk.CTkLabel(self, text="", anchor="w", font=self.font_small)
        self.status_bar.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 5))
        self.frames: Dict[str, ctk.CTkFrame] = {}
        for F_name in ["home", "profiles", "settings"]:
            FrameClass = getattr(views, f"{F_name.capitalize()}Frame")
            frame = FrameClass(parent=self.content_frame, controller=self)
            self.frames[F_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name: str):
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
            self.current_frame_name = page_name
            for name, button in self.nav_buttons.items():
                button.set_active(name == page_name)

    def update_ui_language(self):
        settings_view = self.frames["settings"]; home_view = self.frames["home"]
        lang_map_rev = {"en": "English", "es": "Español", "zh": "中文"}; settings_view.language_selector.set(lang_map_rev.get(self.lang.language, "English"))
        for button in self.nav_buttons.values(): button.update_text()
        self.support_button.update_text()
        for frame in self.frames.values():
            if hasattr(frame, 'update_language'): frame.update_language()
        appearance_map = self._get_translated_appearance_map(); settings_view.appearance_mode_selector.configure(values=list(appearance_map.values())); current_mode_key = self.config.get("appearance_mode", "System"); settings_view.appearance_mode_selector.set(appearance_map.get(current_mode_key, "System"))
        target_monitor = self.config.get("target_monitor")
        if self.monitor_names:
            settings_view.monitor_selector.configure(values=self.monitor_names)
            if target_monitor in self.monitor_names: settings_view.monitor_selector.set(target_monitor)
            else: settings_view.monitor_selector.set(self.monitor_names[0])
        self.on_monitor_change(settings_view.monitor_selector.get())
        home_view.desktop_res_selector.set(self.config.get("desktop_res")); home_view.game_res_selector.set(self.config.get("game_res")); settings_view.start_win_var.set(self.config.get("start_with_windows", False)); settings_view.desktop_hotkey_entry.configure(text=self.config.get("hotkey_desktop")); settings_view.game_hotkey_entry.configure(text=self.config.get("hotkey_game"))
        self.update_theme_for_all_widgets()

    def update_theme_for_all_widgets(self):
        self.apply_theme()
        theme = self.theme
        self.configure(fg_color=theme['bg'])
        self.nav_frame.configure(fg_color=theme['bg_secondary'])
        self.logo_label.configure(text_color=theme['text'])
        self.status_bar.configure(text_color=theme['text_secondary'])
        for button in self.nav_buttons.values(): button.update_theme(theme)
        self.support_button.update_theme(theme)
        for view in self.frames.values():
            if hasattr(view, 'update_theme'):
                view.update_theme(theme)

    def _apply_theme_to_widget(self, widget, theme):
        pass

    def _get_available_monitors(self) -> Dict[str, Any]:
        monitors: Dict[str, Any] = {}; i = 0
        try:
            while True:
                try:
                    device = win32api.EnumDisplayDevices(None, i)
                    if device.StateFlags & win32con.DISPLAY_DEVICE_ACTIVE: monitors[f"Monitor {i+1}: {device.DeviceString}"] = device.DeviceName
                    i += 1
                except win32api.error: break
        except Exception: pass
        if not monitors: monitors["Principal"] = None
        return monitors
        
    def _get_current_resolution_str(self, monitor_name: Optional[str]) -> str:
        device_name = self.monitors.get(monitor_name)
        try:
            settings = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)
            w, h = settings.PelsWidth, settings.PelsHeight
            return f"{w}x{h} {helpers.calculate_aspect_ratio(w, h)}"
        except Exception: return "N/A"

    def set_resolution(self, res_str: str, monitor_name: Optional[str] = None):
        if not monitor_name: monitor_name = self.config.get("target_monitor")
        device_name = self.monitors.get(monitor_name)
        if not res_str or 'x' not in res_str: return
        try:
            res_part = res_str.split(' ')[0]; width, height = map(int, res_part.split('x'))
            devmode = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)
            devmode.PelsWidth = width; devmode.PelsHeight = height; devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
            win32api.ChangeDisplaySettingsEx(device_name, devmode, 0)
            self.update_status("status_res_changed", res=res_str, monitor=monitor_name)
        except Exception as e: self.update_status("status_res_unsupported", res=res_str)

    def _get_supported_resolutions(self, monitor_name: Optional[str]) -> List[str]:
        if not monitor_name or monitor_name in self.supported_resolutions_cache: return self.supported_resolutions_cache.get(monitor_name, [])
        device_name = self.monitors.get(monitor_name); resolutions = set(); i = 0
        try:
            while True:
                devmode = win32api.EnumDisplaySettings(device_name, i); w, h = devmode.PelsWidth, devmode.PelsHeight
                resolutions.add(f"{w}x{h} {helpers.calculate_aspect_ratio(w, h)}"); i += 1
        except Exception: pass 
        sorted_res = sorted(list(resolutions), key=lambda r: tuple(map(int, r.split(' ')[0].split('x'))), reverse=True) if resolutions else ["1920x1080 (16:9)", "1280x720 (16:9)"]
        self.supported_resolutions_cache[monitor_name] = sorted_res; return sorted_res

    def setup_hotkeys(self):
        try:
            keyboard.unhook_all()
            desktop_hotkey = self.config.get("hotkey_desktop"); game_hotkey = self.config.get("hotkey_game")
            if desktop_hotkey: keyboard.add_hotkey(desktop_hotkey, lambda: self.set_resolution(self.config.get("desktop_res")))
            if game_hotkey: keyboard.add_hotkey(game_hotkey, lambda: self.set_resolution(self.config.get("game_res")))
        except Exception as e: self.update_status("status_hotkey_error", e=e)

    def check_for_game_process(self):
        game_is_running = False; active_profile: Optional[GameProfile] = None
        while not self.stop_thread.is_set():
            time.sleep(2); found_profile: Optional[GameProfile] = None
            profile_executables = {os.path.basename(p.path): p for p in self.game_profiles}
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in profile_executables: found_profile = profile_executables[proc.info['name']]; break
            if found_profile and found_profile != active_profile:
                game_is_running = True; active_profile = found_profile
                monitor = active_profile.monitor or self.config.get("target_monitor")
                self.original_resolution = self._get_current_resolution_str(monitor)
                target_res = active_profile.res
                if self._get_current_resolution_str(monitor) != target_res: self.after(0, self.set_resolution, target_res, monitor)
            elif not found_profile and game_is_running and active_profile:
                game_is_running = False
                monitor = active_profile.monitor or self.config.get("target_monitor")
                if self.original_resolution: self.after(0, self.set_resolution, self.original_resolution, monitor)
                active_profile = None

    def start_process_checker(self):
        if self.process_checker_thread and self.process_checker_thread.is_alive(): return
        self.stop_thread.clear(); self.process_checker_thread = threading.Thread(target=self.check_for_game_process, daemon=True); self.process_checker_thread.start()

    def on_monitor_change(self, monitor_name: str):
        resolutions = self._get_supported_resolutions(monitor_name); home_view = self.frames["home"]
        if not resolutions: return
        home_view.desktop_res_selector.configure(values=resolutions); home_view.game_res_selector.configure(values=resolutions)
        if home_view.desktop_res_selector.get() not in resolutions: home_view.desktop_res_selector.set(resolutions[0])
        if home_view.game_res_selector.get() not in resolutions: home_view.game_res_selector.set(resolutions[1] if len(resolutions) > 1 else resolutions[0])

    def change_language(self, choice: str):
        lang_map = {"English": "en", "Español": "es", "中文": "zh"}; self.lang.set_language(lang_map.get(choice, "en")); self.update_ui_language()

    def change_appearance_mode(self, new_mode_translated: str):
        lang_map_rev = {v: k for k, v in self._get_translated_appearance_map().items()}; new_mode_key = lang_map_rev.get(new_mode_translated, "System"); ctk.set_appearance_mode(new_mode_key); self.update_theme_for_all_widgets()
    
    def _get_translated_appearance_map(self) -> Dict[str, str]:
        return { "Light": self.lang.get("theme_light"), "Dark": self.lang.get("theme_dark"), "System": self.lang.get("theme_system") }

    def apply_theme(self):
        mode = ctk.get_appearance_mode(); self.theme = THEMES.get(mode, THEMES["Light"])

    def open_profile_editor(self, profile_to_edit: Optional[GameProfile] = None):
        if hasattr(widgets, 'ProfileEditor'): editor = widgets.ProfileEditor(master=self, controller=self, profile_to_edit=profile_to_edit); editor.grab_set()

    def delete_profile(self, profile_to_delete: GameProfile):
        if profile_to_delete in self.game_profiles: self.game_profiles.remove(profile_to_delete); self.save_settings()
        if "profiles" in self.frames: self.frames["profiles"].refresh_profiles_list()

    def update_status(self, key: str, **kwargs):
        message = self.lang.get(key, **kwargs); level = "error" if "error" in key.lower() else ("success" if "saved" in key or "changed" in key else "info")
        color = self.theme.get(f"text_{level}", self.theme['text_secondary']); self.status_bar.configure(text=message, text_color=color)
        self.after(5000, lambda: self.status_bar.configure(text=""))

    def quick_switch(self):
        monitor = self.config.get("target_monitor"); current_res = self._get_current_resolution_str(monitor); desktop_res = self.config.get("desktop_res"); game_res = self.config.get("game_res")
        target_res = game_res if current_res == desktop_res else desktop_res; self.set_resolution(target_res, monitor)

    def open_support_link(self):
        webbrowser.open("https://buymeacoffee.com/javihhh")

    def apply_startup_setting(self):
        key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        if getattr(sys, 'frozen', False): exe_path = sys.executable; command = f'"{exe_path}"'
        else: script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "run.py")); command = f'"{sys.executable}" "{script_path}"'
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS) as key:
                if self.config.get("start_with_windows"): reg.SetValueEx(key, APP_NAME, 0, reg.REG_SZ, command)
                else:
                    try: reg.DeleteValue(key, APP_NAME)
                    except FileNotFoundError: pass
        except Exception as e: self.update_status("status_startup_error", e=e)

    def capture_hotkey(self, button_widget: ctk.CTkButton):
        if hasattr(widgets, 'HotkeyCaptureWindow'): capture_window = widgets.HotkeyCaptureWindow(master=self, controller=self, button_to_update=button_widget); capture_window.grab_set()

    def open_game_scanner_window(self):
        if hasattr(widgets, 'GameScannerWindow'): scanner = widgets.GameScannerWindow(master=self, controller=self); scanner.grab_set()

    def _show_tray_notification_dialog(self, on_close_callback):
        if hasattr(widgets, 'TrayNotificationDialog'): dialog = widgets.TrayNotificationDialog(master=self, controller=self, on_close_callback=on_close_callback); dialog.grab_set()

    def setup_tray_icon(self):
        icon_image = Image.open(self.icon_path) if os.path.exists(self.icon_path) else None
        menu = (pystray.MenuItem(lambda: self.lang.get("tray_show"), self.show_window, default=True), pystray.MenuItem(lambda: self.lang.get("tray_desktop_mode"), lambda: self.set_resolution(self.config.get("desktop_res"))), pystray.MenuItem(lambda: self.lang.get("tray_game_mode"), lambda: self.set_resolution(self.config.get("game_res"))), pystray.Menu.SEPARATOR, pystray.MenuItem(lambda: self.lang.get("tray_exit"), self.quit_app))
        self.tray_icon = pystray.Icon(APP_NAME, icon_image, APP_NAME, menu); self.tray_icon.run()

    def hide_to_tray(self):
        def _hide():
            self.withdraw()
            if not self.tray_thread or not self.tray_thread.is_alive(): self.tray_thread = threading.Thread(target=self.setup_tray_icon, daemon=True); self.tray_thread.start()
        if not self.config.get("tray_notification_shown", False): self._show_tray_notification_dialog(on_close_callback=_hide)
        else: _hide()

    def show_window(self):
        if self.tray_icon: self.tray_icon.stop()
        self.tray_thread = None; self.after(100, self.deiconify); self.lift(); self.focus_force()

    def quit_app(self):
        self.stop_thread.set()
        if self.tray_icon: self.tray_icon.stop()
        if self.process_checker_thread: self.process_checker_thread.join(timeout=1)
        self.destroy(); sys.exit(0)