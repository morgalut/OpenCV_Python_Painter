import cv2
import numpy as np
from tools.tool import Tool

class Brush(Tool):
    def __init__(self, drawing_manager, brush_type="bristle"):
        """
        Initialize the Brush tool with different types and textures.
        :param drawing_manager: The manager that handles the drawing canvas.
        :param brush_type: Type of brush to use (e.g., "bristle", "soft", "textured").
        """
        super().__init__(drawing_manager)
        self.brush_type = brush_type
        self.last_point = None
        self.opacity = 0.7  # Brushes usually have softer, semi-transparent effects
        self.dynamic_thickness_range = (5, 20)  # Dynamic thickness for brushes (simulates pressure)
        self.temp_image = None  # Temporary image for smoother updates

        # Different texture patterns or effects for various brush types
        self.textures = {
            "bristle": self.create_bristle_texture(),
            "soft": None,  # Soft brush will use Gaussian blur
            "textured": self.create_textured_brush(),
        }
        self.texture = self.textures.get(brush_type, None)

    def create_bristle_texture(self):
        """Create and return a bristle brush texture."""
        texture = np.zeros((10, 10), dtype=np.uint8)
        cv2.randu(texture, 0, 255)  # Random values to simulate bristles
        return texture

    def create_textured_brush(self):
        """Create a textured brush using a noise pattern."""
        texture = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
        return texture

    def log_brush_event(self, event):
        """Log brush press and position."""
        print(f"Brush pressed at {event.pos()}")

    def log_line_draw(self, start_point, end_point):
        """Log the drawing of a line with color."""
        print(f"Drawing line from {start_point} to {end_point} with color {self.drawing_manager.color}")

    def on_press(self, event):
        """Handle the initial press of the brush."""
        self.log_brush_event(event)
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_thickness(np.random.randint(*self.dynamic_thickness_range))  # Random thickness
        self.drawing_manager.set_opacity(self.opacity)  # Brushes tend to have softer opacity
        self.drawing_manager.enable_drawing()
        # Store a temporary image for smoother updates during dragging
        self.temp_image = self.drawing_manager.image.copy()

    def on_drag(self, event):
        """Handle dragging the brush across the canvas."""
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point:
            self.log_line_draw(self.last_point, current_point)  # Log the line drawing
            self.draw_brush_stroke(self.last_point, current_point, temp=True)
            self.last_point = current_point
            # Update the canvas with the temporary image to reduce flickering
            self.drawing_manager.update_canvas_with_image(self.temp_image)

    def on_release(self, event):
        """Handle releasing the brush."""
        if self.last_point:
            current_point = (event.pos().x(), event.pos().y())
            self.log_line_draw(self.last_point, current_point)  # Log the final line draw
            self.draw_brush_stroke(self.last_point, current_point, temp=False)
            self.commit_stroke_to_canvas()
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def draw_brush_stroke(self, start_point, end_point, temp=True):
        """
        Draw the brush stroke from the start to the end point, applying the texture or effect.
        :param start_point: The starting point of the stroke.
        :param end_point: The ending point of the stroke.
        :param temp: Whether to draw on the temporary image (during drag) or the final canvas (on release).
        """
        target_image = self.temp_image if temp else self.drawing_manager.image

        if self.brush_type == "bristle":
            self.draw_bristle_stroke(target_image, start_point, end_point)
        elif self.brush_type == "soft":
            self.draw_soft_stroke(target_image, start_point, end_point)
        elif self.brush_type == "textured":
            self.draw_textured_stroke(target_image, start_point, end_point)

    def commit_stroke_to_canvas(self):
        """Save the current temporary stroke to the base canvas image."""
        # Merge the temporary image with the final canvas
        self.drawing_manager.image = self.temp_image.copy()
        self.drawing_manager.update_canvas()

    def draw_bristle_stroke(self, image, start_point, end_point):
        """Draw a bristle-like stroke by adding randomness to simulate individual bristles."""
        for _ in range(5):  # Simulate multiple bristles with randomness
            jitter_start = (start_point[0] + np.random.randint(-3, 3), start_point[1] + np.random.randint(-3, 3))
            jitter_end = (end_point[0] + np.random.randint(-3, 3), end_point[1] + np.random.randint(-3, 3))
            cv2.line(image, jitter_start, jitter_end, self.drawing_manager.color, np.random.randint(2, 5))

    def draw_soft_stroke(self, image, start_point, end_point):
        """Draw a soft stroke by applying Gaussian blur for a smooth brush effect."""
        cv2.line(image, start_point, end_point, self.drawing_manager.color, self.drawing_manager.thickness)
        blurred_image = cv2.GaussianBlur(image, (21, 21), 0)  # Large blur for soft brush effect
        np.copyto(image, blurred_image)

    def draw_textured_stroke(self, image, start_point, end_point):
        """Draw a textured stroke using a noise pattern for rough brush effects."""
        mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        cv2.line(mask, start_point, end_point, 255, self.drawing_manager.thickness)
        texture_resized = cv2.resize(self.texture, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_NEAREST)

        if len(image.shape) == 3 and image.shape[2] == 3:
            texture_resized = np.stack([texture_resized] * 3, axis=-1)

        image[mask > 0] = cv2.bitwise_and(image[mask > 0], texture_resized[mask > 0])
