import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from create_folder import *
from image_func import process_image  # Import image processing functions

#Codes of Lê Quốc Chính

# Global variable to store the file path
file_path = None

width = 900
height = 900


def on_window_resize(event):
    global height, width
    width = root.winfo_width()
    height = root.winfo_height()


def on_frame_configure(event):
    # Update the Canvas's scrollregion when the child frame's size changes
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_image(image, new_width, new_height):
    return cv2.resize(image, (new_width, new_height))


# Create a function to open an image file using a file dialog
def open_image():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", ".jpg;.png;*.jpeg;*.gif;*.bmp;*.tiff")])
    if file_path:
        img = cv2.imread(file_path)
        if img is not None:
            original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            original_image = Image.fromarray(original_image)
            original_image.thumbnail((300, height))
            original_photo = ImageTk.PhotoImage(original_image)
            original_label.config(image=original_photo)
            original_label.image = original_photo
            original_label.pack(expand=True)


# columns
num_columns = 3
out_labels = []


def show_img():
    directory_path = 'output'
    # Get the list of image files in the directory
    image_paths = [os.path.join(directory_path, file) for file in os.listdir(
        directory_path)]
    frame1 = tk.Frame(frame, bg="#27374D")
    frame1.pack()

    for index, image_path in enumerate(image_paths):
        row = index // num_columns
        column = index % num_columns
        # Get the list of image files in the directory
        img = cv2.imread(image_path)
        image_label = tk.Label(frame1,  width=300, height=300)
        if img is not None:
            # Convert colors from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Convert to Pillow image object
            img = Image.fromarray(img)
            img.thumbnail((300, 300))
            # Create image objects using ImageTk
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)  # Image settings for Label
            # Make sure to keep a reference to the image to prevent it from being destroyed
            image_label.image = photo
            # Display images on the interface
            image_label.grid(row=row, column=column, pady=10, padx=10)
            out_labels.append(image_label)

    canvas.update_idletasks()  # Update the actual size of the Canvas
    canvas.configure(scrollregion=canvas.bbox("all"))  # Update scrollregion


# Create a function to apply image processing options
def apply_options():
    if file_path is None:  # Check if file_path has value or not
        tk.messagebox.showinfo("Error", "Please select an image.")
        return

    if file_path:
        selected_options = [option for i, option in enumerate(
            options) if option_vars[i].get() == 1]
        if selected_options:
            output_dir = "output"
            data_dir = "data"
            os.makedirs(output_dir, exist_ok=True)

            files = os.listdir(output_dir)
            for file in files:
                file_output = os.path.join(output_dir, file)
                if os.path.isfile(file_output):
                    os.remove(file_output)

            for i in range(12):
                for i in enumerate(selected_options):
                    processed_image = process_image(
                        file_path, selected_options)

                number = sum(1 for entry in os.scandir(
                    data_dir) if entry.is_file())

                output_path = f"{output_dir}/{number + 1}.jpg"
                data_path = f"{data_dir}/{number + 1}.jpg"
                cv2.imwrite(output_path, processed_image)
                cv2.imwrite(data_path, processed_image)
    show_img()


def delete():
    #Delete current results
    for widget in frame.winfo_children():
        widget.destroy()
    out_labels.clear() 
        

# Create a function to open the 'data' folder
def open_data_folder():
    data_dir = "data"
    if os.path.exists(data_dir):
        # On Windows, use 'explorer' to open a folder
        os.system(f'explorer "{data_dir}"')
    else:
        tk.messagebox.showinfo("Error", "The 'data' folder does not exist.")


# Create a function to confirm exit and delete files
def exit():
    # Delete files in the 'output' directory
    output_dir = "output"
    files = os.listdir(output_dir)
    for file in files:
        file_output = os.path.join(output_dir, file)
        if os.path.isfile(file_output):
            os.remove(file_output)
    root.destroy()


# Create the main tkinter window
root = tk.Tk()
root.geometry("1455x700+30+30")

root.title("Image Processing App")

left_frame = tk.Frame(root, bg="#DDE6ED", width=300, height=600)
left_frame.pack(side="left", fill=tk.Y)

#Create a frame containing search content and results
content_frame = tk.Frame(root, bg="white")
content_frame.pack(expand=True, fill=tk.BOTH)

left_frame1 = tk.Frame(content_frame, bg="#526D82", width=300, height=600)
left_frame1.pack(side="left", fill=tk.Y)
left_frame1.propagate(False)

# Initialize components in results_frame
showimg_frame = tk.Frame(content_frame, bg="white")
showimg_frame.pack(expand=True, fill=tk.BOTH)


# Create a Canvas to contain the result frame and Scrollbar
canvas = tk.Canvas(showimg_frame, bg="#27374D", width=200, height=700)
canvas.pack(side="left", fill="both", expand=True)

vscrollbar = tk.Scrollbar(showimg_frame, orient="vertical",
                          command=canvas.yview)  # Create a vertical Scrollbar
vscrollbar.pack(side="right", fill="y")


# Create a frame to place content
frame = tk.Frame(canvas, bg="#27374D")
canvas.create_window((0, 0), window=frame, anchor="nw")

canvas.configure(yscrollcommand=vscrollbar.set)

canvas.bind("<Configure>", on_frame_configure)


# Create a button to open an image
open_button = tk.Button(left_frame, text="Open Image", command=open_image,
                        bg="#9DB2BF", fg='#191717', font=('helvetica', 12, 'bold'))
open_button.pack(expand=False, fill=tk.X, pady=10, padx=10)

# Create a button to open the 'data' folder
open_data_button = tk.Button(left_frame, text="Open Data Folder", command=open_data_folder,
                             bg="#9DB2BF", fg='#191717', font=('helvetica', 12, 'bold'))
open_data_button.pack(expand=False, fill=tk.X, pady=10, padx=10)


# Create a label to display the original image
original_label = tk.Label(left_frame1)

# Create a frame for options
options_frame = ttk.LabelFrame(left_frame, text="Image Processing Options")
options_frame.pack()
option_vars = []

# Create checkboxes for different image processing options
options = ['crop', 'bright', 'contrast', 'resize', 'color', 'rotate', 'edge detection']
for opt in options:
    option_var = tk.IntVar()
    option_check = ttk.Checkbutton(
        options_frame, text=opt, variable=option_var)
    option_check.pack(fill='x', padx=25, pady=5)
    option_vars.append(option_var)

# Create a button to apply selected options
apply_button = tk.Button(left_frame, text="Apply", command=apply_options,
                         bg="#9DB2BF", fg='#191717', font=('helvetica', 12, 'bold'))
apply_button.pack(expand=False, fill=tk.X, pady=10, padx=10)

# # Create a button to apply selected options
delete_button = tk.Button(left_frame, text="Delete", command=delete,
                          bg="#9DB2BF", fg='#191717', font=('helvetica', 12, 'bold'))
delete_button.pack(expand=False, fill=tk.X, pady=10, padx=10)

# Intercept the closing of the window to confirm exit and delete files
root.protocol("WM_DELETE_WINDOW", exit)
# Attach the "resize" event to the handler function
root.bind("<Configure>", on_window_resize)

root.mainloop()
