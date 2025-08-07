import customtkinter as ctk
from tkinter import filedialog
import threading
from typing import Callable, Dict, Any, Optional, List
import os
from PIL import Image
from ..core.models import GameProfile

class NavButton(ctk.CTkButton):
    def __init__(self, master: Any, text_key: str, command: Callable, lang_manager: Any, theme: Dict[str, str]):
        self.lang_manager, self.text_key, self.theme, self.is_active = lang_manager, text_key, theme, False
        super().__init__(master, text=lang_manager.get(text_key), command=command, height=40, corner_radius=8, font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), fg_color="transparent", text_color=theme.get('text'), hover_color=theme.get('hover'), anchor="w")
        self.bind("<Enter>", self._on_enter); self.bind("<Leave>", self._on_leave)
    def update_text(self): self.configure(text=self.lang_manager.get(self.text_key))
    def update_theme(self, theme: Dict[str, str]): self.theme = theme; self.set_active(self.is_active)
    def set_active(self, is_active: bool):
        self.is_active = is_active
        self.configure(fg_color=self.theme.get('accent') if is_active else "transparent", text_color=self.theme.get('text_on_accent') if is_active else self.theme.get('text'), hover_color=self.theme.get('accent_hover') if is_active else self.theme.get('hover'))
    def _on_enter(self, event: Any=None):
        if not self.is_active: self.configure(fg_color=self.theme.get('hover'))
    def _on_leave(self, event: Any=None):
        if not self.is_active: self.configure(fg_color="transparent")

class ActionLabel(ctk.CTkLabel):
    def __init__(self, master: Any, text_key: str, command: Callable, color: str, lang_manager: Any):
        self.lang_manager, self.text_key = lang_manager, text_key
        super().__init__(master, text=lang_manager.get(text_key), text_color=color, cursor="hand2", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold", underline=True))
        self.bind("<Button-1>", lambda e: command())
    def update_text(self): self.configure(text=self.lang_manager.get(self.text_key))

class InfoBanner(ctk.CTkFrame):
    def __init__(self, master: Any, text_key: str, lang_manager: Any, theme: Dict[str, str], icon_path: str):
        super().__init__(master, fg_color=theme.get('frame_bg'), border_color=theme.get('frame_border'), border_width=1, corner_radius=8)
        self.lang_manager, self.text_key = lang_manager, text_key
        try:
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(24, 24))
            icon_label = ctk.CTkLabel(self, text="", image=icon_image); icon_label.pack(side="left", padx=(10, 5), pady=10)
        except Exception: pass
        self.text_label = ctk.CTkLabel(self, text=self.lang_manager.get(text_key), font=("Segoe UI", 13), text_color=theme.get('text_secondary'), wraplength=450, justify="left"); self.text_label.pack(side="left", padx=(0, 10), pady=10, fill="x", expand=True)
    def update_language(self): self.text_label.configure(text=self.lang_manager.get(self.text_key))
    def update_theme(self, theme: Dict[str, str]):
        self.configure(fg_color=theme.get('frame_bg'), border_color=theme.get('frame_border'))
        self.text_label.configure(text_color=theme.get('text_secondary'))

