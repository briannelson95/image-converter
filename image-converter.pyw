import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import os

def browse_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
    if file_paths:
        input_image_paths.set(file_paths)
        update_output_entries(file_paths)

def update_output_entries(file_paths):
    output_entries = []
    for file_path in file_paths:
        original_name, _ = os.path.splitext(os.path.basename(file_path))
        output_entries.append(original_name)
    output_entries_var.set(output_entries)

def browse_output_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, output_dir)

def convert_images():
    input_paths = input_image_paths.get()
    conversion_type = conversion_var.get()

    try:
        for input_path, output_filename in zip(input_paths, output_entries_var.get()):
            image = Image.open(input_path)

            # Get the output file extension
            output_extension = get_output_extension(conversion_type)

            # Get the output directory
            output_dir = output_dir_entry.get()
            if not output_dir:
                output_dir = os.path.dirname(input_path)

            # Create the full output file path
            output_path = os.path.join(output_dir, f"{output_filename}.{output_extension}")

            if conversion_type == "WebP to JPEG":
                image = image.convert("RGB")
                image.save(output_path, "JPEG")
            elif conversion_type == "WebP to PNG":
                image.save(output_path, "PNG")
            elif conversion_type == "JPEG to PNG":
                image.save(output_path, "PNG")
            elif conversion_type == "JPEG to WebP":
                image.save(output_path, "WEBP")
            elif conversion_type == "PNG to JPEG":
                image = image.convert("RGB")
                image.save(output_path, "JPEG")
            elif conversion_type == "PNG to WebP":
                image.save(output_path, "WEBP")

        result_label.config(text=f"Conversion successful: {conversion_type}")

        # Open the folder containing the converted files if the checkbox is selected
        if open_folder_var.get():
            open_folder(output_dir)
    except Exception as e:
        result_label.config(text=f"Error during conversion: {str(e)}")

def open_folder(path):
    import subprocess
    try:
        subprocess.Popen(["explorer", path])  # Windows
    except Exception:
        try:
            subprocess.Popen(["xdg-open", path])  # Linux
        except Exception:
            try:
                subprocess.Popen(["open", path])  # macOS
            except Exception as e:
                result_label.config(text=f"Error opening folder: {str(e)}")

def get_output_extension(conversion_type):
    extensions = {
        "WebP to JPEG": "jpg",
        "WebP to PNG": "png",
        "JPEG to PNG": "png",
        "JPEG to WebP": "webp",
        "PNG to JPEG": "jpg",
        "PNG to WebP": "webp"
    }
    return extensions.get(conversion_type, "")

def check_conversion_selection(*args):
    # Disable the Convert button and show an error message if no conversion type is selected
    if not conversion_var.get():
        convert_button.config(state=tk.DISABLED)
        result_label.config(text="Please select a conversion type.")
    else:
        convert_button.config(state=tk.NORMAL)
        result_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Calculate the window position to center it on the screen
window_width = 500  # Adjusted width
window_height = 350  # Adjusted height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a frame to contain the widgets
frame = ttk.Frame(root, padding=(10, 10))
frame.grid(row=0, column=0, sticky="nsew")

# Use ttk style for better visual appearance
style = ttk.Style()
style.configure("TButton", padding=(10, 5), font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))
style.configure("TCheckbutton", font=('Helvetica', 12))

# Create and set variables
input_image_paths = tk.StringVar()
conversion_var = tk.StringVar()
open_folder_var = tk.BooleanVar()  # Variable to store the checkbox state
output_entries_var = tk.StringVar()

# Create GUI components with ttk styling
conversion_label = ttk.Label(frame, text="Select Conversion:")
conversion_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))  # Reduced padding on Y-axis

conversion_options = [
    "WebP to JPEG",
    "WebP to PNG",
    "JPEG to PNG",
    "JPEG to WebP",
    "PNG to JPEG",
    "PNG to WebP"
]

conversion_menu = ttk.Combobox(frame, textvariable=conversion_var, values=conversion_options)
conversion_menu.grid(row=0, column=4, columnspan=4, sticky="ew")

input_label = ttk.Label(frame, text="Select Images:")
input_label.grid(row=1, column=0, columnspan=8, sticky="w")

browse_button = ttk.Button(frame, text="Browse", command=browse_images)
browse_button.grid(row=2, column=0, columnspan=8, sticky="ew")

input_listbox = tk.Listbox(frame, listvariable=input_image_paths, selectmode=tk.MULTIPLE, height=5)
input_listbox.grid(row=3, column=0, columnspan=8, sticky="ew")

output_label = ttk.Label(frame, text="Save As:")
output_label.grid(row=4, column=0, sticky="w")

output_entries = ttk.Entry(frame, textvariable=output_entries_var)
output_entries.grid(row=4, column=1, columnspan=7, sticky="ew")  # Span full width

output_dir_label = ttk.Label(frame, text="Output:")
output_dir_label.grid(row=5, column=0, sticky="w")

output_dir_entry = ttk.Entry(frame)
output_dir_entry.grid(row=5, column=1, columnspan=6, sticky="ew")  # Span full width

browse_output_button = ttk.Button(frame, text="Browse", image="", command=browse_output_directory)
browse_output_button.grid(row=5, column=7, sticky="w")

convert_button = ttk.Button(frame, text="Convert", command=convert_images, state=tk.DISABLED)
convert_button.grid(row=6, column=0, columnspan=8, sticky="ew")  # Span full width

open_folder_checkbox = ttk.Checkbutton(frame, text="Open folder after conversion", variable=open_folder_var)
open_folder_checkbox.grid(row=7, column=0, columnspan=8, sticky="w")  # Span full width

result_label = ttk.Label(frame, text="")
result_label.grid(row=8, column=0, columnspan=8, sticky="w")  # Span full width

# Check for conversion selection when the conversion menu changes
conversion_var.trace_add("write", check_conversion_selection)

# Allow the frame to expand to fill the window space
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Expand the frame to fill the width and height of the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start the GUI
root.mainloop()
