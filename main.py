"""
Creating simple UI with function to download videos from youtube.
Made by Victor G. Hermogenes AKA Victor Galliardis.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from pytube import YouTube
from tkvideo import tkvideo
import os


def browse_directory():
    download_directory = filedialog.askdirectory(initialdir=".", title="Selecione pasta para download:")
    download_path.set(download_directory)


def display_video_info():
    url = video_url.get()
    if not url:
        messagebox.showerror("Erro:", "Link inválido, por favor tente novamente com outro link.")
        return
    
    try:
        yt = YouTube(url)
        video_title = yt.title
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        video_info_window = Toplevel(root)
        video_info_window.title("Informações do Vídeo")
        video_info_window.configure(bg=bg_color)

        title_label = tk.Label(video_info_window, text=video_title, bg=button_bg_color, fg=fg_color, wraplength=400)
        title_label.pack(pady=10)

        # Download the video for preview purposes
        preview_path = "./preview.mp4"
        stream.download(filename=preview_path)

        # Display the video preview
        video_label = tk.Label(video_info_window)
        video_label.pack(pady=10)
        player = tkvideo(preview_path, video_label, loop=1, size=(400, 300))
        player.play()


        def on_close():
            # Ensure cleanup is done before closing the window
            player._kill_thread = True # might get this workaround deleted later
            video_info_window.destroy()
            root.after(100, cleanup_preview)


        def cleanup_preview():
            try:
                if os.path.exists(preview_path):
                    os.remove(preview_path)
            except Exception as e:
                print(f"Erro em remover preview: {e}")
        

        close_button = tk.Button(video_info_window, text="Fechar", command=on_close, bg=button_bg_color, fg=button_fg_color)
        close_button.pack(pady=10)


        video_info_window.protocol("WM_DELETE_WINDOW", on_close)

    except Exception as e:
        messagebox.showerror("Erro:", f"Ocorreu um erro {e}")


def download_video():
    url = video_url.get()
    folder = download_path.get()
    if not url:
        messagebox.showerror("Erro:", "Video URL invalido.")
        return
    if not folder:
        messagebox.showerror("Error:", "Selecione pasta para download.")
        return
    
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=folder)
        messagebox.showinfo("Sucesso!", f"Video importado com sucesso e salvo na pasta {folder}")
    except Exception as e:
        messagebox.showerror("Erro:", f"Um erro aconteceu: {e}")


def center_window(window, width=500, height=200):
    window.update_idletasks() # Ensre all geometry calculations are up to date

    # calculate required height and width
    widget_heights = sum(widget.winfo_height() for widget in window.winfo_children())
    widget_widths = max(widget.winfo_width() for widget in window.winfo_children())

    # Add padding and extra space for margins
    padding = 20 # Adjust as necesary for aesthetics
    total_height = widget_heights + padding
    total_width = widget_widths + padding

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position to center the window
    x = (screen_width // 2) - (total_width // 2)
    y = (screen_height // 2) - (total_height // 2)

    # Set window geometry
    window.geometry(f'{total_width}x{total_height}+{x}+{y}')


# Adjust the window setup in the main code
def setup_main_window():
    global root
    root = tk.Tk
    root.title("youTube Video Downloader")

    # set youTube dark mode theme
    bg_color = "#181818"
    fg_color = "#FFFFFF"
    button_bg_color = "#282828"
    button_fg_color = "#FFFFFF"

    root.configure(bg=bg_color)

    # Create and set variables
    global video_url, download_path
    video_url = tk.StringVar()
    download_path = tk.StringVar()

    # URL label and entry
    url_label = tk.label(root, text="link do YouTube:", bg=bg_color, fg=fg_color)
    url_label.pack(pady=5)
    url_entry = tk.Entry(root, textvariable=video_url, width=50)
    url_entry.pacl(pady=5)

    # Display video info button
    info_button = tk.Button(root, text="Informações do video", command=display_video_info, bg=button_bg_color, fg=button_fg_color)
    info_button.pack(pady=5)

    # Browse button and entry
    path_label = tk.Label(root, text="Caminho do Download:", bg=bg_color, fg=fg_color)
    path_label.pack(pady=5)
    path_entry = tk.Entry(root, textvariable=download_path, width=50)
    path_entry.pack(pady=5)
    browse_button = tk.Button(root, text="Procurar", command=browse_directory, bg=button_bg_color, fg=button_fg_color)
    browse_button.pack(pady=5)

    # Download button
    download_button = tk.Button(root, text="Download", command=download_video, bg=button_bg_color, fg=button_fg_color)
    download_button.pack(pady=5)

    # center the window after all widgets are packed
    center_window(root)

    # Run the GUI loop
    root.mainloop()


# Initialize the main window
setup_main_window()