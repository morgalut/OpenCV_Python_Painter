# C:\Users\Mor\Desktop\drawing_app\drawing_app\src\GUI\tool_selection.py
from tools.line import Line
from tools.pen import Pen
from tools.Brush.brush import Brush
from tools.eraser import Eraser
from tools.turtle_tool import TurtleTool
from GUI.mouse_events import MouseEvents


class ToolSelection:
    def __init__(self, canvas_manager, main_window):
        self.canvas_manager = canvas_manager
        self.main_window = main_window
        self.mouse_events = MouseEvents(self)
        self.current_tool = None

    def select_pen_tool(self):
        self.current_tool = Pen(self.canvas_manager)
        self.main_window.statusBar().showMessage("Pen Tool Selected")

    def select_brush_tool(self):
        """Select the Brush tool."""
        self.current_tool = Brush(self.canvas_manager)
        self.main_window.statusBar().showMessage("Brush Tool Selected")
        self.canvas_manager.enable_drawing()  # Enable drawing for the brush

    def select_eraser_tool(self):
        self.current_tool = Eraser(self.canvas_manager)
        self.main_window.statusBar().showMessage("Eraser Tool Selected")

    def select_turtle_tool(self):
        self.current_tool = TurtleTool(self.canvas_manager)
        self.main_window.statusBar().showMessage("Turtle Tool Selected")

    def select_line_tool(self):
        self.current_tool = Line(self.canvas_manager)
        self.main_window.statusBar().showMessage("Line Tool Selected")


