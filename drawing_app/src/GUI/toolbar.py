from PySide6.QtWidgets import QToolBar, QColorDialog, QSlider, QLabel, QPushButton
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from tools.Brush.BlurBrush import BlurBrush  # Import the new BlurBrush
from tools.Brush.brush import Brush
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

        # Brush tool type selection
        toolbar.addWidget(QLabel("Brush Type:"))
        self.add_brush_button(toolbar, "Bristle")
        self.add_brush_button(toolbar, "Soft")
        self.add_brush_button(toolbar, "Textured")
        self.add_blur_brush_button(toolbar)  # Add Blur Brush Button

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
        self.add_slider(toolbar, "Thickness:", 1, 30, self.main_window.canvas_manager.thickness, self.change_thickness)

        # Opacity Slider
        self.add_slider(toolbar, "Opacity:", 0, 100, int(self.main_window.canvas_manager.opacity * 100), self.change_opacity)

        # Blur Intensity Slider
        self.add_slider(toolbar, "Blur Intensity:", 1, 50, 5, self.change_blur_intensity)

        # Zoom Controls
        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_button)

        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_button)

        # Eraser Shape Controls (for Eraser tool)
        toolbar.addWidget(QLabel("Eraser Shape:"))
        self.add_eraser_shape_button(toolbar, "Circle", "circle")
        self.add_eraser_shape_button(toolbar, "Square", "square")

    def add_brush_button(self, toolbar, brush_type):
        """Helper function to add brush type buttons."""
        brush_button = QPushButton(brush_type)
        brush_button.clicked.connect(lambda: self.select_and_set_brush(brush_type.lower()))
        toolbar.addWidget(brush_button)

    def add_blur_brush_button(self, toolbar):
        """Add a button to select the blur brush."""
        blur_brush_button = QPushButton("Blur Brush")
        blur_brush_button.clicked.connect(self.select_blur_brush)
        toolbar.addWidget(blur_brush_button)

    def add_slider(self, toolbar, label_text, min_val, max_val, initial_val, callback):
        """Helper function to add a slider to the toolbar."""
        toolbar.addWidget(QLabel(label_text))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(initial_val)
        slider.valueChanged.connect(callback)
        toolbar.addWidget(slider)

    def add_eraser_shape_button(self, toolbar, label_text, shape):
        """Helper function to add eraser shape buttons."""
        eraser_button = QPushButton(label_text)
        eraser_button.clicked.connect(lambda: self.set_eraser_shape(shape))
        toolbar.addWidget(eraser_button)

    def select_and_set_brush(self, brush_type):
        """Ensure the Brush tool is selected and set the brush type."""
        current_tool = self.main_window.tool_selection.current_tool

        # If current tool is not a brush, select the brush tool first
        if not isinstance(current_tool, Brush):
            self.main_window.tool_selection.select_brush_tool()  # Ensure brush is selected
            current_tool = self.main_window.tool_selection.current_tool  # Update current_tool

        # Now that the brush tool is selected, set the brush type
        if isinstance(current_tool, Brush):
            current_tool.set_brush_type(brush_type)
            self.main_window.statusBar().showMessage(f"Brush type set to {brush_type.capitalize()}")
            self.main_window.canvas_manager.enable_drawing()
            self.main_window.canvas_manager.update_canvas()
        else:
            self.main_window.statusBar().showMessage("Brush tool not selected properly.")

    def select_blur_brush(self):
        """Select the blur brush tool."""
        self.main_window.tool_selection.current_tool = BlurBrush(self.main_window.canvas_manager)
        self.main_window.statusBar().showMessage("Blur Brush Selected")
        self.main_window.canvas_manager.enable_drawing()

    def change_blur_intensity(self, value):
        """Change the blur intensity of the blur brush."""
        current_tool = self.main_window.tool_selection.current_tool
        if isinstance(current_tool, BlurBrush):
            current_tool.set_blur_strength(value)
            self.main_window.statusBar().showMessage(f"Blur Intensity set to {value}")

    def set_eraser_shape(self, shape):
        """Set the eraser shape if the Eraser tool is selected."""
        current_tool = self.main_window.tool_selection.current_tool
        if isinstance(current_tool, Eraser):
            current_tool.set_eraser_shape(shape)
            self.main_window.statusBar().showMessage(f"Eraser shape set to {shape.capitalize()}")
        else:
            self.main_window.statusBar().showMessage("Select the Eraser Tool to change its shape.")

    def pick_color(self):
        """Open a color picker dialog to choose the drawing color."""
        color = QColorDialog.getColor()
        if color.isValid():
            rgb_color = (color.red(), color.green(), color.blue())
            self.main_window.canvas_manager.set_color(rgb_color)
            self.main_window.statusBar().showMessage(f"Color Selected: {color.name()}")

    def change_thickness(self, value):
        """Adjust the thickness of the current drawing tool."""
        current_tool = self.main_window.tool_selection.current_tool
        if hasattr(current_tool, 'set_thickness'):
            current_tool.set_thickness(value)
        self.main_window.statusBar().showMessage(f"Thickness set to {value}px")

    def change_opacity(self, value):
        """Adjust the opacity of the current drawing tool."""
        opacity = value / 100.0
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
