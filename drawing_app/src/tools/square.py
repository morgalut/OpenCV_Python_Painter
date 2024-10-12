import cv2
from tools.tool import Tool

class Square(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)
        self.start_point = None

    def on_press(self, event):
        # Capture the starting point for the square
        self.start_point = (event.pos().x(), event.pos().y())

    def on_drag(self, event):
        if self.start_point:
            # Calculate the side length based on the current mouse position
            end_point = (event.pos().x(), event.pos().y())
            side_length = min(abs(end_point[0] - self.start_point[0]), abs(end_point[1] - self.start_point[1]))
            temp_image = self.drawing_manager.image.copy()
            cv2.rectangle(temp_image, self.start_point, 
                          (self.start_point[0] + side_length, self.start_point[1] + side_length),
                          self.drawing_manager.color, self.drawing_manager.thickness)
            self.drawing_manager.update_canvas_with_image(temp_image)

    def on_release(self, event):
        if self.start_point:
            end_point = (event.pos().x(), event.pos().y())
            side_length = min(abs(end_point[0] - self.start_point[0]), abs(end_point[1] - self.start_point[1]))
            self.drawing_manager.draw_rectangle(self.start_point, 
                                                (self.start_point[0] + side_length, self.start_point[1] + side_length))
            self.start_point = None
