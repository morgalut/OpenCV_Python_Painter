import sys
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow
from GUI.gui import DrawingApp

class Worker(QThread):
    finished = Signal()
    error = Signal(str)

    def run(self):
        try:
            # Simulate a long-running task
            import time
            print("Worker: Simulating task...")
            time.sleep(5)  # Replace with actual work
            self.finished.emit()  # Signal when task is complete
        except Exception as e:
            self.error.emit(str(e))  # Emit an error signal with the exception message

class DrawingAppWithWorker(DrawingApp):
    def __init__(self):
        super().__init__()

        # Initialize the worker thread but don't start immediately
        self.worker = Worker()
        self.worker.finished.connect(self.on_task_finished)
        self.worker.error.connect(self.on_task_error)

    def start_background_task(self):
        """Start the worker thread for background processing."""
        if not self.worker.isRunning():
            print("Starting background task...")
            self.worker.start()
        else:
            print("Worker is already running.")

    def on_task_finished(self):
        """Handle when the background task finishes."""
        print("Background task finished")
        # Optionally update the GUI or notify the user

    def on_task_error(self, error_message):
        """Handle errors from the worker."""
        print(f"Error occurred: {error_message}")
        # Optionally display an error message to the user

def main():
    # Create the QApplication
    app = QApplication(sys.argv)

    # Create and show the main window with background task capabilities
    window = DrawingAppWithWorker()
    window.show()

    # Start the worker task (can be delayed or conditional)
    window.start_background_task()

    # Execute the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
