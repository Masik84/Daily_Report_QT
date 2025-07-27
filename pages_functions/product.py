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
from models import ABC_cat, TNVED, Product_Group, Product_Names, Materials, ABC_list
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
        """Загрузка данных продуктов в базу данных"""
        try:
            # Закрываем предыдущие сессии, если они есть
            if db.is_active:
                db.close()

            # Определяем путь к файлу
            file_path = self.ui.label_Prod_File.text()
            if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
                file_path = Material_file

            try:
                # Основные операции выполняем в отдельной сессии
                db.begin()
                
                try:
                    # Чтение и обработка данных
                    data = self.read_product_file(file_path)
                    
                    # Сохранение данных (каждый метод сам управляет своими транзакциями)
                    self.save_TNVED(data)
                    self.save_Product_Group(data)
                    self.save_Product_Names(data)
                    self.save_Materials(data)
                    
                    # Финализируем транзакцию
                    db.commit()
                    
                    # Обновляем интерфейс
                    self.refresh_all_comboboxes()
                    self.show_message('Данные продуктов успешно загружены!')
                    
                except Exception as e:
                    db.rollback()
                    raise
                    
            except SQLAlchemyError as e:
                raise Exception(f"Ошибка базы данных: {str(e)}")
                
        except FileNotFoundError as e:
            self.show_error_message(str(e))
        except ValueError as e:
            self.show_error_message(f"Ошибка в данных: {str(e)}")
        except Exception as e:
            self.show_error_message(f"Ошибка загрузки: {str(e)}")
        finally:
            # Всегда закрываем сессию
            if db.is_active:
                db.close()

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
        self.save_TNVED(data)
        self.save_Product_Group(data)
        self.save_Product_Names(data)
        self.save_Materials(data)

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

    def save_TNVED(self, data):
        """Сохранение данных TNVED"""
        if not data:
            return

        # Получаем уникальные коды ТН ВЭД из данных
        tnved_codes = {row['TNVED'] for row in data if row.get('TNVED')}
        
        # Получаем существующие коды из БД
        existing_tnved = {t.code for t in db.query(TNVED.code).all()}
        
        # Находим новые коды для добавления
        new_tnved_codes = tnved_codes - existing_tnved
        
        if new_tnved_codes:
            try:
                # Подготавливаем данные для вставки
                to_insert = [{'code': code} for code in new_tnved_codes]
                db.bulk_insert_mappings(TNVED, to_insert)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                raise Exception(f"Ошибка сохранения TNVED: {str(e)}")
            finally:
                db.close()

    def save_Product_Group(self, data):
        """Сохранение данных Product_Group"""
        if not data:
            return

        # Собираем уникальные группы продуктов
        product_groups = {}
        for row in data:
            if row.get('Код_группы') and row.get('Product_name') and row.get('TNVED'):
                # Находим ID TNVED для этой группы
                tnved_id = db.query(TNVED.id).filter(TNVED.code == row['TNVED']).scalar()
                if tnved_id:
                    product_groups[row['Код_группы']] = {
                        'Product_name': row['Product_name'],
                        'TNVED_id': tnved_id
                    }

        # Получаем существующие группы из БД
        existing_groups = {g.id for g in db.query(Product_Group.id).all()}
        
        # Разделяем на новые и существующие группы
        to_insert = []
        to_update = []
        
        for group_id, group_data in product_groups.items():
            if group_id in existing_groups:
                to_update.append({
                    'id': group_id,
                    **group_data
                })
            else:
                to_insert.append({
                    'id': group_id,
                    **group_data
                })
        
        try:
            if to_insert:
                db.bulk_insert_mappings(Product_Group, to_insert)
            if to_update:
                db.bulk_update_mappings(Product_Group, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения Product_Group: {str(e)}")
        finally:
                db.close()

    def save_Product_Names(self, data):
        """Сохранение данных Product_Names"""
        if not data:
            return

        # Собираем уникальные наименования продуктов
        product_names = {}
        for row in data:
            if row.get('Material_Name') and row.get('Код_группы'):
                product_names[row['Material_Name']] = row['Код_группы']

        # Получаем существующие наименования из БД
        existing_names = {n.Product_name: n for n in db.query(Product_Names).all()}
        
        # Разделяем на новые и существующие наименования
        to_insert = []
        to_update = []
        
        for name, group_id in product_names.items():
            if name in existing_names:
                # Обновляем только если изменилась группа
                if existing_names[name].Product_Group_id != group_id:
                    to_update.append({
                        'id': existing_names[name].id,
                        'Product_Group_id': group_id
                    })
            else:
                to_insert.append({
                    'Name': name,
                    'Product_Group_id': group_id
                })
        
        try:
            if to_insert:
                db.bulk_insert_mappings(Product_Names, to_insert)
            if to_update:
                db.bulk_update_mappings(Product_Names, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения Product_Names: {str(e)}")
        finally:
                db.close()

    def save_Materials(self, data):
        """Сохранение данных Materials (адаптированная версия)"""
        if not data:
            return

        # Получаем существующие материалы из БД (теперь таблица 'material')
        existing_materials = {m.Code: m for m in db.query(Materials).all()}  # Обратите внимание: класс Materials, а таблица 'material'
        
        # Получаем mapping наименований продуктов к их ID (таблица 'product_names')
        name_to_id = {n.Name: n.id for n in db.query(Product_Names).all()}
        
        to_insert = []
        to_update = []
        
        for row in data:
            if not row.get('Code') or not row.get('Material_Name'):
                continue
                
            product_name_id = name_to_id.get(row['Material_Name'])
            if not product_name_id:
                continue
                
            material_data = {
                'Code': row['Code'],
                'Article': row.get('Article'),
                'Full_name': row.get('Full_name'),
                'Brand': row.get('Brand'),
                'Family': row.get('Family'),
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
                'Excise': row.get('Excise'),
                'Product_Names_id': product_name_id
            }
            
            if row['Code'] in existing_materials:
                to_update.append(material_data)
            else:
                to_insert.append(material_data)
        
        try:
            if to_insert:
                db.bulk_insert_mappings(Materials, to_insert)  # Класс Models.Materials, но таблица в БД 'material'
            if to_update:
                db.bulk_update_mappings(Materials, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения Materials: {str(e)}")
        finally:
            db.close()
    
    def save_ABC_list(self):
        """Инициализация списка ABC категорий (A, B, C, D)"""
        try:
            # Стандартные категории ABC
            abc_categories = [
                {'ABC_category': 'A', 'description': 'Высокоприоритетные товары'},
                {'ABC_category': 'B', 'description': 'Товары среднего приоритета'},
                {'ABC_category': 'C', 'description': 'Низкоприоритетные товары'},
                {'ABC_category': 'D', 'description': 'Товары под списание'}
            ]
            
            # Получаем существующие категории
            existing_categories = {c.ABC_category for c in db.query(ABC_list).all()}
            
            # Добавляем только новые категории
            to_insert = [
                ABC_list(**category) 
                for category in abc_categories 
                if category['ABC_category'] not in existing_categories
            ]
            
            if to_insert:
                db.add_all(to_insert)
                db.commit()
                self.show_message('Список ABC категорий успешно инициализирован')
            else:
                self.show_message('Все ABC категории уже существуют')
                
        except Exception as e:
            db.rollback()
            self.show_error_message(f'Ошибка инициализации ABC категорий: {str(e)}')
        finally:
            db.close()

    def update_ABC_cat(self):
        try:
            # Закрываем все предыдущие сессии, если они есть
            if db.is_active:
                db.close()

            file_path = All_data_file
            
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")

            # Читаем Excel файл с использованием контекстного менеджера
            with pd.ExcelFile(file_path) as excel:
                df = pd.read_excel(excel, sheet_name="ABC")

            # Проверка обязательных столбцов
            required_columns = ['Продукт + упаковка', 'Дата изм', 'Дата оконч', 'Категория ABCD']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит всех необходимых столбцов")

            # Переименование колонок
            df = df.rename(columns={
                'Продукт + упаковка': 'product_name',
                'Дата изм': 'Start_date',
                'Дата оконч': 'End_date',
                'Категория ABCD': 'ABC_category'
            })

            # Обработка дат
            df['Start_date'] = pd.to_datetime(df['Start_date'], dayfirst=True, errors='coerce').dt.date
            df['End_date'] = pd.to_datetime(df['End_date'], dayfirst=True, errors='coerce').dt.date

            # Фильтрация данных
            df = df[(df['ABC_category'] != '-') & 
                    (df['product_name'].notna()) & 
                    (df['Start_date'].notna()) & 
                    (df['End_date'].notna())]

            # Получаем соответствия названий продуктов и ABC категорий
            try:
                product_mapping = {n.Product_name: n.id for n in db.query(Product_Names).all()}
                abc_mapping = {c.ABC_category: c.id for c in db.query(ABC_list).all()}
            finally:
                if db.is_active:
                    db.close()

            to_insert = []
            to_update = []

            # Обрабатываем каждую строку DataFrame
            for _, row in df.iterrows():
                product_name = row['product_name']
                abc_category = row['ABC_category']

                # Пропускаем если нет соответствий
                if product_name not in product_mapping or abc_category not in abc_mapping:
                    continue

                product_id = product_mapping[product_name]
                abc_id = abc_mapping[abc_category]

                # Проверяем существующие записи для этого продукта
                try:
                    existing_records = db.query(ABC_cat).filter(
                        ABC_cat.product_name_id == product_id
                    ).all()

                    # Проверяем точное совпадение
                    exact_match = any(
                        record.abc_list_id == abc_id and
                        record.Start_date == row['Start_date'] and
                        record.End_date == row['End_date']
                        for record in existing_records
                    )

                    if exact_match:
                        continue  # Запись уже существует

                    # Проверяем пересечение периодов
                    for record in existing_records:
                        if (record.abc_list_id != abc_id and
                            row['Start_date'] <= record.End_date and
                            row['End_date'] >= record.Start_date):
                            
                            # Обновляем существующую запись
                            to_update.append({
                                'id': record.id,
                                'abc_list_id': abc_id,
                                'Start_date': row['Start_date'],
                                'End_date': row['End_date']
                            })
                            break
                    else:
                        # Добавляем новую запись
                        to_insert.append({
                            'product_name_id': product_id,
                            'abc_list_id': abc_id,
                            'Start_date': row['Start_date'],
                            'End_date': row['End_date']
                        })

                finally:
                    if db.is_active:
                        db.close()

            # Выполняем финальные операции с БД
            try:
                with db.begin():
                    if to_insert:
                        db.bulk_insert_mappings(ABC_cat, to_insert)
                    if to_update:
                        db.bulk_update_mappings(ABC_cat, to_update)

                # Формируем информационное сообщение
                message_parts = []
                if to_insert:
                    message_parts.append(f"Добавлено новых: {len(to_insert)}")
                if to_update:
                    message_parts.append(f"Обновлено: {len(to_update)}")
                
                if message_parts:
                    self.show_message("ABC категории обновлены. " + ", ".join(message_parts))
                else:
                    self.show_message("Нет изменений для обновления")

            except Exception as e:
                db.rollback()
                raise
            finally:
                if db.is_active:
                    db.close()

        except Exception as e:
            self.show_error_message(f'Ошибка обновления ABC категорий: {str(e)}')
        
    @lru_cache(maxsize=32)
    def _get_unique_values(self, column, filter_column=None, filter_value=None):
        """Получение уникальных значений с фильтрацией"""
        try:
            # Специальная обработка для product_name
            if column == "product_name":  # Changed from Materials.product_name
                query = db.query(Product_Names.Product_name).join(Materials, Materials.Product_Names_id == Product_Names.id)
            else:
                query = db.query(column)
            
            # Применяем фильтр если он задан
            if filter_column is not None and filter_value not in (None, '-', ''):
                if filter_column == "product_name":
                    query = query.join(Product_Names, Materials.Product_Names_id == Product_Names.id)
                    query = query.filter(Product_Names.Product_name == filter_value)
                else:
                    query = query.filter(filter_column == filter_value)
            
            # Получаем и сортируем уникальные значения
            result = sorted(v[0] for v in query.distinct().all() if v[0])
            return result
            
        except Exception as e:
            self.show_error_message(f"Ошибка при получении уникальных значений: {str(e)}")
            return []
        finally:
            db.close()

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self.fill_in_prod_brand_list()
        self.fill_in_prod_fam_list()
        self.fill_in_prod_name_list()

    def fill_in_prod_brand_list(self):
        """Заполнение списка брендов"""
        brands = self._get_unique_values(Materials.Brand)
        self._fill_combobox(self.ui.line_Brand, brands)

    def fill_in_prod_fam_list(self):
        """Заполнение списка семейств"""
        brand = self.ui.line_Brand.currentText()
        families = self._get_unique_values(
            Materials.Family,  # Используем прямое обращение к колонке
            Materials.Brand if brand != '-' else None,
            brand
        )
        self._fill_combobox(self.ui.line_Prod_Fam, families)

    def fill_in_prod_name_list(self):
        """Заполнение списка продуктов"""
        family = self.ui.line_Prod_Fam.currentText()
        products = self._get_unique_values(
            "product_name",  # Используем строковый идентификатор
            Materials.Family if family != '-' else None,
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
        
        # Подзапрос для ABC-категорий (теперь через связь с ABC_list)
        subq = (
            db.query(
                ABC_cat.product_name_id,
                ABC_list.ABC_category.label('ABC_category'),  # Берем категорию из ABC_list
                func.max(ABC_cat.Start_date).label('max_date')
            )
            .join(ABC_list, ABC_cat.abc_list_id == ABC_list.id)  # Добавляем join к ABC_list
            .filter(ABC_cat.End_date >= today)
            .group_by(ABC_cat.product_name_id, ABC_list.ABC_category)  # Группируем по категории
            .subquery()
        )
        
        # Основной запрос
        query = (
            db.query(
                Materials.Code,
                Materials.Article,
                Materials.Material_Name,
                Materials.Full_name,
                Materials.Brand,
                Materials.Family,
                Materials.Product_name,
                Materials.Product_type,
                Materials.UoM,
                Materials.Report_UoM,
                Materials.Package_type,
                Materials.Items_per_Package,
                Materials.Items_per_Set,
                Materials.Package_Volume,
                Materials.Net_weight,
                Materials.Gross_weight,
                Materials.Density,
                Materials.TNVED,
                Materials.Excise,
                subq.c.ABC_category.label('ABC_category')  # Используем категорию из подзапроса
            )
            .join(Product_Names, Materials.Product_Names_id == Product_Names.id)
            .outerjoin(
                subq, 
                Product_Names.id == subq.c.product_name_id
            )
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
        
        
