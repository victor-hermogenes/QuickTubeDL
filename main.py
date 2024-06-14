"""
Creating simple UI with function to download videos from youtube.
Made by Victor G. Hermogenes AKA Victor Galliardis.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Canvas, Frame
from pytube import YouTube
from tkvideo import tkvideo
import threading
import os
import time
import tempfile


def browse_directory() -> None:
    """Looking for directory to download"""
    download_directory = filedialog.askdirectory(initialdir=".", title="Selecione pasta para download:")
    download_path.set(download_directory)


def display_video_info() -> None:
    """Video preview setup"""
    url = video_url.get()
    if not url:
        messagebox.showerror("Erro:", "Link inválido, por favor tente novamente com outro link.")
        return
    
    """Window setup to display video preview"""
    try:
        yt = YouTube(url)
        video_title = yt.title
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        video_info_window = Toplevel(root)
        video_info_window.title("Informações do Vídeo")
        video_info_window.configure(bg=bg_color)

        title_label = tk.Label(video_info_window, text=video_title, bg=button_bg_color, fg=fg_color, wraplength=400)
        title_label.pack(pady=10)

        # Use a temporary directory for preview files
        temp_dir = tempfile.gettempdir()
        preview_path = os.path.join(temp_dir, "preview.mp4")
        stream.download(filename=preview_path)

        """Display the video preview"""
        video_label = tk.Label(video_info_window)
        video_label.pack(pady=10)
        player = tkvideo(preview_path, video_label, loop=1, size=(400, 300))
        player.play()


        def on_close() -> None:
            """Command to run on close of display window to erase preview"""
            """Ensure cleanup is done before closing the window"""
            player._kill_thread = True  # Ensure player stops
            video_info_window.destroy()
            root.after(100, cleanup_preview)

        
        def cleanup_preview() -> None:
            """Cleanup routine to ensure on close command work"""
            time.sleep(0.5)  # Allow some time for the player thread to finish
            try:
                if os.path.exists(preview_path):
                    os.remove(preview_path)
            except Exception as e:
                print(f"Erro em remover preview: {e}")

        close_button = tk.Button(video_info_window, text="Fechar", command=on_close, bg=button_bg_color, fg=button_fg_color)
        close_button.pack(pady=10)

        video_info_window.protocol("WM_DELETE_WINDOW", on_close)

    except Exception as e:
        messagebox.showerror("Erro:", f"Ocorreu um erro: {e}")


def threaded_download(url: str, folder: str):
    """Threading download to GUI not freeze"""
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=folder)
        messagebox.showinfo("Sucesso!", f"Video importado com sucesso e salvo na pasta {folder}")
    except Exception as e:
        messagebox.showerror("Erro:", f"Um erro aconteceu: {e}")


def download_video() -> None:
    """Choosing bin and downloading video."""
    url = video_url.get()
    folder = download_path.get()
    if not url:
        messagebox.showerror("Erro:", "Video URL invalido.")
        return
    if not folder:
        messagebox.showerror("Error:", "Selecione pasta para download.")
        return
    
    """Start the download in a new thread"""
    threading.Thread(target=threaded_download, args=(url, folder)).start()


def setup_main_window() -> None:
    """Setup to main window"""
    global root
    root = tk.Tk()
    root.title("YouTube Video Downloader")

    """Set the window icon"""
    root.iconbitmap('icon.ico')

    """Set YouTube dark mode theme"""
    global bg_color, fg_color, button_bg_color, button_fg_color
    bg_color = "#181818"
    fg_color = "#FFFFFF"
    button_bg_color = "#282828"
    button_fg_color = "#FFFFFF"

    root.configure(bg=bg_color)

    """Create a canvas for background image"""
    canvas = Canvas(root, bg=bg_color)
    canvas.pack(fill="both", expand=True)

    """Load the background image"""
    bg_image = tk.PhotoImage(file='icon.png')
    canvas.bg_image = bg_image  # Keep a reference to avoid garbage collection

    """Create and set variables"""
    global video_url, download_path
    video_url = tk.StringVar()
    download_path = tk.StringVar()

    """URL label and entry"""
    url_label = tk.Label(canvas, text="Link do YouTube:", bg=bg_color, fg=fg_color)
    url_label.pack(pady=5)
    url_entry = tk.Entry(canvas, textvariable=video_url, width=50)
    url_entry.pack(pady=5)

    """Display video info button"""
    info_button = tk.Button(canvas, text="Informações do video", command=display_video_info, bg=button_bg_color, fg=button_fg_color)
    info_button.pack(pady=5)

    """Browse button and entry"""
    path_label = tk.Label(canvas, text="Caminho do Download:", bg=bg_color, fg=fg_color)
    path_label.pack(pady=5)
    path_entry = tk.Entry(canvas, textvariable=download_path, width=50)
    path_entry.pack(pady=5)
    browse_button = tk.Button(canvas, text="Procurar", command=browse_directory, bg=button_bg_color, fg=button_fg_color)
    browse_button.pack(pady=5)

    """Download button"""
    download_button = tk.Button(canvas, text="Download", command=download_video, bg=button_bg_color, fg=button_fg_color)
    download_button.pack(pady=5)

    """Maker's signature"""
    signature_label = tk.Label(canvas, text="Feito por Victor Galliardis", bg=bg_color, fg=fg_color)
    signature_label.pack(side='left', anchor='s', padx=10, pady=10)

    """Center the window after all widgets are packed"""
    root.update_idletasks()  # Ensure all geometry calculations are up to date
    center_window(root)

    """Add the background image to the canvas, centered"""
    center_image_in_canvas(canvas, bg_image)

    """Run the GUI loop"""
    root.mainloop()


# Centering icon for design purposes
def center_image_in_canvas(canvas: Canvas, image: tk.PhotoImage):
    # Calculate the center of the canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    img_width = image.width()
    img_height = image.height()

    x = (canvas_width - img_width) // 2
    y = (canvas_height - img_height) // 2

    # Place the image on the canvas
    canvas.create_image(x, y, anchor='nw', image=image)


# Centering window to adjust for screen being used
def center_window(window: tk.Tk):
    window.update_idletasks()  # Ensure all geometry calculations are up to date

    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the window size
    window_width = min(screen_width, window.winfo_reqwidth())
    window_height = min(screen_height, window.winfo_reqheight())

    # Calculate position to center the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set window geometry
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')


# Initialize the main window
setup_main_window()