class ProfileEditor(ctk.CTkToplevel):
    def __init__(self, master: Any, controller: Any, profile_to_edit: Optional[GameProfile] = None):
        super().__init__(master)
        self.controller, self.profile_to_edit, self.lang, self.theme = controller, profile_to_edit, controller.lang, controller.theme
        title_key = "profile_editor_title_edit" if profile_to_edit else "profile_editor_title_new"
        self.title(self.lang.get(title_key))
        self.geometry("500x350")
        
        # --- CORRECCIÓN DEFINITIVA ---
        if controller.app_icon:
            self.iconphoto(True, controller.app_icon)
            
        self.transient(master)
        self.configure(fg_color=self.theme['bg'])
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        ctk.CTkLabel(self, text=self.lang.get("executable_path_label"), font=self.controller.font_main, text_color=self.theme['text']).pack(padx=20, pady=(15,0), anchor="w")
        path_frame = ctk.CTkFrame(self, fg_color="transparent"); path_frame.pack(fill="x", padx=20)
        self.path_entry = ctk.CTkEntry(path_frame, font=self.controller.font_main, fg_color=self.theme['frame_bg'], border_color=self.theme['frame_border'], text_color=self.theme['text']); self.path_entry.pack(side="left", fill="x", expand=True)
        browse_button = ctk.CTkButton(path_frame, text="...", width=30, font=self.controller.font_main, command=self._browse_file); browse_button.pack(side="right", padx=(5,0))
        ctk.CTkLabel(self, text=self.lang.get("monitor_profile_label"), font=self.controller.font_main, text_color=self.theme['text']).pack(padx=20, pady=(15,0), anchor="w")
        self.monitor_selector = ctk.CTkOptionMenu(self, values=self.controller.monitor_names, font=self.controller.font_main, command=self._update_res_for_monitor); self.monitor_selector.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(self, text=self.lang.get("game_resolution_label"), font=self.controller.font_main, text_color=self.theme['text']).pack(padx=20, pady=(15,0), anchor="w")
        initial_monitor = self.controller.monitor_names[0] if self.controller.monitor_names else None
        self.res_selector = ctk.CTkOptionMenu(self, values=self.controller._get_supported_resolutions(initial_monitor), font=self.controller.font_main); self.res_selector.pack(fill="x", padx=20, pady=5)
        save_button = ctk.CTkButton(self, text=self.lang.get("save_profile_button"), height=40, font=self.controller.font_bold, command=self._save_profile); save_button.pack(pady=20, padx=20, fill="x")
        for widget in [browse_button, save_button]: widget.configure(fg_color=self.theme['accent'], text_color=self.theme['text_on_accent'], hover_color=self.theme['accent_hover'])
        for menu in [self.monitor_selector, self.res_selector]: menu.configure(fg_color=self.theme['frame_bg'], button_color=self.theme['button'], button_hover_color=self.theme['button_hover'], text_color=self.theme['text'])
        if self.profile_to_edit:
            self.path_entry.insert(0, self.profile_to_edit.path); monitor = self.profile_to_edit.monitor or initial_monitor
            self.monitor_selector.set(monitor); self._update_res_for_monitor(monitor); self.res_selector.set(self.profile_to_edit.res)
    def _browse_file(self):
        path = filedialog.askopenfilename(title=self.lang.get("select_executable_title"), filetypes=[("Executable", "*.exe")])
        if path: self.path_entry.delete(0, 'end'); self.path_entry.insert(0, path)
    def _update_res_for_monitor(self, monitor_name: str):
        resolutions = self.controller._get_supported_resolutions(monitor_name)
        self.res_selector.configure(values=resolutions)
        if self.res_selector.get() not in resolutions: self.res_selector.set(resolutions[0] if resolutions else "")
    def _save_profile(self):
        path, res, monitor = self.path_entry.get(), self.res_selector.get(), self.monitor_selector.get()
        if path and res:
            if self.profile_to_edit:
                self.profile_to_edit.path, self.profile_to_edit.res, self.profile_to_edit.monitor, self.profile_to_edit.name = path, res, monitor, os.path.basename(path).replace('.exe','')
            else: self.controller.game_profiles.append(GameProfile(path=path, res=res, monitor=monitor, name=os.path.basename(path).replace('.exe','')))
            self.controller.save_settings(); self.controller.frames["profiles"].refresh_profiles_list(); self.destroy()

