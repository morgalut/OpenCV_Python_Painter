from PySide6.QtWidgets import QToolBar, QColorDialog, QSlider, QLabel, QPushButton
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from tools.eraser import Eraser

class ToolbarManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def init_toolbar(self):
        toolbar = QToolBar("Tools")
        self.main_window.addToolBar(toolbar)

        # Pen tool
        pen_action = QAction("Pen Tool", self.main_window)
        pen_action.triggered.connect(self.main_window.tool_selection.select_pen_tool)
        toolbar.addAction(pen_action)

        # Brush tool
        brush_action = QAction("Brush Tool", self.main_window)
        brush_action.triggered.connect(self.main_window.tool_selection.select_brush_tool)
        toolbar.addAction(brush_action)

        # Eraser tool
        eraser_action = QAction("Eraser Tool", self.main_window)
        eraser_action.triggered.connect(self.main_window.tool_selection.select_eraser_tool)
        toolbar.addAction(eraser_action)

        # Turtle tool
        turtle_action = QAction("Turtle Tool", self.main_window)
        turtle_action.triggered.connect(self.main_window.tool_selection.select_turtle_tool)
        toolbar.addAction(turtle_action)

        # Color Picker
        color_action = QAction("Pick Color", self.main_window)
        color_action.triggered.connect(self.pick_color)
        toolbar.addAction(color_action)

        # Clear Canvas
        clear_action = QAction("Clear Canvas", self.main_window)
        clear_action.triggered.connect(self.main_window.canvas_manager.clear_canvas)
        toolbar.addAction(clear_action)

        # Thickness Slider
        toolbar.addWidget(QLabel("Thickness:"))
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(30)
        self.thickness_slider.setValue(self.main_window.canvas_manager.thickness)
        self.thickness_slider.valueChanged.connect(self.change_thickness)
        toolbar.addWidget(self.thickness_slider)

        # Opacity Slider
        toolbar.addWidget(QLabel("Opacity:"))
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.main_window.canvas_manager.opacity * 100))
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        toolbar.addWidget(self.opacity_slider)

        # Zoom Controls
        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_button)

        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_button)

        # Eraser Shape Controls (for Eraser tool)
        toolbar.addWidget(QLabel("Eraser Shape:"))
        circle_eraser_button = QPushButton("Circle")
        circle_eraser_button.clicked.connect(self.set_eraser_shape_circle)
        toolbar.addWidget(circle_eraser_button)

        square_eraser_button = QPushButton("Square")
        square_eraser_button.clicked.connect(self.set_eraser_shape_square)
        toolbar.addWidget(square_eraser_button)

        line_action = QAction("Line Tool", self.main_window)
        line_action.triggered.connect(self.main_window.tool_selection.select_line_tool)
        toolbar.addAction(line_action)

    def set_eraser_shape_circle(self):
        """Set the eraser shape to circle if the Eraser tool is selected."""
        current_tool = self.main_window.tool_selection.current_tool
        if isinstance(current_tool, Eraser):
            current_tool.set_eraser_shape("circle")
            self.main_window.statusBar().showMessage("Eraser shape set to Circle")
        else:
            self.main_window.statusBar().showMessage("Select the Eraser Tool to change the eraser shape.")

    def set_eraser_shape_square(self):
        """Set the eraser shape to square if the Eraser tool is selected."""
        current_tool = self.main_window.tool_selection.current_tool
        if isinstance(current_tool, Eraser):
            current_tool.set_eraser_shape("square")
            self.main_window.statusBar().showMessage("Eraser shape set to Square")
        else:
            self.main_window.statusBar().showMessage("Select the Eraser Tool to change the eraser shape.")

    def pick_color(self):
        """Open a color picker dialog to choose the drawing color."""
        color = QColorDialog.getColor()
        if color.isValid():
            rgb_color = (color.red(), color.green(), color.blue())
            self.main_window.canvas_manager.set_color(rgb_color)
            self.main_window.statusBar().showMessage(f"Color Selected: {color.name()}")

    def change_thickness(self):
        """Adjust the thickness of the current drawing tool."""
        thickness = self.thickness_slider.value()
        current_tool = self.main_window.tool_selection.current_tool
        if hasattr(current_tool, 'set_thickness'):
            current_tool.set_thickness(thickness)
        self.main_window.statusBar().showMessage(f"Thickness set to {thickness}px")

    def change_opacity(self):
        """Adjust the opacity of the current drawing tool."""
        opacity = self.opacity_slider.value() / 100.0
        current_tool = self.main_window.tool_selection.current_tool
        if hasattr(current_tool, 'set_opacity'):
            current_tool.set_opacity(opacity)
        self.main_window.statusBar().showMessage(f"Opacity set to {opacity * 100:.0f}%")

    def zoom_in(self):
        """Zoom in on the canvas."""
        self.main_window.canvas_manager.zoom(1.2)

    def zoom_out(self):
        """Zoom out on the canvas."""
        self.main_window.canvas_manager.zoom(0.8)
