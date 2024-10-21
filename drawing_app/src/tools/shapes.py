import cv2
from tools.tool import Tool

class Shapes(Tool):
    def __init__(self, drawing_manager, shape_type='rectangle'):
        super().__init__(drawing_manager)
        self.start_point = None
        self.shape_type = shape_type  # Shape can be 'rectangle' or 'ellipse'

    def on_press(self, event):
        # Capture the start point when the mouse is pressed
        self.start_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_color(self.color)  # Ensure color is set correctly

    def on_drag(self, event):
        # Handle dragging to preview the shape being drawn
        end_point = (event.pos().x(), event.pos().y())

        # Make a copy of the original image to preview the shape without affecting the base
        temp_image = self.drawing_manager.image.copy()

        # Draw the selected shape (rectangle or ellipse)
        if self.shape_type == 'rectangle':
            cv2.rectangle(temp_image, self.start_point, end_point, self.color, self.drawing_manager.thickness)
        elif self.shape_type == 'ellipse':
            center = ((self.start_point[0] + end_point[0]) // 2, (self.start_point[1] + end_point[1]) // 2)
            axes = (abs(self.start_point[0] - end_point[0]) // 2, abs(self.start_point[1] - end_point[1]) // 2)
            cv2.ellipse(temp_image, center, axes, 0, 0, 360, self.color, self.drawing_manager.thickness)

        # Update the canvas with the temporary shape
        self.drawing_manager.update_canvas_with_image(temp_image)
