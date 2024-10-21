from tools.tool import Tool

class Pen(Tool):
    def __init__(self, drawing_manager):
        super().__init__(drawing_manager)
        self.last_point = None
        self.thickness = 2  # Default pen thickness
        self.opacity = 1.0  # Fully opaque for sharp lines

    def on_press(self, event):
        """
        Handle the initial press for the pen tool. Set the thickness, opacity, and enable drawing.
        """
        if event:
            self.last_point = (event.pos().x(), event.pos().y())
            self.drawing_manager.set_thickness(self.thickness)
            self.drawing_manager.set_opacity(self.opacity)
            self.drawing_manager.enable_drawing()

    def on_drag(self, event):
        """
        Handle dragging for the pen tool, drawing sharp, continuous lines.
        Updates the last point for continuous drawing.
        """
        if self.last_point and event:
            current_point = (event.pos().x(), event.pos().y())
            self.drawing_manager.draw_line(self.last_point, current_point)  # No color passed here
            self.last_point = current_point  # Update to the current point for continuous drawing

    def on_release(self, event):
        """
        Handle releasing the pen, ending the drawing stroke.
        Reset the last point and disable drawing mode.
        """
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def set_thickness(self, thickness):
        """
        Set the thickness of the pen stroke. Ensure that the thickness is valid.
        """
        if thickness > 0:
            self.thickness = thickness
            self.drawing_manager.set_thickness(thickness)
        else:
            raise ValueError("Thickness must be greater than 0.")

    def set_opacity(self, opacity):
        """
        Set the opacity of the pen stroke. Ensure the opacity is within the valid range (0.0 to 1.0).
        """
        if 0.0 <= opacity <= 1.0:
            self.opacity = opacity
            self.drawing_manager.set_opacity(opacity)
        else:
            raise ValueError("Opacity must be between 0.0 and 1.0.")
