from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = None
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("График")
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить график")
        self.save_button.clicked.connect(self.save_chart)
        self.button_layout.addWidget(self.save_button)
        
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.resize(800, 600)

    def show_bar(self, x_data, y_data, x_label, y_label):
        self._clear_canvas()
        self.figure = Figure(figsize=(12, 6))
        ax = self.figure.add_subplot(111)
        ax.bar(x_data, y_data, color='#4c72b0')
        ax.set_title(f"{y_label} по {x_label}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        self._draw_canvas()

    def show_line(self, x_data, y_data, x_label, y_label):
        self._clear_canvas()
        sorted_data = sorted(zip(x_data, y_data), key=lambda x: x[0])
        x_sorted, y_sorted = zip(*sorted_data)
        
        self.figure = Figure(figsize=(12, 6))
        ax = self.figure.add_subplot(111)
        ax.plot(x_sorted, y_sorted, marker='o', linestyle='-', color='#2ca25f')
        ax.set_title(f"{y_label} vs {x_label}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True)
        self._draw_canvas()

    def _draw_canvas(self):
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(self.button_layout)
        self.show()

    def _clear_canvas(self):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

    def save_chart(self):
        if self.figure is None:
            QMessageBox.critical(self, "Ошибка", "Нет активного графика!")
            return

        formats = "PNG (*.png);;JPEG (*.jpg *.jpeg)"
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Сохранить график", "", formats
        )

        if not file_path:
            return

        try:
            if "PNG" in selected_filter:
                self.figure.savefig(file_path, dpi=300, format='png', bbox_inches='tight')
            else:
                self.figure.savefig(file_path, dpi=300, format='jpeg', bbox_inches='tight')
                
            QMessageBox.information(self, "Успех", "График сохранен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")