class Tool:
    def __init__(self, drawing_manager):
        self.drawing_manager = drawing_manager
        self.color = (0, 0, 0)  # Default color is black
        self.thickness = 2  # Default thickness
        self.opacity = 1.0  # Default opacity (fully opaque)
        self.texture = None  # Default: no texture

    def on_press(self, event):
        """Triggered when the mouse is pressed."""
        pass

    def on_drag(self, event):
        """Triggered when the mouse is dragged while pressed."""
        pass

    def on_release(self, event):
        """Triggered when the mouse is released."""
        pass

    def set_color(self, color):
        """Set the drawing color."""
        self.color = color

    def set_thickness(self, thickness):
        """Set the thickness for drawing."""
        self.thickness = thickness

    def set_opacity(self, opacity):
        """Set the opacity level for drawing."""
        self.opacity = opacity

    def set_texture(self, texture):
        """Set the texture for the tool."""
        self.texture = texture

    def apply_tool_style(self, start_point, end_point):
        """
        Apply tool styles like opacity and texture. 
        Override this in derived tools to apply specific styles.
        """
        pass

    def update_canvas(self):
        """Update the canvas after drawing."""
        self.drawing_manager.update_canvas()
