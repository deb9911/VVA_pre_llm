import tkinter as tk
from tkinter import colorchooser, filedialog


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.drawing = False
        self.last_x, self.last_y = 0, 0
        self.line_width = 5
        self.color = "black"
        self.eraser_on = False
        self.active_button = None
        self.create_buttons()
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def create_buttons(self):
        self.pen_button = tk.Button(self.root, text="Pen", command=self.use_pen)
        self.pen_button.pack(side=tk.LEFT)
        self.pen_button.config(relief=tk.RAISED)
        self.active_button = self.pen_button
        self.brush_button = tk.Button(self.root, text="Brush", command=self.use_brush)
        self.brush_button.pack(side=tk.LEFT)
        self.color_button = tk.Button(self.root, text="Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)
        self.eraser_button = tk.Button(self.root, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)
        self.save_button = tk.Button(self.root, text="Save", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT)
        self.load_button = tk.Button(self.root, text="Load", command=self.load_canvas)
        self.load_button.pack(side=tk.LEFT)
        self.canvas.bind("<B1-Motion>", self.draw)

    def use_pen(self):
        self.active_button.config(relief=tk.RAISED)
        self.pen_button.config(relief=tk.SUNKEN)
        self.active_button = self.pen_button
        self.drawing = True

    def use_brush(self):
        self.active_button.config(relief=tk.RAISED)
        self.brush_button.config(relief=tk.SUNKEN)
        self.active_button = self.brush_button
        self.drawing = True

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def use_eraser(self):
        self.active_button.config(relief=tk.RAISED)
        self.eraser_button.config(relief=tk.SUNKEN)
        self.eraser_on = True
        self.drawing = True

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_canvas(self):
        file = filedialog.asksaveasfilename(defaultextension=".png")
        self.canvas.postscript(file=file, colormode="color")

    def load_canvas(self):
        file = filedialog.askopenfilename(defaultextension=".png")
        self.canvas.postscript(file=file, colormode="color")

    def draw(self, event):
        if self.drawing:
            if self.eraser_on:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill="white", width=self.line_width)
            else:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill=self.color, width=self.line_width)
            self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.drawing = False
        self.last_x, self.last_y = 0, 0

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    app.mainloop()


