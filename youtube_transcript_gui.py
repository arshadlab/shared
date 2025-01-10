import tkinter as tk
import json
from tkinter import ttk, scrolledtext, messagebox
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, JSONFormatter


def format_timestamp(seconds):
    """Converts a timestamp in seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
def download_youtube_transcript(url, include_timestamps):
    """Downloads the transcript of a YouTube video."""
    try:
        video_id = url.split("=")[1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        if include_timestamps:
            formatter = JSONFormatter()
            transcript = formatter.format_transcript(transcript_list)
            
            transcript_data = json.loads(transcript)
            formatted_transcript = ""
            for segment in transcript_data:
                start_time = segment['start']
                text = segment['text']
                formatted_time = f"[{format_timestamp(start_time)}] "
                formatted_transcript += formatted_time + text + "\n"
            return formatted_transcript
        else:
            formatter = TextFormatter()
            transcript = formatter.format_transcript(transcript_list)
            return transcript

    except Exception as e:
        print(f"Error downloading transcript: {e}")
        return None

def download_and_display_transcript():
    """Gets the URL, downloads the transcript, and displays it."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    include_timestamps = timestamp_var.get()
    transcript = download_youtube_transcript(url, include_timestamps)

    if transcript:
        transcript_text.delete("1.0", tk.END)
        transcript_text.insert(tk.END, transcript)
    else:
        messagebox.showerror("Error", "No transcript found for the video or invalid URL.")

def select_all(event):
    """Select all text in the transcript_text widget."""
    transcript_text.tag_add(tk.SEL, "1.0", tk.END)
    transcript_text.mark_set(tk.INSERT, "1.0")
    transcript_text.see(tk.INSERT)
    return 'break'

def copy(event):
    """Copy selected text to the clipboard."""
    try:
        transcript_text.clipboard_clear()
        transcript_text.clipboard_append(transcript_text.selection_get())
    except tk.TclError:
        pass
    return 'break'

def show_context_menu(event):
    """Displays a context menu for select all and copy."""
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Select All", command=lambda: select_all(None))
    context_menu.add_command(label="Copy", command=lambda: copy(None))
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

# Create main window
root = tk.Tk()
root.title("YouTube Transcript Downloader")

# Configure grid
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=0)
root.rowconfigure(3, weight=1)

# URL Label
url_label = ttk.Label(root, text="Enter YouTube Video URL:")
url_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")

# URL Entry
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=0, pady=10, sticky="ew")

# Timestamp Checkbox
timestamp_var = tk.BooleanVar(value=False)  # Default is unchecked
timestamp_checkbox = ttk.Checkbutton(root, text="Include Timestamps", variable=timestamp_var)
timestamp_checkbox.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")

# Download Button
download_button = ttk.Button(root, text="Download Transcript", command=download_and_display_transcript)
download_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Transcript Label
transcript_label = ttk.Label(root, text="Transcript:")
transcript_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

# Transcript Text Area
transcript_text = tk.Text(root, wrap=tk.WORD, width=60, height=20)
transcript_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Scrollbar
scrollbar = ttk.Scrollbar(root, command=transcript_text.yview)
scrollbar.grid(row=3, column=3, sticky='nsew')
transcript_text['yscrollcommand'] = scrollbar.set

# Bindings for select all and copy
transcript_text.bind("<Control-a>", select_all)
transcript_text.bind("<Control-A>", select_all)
transcript_text.bind("<Button-3>", lambda e: show_context_menu(e))
transcript_text.bind("<Control-c>", copy)
transcript_text.bind("<Control-C>", copy)

# Start the GUI
root.mainloop()
