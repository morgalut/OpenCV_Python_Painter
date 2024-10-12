import cv2
from tools.tool import Tool

class Circle(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)
        self.center = None

    def on_press(self, event):
        # Capture the center point for the circle
        self.center = (event.pos().x(), event.pos().y())

    def on_drag(self, event):
        if self.center:
            # Calculate the radius dynamically based on the mouse position
            radius = int(((event.pos().x() - self.center[0]) ** 2 + (event.pos().y() - self.center[1]) ** 2) ** 0.5)
            temp_image = self.drawing_manager.image.copy()
            cv2.circle(temp_image, self.center, radius, self.drawing_manager.color, self.drawing_manager.thickness)
            self.drawing_manager.update_canvas_with_image(temp_image)

    def on_release(self, event):
        if self.center:
            radius = int(((event.pos().x() - self.center[0]) ** 2 + (event.pos().y() - self.center[1]) ** 2) ** 0.5)
            self.drawing_manager.draw_ellipse(self.center, (radius, radius))
            self.center = None
