import pandas as pd
import numpy as np
import os
import datetime

import xlwings as xw
from sqlalchemy import extract
from PySide6.QtWidgets import QScrollArea, QMessageBox, QHeaderView, QTableWidget, QMenu, QApplication, QTableWidgetItem, QWidget, QTextEdit
from PySide6.QtCore import Qt, QDate
from functools import lru_cache
import traceback

from db import db
from models import (Movements, Complects_manual, WriteOff, Complects, AddSupplCost, DOCType, Materials, Customer, Supplier, Product_Names)

from config import Movement_folder, Complectation_file
from wind.pages.moves_ui import Ui_Form
from pages_functions.product import ProductsPage

class MovesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.date_Start.dateChanged.connect(self.on_date_changed)
        self.ui.date_Start.setDate(QDate(2022, 1, 1))
        
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
        
        # Настройка контекстного меню для копирования
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
    
    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.line_table.currentTextChanged.connect(self.on_table_changed)
        self.ui.line_doc_type.currentTextChanged.connect(self.on_doc_type_changed)
        self.ui.line_Year.currentTextChanged.connect(self.on_year_changed)
        self.ui.line_Mnth.currentTextChanged.connect(self.on_month_changed)
        
        self.ui.btn_find.clicked.connect(self.find_moves_data)
        self.ui.btn_refresh.clicked.connect(self.upload_data)
    
    def show_context_menu(self, position):
        """Показ контекстного меню для копирования"""
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        copy_action.triggered.connect(self.copy_cell_content)
        menu.exec_(self.table.viewport().mapToGlobal(position))
    
    def copy_cell_content(self):
        """Копирование содержимого выделенных ячеек"""
        selected_items = self.table.selectedItems()
        if selected_items:
            clipboard = QApplication.clipboard()
            if len(selected_items) == 1:
                text = selected_items[0].text()
            else:
                rows = {}
                for item in selected_items:
                    row = item.row()
                    col = item.column()
                    if row not in rows:
                        rows[row] = {}
                    rows[row][col] = item.text()
                
                sorted_rows = sorted(rows.items())
                text = ""
                for row, cols in sorted_rows:
                    sorted_cols = sorted(cols.items())
                    text += "\t".join([text for col, text in sorted_cols]) + "\n"
            
            clipboard.setText(text.strip())
    
    def on_date_changed(self, date):
        """Функция, вызываемая при изменении даты."""
        self.report_start_date = date
        self.report_start_date = self.report_start_date.toPython()
        self.report_start_date = pd.to_datetime(self.report_start_date)
        print(f"Выбрана дата: {self.report_start_date}")

        self.do_something_with_date()

    def do_something_with_date(self):
        """Функция, использующая дату."""
        if self.report_start_date:  # Проверяем, что дата была установлена
            print(f"Обработка даты: {self.report_start_date}")
            # Здесь ваш код, который использует self.report_start_date
        else:
            print("Дата еще не выбрана.")
    
    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self._fill_combobox(self.ui.line_table, ["-", "Движения", "Комплектации", "Комплектации Ручные", "Списания"])
        self.fill_doc_type_list()
        self.fill_year_list()
        self.fill_month_list()
        self.fill_customer_list()
        self.fill_product_list()
    
    def on_table_changed(self):
        """Обработчик изменения таблицы"""
        self.fill_doc_type_list()
        self.fill_year_list()
        self.fill_month_list()
        self.fill_customer_list()
        self.fill_product_list()
    
    def on_doc_type_changed(self):
        """Обработчик изменения типа документа"""
        self.fill_year_list()
        self.fill_month_list()
        self.fill_customer_list()
        self.fill_product_list()
    
    def on_year_changed(self):
        """Обработчик изменения года"""
        self.fill_month_list()
        self.fill_customer_list()
        self.fill_product_list()
    
    def on_month_changed(self):
        """Обработчик изменения месяца"""
        self.fill_customer_list()
        self.fill_product_list()
    
    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        current_text = combobox.currentText()
        combobox.clear()
        
        filtered_items = [str(item) for item in items if item is not None and str(item).strip()]
        unique_items = sorted(list(set(filtered_items)))
        
        if not unique_items or unique_items[0] != "-":
            unique_items = ["-"] + [item for item in unique_items if item != "-"]
        
        combobox.addItems(unique_items)
        
        if current_text in unique_items:
            combobox.setCurrentText(current_text)
        else:
            combobox.setCurrentText("-")

    def fill_doc_type_list(self):
        """Заполнение списка типов документов"""
        try:
            table = self.ui.line_table.currentText()
            if table == "-":
                self._fill_combobox(self.ui.line_doc_type, ["-"])
                return
                
            # Определяем модель в зависимости от выбранной таблицы
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_doc_type, ["-"])
                return
                
            query = db.query(DOCType.Doc_type).join(model.doc_type)
            doc_types = query.distinct()
            doc_types_list = sorted([d[0] for d in doc_types if d[0] is not None])
            
            self._fill_combobox(self.ui.line_doc_type, ["-"] + doc_types_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка типов документов: {str(e)}")
            self._fill_combobox(self.ui.line_doc_type, ["-"])

    def fill_year_list(self):
        """Заполнение списка годов"""
        try:
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            
            if table == "-":
                self._fill_combobox(self.ui.line_Year, ["-"])
                return
                
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_Year, ["-"])
                return
                
            query = db.query(extract('year', model.Date).label('year'))
            
            if doc_type != "-":
                query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                
            years = query.distinct()
            years_list = sorted(list({y[0] for y in years if y[0] is not None}), reverse=True)
            years_list = [str(y) for y in years_list]
            
            self._fill_combobox(self.ui.line_Year, ["-"] + years_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка годов: {str(e)}")
            self._fill_combobox(self.ui.line_Year, ["-"])

    def fill_month_list(self):
        """Заполнение списка месяцев с защитой от пустых значений"""
        try:
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            year = self.ui.line_Year.currentText()
            
            # Если не выбрана таблица или год, очищаем список месяцев
            if table == "-" or year == "-":
                self._fill_combobox(self.ui.line_Mnth, ["-"])
                return
                
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_Mnth, ["-"])
                return
                
            # Проверяем, что год - валидное число
            try:
                year_int = int(year) if year and year != "-" else None
            except ValueError:
                year_int = None
                
            if not year_int:
                self._fill_combobox(self.ui.line_Mnth, ["-"])
                return
                
            # Создаем базовый запрос
            query = db.query(
                extract('month', model.Date).label('month')
            ).filter(
                extract('year', model.Date) == year_int
            )
                
            # Добавляем фильтр по типу документа, если он выбран
            if doc_type and doc_type != "-":
                query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                
            # Получаем уникальные месяцы
            months = query.distinct().all()
            months_list = sorted(
                [str(m[0]) for m in months if m[0] is not None and str(m[0]).strip()]
            )
            
            # Заполняем комбобокс
            self._fill_combobox(self.ui.line_Mnth, ["-"] + months_list)
            
        except Exception as e:
            print(f"Ошибка при загрузке списка месяцев: {str(e)}")
            traceback.print_exc()
            self._fill_combobox(self.ui.line_Mnth, ["-"])

    def fill_customer_list(self):
        """Заполнение списка контрагентов с полной защитой от ошибок"""
        try:
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()

            # Если не выбрана таблица, очищаем список
            if table == "-":
                self._fill_combobox(self.ui.line_customer, ["-"])
                return

            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return

            # Определяем тип запроса в зависимости от модели и типа документа
            if model == Movements:
                if doc_type in ["1.0. Поступление", "1.0. Поступление (перераб)", 
                            "1.1. Поступление (корр-ка)", "7.0. Передача в переработку"]:
                    # Запрос для поставщиков
                    query = db.query(
                        Supplier.id.label('code'),
                        Supplier.Supplier_Name.label('name')
                    ).join(model.supplier)
                else:
                    # Запрос для клиентов
                    query = db.query(
                        Customer.id.label('code'),
                        Customer.Customer_name.label('name')
                    ).join(model.customer)
            elif model == WriteOff:
                # Для списаний всегда используем поставщиков
                query = db.query(
                    Supplier.id.label('code'),
                    Supplier.Supplier_Name.label('name')
                ).join(model.supplier)
            else:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return

            # Применяем фильтры
            if self._is_valid_value(doc_type):
                query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)

            if self._is_valid_value(year):
                try:
                    year_int = int(year)
                    query = query.filter(extract('year', model.Date) == year_int)
                except ValueError:
                    pass

            if self._is_valid_value(month):
                try:
                    month_int = int(month)
                    query = query.filter(extract('month', model.Date) == month_int)
                except ValueError:
                    pass

            # Получаем и обрабатываем результаты
            customers = query.distinct().all()
            customers_list = sorted([f"{c.code} - {c.name}" for c in customers 
                                if c.code is not None and c.name is not None])

            # Заполняем комбобокс
            self._fill_combobox(self.ui.line_customer, ["-"] + customers_list)

        except Exception as e:
            print(f"Ошибка при загрузке списка контрагентов: {str(e)}")
            traceback.print_exc()
            self._fill_combobox(self.ui.line_customer, ["-"])

    def fill_product_list(self):
        """Заполнение списка продуктов с полной защитой от ошибок"""
        try:
            # Получаем текущие значения из интерфейса
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()
            customer = self.ui.line_customer.currentText()

            # Если не выбрана таблица, очищаем список
            if table == "-":
                self._fill_combobox(self.ui.line_product, ["-"])
                return

            # Получаем модель для выбранной таблицы
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_product, ["-"])
                return

            # Создаем базовый запрос
            query = db.query(Product_Names.Product_name).join(Materials, Product_Names.materials)

            # Обрабатываем разные типы моделей
            if model == Movements:
                query = query.join(model, Materials.movements)
                
                # Фильтр по типу документа
                if self._is_valid_value(doc_type):
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                    
                    # Определяем тип контрагента (Supplier или Customer)
                    if doc_type in ["1.0. Поступление", "1.0. Поступление (перераб)", 
                                "1.1. Поступление (корр-ка)", "7.0. Передача в переработку"]:
                        if self._is_valid_value(customer):
                            supplier_name = self._extract_name(customer)
                            query = query.join(model.supplier).filter(Supplier.Supplier_Name == supplier_name)
                    else:
                        if self._is_valid_value(customer):
                            customer_name = self._extract_name(customer)
                            query = query.join(model.customer).filter(Customer.Customer_name == customer_name)

            elif model == WriteOff:
                query = query.join(model, Materials.write_off)
                
                if self._is_valid_value(doc_type):
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                    
                if self._is_valid_value(customer):
                    supplier_name = self._extract_name(customer)
                    query = query.join(model.supplier).filter(Supplier.Supplier_Name == supplier_name)

            elif model == Complects_manual:
                query = query.join(model, Materials.complects_manual)
                
                if self._is_valid_value(doc_type):
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)

            # Применяем фильтры по датам
            if self._is_valid_value(year):
                try:
                    year_int = int(year)
                    query = query.filter(extract('year', model.Date) == year_int)
                except ValueError:
                    pass

            if self._is_valid_value(month):
                try:
                    month_int = int(month)
                    query = query.filter(extract('month', model.Date) == month_int)
                except ValueError:
                    pass

            # Получаем и обрабатываем результаты
            products = query.distinct().all()
            products_list = sorted([str(p[0]) for p in products if p[0] is not None and str(p[0]).strip()])

            # Заполняем комбобокс
            self._fill_combobox(self.ui.line_product, ["-"] + products_list)

        except Exception as e:
            print(f"Ошибка при загрузке списка продуктов: {str(e)}")
            traceback.print_exc()
            self._fill_combobox(self.ui.line_product, ["-"])

    def find_moves_data(self):
        """Поиск данных по заданным критериям"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        try:
            table = self.ui.line_table.currentText()
            if table == "-":
                self.show_message("Пожалуйста, выберите таблицу для поиска")
                return
                
            model = self._get_model_for_table(table)
            if not model:
                self.show_error_message("Неизвестная таблица")
                return
                
            # Создаем базовый запрос
            query = self._build_base_query(model)
            
            # Применяем фильтры
            query = self._apply_filters(query, model)
            
            # Выполняем запрос
            result = query.all()
            
            if not result:
                self.show_message("Данные не найдены")
                return
            
            # Преобразуем результат в DataFrame
            data = []
            for row in result:
                row_data = {
                    "Документ": row.Document,
                    "Дата": row.Date.strftime("%d.%m.%Y") if row.Date else "",
                    "Тип документа": row.Doc_type,
                    "Код": row.Code,
                    "Артикул": row.Article,
                    "Продукт + упаковка": row.Product_name,
                    "Вид упаковки": row.Package_type,
                    "Единица измерения": row.UoM if hasattr(row, 'UoM') else "",
                    "Склад": row.Stock,
                    "Кол-во, шт": self._calculate_pcs(row),
                    "Кол-во, л": self._calculate_liters(row),
                    "Контрагент.Код": self._get_counterparty_code(row, model),
                    "Контрагент": self._get_counterparty_name(row, model) }
                
                # Добавляем специфичные поля для разных таблиц
                if model == Movements:
                    row_data.update({
                        "ДокОсн": row.Doc_based,
                        "Дата ДокОсн": row.Date_Doc_based.strftime("%d.%m.%Y") if row.Date_Doc_based else "",
                        "Грузополучатель.Код": row.Recipient_code,
                        "Грузополучатель": row.Recipient,
                        "Счет": row.Bill,
                        "Дата счета": row.Bill_date.strftime("%d.%m.%Y") if row.Bill_date else ""})
                elif model == WriteOff:
                    row_data.update({
                        "Отчет": row.Reporting,
                        "ДокОсн": row.Doc_based,
                        "Дата ДокОсн": row.Date_Doc_based.strftime("%d.%m.%Y") if row.Date_Doc_based else "",
                        "Order N": row.Order,
                        "Shipment #": row.Shipment,
                        "Вход. док-т": row.Suppl_Inv_N,
                        "Счет": row.Bill,
                        "Дата счета": row.Bill_date.strftime("%d.%m.%Y") if row.Bill_date else "",
                        "Комментарий": row.Comment})
                elif model in [Complects, Complects_manual]:
                    row_data.update({"Дата_Время": row.Date_Time.strftime("%d.%m.%Y %H:%M:%S") if hasattr(row, 'Date_Time') and row.Date_Time else ""})
                
                data.append(row_data)
            
            df = pd.DataFrame(data)
            
            # Отображаем данные в таблице
            self._display_data(df)
            
            # Обновляем сводную информацию
            self._update_summary(df)
            
        except Exception as e:
            self.show_error_message(f"Ошибка при поиске данных: {str(e)}")
            traceback.print_exc()

    def _build_base_query(self, model):
        """Создает базовый запрос в зависимости от модели"""
        if model == Movements:
            return db.query(
                Movements.Document,
                Movements.Date,
                DOCType.Doc_type,
                Materials.Code,
                Materials.Article,
                Product_Names.Product_name,
                Materials.Package_type,
                Materials.UoM,
                Materials.Package_Volume,
                Materials.Items_per_Set,
                Movements.Stock,
                Movements.Qty,
                Movements.Doc_based,
                Movements.Date_Doc_based,
                Movements.Recipient_code,
                Movements.Recipient,
                Movements.Bill,
                Movements.Bill_date,
                Customer.id.label('Customer_id'),
                Customer.Customer_name.label('Customer_name'),
                Supplier.id.label('Supplier_id'),
                Supplier.Supplier_Name.label('Supplier_name')
            ).join(Movements.doc_type
            ).join(Movements.material
            ).join(Materials.product_name
            ).outerjoin(Movements.customer
            ).outerjoin(Movements.supplier)
        
        elif model == WriteOff:
            return db.query(
                WriteOff.Document,
                WriteOff.Date,
                DOCType.Doc_type,
                Materials.Code,
                Materials.Article,
                Product_Names.Product_name,
                Materials.Package_type,
                Materials.UoM,
                Materials.Package_Volume,
                Materials.Items_per_Set,
                WriteOff.Stock,
                WriteOff.Qty,
                WriteOff.Reporting,
                WriteOff.Doc_based,
                WriteOff.Date_Doc_based,
                WriteOff.Order,
                WriteOff.Shipment,
                WriteOff.Suppl_Inv_N,
                WriteOff.Bill,
                WriteOff.Bill_date,
                WriteOff.Comment,
                Supplier.id.label('Supplier_id'),
                Supplier.Supplier_Name.label('Supplier_name')
            ).join(WriteOff.doc_type
            ).join(WriteOff.material
            ).join(Materials.product_name
            ).join(WriteOff.supplier)
        
        elif model == Complects:
            return db.query(
                Complects.Document,
                Complects.Date,
                DOCType.Doc_type,
                Materials.Code,
                Materials.Article,
                Product_Names.Product_name,
                Materials.Package_type,
                Materials.UoM,
                Materials.Package_Volume,
                Materials.Items_per_Set,
                Complects.Stock,
                Complects.Qty,
                Complects.Date_Time
            ).join(Complects.doc_type
            ).join(Complects.material
            ).join(Materials.product_name)
        
        elif model == Complects_manual:
            return db.query(
                Complects_manual.Document,
                Complects_manual.Date,
                DOCType.Doc_type,
                Materials.Code,
                Materials.Article,
                Product_Names.Product_name,
                Materials.Package_type,
                Materials.UoM,
                Materials.Package_Volume,
                Materials.Items_per_Set,
                Complects_manual.Stock,
                Complects_manual.Qty,
                Complects_manual.Date_Time
            ).join(Complects_manual.doc_type
            ).join(Complects_manual.material
            ).join(Materials.product_name)

    def _apply_filters(self, query, model):
        """Применяет фильтры к запросу с полной поддержкой всех моделей"""
        doc_type = self.ui.line_doc_type.currentText()
        year = self.ui.line_Year.currentText()
        month = self.ui.line_Mnth.currentText()
        customer = self.ui.line_customer.currentText()
        cust_id = self.ui.line_cust_id.text()
        article = self.ui.line_article.text()
        product = self.ui.line_product.currentText()
        
        # Общие фильтры для всех моделей
        if doc_type != "-":
            query = query.filter(DOCType.Doc_type == doc_type)
        
        if year != "-":
            query = query.filter(extract('year', model.Date) == int(year))
        
        if month != "-":
            query = query.filter(extract('month', model.Date) == int(month))
        
        if article:
            query = query.filter(Materials.Article.like(f"%{article}%"))
        
        if product != "-":
            query = query.filter(Product_Names.Product_name == product)
        
        # Специфичные фильтры для Movements
        if model == Movements:
            if customer != "-":
                # Определяем, использовать Supplier или Customer по типу документа
                supplier_doc_types = [
                    "1.0. Поступление",
                    "1.0. Поступление (перераб)",
                    "1.1. Поступление (корр-ка)",
                    "7.0. Передача в переработку"
                ]
                
                current_doc_type = self.ui.line_doc_type.currentText()
                if current_doc_type in supplier_doc_types:
                    query = query.filter(Supplier.Supplier_Name == customer)
                else:
                    query = query.filter(Customer.Customer_name == customer)
            
            if cust_id:
                query = query.filter(
                    (Customer.id.like(f"%{cust_id}%")) | 
                    (Supplier.id.like(f"%{cust_id}%")))
        
        # Специфичные фильтры для WriteOff
        elif model == WriteOff:
            if customer != "-":
                query = query.filter(Supplier.Supplier_Name == customer)
            
            if cust_id:
                query = query.filter(Supplier.id.like(f"%{cust_id}%"))
        
        return query

    def _calculate_pcs(self, row):
        """Рассчитывает количество в штуках с защитой от ошибок"""
        try:
            # Проверяем, является ли row словарем или объектом Row
            if isinstance(row, dict):
                package_type = row.get('Package_type', row.get('Вид упаковки'))
                uom = row.get('UoM', row.get('Единица измерения'))
                package_volume = float(row.get('Package_Volume', row.get('Упаковка', 0)))
                items_per_set = float(row.get('Items_per_Set', row.get('Кол-во в упак', 1)))
                qty = float(row.get('Qty', row.get('Количество', 0)))
            else:
                # Для объектов Row/SQLAlchemy
                package_type = getattr(row, 'Package_type', getattr(row, 'Вид упаковки', None))
                uom = getattr(row, 'UoM', getattr(row, 'Единица измерения', None))
                package_volume = float(getattr(row, 'Package_Volume', getattr(row, 'Упаковка', 0)))
                items_per_set = float(getattr(row, 'Items_per_Set', getattr(row, 'Кол-во в упак', 1)))
                qty = float(getattr(row, 'Qty', getattr(row, 'Количество', 0)))

            if not package_type or not qty:
                return 0.0

            if package_type == "комплект":
                return qty * items_per_set
            elif uom == "шт":
                return qty
            elif uom == "т":
                return qty * 1000 / package_volume if package_volume != 0 else 0.0
            else:
                return qty / package_volume if package_volume != 0 else 0.0

        except Exception as e:
            print(f"Ошибка расчета количества в штуках: {str(e)}")
            return 0.0

    def _calculate_liters(self, row):
        """Рассчитывает количество в литрах с защитой от ошибок"""
        try:
            # Получаем количество в штуках
            pcs = self._calculate_pcs(row)
            
            # Получаем объем упаковки
            if isinstance(row, dict):
                package_volume = float(row.get('Package_Volume', row.get('Упаковка', 0)))
            else:
                package_volume = float(getattr(row, 'Package_Volume', getattr(row, 'Упаковка', 0)))

            return pcs * package_volume

        except Exception as e:
            print(f"Ошибка расчета количества в литрах: {str(e)}")
            return 0.0

    def _get_counterparty_code(self, row, model):
        """Возвращает код контрагента"""
        if model == Movements:
            return row.Supplier_id if row.Supplier_id else row.Customer_id
        elif model == WriteOff:
            return row.Supplier_id
        return ""

    def _get_counterparty_name(self, row, model):
        """Возвращает название контрагента"""
        if model == Movements:
            return row.Supplier_name if row.Supplier_name else row.Customer_name
        elif model == WriteOff:
            return row.Supplier_name
        return ""

    def _display_data(self, df):
        """Отображение данных в таблице"""
        self.table.clearContents()
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        numeric_cols = ["Кол-во, шт", "Кол-во, л"]
        
        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                # Преобразуем None/NaN в пустую строку
                if pd.isna(value) or value is None or str(value) in ['None', 'nan', 'NaT']:
                    value = ''

                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                if df.columns[col_idx] in numeric_cols:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    if pd.notna(value) and value != '':
                        try:
                            if df.columns[col_idx] == "Кол-во, шт":
                                item.setText(f"{int(float(value)):,}".replace(",", " "))
                            else:
                                item.setText(f"{float(value):,.2f}".replace(",", " ").replace(".", ","))
                        except (ValueError, TypeError):
                            pass
                
                self.table.setItem(row_idx, col_idx, item)
        
        self.table.resizeColumnsToContents()

    def _update_summary(self, df):
        """Обновление сводной информации"""
        if df.empty:
            volume = pcs = 0
        else:
            volume = df["Кол-во, л"].sum()
            pcs = df["Кол-во, шт"].sum()
        
        def format_number(value):
            return f"{float(value):,.2f}".replace(",", " ").replace(".", ",")
        
        self.ui.label_Volume.setText(f"{format_number(volume)} л." if volume != 0 else "0,00 л.")
        self.ui.label_qty_pcs.setText(f"{int(pcs):,} шт".replace(",", " ") if pcs != 0 else "0 шт.")

    def upload_data(self):
        """Обновление данных из файлов и загрузка в БД"""
        try:
            date_start = self.ui.date_Start.date()
            report_start_date = date_start.toPython()
            report_start_date = pd.to_datetime(report_start_date)
            move_df = self.read_movement_data(report_start_date)
            
            if move_df.empty:
                self.show_message("Нет данных для обновления")
                return
            
            # Проверка наличия документов в AddSupplCost для поступлений
            if not self._check_purchases_in_add_suppl_cost(move_df):
                return  # Прекращаем выполнение, если найдены новые поступления
                
            # Обработка комплектаций и списаний
            move_df = self._process_complectations(move_df, report_start_date)
            
            # Обработка списаний
            move_df = self._process_write_offs(move_df, report_start_date)
            
            # Обновление данных в БД
            self._update_moves_in_db(move_df, report_start_date)
            
            # Запись финальных данных в Excel
            self._write_final_data_to_excel(move_df)
            
            self.show_message("Движения успешно обновлены")
            self.refresh_all_comboboxes()
            
        except Exception as e:
            self.show_error_message(f"Ошибка при обновлении данных: {str(e)}")
            traceback.print_exc()

    def read_movement_data(self, report_start_date):
        """Чтение данных о движениях из файлов"""
        
        move_df = pd.DataFrame()
        dtypes = {"Артикул": str, "Дата": "datetime64[ns]"}
        
        # Определяем файлы для чтения на основе года из date_start
        target_year = report_start_date.year
        files_to_read = []
        
        for root, dirs, files in os.walk(Movement_folder):
            for name in files:
                if name.startswith("Движения_") and name.endswith(".xlsx"):
                    try:
                        file_year = int(name.split("_")[1].split(".")[0])
                        if file_year >= target_year:
                            files_to_read.append(os.path.join(root, name))
                    except (IndexError, ValueError):
                        continue
        
        # Чтение файлов
        frames = []
        for file_path in files_to_read:
            try:
                data = pd.read_excel(file_path, skiprows=5, dtype=dtypes)
                frames.append(data)
            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}")
        
        if frames:
            move_df = pd.concat(frames, axis=0, ignore_index=True)
        
        if move_df.empty:
            return pd.DataFrame()
            
        # Обработка данных
        move_df = self._process_movement_data(move_df, report_start_date)
        return move_df

    def _process_movement_data(self, move_df, report_start_date):
        """Обработка данных о движениях с улучшенной проверкой продуктов"""
        # Переименование колонок
        move_df = move_df.rename(columns={
            "Рег дата время": "Дата_Время",
            "Рег номер": "Документ",
            "Рег дата": "Дата",
            "Рег тип значения": "Вид документа",
            "Рег вид операции": "Вид операции",
            "Единица": "Единица измерения",
            "Код": "Контрагент.Код",
            "Код.1": "Код",
            "Код.2": "Грузополучатель.Код",
        })
        
        # Фильтрация данных
        move_df = move_df.loc[
            (move_df["Приход"] != "Количество приход") & 
            (move_df["Приход"] != "Приход") & 
            (move_df["Дата_Время"] != "Итого")
        ]
        
        # Очистка данных
        move_df["Счет на оплату"] = move_df['Счет на оплату'].str.replace('   ', ' ', regex=False)
        move_df["Код"] = move_df["Код"].str.strip()
        move_df[["Приход", "Расход"]] = move_df[["Приход", "Расход"]].astype(float)
        move_df["Вид операции"] = move_df["Вид операции"].fillna("-")
        move_df.dropna(subset=['Дата'], inplace=True)
        
        # Получаем тип документа из БД
        doc_types = pd.read_sql(
            db.query(
                DOCType.Document,
                DOCType.Transaction,
                DOCType.Doc_type
            ).statement,
            db.bind
        )
        
        move_df = move_df.merge(
            doc_types,
            left_on=["Вид документа", "Вид операции"],
            right_on=["Document", "Transaction"],
            how="left"
        ).rename(columns={"Doc_type": "Тип документа"
        }).drop(columns=["Document", "Transaction"])
        
        # Улучшенная проверка продуктов в БД с возможностью обновления
        move_df = self._check_and_update_products(move_df)
        if move_df.empty:
            return pd.DataFrame()
        
        # Обработка счета на оплату
        move_df[["field_0", "field_1", "Счет", "field_3", "Дата счета", "field_5"]] = move_df["Счет на оплату"].str.split(" ", n=5, expand=True)
        move_df = move_df.drop(columns=["field_0", "field_1", "field_3", "field_5"], axis=1)
        
        # Преобразование дат
        move_df["Дата"] = pd.to_datetime(move_df["Дата"], format="%d.%m.%Y")
        move_df["Дата счета"] = pd.to_datetime(move_df["Дата счета"], format="%d.%m.%Y")
        move_df["Дата_Время"] = pd.to_datetime(move_df["Дата_Время"], format="%d.%m.%Y %H:%M:%S")
        
        # Убедимся, что report_start_date имеет правильный тип
        if not isinstance(report_start_date, pd.Timestamp):
            report_start_date = pd.to_datetime(report_start_date)
        
        # Убедимся, что колонка 'Дата' имеет тип datetime64[ns]
        if not pd.api.types.is_datetime64_any_dtype(move_df['Дата']):
            move_df['Дата'] = pd.to_datetime(move_df['Дата'], format='%d.%m.%Y')
        
        # Теперь фильтрация будет работать корректно
        move_df = move_df[(move_df["Дата"] >= report_start_date)]
        
        # Корректировка типа документа для недостач/утилизаций
        move_df.loc[(move_df["Склад"].str.contains("Недостача")) & (~move_df["Тип документа"].isin(["2.0. Комплектация", "4.0. Реализация"])), "Тип документа"] = "5.0. Списание (недостача)"
        move_df.loc[(move_df["Склад"].str.contains("Утилизация")) & (~move_df["Тип документа"].isin(["2.0. Комплектация", "4.0. Реализация"])), "Тип документа"] = "5.0. Списание (утилизация)"
        
        # 1. Условие для "5.0. Списание (утилизация)"
        move_df.loc[move_df["Тип документа"] == "5.0. Списание (утилизация)", "Вид операции"] = "Списание со склада"
        move_df.loc[move_df["Тип документа"] == "5.0. Списание (утилизация)", "Вид документа"] = "Утилизация"

        # 2. Условие для "5.0. Списание (недостача)"
        move_df.loc[move_df["Тип документа"] == "5.0. Списание (недостача)", "Вид операции"] = "Списание со склада"
        move_df.loc[move_df["Тип документа"] == "5.0. Списание (недостача)", "Вид документа"] = "Недостача"

        # Расчет количества
        # Условие для "5.0. Списание (недостача)" или "5.0. Списание (утилизация)"
        condition = (move_df["Тип документа"] == "5.0. Списание (недостача)") | (move_df["Тип документа"] == "5.0. Списание (утилизация)")
        # Инициализация колонки "Количество"
        move_df["Количество"] = None
        # Условие 1: Если тип документа "5.0. Списание (недостача)" или "5.0. Списание (утилизация)", и "Приход" не пустой, а "Расход" пустой, то "Количество" = Приход * (-1)
        move_df.loc[condition & move_df["Приход"].notnull() & move_df["Расход"].isnull(), "Количество"] = move_df["Приход"] * (-1)
        # Условие 2: Если тип документа "5.0. Списание (недостача)" или "5.0. Списание (утилизация)", и "Расход" не пустой, а "Приход" пустой, то "Количество" = Расход
        move_df.loc[condition & move_df["Расход"].notnull() & move_df["Приход"].isnull(), "Количество"] = move_df["Расход"]
        # Условие 3: Если тип документа не "5.0. Списание (недостача)" или не "5.0. Списание (утилизация)", и "Приход" не пустой, а "Расход" пустой, то "Количество" = Приход
        move_df.loc[~condition & move_df["Приход"].notnull() & move_df["Расход"].isnull(), "Количество"] = move_df["Приход"]
        # Условие 4: Если тип документа не "5.0. Списание (недостача)" или не "5.0. Списание (утилизация)", и "Расход" не пустой, а "Приход" пустой, то "Количество" = Расход * (-1)
        move_df.loc[~condition & move_df["Расход"].notnull() & move_df["Приход"].isnull(), "Количество"] = move_df["Расход"] * (-1)
        
        # Фильтрация перемещений
        move_df = move_df[move_df["Тип документа"] != "3.0. Перемещение"]
        
        return move_df

    def _check_and_update_products(self, df):
        """Проверяет наличие продуктов в БД с возможностью обновления"""
        if df.empty:
            return df
            
        # Получаем список всех кодов материалов из БД
        try:
            existing_codes = {str(m[0]) for m in db.query(Materials.Code).all()}
        except Exception as e:
            self.show_error_message(f"Ошибка при проверке продуктов в БД: {str(e)}")
            return pd.DataFrame()
            
        # Находим отсутствующие коды (убеждаемся, что они строковые)
        df['Код'] = df['Код'].astype(str)
        missing_codes = set(df['Код'].unique()) - existing_codes
        
        if not missing_codes:
            return df
            
        # Фильтруем строки с отсутствующими продуктами
        missing_df = df[df['Код'].isin(missing_codes)]
        missing_products = missing_df[['Артикул', 'Код', 'Номенклатура']].drop_duplicates()
        
        # Формируем сообщение с информацией об отсутствующих продуктах
        msg = "Следующие продукты отсутствуют в БД:\n\n"
        msg += "\n".join(f"{row['Артикул']}, {row['Код']}, {row['Номенклатура']}" 
                        for _, row in missing_products.iterrows())
        msg += "\n\nЗапустить обновление продуктов?"
        
        # Показываем диалог с вопросом
        reply = QMessageBox.question(
            self, 
            "Отсутствующие продукты", 
            msg,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Запускаем обновление продуктов
            try:
                product_updater = ProductsPage()
                product_updater.upload_data()
                
                # Повторно проверяем наличие продуктов после обновления
                existing_codes = {str(m[0]) for m in db.query(Materials.Code).all()}
                still_missing = set(df['Код'].unique()) - existing_codes
                
                if still_missing:
                    # Формируем сообщение о продуктах, которые все еще отсутствуют
                    still_missing_df = df[df['Код'].isin(still_missing)]
                    still_missing_products = still_missing_df[['Артикул', 'Код', 'Номенклатура']].drop_duplicates()
                    
                    msg = "Следующие продукты все еще отсутствуют в БД и будут пропущены:\n\n"
                    msg += "\n".join(f"{row['Артикул']}, {row['Код']}, {row['Номенклатура']}" 
                                    for _, row in still_missing_products.iterrows())
                    self.show_message(msg)
                    
                    # Удаляем строки с отсутствующими продуктами
                    df = df[~df['Код'].isin(still_missing)]
            except Exception as e:
                self.show_error_message(f"Ошибка при обновлении продуктов: {str(e)}")
                return pd.DataFrame()
        else:
            # Пользователь отказался обновлять - просто удаляем отсутствующие продукты
            df = df[~df['Код'].isin(missing_codes)]
        
        return df

    def _check_purchases_in_add_suppl_cost(self, move_df):
        """Проверка наличия поступлений в AddSupplCost"""
        purchases = move_df[(move_df["Тип документа"] == "1.0. Поступление") & (move_df["Контрагент.Код"] != "ОП-001636")]
        
        if purchases.empty:
            return True  # Возвращаем True, если проверка прошла успешно
            
        # Проверяем наличие документов в AddSupplCost
        doc_dates = purchases[["Документ", "Дата", "Контрагент.Код", "Контрагент", "Комментарий"]].drop_duplicates()
        errors = []
        
        for _, row in doc_dates.iterrows():
            exists = db.query(AddSupplCost).filter(
                AddSupplCost.Document == row["Документ"],
                AddSupplCost.Date == row["Дата"],
                AddSupplCost.Supplier_id == row["Контрагент.Код"]
            ).first()
            
            if not exists:
                errors.append(row)
        
        if errors:
            error_df = pd.DataFrame(errors)
            error_df.to_excel("ERRORs_Purchase_new.xlsx", index=False)
            
            error_msg = "Найдены новые Поступления:\n\n"
            error_msg += "\n".join(
                f"{row['Документ']}, {row['Дата']}, {row['Контрагент.Код']}" 
                for _, row in error_df.iterrows()
            )
            error_msg += "\n\nОшибки сохранены в файл ERRORs_Purchase_new.xlsx"
            
            self.show_error_message(error_msg)
            return False  # Возвращаем False, если найдены ошибки
        
        return True  # Возвращаем True, если проверка прошла успешно

    def _update_moves_in_db(self, move_df, report_start_date):
        """Обновление данных Movements в БД с полной обработкой ошибок"""
        try:
            if move_df.empty:
                self.show_message("Нет данных для обновления")
                return
            
            move_df = self._clean_dataframe(move_df)
            move_df.to_excel('test_move.xlsx')
            db.query(Movements).filter(Movements.Date >= report_start_date).delete()

            # Получаем список существующих клиентов и поставщиков из БД
            existing_customers = {str(c[0]) for c in db.query(Customer.id).all()}
            existing_suppliers = {str(s[0]) for s in db.query(Supplier.id).all()}

            # Подготовка данных
            records = []
            skipped_details = []  # Детальная информация о пропущенных записях
            
            for idx, row in move_df.iterrows():
                try:
                    
                    record = {
                        'Date_Time': row.get('Дата_Время'),
                        'Document': row.get('Документ', ''),
                        'Date': row.get('Дата'),
                        'Doc_based': row.get('ДокОсн'),
                        'Date_Doc_based': row.get('Дата ДокОсн'),
                        'Stock': row.get('Склад', ''),
                        'Qty': row.get('Количество'),
                        'Recipient_code': row.get('Грузополучатель.Код'),
                        'Recipient': row.get('Грузополучатель'),
                        'Bill': row.get('Счет'),
                        'Bill_date': row.get('Дата счета'),
                        'DocType_id': self._get_doc_type_id(row.get('Вид документа', ''), row.get('Вид операции', ''), row.get('Тип документа', '')),
                        'Material_id': row.get('Код', '')
                    }

                    counterparty_code = row.get('Контрагент.Код')
                    doc_type = row.get('Тип документа')
                    document = row.get('Документ')
                    material = row.get('Код')
                    
                    if counterparty_code is None:
                        record['Supplier_id'] = None
                        record['Customer_id'] = None
                    else:
                        # Проверяем, кем является контрагент - клиентом или поставщиком
                        if counterparty_code in existing_suppliers:
                            record['Supplier_id'] = counterparty_code
                            record['Customer_id'] = None
                        elif counterparty_code in existing_customers:
                            record['Customer_id'] = counterparty_code
                            record['Supplier_id'] = None
                        else:
                            # Если код не найден ни у клиентов, ни у поставщиков
                            supplier_doc_types = [
                                "1.0. Поступление",
                                "1.0. Поступление (перераб)", 
                                "1.1. Поступление (корр-ка)",
                                "7.0. Передача в переработку",
                                '5.0. Списание (недостача)',
                                '5.0. Списание (утилизация)'
                            ]
                            
                            if doc_type in supplier_doc_types:
                                reason = f"Поставщик '{counterparty_code}' не существует в БД"
                            else:
                                reason = f"Клиент '{counterparty_code}' не существует в БД"
                                
                            skipped_details.append(f"Документ: {document}, Дата: {date}, Код: {material}, Причина: {reason}")
                            continue

                    records.append(record)
                except Exception as e:
                    document = row.get('Документ', 'N/A')
                    date = row.get('Дата', 'N/A')
                    material = row.get('Код', 'N/A')
                    reason = f"Ошибка обработки: {str(e)}"
                    skipped_details.append(f"Документ: {document}, Дата: {date}, Код: {material}, Причина: {reason}")
                    continue

            if records:
                db.bulk_insert_mappings(Movements, records)
                db.commit()
                
                # Формируем детальное сообщение
                msg = f"Успешно обновлено {len(records)} записей"
                
                if skipped_details:
                    skipped_count = len(skipped_details)
                    msg += f"\n\nПропущено {skipped_count} записей:\n"
                    msg += "\n".join(skipped_details[:10])  # Показываем первые 10 пропущенных
                    
                    if skipped_count > 10:
                        msg += f"\n... и еще {skipped_count - 10} записей"
                    
                    # Сохраняем полный список пропущенных записей в файл
                    try:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"skipped_records_{timestamp}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write("Пропущенные записи:\n")
                            f.write("\n".join(skipped_details))
                        msg += f"\n\nПолный список сохранен в файл: {filename}"
                    except Exception as e:
                        msg += f"\n\nНе удалось сохранить файл с пропущенными записями: {str(e)}"
                
                self.show_message(msg)
            else:
                if skipped_details:
                    msg = "Все записи пропущены. Причины:\n"
                    msg += "\n".join(skipped_details[:20])  # Показываем первые 20 причин
                    
                    if len(skipped_details) > 20:
                        msg += f"\n... и еще {len(skipped_details) - 20} записей"
                    
                    self.show_error_message(msg)
                else:
                    self.show_message("Нет корректных данных для вставки")

        except Exception as e:
            db.rollback()
            error_msg = f"Критическая ошибка: {str(e)}\n{traceback.format_exc()}"
            self.show_error_message(error_msg)
            raise Exception(error_msg)

    def _process_complectations(self, move_df, report_start_date):
        """Обработка данных о комплектациях - упрощенная версия"""
        try:
            # 1. Читаем данные из Excel файла
            dtype_compl = {"Артикул": str, "Упаковка": float, "Кол-во в упак": float, "Количество": float}
            excel_complect_df = pd.read_excel(Complectation_file, sheet_name="ручные компл", dtype=dtype_compl)
            
            # Обрабатываем данные из Excel
            excel_complect_df["Код"] = excel_complect_df["Код"].str.strip()
            excel_complect_df["Дата"] = pd.to_datetime(excel_complect_df["Дата"], format="%d.%m.%Y")
            excel_complect_df["Дата_Время"] = pd.to_datetime(excel_complect_df["Дата_Время"], format="%d.%m.%Y %H:%M:%S")
            excel_complect_df = excel_complect_df.drop(columns=["Вид упаковки", "Упаковка", "Кол-во в упак"], axis=1, errors="ignore")
            excel_complect_df = excel_complect_df[(excel_complect_df["Дата"] >= report_start_date)]
            
            # 2. Добавляем обязательные колонки
            excel_complect_df['Вид операции'] = 'Комплектация'
            excel_complect_df['Вид документа'] = 'Комплектация номенклатуры'
            
            # 3. Обновляем БД данными из Excel
            self._update_complects_manual_in_db(excel_complect_df, report_start_date)
            
            # 4. Добавляем данные из Excel в общий DataFrame движений
            move_df = pd.concat([move_df, excel_complect_df], axis=0, ignore_index=True)
            
            # 5. Обрабатываем автоматические комплектации
            complect_df = move_df[
                (move_df['Тип документа'] == '2.0. Комплектация') | 
                (move_df['Тип документа'] == '5.0. Списание') | 
                (move_df['Тип документа'] == '6.0. Расход')
            ]
            
            if not complect_df.empty:
                self._update_complects_in_db(complect_df, report_start_date)
            
            return move_df
            
        except Exception as e:
            self.show_error_message(f"Ошибка обработки комплектаций: {str(e)}")
            traceback.print_exc()
            return move_df

    def _update_complects_in_db(self, df, report_start_date):
        """Обновление данных о комплектациях в БД с защитой от ошибок"""
        try:
            if df.empty:
                return

            df = self._clean_dataframe(df)
            df.to_excel('test_complect.xlsx')
            db.query(Complects).filter(Complects.Date >= report_start_date).delete()

            # Подготавливаем данные для вставки
            records = []
            for _, row in df.iterrows():
                try:
                    record = {
                        'Date_Time':row.get('Date_Time'),
                        'Document': row['Документ'],
                        'Date': row['Дата'],
                        'Stock': row['Склад'],
                        'Qty': row['Количество'],
                        'DocType_id': self._get_doc_type_id(row.get('Вид документа', ''), row.get('Вид операции', ''), row.get('Тип документа', '')),
                        'Material_id': row['Код'],
                    }
                    records.append(record)
                except Exception as e:
                    print(f"Ошибка обработки строки: {e}\nДанные: {row.to_dict()}")
                    continue
            
            # Вставляем данные порциями по 500 записей
            for i in range(0, len(records), 500):
                try:
                    db.bulk_insert_mappings(Complects, records[i:i+500])
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"Ошибка вставки записей {i}-{i+500}: {str(e)}")
                    traceback.print_exc()
                    
        except Exception as e:
            db.rollback()
            error_msg = f"Ошибка обновления данных Complects в БД: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            raise Exception(error_msg)

    def _update_complects_manual_in_db(self, df, report_start_date):
        """Обновление данных о ручных комплектациях в БД"""
        try:
            df = self._clean_dataframe(df)
            
            df['Вид операции'] = 'Комплектация'
            df['Вид документа'] = 'Комплектация номенклатуры'
            
            df.to_excel('test_complect_man.xlsx')
            
            db.query(Complects_manual).filter(Complects_manual.Date >= report_start_date).delete()
            
            # Подготавливаем данные для вставки
            records = []
            for _, row in df.iterrows():
                try:
                    doc_type_id = self._get_doc_type_id(
                        row.get('Вид документа', ''), 
                        row.get('Вид операции', ''), 
                        row.get('Тип документа', '')
                    )
                    
                    record = {
                        'Date_Time': self._safe_datetime(row.get('Дата_Время')),
                        'Document': row['Документ'],
                        'Date': row['Дата'],
                        'Stock': row['Склад'],
                        'Qty': row['Количество'],
                        'DocType_id': doc_type_id,
                        'Material_id': row['Код'],
                    }
                    records.append(record)
                except Exception as e:
                    print(f"Ошибка обработки строки: {e}")
                    continue
            
            # Массовая вставка
            if records:
                db.bulk_insert_mappings(Complects_manual, records)
                db.commit()
                
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления данных Complects_manual в БД: {e}")
    
    def _process_write_offs(self, move_df, report_start_date):
        """Обработка списаний с правильной последовательностью операций"""
        try:
            # Получаем дату начала отчета из интерфейса
            report_start_date = self.ui.date_Start.date().toPython()
            report_start_date = pd.to_datetime(report_start_date)
            
            # 1. Чтение данных из файла списаний
            dtype_compl = {
                "Артикул": str, 
                "Упаковка": float, 
                "Кол-во в упак": float, 
                "Количество": float
            }
            write_off_df = pd.read_excel(Complectation_file, sheet_name="Недостачи_Утилизации", dtype=dtype_compl)
            
            # Проверка обязательных колонок
            required_columns = ['Документ', 'Дата', 'Код', 'Склад', 'Отчет', 'Тип документа']
            for col in required_columns:
                if col not in write_off_df.columns:
                    raise ValueError(f"Отсутствует обязательная колонка: {col}")
            
            # 2. Подготовка данных из файла
            write_off_df = write_off_df.rename(columns={'Order N': 'Order', 'Shipment #': 'Shipment'})
            write_off_df["Код"] = write_off_df["Код"].str.strip()
            write_off_df["Дата"] = pd.to_datetime(write_off_df["Дата"], format="%d.%m.%Y")
            write_off_df["Дата_Время"] = pd.to_datetime(write_off_df["Дата_Время"], format="%d.%m.%Y %H:%M:%S")
            write_off_df["merge2"] = (
                write_off_df["Документ"] + "_" + 
                write_off_df["Дата"].astype(str) + "_" + 
                write_off_df["Код"] + "_" + 
                write_off_df["Склад"]
            )
            write_off_df["CHECK_write_off"] = "yes"
            
            write_off_for_db = write_off_df.copy()
            # 3. Фильтрация данных для БД
            optional_columns = {
                'ДокОсн': '',
                'Дата ДокОсн': None,
                'Order N': '',
                'Shipment #': '',
                'Вход. док-т': '',
                'Счет': '',
                'Дата счета': None,
                'Комментарий': ''
            }
            
            for col, default in optional_columns.items():
                if col not in write_off_for_db.columns:
                    write_off_for_db[col] = default
            
            # Обновление БД
            if not write_off_for_db.empty:
                self._update_write_off_in_db(write_off_for_db, report_start_date)
            
            # 5. Подготовка данных для проверки новых списаний
            write_off_for_check = write_off_df[["merge2", "CHECK_write_off"]].drop_duplicates()
            
            # 6. Фильтрация move_df - исключаем уже проверенные списания
            move_df["merge2"] = (
                move_df["Документ"] + "_" + 
                move_df["Дата"].astype(str) + "_" + 
                move_df["Код"] + "_" + 
                move_df["Склад"]
            )
            move_df = move_df.merge(write_off_for_check, on="merge2", how="left")
            move_df["CHECK_write_off"] = move_df["CHECK_write_off"].fillna("no")
            move_df = move_df[move_df["CHECK_write_off"] != "yes"]
            
            # 7. Добавление подтвержденных списаний обратно в move_df
            write_off_df2 = write_off_df[
                (write_off_df["Отчет"] == "да") & 
                (write_off_df["Тип документа"] != "2.0. Комплектация") &
                (write_off_df["Дата"] >= report_start_date)
            ]
    
            if not write_off_df2.empty:
                move_df = pd.concat([move_df, write_off_df2], axis=0, ignore_index=True)
                
            
            # 8. Поиск новых списаний для сохранения в Excel
            write_off_mask = (
                (move_df["Склад"].str.contains("Недостача|Утилизация", na=False)) & 
                (~move_df["Тип документа"].isin(["2.0. Комплектация", "4.0. Реализация"])) &
                (move_df["CHECK_write_off"] == "no")
            )
            new_write_offs = move_df[write_off_mask].copy()
            
            if not new_write_offs.empty:
                try:
                    # Получаем уникальные коды материалов из DataFrame
                    material_codes = move_df['Код'].unique().tolist()
                    
                    # Запрашиваем дополнительные данные из БД
                    materials_data = db.query(
                        Materials.Code,
                        Materials.Article,
                        Materials.Package_type,
                        Materials.Items_per_Package,
                        Materials.Package_Volume,
                        Materials.UoM,
                        Product_Names.Product_name
                    ).join(Materials.product_name
                    ).filter(Materials.Code.in_(material_codes)
                    ).all()
                    
                    # Создаём словарь для быстрого доступа к данным по коду материала
                    materials_dict = {
                        m.Code: {
                            'Артикул': m.Article,
                            'Продукт + упаковка': m.Product_name,
                            'Вид упаковки': m.Package_type,
                            'Упаковка': m.Package_Volume,
                            'Кол-во в упак': m.Items_per_Package,
                            'Единица измерения': m.UoM
                        }
                        for m in materials_data
                    }
                    
                    # Добавляем недостающие колонки в DataFrame
                    for code, data in materials_dict.items():
                        mask = new_write_offs['Код'] == code
                        for col_name, value in data.items():
                            try:
                                new_write_offs.loc[mask, col_name] = pd.to_numeric(value)
                            except (ValueError, TypeError):
                                new_write_offs.loc[mask, col_name] = value
                    
                    # Рассчитываем дополнительные колонки
                    new_write_offs['Кол-во, шт'] = new_write_offs.apply(lambda row: self._calculate_pcs(row.to_dict()), axis=1)
                    new_write_offs['Кол-во в л прод'] = new_write_offs.apply(lambda row: self._calculate_liters(row.to_dict()), axis=1)
                    
                    new_write_offs = new_write_offs[[ "Дата_Время", "Документ", "Дата", "Вид операции", "Вид документа", "Код", "Артикул", "Продукт + упаковка", "Вид упаковки", "Упаковка", 
                                                                        "Кол-во в упак", "Единица измерения", "Склад", "Комментарий", "Приход", "Расход", "Количество", "Тип документа", 
                                                                        "Контрагент.Код", "Контрагент", "Грузополучатель.Код", "Грузополучатель", "Счет", "Дата счета", "CHECK_write_off" ]]
                    new_write_offs.to_excel("ERRORs_Write_OFF_new.xlsx", index=False)
                    self.show_message(
                        f"Найдено {len(new_write_offs)} новых списаний\n"
                        "Сохранено в ERRORs_Write_OFF_new.xlsx"
                    )
                except Exception as e:
                    self.show_error_message(f"Ошибка при записи данных в Excel: {str(e)}")
                    traceback.print_exc()
                    
            return move_df.drop(columns=["merge2", "CHECK_write_off"], errors="ignore")
            
        except Exception as e:
            self.show_error_message(f"Ошибка обработки списаний: {str(e)}")
            traceback.print_exc()
            return move_df

    def _update_write_off_in_db(self, write_off_df, report_start_date):
        """Обновление данных WriteOff в БД с проверкой всех колонок и обработкой NaN"""
        try:
            # Проверяем, что DataFrame не пустой
            if write_off_df.empty:
                self.show_message("Нет данных для обновления в таблице WriteOff")
                return

            write_off_df = self._clean_dataframe(write_off_df)
            
            db.query(WriteOff).filter(WriteOff.Date >= report_start_date).delete()

            # Подготавливаем данные для вставки
            records = []
            for _, row in write_off_df.iterrows():
                try:
                    # Создаем запись с проверкой наличия всех полей
                    record = {
                        'Date_Time': row.get('Date_Time'),
                        'Document': row.get('Документ', ''),
                        'Date': row.get('Дата'),
                        'Stock': row.get('Склад', ''),
                        'Comment': row.get('Комментарий'),
                        'inComing': self._safe_float(row.get('Приход')),
                        'outComing': self._safe_float(row.get('Расход')),
                        'Qty': self._safe_float(row.get('Количество')),
                        'Reporting': row.get('Отчет', 'нет'),
                        'Doc_based': row.get('ДокОсн', None),
                        'Date_Doc_based': row.get('Дата ДокОсн'),
                        'Order': row.get('Order N', row.get('Order')),
                        'Shipment': row.get('Shipment #', row.get('Shipment', None)),
                        'Suppl_Inv_N': row.get('Вход. док-т'),
                        'Bill': row.get('Счет'),
                        'Bill_date': row.get('Дата счета'),
                        'DocType_id': self._get_doc_type_id(row.get('Вид документа', ''), row.get('Вид операции', ''), row.get('Тип документа', '')),
                        'Material_id': row.get('Код'),
                        'Supplier_id': row.get('Контрагент.Код')
                    }

                    records.append(record)
                except Exception as row_error:
                    error_msg = f"Ошибка обработки строки: {row_error}\nДанные строки: {row.to_dict()}"
                    self.show_error_message(error_msg)
                    continue

            # Массовая вставка
            if records:
                db.bulk_insert_mappings(WriteOff, records)
                db.commit()

        except Exception as e:
            db.rollback()
            error_msg = f"Ошибка обновления данных WriteOff в БД: {str(e)}\n{traceback.format_exc()}"
            self.show_error_message(error_msg)
            raise Exception(error_msg)

    def _write_final_data_to_excel(self, move_df):
        """Запись финальных данных в Excel с подтягиванием данных из БД и расчётом колонок"""
        try:
            # Получаем уникальные коды материалов из DataFrame
            material_codes = move_df['Код'].unique().tolist()
            
            # Запрашиваем дополнительные данные из БД
            materials_data = db.query(
                Materials.Code,
                Materials.Article,
                Materials.Package_type,
                Materials.Items_per_Package,
                Materials.Package_Volume,
                Materials.UoM,
                Product_Names.Product_name
            ).join(Materials.product_name
            ).filter(Materials.Code.in_(material_codes)
            ).all()
            
            # Создаём словарь для быстрого доступа к данным по коду материала
            materials_dict = {
                m.Code: {
                    'Артикул': m.Article,
                    'Продукт + упаковка': m.Product_name,
                    'Вид упаковки': m.Package_type,
                    'Упаковка': self.convert_decimal_to_float(m.Package_Volume),
                    'Кол-во в упак': self.convert_decimal_to_float(m.Items_per_Package),
                    'Единица измерения': m.UoM
                }
                for m in materials_data
            }
                
            # Добавляем недостающие колонки в DataFrame
            for code, data in materials_dict.items():
                mask = move_df['Код'] == code
                for col_name, value in data.items():
                    if col_name in ['Артикул', 'Продукт + упаковка', 'Вид упаковки', 'Единица измерения']:
                        move_df.loc[mask, col_name] = str(value) if value is not None else ''
                    else:
                        move_df.loc[mask, col_name] = float(value) if value is not None else 0.0
            
            # Рассчитываем дополнительные колонки
            move_df['Кол-во, шт'] = move_df.apply(lambda row: self._calculate_pcs(row.to_dict()), axis=1)
            move_df['Кол-во в л прод'] = move_df.apply(lambda row: self._calculate_liters(row.to_dict()), axis=1)

            # Подготовка финальных данных для записи
            move_full_to_write = move_df[[
                "Дата_Время", "Документ", "Дата", "Вид операции", "Вид документа", "ДокОсн", "Дата ДокОсн", 
                "Тип документа", "Код", "Артикул", "Продукт + упаковка", "Вид упаковки", 
                "Упаковка", "Кол-во в упак", "Единица измерения", "Склад", "Количество", 
                "Кол-во, шт", "Кол-во в л прод", "Контрагент.Код", "Контрагент", 
                "Грузополучатель.Код", "Грузополучатель", "Счет", "Дата счета"]]

            # Запись движений
            self._write_prod_move(move_full_to_write)
            
            # Запись комплектаций
            complect_df = move_full_to_write[
                (move_full_to_write['Тип документа'] == '2.0. Комплектация') | 
                (move_full_to_write['Тип документа'] == '5.0. Списание') | 
                (move_full_to_write['Тип документа'] == '6.0. Расход') 
            ]
            self._write_complectations(complect_df)
            
        except Exception as e:
            self.show_error_message(f"Ошибка при записи данных в Excel: {str(e)}")
            traceback.print_exc()

    def _write_prod_move(self, movement_df):
        """Адаптированная версия функции write_prod_move для класса MovesPage"""
        try:
            sheetname = "Движения"
            cells_num = movement_df.shape[0] + 1
            
            with xw.App(add_book=False, visible=False) as app:
                wb = app.books.open(Complectation_file, update_links=False, read_only=False)
                ws = wb.sheets[sheetname]
                ws.api.AutoFilter.ShowAllData()
                num_col = ws.range("A1").end("right").column
                num_row = ws.range("A" + str(wb.sheets[sheetname].cells.last_cell.row)).end("up").row
                ws.range((2, 1), (num_row + 5, num_col)).delete()

                # Установка форматов ячеек
                ws.range("A2:A" + str(cells_num)).number_format = "ДД.ММ.ГГГГ чч:мм:сс"
                ws.range("C2:C" + str(cells_num)).number_format = "ДД.ММ.ГГГГ"
                ws.range("F2:F" + str(cells_num)).number_format = "ДД.ММ.ГГГГ"
                ws.range("I2:I" + str(cells_num)).number_format = "@"
                ws.range("L2:M" + str(cells_num)).number_format = "0"
                ws.range("P2:R" + str(cells_num)).number_format = "# ##0,00_ ;[Red]-# ##0,00_ ;\"\"-\"\""
                ws.range("T2:T" + str(cells_num)).number_format = "@"
                ws.range("U2:U" + str(cells_num)).number_format = "# ##0,0_ ;[Red]-# ##0,0_ ;\"\"-\"\""
                ws.range("Y2:Y" + str(cells_num)).number_format = "ДД.ММ.ГГГГ"
                
                # Запись данных
                ws.range((2, 1), (cells_num, num_col)).options(index=False, header=False).value = movement_df.values

                wb.save()
                wb.close()
                
        except Exception as e:
            raise Exception(f"Ошибка при записи движений в Excel: {str(e)}")

    def _write_complectations(self, movement_df):
        """Адаптированная версия функции write_complectations для класса MovesPage"""
        try:
            sheetname = "Комплектации"
            cells_num = movement_df.shape[0] + 1
            
            with xw.App(add_book=False, visible=False) as app:
                wb = app.books.open(Complectation_file, update_links=False, read_only=False)
                ws = wb.sheets[sheetname]
                ws.api.AutoFilter.ShowAllData()
                num_col = ws.range("A1").end("right").column
                num_row = ws.range("A" + str(wb.sheets[sheetname].cells.last_cell.row)).end("up").row
                ws.range((2, 1), (num_row + 5, num_col)).delete()

                # Установка форматов ячеек
                ws.range("A2:A" + str(cells_num)).number_format = "ДД.ММ.ГГГГ чч:мм:сс"
                ws.range("C2:C" + str(cells_num)).number_format = "ДД.ММ.ГГГГ"
                ws.range("F2:F" + str(cells_num)).number_format = "ДД.ММ.ГГГГ"
                ws.range("I2:I" + str(cells_num)).number_format = "@"
                ws.range("L2:M" + str(cells_num)).number_format = "0"
                ws.range("P2:R" + str(cells_num)).number_format = "# ##0,00_ ;[Red]-# ##0,00_ ;\"\"-\"\""
                ws.range("T2:T" + str(cells_num)).number_format = "@"
                ws.range("U2:U" + str(cells_num)).number_format = "# ##0,0_ ;[Red]-# ##0,0_ ;\"\"-\"\""
                ws.range("Y2:Y" + str(cells_num)).number_format = "ДД.ММ.ГГГГ"
                
                # Запись данных
                ws.range((2, 1), (cells_num, num_col)).options(index=False, header=False).value = movement_df.values

                wb.save()
                wb.close()
                
        except Exception as e:
            raise Exception(f"Ошибка при записи комплектаций в Excel: {str(e)}")

    @lru_cache(maxsize=128)
    def _get_doc_type_id(self, document: str, transaction: str, doc_type: str) -> int:
        """Получение ID типа документа с защитой от NaN и None значений"""
        try:
            # Обработка None и NaN значений
            document = None if document is None or str(document).lower() in ['none', 'nan', ''] else str(document)
            transaction = None if transaction is None or str(transaction).lower() in ['none', 'nan', ''] else str(transaction)
            doc_type = None if doc_type is None or str(doc_type).lower() in ['none', 'nan', ''] else str(doc_type)
            
            query = db.query(DOCType.id)
            
            # Добавляем условия в зависимости от наличия значений
            conditions = []
            if document is not None:
                conditions.append(DOCType.Document == document)
            else:
                conditions.append(DOCType.Document.is_(None))
                
            if transaction is not None:
                conditions.append(DOCType.Transaction == transaction)
            else:
                conditions.append(DOCType.Transaction.is_(None))
                
            if doc_type is not None:
                conditions.append(DOCType.Doc_type == doc_type)
                
            # Применяем все условия
            query = query.filter(*conditions)
            
            result = query.first()
            
            if result:
                return result[0]
            
            # Если запись не найдена, создаем новую (если требуется)
            if document or transaction or doc_type:
                try:
                    new_doc_type = DOCType(
                        Document=document,
                        Transaction=transaction,
                        Doc_type=doc_type
                    )
                    db.add(new_doc_type)
                    db.commit()
                    return new_doc_type.id
                except Exception:
                    db.rollback()
                    return None
                    
            return None
            
        except Exception as e:
            print(f"Ошибка при получении ID типа документа: {str(e)}")
            traceback.print_exc()
            db.rollback()
            return None

    def _get_model_for_table(self, table_name: str):
        """Возвращает модель SQLAlchemy по имени таблицы"""
        models = {
            "Движения": Movements,
            "Комплектации": Complects,
            "Комплектации Ручные": Complects_manual,
            "Списания": WriteOff
        }
        return models.get(table_name)
    
    def _safe_supplier_id(self, value):
        """Обрабатывает Supplier_id, заменяя NaN/None на NULL"""
        if pd.isna(value) or value is None or str(value).strip() in ['', 'nan', 'None']:
            return None
        return str(value).strip()
        
    def _safe_date(self, value):
        """Безопасное преобразование в date с обработкой некорректных значений"""
        if pd.isna(value) or value is None or str(value) in ['NaT', 'nan', 'None', '']:
            return None
        
        # Если значение уже является датой
        if isinstance(value, (datetime.date, pd.Timestamp)):
            if isinstance(value, pd.Timestamp):
                return value.date()
            return value
        
        # Если значение - строка, проверяем, является ли оно датой
        if isinstance(value, str):
            # Пропускаем явно не датовые значения
            if any(char in value for char in ['СЧ', 'ОП', 'НМ', '-', '/', '\\']):
                return None
            
            try:
                # Пробуем разные форматы дат
                for fmt in ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                    try:
                        return datetime.datetime.strptime(value, fmt).date()
                    except ValueError:
                        continue
                # Если ни один формат не подошел
                return None
            except (ValueError, TypeError):
                return None
        
        return None

    def _safe_datetime(self, value):
        """Безопасное преобразование в datetime с форматом 19.08.2025 10:57:21"""
        if pd.isna(value) or value is None or str(value) in ['NaT', 'nan', 'None', '']:
            return None
        
        # Если значение уже является datetime
        if isinstance(value, (datetime.datetime, pd.Timestamp)):
            return value
        
        # Если значение - строка, пытаемся распарсить
        if isinstance(value, str):
            try:
                # Убираем лишние пробелы
                value = value.strip()
                # Пробуем разные форматы
                for fmt in ['%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S', 
                        '%Y-%m-%d %H:%M', '%d.%m.%Y', '%Y-%m-%d']:
                    try:
                        return datetime.datetime.strptime(value, fmt)
                    except ValueError:
                        continue
            except (ValueError, TypeError):
                pass
        
        # Если значение - дата, добавляем время по умолчанию
        if isinstance(value, datetime.date):
            return datetime.datetime.combine(value, datetime.time(0, 0, 0))
        
        return None

    def _format_datetime_display(self, dt):
        """Форматирование datetime для отображения 19.08.2025 10:57:21"""
        if dt is None:
            return ""
        return dt.strftime("%d.%m.%Y %H:%M:%S")

    def _null_if_empty(self, value):
        """Преобразует пустые/некорректные значения в None"""
        if pd.isna(value) or value in ['', 'nan', 'None', 'NaT', None]:
            return None
        return str(value) if not isinstance(value, (int, float)) else value

    def _safe_float(self, value):
        """Безопасное преобразование в float с обработкой ошибок"""
        if pd.isna(value) or value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _is_valid_value(self, value):
        """Проверяет, что значение не пустое и не равно '-'"""
        return value is not None and str(value).strip() not in ["", "-"]

    def _extract_name(self, combined_value):
        """Извлекает имя из строки формата 'код - имя' или возвращает исходное значение"""
        if " - " in combined_value:
            return combined_value.split(" - ")[-1].strip()
        return combined_value.strip()

    def convert_decimal_to_float(self, value):
        """Безопасное преобразование Decimal в float"""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

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

    def _clean_dataframe(self, df):
        """
        Заменяет все NaN/NaT значения на None используя replace
        """
        if df.empty:
            return df
        
        cleaned_df = df.copy()
        cleaned_df = cleaned_df.replace([np.nan, pd.NaT], None)
        cleaned_df = cleaned_df.replace(['nan', 'NaN', 'NaT', 'NONE', ''], None)
        
        return cleaned_df



