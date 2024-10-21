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
        self.opacity = 0.7  # Default brush opacity for softer effects
        self.dynamic_thickness_range = (5, 20)  # Simulates pressure sensitivity
        self.temp_image = None  # Temporary image for smoother drawing updates

        # Initialize and load textures for different brush types
        self.textures = self._initialize_textures()
        self.texture = self.textures.get(brush_type, None)

    def _initialize_textures(self):
        """Initialize textures for different brush types."""
        return {
            "bristle": self._create_bristle_texture(),
            "soft": None,  # Soft brush uses Gaussian blur directly
            "textured": self._create_textured_brush(),
        }

    def set_brush_type(self, brush_type):
        """Change the brush type dynamically."""
        self.brush_type = brush_type
        self.texture = self.textures.get(brush_type, None)
        print(f"Brush type changed to: {brush_type}")

    def _create_bristle_texture(self):
        """Create and return a texture for a bristle brush."""
        texture = np.zeros((10, 10), dtype=np.uint8)
        cv2.randu(texture, 0, 255)  # Simulates random bristle strokes
        return texture

    def _create_textured_brush(self):
        """Create a texture for a textured brush using a noise pattern."""
        texture = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
        return texture

    def on_press(self, event):
        """Handle the initial press of the brush tool."""
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.set_thickness(np.random.randint(*self.dynamic_thickness_range))  # Randomized thickness
        self.drawing_manager.set_opacity(self.opacity)  # Adjust opacity for soft brushes
        self.drawing_manager.enable_drawing()
        self.temp_image = self.drawing_manager.image.copy()  # Store the image for smoother dragging

    def on_drag(self, event):
        """Handle dragging the brush across the canvas."""
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point:
            self._draw_brush_stroke(self.last_point, current_point, temp=True)
            self.last_point = current_point
            self.drawing_manager.update_canvas_with_image(self.temp_image)

    def on_release(self, event):
        """Handle the brush release event."""
        if self.last_point:
            current_point = (event.pos().x(), event.pos().y())
            self._draw_brush_stroke(self.last_point, current_point, temp=False)
            self._commit_stroke_to_canvas()
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def _draw_brush_stroke(self, start_point, end_point, temp=True):
        """
        Draw the brush stroke from start to end, applying the appropriate texture or effect.
        """
        target_image = self.temp_image if temp else self.drawing_manager.image

        if self.brush_type == "bristle":
            self._draw_bristle_stroke(target_image, start_point, end_point)
        elif self.brush_type == "soft":
            self._draw_soft_stroke(target_image, start_point, end_point)
        elif self.brush_type == "textured":
            self._draw_textured_stroke(target_image, start_point, end_point)

    def _draw_bristle_stroke(self, image, start_point, end_point):
        """Draw a bristle-like stroke with randomness to simulate individual bristles."""
        color_with_opacity = self._apply_opacity(self.drawing_manager.color, self.opacity)
        for _ in range(5):  # Simulate multiple bristles by adding jitter
            jitter_start = (start_point[0] + np.random.randint(-3, 3), start_point[1] + np.random.randint(-3, 3))
            jitter_end = (end_point[0] + np.random.randint(-3, 3), end_point[1] + np.random.randint(-3, 3))
            cv2.line(image, jitter_start, jitter_end, color_with_opacity, np.random.randint(2, 5))

    def _draw_soft_stroke(self, image, start_point, end_point):
        """Draw a soft stroke using Gaussian blur localized to the stroke area."""
        color_with_opacity = self._apply_opacity(self.drawing_manager.color, self.opacity)
        cv2.line(image, start_point, end_point, color_with_opacity, self.drawing_manager.thickness)

        # Create a mask to localize the blur effect
        mask = np.zeros_like(image)
        cv2.line(mask, start_point, end_point, 255, self.drawing_manager.thickness)
        
        # Only apply blur to the stroke area
        blurred_image = cv2.GaussianBlur(image, (21, 21), 0)
        np.copyto(image, blurred_image, where=mask.astype(bool))

    def _draw_textured_stroke(self, image, start_point, end_point):
        """Draw a textured stroke using a noise pattern for rough effects."""
        if self.texture is None:
            print("No texture available for this brush type.")
            return

        mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        cv2.line(mask, start_point, end_point, 255, self.drawing_manager.thickness)
        texture_resized = cv2.resize(self.texture, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_NEAREST)

        # Ensure the texture matches the image's color channels
        if len(image.shape) == 3 and image.shape[2] == 3:
            texture_resized = np.stack([texture_resized] * 3, axis=-1)

        # Apply the texture to the stroke area
        image[mask > 0] = cv2.bitwise_and(image[mask > 0], texture_resized[mask > 0])

    def _apply_opacity(self, color, opacity):
        """Apply opacity to the color for blending."""
        return [int(c * opacity) for c in color]

    def _commit_stroke_to_canvas(self):
        """Save the current stroke from the temporary image to the base canvas image."""
        self.drawing_manager.image = self.temp_image.copy()
        self.drawing_manager.update_canvas()
