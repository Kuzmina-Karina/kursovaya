from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox

class AxisDialog(QDialog):
    def __init__(self, headers, parent=None, chart_type="bar"):
        super().__init__(parent)
        self.headers = headers
        self.chart_type = chart_type
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Выбор осей")
        layout = QVBoxLayout()
        
        self.x_combo = QComboBox()
        self.y_combo = QComboBox()
        
        for header in self.headers:
            self.x_combo.addItem(header)
            self.y_combo.addItem(header)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        # Динамические подписи
        x_label_text = (
            "Ось X (текстовые значения):" 
            if self.chart_type == "bar" 
            else "Ось X (числовые значения):"
        )
        layout.addWidget(QLabel(x_label_text))
        layout.addWidget(self.x_combo)
        layout.addWidget(QLabel("Ось Y (числовые значения):"))
        layout.addWidget(self.y_combo)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

    def get_selected_axes(self):
        return (
            self.x_combo.currentText(),
            self.y_combo.currentText()
        )