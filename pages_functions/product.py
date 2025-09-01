import os, re
import pandas as pd
from sqlalchemy import func
import datetime
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QMenu, 
                              QTableWidgetItem, QWidget, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator, QIntValidator
from functools import lru_cache
import traceback

from wind.pages.products_ui import Ui_Form
from config import Material_file, All_data_file
from models import ABC_cat, TNVED, Product_Group, Product_Names, Materials, ABC_list
from db import db


class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self._updating_table = False
        self._original_values = {}  # Для хранения оригинальных значений
        self._pending_changes = {}  # Для отслеживания незакоммиченных изменений

        self._setup_ui()
        self._setup_connections()
        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса таблицы с поддержкой редактирования"""
        self.table = self.ui.table
        
        # Базовые настройки таблицы
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # Выделение отдельных ячеек
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)  # Разрешить редактирование
        self.table.setAlternatingRowColors(True)  # Чередование цветов строк
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Изменяемые размеры
        self.table.horizontalHeader().setStretchLastSection(True)  # Растягивание последнего столбца
        self.table.verticalHeader().setVisible(False)  # Скрытие вертикальных заголовков
        self.table.setSortingEnabled(True)  # Сортировка по клику на заголовок
        self.table.setWordWrap(False)  # Запрет переноса слов
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)  # Обрезка длинного текста
        
        # Настройка контекстного меню для копирования и редактирования
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Стилизация таблицы с подсветкой редактируемых ячеек
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                selection-background-color: #3daee9;
                selection-color: black;
            }
            QTableWidget::item {
                padding: 3px;
            }
            QTableWidget::item:editable {
                background-color: #ffffd0;
                border: #ffcc00;
            }
            QTableWidget::item:focus {
                background-color: #ffffa0;
                border: 2px solid #ff9900;
            }
        """)
        
        # Флаг для отслеживания обновления таблицы (чтобы избежать рекурсии)
        self._updating_table = False
        
        # Настройка поведения при редактировании
        self.table.setTabKeyNavigation(True)
        self.table.setCornerButtonEnabled(False)

    def show_context_menu(self, position):
        """Показ контекстного меню"""
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        apply_action = menu.addAction("Применить изменения")
        revert_action = menu.addAction("Отменить изменения")
        
        copy_action.triggered.connect(self.copy_cell_content)
        apply_action.triggered.connect(self.apply_pending_changes)
        revert_action.triggered.connect(self.revert_changes)
        
        menu.exec_(self.table.viewport().mapToGlobal(position))
    
    def _setup_connections(self):
            """Настройка сигналов и слотов"""
            self.table.itemChanged.connect(self.on_item_changed)
            self.ui.line_Brand.currentTextChanged.connect(self.fill_in_prod_fam_list)
            self.ui.line_Prod_Fam.currentTextChanged.connect(self.fill_in_prod_name_list)
            self.ui.btn_open_file.clicked.connect(self.get_file)
            self.ui.btn_upload_file.clicked.connect(self.upload_data)
            self.ui.btn_find.clicked.connect(self.find_Product)

    def on_item_changed(self, item):
        """Обработчик изменения данных в таблице"""
        if not hasattr(self, '_updating_table') or self._updating_table:
            return
        
        try:
            row = item.row()
            column = item.column()
            header = self.table.horizontalHeaderItem(column).text()
            code_item = self.table.item(row, 0)
            
            if not code_item:
                return
                
            material_code = code_item.text()
            new_value = item.text()
            
            # Сохраняем изменение в pending_changes
            if material_code not in self._pending_changes:
                self._pending_changes[material_code] = {}
            
            self._pending_changes[material_code][header] = new_value
            
            # Автоматически применяем изменения (можно убрать, если хотите ручное сохранение)
            self.apply_pending_changes()
                
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")
            self.revert_changes()  # Откатываем при ошибке
    
    def revert_changes(self):
        """Отмена изменений и обновление таблицы"""
        db.rollback()
        self.find_Product()
        self.show_message("Изменения отменены")

    def copy_cell_content(self):
        """Копирование содержимого выделенных ячеек"""
        selected_items = self.table.selectedItems()
        if selected_items:
            clipboard = QApplication.clipboard()
            # Если выделена одна ячейка - копируем только ее
            if len(selected_items) == 1:
                text = selected_items[0].text()
            else:
                # Если выделено несколько ячеек - копируем с разделением табуляцией и переносом строк
                rows = {}
                for item in selected_items:
                    row = item.row()
                    col = item.column()
                    if row not in rows:
                        rows[row] = {}
                    rows[row][col] = item.text()
                
                # Сортируем ячейки по строкам и столбцам
                sorted_rows = sorted(rows.items())
                text = ""
                for row, cols in sorted_rows:
                    sorted_cols = sorted(cols.items())
                    text += "\t".join([text for col, text in sorted_cols]) + "\n"
            
            clipboard.setText(text.strip())

    def apply_pending_changes(self):
        """Применение всех ожидающих изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для применения")
            return
            
        try:
            applied_changes = 0
            
            # Создаем копию для безопасной итерации
            pending_changes_copy = self._pending_changes.copy()
            changes_to_remove = []
            
            for material_code, changes in pending_changes_copy.items():
                for header, new_value in changes.items():
                    # Маппинг колонок таблицы на поля БД
                    column_mapping = {
                        'Article': ('Materials', 'Article'),
                        'Full_name': ('Materials', 'Full_name'),
                        'Brand': ('Materials', 'Brand'),
                        'Family': ('Materials', 'Family'),
                        'Product_type': ('Materials', 'Product_type'),
                        'UoM': ('Materials', 'UoM'),
                        'Report_UoM': ('Materials', 'Report_UoM'),
                        'Package_type': ('Materials', 'Package_type'),
                        'Items_per_Package': ('Materials', 'Items_per_Package'),
                        'Items_per_Set': ('Materials', 'Items_per_Set'),
                        'Package_Volume': ('Materials', 'Package_Volume'),
                        'Net_weight': ('Materials', 'Net_weight'),
                        'Gross_weight': ('Materials', 'Gross_weight'),
                        'Density': ('Materials', 'Density'),
                        'Excise': ('Materials', 'Excise'),
                        'Status': ('Materials', 'Status'),
                        'TNVED': ('TNVED', 'code'),
                        'Material_Name': ('Product_Names', 'Product_name')
                    }
                    
                    if header in column_mapping:
                        table_name, field_name = column_mapping[header]
                        
                        # Для числовых полей преобразуем значение
                        numeric_fields = ['Items_per_Package', 'Items_per_Set', 'Package_Volume', 
                                        'Net_weight', 'Gross_weight', 'Density']
                        
                        if field_name in numeric_fields:
                            try:
                                new_value = float(new_value) if new_value else 0.0
                            except ValueError:
                                raise Exception(f"Неверное числовое значение в колонке {header}: {new_value}")
                        
                        # Обработка разных таблиц
                        success = False
                        if table_name == 'Materials':
                            success = self.update_material_field(material_code, field_name, new_value)
                        elif table_name == 'Product_Names':
                            success = self.update_product_name(material_code, new_value)
                        elif table_name == 'TNVED':
                            success = self.update_tnved_for_material(material_code, new_value)
                        
                        if success:
                            applied_changes += 1
                            # Запоминаем изменения для удаления
                            changes_to_remove.append((material_code, header))
            
            # Коммитим все изменения одним разом
            try:
                db.commit()
                
                # Удаляем примененные изменения из pending_changes
                for material_code, header in changes_to_remove:
                    if material_code in self._pending_changes and header in self._pending_changes[material_code]:
                        del self._pending_changes[material_code][header]
                        # Если для этого материала больше нет изменений, удаляем запись
                        if not self._pending_changes[material_code]:
                            del self._pending_changes[material_code]
                
                # Обновляем оригинальные значения из базы
                self._update_original_values()
                
                if applied_changes > 0:
                    self.show_message(f"Успешно применено {applied_changes} изменений")
                    # Обновляем таблицу для отображения актуальных данных
                    self.find_Product()
                else:
                    self.show_message("Нет изменений для применения")
                    
            except SQLAlchemyError as e:
                db.rollback()
                raise Exception(f"Ошибка сохранения в базу данных: {str(e)}")
            
        except Exception as e:
            # Откатываем все изменения при ошибке
            try:
                db.rollback()
            except:
                pass
                
            self.show_error_message(f"Ошибка применения изменений: {str(e)}")
            
            # Восстанавливаем таблицу из оригинальных значений
            self._reload_data_from_database()

    def _mark_change_applied(self, material_code, header):
        """Помечает изменение как примененное (удаляет из pending_changes)"""
        if material_code in self._pending_changes and header in self._pending_changes[material_code]:
            del self._pending_changes[material_code][header]
            # Если для этого материала больше нет изменений, удаляем запись
            if not self._pending_changes[material_code]:
                del self._pending_changes[material_code]

    def revert_changes(self):
        """Полный откат всех изменений - восстановление из базы данных"""
        try:
            # Откатываем все незакоммиченные изменения в БД
            if db.is_active:
                db.rollback()
            
            # Закрываем и заново открываем сессию для полного сброса
            db.close()
            
            # Полностью перезагружаем данные из базы
            self._reload_data_from_database()
            
            # Очищаем pending changes
            self._pending_changes.clear()
            
            # Обновляем комбобоксы
            self.refresh_all_comboboxes()
            
            self.show_message("Все изменения отменены, данные восстановлены из базы")
            
        except Exception as e:
            self.show_error_message(f"Ошибка отката: {str(e)}")
            # Пытаемся восстановить соединение
            try:
                if not db.is_active:
                    db.begin()
            except:
                pass

    def _update_original_values(self):
        """Обновление оригинальных значений из текущей таблицы"""
        try:
            self._original_values.clear()
            
            for row in range(self.table.rowCount()):
                code_item = self.table.item(row, 0)
                if code_item:
                    material_code = code_item.text()
                    self._original_values[material_code] = {}
                    
                    for col in range(self.table.columnCount()):
                        header = self.table.horizontalHeaderItem(col).text()
                        item = self.table.item(row, col)
                        if item:
                            self._original_values[material_code][header] = item.text()
        except Exception as e:
            print(f"Ошибка обновления оригинальных значений: {e}")

    def _reload_data_from_database(self):
        """Полная перезагрузка данных из базы данных с восстановлением"""
        try:
            # Сохраняем текущие фильтры
            current_filters = {
                'code': self.ui.line_ID.text().strip(),
                'article': self.ui.line_Artical.text().strip(),
                'brand': self.ui.line_Brand.currentText(),
                'family': self.ui.line_Prod_Fam.currentText(),
                'product_name': self.ui.line_Prod_name.currentText()
            }
            
            # Закрываем текущую сессию для чистого старта
            if db.is_active:
                db.close()
            
            # Открываем новую сессию
            db.begin()
            
            # Получаем свежие данные из базы
            prod_df = self.get_Products_from_db()
            
            # Применяем фильтры
            if not prod_df.empty:
                code = current_filters['code']
                article = current_filters['article']
                brand = current_filters['brand']
                family = current_filters['family']
                product_name = current_filters['product_name']

                if code:
                    prod_df = prod_df[prod_df["Code"].astype(str).str.contains(code, case=False, na=False)]
                if article:
                    prod_df = prod_df[prod_df["Article"].astype(str).str.contains(article, case=False, na=False)]
                if brand != "-":
                    prod_df = prod_df[prod_df["Brand"] == brand]
                if family != "-":
                    prod_df = prod_df[prod_df["Family"] == family]
                if product_name != "-":
                    prod_df = prod_df[prod_df["Material_Name"] == product_name]

            # Обновляем таблицу
            self._display_data(prod_df)
            
        except Exception as e:
            raise Exception(f"Ошибка перезагрузки данных: {str(e)}")
        finally:
            # Всегда коммитим изменения
            try:
                db.commit()
            except:
                db.rollback()

    def update_material_field(self, material_code, field_name, new_value):
        """Обновление поля материала в БД (без коммита)"""
        try:
            material = db.query(Materials).filter(Materials.Code == material_code).first()
            if material:
                setattr(material, field_name, new_value)
                return True
            return False
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка БД при обновлении материала: {str(e)}")

    def update_product_name(self, material_code, new_product_name):
        """Обновление названия продукта в связанной таблице Product_Names (без коммита)"""
        try:
            material = db.query(Materials).filter(Materials.Code == material_code).first()
            if not material:
                return False
            
            product_name = db.query(Product_Names).filter(
                Product_Names.id == material.Product_Names_id
            ).first()
            
            if product_name:
                product_name.Product_name = new_product_name
                # После изменения обновляем отображение
                self.find_Product()
                return True
            return False
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка БД при обновлении названия продукта: {str(e)}")

    def update_tnved_for_material(self, material_code, new_tnved_code):
        """Обновление TNVED для материала"""
        try:
            # Закрываем предыдущую сессию если активна
            if db.is_active:
                db.close()
                
            material = db.query(Materials).filter(Materials.Code == material_code).first()
            if not material:
                raise Exception("Материал не найден")
            
            product_name = db.query(Product_Names).filter(
                Product_Names.id == material.Product_Names_id
            ).first()
            
            if not product_name:
                raise Exception("Наименование продукта не найдено")
            
            # Находим или создаем TNVED
            tnved = db.query(TNVED).filter(TNVED.code == new_tnved_code).first()
            if not tnved:
                tnved = TNVED(code=new_tnved_code)
                db.add(tnved)
                db.flush()  # Используем flush вместо commit
                
            # Находим или создаем product_group
            if product_name.Product_Group_id:
                product_group = db.query(Product_Group).filter(
                    Product_Group.id == product_name.Product_Group_id
                ).first()
                if product_group:
                    product_group.TNVED_id = tnved.id
            else:
                # Создаем новую группу если нет привязки
                new_group_id = f"GRP_{material_code}"
                product_group = Product_Group(
                    id=new_group_id,
                    Product_name=product_name.Product_name,
                    TNVED_id=tnved.id
                )
                db.add(product_group)
                db.flush()
                
                # Обновляем привязку product_name к группе
                product_name.Product_Group_id = new_group_id
            
            return True
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка БД при обновлении TNVED: {str(e)}")
        finally:
            if db.is_active:
                db.close()

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
                    self.update_ABC_cat()
                    
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

    def read_product_file(self, file_path):
        """Чтение данных из Excel с фильтрацией и обработкой значений"""
        try:
            # Чтение файла с новыми продуктами (из All_data_file)
            dtype_prod = {"Артикул": str, "ТН ВЭД": str}
            new_df_oil = pd.read_excel(All_data_file, sheet_name="Oils", dtype=dtype_prod)
            new_df_other = pd.read_excel(All_data_file, sheet_name="Other", dtype=dtype_prod)
            
            # Объединяем и фильтруем новые продукты (только те, где ID начинается с 'new')
            new_df = pd.concat([new_df_oil, new_df_other], ignore_index=True)
            new_df = new_df[new_df['ID 1C'].str.startswith('new', na=False)]
            
            # Переименовываем колонки для соответствия с основной таблицей
            new_df = new_df.rename(columns={
                'ID 1C': 'Code',
                'Артикул': 'Article',
                'Продукт + упаковка': 'Material_Name',
                'Product name': 'Product_name',
                'Type': 'Product_type',
                'Brand': 'Brand',
                'Family': 'Family',
                'ЕИ в 1С': 'UoM',
                'ЕИ': 'Report_UoM',
                'Вид упаковки': 'Package_type',
                'Акциз (да/нет)': 'Excise',
                'Упаковка': 'Package_Volume',
                'Кол-во в упак': 'Items_per_Package',
                'Плотность': 'Density',
                'Вес Нетто кг': 'Net_weight',
                'Вес Брутто кг': 'Gross_weight',
                'Код ТНВЭД': 'TNVED',
                'Полное наименование': 'Full_name',
                'Код группы': 'Код_группы'
            })
            
            # Устанавливаем фиксированные значения для новых продуктов
            new_df['Items_per_Set'] = 1
            new_df['Status'] = 'новый'

            df = pd.read_excel(file_path, sheet_name=0, dtype=dtype_prod)
            
            required_columns = ['Код', 'Product name', 'Шт в комплекте', 'Единица измерения отчетов']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит необходимых столбцов")

            valid_types = ['Товары', 'Услуги', 'Нефтепродукты', 'Продукция']
            df = df[df['Вид номенклатуры'].isin(valid_types)]

            valid_groups = ['Доставка (курьерская)', 'ГСМ', 'ЗАПАСНЫЕ ЧАСТИ']
            df = df[df['Номенклатурная группа'].isin(valid_groups)]

            df['Статус'] = df['Артикул'].apply(lambda x: 'не активный' if 'удален_' in str(x) else 'активный')
            df['Артикул'] = df['Артикул'].str.replace('удален_', '', regex=False)
            df['Наименование'] = df['Наименование'].str.replace('удален_', '', regex=False)
            df['Type'] = df['Type'].fillna(df['Вид номенклатуры'])
            
            # 3. Переименование колонок
            column_map = {
                'Код': 'Code', 
                'Артикул': 'Article', 
                'Наименование': 'Material_Name',
                'Полное наименование': 'Full_name',
                'Brand': 'Brand', 
                'Family': 'Family',
                'Product name': 'Product_name', 
                'Type': 'Product_type', 
                'Единица': 'UoM',
                'Единица измерения отчетов': 'Report_UoM', 
                'Вид упаковки': 'Package_type',
                'Количество в упаковке': 'Items_per_Package', 
                'Шт в комплекте': 'Items_per_Set',
                'Упаковка(Литраж)': 'Package_Volume', 
                'Нетто': 'Net_weight', 
                'Брутто': 'Gross_weight',
                'Плотность': 'Density', 
                'ТН ВЭД': 'TNVED', 
                'Акциз': 'Excise',
                'Код группы': 'Код_группы',
                'Статус': 'Status'  # Добавляем новую колонку в маппинг
            }
            df = df.rename(columns=column_map)
            df = pd.concat([df, new_df], ignore_index=True)
            
            df["Package_type"] = df["Package_type"].replace({"комплект кан": "комплект", "комплект туб": "комплект"})
            df.loc[df["Package_type"] == "комплект", "Package_Volume"] = df["Package_Volume"] / df["Items_per_Set"]
            
            for_replace = {"Канистра": "шт", "бочка": "шт", "Туба": "шт", "банка": "шт", "л ": "л"}
            df["UoM"] = df["UoM"].replace(for_replace)
            
            df['TNVED'] = df['TNVED'].fillna('-')
            df['TNVED'] = df['TNVED'].replace({'': '-', 'nan': '-', 'None': '-', None: '-'})
            df['TNVED'] = df['TNVED'].astype(str).str.strip()
            
            # 4. Обработка числовых и текстовых значений
            numeric_cols = ['Items_per_Package', 'Items_per_Set', 'Package_Volume', 
                        'Net_weight', 'Gross_weight', 'Density']
            text_cols = ['Article', 'Material_Name', 'Full_name', 'Brand', 'Family',
                    'Product_name', 'Product_type', 'UoM', 'Report_UoM', 
                    'Package_type', 'TNVED', 'Excise', 'Status']  # Добавляем Status
            
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
        """Сохранение данных TNVED с правильным приведением типов"""
        if not data:
            return

        try:
            # Получаем уникальные коды ТН ВЭД из данных (как строки)
            tnved_codes = {str(row['TNVED']) for row in data if row.get('TNVED') and str(row['TNVED']) != '-'}
            
            if not tnved_codes:
                return
                
            # Получаем существующие коды из БД (как строки)
            existing_tnved = {str(t.code) for t in db.query(TNVED.code).all()}
            
            # Находим новые коды для добавления
            new_tnved_codes = tnved_codes - existing_tnved
            
            if new_tnved_codes:
                try:
                    # Вставка в вашем стиле с явным приведением типов
                    to_insert = [{"code": str(code)} for code in new_tnved_codes]
                    db.bulk_insert_mappings(TNVED, to_insert)
                    db.commit()
                    
                    # Уведомления о новых кодах
                    for code in new_tnved_codes:
                        self.show_message(f"Добавлен новый ТН ВЭД {code}. Проверьте таблицу Пошлины и ЭкоСбор")
                    
                except SQLAlchemyError as e:
                    db.rollback()
                    raise Exception(f"Ошибка сохранения TNVED: {str(e)}")

            # Получаем соответствие кодов и ID (с явным приведением типов)
            tnved_mapping = {
                str(t.code): t.id 
                for t in db.query(TNVED).all()
            }
            
            # Обновляем TNVED_id для всех строк данных
            for row in data:
                if row.get('TNVED') and str(row['TNVED']) != '-':
                    row['TNVED_id'] = tnved_mapping.get(str(row['TNVED']))
                        
        except Exception as e:
            raise Exception(f"Ошибка обработки TNVED: {str(e)}")
        finally:
            db.close()

    def save_Product_Group(self, data):
        """Сохранение данных Product_Group"""
        if not data:
            return

        # Собираем уникальные группы продуктов
        product_groups = {}
        for row in data:
            if row.get('Код_группы') and row.get('Product_name') != '-' and row.get('TNVED'):
                # Находим ID TNVED для этой группы
                tnved_id = db.query(TNVED.id).filter(TNVED.code == row['TNVED']).scalar()
                if tnved_id:
                    product_groups[row['Код_группы']] = {
                        'id': row['Код_группы'],
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
            if row.get('Material_Name'):
                product_group_id = row['Код_группы'] if row.get('Код_группы') and row.get('Product_name') != '-' else None
                product_names[row['Material_Name']] = {
                    'Product_name': row['Material_Name'], 
                    'Product_Group_id': product_group_id
                }

        # Получаем существующие наименования из БД
        existing_names = {n.Product_name: n for n in db.query(Product_Names).all()}
        
        # Разделяем на новые и существующие наименования
        to_insert = []
        to_update = []
        
        for name, name_data in product_names.items():
            if name in existing_names:
                # Обновляем только если изменилась группа
                if existing_names[name].Product_Group_id != name_data['Product_Group_id']:
                    to_update.append({
                        'id': existing_names[name].id,
                        'Product_Group_id': name_data['Product_Group_id']
                    })
            else:
                to_insert.append({
                    'Product_name': name_data['Product_name'],
                    'Product_Group_id': name_data['Product_Group_id']
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

        try:
            # Получаем существующие материалы из БД
            existing_materials = {m.Code: m for m in db.query(Materials).all()}
            
            # Получаем mapping наименований продуктов к их ID
            name_to_id = {n.Product_name: n.id for n in db.query(Product_Names).all()}
            
            # Получаем список новых продуктов из текущего файла
            current_new_products = {row['Code'] for row in data if str(row.get('Code', '')).startswith('new')}

            to_delete = [
                code for code in existing_materials.items() 
                if str(code).startswith('new') and code not in current_new_products]
            
            if to_delete:
                db.query(Materials).filter(Materials.Code.in_(to_delete)).delete(synchronize_session=False)
                db.commit()
            
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
                    'Status': row.get('Status', 'активный'),  # Добавляем статус
                    'Product_Names_id': product_name_id
                }
                
                if row['Code'] in existing_materials:
                    to_update.append(material_data)
                else:
                    to_insert.append(material_data)
            
            if to_insert:
                db.bulk_insert_mappings(Materials, to_insert)
            if to_update:
                db.bulk_update_mappings(Materials, to_update)
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения Materials: {str(e)}")
        finally:
            db.close()
    
    def update_ABC_cat(self):
        """Обновление ABC категорий для продуктов с улучшенной обработкой"""
        try:
            # Чтение файла
            file_path = All_data_file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {os.path.basename(file_path)} не найден")

            with pd.ExcelFile(file_path) as excel:
                df = pd.read_excel(excel, sheet_name="ABC")

            if 'Категория ABCD' not in df.columns:
                raise ValueError("Файл не содержит обязательной колонки 'Категория ABCD'")
            
            df["Дата изм"] = pd.to_datetime(df["Дата изм"], format="%d.%m.%Y", errors="coerce")
            df["Дата оконч"] = pd.to_datetime(df["Дата оконч"], format="%d.%m.%Y", errors="coerce")
            
            # Переименование колонок
            df = df.rename(columns={
                'Продукт + упаковка': 'product_name',
                'Дата изм': 'Start_date',
                'Дата оконч': 'End_date',
                'Категория ABCD': 'ABC_category'
            })

            # Очистка данных
            df = df.dropna(subset=['product_name', 'ABC_category', 'Start_date', 'End_date'])
            df['ABC_category'] = df['ABC_category'].astype(str).str.strip()
            df = df[df['ABC_category'] != '']
            
            # Преобразование дат
            df['Start_date'] = pd.to_datetime(df['Start_date'], dayfirst=True, errors='coerce').dt.date
            df['End_date'] = pd.to_datetime(df['End_date'], dayfirst=True, errors='coerce').dt.date
            df = df.dropna(subset=['Start_date', 'End_date'])
            
            if df.empty:
                self.show_message("Нет данных для обработки после очистки")
                return

            # Получаем данные из БД с нормализацией
            products = {n.Product_name.lower().strip(): n.id for n in db.query(Product_Names).all()}
            categories = {c.ABC_category.lower().strip(): c.id for c in db.query(ABC_list).all()}
            
            # Создаем временный словарь для новых категорий
            new_categories = {}
            for cat in df['ABC_category'].unique():
                norm_cat = str(cat).lower().strip()
                if norm_cat not in categories and norm_cat not in new_categories:
                    new_categories[norm_cat] = cat  # Сохраняем оригинальное написание

            # Добавляем новые категории в БД
            if new_categories:
                for norm_cat, orig_cat in new_categories.items():
                    db.add(ABC_list(ABC_category=orig_cat))
                db.commit()
                # Обновляем список категорий
                categories = {c.ABC_category.lower().strip(): c.id for c in db.query(ABC_list).all()}

            # Подготовка данных для вставки
            to_insert = []
            missing_products = set()
            
            for _, row in df.iterrows():
                norm_product = str(row['product_name']).lower().strip()
                norm_category = str(row['ABC_category']).lower().strip()
                
                product_id = products.get(norm_product)
                category_id = categories.get(norm_category)
                
                if not product_id:
                    missing_products.add(row['product_name'])
                    continue
                    
                # Проверяем существование записи
                exists = db.query(ABC_cat).filter(
                    ABC_cat.product_name_id == product_id,
                    ABC_cat.abc_list_id == category_id,
                    ABC_cat.Start_date == row['Start_date'],
                    ABC_cat.End_date == row['End_date']
                ).first()
                
                if not exists:
                    to_insert.append({
                        'product_name_id': product_id,
                        'abc_list_id': category_id,
                        'Start_date': row['Start_date'],
                        'End_date': row['End_date']
                    })

            # Вставка данных
            if to_insert:
                db.bulk_insert_mappings(ABC_cat, to_insert)
                db.commit()
            
            # Формирование отчета
            report = [
                f"Пропущено ABCD из-за отсутствия продукта: {len(missing_products)}"
            ]
            
            if missing_products:
                report.append("\nПримеры отсутствующих продуктов:")
                report.extend(list(missing_products)[:5])
            
            self.show_message("\n".join(report))
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка обновления ABC: {str(e)}")
        finally:
            db.close()

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
        self._get_unique_values.cache_clear()
        self.fill_in_prod_brand_list()
        self.fill_in_prod_fam_list()
        self.fill_in_prod_name_list()

    def fill_in_prod_brand_list(self):
        """Заполнение списка брендов"""
        brands = self._get_unique_values(Materials.Brand)
        self._fill_combobox(self.ui.line_Brand, brands)

    def fill_in_prod_fam_list(self):
        """Заполняет список Family только для выбранного Brand"""
        brand = self.ui.line_Brand.currentText()
        
        if brand == '-':
            # Если бренд не выбран, показываем все семейства
            families = self._get_unique_values(Materials.Family)
        else:
            # Фильтруем Family только для выбранного Brand
            families = self._get_unique_values(
                Materials.Family,
                filter_column=Materials.Brand,
                filter_value=brand
            )
        
        self._fill_combobox(self.ui.line_Prod_Fam, families)

    def fill_in_prod_name_list(self):
        """Заполняет список Product_name только для выбранных Brand и Family"""
        brand = self.ui.line_Brand.currentText()
        family = self.ui.line_Prod_Fam.currentText()
        
        if family == '-':
            # Если Family не выбрано, фильтруем только по Brand (если выбран)
            if brand == '-':
                products = self._get_unique_values("product_name")  # Все продукты
            else:
                products = self._get_unique_values(
                    "product_name",
                    filter_column=Materials.Brand,
                    filter_value=brand
                )
        else:
            # Фильтруем Product_name по Brand + Family
            products = self._get_unique_values(
                "product_name",
                filter_column=Materials.Family,
                filter_value=family
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
        
        # Подзапрос для ABC-категорий
        subq = (
            db.query(
                ABC_cat.product_name_id,
                ABC_list.ABC_category.label('ABC_category'),
                func.max(ABC_cat.Start_date).label('max_date')
            )
            .join(ABC_list, ABC_cat.abc_list_id == ABC_list.id)
            .filter(ABC_cat.End_date >= today)
            .group_by(ABC_cat.product_name_id, ABC_list.ABC_category)
            .subquery()
        )
        
        # Основной запрос с JOIN к TNVED и Product_Names
        query = (
            db.query(
                Materials.Code,
                Materials.Article,
                Materials.Full_name,
                Product_Names.Product_name.label('Material_Name'),  # Берем из Product_Names
                Materials.Brand,
                Materials.Family,
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
                Materials.Excise,
                Materials.Status,  # Добавляем статус
                TNVED.code.label('TNVED'),
                subq.c.ABC_category
            )
            .join(Product_Names, Materials.Product_Names_id == Product_Names.id)
            .join(Product_Group, Product_Names.Product_Group_id == Product_Group.id)
            .join(TNVED, Product_Group.TNVED_id == TNVED.id)
            .outerjoin(subq, Product_Names.id == subq.c.product_name_id)
        )
        
        df = pd.read_sql(query.statement, db.bind)
        return df.where(pd.notnull(df), None)
    
    def find_Product(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        prod_df = self.get_Products_from_db()

        # Применяем фильтры
        if not prod_df.empty:
            code = self.ui.line_ID.text().strip()
            article = self.ui.line_Artical.text().strip()
            brand = self.ui.line_Brand.currentText()
            family = self.ui.line_Prod_Fam.currentText()
            product_name = self.ui.line_Prod_name.currentText()

            # Для Code: поиск по началу строки
            if code:
                prod_df = prod_df[prod_df["Code"].astype(str).str.startswith(code, na=False)]
                
            # Для Article: обычный contains (без regex) для избежания проблем со спецсимволами
            if article:
                prod_df = prod_df[prod_df["Article"].astype(str).str.contains(article, case=False, na=False)]
                
            if brand != "-":
                prod_df = prod_df[prod_df["Brand"] == brand]
            if family != "-":
                prod_df = prod_df[prod_df["Family"] == family]
            if product_name != "-":
                prod_df = prod_df[prod_df["Material_Name"] == product_name]

            self._display_data(prod_df)
        else:
            self.show_error_message("Нет данных для отображения")

    def _display_data(self, df):
        """Отображение данных в таблице с сохранением оригинальных значений"""
        self.table.clear()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        
        if df.empty:
            self.show_error_message('Нет данных для отображения')
            return
        
        # Устанавливаем флаг обновления таблицы
        self._updating_table = True
        
        # Очищаем предыдущие значения
        self._original_values.clear()
        self._pending_changes.clear()
        
        # Заполнение пропущенных значений
        df = df.fillna('')
        
        # Установка размеров таблицы
        headers = df.columns.tolist()
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Определение типов колонок
        text_columns = ['Article', 'Material_Name', 'Full_name', 'Brand', 'Family', 
                    'Product_name', 'Product_type', 'UoM', 'Report_UoM', 
                    'Package_type', 'TNVED', 'Excise', 'Status']
        
        # Заполнение данных
        for i in range(len(df)):
            material_code = str(df.iloc[i]['Code'])
            self._original_values[material_code] = {}
            
            for j, col in enumerate(headers):
                value = df.iloc[i][col]
                item = QTableWidgetItem(str(value))
                
                # Сохраняем оригинальное значение
                self._original_values[material_code][col] = str(value)
                
                # Устанавливаем флаги для возможности редактирования
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                
                # Выравнивание
                if col in text_columns:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                    
                self.table.setItem(i, j, item)
        
        # Автоматическая настройка ширины столбцов
        self.table.resizeColumnsToContents()
        
        # Установка минимальной ширины для столбцов
        for i in range(self.table.columnCount()):
            if self.table.columnWidth(i) < 100:
                self.table.setColumnWidth(i, 100)
        
        # Снимаем флаг обновления таблицы
        self._updating_table = False
        self._update_original_values()

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
        """Показать информационное сообщение"""
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setIcon(QMessageBox.Information)
        
        # Устанавливаем большой минимальный размер
        msg.setMinimumSize(900, 600)
        
        # Всегда используем detailed text для длинных сообщений
        if len(text) > 500:
            short_text = "Подробная информация ниже (используйте кнопку 'Show Details')"
            msg.setText(short_text)
            msg.setDetailedText(text)
        else:
            msg.setText(text)
        
        # Кнопки
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        def copy_text():
            QApplication.clipboard().setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setIcon(QMessageBox.Critical)
        
        # Устанавливаем большой минимальный размер
        msg.setMinimumSize(900, 600)
        
        # Всегда используем detailed text для длинных сообщений
        if len(text) > 500:
            short_text = "Произошла ошибка. Подробности ниже (используйте кнопку 'Show Details')"
            msg.setText(short_text)
            msg.setDetailedText(text)
        else:
            msg.setText(text)
        
        # Кнопки
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        def copy_text():
            QApplication.clipboard().setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()

    
    