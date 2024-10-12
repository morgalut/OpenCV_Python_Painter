from PySide6.QtCore import Qt

class MouseEvents:
    def __init__(self, tool_selection):
        self.tool_selection = tool_selection

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton and self.tool_selection.current_tool:
            # Call on_press only if the tool has this method
            if hasattr(self.tool_selection.current_tool, 'on_press'):
                self.tool_selection.current_tool.on_press(event)

    def mouse_move_event(self, event):
        if event.buttons() == Qt.LeftButton and self.tool_selection.current_tool:
            # Call on_drag only if the tool has this method
            if hasattr(self.tool_selection.current_tool, 'on_drag'):
                self.tool_selection.current_tool.on_drag(event)

    def mouse_release_event(self, event):
        if event.button() == Qt.LeftButton and self.tool_selection.current_tool:
            # Call on_release only if the tool has this method
            if hasattr(self.tool_selection.current_tool, 'on_release'):
                self.tool_selection.current_tool.on_release(event)
