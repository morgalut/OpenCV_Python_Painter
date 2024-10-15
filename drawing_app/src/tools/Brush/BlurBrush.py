import cv2
import numpy as np
from tools.tool import Tool

class BlurBrush(Tool):
    def __init__(self, drawing_manager, blur_strength=5):
        """
        Initialize the Blur Brush tool.
        :param drawing_manager: The manager that handles the drawing canvas.
        :param blur_strength: The intensity of the blur effect (higher values = stronger blur).
        """
        super().__init__(drawing_manager)
        self.blur_strength = blur_strength  # Control the blur level
        self.last_point = None
        self.temp_image = None  # Temporary image for smoother updates during drag operations

    def set_blur_strength(self, strength):
        """Set the blur strength dynamically."""
        self.blur_strength = strength
        print(f"Blur strength set to: {self.blur_strength}")

    def on_press(self, event):
        """Handle the initial press of the brush."""
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.enable_drawing()
        self.temp_image = self.drawing_manager.image.copy()  # Store the image for smoother dragging

    def on_drag(self, event):
        """Handle dragging the brush across the canvas."""
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point:
            self._blur_region(self.last_point, current_point)
            self.last_point = current_point
            self.drawing_manager.update_canvas_with_image(self.temp_image)

    def on_release(self, event):
        """Handle releasing the brush."""
        if self.last_point:
            current_point = (event.pos().x(), event.pos().y())
            self._blur_region(self.last_point, current_point)
            self._commit_blur_to_canvas()
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def _blur_region(self, start_point, end_point):
        """
        Apply a blur to the region between the start and end points.
        :param start_point: Starting point of the blur.
        :param end_point: Ending point of the blur.
        """
        # Draw a line to define the blur region
        cv2.line(self.temp_image, start_point, end_point, (255, 255, 255), self.drawing_manager.thickness)

        # Extract a local region around the brush stroke for blurring
        blur_radius = max(1, self.drawing_manager.thickness // 2)
        region = cv2.getRectSubPix(self.temp_image, (blur_radius * 2, blur_radius * 2), start_point)

        # Apply Gaussian blur to the region
        blurred_region = cv2.GaussianBlur(region, (self.blur_strength * 2 + 1, self.blur_strength * 2 + 1), 0)

        # Put the blurred region back in place
        self._apply_blurred_region(self.temp_image, blurred_region, start_point)

    def _apply_blurred_region(self, image, blurred_region, point):
        """Apply the blurred region to the original image at the given point."""
        x, y = int(point[0]), int(point[1])
        h, w = blurred_region.shape[:2]

        # Ensure the blurred region is applied within bounds
        image[y:y + h, x:x + w] = blurred_region

    def _commit_blur_to_canvas(self):
        """Commit the blurred stroke to the base canvas image."""
        self.drawing_manager.image = self.temp_image.copy()
        self.drawing_manager.update_canvas()
