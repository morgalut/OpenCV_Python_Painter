from PySide6.QtWidgets import QToolBar, QColorDialog, QSlider, QLabel, QPushButton
from PySide6.QtCore import Qt
from tools.Brush.BlurBrush import BlurBrush
from tools.Brush.brush import Brush
from tools.line import Line  # Import the Line tool
from tools.back_button import BackButton  # Import BackButton class

class ToolbarManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.back_button = BackButton(main_window.canvas_manager.drawing_manager)  # Initialize BackButton with drawing manager

    def init_toolbar(self):
        """
        Initialize the toolbar and add all necessary tools, sliders, and buttons.
        """
        toolbar = QToolBar("Tools")
        self.main_window.addToolBar(toolbar)

        # Add Undo button (disabled initially)
        self.add_undo_button(toolbar)
        self.undo_button.setEnabled(False)

        # Add tool buttons (Pen, Brush, Line, Eraser, etc.)
        self.add_tool_buttons(toolbar)

        # Add sliders for adjusting tool properties
        self.add_sliders(toolbar)

        # Add Zoom controls
        self.add_zoom_controls(toolbar)

        # Update the state of the undo button
        self.update_undo_button()

    def add_undo_button(self, toolbar):
        """
        Adds the undo button to the toolbar and connects it to the undo functionality.
        """
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_last_action)
        toolbar.addWidget(undo_button)
        self.undo_button = undo_button

    def undo_last_action(self):
        """
        Trigger the undo functionality and update the undo button state.
        """
        if self.main_window.tool_selection.back_button.can_undo():
            self.main_window.tool_selection.back_button.undo()
        else:
            print("No more actions to undo.")
        self.update_undo_button()

    def update_undo_button(self):
        """
        Enable or disable the undo button based on whether undo actions are available.
        """
        can_undo = self.main_window.tool_selection.back_button.can_undo()
        self.undo_button.setEnabled(can_undo)

    def add_tool_buttons(self, toolbar):
        """
        Adds buttons for tools like Pen, Brush, Line, Eraser, and Color Picker.
        """
        # Add Pen tool button
        pen_button = QPushButton("Pen Tool")
        pen_button.clicked.connect(self.main_window.tool_selection.select_pen_tool)
        toolbar.addWidget(pen_button)

        # Add Line tool button
        line_button = QPushButton("Line Tool")
        line_button.clicked.connect(self.main_window.tool_selection.select_line_tool)
        toolbar.addWidget(line_button)

        # Add Brush tool buttons (different brush types)
        toolbar.addWidget(QLabel("Brush Type:"))
        self.add_brush_button(toolbar, "Bristle")
        self.add_brush_button(toolbar, "Soft")
        self.add_brush_button(toolbar, "Textured")
        self.add_blur_brush_button(toolbar)

        # Add Eraser tool button
        eraser_button = QPushButton("Eraser Tool")
        eraser_button.clicked.connect(self.main_window.tool_selection.select_eraser_tool)
        toolbar.addWidget(eraser_button)

        # Add Color Picker button
        color_picker_button = QPushButton("Pick Color")
        color_picker_button.clicked.connect(self.pick_color)
        toolbar.addWidget(color_picker_button)

        # Add Clear Canvas button
        clear_canvas_button = QPushButton("Clear Canvas")
        clear_canvas_button.clicked.connect(self.main_window.canvas_manager.clear_canvas)
        toolbar.addWidget(clear_canvas_button)

    def add_sliders(self, toolbar):
        """
        Adds sliders to adjust tool properties like thickness, opacity, and blur intensity.
        """
        # Thickness Slider
        thickness_slider = QSlider(Qt.Horizontal)
        thickness_slider.setMinimum(1)
        thickness_slider.setMaximum(30)
        thickness_slider.setValue(self.main_window.canvas_manager.thickness)
        thickness_slider.valueChanged.connect(self.change_thickness)
        toolbar.addWidget(QLabel("Thickness:"))
        toolbar.addWidget(thickness_slider)

        # Opacity Slider
        opacity_slider = QSlider(Qt.Horizontal)
        opacity_slider.setMinimum(0)
        opacity_slider.setMaximum(100)
        opacity_slider.setValue(int(self.main_window.canvas_manager.opacity * 100))
        opacity_slider.valueChanged.connect(self.change_opacity)
        toolbar.addWidget(QLabel("Opacity:"))
        toolbar.addWidget(opacity_slider)

        # Blur Intensity Slider
        blur_slider = QSlider(Qt.Horizontal)
        blur_slider.setMinimum(1)
        blur_slider.setMaximum(50)
        blur_slider.setValue(5)
        blur_slider.valueChanged.connect(self.change_blur_intensity)
        toolbar.addWidget(QLabel("Blur Intensity:"))
        toolbar.addWidget(blur_slider)

    def add_zoom_controls(self, toolbar):
        """
        Adds zoom in/out controls to the toolbar.
        """
        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.main_window.canvas_manager.zoom_in)
        toolbar.addWidget(zoom_in_button)

        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.main_window.canvas_manager.zoom_out)
        toolbar.addWidget(zoom_out_button)

    def add_brush_button(self, toolbar, brush_type):
        """
        Helper function to add a brush tool button.
        """
        brush_button = QPushButton(brush_type)
        brush_button.clicked.connect(lambda: self.select_and_set_brush(brush_type.lower()))
        toolbar.addWidget(brush_button)

    def add_blur_brush_button(self, toolbar):
        """
        Add a button to select the blur brush tool.
        """
        blur_brush_button = QPushButton("Blur Brush")
        blur_brush_button.clicked.connect(self.select_blur_brush)
        toolbar.addWidget(blur_brush_button)

    def select_and_set_brush(self, brush_type):
        """
        Select and set the current brush type.
        """
        current_tool = self.main_window.tool_selection.current_tool
        if not isinstance(current_tool, Brush):
            self.main_window.tool_selection.select_brush_tool()
            current_tool = self.main_window.tool_selection.current_tool
        if isinstance(current_tool, Brush):
            current_tool.set_brush_type(brush_type)
            self.main_window.statusBar().showMessage(f"Brush type set to {brush_type.capitalize()}")
            self.main_window.canvas_manager.enable_drawing()
            self.main_window.canvas_manager.update_canvas()

    def select_blur_brush(self):
        """
        Select the blur brush tool.
        """
        self.main_window.tool_selection.current_tool = BlurBrush(self.main_window.canvas_manager)
        self.main_window.statusBar().showMessage("Blur Brush Selected")
        self.main_window.canvas_manager.enable_drawing()

    def pick_color(self):
        """
        Open a color picker dialog to select a color for drawing.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            rgb_color = (color.red(), color.green(), color.blue())
            self.main_window.canvas_manager.set_color(rgb_color)
            self.main_window.statusBar().showMessage(f"Color Selected: {color.name()}")

    def change_thickness(self, value):
        """
        Change the thickness of the current drawing tool.
        """
        current_tool = self.main_window.tool_selection.current_tool
        if hasattr(current_tool, 'set_thickness'):
            current_tool.set_thickness(value)
        self.main_window.statusBar().showMessage(f"Thickness set to {value}px")

    def change_opacity(self, value):
        """
        Change the opacity of the current drawing tool.
        """
        opacity = value / 100.0
        current_tool = self.main_window.tool_selection.current_tool
        if hasattr(current_tool, 'set_opacity'):
            current_tool.set_opacity(opacity)
        self.main_window.statusBar().showMessage(f"Opacity set to {opacity * 100:.0f}%")

    def change_blur_intensity(self, value):
        """
        Change the blur intensity of the blur brush tool.
        """
        current_tool = self.main_window.tool_selection.current_tool
        if isinstance(current_tool, BlurBrush):
            current_tool.set_blur_strength(value)
            self.main_window.statusBar().showMessage(f"Blur Intensity set to {value}")
