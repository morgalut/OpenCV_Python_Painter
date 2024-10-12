from tools.tool import Tool

class Pencil(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)
        self.thickness = 1  # Very thin strokes
        self.opacity = 0.5  # Semi-transparent

    def on_press(self, event):
        # Drawing thin and transparent lines
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_thickness(self.thickness)
        self.drawing_manager.set_opacity(self.opacity)
        self.drawing_manager.enable_drawing()


    def on_drag(self, event):
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point is not None:
            self.drawing_manager.draw_line(self.last_point, current_point)
            self.last_point = current_point

    def on_release(self, event):
        self.last_point = None
