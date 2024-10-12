from tools.tool import Tool

class Pen(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)
        self.last_point = None
        self.thickness = 3  # Default thickness for pen strokes
        self.opacity = 1.0  # Default opacity for pen strokes

    def on_press(self, event):
        """
        Triggered when the mouse is pressed. Captures the starting point of the pen stroke.
        """
        if event:
            self.last_point = (event.pos().x(), event.pos().y())
            self.drawing_manager.enable_drawing()

    def on_drag(self, event):
        """
        Triggered when the mouse is dragged. Draws a line from the last point to the current point.
        """
        if self.last_point is not None and event:
            current_point = (event.pos().x(), event.pos().y())
            self.drawing_manager.draw_line(self.last_point, current_point)
            self.last_point = current_point  # Update last point to continue drawing

    def on_release(self, event):
        """
        Triggered when the mouse is released. Resets the last point and stops drawing.
        """
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def set_thickness(self, thickness):
        """
        Set the thickness of the pen stroke.
        """
        if thickness > 0:
            self.thickness = thickness
            self.drawing_manager.set_thickness(thickness)
        else:
            raise ValueError("Thickness must be greater than 0.")

    def set_opacity(self, opacity):
        """
        Set the opacity of the pen stroke.
        """
        if 0.0 <= opacity <= 1.0:
            self.opacity = opacity
            self.drawing_manager.set_opacity(opacity)
        else:
            raise ValueError("Opacity must be between 0.0 and 1.0.")
