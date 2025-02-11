import sys
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QMessageBox
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload, exc
from sqlalchemy.exc import SQLAlchemyError
from models import *
from db import db, Base, engine

# SQLAlchemy setup
# Base = declarative_base()

# class Item(Base):
#     __tablename__ = 'items'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)

# engine = create_engine('sqlite:///mydatabase.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()


class TableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            col = index.column()
            try:
                item_id = self._data[row][0]  # Assuming ID is the first column
                if col == 1:  # Update name
                    db.query(Material).filter(Material.id == item_id).update({"prod_art": value})
                elif col == 2:  # Update description
                    db.query(Material).filter(Material.id == item_id).update({"Material_Name": value})
                self._data[row][col] = value
                self.dataChanged.emit(index, index)
                db.commit()  # Commit changes to the database
                return True
            except exc.SQLAlchemyError as e:
                QMessageBox.critical(None, "Database Error", f"Error updating database: {e}")
                db.rollback()  # Rollback transaction on error
                return False
            except Exception as e:
                print(f"Error setting data: {e}")
                return False
        return False

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

class CombinedTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = ["id", "prod_art", "Material_Name", "Pack_type", "Pack", "Product_Name", "Type",  ] # Add more headers as needed

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            col = index.column()
            try:
                item_id = self._data[row][0]  # Assuming ID is the first column
                if col == 1:  # Update name
                    db.query(Material).filter(Material.id == item_id).update({"prod_art": value})
                elif col == 2:  # Update description
                    db.query(Material).filter(Material.id == item_id).update({"Material_Name": value})
                elif col == 3:  # Update description
                    db.query(Material).filter(Material.id == item_id).update({"Pack_type": value})
                # elif col == 5:  # Update description
                #     prod_name = db.query(Material).filter(Material.id == item_id)
                #     prod_name_id = prod_name.ProdName_id
                #     print(prod_name_id)
                #     db.query(ProdName).filter(ProdName.id == prod_name_id).update({"Product_Name": value})
                    
                self._data[row][col] = value
                self.dataChanged.emit(index, index)
                db.commit()  # Commit changes to the database
                return True
            except exc.SQLAlchemyError as e:
                QMessageBox.critical(None, "Database Error", f"Error updating database: {e}")
                db.rollback()  # Rollback transaction on error
                return False
            except Exception as e:
                print(f"Error setting data: {e}")
                return False
        return False

    def flags(self, index):
        if index.column() < 5: #Only allow editing of ProdName columns
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Table View")
        self.table_view = QTableView()
        self.setCentralWidget(self.table_view)
        self.populate_table()

    def populate_table(self):
        # items = db.query(Material).join(ProdName).all()
        # data = [[item.id, item.prod_art, item.Material_Name,  ] for item in items]
        # model = TableModel(data)
        # self.table_view.setModel(model)
        # self.table_view.resizeColumnsToContents()
        
        items = db.query(Material).options(joinedload(Material.ProdName_Table)).all()
        data = []
        for item in items:
            # for prodname in item.ProdName_Table:
                row = [item.id, item.prod_art, item.Material_Name, item.Pack_type, item.Pack,  
                            item.ProdName_Table.Product_Name, item.ProdName_Table.Type,  ] # Add more columns as needed
                data.append(row)
        model = CombinedTableModel(data)
        self.table_view.setModel(model)
        self.table_view.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())