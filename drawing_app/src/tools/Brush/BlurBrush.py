import cv2
import numpy as np
from tools.tool import Tool

class BlurBrush(Tool):
    def __init__(self, drawing_manager, blur_strength=5):
        super().__init__(drawing_manager)
        self.blur_strength = blur_strength
        self.last_point = None
        self.temp_image = None
        self.canvas_backup = None  # Store the canvas state before applying blur for undo

    def set_blur_strength(self, strength):
        self.blur_strength = strength
        print(f"Blur strength set to: {self.blur_strength}")

    def on_press(self, event):
        """Handle the initial press of the brush."""
        self.last_point = (event.pos().x(), event.pos().y())
        self.drawing_manager.enable_drawing()
        self.temp_image = self.drawing_manager.image.copy()
        self.canvas_backup = self.drawing_manager.image.copy()  # Backup for undo feature

    def on_drag(self, event):
        """Handle dragging the brush across the canvas."""
        current_point = (event.pos().x(), event.pos().y())
        if self.last_point:
            distance = self._calculate_distance(self.last_point, current_point)
            dynamic_blur_strength = self._adjust_blur_based_on_speed(distance)
            self._blur_region(self.last_point, current_point, dynamic_blur_strength)
            self.last_point = current_point
            self.drawing_manager.update_canvas_with_image(self.temp_image)

    def on_release(self, event):
        """Handle releasing the brush."""
        if self.last_point:
            current_point = (event.pos().x(), event.pos().y())
            distance = self._calculate_distance(self.last_point, current_point)
            dynamic_blur_strength = self._adjust_blur_based_on_speed(distance)
            self._blur_region(self.last_point, current_point, dynamic_blur_strength)
            self._commit_blur_to_canvas()
        self.last_point = None
        self.drawing_manager.disable_drawing()

    def _blur_region(self, start_point, end_point, dynamic_blur_strength):
        """
        Apply a blur to the region between the start and end points.
        The blur strength is adjusted dynamically based on stroke speed.
        """
        # Draw a line to define the blur region
        cv2.line(self.temp_image, start_point, end_point, (0, 0, 0, 0), self.drawing_manager.thickness)

        # Extract a local region around the brush stroke for blurring
        blur_radius = max(1, self.drawing_manager.thickness // 2)
        region = cv2.getRectSubPix(self.temp_image, (blur_radius * 2, blur_radius * 2), start_point)

        # Apply Gaussian blur with dynamic strength
        blurred_region = cv2.GaussianBlur(region, (dynamic_blur_strength * 2 + 1, dynamic_blur_strength * 2 + 1), 0)

        # Merge the blurred region back without erasing
        self._apply_blurred_region(self.temp_image, blurred_region, start_point)

    def _apply_blurred_region(self, image, blurred_region, point):
        """Apply the blurred region to the original image at the given point."""
        x, y = int(point[0]), int(point[1])
        h, w = blurred_region.shape[:2]

        # Ensure the blurred region is applied within bounds
        image[y:y + h, x:x + w] = cv2.addWeighted(image[y:y + h, x:x + w], 0.7, blurred_region, 0.3, 0)

    def _commit_blur_to_canvas(self):
        """Commit the blurred stroke to the base canvas image."""
        self.drawing_manager.image = self.temp_image.copy()
        self.drawing_manager.update_canvas()

    def undo(self):
        """Undo the last brush stroke by restoring the previous canvas state."""
        if self.canvas_backup is not None:
            self.drawing_manager.image = self.canvas_backup.copy()
            self.drawing_manager.update_canvas()
            print("Undo successful")

    def _adjust_blur_based_on_speed(self, distance):
        """
        Adjust blur strength based on the speed of the stroke.
        Faster strokes apply less blur, slower strokes apply more.
        :param distance: The distance between the current and last points.
        :return: Adjusted blur strength.
        """
        speed_factor = max(1, min(10, int(distance / 5)))  # Control speed impact on blur
        adjusted_blur_strength = max(1, self.blur_strength // speed_factor)
        return adjusted_blur_strength

    def _calculate_distance(self, point1, point2):
        """Calculate the Euclidean distance between two points."""
        return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
