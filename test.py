# import operator
# from PySide6 import QtWidgets
# from PySide6 import QtGui
# from PySide6 import QtCore


# class MyWindow(QtWidgets.QWidget):
#     def __init__(self, data_list, header, *args):
#         QtWidgets.QWidget.__init__(self, *args)
#         # setGeometry(x_pos, y_pos, width, height)
#         self.setGeometry(300, 200, 570, 450)
#         self.setWindowTitle("Click on column title to sort")
#         table_model = MyTableModel(self, data_list, header)
#         table_view = QtWidgets.QTableView()
#         table_view.setModel(table_model)
#         # set font
#         font = QtGui.QFont("Courier New", 14)
#         table_view.setFont(font)
#         # set column width to fit contents (set font first!)
#         table_view.resizeColumnsToContents()
#         # enable sorting
#         table_view.setSortingEnabled(True)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(table_view)
#         self.setLayout(layout)


# class MyTableModel(QtCore.QAbstractTableModel):
#     def __init__(self, parent, mylist, header, *args):
#         QtCore.QAbstractTableModel.__init__(self, parent, *args)
#         self.mylist = mylist
#         self.header = header

#     def rowCount(self, parent):
#         return len(self.mylist)

#     def columnCount(self, parent):
#         return len(self.mylist[0])

#     def data(self, index, role):
#         if not index.isValid():
#             return None
#         elif role != QtCore.Qt.DisplayRole:
#             return None
#         return self.mylist[index.row()][index.column()]

#     def headerData(self, col, orientation, role):
#         if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#             return self.header[col]
#         return None

#     def sort(self, col, order):
#         """sort table by given column number col"""
#         self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
#         self.mylist = sorted(self.mylist,
#                              key=operator.itemgetter(col))
#         if order == QtCore.Qt.DescendingOrder:
#             self.mylist.reverse()
#         self.emit(QtCore.SIGNAL("layoutChanged()"))


# # the solvent data ...
# header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
# # use numbers for numeric data to sort properly
# data_list = [
#     ('ACETIC ACID', 117.9, 16.7, 1.049),
#     ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
#     ('ACETONE', 56.3, -94.7, 0.791),
#     ('ACETONITRILE', 81.6, -43.8, 0.786),
#     ('ANISOLE', 154.2, -37.0, 0.995),
#     ('BENZYL ALCOHOL', 205.4, -15.3, 1.045),
#     ('BENZYL BENZOATE', 323.5, 19.4, 1.112),
#     ('BUTYL ALCOHOL NORMAL', 117.7, -88.6, 0.81),
#     ('BUTYL ALCOHOL SEC', 99.6, -114.7, 0.805),
#     ('BUTYL ALCOHOL TERTIARY', 82.2, 25.5, 0.786),
#     ('CHLOROBENZENE', 131.7, -45.6, 1.111),
#     ('CYCLOHEXANE', 80.7, 6.6, 0.779),
#     ('CYCLOHEXANOL', 161.1, 25.1, 0.971),
#     ('CYCLOHEXANONE', 155.2, -47.0, 0.947),
#     ('DICHLOROETHANE 1 2', 83.5, -35.7, 1.246),
#     ('DICHLOROMETHANE', 39.8, -95.1, 1.325),
#     ('DIETHYL ETHER', 34.5, -116.2, 0.715),
#     ('DIMETHYLACETAMIDE', 166.1, -20.0, 0.937),
#     ('DIMETHYLFORMAMIDE', 153.3, -60.4, 0.944),
#     ('DIMETHYLSULFOXIDE', 189.4, 18.5, 1.102),
#     ('DIOXANE 1 4', 101.3, 11.8, 1.034),
#     ('DIPHENYL ETHER', 258.3, 26.9, 1.066),
#     ('ETHYL ACETATE', 77.1, -83.9, 0.902),
#     ('ETHYL ALCOHOL', 78.3, -114.1, 0.789),
#     ('ETHYL DIGLYME', 188.2, -45.0, 0.906),
#     ('ETHYLENE CARBONATE', 248.3, 36.4, 1.321),
#     ('ETHYLENE GLYCOL', 197.3, -13.2, 1.114),
#     ('FORMIC ACID', 100.6, 8.3, 1.22),
#     ('HEPTANE', 98.4, -90.6, 0.684),
#     ('HEXAMETHYL PHOSPHORAMIDE', 233.2, 7.2, 1.027),
#     ('HEXANE', 68.7, -95.3, 0.659),
#     ('ISO OCTANE', 99.2, -107.4, 0.692),
#     ('ISOPROPYL ACETATE', 88.6, -73.4, 0.872),
#     ('ISOPROPYL ALCOHOL', 82.3, -88.0, 0.785),
#     ('METHYL ALCOHOL', 64.7, -97.7, 0.791),
#     ('METHYL ETHYLKETONE', 79.6, -86.7, 0.805),
#     ('METHYL ISOBUTYL KETONE', 116.5, -84.0, 0.798),
#     ('METHYL T-BUTYL ETHER', 55.5, -10.0, 0.74),
#     ('METHYLPYRROLIDINONE N', 203.2, -23.5, 1.027),
#     ('MORPHOLINE', 128.9, -3.1, 1.0),
#     ('NITROBENZENE', 210.8, 5.7, 1.208),
#     ('NITROMETHANE', 101.2, -28.5, 1.131),
#     ('PENTANE', 36.1, ' -129.7', 0.626),
#     ('PHENOL', 181.8, 40.9, 1.066),
#     ('PROPANENITRILE', 97.1, -92.8, 0.782),
#     ('PROPIONIC ACID', 141.1, -20.7, 0.993),
#     ('PROPIONITRILE', 97.4, -92.8, 0.782),
#     ('PROPYLENE GLYCOL', 187.6, -60.1, 1.04),
#     ('PYRIDINE', 115.4, -41.6, 0.978),
#     ('SULFOLANE', 287.3, 28.5, 1.262),
#     ('TETRAHYDROFURAN', 66.2, -108.5, 0.887),
#     ('TOLUENE', 110.6, -94.9, 0.867),
#     ('TRIETHYL PHOSPHATE', 215.4, -56.4, 1.072),
#     ('TRIETHYLAMINE', 89.5, -114.7, 0.726),
#     ('TRIFLUOROACETIC ACID', 71.8, -15.3, 1.489),
#     ('WATER', 100.0, 0.0, 1.0),
#     ('XYLENES', 139.1, -47.8, 0.86)
# ]
# app = QtWidgets.QApplication([])
# win = MyWindow(data_list, header)
# win.show()
# app.exec_()

