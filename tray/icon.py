import pystray
from pystray import MenuItem as item
from PIL import Image as PILImage
import threading
import os

def create_tray_icon(capture_callback, exit_callback):
    image_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'icon.ico')
    if os.path.exists(image_path):
        image = PILImage.open(image_path)
    else:
        image = PILImage.new('RGB', (64, 64), 'blue')
    menu = (
        item('Захватить текст (Ctrl+Alt+C)', capture_callback),
        item('Выход', exit_callback)
    )
    tray_icon = pystray.Icon('text_capture', image, 'Text Capture Pro', menu)
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()
    return tray_icon