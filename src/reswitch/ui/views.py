import customtkinter as ctk
import os
from typing import Any, Dict
from .widgets import ActionLabel, InfoBanner
from ..utils import helpers

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent: Any, controller: Any):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.lang = controller.lang
        self.grid_columnconfigure(0, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        self.home_title_label = ctk.CTkLabel(self, text="", font=self.controller.font_title, anchor="w")
        self.home_title_label.grid(row=0, column=0, sticky="ew", pady=(10, 0))
        self.home_subtitle_label = ctk.CTkLabel(self, text="", font=self.controller.font_subtitle, anchor="w")
        self.home_subtitle_label.grid(row=1, column=0, sticky="ew", pady=(0, 30))
        self.quick_switch_title_label = ctk.CTkLabel(self, text="", font=self.controller.font_bold, anchor="w")
        self.quick_switch_title_label.grid(row=2, column=0, sticky="ew", pady=(10, 5))
        self.res_frame = ctk.CTkFrame(self, corner_radius=10)
        self.res_frame.grid(row=3, column=0, sticky="ew")
        self.res_frame.grid_columnconfigure((1, 3), weight=1)
        self.desktop_res_text_label = ctk.CTkLabel(self.res_frame, text="", font=self.controller.font_main)
        self.desktop_res_text_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.desktop_res_selector = ctk.CTkOptionMenu(self.res_frame, values=[], height=35, font=self.controller.font_main, dropdown_font=self.controller.font_main)
        self.desktop_res_selector.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        self.game_res_text_label = ctk.CTkLabel(self.res_frame, text="", font=self.controller.font_main)
        self.game_res_text_label.grid(row=0, column=2, padx=(30, 15), pady=15, sticky="w")
        self.game_res_selector = ctk.CTkOptionMenu(self.res_frame, values=[], height=35, font=self.controller.font_main, dropdown_font=self.controller.font_main)
        self.game_res_selector.grid(row=0, column=3, padx=15, pady=15, sticky="ew")
        self.switch_button = ctk.CTkButton(self, text="", command=self.controller.quick_switch, height=50, font=self.controller.font_bold)
        self.switch_button.grid(row=4, column=0, sticky="ew", pady=(20, 0))

    def update_language(self):
        self.home_title_label.configure(text=self.lang.get("home_title"))
        self.home_subtitle_label.configure(text=self.lang.get("home_subtitle"))
        self.quick_switch_title_label.configure(text=self.lang.get("quick_switch_title"))
        self.desktop_res_text_label.configure(text=self.lang.get("desktop_res_label"))
        self.game_res_text_label.configure(text=self.lang.get("game_res_label"))
        self.switch_button.configure(text=self.lang.get("switch_button"))
    
    def update_theme(self, theme: Dict[str, str]):
        self.home_title_label.configure(text_color=theme['text'])
        self.home_subtitle_label.configure(text_color=theme['text_secondary'])
        self.quick_switch_title_label.configure(text_color=theme['text'])
        self.res_frame.configure(fg_color=theme['frame_bg'], border_color=theme['frame_border'])
        self.desktop_res_text_label.configure(text_color=theme['text'])
        self.game_res_text_label.configure(text_color=theme['text'])
        for selector in [self.desktop_res_selector, self.game_res_selector]:
            selector.configure(fg_color=theme['frame_bg'], button_color=theme['button'], button_hover_color=theme['button_hover'], text_color=theme['text'])
        self.switch_button.configure(fg_color=theme['accent'], text_color=theme['text_on_accent'], hover_color=theme['accent_hover'])

class ProfilesFrame(ctk.CTkFrame):
    def __init__(self, parent: Any, controller: Any):
        super().__init__(parent, fg_color="transparent")
        self.controller, self.lang, self.theme = controller, controller.lang, controller.theme
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 0))
        header_frame.grid_columnconfigure(0, weight=1)
        self.profiles_title_label = ctk.CTkLabel(header_frame, text="", font=self.controller.font_title, anchor="w")
        self.profiles_title_label.grid(row=0, column=0, sticky="w")
        button_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_container.grid(row=0, column=1, sticky="e")
        self.scan_games_button = ctk.CTkButton(button_container, text="", command=self.controller.open_game_scanner_window, height=40, font=self.controller.font_bold)
        self.scan_games_button.pack(side="left", padx=(0, 10))
        self.add_profile_button = ctk.CTkButton(button_container, text="", command=self.controller.open_profile_editor, height=40, font=self.controller.font_bold)
        self.add_profile_button.pack(side="left")
        self.list_container = ctk.CTkFrame(self, corner_radius=8)
        self.list_container.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        self.profiles_list_frame = ctk.CTkScrollableFrame(self.list_container, fg_color="transparent")
        self.profiles_list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.profiles_list_frame.grid_columnconfigure(0, weight=1)
        icon_path = helpers.resource_path("info_icon.png")
        self.info_banner = InfoBanner(self, text_key="fullscreen_warning", lang_manager=self.lang, theme=self.theme, icon_path=icon_path)
        self.info_banner.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    def update_language(self):
        self.profiles_title_label.configure(text=self.lang.get("profiles_title"))
        self.scan_games_button.configure(text=self.lang.get("scan_games_button"))
        self.add_profile_button.configure(text=self.lang.get("add_profile_button"))
        self.info_banner.update_language()
        self.refresh_profiles_list()
    
    def update_theme(self, theme: Dict[str, str]):
        self.theme = theme
        self.profiles_title_label.configure(text_color=theme['text'])
        self.scan_games_button.configure(fg_color=theme['accent'], text_color=theme['text_on_accent'], hover_color=theme['accent_hover'])
        self.add_profile_button.configure(fg_color=theme['accent'], text_color=theme['text_on_accent'], hover_color=theme['accent_hover'])
        self.list_container.configure(fg_color=theme['frame_bg'], border_color=theme['frame_border'])
        # --- CORRECCIÓN: Se actualiza el color de fondo del scrollable frame ---
        self.profiles_list_frame.configure(fg_color=theme['frame_bg'])
        self.info_banner.update_theme(theme)
        self.refresh_profiles_list()

    def refresh_profiles_list(self):
        for widget in self.profiles_list_frame.winfo_children(): widget.destroy()
        if not self.controller.game_profiles:
            placeholder_frame = ctk.CTkFrame(self.profiles_list_frame, fg_color="transparent")
            placeholder_frame.pack(expand=True, fill="both", padx=20, pady=20)
            ctk.CTkLabel(placeholder_frame, text=self.lang.get("no_profiles_text"), font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=self.theme['text_secondary']).pack(pady=(0, 5))
            ctk.CTkLabel(placeholder_frame, text=self.lang.get("no_profiles_subtext"), font=self.controller.font_subtitle, text_color=self.theme['text_secondary']).pack()
        else:
            list_header_frame = ctk.CTkFrame(self.profiles_list_frame, fg_color="transparent", height=30)
            list_header_frame.pack(fill="x", padx=10, pady=(5, 0))
            list_header_frame.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(list_header_frame, text=self.lang.get("list_header_game"), font=self.controller.font_small, text_color=self.theme['text_secondary']).grid(row=0, column=0, padx=(50, 0))
            ctk.CTkLabel(list_header_frame, text=self.lang.get("list_header_resolution"), font=self.controller.font_small, text_color=self.theme['text_secondary']).grid(row=0, column=2, padx=(0, 120))
            for profile in self.controller.game_profiles:
                p_frame = ctk.CTkFrame(self.profiles_list_frame, height=50, fg_color=self.theme['bg_secondary'], border_color=self.theme['frame_border'], border_width=1, corner_radius=8)
                p_frame.pack(fill="x", padx=5, pady=4)
                p_frame.grid_columnconfigure(1, weight=1)
                icon = helpers.get_icon_from_exe(profile.path)
                ctk.CTkLabel(p_frame, text="", image=icon).grid(row=0, column=0, padx=10, pady=10)
                game_name = profile.name or os.path.basename(profile.path).replace('.exe', '')
                ctk.CTkLabel(p_frame, text=game_name, font=self.controller.font_bold, text_color=self.theme['text']).grid(row=0, column=1, sticky="w", padx=10)
                ctk.CTkLabel(p_frame, text=profile.res, font=self.controller.font_main, text_color=self.theme['text']).grid(row=0, column=2, padx=40)
                actions_frame = ctk.CTkFrame(p_frame, fg_color="transparent")
                actions_frame.grid(row=0, column=3, padx=10)
                ActionLabel(actions_frame, "edit_button", lambda p=profile: self.controller.open_profile_editor(p), color=self.theme['accent'], lang_manager=self.lang).pack(side="left", padx=5)
                ActionLabel(actions_frame, "delete_button", lambda p=profile: self.controller.delete_profile(p), color=self.theme.get('error', '#e74c3c'), lang_manager=self.lang).pack(side="left", padx=5)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent: Any, controller: Any):
        super().__init__(parent, fg_color="transparent")
        self.controller, self.lang = controller, controller.lang
        self.grid_columnconfigure((0, 1), weight=1)
        self._create_widgets()
    
    def _create_widgets(self):
        self.settings_title_label = ctk.CTkLabel(self, text="", font=self.controller.font_title, anchor="w")
        self.settings_title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 20))
        self.left_col = ctk.CTkFrame(self, fg_color="transparent")
        self.left_col.grid(row=1, column=0, sticky="new", padx=(0, 10))
        self.appearance_frame = ctk.CTkFrame(self.left_col)
        self.appearance_frame.pack(fill="x", pady=10, anchor="n")
        self.appearance_label = ctk.CTkLabel(self.appearance_frame, text="", font=self.controller.font_bold)
        self.appearance_label.pack(padx=15, pady=(10, 5), anchor="w")
        self.appearance_mode_selector = ctk.CTkOptionMenu(self.appearance_frame, values=[], command=self.controller.change_appearance_mode, height=35, font=self.controller.font_main, dropdown_font=self.controller.font_main)
        self.appearance_mode_selector.pack(fill="x", padx=15, pady=10)
        self.startup_frame = ctk.CTkFrame(self.left_col)
        self.startup_frame.pack(fill="x", pady=10, anchor="n")
        self.startup_options_label = ctk.CTkLabel(self.startup_frame, text="", font=self.controller.font_bold)
        self.startup_options_label.pack(padx=15, pady=(10, 5), anchor="w")
        self.start_win_var = ctk.BooleanVar()
        self.start_win_check = ctk.CTkCheckBox(self.startup_frame, text="", variable=self.start_win_var, font=self.controller.font_main)
        self.start_win_check.pack(padx=15, pady=15, anchor="w")
        self.lang_frame = ctk.CTkFrame(self.left_col)
        self.lang_frame.pack(fill="x", pady=10, anchor="n")
        self.language_text_label = ctk.CTkLabel(self.lang_frame, text="", font=self.controller.font_bold)
        self.language_text_label.pack(padx=15, pady=(10, 5), anchor="w")
        self.language_selector = ctk.CTkOptionMenu(self.lang_frame, values=["English", "Español", "中文"], command=self.controller.change_language, font=self.controller.font_main, dropdown_font=self.controller.font_main, height=35)
        self.language_selector.pack(fill="x", padx=15, pady=10)
        self.right_col = ctk.CTkFrame(self, fg_color="transparent")
        self.right_col.grid(row=1, column=1, sticky="new", padx=(10, 0))
        self.monitor_frame = ctk.CTkFrame(self.right_col)
        self.monitor_frame.pack(fill="x", pady=10, anchor="n")
        self.monitor_text_label = ctk.CTkLabel(self.monitor_frame, text="", font=self.controller.font_bold)
        self.monitor_text_label.pack(padx=15, pady=(10, 5), anchor="w")
        self.monitor_selector = ctk.CTkOptionMenu(self.monitor_frame, values=[], command=self.controller.on_monitor_change, height=35, font=self.controller.font_main, dropdown_font=self.controller.font_main)
        self.monitor_selector.pack(fill="x", padx=15, pady=10)
        self.hotkey_frame = ctk.CTkFrame(self.right_col)
        self.hotkey_frame.pack(fill="x", pady=10, anchor="n")
        self.hotkey_frame.grid_columnconfigure(1, weight=1)
        self.hotkeys_text_label = ctk.CTkLabel(self.hotkey_frame, text="", font=self.controller.font_bold)
        self.hotkeys_text_label.grid(row=0, column=0, columnspan=2, pady=(10, 15), padx=15, sticky="w")
        self.desktop_hotkey_text_label = ctk.CTkLabel(self.hotkey_frame, text="", font=self.controller.font_main)
        self.desktop_hotkey_text_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.desktop_hotkey_entry = ctk.CTkButton(self.hotkey_frame, text="", command=lambda: self.controller.capture_hotkey(self.desktop_hotkey_entry))
        self.desktop_hotkey_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")
        self.game_hotkey_text_label = ctk.CTkLabel(self.hotkey_frame, text="", font=self.controller.font_main)
        self.game_hotkey_text_label.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.game_hotkey_entry = ctk.CTkButton(self.hotkey_frame, text="", command=lambda: self.controller.capture_hotkey(self.game_hotkey_entry))
        self.game_hotkey_entry.grid(row=2, column=1, padx=15, pady=10, sticky="ew")
        self.save_settings_button = ctk.CTkButton(self, text="", command=self.controller.save_settings, height=40, font=self.controller.font_bold)
        self.save_settings_button.grid(row=2, column=1, sticky="se", pady=20, padx=(10, 0))

    def update_language(self):
        self.settings_title_label.configure(text=self.lang.get("settings_title"))
        self.appearance_label.configure(text=self.lang.get("appearance_label"))
        self.startup_options_label.configure(text=self.lang.get("startup_options_label"))
        self.start_win_check.configure(text=self.lang.get("start_with_windows"))
        self.language_text_label.configure(text=self.lang.get("language_label"))
        self.monitor_text_label.configure(text=self.lang.get("monitor_label"))
        self.hotkeys_text_label.configure(text=self.lang.get("hotkeys_label"))
        self.desktop_hotkey_text_label.configure(text=self.lang.get("desktop_hotkey"))
        self.game_hotkey_text_label.configure(text=self.lang.get("game_hotkey"))
        self.save_settings_button.configure(text=self.lang.get("save_settings_button"))

    def update_theme(self, theme: Dict[str, str]):
        self.settings_title_label.configure(text_color=theme['text'])
        for frame in [self.appearance_frame, self.startup_frame, self.lang_frame, self.monitor_frame, self.hotkey_frame]:
            frame.configure(fg_color=theme['frame_bg'], border_color=theme['frame_border'])
        for label in [self.appearance_label, self.startup_options_label, self.language_text_label, self.monitor_text_label, self.hotkeys_text_label, self.desktop_hotkey_text_label, self.game_hotkey_text_label]:
            label.configure(text_color=theme['text'])
        for menu in [self.appearance_mode_selector, self.language_selector, self.monitor_selector]:
            menu.configure(fg_color=theme['frame_bg'], button_color=theme['button'], button_hover_color=theme['button_hover'], text_color=theme['text'])
        self.start_win_check.configure(text_color=theme['text'], fg_color=theme['accent'], checkmark_color=theme['text_on_accent'])
        for button in [self.desktop_hotkey_entry, self.game_hotkey_entry]:
            button.configure(fg_color=theme['button'], text_color=theme['text'], hover_color=theme['button_hover'])
        self.save_settings_button.configure(fg_color=theme['accent'], text_color=theme['text_on_accent'], hover_color=theme['accent_hover'])