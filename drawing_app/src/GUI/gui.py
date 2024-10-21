from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QColorDialog
from GUI.canvas_manager import CanvasManager
from GUI.toolbar import ToolbarManager
from GUI.tool_selection import ToolSelection
from PySide6.QtCore import Qt
from tools.back_button import BackButton
from main import Worker  # Import Worker from the main module

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
        self.back_button = BackButton(self.canvas_manager.drawing_manager)

    def mouse_press_event(self, event):
        """Handle mouse press events for drawing."""
        self.tool_selection.back_button.save_state()  # Save state on mouse press
        self.tool_selection.mouse_events.mouse_press_event(event)

    def mouse_move_event(self, event):
        """Handle mouse move events for drawing."""
        self.tool_selection.mouse_events.mouse_move_event(event)

    def mouse_release_event(self, event):
        """Handle mouse release events for drawing."""
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

    def some_method(self):
        """An example method showcasing internal usage."""
        self.set_thickness(5)  # Example call to another method within the same class


class DrawingAppWithWorker(DrawingApp):
    def __init__(self):
        super().__init__()
        # Worker thread initialization
        self.worker = Worker()
        self.worker.finished.connect(self.on_task_finished)
        self.worker.error.connect(self.on_task_error)

        # Setup your main window and canvas
        self.setWindowTitle("Drawing Application")
        self.setGeometry(100, 100, 800, 600)

        # Create a label to serve as the canvas
        self.canvas_label = QLabel(self)
        self.canvas_label.setFixedSize(800, 600)
        self.canvas_label.setStyleSheet("background-color: white;")

        # Layout management
        layout = QVBoxLayout()
        layout.addWidget(self.canvas_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize the CanvasManager with the drawing app reference
        self.canvas_manager = CanvasManager(self.canvas_label, drawing_app=self)

        # Initialize the BackButton for undo functionality
        self.back_button = BackButton(self.canvas_manager.drawing_manager)

        # Initialize the tool selection
        self.tool_selection = ToolSelection(self.canvas_manager, self)
        self.tool_selection.select_pen_tool()

        # Setup the toolbar and pass the BackButton
        self.toolbar_manager = ToolbarManager(self, self.back_button)
        self.toolbar_manager.init_toolbar()

        # Mouse events handling
        self.canvas_label.mousePressEvent = self.mouse_press_event
        self.canvas_label.mouseMoveEvent = self.mouse_move_event
        self.canvas_label.mouseReleaseEvent = self.mouse_release_event

    def on_task_finished(self):
        """Handle worker task completion."""
        self.statusBar().showMessage("Background task finished.")

    def on_task_error(self, error_message):
        """Handle worker task error."""
        self.statusBar().showMessage(f"Error occurred: {error_message}")

    def set_opacity(self, value):
        """Set the opacity for the current drawing tool via the DrawingManager."""
        opacity = value / 100.0  # Convert slider value to opacity (0.0 to 1.0)
        self.canvas_manager.set_opacity(opacity)  # Pass the value to DrawingManager
        self.statusBar().showMessage(f"Opacity set to {opacity * 100:.0f}%")
