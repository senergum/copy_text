import tkinter as tk
import keyboard

def get_selection(monitors):
    root = tk.Tk()
    root.attributes('-alpha', 0.2)
    root.configure(bg='black')
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    total_width = sum(monitor['right'] - monitor['left'] for monitor in monitors)
    total_height = max(monitor['bottom'] - monitor['top'] for monitor in monitors)
    root.geometry(f"{total_width}x{total_height}+0+0")
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    start_x, start_y = None, None
    rect = None
    coords = None
    selection_cancelled = False
    def close_window():
        nonlocal selection_cancelled
        selection_cancelled = True
        root.quit()
    def on_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=3, fill='blue', stipple='gray50')
    def on_drag(event):
        if rect:
            canvas.coords(rect, start_x, start_y, event.x, event.y)
    def on_release(event):
        nonlocal coords
        if rect:
            x1, y1, x2, y2 = canvas.coords(rect)
            coords = (int(min(x1, x2)), int(min(y1, y2)), int(max(x1, x2)), int(max(y1, y2)))
        root.quit()
    canvas.bind('<Button-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)
    root.bind('<Escape>', lambda event: close_window())
    esc_hook = keyboard.add_hotkey('esc', close_window)
    root.mainloop()
    keyboard.remove_hotkey(esc_hook)
    root.destroy()
    return None if selection_cancelled else coords