# import sys
# import pandas as pd
# from PySide6.QtCore import (QAbstractTableModel, QModelIndex, QSortFilterProxyModel, Qt, Signal)
# from PySide6.QtWidgets import (QApplication, QLineEdit, QTableView, QVBoxLayout, QWidget, QLabel, QHeaderView)


# data = {
#     "Артикул": ["550042231", "550046940", "550046808", "ATF6011RC", "W309", "W309_", "GS55545D2EUR"],
#     "Продукт + упаковка": ["AGCO PARTS AXLE OIL 80W-90 209л", "AGCO PARTS HYDRAULIC OIL 46 209л", "AGCO PARTS HYDRAULIC OIL 68 209л", "AISIN AFW-6 1л", "ALPHA WAX CARISMA 56 20кг", "ALPHA WAX CARISMA 56 20кг", "AUDI LongLife III FE 0W-30 504 00/507 00 1л"],
#     "Product name": ["AGCO PARTS AXLE OIL 80W-90", "AGCO PARTS HYDRAULIC OIL 46", "AGCO PARTS HYDRAULIC OIL 68", "AISIN AFW-6", "ALPHA WAX CARISMA 56", "ALPHA WAX CARISMA 56", "AUDI LongLife III FE 0W-30 504 00/507 00"],
#     "Brand": ["AGCO", "AGCO", "AGCO", "AISIN", "ALPHA WAX", "ALPHA WAX", "AUDI"],
#     "ЕИ": ["л", "л", "л", "л", "кг", "кг", "л"],
#     "Вид упаковки": ["бочка", "бочка", "бочка", "канистра", "пакет", "ведро", "канистра"],
#     "Акциз (да/нет)": ["нет", "нет", "нет", "да", "нет", "нет", "да"],
#     "Упаковка для названия": [209, 209, 209, 1, 20, 20, 1],
#     "Упаковка": [209, 209, 209, 1, 20, 20, 1],
#     "Кол-во в упак": [1, 1, 1, 12, 1, 1, 12],
#     "Плотность": [880, 877, 877, 847, 1000, 1000, 838],
#     "Код ТНВЭД": [2710198800, 2710198400, 2710198400, 2710199800, 2712209000, 2712209000, 2710198200],
# }

