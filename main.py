from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QAction, QMessageBox
from PyQt5.QtCore import Qt
from widgets import DataTable
from dialogs import AxisDialog
from data_manager import DataManager
from charts import ChartWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataViz Lite")
        self.setGeometry(100, 100, 800, 600)
        
        self.search_button = QPushButton("Найти (Ctrl+F)")
        self.search_button.clicked.connect(self.search_text)
        
        self.data_manager = DataManager()
        self.chart_window = ChartWindow()
        self.table = DataTable()
        
        self.init_ui()
        self.init_menu()

    def init_ui(self):
        self.load_button = QPushButton("Загрузить CSV")
        self.plot_button_S = QPushButton("Столбчатый график")
        self.plot_button_L = QPushButton("Линейный график")
        self.search_button = QPushButton("Найти (Ctrl+F)")  # Добавляем кнопку поиска

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.plot_button_S)
        layout.addWidget(self.plot_button_L)
        layout.addWidget(self.search_button)  # Добавляем кнопку в layout
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_button.clicked.connect(self.load_csv)
        self.plot_button_S.clicked.connect(self.plot_bar)
        self.plot_button_L.clicked.connect(self.plot_line)
        self.search_button.clicked.connect(self.search_text)  # Подключаем обработчик

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        
        open_action = QAction("Открыть CSV...", self)
        open_action.triggered.connect(self.load_csv)
        file_menu.addAction(open_action)
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_csv(self):
        try:
            self.data_manager.load_csv(self)
            if self.data_manager.df is not None:
                self.table.load_data(self.data_manager.df)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")

    def plot_bar(self):
        try:
            data = self.table.get_selected_data()
            if not data or len(data) != 2:
                QMessageBox.warning(self, "Ошибка", "Выделите два столбца!")
                return
                
            dialog = AxisDialog(list(data.keys()), self, chart_type="bar")
            if dialog.exec_() == dialog.Accepted:
                x_header, y_header = dialog.get_selected_axes()
                self.chart_window.show_bar(
                    data[x_header], 
                    data[y_header], 
                    x_header, 
                    y_header
                )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")

    def plot_line(self):
        try:
            data = self.table.get_selected_data()
            if not data or len(data) != 2:
                QMessageBox.warning(self, "Ошибка", "Выделите два столбца!")
                return

            dialog = AxisDialog(list(data.keys()), self, chart_type="line")
            if dialog.exec_() == dialog.Accepted:
                x_header, y_header = dialog.get_selected_axes()
                
                x_data = data.get(x_header, [])
                y_data = data.get(y_header, [])

                if not x_data or not y_data:
                    QMessageBox.warning(self, "Ошибка", "Неверные столбцы!")
                    return
                    
                if not all(isinstance(v, (int, float)) for v in x_data):
                    QMessageBox.warning(self, "Ошибка", f"'{x_header}' должен быть числовым!")
                    return
                    
                if not all(isinstance(v, (int, float)) for v in y_data):
                    QMessageBox.warning(self, "Ошибка", f"'{y_header}' должен быть числовым!")
                    return

                if len(x_data) != len(y_data):
                    QMessageBox.warning(self, "Ошибка", "Столбцы разной длины!")
                    return

                self.chart_window.show_line(x_data, y_data, x_header, y_header)
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")

    def search_text(self):
        query, ok = QInputDialog.getText(self, "Поиск", "Введите текст:")
        if ok:
            self.table.find_text(query)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()