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
        self.thickness = 10  # Default brush thickness
        self.brush_type = brush_type  # Brush type ("bristle", "soft", "textured")
        self.last_point = None
        self.textures = {
            "bristle": self.create_bristle_texture(),
            "soft": None,  # Soft brush will use Gaussian blur, no texture needed
            "textured": self.create_textured_brush(),
        }
        self.texture = self.textures.get(brush_type, None)

    def create_bristle_texture(self):
        """Create and return a bristle brush texture."""
        texture = np.zeros((5, 5), dtype=np.uint8)
        cv2.randu(texture, 0, 255)  # Random values to simulate bristles
        return texture

    def create_textured_brush(self):
        """Create a textured brush using a noise pattern."""
        texture = np.random.randint(0, 255, (15, 15), dtype=np.uint8)
        return texture

    def set_brush_type(self, brush_type):
        """Change the brush type dynamically."""
        self.brush_type = brush_type
        self.texture = self.textures.get(brush_type, None)

    def on_press(self, event):
        """Handle the initial press of the brush."""
        print(f"Brush pressed at {event.pos()}")
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_thickness(self.thickness)
        self.drawing_manager.enable_drawing()  # Ensure drawing is enabled

    def on_drag(self, event):
        """Handle dragging the brush across the canvas."""
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point is not None:
            self.draw_brush_stroke(self.last_point, current_point)
            self.last_point = current_point

    def on_release(self, event):
        """Handle releasing the brush."""
        if self.last_point is not None:
            self.draw_brush_stroke(self.last_point, (event.pos().x(), event.pos().y()))
            self.commit_stroke_to_canvas()
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def draw_brush_stroke(self, start_point, end_point):
        """
        Draw the brush stroke from the start to the end point, applying the texture or effect.
        :param start_point: The starting point of the stroke.
        :param end_point: The ending point of the stroke.
        """
        temp_image = self.drawing_manager.image.copy()

        if self.brush_type == "bristle":
            self.draw_bristle_stroke(temp_image, start_point, end_point)
        elif self.brush_type == "soft":
            self.draw_soft_stroke(temp_image, start_point, end_point)
        elif self.brush_type == "textured":
            self.draw_textured_stroke(temp_image, start_point, end_point)

        # Ensure the temporary image is drawn on the canvas
        self.drawing_manager.update_canvas_with_image(temp_image)

    def commit_stroke_to_canvas(self):
        """Save the current temporary stroke to the base canvas image."""
        new_image = self.drawing_manager.image.copy()  # Copy the current image
        self.drawing_manager.image = new_image.copy()  # Commit the stroke to the canvas
        self.drawing_manager.update_canvas()  # Update the canvas to reflect the stroke

    def draw_bristle_stroke(self, image, start_point, end_point):
        """Draw a bristle-like stroke by adding randomness to simulate individual bristles."""
        for _ in range(5):  # Simulate multiple bristles
            jitter_start = (start_point[0] + np.random.randint(-2, 2), start_point[1] + np.random.randint(-2, 2))
            jitter_end = (end_point[0] + np.random.randint(-2, 2), end_point[1] + np.random.randint(-2, 2))
            cv2.line(image, jitter_start, jitter_end, self.drawing_manager.color, self.drawing_manager.thickness)

    def draw_soft_stroke(self, image, start_point, end_point):
        """Draw a soft stroke by applying Gaussian blur to smooth out edges."""
        cv2.line(image, start_point, end_point, self.drawing_manager.color, self.drawing_manager.thickness)
        blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
        np.copyto(image, blurred_image)

    def draw_textured_stroke(self, image, start_point, end_point):
        """Draw a textured stroke using a repeating noise pattern."""
        texture = self.textures["textured"]
        mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        cv2.line(mask, start_point, end_point, 255, self.drawing_manager.thickness)
        texture_resized = cv2.resize(texture, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_NEAREST)

        # Apply the texture to the line
        if len(image.shape) == 3 and image.shape[2] == 3:
            texture_resized = np.stack([texture_resized] * 3, axis=-1)

        image[mask > 0] = cv2.bitwise_and(image[mask > 0], texture_resized[mask > 0])
