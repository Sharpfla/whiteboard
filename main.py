import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

# Global variables
num_rows, num_cols, rect_width, rect_height = 3, 3, 200, 200
scale_factor = 1.0  # Initial scale factor
drawings = []
draw_mode = "draw"
brush_size = 10  # Initial brush size

# Function to handle drawing or erasing within rectangles
def draw_or_erase(event, label, draw_image):
    x, y = event.x, event.y
    draw = ImageDraw.Draw(draw_image)
    if draw_mode == "draw":
        draw.ellipse((x - brush_size, y - brush_size, x + brush_size, y + brush_size), fill='black')
    else:
        draw.rectangle((x - brush_size, y - brush_size, x + brush_size, y + brush_size), fill='white')
    del draw
    updated_photo = ImageTk.PhotoImage(draw_image)
    label.config(image=updated_photo)
    label.image = updated_photo  # Keep a reference
    drawings[int(label.grid_info()['row']) * num_cols + int(label.grid_info()['column'])] = draw_image  # Update the drawn image

# Function to switch between drawing and erasing modes
def switch_mode():
    global draw_mode
    if draw_mode == "draw":
        draw_mode = "erase"
        switch_button.config(text="Switch to Drawing Mode")
    else:
        draw_mode = "draw"
        switch_button.config(text="Switch to Erasing Mode")

# Function to clear all drawings
def clear_all():
    global drawings
    drawings = [Image.new('RGB', (rect_width, rect_height), 'white') for _ in range(num_rows * num_cols)]
    create_grid()

# Function to export images
def export_images():
    directory = filedialog.askdirectory(title="Select Directory to Save Images")
    if directory:
        for i, img in enumerate(drawings):
            img.save(f'{directory}/drawing_{i+1}.png', 'PNG')

# Function to update global variables and redraw grid
def update_variables():
    global num_rows, num_cols, rect_width, rect_height
    num_rows = int(entry_rows.get())
    num_cols = int(entry_cols.get())
    rect_width = int(entry_width.get())
    rect_height = int(entry_height.get())
    clear_all()

# Function to update brush size
def update_brush_size(val):
    global brush_size
    brush_size = int(val)

# Function to create the drawing grid
def create_grid():
    for i in range(num_rows):
        for j in range(num_cols):
            draw_image = drawings[i * num_cols + j]
            frame = tk.Frame(root, width=rect_width, height=rect_height, relief='solid', borderwidth=1)
            frame.grid(row=i+1, column=j)
            label = tk.Label(frame, bg='white', width=rect_width, height=rect_height)
            label.pack()
            tk_img = ImageTk.PhotoImage(draw_image)
            label.config(image=tk_img)
            label.image = tk_img  # Keep a reference
            label.bind('<B1-Motion>', lambda event, l=label, img=draw_image: draw_or_erase(event, l, img))

# Create main window
root = tk.Tk()
root.title("Simple Drawing Program")

# UI elements to modify global variables
label_rows = tk.Label(root, text="Rows:")
label_rows.grid(row=0, column=0)
entry_rows = tk.Entry(root)
entry_rows.grid(row=0, column=1)
entry_rows.insert(0, str(num_rows))

label_cols = tk.Label(root, text="Columns:")
label_cols.grid(row=0, column=2)
entry_cols = tk.Entry(root)
entry_cols.grid(row=0, column=3)
entry_cols.insert(0, str(num_cols))

label_width = tk.Label(root, text="Width:")
label_width.grid(row=0, column=4)
entry_width = tk.Entry(root)
entry_width.grid(row=0, column=5)
entry_width.insert(0, str(rect_width))

label_height = tk.Label(root, text="Height:")
label_height.grid(row=0, column=6)
entry_height = tk.Entry(root)
entry_height.grid(row=0, column=7)
entry_height.insert(0, str(rect_height))

update_button = tk.Button(root, text="Update", command=update_variables)
update_button.grid(row=0, column=8)

# Brush size slider
label_brush = tk.Label(root, text="Brush Size:")
label_brush.grid(row=0, column=9)
brush_slider = tk.Scale(root, from_=1, to=20, orient="horizontal", command=update_brush_size)
brush_slider.set(brush_size)
brush_slider.grid(row=0, column=10)

# Buttons for switching drawing/erasing modes, clearing all drawings, and exporting images
switch_button = tk.Button(root, text="Switch to Erasing Mode", command=switch_mode)
switch_button.grid(row=0, column=11, columnspan=2)

clear_button = tk.Button(root, text="Clear All", command=clear_all)
clear_button.grid(row=0, column=13, columnspan=2)

export_button = tk.Button(root, text="Export Images", command=export_images)
export_button.grid(row=0, column=15, columnspan=2)

# Initialize drawings list
drawings = [Image.new('RGB', (rect_width, rect_height), 'white') for _ in range(num_rows * num_cols)]

# Create initial drawing grid
create_grid()

root.mainloop()
