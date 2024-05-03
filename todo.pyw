from tkinter import *
import ctypes
import config


def save_file(text: str) -> None:
    """Save the text to the file"""
    try:
        with open(config.note, "w+") as f:
            f.write(text)
    except IOError as e:
        print(f"Error saving file: {e}")


def on_closing(root: Tk, text_widget: Text) -> None:
    """Handle window closing event"""
    text = text_widget.get("1.0", "end-1c")
    save_file(text)
    root.destroy()


def setup_gui(text: str) -> None:
    """Set up the GUI"""
    root = Tk()
    root.title(config.title)

    # Create a frame to hold the text widget and scrollbar
    frame = Frame(root)
    frame.pack(fill="both", expand=True)

    # Create a text widget with a scrollbar
    text_widget = Text(
        frame,
        height=config.MAX_LINES,
        width=config.MAX_WIDTH,
        bg=config.background,
        font=config.font,
    )
    text_widget.insert(END, text)

    # Create a scrollbar and associate it with the text widget
    scrollbar = Scrollbar(frame, orient="vertical", command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Pack the text widget and scrollbar
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, text_widget))
    root.mainloop()


def open_file() -> tuple:
    """Open the file and return the text"""
    try:
        with open(config.note, "r") as f:
            text = f.read()
            return text
    except IOError as e:
        print(f"Error opening file: {e}")
        return "Error opening notes file!\nOn closing the window the current content is saved in a new file."


if __name__ == "__main__":
    # Make application aware of the system DPI to scale UI accordingly on Windows
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    text = open_file()
    setup_gui(text)
