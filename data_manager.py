import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class DataManager:
    def __init__(self):
        self.df = None

    def load_csv(self, parent):
        file_path, _ = QFileDialog.getOpenFileName(
            parent, "Выберите CSV", "", "CSV Files (*.csv)")
        
        if not file_path:
            return
        
        try:
            self.df = pd.read_csv(file_path, sep=None, engine='python')
        except Exception as e:
            QMessageBox.critical(parent, "Ошибка", f"Ошибка: {str(e)}")
            self.df = None