class GameScannerWindow(ctk.CTkToplevel):
    def __init__(self, master: Any, controller: Any):
        super().__init__(master)
        self.controller, self.lang, self.theme, self.checkboxes = controller, controller.lang, controller.theme, []
        self.title(self.lang.get("game_scanner_title"))
        self.geometry("600x500")
        if controller.app_icon: self.iconphoto(True, controller.app_icon) # <-- CORRECCIÓN
        self.transient(master)
        self.configure(fg_color=self.theme['bg'])
        self.status_label = ctk.CTkLabel(self, text=self.lang.get("scanner_status_scanning"), font=self.controller.font_main, text_color=self.theme['text']); self.status_label.pack(pady=20)
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=self.theme['frame_bg']); self.scroll_frame.pack(fill="both", expand=True, padx=20)
        self.add_button = ctk.CTkButton(self, text=self.lang.get("scanner_add_selected_button"), state="disabled", fg_color=self.theme['accent'], text_color=self.theme['text_on_accent'], hover_color=self.theme['accent_hover'], command=self._add_selected_games); self.add_button.pack(pady=20)
        threading.Thread(target=self._run_scan, daemon=True).start()
    def _update_ui_with_games(self, games: Dict[str, str]):
        if not games: self.status_label.configure(text=self.lang.get("scanner_no_new_games")); return
        self.status_label.configure(text=self.lang.get("scanner_status_found", count=len(games)))
        for game_name, exe_path in games.items():
            var = ctk.StringVar(value=exe_path)
            cb = ctk.CTkCheckBox(self.scroll_frame, text=f"{game_name}\n({exe_path})", variable=var, onvalue=exe_path, offvalue="", text_color=self.theme['text'], fg_color=self.theme['accent'], checkmark_color=self.theme['text_on_accent']); cb.pack(anchor="w", padx=10, pady=5); self.checkboxes.append(cb)
        self.add_button.configure(state="normal")
    def _add_selected_games(self):
        default_res_list = self.controller._get_supported_resolutions(self.controller.config.get("target_monitor")); default_res = default_res_list[0] if default_res_list else ""
        for cb in self.checkboxes:
            if exe_path := cb.get(): self.controller.game_profiles.append(GameProfile(path=exe_path, res=default_res, monitor=self.controller.config.get("target_monitor"), name=os.path.basename(exe_path).replace('.exe','')))
        self.controller.save_settings(); self.controller.frames["profiles"].refresh_profiles_list(); self.destroy()
    def _run_scan(self):
        found_games = self.controller.engine.scan_all()
        existing_paths = [p.path for p in self.controller.game_profiles]
        new_games = {name: path for name, path in found_games.items() if path not in existing_paths}
        self.after(0, self._update_ui_with_games, new_games)

class HotkeyCaptureWindow(ctk.CTkToplevel):
    def __init__(self, master: Any, controller: Any, button_to_update: ctk.CTkButton):
        super().__init__(master)
        if controller.app_icon: self.iconphoto(True, controller.app_icon) # <-- CORRECCIÓN
        self.controller, self.lang, self.theme, self.button_to_update, self.keys_pressed = controller, controller.lang, controller.theme, button_to_update, []
        self.title(self.lang.get("hotkey_capture_title")); self.geometry("300x100"); self.transient(master); self.configure(fg_color=self.theme['bg'])
        self.label = ctk.CTkLabel(self, text=self.lang.get("hotkey_capture_text"), font=self.controller.font_main, text_color=self.theme['text']); self.label.pack(expand=True)
        import keyboard; self.keyboard = keyboard
        self.hook = self.keyboard.on_press(self._on_key_press, suppress=True)
        self.protocol("WM_DELETE_WINDOW", self._cleanup)
    def _on_key_press(self, event):
        key = event.name
        if key not in self.keys_pressed: self.keys_pressed.append(key); self.label.configure(text=" + ".join(self.keys_pressed).upper())
        self.after(1000, self._finalize_hotkey)
    def _finalize_hotkey(self):
        if hotkey_str := "+".join(self.keys_pressed): self.button_to_update.configure(text=hotkey_str)
        self._cleanup()
    def _cleanup(self): self.keyboard.unhook(self.hook); self.destroy()

class TrayNotificationDialog(ctk.CTkToplevel):
    def __init__(self, master: Any, controller: Any, on_close_callback: Callable):
        super().__init__(master)
        if controller.app_icon: self.iconphoto(True, controller.app_icon) # <-- CORRECCIÓN
        self.controller, self.lang, self.theme, self.on_close_callback = controller, controller.lang, controller.theme, on_close_callback
        self.title(self.lang.get("tray_notice_title")); self.transient(master); self.configure(fg_color=self.theme['bg'])
        main_x, main_y, main_w, main_h = master.winfo_x(), master.winfo_y(), master.winfo_width(), master.winfo_height(); dialog_w, dialog_h = 400, 150
        self.geometry(f"{dialog_w}x{dialog_h}+{main_x + (main_w - dialog_w) // 2}+{main_y + (main_h - dialog_h) // 2}")
        ctk.CTkLabel(self, text=self.lang.get("tray_notice_text"), wraplength=380, font=self.controller.font_main, text_color=self.theme['text']).pack(pady=20, padx=20)
        button = ctk.CTkButton(self, text=self.lang.get("tray_notice_button"), command=self._close_dialog, fg_color=self.theme['accent'], text_color=self.theme['text_on_accent'], hover_color=self.theme['accent_hover']); button.pack(pady=10)
        self.protocol("WM_DELETE_WINDOW", self._close_dialog)
    def _close_dialog(self): self.controller.config["tray_notification_shown"] = True; self.controller.save_settings(); self.destroy(); self.on_close_callback()