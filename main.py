import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

# Global variables
num_rows, num_cols, rect_width, rect_height = 3, 3, 200, 200
drawings = []
draw_mode = "draw"
brush_size = 10  # Initial brush size

def create_grid():
    global canvas_frame, canvas
    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.grid(row=1, column=0, sticky="nsew")
    canvas_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    for i in range(num_rows):
        for j in range(num_cols):
            draw_image = drawings[i * num_cols + j]
            frame = tk.Frame(canvas_frame, width=rect_width, height=rect_height, relief='solid', borderwidth=1)
            frame.grid(row=i, column=j, padx=5, pady=5)
            label = tk.Label(frame, bg='white', width=rect_width, height=rect_height)
            label.pack()
            tk_img = ImageTk.PhotoImage(draw_image)
            label.config(image=tk_img)
            label.image = tk_img
            label.bind('<B1-Motion>', lambda event, l=label, img=draw_image: draw_or_erase(event, l, img))

    canvas_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    

def update_scroll_region():
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    canvas_scrollbar_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas_scrollbar_y.grid(row=1, column=1, sticky="ns")
    canvas_scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas_scrollbar_x.grid(row=2, column=0, sticky="ew")
    canvas.configure(yscrollcommand=canvas_scrollbar_y.set, xscrollcommand=canvas_scrollbar_x.set)
    
    print("Scroll region updated, forehead.")


def open_parameter_window():
    parameter_window = tk.Toplevel(root)
    parameter_window.title("Parameter Settings")

    tk.Label(parameter_window, text="Rows:").grid(row=0, column=0)
    tk.Label(parameter_window, text="Columns:").grid(row=1, column=0)
    tk.Label(parameter_window, text="Width:").grid(row=2, column=0)
    tk.Label(parameter_window, text="Height:").grid(row=3, column=0)

    entry_rows = tk.Entry(parameter_window)
    entry_rows.grid(row=0, column=1)
    entry_rows.insert(0, str(num_rows))

    entry_cols = tk.Entry(parameter_window)
    entry_cols.grid(row=1, column=1)
    entry_cols.insert(0, str(num_cols))

    entry_width = tk.Entry(parameter_window)
    entry_width.grid(row=2, column=1)
    entry_width.insert(0, str(rect_width))

    entry_height = tk.Entry(parameter_window)
    entry_height.grid(row=3, column=1)
    entry_height.insert(0, str(rect_height))

    def update_parameters():
        global num_rows, num_cols, rect_width, rect_height, drawings

        new_num_rows = int(entry_rows.get())
        new_num_cols = int(entry_cols.get())
        new_rect_width = int(entry_width.get())
        new_rect_height = int(entry_height.get())

        new_drawings = []
        for i in range(min(num_rows, new_num_rows)):
            for j in range(min(num_cols, new_num_cols)):
                source_image = drawings[i * num_cols + j]
                resized_image = source_image.resize((new_rect_width, new_rect_height), Image.LANCZOS)
                new_drawings.append(resized_image)

        drawings = new_drawings + [Image.new('RGB', (new_rect_width, new_rect_height), 'white') for _ in range(new_num_rows * new_num_cols - len(new_drawings))]

        num_rows, num_cols, rect_width, rect_height = new_num_rows, new_num_cols, new_rect_width, new_rect_height
        delete_grid()
        create_grid()
        update_scroll_region()

        parameter_window.destroy()


    update_button = tk.Button(parameter_window, text="Update", command=update_parameters)
    update_button.grid(row=4, columnspan=2)

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
    label.image = updated_photo
    drawings[int(label.grid_info()['row']) * num_cols + int(label.grid_info()['column'])] = draw_image

def switch_mode():
    global draw_mode
    if draw_mode == "draw":
        draw_mode = "erase"
        switch_button.config(text="Switch to Drawing Mode")
    else:
        draw_mode = "draw"
        switch_button.config(text="Switch to Erasing Mode")

def update_brush_size(val):
    global brush_size
    brush_size = int(val)

def delete_grid():
    global canvas_frame
    if canvas_frame:
        canvas_frame.destroy()

def clear_all():
    global drawings
    drawings = [Image.new('RGB', (rect_width, rect_height), 'white') for _ in range(num_rows * num_cols)]
    create_grid()
    update_scroll_region()

def export_images():
    directory = filedialog.askdirectory(title="Select Directory to Save Images")
    if directory:
        for i, img in enumerate(drawings):
            img.save(f'{directory}/drawing_{i+1}.png', 'PNG')

root = tk.Tk()
root.title("Whiteboard")

param_button = tk.Button(root, text="Parameter Settings", command=open_parameter_window)
param_button.grid(row=0, column=0)

canvas_frame = tk.Frame(root)
canvas_frame.grid(row=1, column=0, columnspan=16)

drawings = [Image.new('RGB', (rect_width, rect_height), 'white') for _ in range(num_rows * num_cols)]

create_grid()

brush_label = tk.Label(root, text="Brush Size:")
brush_label.grid(row=0, column=1)
brush_slider = tk.Scale(root, from_=1, to=20, orient="horizontal", command=update_brush_size)
brush_slider.set(brush_size)
brush_slider.grid(row=0, column=2)

switch_button = tk.Button(root, text="Switch to Erasing Mode", command=switch_mode)
switch_button.grid(row=0, column=3, padx=10)

clear_button = tk.Button(root, text="Clear All", command=clear_all)
clear_button.grid(row=0, column=4, padx=10)

export_button = tk.Button(root, text="Export Images", command=export_images)
export_button.grid(row=0, column=5, padx=10)

# Configuring row and column weights to make the canvas and scrollbars expandable
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

canvas_scrollbar_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas_scrollbar_y.grid(row=1, column=1, sticky="ns")
canvas_scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
canvas_scrollbar_x.grid(row=2, column=0, sticky="ew")
canvas.configure(yscrollcommand=canvas_scrollbar_y.set, xscrollcommand=canvas_scrollbar_x.set)

root.mainloop()
