import ctypes

class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]

def get_all_monitors():
    monitors = []
    def callback(hmonitor, hdc, lprect, lparam):
        rect = lprect.contents
        monitors.append({
            'left': rect.left,
            'top': rect.top,
            'right': rect.right,
            'bottom': rect.bottom
        })
        return 1
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_ulong)
    ctypes.windll.user32.EnumDisplayMonitors(None, None, callback_type(callback), 0)
    return monitors