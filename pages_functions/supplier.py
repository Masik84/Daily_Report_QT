import os
import pandas as pd
import numpy as np
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QApplication, QMenu,
                              QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from functools import lru_cache

from db import db, engine
from models import Supplier, SupplScheme
from wind.pages.supplier_ui import Ui_Form
from config import All_data_file, AddCosts_File


class SupplierWidget(QWidget):
    def __init__(self):
        super(SupplierWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._setup_ui()
        self._setup_connections()

        self.supplier_file_path = All_data_file
        self.scheme_file_path = AddCosts_File

        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)
        
        # Добавляем контекстное меню для копирования
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                selection-background-color: #3daee9;
                selection-color: black;
            }
        """)

    def show_context_menu(self, position):
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        copy_action.triggered.connect(self.copy_cell_content)
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def copy_cell_content(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            clipboard = QApplication.clipboard()
            text = "\n".join(item.text() for item in selected_items)
            clipboard.setText(text)

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.btn_find_suppl.clicked.connect(self.find_supplier)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)

    def upload_data(self):
        """Загрузка данных поставщиков и схем за один шаг"""
        try:
            
            try:
                self.run_supplier_func(All_data_file)
                self.run_scheme_func(AddCosts_File)
                
                db.commit()
                self.show_message('Данные поставщиков и схем успешно загружены!')
                
                self.refresh_all_comboboxes()
                
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()

        except Exception as e:
            self._handle_upload_error(e, "поставщиков и схем")

    def _handle_upload_error(self, error, data_type):
        """Обработка ошибок загрузки"""
        if "transaction is already begun" in str(error):
            msg = "Ошибка БД. Закройте программу и попробуйте снова."
        elif "required columns" in str(error).lower():
            msg = "Файл не содержит всех необходимых столбцов."
        else:
            msg = f"Ошибка загрузки {data_type}: {str(error)}"
        self.show_error_message(msg)

    def run_supplier_func(self, data_file_xls):
        """Основная функция обработки данных Supplier"""
        data = self.read_supplier_file(data_file_xls)
        self.save_Supplier(data)
        self.show_message('Данные поставщиков загружены в БД')

    def run_scheme_func(self, scheme_file_xls):
        """Основная функция обработки данных SupplScheme"""
        data = self.read_scheme_file(scheme_file_xls)
        self.save_Scheme(data)

    def read_supplier_file(self, supplier_file_xls):
        """Чтение данных поставщиков из Excel"""
        try:
            df = pd.read_excel(supplier_file_xls, sheet_name='Supplier', dtype={'Контрагент.Код': str})
            
            column_map = {
                'Контрагент.Код': 'id',
                'Полное наименование': 'Full_Suppl_name',
                'Имп/Лок': 'Imp_Loc',
                'Тамож. Пошлина': 'Customs',
                'Перемещ': 'Movement',
                'Страна Рег-ии': 'Country',
                'Контрагент': 'Supplier_Name'
            }
            
            df = df.rename(columns=column_map)[list(column_map.values())]
            
            # Замена значений на "да"/"нет"
            for col in ['Imp_Loc', 'Customs', 'Movement']:
                df[col] = np.where(df[col] == 'да', 'да', 'нет')
            
            return df.to_dict('records')

        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла поставщиков: {str(e)}")
            return []

    def read_scheme_file(self, scheme_file_xls):
        """Чтение данных схем из Excel с уникальным Supplier_Name_report"""
        try:
            df = pd.read_excel(scheme_file_xls, sheet_name='Схемы оплат и доп расх', dtype={'Контрагент.Код': str})
            
            column_map = {
                'Supplier 1': 'Supplier1',
                'Страна': 'Country',
                'Supplier 2': 'Supplier2',
                'Контрагент.Код': 'Supplier_id',
                'Контрагент для отчета': 'Supplier_Name_report',
                'Агентские': 'Agency',
                'Re-export': 'Re_export',
                'Доставка': 'Delivery',
                'Комментарий': 'Comment'
            }
            
            df = df.rename(columns=column_map)[list(column_map.values())]
            df[['Agency', 'Re_export', 'Delivery']] = df[['Agency', 'Re_export', 'Delivery']].astype(float).fillna(0.0)
            
            # Проверка уникальности Supplier_Name_report
            if df['Supplier_Name_report'].duplicated().any():
                duplicates = df[df['Supplier_Name_report'].duplicated(keep=False)]['Supplier_Name_report'].unique()
                raise ValueError(f"Найдены дубликаты в Supplier_Name_report: {', '.join(duplicates)}")
            
            return df.to_dict('records')

        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла схем: {str(e)}")
            return []

    def save_Supplier(self, data):
        """Сохранение поставщиков с обновлением существующих"""
        if not data:
            return

        existing_suppliers = {s.id: s for s in db.query(Supplier).all()}
        to_insert = []
        to_update = []

        for row in data:
            supplier_id = row['id']
            supplier_data = {
                'id': supplier_id,
                'Supplier_Name': row['Supplier_Name'],
                'Full_Suppl_name': row['Full_Suppl_name'],
                'Imp_Loc': row['Imp_Loc'],
                'Customs': row['Customs'],
                'Movement': row['Movement'],
                'Country': row['Country']
            }

            if supplier_id in existing_suppliers:
                to_update.append(supplier_data)
            else:
                to_insert.append(supplier_data)

        try:
            if to_insert:
                db.bulk_insert_mappings(Supplier, to_insert)
            if to_update:
                db.bulk_update_mappings(Supplier, to_update)
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения поставщиков: {str(e)}")
        finally:
            db.close()

    def save_Scheme(self, data):
        if not data:
            self.show_message("Нет данных для сохранения")
            return

        stats = {
            'total': 0,
            'saved': 0,
            'invalid_supplier': 0,
            'duplicate_report_name': 0,
            'skipped': []
        }

        try:
            # Получаем существующие схемы и поставщиков
            existing_schemes = {s.Supplier_Name_report: s for s in db.query(SupplScheme).all()}
            supplier_ids = {s[0] for s in db.query(Supplier.id).all()}
            
            # Получаем максимальный существующий ID для новых записей
            max_id = db.query(func.max(SupplScheme.id)).scalar() or 0
            new_id = max_id + 1

            for row in data:
                stats['total'] += 1
                
                # Проверка supplier_id
                supplier_id = row['Supplier_id']
                if not supplier_id or supplier_id not in supplier_ids:
                    stats['invalid_supplier'] += 1
                    stats['skipped'].append(f"Неверный Supplier_id: {supplier_id}")
                    continue
                
                report_name = row['Supplier_Name_report']
                
                # Проверка и преобразование данных
                try:
                    if report_name in existing_schemes:
                        # Обновление существующей записи
                        scheme = existing_schemes[report_name]
                        scheme.Supplier1 = str(row['Supplier1'])
                        scheme.Country = str(row['Country']) if pd.notna(row.get('Country')) else "-"
                        scheme.Supplier2 = str(row['Supplier2'])
                        scheme.Supplier_id = supplier_id
                        scheme.Agency = float(row.get('Agency', 0.0)) if pd.notna(row.get('Agency')) else 0.0
                        scheme.Re_export = float(row.get('Re_export', 0.0)) if pd.notna(row.get('Re_export')) else 0.0
                        scheme.Delivery = float(row.get('Delivery', 0.0)) if pd.notna(row.get('Delivery')) else 0.0
                        scheme.Comment = str(row.get('Comment')) if pd.notna(row.get('Comment')) else "-"
                    else:
                        # Создание новой записи с явным указанием ID
                        scheme = SupplScheme(
                            id=new_id,
                            Supplier1=str(row['Supplier1']),
                            Country=str(row['Country']) if pd.notna(row.get('Country')) else "-",
                            Supplier2=str(row['Supplier2']),
                            Supplier_id=supplier_id,
                            Supplier_Name_report=report_name,
                            Agency=float(row.get('Agency', 0.0)) if pd.notna(row.get('Agency')) else 0.0,
                            Re_export=float(row.get('Re_export', 0.0)) if pd.notna(row.get('Re_export')) else 0.0,
                            Delivery=float(row.get('Delivery', 0.0)) if pd.notna(row.get('Delivery')) else 0.0,
                            Comment=str(row.get('Comment')) if pd.notna(row.get('Comment')) else "-"
                        )
                        db.add(scheme)
                        new_id += 1
                    
                    stats['saved'] += 1

                except (ValueError, TypeError) as e:
                    stats['skipped'].append(f"Некорректные данные для {report_name}: {str(e)}")
                    continue

            db.commit()

            report = [
                f"Всего обработано: {stats['total']}",
                f"Сохранено схем: {stats['saved']}",
                f"Пропущено из-за неверного Supplier_id: {stats['invalid_supplier']}",
                f"Пропущено из-за некорректных данных: {len([x for x in stats['skipped'] if 'данные' in x])}"
            ]
            
            self.show_message("\n".join(report))

        except SQLAlchemyError as e:
            db.rollback()
            error_msg = f"Ошибка сохранения схем: {str(e)}\n\n{stats}"
            self.show_error_message(error_msg)
        finally:
            db.close()

    def get_Suppliers_from_db(self):
        """Получение списка поставщиков из базы"""
        try:
            suppliers = db.query(Supplier).all()
            return [s.Supplier_Name for s in suppliers]
        except Exception as e:
            self.show_error_message(f"Ошибка при получении поставщиков: {str(e)}")
            return []

    def get_merged_schemes_from_db(self):
        """Получение объединенных данных схем с информацией о поставщиках"""
        try:
            query = db.query(
                SupplScheme.Supplier1,
                SupplScheme.Country,
                SupplScheme.Supplier2,
                SupplScheme.Supplier_id,
                SupplScheme.Supplier_Name_report,
                Supplier.Imp_Loc,
                Supplier.Movement,
                SupplScheme.Agency,
                SupplScheme.Re_export,
                SupplScheme.Delivery,
                SupplScheme.Comment
            ).join(Supplier, SupplScheme.Supplier_id == Supplier.id)
            
            df = pd.read_sql(query.statement, db.bind)
            return df.where(pd.notnull(df), None)
        except Exception as e:
            self.show_error_message(f"Ошибка при получении схем: {str(e)}")
            return pd.DataFrame()

    def find_supplier(self):
        """Поиск поставщиков"""
        scheme_df = self._search_schemes()
        self._display_schemes(scheme_df)

    def _search_schemes(self):
        """Логика поиска схем поставщиков"""
        scheme_df = self.get_merged_schemes_from_db()
        if scheme_df.empty:
            self.show_error_message('Нет данных о схемах')
            return pd.DataFrame()

        supplier_id = self.ui.line_ID.text().strip()
        supplier_name1 = self.ui.line_Suppl1.currentText()
        supplier_name2 = self.ui.line_Suppl2.currentText()

        # Фильтрация DataFrame
        if supplier_id:
            scheme_df = scheme_df[scheme_df['Supplier_id'] == supplier_id]
        elif supplier_name1 != '-':
            scheme_df = scheme_df[scheme_df['Supplier_Name_report'].str.contains(supplier_name1, case=False, na=False)]
        elif supplier_name2 != '-':
            scheme_df = scheme_df[scheme_df['Supplier_Name_report'].str.contains(supplier_name2, case=False, na=False)]

        return scheme_df.sort_values('Supplier_Name_report')

    def _display_schemes(self, scheme_df):
        """Отображение данных схем в таблице"""
        self.table.clearContents()
        self.table.setRowCount(0)

        if scheme_df.empty:
            self.show_error_message('Ничего не найдено')
            return
        
        scheme_df = scheme_df.fillna('')
        headers = [
            'Supplier 1', 'Страна', 'Supplier 2', 'Контрагент.Код', 
            'Контрагент для отчета', 'Имп/Лок', 'Перемещ', 
            'Агентские', 'Re-export', 'Доставка', 'Комментарий'
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(scheme_df))
        
        for i in range(len(scheme_df)):
            for j, col in enumerate(headers):
                # Сопоставление имен колонок с именами в DataFrame
                db_col = {
                    'Supplier 1': 'Supplier1',
                    'Страна': 'Country',
                    'Supplier 2': 'Supplier2',
                    'Контрагент.Код': 'Supplier_id',
                    'Контрагент для отчета': 'Supplier_Name_report',
                    'Имп/Лок': 'Imp_Loc',
                    'Перемещ': 'Movement',
                    'Агентские': 'Agency',
                    'Re-export': 'Re_export',
                    'Доставка': 'Delivery',
                    'Комментарий': 'Comment'
                }.get(col, col)
                
                value = scheme_df.iloc[i][db_col]
                value_str = str(value)
                
                item = QTableWidgetItem(value_str)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
        
        # Авто-подгонка ширины столбцов
        self.table.resizeColumnsToContents()
        # Установите минимальную ширину для столбцов, если нужно
        for i in range(self.table.columnCount()):
            if self.table.columnWidth(i) < 100:
                self.table.setColumnWidth(i, 100)

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self._fill_combobox(self.ui.line_Suppl1, self.get_Suppliers_from_db())
        self._fill_combobox(self.ui.line_Suppl2, self.get_Suppliers_from_db())

    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if items:
            combobox.addItems(sorted(items))

    def show_message(self, text):
        """Показать компактное информационное сообщение"""
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        
        # Уменьшаем размер окна
        msg.setMinimumSize(400, 200)
        
        # Добавляем кнопку Copy
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        # Настройка буфера обмена
        clipboard = QApplication.clipboard()
        
        # Обработчики кнопок
        def copy_text():
            clipboard.setText(text)
        
        copy_button.clicked.connect(copy_text)
        
        # Показываем сообщение
        msg.exec_()

    def show_error_message(self, text):
        """Показать компактное сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setMinimumSize(400, 200)
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        clipboard = QApplication.clipboard()
        def copy_text():
            clipboard.setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()



