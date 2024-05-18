import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# Define the main application class
class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")

        # Center the window
        window_width = 800
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Configure styles
        style = ttk.Style()
        style.configure("TButton", padding=(10, 5), font=('Helvetica', 12))
        style.configure("TLabel", font=('Helvetica', 12))
        style.configure("TCheckbutton", font=('Helvetica', 12))

        # Create frames
        self.mode_frame = ttk.Frame(root)
        self.mode_frame.pack(side=tk.TOP, fill=tk.X)

        self.frame_left = ttk.Frame(root)
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_right = ttk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize variables
        self.is_single_conversion = tk.BooleanVar(value=True)
        self.input_image_path = tk.StringVar()
        self.input_image_paths = tk.StringVar()
        self.conversion_var = tk.StringVar()
        self.open_folder_var = tk.BooleanVar()

        # Create mode buttons
        self.single_mode_button = tk.Button(self.mode_frame, text="Single Conversion", command=self.switch_to_single_conversion, bd=0)
        self.single_mode_button.pack(side=tk.LEFT, padx=10)
        
        self.batch_mode_button = tk.Button(self.mode_frame, text="Batch Conversion", command=self.switch_to_batch_conversion, bd=0)
        self.batch_mode_button.pack(side=tk.LEFT, padx=10)

        # Build initial UI
        self.switch_to_single_conversion()

    def switch_to_single_conversion(self):
        self.clear_frame(self.frame_left)
        self.clear_frame(self.frame_right)
        self.build_single_conversion_ui()
        self.single_mode_button.config(bg='lightblue', fg='black', relief='raised')
        self.batch_mode_button.config(bg=self.root.cget('bg'), fg='black', relief='flat')
        self.is_single_conversion.set(True)

    def switch_to_batch_conversion(self):
        self.clear_frame(self.frame_left)
        self.clear_frame(self.frame_right)
        self.build_batch_conversion_ui()
        self.batch_mode_button.config(bg='lightblue', fg='black', relief='raised')
        self.single_mode_button.config(bg=self.root.cget('bg'), fg='black', relief='flat')
        self.is_single_conversion.set(False)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def build_single_conversion_ui(self):
        input_label = ttk.Label(self.frame_left, text="Select an image file:")
        input_label.pack(fill=tk.X)

        browse_button = ttk.Button(self.frame_left, text="Browse", command=self.browse_image)
        browse_button.pack(fill=tk.X)

        input_entry = ttk.Entry(self.frame_left, textvariable=self.input_image_path)
        input_entry.pack(fill=tk.X)

        preview_label = ttk.Label(self.frame_left, text="Preview:")
        preview_label.pack(fill=tk.X)

        self.canvas = tk.Canvas(self.frame_left, width=200, height=200)
        self.canvas.pack(fill=tk.X)

        browse_output_button = ttk.Button(self.frame_right, text="Choose Output Directory", command=self.browse_output_directory)
        browse_output_button.pack(fill=tk.X)

        output_dir_label = ttk.Label(self.frame_right, text="Output directory:")
        output_dir_label.pack(fill=tk.X)

        self.output_dir_entry = ttk.Entry(self.frame_right)
        self.output_dir_entry.pack(fill=tk.X)

        conversion_label = ttk.Label(self.frame_right, text="Select conversion:")
        conversion_label.pack(fill=tk.X)

        self.conversion_menu = ttk.Combobox(self.frame_right, textvariable=self.conversion_var, values=[], state="readonly")
        self.conversion_menu.pack(fill=tk.X)

        output_label = ttk.Label(self.frame_right, text="Save as:")
        output_label.pack(fill=tk.X)

        self.output_entry = ttk.Entry(self.frame_right)
        self.output_entry.pack(fill=tk.X)

        self.open_folder_checkbox = ttk.Checkbutton(self.frame_right, text="Open folder after conversion", variable=self.open_folder_var)
        self.open_folder_checkbox.pack(fill=tk.X)

        self.convert_button = ttk.Button(self.frame_right, text="Convert", command=self.convert_image, state=tk.DISABLED)
        self.convert_button.pack(fill=tk.X)

        self.result_label = ttk.Label(self.frame_right, text="", wraplength=200)
        self.result_label.pack(fill=tk.X)

        self.conversion_var.trace_add("write", self.check_conversion_selection)

    def build_batch_conversion_ui(self):
        input_label = ttk.Label(self.frame_left, text="Select image files:")
        input_label.pack(fill=tk.X)

        browse_button = ttk.Button(self.frame_left, text="Browse", command=self.browse_images)
        browse_button.pack(fill=tk.X)

        self.input_listbox = tk.Listbox(self.frame_left, listvariable=self.input_image_paths, height=10)
        self.input_listbox.pack(fill=tk.X)

        # Bind event handler to remove selected file from the listbox
        self.input_listbox.bind("<BackSpace>", self.remove_selected_file)
        self.input_listbox.bind("<Button-3>", self.remove_file_popup_menu)

        # Button to clear all files
        clear_all_button = ttk.Button(self.frame_left, text="Clear All", command=self.clear_all_files)
        clear_all_button.pack(fill=tk.X)

        browse_output_button = ttk.Button(self.frame_right, text="Choose Output Directory", command=self.browse_output_directory)
        browse_output_button.pack(fill=tk.X)

        output_dir_label = ttk.Label(self.frame_right, text="Output directory:")
        output_dir_label.pack(fill=tk.X)

        self.output_dir_entry = ttk.Entry(self.frame_right)
        self.output_dir_entry.pack(fill=tk.X)

        conversion_label = ttk.Label(self.frame_right, text="Select conversion:")
        conversion_label.pack(fill=tk.X)

        self.conversion_menu = ttk.Combobox(self.frame_right, textvariable=self.conversion_var, values=["JPEG", "PNG", "WebP"], state="readonly")
        self.conversion_menu.pack(fill=tk.X)

        self.open_folder_checkbox = ttk.Checkbutton(self.frame_right, text="Open folder after conversion", variable=self.open_folder_var)
        self.open_folder_checkbox.pack(fill=tk.X)

        self.convert_button = ttk.Button(self.frame_right, text="Convert", command=self.convert_batch_images, state=tk.DISABLED)
        self.convert_button.pack(fill=tk.X)

        self.result_label = ttk.Label(self.frame_right, text="", wraplength=200)
        self.result_label.pack(fill=tk.X)

        # Spinner for indicating conversion process
        self.spinner = ttk.Spinbox(self.frame_right, from_=0, to=100, state="disabled")
        self.spinner.pack(fill=tk.X, pady=10)

        # Hide the spinner initially
        self.spinner.pack_forget()

        self.conversion_var.trace_add("write", self.check_conversion_selection)

    def clear_all_files(self):
        self.input_listbox.delete(0, tk.END)  # Delete all items from the listbox

    def remove_selected_file(self, event=None):
        selected_index = self.input_listbox.curselection()
        if selected_index:
            self.input_listbox.delete(selected_index)

    def remove_file_popup_menu(self, event):
        # Create a popup menu to remove files
        popup_menu = tk.Menu(self.frame_left, tearoff=0)
        popup_menu.add_command(label="Remove", command=self.remove_selected_file)
        popup_menu.post(event.x_root, event.y_root)


    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.heic, *.HEIC")])
        if file_path:
            self.input_image_path.set(file_path)
            self.update_preview_image(file_path)

            with Image.open(file_path) as img:
                formats = ["JPEG", "PNG", "WebP"]
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

                self.conversion_menu['values'] = formats

    def browse_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.heic *.HEIC")])
        if file_paths:
            self.input_image_paths.set("\n".join(file_paths))

    def browse_output_directory(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, output_dir)

    def convert_image(self):
        if self.is_single_conversion.get():
            self.convert_single_image()
        else:
            self.convert_batch_images()

    def convert_single_image(self):
        input_path = self.input_image_path.get()
        conversion_type = self.conversion_var.get()

        try:
            image = Image.open(input_path)

            output_filename = self.output_entry.get()
            if not output_filename:
                output_filename, _ = os.path.splitext(os.path.basename(input_path))

            output_dir = self.output_dir_entry.get()
            if not output_dir:
                output_dir = os.path.dirname(input_path)

            output_extension = self.get_output_extension(conversion_type)
            output_path = os.path.join(output_dir, f"{output_filename}.{output_extension}")

            counter = 1
            while os.path.exists(output_path):
                result = messagebox.askyesno(
                    "File Already Exists",
                    f"A file named '{output_filename}.{output_extension}' already exists in the chosen directory. Do you want to override it?"
                )
                if result:
                    break
                else:
                    counter += 1
                    output_filename = f"{output_filename}_{counter}"
                output_path = os.path.join(output_dir, f"{output_filename}.{output_extension}")

            if conversion_type == "WebP":
                image.save(output_path, "WEBP")
            elif conversion_type == "JPEG":
                image = image.convert("RGB")
                image.save(output_path, "JPEG")
            elif conversion_type == "PNG":
                image.save(output_path, "PNG")
            elif conversion_type == "HEIC":
                image.save(output_path, "JPEG", quality=95)
            self.result_label.config(text=f"Conversion successful: {conversion_type}")

            if self.open_folder_var.get():
                os.startfile(output_dir)
        except Exception as e:
            self.result_label.config(text=f"Error during conversion: {str(e)}")

    def convert_batch_images(self):
        input_paths = self.input_image_paths.get()
        conversion_type = self.conversion_var.get()

        output_dir = self.output_dir_entry.get()

        try:
            input_paths = eval(input_paths)  # Convert string representation of tuple to actual tuple

            # Clear the selection fields
            self.input_image_paths.set("")

            # If output directory is not specified, create a new folder within the input folder
            if not output_dir:
                input_dir = os.path.dirname(input_paths[0])  # Get the directory of the first input image
                output_dir = os.path.join(input_dir, f"conversion-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")

            os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

            for input_path in input_paths:
                input_path = input_path.strip()  # Remove whitespace
                if not input_path:
                    continue

                print("Input path:", input_path)  # Debug statement

                image = Image.open(input_path)

                print("Image:", image)  # Debug statement

                output_filename, _ = os.path.splitext(os.path.basename(input_path))
                output_extension = self.get_output_extension(conversion_type)
                output_path = os.path.join(output_dir, f"{output_filename}.{output_extension}")

                print("Output path:", output_path)  # Debug statement

                if conversion_type == "WebP":
                    image.save(output_path, "WEBP")
                elif conversion_type == "JPEG":
                    image = image.convert("RGB")
                    image.save(output_path, "JPEG")
                elif conversion_type == "PNG":
                    image.save(output_path, "PNG")
                elif conversion_type == "HEIC":
                    image.save(output_path, "JPEG", quality=95)

            self.result_label.config(text=f"Batch conversion successful: {conversion_type}")

            if self.open_folder_var.get():
                os.startfile(output_dir)
        except Exception as e:
            self.result_label.config(text=f"Error during batch conversion: {str(e)}")


    def get_output_extension(self, conversion_type):
        extensions = {
            "WebP": "webp",
            "JPEG": "jpg",
            "PNG": "png",
        }
        return extensions.get(conversion_type, "")

    def check_conversion_selection(self, *args):
        if not self.conversion_var.get():
            self.convert_button.config(state=tk.DISABLED)
            self.result_label.config(text="Please select a conversion type.")
        else:
            self.convert_button.config(state=tk.NORMAL)
            self.result_label.config(text="")

    def update_preview_image(self, file_path):
        try:
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor='nw', image=photo)
            self.canvas.photo = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the preview image: {str(e)}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