# df = pd.DataFrame(data)
data_file = "C:\\работа\\My_Work_Phoenix\\Daily_Report\\! All DATA !.xlsx"

# class PandasModel(QAbstractTableModel):
#     def __init__(self, data):
#         QAbstractTableModel.__init__(self)
#         self._data = data
#         self.dataChangedSignal = Signal(pd.DataFrame)  # Custom signal

#     def rowCount(self, parent=None):
#         return len(self._data.values)

#     def columnCount(self, parent=None):
#         return self._data.columns.size

#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 return str(self._data.iloc[index.row(), index.column()])
#             elif role == Qt.EditRole:
#                 return self._data.iloc[index.row(), index.column()]
#         return None

#     def headerData(self, section, orientation, role):
#         if role == Qt.DisplayRole:
#             if orientation == Qt.Horizontal:
#                 return str(self._data.columns[section])
#             else:
#                 return str(self._data.index[section])
#         return None
    
#     def setData(self, index, value, role):
#         if role == Qt.EditRole:
#             self._data.iloc[index.row(), index.column()] = value
#             self.dataChanged.emit(index, index)
#             self.dataChangedSignal.emit(self._data)  # Emit signal with updated DataFrame
#             return True
#         return False

#     def flags(self, index):
#         return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         df = pd.read_excel(data_file, sheet_name="Oils")
#         df = df[["Артикул", "ID 1C", "Продукт + упаковка", "Product name", "Type", "Категория", "Brand", 
#                             "Family", "ЕИ в 1С", "ЕИ", "Вид упаковки", "Акциз (да/нет)", "ЭкоСбор (да/нет)", 
#                             "Упаковка для названия", "Упаковка", "Кол-во в упак", "Плотность", "Код ТНВЭД", 
#                             "проверка ТН ВЭД", "Страна происх.", "Stock strategy", "Статус", "ABC"]]
        
#         self.model = PandasModel(df)
#         self.proxy_model = QSortFilterProxyModel()
#         self.proxy_model.setSourceModel(self.model)

#         self.table_view = QTableView()
#         self.table_view.setModel(self.proxy_model)
#         self.table_view.setSortingEnabled(True)
        
#         # Resize header to content
#         # header = self.table_view.horizontalHeader()
#         # header.setSectionResizeMode(QHeaderView.ResizeToContents) #Added this line

#         self.filter_line_edits = {}
#         filter_columns = ["Артикул", "Продукт + упаковка", "Brand", "Код ТНВЭД"]
#         for column_name in filter_columns:
#             line_edit = QLineEdit()
#             line_edit.textChanged.connect(lambda text, col=column_name: self.filter_table(text, col))
#             self.filter_line_edits[column_name] = line_edit

#         layout = QVBoxLayout()
#         for col in filter_columns:
#             layout.addWidget(QLabel(f"Filter {col}:"))
#             layout.addWidget(self.filter_line_edits[col])
#         layout.addWidget(self.table_view)
#         self.setLayout(layout)

#     def filter_table(self, text, column_name):
#         filter_string = text
#         column_index = self.model.headerData(self.model._data.columns.get_loc(column_name), Qt.Horizontal, Qt.DisplayRole)
#         self.proxy_model.setFilterRegExp(filter_string)
#         self.proxy_model.setFilterKeyColumn(column_index)
        
