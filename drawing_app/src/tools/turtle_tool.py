import cv2
import numpy as np
from tools.tool import Tool

class TurtleTool(Tool):
    def __init__(self, drawing_manager, initial_angle=0, start_position=None, speed=10):
        """
        Initialize the Turtle Tool.
        :param drawing_manager: The canvas manager.
        :param initial_angle: Initial angle for the turtle (default is 0 degrees).
        :param start_position: Optional starting position (default is the center of the canvas).
        :param speed: Speed of turtle's movement (default is 10 pixels per step).
        """
        super().__init__(drawing_manager)
        self.angle = initial_angle
        self.position = start_position or self.get_default_start_position()
        self.previous_position = self.position
        self.speed = speed
        self.drawing_manager.enable_drawing()

    def get_default_start_position(self):
        """Get the default start position as the center of the canvas."""
        return (self.drawing_manager.width // 2, self.drawing_manager.height // 2)

    def move_forward(self, distance=None):
        """Move the turtle forward by the specified distance, defaults to speed if not provided."""
        distance = distance if distance else self.speed
        self.position = self.calculate_new_position(distance)
        self.drawing_manager.draw_line(self.previous_position, self.position)
        self.previous_position = self.position
        self._update_canvas()

    def move_backward(self, distance=None):
        """Move the turtle backward by the specified distance."""
        self.turn_left(180)
        self.move_forward(distance)
        self.turn_right(180)

    def turn_left(self, degrees=90):
        """Turn the turtle left by the given number of degrees, defaults to 90 degrees."""
        self.angle = (self.angle + degrees) % 360

    def turn_right(self, degrees=90):
        """Turn the turtle right by the given number of degrees, defaults to 90 degrees."""
        self.angle = (self.angle - degrees) % 360

    def draw_circle(self, radius):
        """Draw a circle with the turtle as the center."""
        cv2.circle(self.drawing_manager.image, self.position, radius, self.color, self.thickness)
        self._update_canvas()

    def draw_square(self, side_length):
        """Draw a square with the turtle moving forward and turning at right angles."""
        for _ in range(4):
            self.move_forward(side_length)
            self.turn_right(90)
        self._update_canvas()

    def draw_polygon(self, sides, side_length):
        """Draw a regular polygon with the specified number of sides and side length."""
        angle = 360 / sides
        for _ in range(sides):
            self.move_forward(side_length)
            self.turn_right(angle)
        self._update_canvas()

    def teleport(self, x, y):
        """
        Instantly move the turtle to a new position without drawing.
        :param x: The x-coordinate.
        :param y: The y-coordinate.
        """
        self.set_position((x, y))

    def home(self):
        """Move the turtle back to the center of the canvas without drawing."""
        self.set_position(self.get_default_start_position())

    def pen_up(self):
        """Temporarily disable drawing (i.e., lift the pen)."""
        self.drawing_manager.disable_drawing()

    def pen_down(self):
        """Re-enable drawing (i.e., put the pen down)."""
        self.drawing_manager.enable_drawing()

    def reset(self):
        """Reset the turtle's position and angle to default."""
        self.angle = 0
        self.position = self.get_default_start_position()
        self.previous_position = self.position
        self._update_canvas()

    def set_position(self, new_position):
        """Set the turtle to a new position without drawing."""
        self.position = new_position

    def set_angle(self, angle):
        """Set the turtle's angle directly."""
        self.angle = angle % 360

    def set_speed(self, speed):
        """Set the movement speed of the turtle."""
        self.speed = max(1, speed)  # Ensure the speed is at least 1 pixel per step

    def calculate_new_position(self, distance):
        """Calculate new position based on the distance and current angle."""
        x, y = self.position
        radian_angle = np.deg2rad(self.angle)
        new_x = int(x + distance * np.cos(radian_angle))
        new_y = int(y - distance * np.sin(radian_angle))  # Subtract for upward direction in image
        return new_x, new_y

    def _update_canvas(self):
        """Ensure the canvas is updated after each operation."""
        self.drawing_manager.update_canvas()
