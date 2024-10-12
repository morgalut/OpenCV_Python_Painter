# C:\Users\Mor\Desktop\drawing_app\drawing_app\src\GUI\canvas_manager.py
import cv2
from PySide6.QtGui import QImage, QPixmap
from drawing_manager import DrawingManager

class CanvasManager:
    def __init__(self, canvas_label):
        """
        Initialize the CanvasManager class that manages the drawing canvas and interacts
        with the DrawingManager for performing drawing operations.
        """
        self.canvas_label = canvas_label
        self.drawing_manager = DrawingManager(self.canvas_label)
        self.zoom_factor = 1.0

    def update_canvas(self):
        """Update the canvas display with the current drawing."""
        image = self.drawing_manager.image
        self._set_canvas_image(image)

    def update_canvas_with_image(self, image):
        """
        Update the canvas display with a temporary image (e.g., during drag events).
        This does not modify the base image but shows a preview.
        """
        self._set_canvas_image(image)

    def clear_canvas(self):
        """Clear the canvas to its initial background color."""
        self.drawing_manager.clear_canvas()
        self.update_canvas()

    def enable_drawing(self):
        """Enable the drawing feature on the canvas."""
        self.drawing_manager.enable_drawing()

    def disable_drawing(self):
        """Disable the drawing feature on the canvas."""
        self.drawing_manager.disable_drawing()

    def draw_line(self, start_point, end_point):
        """Draw a zoom-aware line on the canvas."""
        scaled_start, scaled_end = self._scale_points(start_point, end_point)
        self.drawing_manager.draw_line(scaled_start, scaled_end)
        self.update_canvas()

    def draw_rectangle(self, start_point, end_point):
        """Draw a zoom-aware rectangle on the canvas."""
        scaled_start, scaled_end = self._scale_points(start_point, end_point)
        self.drawing_manager.draw_rectangle(scaled_start, scaled_end)
        self.update_canvas()

    def draw_ellipse(self, center_point, axes_lengths):
        """Draw a zoom-aware ellipse on the canvas."""
        scaled_center = self._scale_point(center_point)
        scaled_axes = self._scale_tuple(axes_lengths)
        self.drawing_manager.draw_ellipse(scaled_center, scaled_axes)
        self.update_canvas()

    def set_color(self, color):
        """Set the drawing color."""
        self.drawing_manager.set_color(color)

    def set_thickness(self, thickness):
        """Set the thickness for the drawing tools, scaled by zoom factor."""
        scaled_thickness = max(1, int(thickness * self.zoom_factor))
        self.drawing_manager.set_thickness(scaled_thickness)

    def set_opacity(self, opacity):
        """Set the opacity for the drawing tools."""
        self.drawing_manager.set_opacity(opacity)

    def zoom(self, factor):
        """
        Adjust the zoom factor, scaling all drawing operations accordingly.
        This scales the display of the canvas as well as tools like pens and shapes.
        """
        self.zoom_factor = max(0.1, self.zoom_factor * factor)  # Prevent zooming too small
        self.update_zoomed_canvas()

    def update_zoomed_canvas(self):
        """Update the canvas with the current zoom factor applied."""
        zoomed_image = cv2.resize(self.drawing_manager.image, None, fx=self.zoom_factor, fy=self.zoom_factor, interpolation=cv2.INTER_LINEAR)
        self.update_canvas_with_image(zoomed_image)

    def _scale_points(self, *points):
        """
        Scale points according to the current zoom factor.
        This ensures that drawing operations like lines and shapes behave correctly when zooming.
        """
        return tuple(self._scale_point(point) for point in points)

    def _scale_point(self, point):
        """Scale a single point (x, y) by the current zoom factor."""
        return int(point[0] * self.zoom_factor), int(point[1] * self.zoom_factor)

    def _scale_tuple(self, values):
        """Scale a tuple of values by the zoom factor, useful for axes lengths."""
        return tuple(int(v * self.zoom_factor) for v in values)

    def _set_canvas_image(self, image):
        """
        Convert the image to QPixmap and set it on the QLabel canvas.
        """
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.canvas_label.setPixmap(QPixmap.fromImage(q_image))

    # Expose properties like color, image, thickness, etc., from DrawingManager
    @property
    def color(self):
        return self.drawing_manager.color

    @property
    def image(self):
        return self.drawing_manager.image

    @property
    def thickness(self):
        return self.drawing_manager.thickness

    @property
    def opacity(self):
        return self.drawing_manager.opacity

    @property
    def width(self):
        return self.drawing_manager.width

    @property
    def height(self):
        return self.drawing_manager.height

    @property
    def background_color(self):
        """Expose background_color from DrawingManager."""
        return self.drawing_manager.background_color
