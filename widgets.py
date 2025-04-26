from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import ctypes
import os

class DataTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(self.ExtendedSelection)
        self.setSelectionBehavior(self.SelectItems)
        self.lib = ctypes.CDLL(os.path.abspath("libfast_search.so"))  # или .dll
        self.lib.find_matches.restype = None
        self.lib.find_matches.argtypes = [
            ctypes.POINTER(ctypes.c_char_p),  # data
            ctypes.c_int,                     # rows
            ctypes.c_int,                     # cols
            ctypes.c_char_p,                  # query
            ctypes.POINTER(ctypes.c_int)      # results
        ]

    def find_text(self, query):
        from PyQt5.QtGui import QColor  # Добавляем импорт
        
        rows = self.rowCount()
        cols = self.columnCount()
        
        # Подготовка данных для C++
        data = []
        for row in range(rows):
            for col in range(cols):
                item = self.item(row, col)
                text = item.text() if item else ""
                data.append(text.encode('utf-8'))
        
        # Вызов C++ функции
        query_encoded = query.encode('utf-8')
        results = (ctypes.c_int * rows)()
        data_ptr = (ctypes.c_char_p * len(data))(*data)
        
        self.lib.find_matches(
            data_ptr, rows, cols, query_encoded, results
        )
        
        # Подсветка найденных строк
        for row in range(rows):
            color = QColor("#FFCCCB") if results[row] else QColor("#FFFFFF")
            for col in range(cols):
                if self.item(row, col):
                    self.item(row, col).setBackground(color)
                
    def load_data(self, df):
        self.clear()
        self.setRowCount(len(df))
        self.setColumnCount(len(df.columns))
        self.setHorizontalHeaderLabels(df.columns.tolist())

        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.setItem(row, col, item)
        
        self.resizeColumnsToContents()

    def get_selected_data(self):
        selected = {}
        for item in self.selectedItems():
            col = item.column()
            row = item.row()
            header = self.horizontalHeaderItem(col).text()
            
            if header not in selected:
                selected[header] = {}
            
            try:
                value = float(item.text().replace(',', '.'))
            except ValueError:
                value = item.text().strip()
            
            selected[header][row] = value

        rows = set().union(*[d.keys() for d in selected.values()])
        return {
            header: [col_data[row] for row in sorted(rows) 
            if row in col_data] 
            for header, col_data in selected.items()
        }