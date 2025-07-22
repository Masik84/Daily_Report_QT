import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, 
                              QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from functools import lru_cache

from wind.pages.products_ui import Ui_Form
from config import Material_file
from models import Material
from db import db


class Product(QWidget):
    def __init__(self):
        super(Product, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._setup_ui()
        self._setup_connections()
        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.line_Brand.currentTextChanged.connect(self.fill_in_prod_fam_list)
        self.ui.line_Prod_Fam.currentTextChanged.connect(self.fill_in_prod_name_list)
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_Product)

    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл')
        if file_path:
            self.ui.label_Prod_File.setText(file_path)

    def upload_data(self):
        """Загрузка данных в базу"""
        file_path = self.ui.label_Prod_File.text() or Material_file
        
        try:
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")
                
            self.run_product_func(file_path)
            self.show_message('База данных обновлена!')
            self.refresh_all_comboboxes()
            
        except Exception as e:
            db.session.rollback()
            self._handle_upload_error(e)
        finally:
            self.ui.label_Prod_File.setText("Выбери файл или нажми Upload")

    def _handle_upload_error(self, error):
        """Обработка ошибок загрузки"""
        if "transaction is already begun" in str(error):
            msg = "Ошибка БД. Закройте программу и попробуйте снова."
        elif "required columns" in str(error).lower():
            msg = "Файл не содержит всех необходимых столбцов."
        else:
            msg = f"Ошибка загрузки данных: {str(error)}"
        self.show_error_message(msg)

    def run_product_func(self, data_file_xls):
        """Основная функция обработки данных"""
        data = self.read_product_file(data_file_xls)
        self.save_Material(data)

    def read_product_file(self, file_path):
        """Чтение данных из Excel"""
        try:
            dtype_prod = {"Артикул": str, "ТН ВЭД": str}
            df = pd.read_excel(file_path, sheet_name=0, dtype=dtype_prod)
            
            required_columns = ['Код', 'Product name', 'Шт в комплекте', 'Единица измерения отчетов']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит необходимых столбцов")
            
            column_map = {
                'Код': 'Code', 'Артикул': 'Article', 'Наименование': 'Material_Name',
                'Полное наименование': 'Full_name', 'Brand': 'Brand', 'Family': 'Family',
                'Product name': 'Product_name', 'Type': 'Product_type', 'Единица': 'UoM',
                'Единица измерения отчетов': 'Report_UoM', 'Вид упаковки': 'Package_type',
                'Количество в упаковке': 'Items_per_Package', 'Шт в комплекте': 'Items_per_Set',
                'Упаковка(Литраж)': 'Package_Volume', 'Нетто': 'Net_weight', 'Брутто': 'Gross_weight',
                'Плотность': 'Density', 'ТН ВЭД': 'TNVED', 'Акциз': 'Excise'
            }
            
            df = df.rename(columns=column_map)
            df['Items_per_Set'] = pd.to_numeric(df['Items_per_Set'], errors='coerce').fillna(0).astype(int)
            
            numeric_cols = ['Items_per_Package', 'Package_Volume', 'Net_weight', 'Gross_weight', 'Density']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            
            return df[df['Code'].notna()].replace({pd.NA: None}).to_dict('records')
            
        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла: {str(e)}")
            return []

    def save_Material(self, data):
        """Сохранение данных"""
        if not data:
            return

        existing_codes = {code[0] for code in db.session.query(Material.Code).all()}
        to_insert = []
        to_update = []
        
        for row in data:
            material = {
                'Code': row['Code'],
                'Article': row.get('Article'),
                'Material_Name': row['Material_Name'],
                'Full_name': row.get('Full_name'),
                'Brand': row.get('Brand'),
                'Family': row.get('Family'),
                'Product_name': row.get('Product_name'),
                'Product_type': row.get('Product_type'),
                'UoM': row.get('UoM'),
                'Report_UoM': row.get('Report_UoM'),
                'Package_type': row.get('Package_type'),
                'Items_per_Package': row.get('Items_per_Package'),
                'Items_per_Set': row.get('Items_per_Set'),
                'Package_Volume': row.get('Package_Volume'),
                'Net_weight': row.get('Net_weight'),
                'Gross_weight': row.get('Gross_weight'),
                'Density': row.get('Density'),
                'TNVED': row.get('TNVED'),
                'Excise': row.get('Excise')
            }
            
            if row['Code'] in existing_codes:
                to_update.append(material)
            else:
                to_insert.append(material)
        
        try:
            if to_insert:
                db.session.bulk_insert_mappings(Material, to_insert)
            if to_update:
                db.session.bulk_update_mappings(Material, to_update)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            self.show_error_message(f"Ошибка сохранения данных: {str(e)}")

    @lru_cache(maxsize=32)
    def _get_unique_values(self, column, filter_column=None, filter_value=None):
        """Получение уникальных значений с фильтрацией"""
        query = db.session.query(column)
        if filter_column is not None and filter_value not in (None, '-', ''):
            query = query.filter(filter_column == filter_value)
        return sorted(v[0] for v in query.distinct().all() if v[0])

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self.fill_in_prod_brand_list()
        self.fill_in_prod_fam_list()
        self.fill_in_prod_name_list()

    def fill_in_prod_brand_list(self):
        """Заполнение списка брендов"""
        brands = self._get_unique_values(Material.Brand)
        self._fill_combobox(self.ui.line_Brand, brands)

    def fill_in_prod_fam_list(self):
        """Заполнение списка семейств"""
        brand = self.ui.line_Brand.currentText()
        families = self._get_unique_values(
            Material.Family, 
            Material.Brand if brand != '-' else None, 
            brand
        )
        self._fill_combobox(self.ui.line_Prod_Fam, families)

    def fill_in_prod_name_list(self):
        """Заполнение списка продуктов"""
        family = self.ui.line_Prod_Fam.currentText()
        products = self._get_unique_values(
            Material.Product_name,
            Material.Family if family != '-' else None,
            family
        )
        self._fill_combobox(self.ui.line_Prod_name, products)

    def _fill_combobox(self, combobox, values):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if values:
            combobox.addItems(values)

    def get_all_Products_from_db(self, columns=None):
        """Получение всех продуктов из базы"""
        if columns:
            query = db.session.query(*[getattr(Material, col) for col in columns])
        else:
            query = db.session.query(Material)
        
        df = pd.read_sql(query.statement, db.session.bind)
        return df.where(pd.notnull(df), None)

    def find_Product(self):
        """Поиск продуктов"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        code = self.ui.line_ID.text().strip()
        article = self.ui.line_Artical.text().strip()
        product_name = self.ui.line_Prod_name.currentText()
        product_family = self.ui.line_Prod_Fam.currentText()
        brand = self.ui.line_Brand.currentText()

        query = db.session.query(Material)
        
        if code:
            query = query.filter(Material.Code == code)
        elif article:
            query = query.filter(Material.Article == article)
        elif brand != '-':
            query = query.filter(Material.Brand == brand)
            if product_family != '-':
                query = query.filter(Material.Family == product_family)
                if product_name != '-':
                    query = query.filter(Material.Product_name == product_name)
        elif product_family != '-':
            query = query.filter(Material.Family == product_family)
            if product_name != '-':
                query = query.filter(Material.Product_name == product_name)
        elif product_name != '-':
            query = query.filter(Material.Product_name == product_name)

        df = pd.read_sql(query.statement, db.session.bind).replace({pd.NA: None})
        
        if df.empty:
            self.show_error_message('Ничего не найдено')
            return

        self._display_data(df)

    def _display_data(self, df):
        """Отображение данных в таблице"""
        headers = df.columns.tolist()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def show_message(self, text):
        """Показать информационное сообщение"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setStyleSheet("""
            background-color: #f8f8f2;
            font: 10pt "Tahoma";
            color: #237508;
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setStyleSheet("""
            background-color: #f8f8f2;
            font: 10pt "Tahoma";
            color: #ff0000;
        """)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def dowload_Products(self):
        """Скачивание продуктов"""
        file_path, _ = QFileDialog.getSaveFileName(
            None, 'Сохранение', 'Products.xlsx', 'Excel Workbook (*.xlsx)')
        
        if not file_path:
            return

        data = []
        for row in range(self.table.rowCount()):
            data.append([
                self.table.item(row, col).text() if self.table.item(row, col) else ''
                for col in range(self.table.columnCount())
            ])

        headers = [self.table.horizontalHeaderItem(col).text() 
                  for col in range(self.table.columnCount())]
        
        pd.DataFrame(data, columns=headers).to_excel(file_path, index=False)
        self.show_message('Отчет сохранен')