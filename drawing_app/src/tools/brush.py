from tools.tool import Tool

class Brush(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)
        self.thickness = 10  # Thick brush
        self.texture = "bristle"  # Example texture

    def on_press(self, event):
        # Drawing thick lines with texture
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_thickness(self.thickness)
        self.drawing_manager.enable_drawing()

    def on_drag(self, event):
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point is not None:
            self.drawing_manager.draw_line(self.last_point, current_point)
            self.last_point = current_point

    def on_release(self, event):
        self.last_point = None
        self.drawing_manager.disable_drawing()  # Renamed method
