class Tool:
    def __init__(self, drawing_manager):
        self.drawing_manager = drawing_manager
        self.color = (0, 0, 0)  # Default color is black (RGB tuple)
        self.thickness = 2  # Default thickness
        self.opacity = 1.0  # Default opacity (fully opaque)
        self.texture = None  # Default: no texture

    def set_color(self, color):
        """
        Set the drawing color. Ensure the color is applied correctly.
        The color should be an (R, G, B) tuple.
        """
        if isinstance(color, tuple) and len(color) == 3:
            self.color = color  # Set the color as an RGB tuple
            self.drawing_manager.set_color(self.color)
        else:
            raise ValueError("Color must be a tuple of (R, G, B) values.")

    def set_thickness(self, thickness):
        """Set the thickness for drawing."""
        self.thickness = thickness
        self.drawing_manager.set_thickness(self.thickness)

    def set_opacity(self, opacity):
        """Set the opacity level for drawing."""
        self.opacity = opacity
        self.drawing_manager.set_opacity(self.opacity)

    def apply_tool_style(self, start_point, end_point):
        """
        Apply tool styles like opacity and texture. 
        Override this in derived tools to apply specific styles.
        """
        pass

    def update_canvas(self):
        """Update the canvas after drawing."""
        self.drawing_manager.update_canvas()
