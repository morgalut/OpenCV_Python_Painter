import cv2
from tools.tool import Tool

class Line(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)  # Initialize base Tool class
        self.start_point = None

    def on_press(self, event):
        # Capture the start point when the mouse is pressed
        self.start_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_thickness(self.drawing_manager.thickness)  # Ensure thickness is set

    def on_drag(self, event):
        if self.start_point:
            end_point = (event.pos().x(), event.pos().y())
            temp_image = self.drawing_manager.image.copy()  # Copy the image to preview
            cv2.line(temp_image, self.start_point, end_point, self.drawing_manager.color, self.drawing_manager.thickness)
            self.drawing_manager.update_canvas_with_image(temp_image)

    def on_release(self, event):
        end_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.draw_line(self.start_point, end_point)
        self.start_point = None

