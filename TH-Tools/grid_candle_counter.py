# Copyright (c) 2024, John Simonis and The Ohio State University
# This code was written by John Simonis for the ThunderHead research project at The Ohio State University.

# Import required libraries and modules
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import openpyxl

# Class that handles the grid adjustment for candle detection
class GridAdjuster:
    def __init__(self, master):
        # Initialize the main application window
        self.master = master
        self.master.title("Candle Grid Adjuster")

        # Set colors for the UI elements
        self.bg_color = "#2E2E2E"
        self.fg_color = "#FFFFFF"
        self.grid_color = "#00FF00"
        self.line_color = "#888888"

        # Configure the main window background color
        self.master.configure(bg=self.bg_color)

        # Create a canvas widget for displaying images and grid points
        self.canvas = tk.Canvas(master, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize grid and image related attributes
        self.grid_points = []
        self.selected_point = None
        self.panning = False
        self.pan_start = None
        self.image = None
        self.photo_image = None
        self.grid_offset = [0, 0]  # Offset for panning the image
        self.scale = 1.0  # Scaling factor for zooming in/out

        # Set grid dimensions (rows and columns)
        self.grid_rows = 6  
        self.grid_cols = 10
        self.candle_grid = None  # Placeholder for storing detected candle positions

        # Add buttons for various functionalities
        load_button = tk.Button(master, text="Load Image", command=self.load_image, bg=self.bg_color, fg=self.fg_color)
        load_button.pack(side=tk.TOP, padx=10, pady=10)

        detect_button = tk.Button(master, text="Detect Candles", command=self.detect_candles, bg=self.bg_color, fg=self.fg_color)
        detect_button.pack(side=tk.TOP, padx=10, pady=10)

        save_button = tk.Button(master, text="Save Candle Grid", command=self.save_candle_grid, bg=self.bg_color, fg=self.fg_color)
        save_button.pack(side=tk.TOP, padx=10, pady=10)

        save_layout_button = tk.Button(master, text="Save Grid Layout", command=self.save_grid_layout, bg=self.bg_color, fg=self.fg_color)
        save_layout_button.pack(side=tk.TOP, padx=10, pady=10)

        load_layout_button = tk.Button(master, text="Load Grid Layout", command=self.load_grid_layout, bg=self.bg_color, fg=self.fg_color)
        load_layout_button.pack(side=tk.TOP, padx=10, pady=10)

        # Bind mouse and keyboard events to their respective handlers
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.pan_image)
        self.canvas.bind("<ButtonRelease-2>", self.end_pan)

        self.master.bind("<Shift_L>", self.shift_pressed)
        self.master.bind("<KeyRelease-Shift_L>", self.shift_released)
        self.master.bind("<Prior>", self.zoom_in)   # Page Up
        self.master.bind("<Next>", self.zoom_out)   # Page Down
        self.shift_held = False  # Boolean to track if Shift key is held down

    # Initialize the grid points based on the image dimensions
    def initialize_grid(self, img_width, img_height):
        self.cell_width = img_width / (self.grid_cols - 1)
        self.cell_height = img_height / (self.grid_rows - 1)
        self.grid_points = [
            (col * self.cell_width, row * self.cell_height)
            for row in range(self.grid_rows)
            for col in range(self.grid_cols)
        ]
        self.draw_grid_points()  # Draw the grid points on the canvas

    # Draw grid points and lines on the canvas
    def draw_grid_points(self):
        self.canvas.delete("all")  # Clear the canvas

        # Draw the image on the canvas, if it exists
        if self.image:
            resized_image = self.image.resize((int(self.image.width * self.scale), int(self.image.height * self.scale)))
            self.photo_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(self.grid_offset[0], self.grid_offset[1], anchor="nw", image=self.photo_image, tags="image")

        # Draw grid points and connecting lines
        for i, (x, y) in enumerate(self.grid_points):
            x = x * self.scale + self.grid_offset[0]
            y = y * self.scale + self.grid_offset[1]
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=self.grid_color, outline=self.fg_color, tags="grid_point")
            if i % self.grid_cols != self.grid_cols - 1:
                next_point = self.grid_points[i + 1]
                nx, ny = next_point
                nx = nx * self.scale + self.grid_offset[0]
                ny = ny * self.scale + self.grid_offset[1]
                self.canvas.create_line(x, y, nx, ny, fill=self.line_color, tags="grid_point")
            if i < len(self.grid_points) - self.grid_cols:
                next_point = self.grid_points[i + self.grid_cols]
                nx, ny = next_point
                nx = nx * self.scale + self.grid_offset[0]
                ny = ny * self.scale + self.grid_offset[1]
                self.canvas.create_line(x, y, nx, ny, fill=self.line_color, tags="grid_point")

    # Load an image and initialize the grid based on the image size
    def load_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if image_path:
            self.image = Image.open(image_path)
            img_width, img_height = self.image.size
            self.grid_offset = [0, 0]  # Reset the offset whenever a new image is loaded
            self.scale = 1.0  # Reset the scale to 1.0
            self.canvas.config(scrollregion=(0, 0, img_width, img_height))
            self.initialize_grid(img_width, img_height)
            self.draw_grid_points()

    # Detect candles in the loaded image based on color thresholds
    def detect_candles(self):
        if not self.image:
            print("No image loaded.")
            return

        # Convert image to OpenCV format for processing
        cv_image = np.array(self.image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        lower_orange = np.array([10, 120, 120])  # Loosened thresholds for better detection
        upper_orange = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # Initialize an empty grid to store candle detection results
        self.candle_grid = np.zeros((self.grid_rows - 1, self.grid_cols - 1), dtype=int)

        # Iterate over each cell in the grid to detect candles
        for row in range(self.grid_rows - 1):
            for col in range(self.grid_cols - 1):
                p1 = self.grid_points[row * self.grid_cols + col]
                p2 = self.grid_points[row * self.grid_cols + col + 1]
                p3 = self.grid_points[(row + 1) * self.grid_cols + col]
                p4 = self.grid_points[(row + 1) * self.grid_cols + col + 1]

                # Calculate the bounding box for the current grid cell
                x_start = min(p1[0], p2[0], p3[0], p4[0]) * self.scale
                y_start = min(p1[1], p2[1], p3[1], p4[1]) * self.scale
                x_end = max(p1[0], p2[0], p3[0], p4[0]) * self.scale
                y_end = max(p1[1], p2[1], p3[1], p4[1]) * self.scale

                # Check if the cell contains any candle-like pixels
                cell = mask[int(y_start):int(y_end), int(x_start):int(x_end)]
                if np.any(cell > 0):
                    self.candle_grid[row, col] = 1

        print(f"Detected Candle Grid:\n{self.candle_grid}")
        self.prompt_candle_correction()  # Prompt the user for manual corrections

    # Zoom in by increasing the scale factor
    def zoom_in(self, event):
        self.scale *= 1.1
        self.draw_grid_points()

    # Zoom out by decreasing the scale factor
    def zoom_out(self, event):
        self.scale /= 1.1
        self.draw_grid_points()

    # Prompt the user to manually correct the candle detection grid
    def prompt_candle_correction(self):
        correction_window = tk.Toplevel(self.master)
        correction_window.title("Correct Candle Detection")
        correction_window.configure(bg=self.bg_color)

        correction_grid = []

        # Create a grid of checkbuttons for manual corrections
        for r in range(self.grid_rows - 1):
            row_widgets = []
            for c in range(self.grid_cols - 1):
                var = tk.IntVar(value=self.candle_grid[r, c])
                checkbutton = tk.Checkbutton(correction_window, variable=var, bg=self.bg_color, fg=self.fg_color, selectcolor=self.bg_color)
                checkbutton.grid(row=r, column=c)
                row_widgets.append(var)
            correction_grid.append(row_widgets)

        # Apply the user's corrections to the candle grid
        def apply_corrections():
            for r in range(self.grid_rows - 1):
                for c in range(self.grid_cols - 1):
                    self.candle_grid[r, c] = correction_grid[r][c].get()
            correction_window.destroy()
            print(f"Corrected Candle Grid:\n{self.candle_grid}")

        apply_button = tk.Button(correction_window, text="Apply Corrections", command=apply_corrections, bg=self.bg_color, fg=self.fg_color)
        apply_button.grid(row=self.grid_rows, columnspan=self.grid_cols - 1)

    # Save the candle detection grid to an Excel file
    def save_candle_grid(self):
        if self.candle_grid is None:
            print("No candle grid to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not save_path:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Write the grid data to the Excel sheet
        for r in range(self.candle_grid.shape[0]):
            for c in range(self.candle_grid.shape[1]):
                sheet.cell(row=r + 1, column=c + 1, value=self.candle_grid[r, c])

        workbook.save(save_path)
        print(f"Candle grid saved to {save_path}")

    # Save the grid layout (positions of grid points) to a file
    def save_grid_layout(self):
        layout_path = filedialog.asksaveasfilename(defaultextension=".npy", filetypes=[("NumPy files", "*.npy")])
        if not layout_path:
            return
        np.save(layout_path, self.grid_points)
        print(f"Grid layout saved to {layout_path}")

    # Load a grid layout from a file
    def load_grid_layout(self):
        layout_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if not layout_path:
            return
        self.grid_points = np.load(layout_path).tolist()
        self.draw_grid_points()
        print(f"Grid layout loaded from {layout_path}")

    # Handle left mouse click event (select grid point or start panning)
    def on_click(self, event):
        if self.panning:
            self.pan_start = [event.x, event.y]
        elif self.shift_held:
            self.pan_start = [event.x, event.y]  # Start moving all points
        else:
            self.selected_point = None
            for i, (x, y) in enumerate(self.grid_points):
                x = x * self.scale + self.grid_offset[0]
                y = y * self.scale + self.grid_offset[1]
                if abs(event.x - x) < 10 and abs(event.y - y) < 10:
                    self.selected_point = i
                    break

    # Handle dragging event (move selected grid point or pan the image)
    def on_drag(self, event):
        if self.panning and self.pan_start is not None:
            dx, dy = event.x - self.pan_start[0], event.y - self.pan_start[1]
            self.grid_offset[0] += dx
            self.grid_offset[1] += dy
            self.pan_start = [event.x, event.y]
            self.draw_grid_points()
        elif self.shift_held and self.pan_start is not None:
            dx, dy = event.x - self.pan_start[0], event.y - self.pan_start[1]
            self.grid_points = [(x + dx / self.scale, y + dy / self.scale) for x, y in self.grid_points]
            self.pan_start = [event.x, event.y]
            self.draw_grid_points()
        elif self.selected_point is not None:
            new_x = (event.x - self.grid_offset[0]) / self.scale
            new_y = (event.y - self.grid_offset[1]) / self.scale
            self.grid_points[self.selected_point] = (new_x, new_y)
            self.draw_grid_points()

    # End the dragging event (reset the panning start position)
    def end_drag(self, event):
        self.pan_start = None

    # Start panning the image
    def start_pan(self, event):
        self.panning = True
        self.pan_start = [event.x, event.y]

    # Handle panning the image with the middle mouse button
    def pan_image(self, event):
        if self.panning and self.pan_start is not None:
            dx, dy = event.x - self.pan_start[0], event.y - self.pan_start[1]
            self.grid_offset[0] += dx
            self.grid_offset[1] += dy
            self.pan_start = [event.x, event.y]
            self.draw_grid_points()

    # End the panning event (reset the panning flag)
    def end_pan(self, event):
        self.panning = False
        self.pan_start = None

    # Handle pressing the Shift key (used for moving all grid points)
    def shift_pressed(self, event):
        self.shift_held = True

    # Handle releasing the Shift key (stop moving all grid points)
    def shift_released(self, event):
        self.shift_held = False

# Main execution block to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = GridAdjuster(root)
    root.mainloop()

