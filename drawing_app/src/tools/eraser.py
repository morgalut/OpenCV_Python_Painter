# C:\Users\Mor\Desktop\drawing_app\drawing_app\src\tools\eraser.py
import cv2
from tools.tool import Tool

class Eraser(Tool):
    def __init__(self, drawing_manager, eraser_size=10, shape="circle"):
        super().__init__(drawing_manager)
        self.eraser_size = eraser_size
        self.eraser_shape = shape  # "circle" or "square"
        self.last_point = None

    def on_press(self, event):
        self.last_point = (event.pos().x(), event.pos().y())
        self.erase_at_point(self.last_point)

    def on_drag(self, event):
        if self.last_point is not None:
            current_point = (event.pos().x(), event.pos().y())
            self.erase_at_point(current_point)
            self.last_point = current_point

    def on_release(self, event):
        self.last_point = None

    def erase_at_point(self, point):
        # Erase by setting the pixel to the background color
        background_color = self.drawing_manager.background_color
        if self.eraser_shape == "circle":
            cv2.circle(self.drawing_manager.image, point, self.eraser_size, background_color, -1)
        elif self.eraser_shape == "square":
            top_left = (point[0] - self.eraser_size // 2, point[1] - self.eraser_size // 2)
            bottom_right = (point[0] + self.eraser_size // 2, point[1] + self.eraser_size // 2)
            cv2.rectangle(self.drawing_manager.image, top_left, bottom_right, background_color, -1)
        self.drawing_manager.update_canvas()

    def set_eraser_size(self, size):
        self.eraser_size = size

    def set_eraser_shape(self, shape):
        if shape in ["circle", "square"]:
            self.eraser_shape = shape
        else:
            raise ValueError("Invalid eraser shape. Use 'circle' or 'square'.")