#     def handle_data_changes(self, updated_df):
#         print("Data changed:")
#         print(updated_df)  # Process the updated DataFrame here
#         # Save to file, update database, or perform other actions
#         # Example: updated_df.to_csv("updated_data.csv", index=False)



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
# import pandas as pd
# from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
#                              QLineEdit, QTableWidget, QTableWidgetItem,
#                              QHeaderView)
# from PySide6.QtCore import Qt


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

        # self.df = pd.DataFrame({  # DataFrame remains the same
        #     "Артикул": ["550042231", "550046940", "550046808", "ATF6011RC", "W309", "W309_", "GS55545D2EUR"],
        #     "Продукт + упаковка": ["AGCO PARTS AXLE OIL 80W-90 209л", "AGCO PARTS HYDRAULIC OIL 46 209л", "AGCO PARTS HYDRAULIC OIL 68 209л", "AISIN AFW-6 1л", "ALPHA WAX CARISMA 56 20кг",
        #                           "ALPHA WAX CARISMA 56 20кг", "AUDI LongLife III FE 0W-30 504 00/507 00 1л"],
        #     "Product name": ["AGCO PARTS AXLE OIL 80W-90", "AGCO PARTS HYDRAULIC OIL 46", "AGCO PARTS HYDRAULIC OIL 68", "AISIN AFW-6", "ALPHA WAX CARISMA 56", "ALPHA WAX CARISMA 56",
        #                      "AUDI LongLife III FE 0W-30 504 00/507 00"],
        #     "Brand": ["AGCO", "AGCO", "AGCO", "AISIN", "ALPHA WAX", "ALPHA WAX", "AUDI"],
        #     "ЕИ": ['л', 'л', 'л', 'л', 'кг', 'кг', 'л'],
        #     "Вид упаковки": ['бочка', 'бочка', 'бочка', 'канистра', 'пакет', 'ведро', 'канистра'],
        #     "Акциз (да/нет)": ['нет', 'нет', 'нет', 'да', 'нет', 'нет', 'да'],
        #     "Упаковка для названия": [209, 209, 209, 1, 20, 20, 1],
        #     "Упаковка": [209, 209, 209, 1, 20, 20, 1],
        #     "Кол-во в упак": [1, 1, 1, 12, 1, 1, 12],
        #     "Плотность": [880, 877, 877, 847, 1000, 1000, 838],
        #     "Код ТНВЭД": [2710198800, 2710198400, 2710198400, 2710199800, 2712209000, 2712209000, 2710198200]
        # })
#         self.df = pd.read_excel(data_file, sheet_name="Oils")
#         self.df = self.df[["Артикул", "ID 1C", "Продукт + упаковка", "Product name", "Type", "Категория", "Brand", 
#                             "Family", "ЕИ в 1С", "ЕИ", "Вид упаковки", "Акциз (да/нет)", "ЭкоСбор (да/нет)", 
#                             "Упаковка для названия", "Упаковка", "Кол-во в упак", "Плотность", "Код ТНВЭД", 
#                             "проверка ТН ВЭД", "Страна происх.", "Stock strategy", "Статус", "ABC"]]
        
#         self.table = QTableWidget()
#         self.table.setColumnCount(len(self.df.columns))
#         self.table.setRowCount(len(self.df))
#         self.table.setHorizontalHeaderLabels(self.df.columns)
#         self.populate_table()

#         filter_columns = ["Артикул", "Продукт + упаковка", "Вид упаковки", "Код ТНВЭД"]
#         self.filters = {col: QLineEdit() for col in filter_columns}
#         for i, col in enumerate(filter_columns):
#             self.filters[col].textChanged.connect(lambda text, col=col: self.filter_table(col, text))

#         layout = QVBoxLayout()
#         for col in filter_columns:
#             layout.addWidget(self.filters[col])
#         layout.addWidget(self.table)
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#     def populate_table(self):
#         for i, row in self.df.iterrows():
#             for j, col in enumerate(self.df.columns):
#                 item = QTableWidgetItem(str(row[col]))
#                 self.table.setItem(i, j, item)

#     def filter_table(self, column, text):
#         filter_string = text.lower()
#         filtered_df = self.df[self.df[column].str.lower().str.contains(filter_string)]
#         self.table.setRowCount(len(filtered_df))
#         self.populate_table(filtered_df)  # Update the table with filtered data

#     def populate_table(self, df=None):
#         df_to_use = df if df is not None else self.df
#         for i, row in df_to_use.iterrows():
#             for j, col in enumerate(df_to_use.columns):
#                 item = QTableWidgetItem(str(row[col]))
#                 self.table.setItem(i, j, item)

#     def sort_table(self, column, order):
#         self.df.sort_values(by=self.df.columns[column], ascending=order == Qt.AscendingOrder, inplace=True)
#         self.populate_table()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

data_file = "C:\\работа\\My_Work_Phoenix\\Daily_Report_QT\\WorkFiles\\! All DATA !.xlsx"
import pandas as pd


df = pd.read_excel(data_file, sheet_name="экосбор_ставки", skiprows=1)
df = df.drop(["признак", "группа"], axis=1)
df_melted = df.melt(id_vars=["Код ТНВЭД",  ])
df_melted = df_melted.rename(columns={"Код ТНВЭД": "TNVED", "variable": "Year", "value": "amount"})
df_melted = df_melted.sort_values(["TNVED", "Year"])
df_melted["id"] = df_melted.TNVED.astype(str) + "_" + df_melted.Year.astype(str)
# print(df_melted.to_string())
print(df_melted)
