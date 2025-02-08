data_file = "C:\\работа\\My_Work_Phoenix\\Daily_Report\\! All DATA !.xlsx"

import sys, re
import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QHeaderView, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox

class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            elif role == Qt.EditRole:
                return self._data.iloc[index.row(), index.column()]
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        return None

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            col = index.column()
            try:
                self._data.iloc[row, col] = value
                self.dataChanged.emit(index, index)
                return True
            except Exception as e:
                print(f"Error setting data: {e}")
                return False
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def sort(self, column, order):
        col_name = self._data.columns[column]
        self._data.sort_values(by=col_name, ascending=order == Qt.AscendingOrder, inplace=True)
        self.layoutChanged.emit()

class MultiFilterMode:
    AND = 0
    OR = 1

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}

    def setFilterByColumn(self, regex, column):
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for key, regex in self.filters.items():
            ix = self.sourceModel().index(source_row, key, source_parent)
            if ix.isValid():
                text = self.sourceModel().data(ix)
                #if not text.contains(regex):
                if regex.indexIn(text, 0)==-1:
                    return False
        return True
    
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pandas TableView with Column Filtering and Sorting")

        # Sample DataFrame (replace with your actual data)
        data = {'col1': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
                'col2': [6, 7, 8, 9, 10, 6, 7, 8, 9, 10],
                'col3': [11, 12, 13, 14, 15, 11, 12, 13, 14, 15],
                'col4': [16, 17, 18, 19, 20, 16, 17, 18, 19, 20],
                'col5': [21, 22, 23, 24, 25, 21, 22, 23, 24, 25],
                'col6': [26, 27, 28, 29, 30, 26, 27, 28, 29, 30],
                'col7': [31, 32, 33, 34, 35, 31, 32, 33, 34, 35],
                'col8': [36, 37, 38, 39, 40, 36, 37, 38, 39, 40],
                'col9': [41, 42, 43, 44, 45, 41, 42, 43, 44, 45],
                'col10': [46, 47, 48, 49, 50, 46, 47, 48, 49, 50]}
        
        data = {"Артикул": ["550042231", "550046940", "550046808", "ATF6011RC", "W309", "W309_", "GS55545D2EUR"],	
                "Продукт + упаковка": ["AGCO PARTS AXLE OIL 80W-90 209л", "AGCO PARTS HYDRAULIC OIL 46 209л", "AGCO PARTS HYDRAULIC OIL 68 209л", "AISIN AFW-6 1л", "ALPHA WAX CARISMA 56 20кг", 
                                       "ALPHA WAX CARISMA 56 20кг", "AUDI LongLife III FE 0W-30 504 00/507 00 1л"],	
                "Product name": ["AGCO PARTS AXLE OIL 80W-90", "AGCO PARTS HYDRAULIC OIL 46", "AGCO PARTS HYDRAULIC OIL 68", "AISIN AFW-6", "ALPHA WAX CARISMA 56", "ALPHA WAX CARISMA 56", 
                                        "AUDI LongLife III FE 0W-30 504 00/507 00"],	
                "Brand": ["AGCO", "AGCO", "AGCO", "AISIN", "ALPHA WAX", "ALPHA WAX", "AUDI"],	
                "ЕИ": ['л', 'л', 'л', 'л', 'кг', 'кг', 'л'],	
                "Вид упаковки": ['бочка', 'бочка', 'бочка', 'канистра', 'пакет', 'ведро', 'канистра'],	
                "Акциз (да/нет)": ['нет', 'нет', 'нет', 'да', 'нет', 'нет', 'да'],	
                "Упаковка для названия": [209, 209, 209, 1, 20, 20, 1],	
                "Упаковка": [209, 209, 209, 1, 20, 20, 1],	
                "Кол-во в упак": [1, 1, 1, 12, 1, 1, 12],	
                "Плотность": [880, 877, 877, 847, 1000, 1000, 838],	
                "Код ТНВЭД": [2710198800, 2710198400, 2710198400, 2710199800, 2712209000, 2712209000, 2710198200]}

        
        
        # self.df = pd.DataFrame(data)
        self.df = pd.read_excel(data_file, sheet_name="Oils")
        self.df = self.df[["Артикул", "ID 1C", "Продукт + упаковка", "Product name", "Type", "Категория", "Brand", 
                            "Family", "ЕИ в 1С", "ЕИ", "Вид упаковки", "Акциз (да/нет)", "ЭкоСбор (да/нет)", 
                            "Упаковка для названия", "Упаковка", "Кол-во в упак", "Плотность", "Код ТНВЭД", 
                            "проверка ТН ВЭД", "Страна происх.", "Stock strategy", "Статус", "ABC"]]
        self.model = PandasModel(self.df)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.sortByColumn(0, Qt.AscendingOrder) #Initial sort

        # Add filter and sort functionality (per column)
        # self.filter_lines = [QLineEdit() for _ in range(self.df.shape[1])]
        # self.sort_combos = [QComboBox() for _ in range(self.df.shape[1])]
        # for i, col in enumerate(self.df.columns):
        #     self.filter_lines[i].setPlaceholderText(f"Filter {col}...")
        #     self.filter_lines[i].textChanged.connect(lambda text, col_index=i: self.filter_column(text, col_index))
        #     self.sort_combos[i].addItem("Ascending")
        #     self.sort_combos[i].addItem("Descending")
        #     self.sort_combos[i].currentIndexChanged.connect(lambda index, col_index=i: self.sort_column(col_index, index))

        #Layout
        layout = QVBoxLayout()
        # for i in range(self.df.shape[1]):
        #     hlayout = QVBoxLayout()
        #     hlayout.addWidget(self.filter_lines[i])
            # hlayout.addWidget(self.sort_combos[i])
            # layout.addLayout(hlayout)
        layout.addWidget(self.table_view)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # def filter_column(self, text, col_index):
    #     filter_str = text.lower()
    #     col_name = self.df.columns[col_index]
    #     filtered_df = self.df[self.df[col_name].astype(str).str.lower().str.contains(filter_str)]
    #     self.model = PandasModel(filtered_df)
    #     self.table_view.setModel(self.model)

    # def sort_column(self, col_index, order):
    #     self.model.sort(col_index, order)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())