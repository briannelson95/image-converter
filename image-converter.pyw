import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.heic")])
    if file_path:
        input_image_path.set(file_path)
        update_preview_image(file_path)

        # Automatically detect file format and set available conversion options
        with Image.open(file_path) as img:
            formats = []
            if img.format == "JPEG":
                formats.extend(["WebP", "PNG"])
            elif img.format == "PNG":
                formats.extend(["WebP", "JPEG"])
            elif img.format == "WebP":
                formats.extend(["JPEG", "PNG"])
            elif img.format == "HEIC":
                formats.extend(["JPEG", "PNG", "WebP"])
            else:
                formats.extend(["WebP", "JPEG", "PNG"])

            conversion_menu['values'] = formats

def browse_output_directory():
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, output_dir)

def convert_image():
    input_path = input_image_path.get()
    conversion_type = conversion_var.get()

    try:
        image = Image.open(input_path)

        # Get the output file name and extension
        output_filename = output_entry.get()
        if not output_filename:
            output_filename, _ = os.path.splitext(os.path.basename(input_path))

        # Get the output directory
        output_dir = output_dir_entry.get()
        if not output_dir:
            output_dir = os.path.dirname(input_path)

        # Create the full output file path
        output_extension = get_output_extension(conversion_type)
        output_path = os.path.join(output_dir, f"{output_filename}.{output_extension}")

        # Check if the file already exists in the output directory
        counter = 1
        while os.path.exists(output_path):
            # File with the same name already exists, prompt the user
            result = messagebox.askyesno(
                "File Already Exists",
                f"A file named '{output_filename}.{output_extension}' already exists in the chosen directory. Do you want to override it?"
            )
            if result:
                # User chose to override the file
                break
            else:
                # User chose not to override the file, add a number to the filename
                counter += 1
                output_filename = f"{output_filename}_{counter}"

            # Update the output path with the new filename
            output_path = os.path.join(output_dir, f"{output_filename}.{output_extension}")

        if conversion_type == "WebP":
            image.save(output_path, "WEBP")
        elif conversion_type == "JPEG":
            image = image.convert("RGB")
            image.save(output_path, "JPEG")
        elif conversion_type == "PNG":
            image.save(output_path, "PNG")
        elif conversion_type == "HEIC":
            image.save(output_path, "JPEG", quality=95)  # Convert .HEIC to .JPEG
        result_label.config(text=f"Conversion successful: {conversion_type}")

        # Open the folder containing the converted file if the checkbox is selected
        if open_folder_var.get():
            os.startfile(output_dir)
    except Exception as e:
        result_label.config(text=f"Error during conversion: {str(e)}")

def get_output_extension(conversion_type):
    extensions = {
        "WebP": "webp",
        "JPEG": "jpg",
        "PNG": "png",
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

def update_preview_image(file_path):
    try:
        image = Image.open(file_path)
        image.thumbnail((200, 200))  # Adjust the size of the preview image
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.photo = photo  # Keep a reference to the photo to prevent garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load the preview image: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Calculate the window position to center it on the screen
window_width = 800  # Adjusted width
window_height = 400  # Adjusted height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Use ttk style for better visual appearance
style = ttk.Style()
style.configure("TButton", padding=(10, 5), font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))
style.configure("TCheckbutton", font=('Helvetica', 12))

# Create and set variables
input_image_path = tk.StringVar()
conversion_var = tk.StringVar()
open_folder_var = tk.BooleanVar()  # Variable to store the checkbox state

# Create GUI components with ttk styling
frame_left = ttk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_right = ttk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

input_label = ttk.Label(frame_left, text="Select an image file:")
input_label.pack(fill=tk.X)

browse_button = ttk.Button(frame_left, text="Browse", command=browse_image)
browse_button.pack(fill=tk.X)

input_entry = ttk.Entry(frame_left, textvariable=input_image_path)
input_entry.pack(fill=tk.X)

preview_label = ttk.Label(frame_left, text="Preview:")
preview_label.pack(fill=tk.X)

# Create a canvas to display the preview image
canvas = tk.Canvas(frame_left, width=200, height=200)
canvas.pack(fill=tk.X)

output_dir_label = ttk.Label(frame_left, text="Output directory:")
output_dir_label.pack(fill=tk.X)

output_dir_entry = ttk.Entry(frame_left)
output_dir_entry.pack(fill=tk.X)

browse_output_button = ttk.Button(frame_left, text="Browse Output Directory", command=browse_output_directory)
browse_output_button.pack(fill=tk.X)

conversion_label = ttk.Label(frame_right, text="Select conversion:")
conversion_label.pack(fill=tk.X)

conversion_menu = ttk.Combobox(frame_right, textvariable=conversion_var, values=[], state="readonly")
conversion_menu.pack(fill=tk.X)

output_label = ttk.Label(frame_right, text="Save as:")
output_label.pack(fill=tk.X)

output_entry = ttk.Entry(frame_right)
output_entry.pack(fill=tk.X)

# Checkbox to open the folder after conversion
open_folder_checkbox = ttk.Checkbutton(frame_right, text="Open folder after conversion", variable=open_folder_var)
open_folder_checkbox.pack(fill=tk.X)

convert_button = ttk.Button(frame_right, text="Convert", command=convert_image, state=tk.DISABLED)
convert_button.pack(fill=tk.X)

result_label = ttk.Label(frame_right, text="", wraplength=200)  # Wrap text to a maximum width of 200 pixels
result_label.pack(fill=tk.X)

# Check for conversion selection when the conversion menu changes
conversion_var.trace_add("write", check_conversion_selection)

# Start the GUI
root.mainloop()
