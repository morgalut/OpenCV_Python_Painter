import numpy as np

class BackButton:
    def __init__(self, drawing_manager, max_history=50):
        """
        Initialize the BackButton class.
        
        Args:
            drawing_manager: The drawing manager responsible for canvas drawing operations.
            max_history (int): Maximum number of undo states to store in history.
        """
        self.drawing_manager = drawing_manager
        self.history = []  # Store history of canvas states for undo
        self.max_history = max_history  # Limit the size of the history to avoid memory overflow

    def save_state(self):
        """
        Save the current canvas state to the history.
        Ensures the number of saved states does not exceed `max_history`.
        """
        # Save a deep copy of the current image to the history stack
        if len(self.history) >= self.max_history:
            self.history.pop(0)  # Remove the oldest state if history exceeds max limit
        self.history.append(np.copy(self.drawing_manager.image))

    def undo(self):
        """
        Undo the last action by restoring the previous canvas state.
        If no more history is available, it prints a message and does nothing.
        """
        if self.history:
            last_state = self.history.pop()
            self.drawing_manager.update_canvas_with_image(last_state)
        else:
            print("No more actions to undo.")

    def clear_history(self):
        """Clear the undo history."""
        self.history.clear()

    def can_undo(self):
        """Check if there are states in the history that can be undone."""
        return bool(self.history)
