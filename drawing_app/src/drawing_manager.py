import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class DrawingManager:
    def __init__(self, canvas: QLabel, width=800, height=600, background_color=(255, 255, 255), drawing_app=None):
        """
        Initialize the drawing manager.

        :param canvas: The QWidget (label) where the image is drawn.
        :param width: Initial width of the canvas.
        :param height: Initial height of the canvas.
        :param background_color: The background color of the canvas.
        :param drawing_app: Reference to the drawing application (optional).
        """
        self.canvas = canvas
        self.width = width
        self.height = height
        self.background_color = background_color
        self.image = np.full((height, width, 3), background_color, dtype=np.uint8)
        self.color = (0, 0, 0)  # Default drawing color (black)
        self.thickness = 2  # Default thickness
        self.opacity = 1.0  # Default opacity (fully opaque)
        self.is_pen_down = False  # Control drawing state (pen down = drawing)
        self.zoom_factor = 1.0  # Default zoom factor (no zoom)
        self.offset_x = 0  # Offset to pan the zoomed image
        self.offset_y = 0  # Offset to pan the zoomed image
        self.drawing_app = drawing_app  # Reference to the parent drawing app (optional)

        # Update the canvas with the initial blank image
        self.update_canvas()

    def enable_drawing(self):
        """Enable drawing (simulate pen down)."""
        self.is_pen_down = True

    def disable_drawing(self):
        """Disable drawing (simulate pen up)."""
        self.is_pen_down = False

    def set_zoom_factor(self, factor: float):
        """
        Set the zoom factor and adjust the canvas accordingly.
        :param factor: Zoom factor (1.0 = 100%, 2.0 = 200%, etc.)
        """
        if factor > 0:
            self.zoom_factor = factor
            self.update_canvas()

    def set_color(self, color: tuple):
        """Set the color for drawing."""
        self.color = color

    def set_thickness(self, thickness: int):
        """Set the thickness for drawing, adjusted for zoom."""
        self.thickness = thickness

    def set_opacity(self, opacity: float):
        """Set the opacity level for drawing."""
        self.opacity = opacity

    def _apply_opacity(self, color: tuple):
        """Apply the specified opacity to the given color."""
        return tuple(int(c * self.opacity) for c in color)

    def _adjust_for_zoom(self, point: tuple):
        """Adjust a given point for the current zoom factor."""
        return int(point[0] * self.zoom_factor), int(point[1] * self.zoom_factor)

    def _draw_shape(self, shape_func, *args):
        """Internal helper to draw a shape on the canvas if drawing is enabled."""
        if self.is_pen_down:
            color_with_opacity = self._apply_opacity(self.color)
            shape_func(self.image, *args, color_with_opacity, self.thickness)
            self.update_canvas()

    def draw_line(self, start_point: tuple, end_point: tuple):
        """Draw a line between two points on the canvas, adjusted for zoom."""
        zoomed_start = self._adjust_for_zoom(start_point)
        zoomed_end = self._adjust_for_zoom(end_point)
        self._draw_shape(cv2.line, zoomed_start, zoomed_end)

    def draw_rectangle(self, start_point: tuple, end_point: tuple):
        """Draw a rectangle on the canvas, adjusted for zoom."""
        zoomed_start = self._adjust_for_zoom(start_point)
        zoomed_end = self._adjust_for_zoom(end_point)
        self._draw_shape(cv2.rectangle, zoomed_start, zoomed_end)

    def draw_ellipse(self, center_point: tuple, axes_lengths: tuple):
        """Draw an ellipse on the canvas, adjusted for zoom."""
        zoomed_center = self._adjust_for_zoom(center_point)
        zoomed_axes = tuple(map(self._adjust_for_zoom, axes_lengths))
        self._draw_shape(cv2.ellipse, zoomed_center, zoomed_axes, 0, 0, 360)

    def clear_canvas(self):
        """Clear the canvas by resetting the image to the background color."""
        self.image = np.full((self.height, self.width, 3), self.background_color, dtype=np.uint8)
        self.update_canvas()

    def update_canvas(self):
        """Update the canvas with the current image, applying the zoom factor."""
        zoomed_image = cv2.resize(self.image, None, fx=self.zoom_factor, fy=self.zoom_factor, interpolation=cv2.INTER_NEAREST)

        # Adjust offsets to ensure they are within bounds
        self.offset_x = min(max(self.offset_x, 0), max(0, zoomed_image.shape[1] - self.width))
        self.offset_y = min(max(self.offset_y, 0), max(0, zoomed_image.shape[0] - self.height))

        # Crop the zoomed image based on the offsets
        cropped_image = zoomed_image[self.offset_y:self.offset_y + self.height, self.offset_x:self.offset_x + self.width]

        # Display the cropped zoomed image on the canvas
        self._set_canvas_image(cropped_image)

    def _set_canvas_image(self, image: np.ndarray):
        """Convert the image to QPixmap and set it on the QLabel canvas."""
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.canvas.setPixmap(QPixmap.fromImage(q_image))

    def update_canvas_with_image(self, image: np.ndarray):
        """Update the canvas with an external image, resizing it to fit the canvas."""
        resized_image = cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
        self.image = resized_image
        self.update_canvas()

    def pan(self, delta_x: int, delta_y: int):
        """Pan the canvas by adjusting the offset."""
        self.offset_x += delta_x
        self.offset_y += delta_y
        self.update_canvas()
