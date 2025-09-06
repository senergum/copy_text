from ocr import recognize_text
from gui.selection import get_selection
from tray.icon import create_tray_icon
from utils.rect import get_all_monitors
import pyperclip
import threading
import keyboard
import time
import ctypes

class TextCapturePro:
    def __init__(self):
        self.is_active = True
        self.hotkey = 'ctrl+alt+c'
        self.monitors = get_all_monitors()
        self.tray_icon = None

    def capture_process(self):
        coords = get_selection(self.monitors)
        if not coords:
            return
        from PIL import ImageGrab
        screenshot = ImageGrab.grab(bbox=coords, all_screens=True)
        text = recognize_text(screenshot)
        if text:
            pyperclip.copy(text)

    def on_hotkey_pressed(self, *args, **kwargs):
        thread = threading.Thread(target=self.capture_process, daemon=True)
        thread.start()

    def run(self):
        if hasattr(ctypes, 'windll'):
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        self.tray_icon = create_tray_icon(self.on_hotkey_pressed, self.exit_app)
        keyboard.add_hotkey(self.hotkey, self.on_hotkey_pressed)
        keyboard.add_hotkey('ctrl+alt+q', self.exit_app)
        while self.is_active:
            time.sleep(0.1)

    def exit_app(self, icon=None, item=None):
        self.is_active = False
        if self.tray_icon:
            self.tray_icon.stop()
        import os
        os._exit(0)