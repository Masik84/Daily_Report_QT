import os
import pandas as pd
from sqlalchemy import func
import datetime
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, 
                              QTableWidgetItem, QWidget, QApplication, QPushButton)
from PySide6.QtCore import Qt
from functools import lru_cache

from wind.pages.products_ui import Ui_Form
from config import Material_file, All_data_file
from models import Material, ABC_cat
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
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.line_Brand.currentTextChanged.connect(self.fill_in_prod_fam_list)
        self.ui.line_Prod_Fam.currentTextChanged.connect(self.fill_in_prod_name_list)
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_Product)
        self.ui.btn_upd_ABCD.clicked.connect(self.update_ABC_cat)
        

    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с данными продуктов')
        if file_path:
            self.ui.label_Prod_File.setText(file_path)

    def upload_data(self):
        """Загрузка данных в базу"""
        file_path = self.ui.label_Prod_File.text()
        if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
            file_path = Material_file
        
        try:
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")

            try:
                self.run_product_func(file_path)
                db.commit()
                self.show_message('Данные продуктов загружены!')
                self.refresh_all_comboboxes()
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()

        except Exception as e:
            self._handle_upload_error(e)

    def _handle_upload_error(self, error):
        """Обработка ошибок загрузки"""
        if "transaction is already begun" in str(error):
            msg = "Ошибка БД. Закройте программу и попробуйте снова."
        elif "required columns" in str(error).lower():
            msg = "Файл не содержит всех необходимых столбцов."
        else:
            msg = f"Ошибка загрузки данных продуктов: {str(error)}"
        self.show_error_message(msg)

    def run_product_func(self, data_file_xls):
        """Основная функция обработки данных"""
        data = self.read_product_file(data_file_xls)
        self.save_Material(data)

    def read_product_file(self, file_path):
        """Чтение данных из Excel с фильтрацией и обработкой значений"""
        try:
            dtype_prod = {"Артикул": str, "ТН ВЭД": str}
            df = pd.read_excel(file_path, sheet_name=0, dtype=dtype_prod)
            
            required_columns = ['Код', 'Product name', 'Шт в комплекте', 'Единица измерения отчетов']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит необходимых столбцов")
            
            # 1. Фильтрация по "Вид номенклатуры"
            if 'Вид номенклатуры' in df.columns:
                valid_types = ['Товары', 'Услуги', 'Нефтепродукты', 'Продукция']
                df = df[df['Вид номенклатуры'].isin(valid_types)]
            
            # 2. Фильтрация по "Номенклатурная группа"
            if 'Номенклатурная группа' in df.columns:
                valid_groups = ['Доставка (курьерская)', 'ГСМ', 'ЗАПАСНЫЕ ЧАСТИ']
                df = df[df['Номенклатурная группа'].isin(valid_groups)]
            
            # 3. Переименование колонок
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
            
            # 4. Обработка числовых и текстовых значений
            numeric_cols = ['Items_per_Package', 'Items_per_Set', 'Package_Volume', 
                        'Net_weight', 'Gross_weight', 'Density']
            text_cols = ['Article', 'Material_Name', 'Full_name', 'Brand', 'Family',
                    'Product_name', 'Product_type', 'UoM', 'Report_UoM', 
                    'Package_type', 'TNVED', 'Excise']
            
            # Замена пустот в числовых колонках на 0
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Замена пустот в текстовых колонках на "-"
            for col in text_cols:
                if col in df.columns:
                    df[col] = df[col].fillna('-')
            
            return df[df['Code'].notna()].replace({pd.NA: None}).to_dict('records')
            
        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла продуктов: {str(e)}")
            return []

    def save_Material(self, data):
        """Сохранение данных"""
        if not data:
            return

        existing_materials = {m.Code: m for m in db.query(Material).all()}
        to_insert = []
        to_update = []
        
        for row in data:
            material_data = {
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
            
            if row['Code'] in existing_materials:
                to_update.append(material_data)
            else:
                to_insert.append(material_data)
        
        try:
            if to_insert:
                db.bulk_insert_mappings(Material, to_insert)
            if to_update:
                db.bulk_update_mappings(Material, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения продуктов: {str(e)}")
        finally:
            db.close()

    def update_ABC_cat(self):
        """Обновление категорий ABCD из файла All_data_file (лист 'ABC')"""
        try:
            # Используем стандартный файл из конфига, как в Product
            file_path = All_data_file
            
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")

            df = pd.read_excel(file_path, sheet_name="ABC")

            required_columns = [
                'Продукт + упаковка', 
                'Дата изм', 
                'Дата оконч', 
                'Категория ABCD'
            ]
            if not all(col in df.columns for col in required_columns):
                raise ValueError(
                    "Файл не содержит всех необходимых столбцов. "
                    "Требуемые колонки: " + ", ".join(required_columns)
                )
            
            # Переименование колонок для соответствия модели
            df = df.rename(columns={
                'Продукт + упаковка': 'Material_Name',
                'Дата изм': 'Start_date',
                'Дата оконч': 'End_date',
                'Категория ABCD': 'ABC_category'
            })
            
            # Преобразование дат
            df['Start_date'] = pd.to_datetime(df['Start_date'], dayfirst=True).dt.date
            df['End_date'] = pd.to_datetime(df['End_date'], dayfirst=True).dt.date
            
            # Получаем текущие материалы из базы
            materials = {m.Material_Name: m.Code for m in db.query(Material).all()}
            
            # Подготовка данных для вставки
            to_insert = []
            today = datetime.date.today()
            
            for _, row in df.iterrows():
                material_name = row['Material_Name']
                if material_name not in materials:
                    continue  # Пропускаем если материал не найден
                    
                # Проверяем есть ли уже такая запись (уникальность по материалу и датам)
                exists = db.query(ABC_cat).filter(
                    ABC_cat.material_code == materials[material_name],
                    ABC_cat.Start_date == row['Start_date'],
                    ABC_cat.End_date == row['End_date']
                ).first()
                
                if not exists and row['ABC_category'] != '-':
                    to_insert.append({
                        'material_code': materials[material_name],
                        'Start_date': row['Start_date'],
                        'End_date': row['End_date'],
                        'ABC_category': row['ABC_category']
                    })
            
            # Массовая вставка новых записей
            if to_insert:
                db.bulk_insert_mappings(ABC_cat, to_insert)
                db.commit()
                self.show_message(f'Успешно добавлено {len(to_insert)} записей ABC категорий!')
            else:
                self.show_message('Нет новых данных для добавления')
                
        except Exception as e:
            db.rollback()
            self.show_error_message(f'Ошибка обновления ABC категорий: {str(e)}')
        finally:
            db.close()

    @lru_cache(maxsize=32)
    def _get_unique_values(self, column, filter_column=None, filter_value=None):
        """Получение уникальных значений с фильтрацией"""
        query = db.query(column)
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

    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if items:
            combobox.addItems(sorted(items))

    def get_Products_from_db(self):

        today = datetime.date.today()
        
        # Создаем подзапрос для получения последней действующей ABC категории
        subq = db.query(
            ABC_cat.material_code,
            ABC_cat.ABC_category,
            func.max(ABC_cat.Start_date).label('max_date')
        ).filter(
            ABC_cat.End_date >= today
        ).group_by(
            ABC_cat.material_code,
            ABC_cat.ABC_category
        ).subquery()
        
        query = db.query(
            Material.Code,
            Material.Article,
            Material.Material_Name,
            Material.Full_name,
            Material.Brand,
            Material.Family,
            Material.Product_name,
            Material.Product_type,
            Material.UoM,
            Material.Report_UoM,
            Material.Package_type,
            Material.Items_per_Package,
            Material.Items_per_Set,
            Material.Package_Volume,
            Material.Net_weight,
            Material.Gross_weight,
            Material.Density,
            Material.TNVED,
            Material.Excise,
            subq.c.ABC_category.label('ABC_category')
        ).outerjoin(
            subq, Material.Code == subq.c.material_code
        )
        
        df = pd.read_sql(query.statement, db.bind)
        return df.where(pd.notnull(df), None)

    def find_Product(self):
        """Поиск продуктов"""
        self.table.clearContents()
        self.table.setRowCount(0)

        prod_df = self.get_Products_from_db()
        if prod_df.empty:
            self.show_error_message('Нет данных о продуктах')
            return

        code = self.ui.line_ID.text().strip()
        article = self.ui.line_Artical.text().strip()
        product_name = self.ui.line_Prod_name.currentText()
        product_family = self.ui.line_Prod_Fam.currentText()
        brand = self.ui.line_Brand.currentText()

        if code:
            prod_df = prod_df[prod_df['Code'] == code]
        elif article:
            prod_df = prod_df[prod_df['Article'] == article]
        elif brand != '-':
            prod_df = prod_df[prod_df['Brand'] == brand]
            if product_family != '-':
                prod_df = prod_df[prod_df['Family'] == product_family]
                if product_name != '-':
                    prod_df = prod_df[prod_df['Product_name'] == product_name]
        elif product_family != '-':
            prod_df = prod_df[prod_df['Family'] == product_family]
            if product_name != '-':
                prod_df = prod_df[prod_df['Product_name'] == product_name]
        elif product_name != '-':
            prod_df = prod_df[prod_df['Product_name'] == product_name]

        self._display_data(prod_df.sort_values('Material_Name'))

    def _display_data(self, df):
        """Отображение данных в таблице"""
        self.table.clear()
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())
        self.table.setRowCount(len(df))

        if df.empty:
            self.show_error_message('Ничего не найдено')
            return

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

    def download_Products(self):
        """Скачивание продуктов"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Сохранение', 'Products.xlsx', 'Excel Workbook (*.xlsx)')
        
        if not file_path:
            return

        data = []
        headers = []
        
        for col in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(col).text())
        
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else '')
            data.append(row_data)

        pd.DataFrame(data, columns=headers).to_excel(file_path, index=False)
        self.show_message('Отчет сохранен')

    def show_message(self, text):
        """Показать информационное сообщение с кнопкой копирования"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f8f8f2;
                font: 10pt "Tahoma";
            }
            QMessageBox QLabel {
                color: #237508;
            }
        """)
        msg.setIcon(QMessageBox.Information)

        clipboard = QApplication.clipboard()
        copy_button = msg.addButton("Copy msg", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        copy_button.clicked.connect(lambda: None)

        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке с кнопкой копирования"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f8f8f2;
                font: 10pt "Tahoma";
            }
            QMessageBox QLabel {
                color: #ff0000;
            }
        """)
        msg.setIcon(QMessageBox.Critical)

        clipboard = QApplication.clipboard()
        copy_button = msg.addButton("Copy msg", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        copy_button.clicked.connect(lambda: None)

        msg.exec_()
        
        
