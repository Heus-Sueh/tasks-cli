import json
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFont,
    QGroupBox,
    QLabel,
    QMainWindow,
    QMenuBar,
    QVBoxLayout,
    QWidget,
)

JSON_FILE = "tasks.json"


def read_json(json_file: Path) -> list:
    json_file = JSON_FILE
    if Path(json_file).exists():
        try:
            with Path.open(json_file) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error find the json file")
    return []


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("My App")

        self.widget = QWidget()
        self.v_layout = QVBoxLayout()
        self.widget.setLayout(self.v_layout)

        tasks = read_json(JSON_FILE)
        for task in tasks:
            task_widget = TaskWidget(
                task["description"],
                task["status"],
                task["createdAt"],
                task["updatedAt"],
            )
            self.v_layout.addWidget(task_widget)
        # Set the central widget of the Window.
        self.setCentralWidget(self.widget)
        self.v_layout.addWidget(self.widget)
        self._create_menu()

    def _create_menu(self) -> None:
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Exit", self.close)

    def open_file_dialog(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        dialog.setNameFilter("Images (*.png *.jpg)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.file_list.addItems([str(Path(filename)) for filename in filenames])


class TaskWidget(QGroupBox):
    def __init__(
        self,
        description: str,
        status: str,
        created_at: str,
        updated_at: str,
    ) -> None:
        super().__init__()

        self.v_layout = QVBoxLayout()
        self.description = QLabel(description)
        self.status = QLabel(status)
        self.createdAt = QLabel(created_at)
        self.updatedAt = QLabel(updated_at)

        for label in [self.description, self.status, self.createdAt, self.updatedAt]:
            self.v_layout.addWidget(label)

        self.setLayout(self.v_layout)


# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 10))
    # qdarktheme.setup_theme("dark")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
