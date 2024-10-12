from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QColorDialog
from GUI.canvas_manager import CanvasManager
from GUI.toolbar import ToolbarManager
from GUI.tool_selection import ToolSelection
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cross-Platform Drawing App with Turtle")
        self.setGeometry(100, 100, 1000, 700)

        # Setup main layout
        self.canvas_label = QLabel("Drawing Area")
        self.canvas_label.setFixedSize(800, 600)
        self.canvas_label.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize canvas, toolbar, and tools
        self.canvas_manager = CanvasManager(self.canvas_label)
        self.toolbar_manager = ToolbarManager(self)
        self.tool_selection = ToolSelection(self.canvas_manager, self)

        # Initialize the toolbar
        self.toolbar_manager.init_toolbar()

        # Initialize default tool (Pen)
        self.tool_selection.select_pen_tool()

        # Add mouse event handling
        self.canvas_label.mousePressEvent = self.mouse_press_event
        self.canvas_label.mouseMoveEvent = self.mouse_move_event
        self.canvas_label.mouseReleaseEvent = self.mouse_release_event

        # Add status bar
        self.statusBar().showMessage("Pen Tool Selected")

        # Add color picker and initial color setting
        self.current_color = (0, 0, 0)  # Default color (black)
        self.canvas_manager.set_color(self.current_color)

    def mouse_press_event(self, event):
        self.tool_selection.mouse_events.mouse_press_event(event)

    def mouse_move_event(self, event):
        self.tool_selection.mouse_events.mouse_move_event(event)

    def mouse_release_event(self, event):
        self.tool_selection.mouse_events.mouse_release_event(event)

    def pick_color(self):
        """Open a color picker dialog to choose the drawing color."""
        color = QColorDialog.getColor()
        if color.isValid():
            rgb_color = (color.red(), color.green(), color.blue())
            self.current_color = rgb_color
            self.canvas_manager.set_color(self.current_color)
            self.statusBar().showMessage(f"Color Selected: {color.name()}")

    def set_thickness(self, thickness):
        """Update the tool's thickness based on user input."""
        self.canvas_manager.set_thickness(thickness)
        self.statusBar().showMessage(f"Thickness set to {thickness}px")
