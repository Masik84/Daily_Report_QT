import pandas as pd
import numpy as np
import os
import datetime
from sqlalchemy import extract
from PySide6.QtWidgets import QMessageBox, QHeaderView, QTableWidget, QMenu, QApplication, QTableWidgetItem, QWidget
from PySide6.QtCore import Qt, QDate
from functools import lru_cache
import traceback
import sys

from db import db
from models import (temp_Purchase, temp_Sales, temp_Orders, Purchase_Order, DOCType, Materials, 
        Customer, Supplier, Contract, Manager, Product_Names, Complects, Complects_manual, Holding, Marketplace, Hyundai_Dealer)
from config import Purchase_folder, Sales_folder, Orders_file, Reserve_file, Customer_file, Contract_file, AddCosts_File, CustDelivery_File, All_data_file
from wind.pages.temp_tables_ui import Ui_Form
from pages_functions.product import ProductsPage
from pages_functions.customer import CustomerPage

class TempTablesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.date_Start.setDate(QDate(2022, 1, 1))
        
        # self.ui.date_Start.dateChanged.connect(self.on_date_changed)
        # today = datetime.datetime.now()
        # if today.day > 5:
        #     target_date = QDate(today.year, today.month, 1)
        # else:
        #     # Получаем первый день прошлого месяца
        #     first_day_prev_month = today.replace(day=1) - datetime.timedelta(days=1)
        #     target_date = QDate(first_day_prev_month.year, first_day_prev_month.month, 1)

        # self.ui.date_Start.setDate(target_date)
        
        self._setup_ui()
        self._setup_connections()
        
        self.table_data_cache = {}
        self.current_table_data = None
        
        # Инициализация вместо полного обновления
        self._initialize_comboboxes()
    
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
        self.ui.line_customer.currentTextChanged.connect(self.on_customer_changed)
        self.ui.line_customer.currentTextChanged.connect(self.on_supplier_changed)
        
        self.ui.btn_find.clicked.connect(self.find_temp_data)
        self.ui.btn_refresh.clicked.connect(self.upload_data)
        
    def show_context_menu(self, position):
        """Показ контекстного меню для копирования"""
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        copy_action.triggered.connect(self.copy_cell_content)
        menu.exec_(self.table.viewport().mapToGlobal(position))
    
    def copy_content(self):
        """Копирование содержимого в зависимости от выделения"""
        selected_ranges = self.table.selectedRanges()

        if not selected_ranges:
            return  # Ничего не выделено

        # Проверяем, выделена ли полностью строка
        if self.table.selectionBehavior() == QTableWidget.SelectRows:
            row = self.table.currentRow()
            if row >= 0:
                row_values = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item is not None:
                        row_values.append(item.text())
                    else:
                        row_values.append("")
                text_to_copy = "\t".join(row_values) #Табуляция между значениями
        else: # Выделена ячейка или несколько ячеек
            selected_items = self.table.selectedItems()
            if selected_items:
                text_to_copy = selected_items[0].text() #Копируем только первую выделенную ячейку
            else:
                return

        # Копируем текст в буфер обмена
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)
    
    def _fill_combobox(self, combobox, items):
        """Заполнение выпадающего списка элементами с обязательным первым элементом '-'"""
        current_text = combobox.currentText()
        
        # Всегда добавляем "-" первым элементом
        if "-" not in items:
            items = ["-"] + items
        else:
            # Если "-" уже есть в списке, перемещаем его на первое место
            items = ["-"] + [item for item in items if item != "-"]
        
        combobox.clear()
        combobox.addItems(items)
        
        # Пытаемся восстановить предыдущее значение, если оно есть в новом списке
        if current_text in items:
            combobox.setCurrentText(current_text)
        else:
            combobox.setCurrentIndex(0)  # Устанавливаем на "-"

    def _initialize_comboboxes(self):
        """Инициализация комбобоксов без загрузки данных"""
        models = {
            "Закупки": temp_Purchase,
            "Продажи": temp_Sales,
            "Заказы клиентов": temp_Orders,
            "Заказы поставщиков": Purchase_Order
        }
        self._fill_combobox(self.ui.line_table, ["-"] + list(models.keys()))
        
        # Очищаем остальные комбобоксы
        self._fill_combobox(self.ui.line_doc_type, ["-"])
        self._fill_combobox(self.ui.line_Year, ["-"])
        self._fill_combobox(self.ui.line_Mnth, ["-"])
        self._fill_combobox(self.ui.line_customer, ["-"])
        self._fill_combobox(self.ui.line_product, ["-"])
    
    def _update_comboboxes_from_cache(self):
        """Обновление комбобоксов из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])
            return
        
        df = self.current_table_data
        
        # Обновляем год и месяц
        self.fill_year_list()
        self.fill_month_list()
        
        # Обновляем тип документа
        self.fill_doc_type_list()
        
        # Обновляем клиента/поставщика в зависимости от типа таблицы
        table = self.ui.line_table.currentText()
        if table in ["Продажи", "Заказы клиентов"]:
            self.fill_customer_list()
        elif table in ["Закупки", "Заказы поставщиков"]:
            self.fill_supplier_list()
        
        # Обновляем продукт
        self.fill_product_list()
    
    def fill_year_list(self):
        """Заполнение списка годов из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_Year, ["-"])
            return
        
        df = self.current_table_data
        if 'Date' not in df.columns:
            self._fill_combobox(self.ui.line_Year, ["-"])
            return
        
        years = df['Date'].dropna().apply(lambda x: x.year).unique()
        years_list = sorted([str(int(y)) for y in years if y is not None])
        self._fill_combobox(self.ui.line_Year, ["-"] + years_list)

    def fill_month_list(self):
        """Заполнение списка месяцев из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            return
        
        df = self.current_table_data
        if 'Date' not in df.columns:
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            return
        
        months = df['Date'].dropna().apply(lambda x: x.month).unique()
        months_list = sorted([str(int(m)) for m in months if m is not None])
        self._fill_combobox(self.ui.line_Mnth, ["-"] + months_list)

    def fill_doc_type_list(self):
        """Заполнение списка типов документов из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            return
        
        try:
            df = self.current_table_data
            if 'DocType_id' not in df.columns:
                self._fill_combobox(self.ui.line_doc_type, ["-"])
                return
            
            # Преобразуем numpy.int64 в обычные Python int
            doc_type_ids = df['DocType_id'].dropna().unique()
            doc_type_ids = [int(id) for id in doc_type_ids]  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            
            if len(doc_type_ids) == 0:
                self._fill_combobox(self.ui.line_doc_type, ["-"])
                return
            
            # Получаем соответствующие типы документов из БД
            doc_types = db.query(DOCType.Doc_type).filter(DOCType.id.in_(doc_type_ids)).distinct().all()
            doc_types_list = sorted([d[0] for d in doc_types if d[0] is not None])
            
            self._fill_combobox(self.ui.line_doc_type, ["-"] + doc_types_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка типов документов: {str(e)}")
            self._fill_combobox(self.ui.line_doc_type, ["-"])

    def fill_customer_list(self):
        """Заполнение списка клиентов из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_customer, ["-"])
            return
        
        try:
            df = self.current_table_data
            if 'Customer_id' not in df.columns:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
            
            # Преобразуем numpy типы в строки
            customer_ids = df['Customer_id'].dropna().unique()
            customer_ids = [str(id) for id in customer_ids]  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            
            if len(customer_ids) == 0:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
            
            # Получаем названия клиентов из БД
            customers = db.query(Customer.id, Customer.Customer_name).filter(
                Customer.id.in_(customer_ids)
            ).distinct().all()
            
            customers_list = sorted([f"{c.id} - {c.Customer_name}" for c in customers if c.Customer_name])
            self._fill_combobox(self.ui.line_customer, ["-"] + customers_list)
            
        except Exception as e:
            self._fill_combobox(self.ui.line_customer, ["-"])

    def fill_supplier_list(self):
        """Заполнение списка поставщиков из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_customer, ["-"])
            return
        
        try:
            df = self.current_table_data
            if 'Supplier_id' not in df.columns:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
            
            # Преобразуем numpy типы в строки
            supplier_ids = df['Supplier_id'].dropna().unique()
            supplier_ids = [str(id) for id in supplier_ids]  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            
            if len(supplier_ids) == 0:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
            
            # Получаем названия поставщиков из БД
            suppliers = db.query(Supplier.id, Supplier.Supplier_Name).filter(
                Supplier.id.in_(supplier_ids)
            ).distinct().all()
            
            suppliers_list = sorted([f"{s.id} - {s.Supplier_Name}" for s in suppliers if s.Supplier_Name])
            self._fill_combobox(self.ui.line_customer, ["-"] + suppliers_list)
            
        except Exception as e:
            self._fill_combobox(self.ui.line_customer, ["-"])

    def fill_product_list(self):
        """Заполнение списка продуктов из кэшированных данных"""
        if self.current_table_data is None or self.current_table_data.empty:
            self._fill_combobox(self.ui.line_product, ["-"])
            return
        
        try:
            df = self.current_table_data
            if 'Material_id' not in df.columns:
                self._fill_combobox(self.ui.line_product, ["-"])
                return
            
            # Преобразуем numpy типы в строки
            material_ids = df['Material_id'].dropna().unique()
            material_ids = [str(id) for id in material_ids]  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
            
            if len(material_ids) == 0:
                self._fill_combobox(self.ui.line_product, ["-"])
                return
            
            # Получаем названия продуктов из БД
            products = db.query(
                Materials.Code, 
                Product_Names.Product_name
            ).join(
                Materials.product_name
            ).filter(
                Materials.Code.in_(material_ids)
            ).distinct().all()
            
            products_list = sorted([p.Product_name for p in products if p.Product_name])
            self._fill_combobox(self.ui.line_product, ["-"] + products_list)
            
        except Exception as e:
            self._fill_combobox(self.ui.line_product, ["-"])

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков с кэшированием данных"""
        table = self.ui.line_table.currentText()
        
        # Всегда обновляем список таблиц
        models = {
            "Закупки": temp_Purchase,
            "Продажи": temp_Sales,
            "Заказы клиентов": temp_Orders,
            "Заказы поставщиков": Purchase_Order
        }
        self._fill_combobox(self.ui.line_table, list(models.keys()))
        
        if table == "-":
            # Если таблица не выбрана, очищаем остальные комбобоксы
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])
            return
        
        # Если данные уже в кэше - используем их
        if table in self.table_data_cache:
            df = self.table_data_cache[table]
            self.current_table_data = df
            
            # Обновляем комбобоксы из кэшированных данных
            self.fill_year_list()
            self.fill_month_list()
            self.fill_doc_type_list()
            
            # Обновляем список клиентов/поставщиков в зависимости от типа таблицы
            if table in ["Продажи", "Заказы клиентов"]:
                self.fill_customer_list()
            elif table in ["Закупки", "Заказы поставщиков"]:
                self.fill_supplier_list()
            
            self.fill_product_list()
            return
        
        # Если нет в кэше - загружаем из БД один раз
        try:
            model = self._get_model_for_table(table)
            if not model:
                return
                
            # Загружаем минимальные данные таблицы в DataFrame
            query = db.query(
                model.Date,
                model.DocType_id,
                model.Customer_id if hasattr(model, 'Customer_id') else None,
                model.Supplier_id if hasattr(model, 'Supplier_id') else None,
                model.Material_id
            )
            
            # Преобразуем в DataFrame
            data = []
            for row in query.all():
                row_data = {
                    'Date': row.Date,
                    'DocType_id': row.DocType_id
                }
                if hasattr(row, 'Customer_id') and row.Customer_id:
                    row_data['Customer_id'] = row.Customer_id
                if hasattr(row, 'Supplier_id') and row.Supplier_id:
                    row_data['Supplier_id'] = row.Supplier_id
                if hasattr(row, 'Material_id') and row.Material_id:
                    row_data['Material_id'] = row.Material_id
                data.append(row_data)
            
            df = pd.DataFrame(data)
            
            # Сохраняем в кэш
            self.table_data_cache[table] = df
            self.current_table_data = df
            
            # Обновляем комбобоксы из DataFrame
            self.fill_year_list()
            self.fill_month_list()
            self.fill_doc_type_list()
            
            # Обновляем список клиентов/поставщиков в зависимости от типа таблицы
            if table in ["Продажи", "Заказы клиентов"]:
                self.fill_customer_list()
            elif table in ["Закупки", "Заказы поставщиков"]:
                self.fill_supplier_list()
            
            self.fill_product_list()
            
        except Exception as e:
            print(f"Ошибка при загрузке данных таблицы: {str(e)}")
            # В случае ошибки очищаем комбобоксы
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])

    def on_table_changed(self):
        """Обработчик изменения таблицы - с кэшированием данных"""
        table = self.ui.line_table.currentText()
        if table == "-":
            self.current_table_data = None
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])
            return
        
        # Если данные уже в кэше - используем их
        if table in self.table_data_cache:
            self.current_table_data = self.table_data_cache[table]
            self._update_comboboxes_from_cache()  # Этот метод должен обновлять из кэша
            return
        
        # Если нет в кэше - загружаем из БД один раз
        try:
            model = self._get_model_for_table(table)
            if not model:
                return
                
            # Загружаем минимальные данные таблицы в DataFrame
            query = db.query(
                model.Date,
                model.DocType_id,
                model.Customer_id if hasattr(model, 'Customer_id') else None,
                model.Supplier_id if hasattr(model, 'Supplier_id') else None,
                model.Material_id
            )
            
            # Преобразуем в DataFrame
            data = []
            for row in query.all():
                row_data = {
                    'Date': row.Date,
                    'DocType_id': row.DocType_id
                }
                if hasattr(row, 'Customer_id') and row.Customer_id:
                    row_data['Customer_id'] = row.Customer_id
                if hasattr(row, 'Supplier_id') and row.Supplier_id:
                    row_data['Supplier_id'] = row.Supplier_id
                if hasattr(row, 'Material_id') and row.Material_id:
                    row_data['Material_id'] = row.Material_id
                data.append(row_data)
            
            df = pd.DataFrame(data)
            
            # Сохраняем в кэш
            self.table_data_cache[table] = df
            self.current_table_data = df
            
            # Обновляем комбобоксы из DataFrame
            self._update_comboboxes_from_cache()  # Этот метод должен обновлять из кэша
            
        except Exception as e:
            print(f"Ошибка при загрузке данных таблицы: {str(e)}")
            self.current_table_data = None

    def on_doc_type_changed(self):
        """Обработчик изменения типа документа"""
        self.fill_year_list()
        self.fill_month_list()
        self.fill_customer_list()
        self.fill_supplier_list()
        self.fill_product_list()

    def on_year_changed(self):
        """Обработчик изменения года"""
        self.fill_month_list()
        self.fill_customer_list()
        self.fill_supplier_list()
        self.fill_product_list()

    def on_month_changed(self):
        """Обработчик изменения месяца"""
        self.fill_customer_list()
        self.fill_supplier_list()
        self.fill_product_list()

    def on_customer_changed(self):
        """Обработчик изменения клиента"""
        self.fill_product_list()

    def on_supplier_changed(self):
        """Обработчик изменения поставщика"""
        self.fill_product_list()

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков с кэшированием данных"""
        table = self.ui.line_table.currentText()
        
        # Всегда обновляем список таблиц
        models = {
            "Закупки": temp_Purchase,
            "Продажи": temp_Sales,
            "Заказы клиентов": temp_Orders,
            "Заказы поставщиков": Purchase_Order
        }
        self._fill_combobox(self.ui.line_table, list(models.keys()))
        
        if table == "-":
            # Если таблица не выбрана, очищаем остальные комбобоксы
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])
            return
        
        # Если данные уже в кэше - используем их
        if table in self.table_data_cache:
            df = self.table_data_cache[table]
            self.current_table_data = df
            
            # Обновляем комбобоксы из кэшированных данных
            self.fill_year_list()
            self.fill_month_list()
            self.fill_doc_type_list()
            
            # Обновляем список клиентов/поставщиков в зависимости от типа таблицы
            if table in ["Продажи", "Заказы клиентов"]:
                self.fill_customer_list()
            elif table in ["Закупки", "Заказы поставщиков"]:
                self.fill_supplier_list()
            
            self.fill_product_list()
            return
        
        # Если нет в кэше - загружаем из БД один раз
        try:
            model = self._get_model_for_table(table)
            if not model:
                return
                
            # Загружаем минимальные данные таблицы в DataFrame
            query = db.query(
                model.Date,
                model.DocType_id,
                model.Customer_id if hasattr(model, 'Customer_id') else None,
                model.Supplier_id if hasattr(model, 'Supplier_id') else None,
                model.Material_id
            )
            
            # Преобразуем в DataFrame
            data = []
            for row in query.all():
                row_data = {
                    'Date': row.Date,
                    'DocType_id': row.DocType_id
                }
                if hasattr(row, 'Customer_id') and row.Customer_id:
                    row_data['Customer_id'] = row.Customer_id
                if hasattr(row, 'Supplier_id') and row.Supplier_id:
                    row_data['Supplier_id'] = row.Supplier_id
                if hasattr(row, 'Material_id') and row.Material_id:
                    row_data['Material_id'] = row.Material_id
                data.append(row_data)
            
            df = pd.DataFrame(data)
            
            # Сохраняем в кэш
            self.table_data_cache[table] = df
            self.current_table_data = df
            
            # Обновляем комбобоксы из DataFrame
            self.fill_year_list()
            self.fill_month_list()
            self.fill_doc_type_list()
            
            # Обновляем список клиентов/поставщиков в зависимости от типа таблицы
            if table in ["Продажи", "Заказы клиентов"]:
                self.fill_customer_list()
            elif table in ["Закупки", "Заказы поставщиков"]:
                self.fill_supplier_list()
            
            self.fill_product_list()
            
        except Exception as e:
            print(f"Ошибка при загрузке данных таблицы: {str(e)}")
            # В случае ошибки очищаем комбобоксы
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])

    def find_temp_data(self):
        """Поиск данных по заданным критериям с улучшенной обработкой"""
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
                total_count = db.query(model).count()
                self.show_message(f"Данные не найдены с текущими фильтрами.\nВсего записей в таблице: {total_count}")
                return
            
            # Преобразуем результат в DataFrame
            data = []
            for row in result:
                row_data = {}
                
                # Базовые поля модели
                for column in model.__table__.columns:
                    value = getattr(row, column.name)
                    if isinstance(value, datetime.date):
                        value = value.strftime("%d.%m.%Y") if value else ""
                    elif isinstance(value, float):
                        value = round(value, 2)
                    row_data[column.name] = value
                
                # Добавляем связанные данные
                if hasattr(row, 'material') and row.material:
                    row_data['Артикул'] = row.material.Article
                    row_data['Продукт + упаковка'] = row.material.product_name.Product_name if row.material.product_name else ""
                    row_data['Упаковка'] = row.material.Package_Volume if row.material.Package_Volume else 0
                    row_data['Кол-во в упак'] = row.material.Items_per_Package if row.material.Items_per_Package else 1
                    row_data['Единица измерения'] = row.material.UoM if row.material.UoM else ""
                    row_data['Вид упаковки'] = row.material.Package_type if row.material.Package_type else ""
                    row_data['Type'] = row.material.Product_type if row.material.Product_type else ""
                    row_data['Шт в комплекте'] = row.material.Items_per_Set if row.material.Items_per_Set else 1
                
                # ВАЖНО: Добавляем правильные названия контрагентов
                if hasattr(row, 'customer') and row.customer:
                    row_data['Контрагент.Код'] = row.customer.id
                    row_data['Контрагент'] = row.customer.Customer_name
                    row_data['Customer_Name'] = row.customer.Customer_name  # Добавляем для унификации
                
                if hasattr(row, 'supplier') and row.supplier:
                    row_data['Поставщик.Код'] = row.supplier.id
                    row_data['Поставщик'] = row.supplier.Supplier_Name
                    row_data['Supplier_Name'] = row.supplier.Supplier_Name  # Добавляем для унификации
                
                if hasattr(row, 'doc_type') and row.doc_type:
                    row_data['Тип документа'] = row.doc_type.Doc_type
                
                # Вычисляем Кол-во, шт и Кол-во, л если нужно
                if 'Qty' in row_data and 'Упаковка' in row_data:
                    # Защита от деления на ноль
                    packaging = float(row_data['Упаковка']) if row_data['Упаковка'] else 1.0
                    qty = float(row_data['Qty']) if row_data['Qty'] else 0.0
                    
                    # Условия для расчета количества в штуках
                    conditions_quantity = [
                        row_data.get('Type') == 'Услуги',
                        row_data.get('Вид упаковки') == 'комплект',
                        row_data.get('Единица измерения') == 'шт',
                        row_data.get('Единица измерения') == 'л',
                        row_data.get('Единица измерения') == 'кг',
                        row_data.get('Единица измерения') == 'т'
                    ]

                    choices_quantity = [
                        0,  # Для услуг
                        qty * float(row_data.get('Шт в комплекте', 1)),  # Для комплектов
                        qty,  # Для штук
                        qty / packaging if packaging != 0 else 0,  # Для литров
                        qty / packaging if packaging != 0 else 0,  # Для килограммов
                        round(qty * 1000 / packaging, 0) if packaging != 0 else 0  # Для тонн
                    ]

                    # Вычисляем количество в штуках
                    qty_pcs_result = np.select(conditions_quantity, choices_quantity, default=qty)
                    # Преобразуем numpy array в скалярное значение
                    qty_pcs = float(qty_pcs_result) if hasattr(qty_pcs_result, '__len__') else qty_pcs_result
                    
                    # Вычисляем количество в литрах
                    if row_data.get('Единица измерения') == 'л':
                        qty_liters = qty
                    elif row_data.get('Единица измерения') == 'кг':
                        qty_liters = qty  # Предполагаем эквивалентность
                    elif row_data.get('Единица измерения') == 'т':
                        qty_liters = qty * 1000
                    else:
                        qty_liters = qty_pcs * packaging

                    row_data['Кол-во, шт'] = qty_pcs
                    row_data['Кол-во, л'] = qty_liters

                data.append(row_data)
            
            df = pd.DataFrame(data)
            
            # Безопасное преобразование числовых колонок
            numeric_columns = ['Qty', 'Упаковка', 'Кол-во, шт', 'Кол-во, л']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            if df.empty:
                self.show_message("Данные не найдены")
                return
            
            # Отображаем данные в таблице
            self._display_data(df)
            
            # Обновляем сводную информацию
            self._update_summary(df, model)
            
        except Exception as e:
            error_msg = f"Ошибка при поиске данных: {str(e)}"
            self.show_error_message(error_msg)

    def _build_base_query(self, model):
        """Создает базовый запрос в зависимости от модели"""
        # Базовый запрос только с нужными полями, без лишних JOIN'ов
        query = db.query(model)
        
        # Добавляем только JOIN с doc_type для фильтрации по типу документа
        query = query.join(DOCType, model.DocType_id == DOCType.id)
        
        return query

    def _apply_filters(self, query, model):
        """Применяет фильтры к запросу с учетом типа модели"""
        # Фильтр по году
        year = self.ui.line_Year.currentText()
        if year != "-" and year != "":
            try:
                year_int = int(year)
                query = query.filter(extract('year', model.Date) == year_int)
            except ValueError:
                pass
        
        # Фильтр по месяцу
        month = self.ui.line_Mnth.currentText()
        if month != "-" and month != "":
            try:
                month_int = int(month)
                query = query.filter(extract('month', model.Date) == month_int)
            except ValueError:
                pass
        
        # Фильтр по типу документа
        doc_type = self.ui.line_doc_type.currentText()
        if doc_type != "-" and doc_type != "":
            # Получаем все DocType_id, соответствующие выбранному Doc_type
            doc_type_ids = db.query(DOCType.id).filter(DOCType.Doc_type == doc_type).all()
            doc_type_ids = [doc_id[0] for doc_id in doc_type_ids]
            
            if doc_type_ids:
                query = query.filter(model.DocType_id.in_(doc_type_ids))
        
        # Фильтр по контрагенту (клиент или поставщик) - добавляем JOIN только если нужен
        customer_supplier = self.ui.line_customer.currentText()
        if customer_supplier != "-" and customer_supplier != "":
            if model in [temp_Sales, temp_Orders]:
                query = query.join(Customer, model.Customer_id == Customer.id)
                query = query.filter(Customer.Customer_name == customer_supplier)
            elif model in [temp_Purchase, Purchase_Order]:
                query = query.join(Supplier, model.Supplier_id == Supplier.id)
                query = query.filter(Supplier.Supplier_Name == customer_supplier)
        
        # Фильтр по продукту - добавляем JOIN только если нужен
        product = self.ui.line_product.currentText()
        if product != "-" and product != "":
            query = query.join(Materials, model.Material_id == Materials.Code)
            query = query.join(Product_Names, Materials.Product_Names_id == Product_Names.id)
            query = query.filter(Product_Names.Product_name == product)
        
        return query

    def _update_summary(self, df, model):
        """Обновление сводной информации с учетом label_qty_pcs и label_Volume"""
        if df.empty:
            volume_liters = qty_pcs = amount = 0
        else:
            # Определяем колонки для суммирования в зависимости от модели
            amount_col = 'Amount_1C' if 'Amount_1C' in df.columns else df.columns[0]
            amount = df[amount_col].sum() if amount_col in df.columns else 0
            
            # Для количества в штуках и литрах используем специальные колонки или вычисления
            if 'Кол-во, шт' in df.columns:
                qty_pcs = df['Кол-во, шт'].sum()
            elif 'Qty_pcs' in df.columns:
                qty_pcs = df['Qty_pcs'].sum()
            elif 'Qty' in df.columns and hasattr(model, 'material'):
                # Если нет специальной колонки, пытаемся вычислить из Qty
                qty_pcs = df['Qty'].sum()
            else:
                qty_pcs = 0
            
            if 'Кол-во, л' in df.columns:
                volume_liters = df['Кол-во, л'].sum()
            elif 'Qty_lt' in df.columns:
                volume_liters = df['Qty_lt'].sum()
            elif 'Volume_liters' in df.columns:
                volume_liters = df['Volume_liters'].sum()
            else:
                volume_liters = 0
        
        def format_number(value, is_integer=False):
            """Форматирование чисел с учетом типа"""
            if pd.isna(value) or value is None:
                return "0"
            
            try:
                if is_integer:
                    return f"{int(value):,}".replace(",", " ")
                else:
                    return f"{float(value):,.2f}".replace(",", " ").replace(".", ",")
            except (ValueError, TypeError):
                return "0"
        
        # Обновляем информацию в интерфейсе
        self.ui.label_qty_pcs.setText(f"{format_number(qty_pcs, True)} шт.")
        self.ui.label_Volume.setText(f"{format_number(volume_liters)} л.")

    def _display_data(self, df):
        """Отображение данных в таблице с сортировкой и переименованными колонками"""
        self.table.clearContents()

        # Определяем базовые колонки для показа
        base_columns_to_show = [
            'Document', 'Date', 'Status', 'Тип документа', 'Material_id', 'Артикул',
            'Продукт + упаковка', 'Кол-во, шт', 'Кол-во, л', 'Amount_1C'
        ]

        # Добавляем колонки счета и даты счета только для продаж и заказов клиентов
        table = self.ui.line_table.currentText()
        if table in ["Продажи", "Заказы клиентов"]:
            base_columns_to_show.extend(['Bill', 'Bill_Date'])

        # Добавляем колонку контрагента в зависимости от типа таблицы
        if table in ["Закупки", "Заказы поставщиков"] and 'Supplier_Name' in df.columns:
            base_columns_to_show.append('Supplier_Name')
        elif table in ["Продажи", "Заказы клиентов"] and 'Customer_Name' in df.columns:
            base_columns_to_show.append('Customer_Name')

        # Фильтруем только существующие колонки
        columns_to_show = [col for col in base_columns_to_show if col in df.columns]

        # Создаем DataFrame только с нужными колонками
        display_df = df[columns_to_show].copy()

        # Переименовываем колонки для отображения
        column_rename_map = {
            'Document': 'Документ',
            'Date': 'Дата',
            'Material_id': 'Код',
            'Status': 'Статус',
            'Amount_1C': 'Сумма 1С'
        }

        # Добавляем переименование для счета и даты счета (только если они есть)
        if 'Bill' in display_df.columns:
            column_rename_map['Bill'] = 'Счет'
        if 'Bill_Date' in display_df.columns:
            column_rename_map['Bill_Date'] = 'Дата счета'

        # Переименовываем колонку контрагента
        if table in ["Закупки", "Заказы поставщиков"] and 'Supplier_Name' in display_df.columns:
            column_rename_map['Supplier_Name'] = 'Контрагент'
        elif table in ["Продажи", "Заказы клиентов"] and 'Customer_Name' in display_df.columns:
            column_rename_map['Customer_Name'] = 'Контрагент'

        # Применяем переименование
        display_df = display_df.rename(columns=column_rename_map)
        
        # Безопасное преобразование дат - только если колонки существуют
        if 'Дата' in display_df.columns:
            display_df['Дата'] = pd.to_datetime(display_df['Дата'], format='%d.%m.%Y', errors='coerce')
        
        if 'Дата счета' in display_df.columns:
            display_df['Дата счета'] = pd.to_datetime(display_df['Дата счета'], format='%d.%m.%Y', errors='coerce')
        
        # Сортировка только по существующим колонкам
        sort_columns = []
        for col in ['Дата', 'Тип документа', 'Документ', 'Дата счета', 'Счет', 'Кол-во, шт']:
            if col in display_df.columns:
                sort_columns.append(col)
        
        if sort_columns:
            display_df = display_df.sort_values(by=sort_columns, ascending=[True] * len(sort_columns))
        
        # Форматирование дат обратно в строки
        if 'Дата' in display_df.columns:
            display_df['Дата'] = display_df['Дата'].dt.strftime('%d.%m.%Y')
        
        if 'Дата счета' in display_df.columns:
            display_df['Дата счета'] = display_df['Дата счета'].dt.strftime('%d.%m.%Y')
        
        display_columns = list(display_df.columns)

        # Устанавливаем колонки и строки
        self.table.setColumnCount(len(display_columns))
        self.table.setRowCount(len(display_df))
        self.table.setHorizontalHeaderLabels(display_columns)

        numeric_cols = ["Кол-во, шт", "Кол-во, л", "Сумма 1С"]
        # Заполняем таблицу данными
        for row_idx in range(len(display_df)):
            for col_idx, col_name in enumerate(display_columns):
                value = display_df.iloc[row_idx][col_name]

                # Преобразуем None/NaN в пустую строку
                if pd.isna(value) or value is None or str(value) in ['None', 'nan', 'NaT']:
                    value = ''

                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                # Форматирование числовых колонок
                if col_name in numeric_cols and pd.notna(value) and value != '':
                    try:
                        if col_name in ["Кол-во, шт"]:
                            # Целочисленные значения
                            item.setText(f"{int(float(value)):,}".replace(",", " "))
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        else:
                            # Дробные значения
                            item.setText(f"{float(value):,.2f}".replace(",", " ").replace(".", ","))
                            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    except (ValueError, TypeError):
                        pass

                self.table.setItem(row_idx, col_idx, item)

        # Включаем сортировку
        self.table.setSortingEnabled(True)

        # Настраиваем resize mode для колонок
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)

        # Делаем последнюю колонку растяжимой
        self.table.horizontalHeader().setStretchLastSection(True)

        # Автоподбор ширины колонок
        self.table.resizeColumnsToContents()

    def upload_data(self):
        """Обновление данных из файлов и загрузка в БД"""
        try:
            # Очищаем кэш при обновлении данных
            self.table_data_cache = {}
            self.current_table_data = None
            
            date_start = self.ui.date_Start.date()
            self.report_start_date = date_start.toPython()
            self.report_start_date = pd.to_datetime(self.report_start_date)
            
            # Обработка данных в зависимости от выбранной таблицы
            table = self.ui.line_table.currentText()
            
            if table == '-':
                purchase_df = self.read_purchase_data(self.report_start_date)
                if not purchase_df.empty:
                    self._update_temp_purchase_in_db(purchase_df, self.report_start_date)
                    self.show_message("Данные о закупках успешно обновлены")
                    
                sales_df = self.read_sales_data(self.report_start_date)
                if not sales_df.empty:
                    self._update_temp_sales_in_db(sales_df)
                    self.show_message("Данные о продажах успешно обновлены")
                    
                orders_df = self.read_orders_data()
                if not orders_df.empty:
                    self._update_temp_orders_in_db(orders_df)
                    self.show_message("Данные о заказах успешно обновлены")
                    
                purchase_order_df = self.read_purchase_order_data()
                if not purchase_order_df.empty:
                    self._update_purchase_order_in_db(purchase_order_df)
                    self.show_message("Данные о заказах поставщиков успешно обновлены")
                
            elif table == "Закупки":
                purchase_df = self.read_purchase_data(self.report_start_date)
                if not purchase_df.empty:
                    self._update_temp_purchase_in_db(purchase_df, self.report_start_date)
                    self.show_message("Данные о закупках успешно обновлены")
            
            elif table == "Продажи":
                sales_df = self.read_sales_data(self.report_start_date)
                if not sales_df.empty:
                    self._update_temp_sales_in_db(sales_df)
                    self.show_message("Данные о продажах успешно обновлены")
            
            elif table == "Заказы клиентов":
                orders_df = self.read_orders_data()
                if not orders_df.empty:
                    self._update_temp_orders_in_db(orders_df)
                    self.show_message("Данные о заказах успешно обновлены")
            
            elif table == "Заказы поставщиков":
                purchase_order_df = self.read_purchase_order_data()
                if not purchase_order_df.empty:
                    self._update_purchase_order_in_db(purchase_order_df)
                    self.show_message("Данные о заказах поставщиков успешно обновлены")
            
            # После обновления данных обновляем только базовые комбобоксы
            models = {
                "Закупки": temp_Purchase,
                "Продажи": temp_Sales,
                "Заказы клиентов": temp_Orders,
                "Заказы поставщиков": Purchase_Order
            }
            self._fill_combobox(self.ui.line_table, list(models.keys()))
            
            # Остальные списки очищаем
            self._fill_combobox(self.ui.line_doc_type, ["-"])
            self._fill_combobox(self.ui.line_Year, ["-"])
            self._fill_combobox(self.ui.line_Mnth, ["-"])
            self._fill_combobox(self.ui.line_customer, ["-"])
            self._fill_combobox(self.ui.line_product, ["-"])

        except Exception as e:
            self.show_error_message(f"Ошибка при обновлении данных: {str(e)}")
            traceback.print_exc()

    def read_purchase_data(self, report_start_date):
        """Чтение данных о закупках"""

        purchase_df = pd.DataFrame()
        dtypes = {"Номер документа сторонней организации": str, "Артикул": str, "Курс взаиморасчетов": float, 
                    "Цена": float, "% НДС": str, "Количество": float, "Сумма без НДС": float}
        
        # Определяем файлы для чтения на основе года из date_start
        target_year = report_start_date.year
        files_to_read = []
        
        for root, dirs, files in os.walk(Purchase_folder):
            for name in files:
                if name.startswith("Закупки_") and name.endswith(".xlsx"):
                    try:
                        file_year = int(name.split("_")[1].split(".")[0])
                        if file_year >= target_year:
                            files_to_read.append(os.path.join(root, name))
                    except (IndexError, ValueError):
                        continue
        
        frames = []
        for file_path in files_to_read:
            try:
                data = pd.read_excel(file_path, skiprows=4, dtype=dtypes)
                frames.append(data)
            except Exception as e:
                self.show_error_message(f"Ошибка при чтении файла {file_path}: {e}")
        
        if frames:
            purchase_df = pd.concat(frames, axis=0, ignore_index=True)
        
        if purchase_df.empty:
            return pd.DataFrame()
        
        # Обработка данных
        purchase_df = self._process_purchase_data(purchase_df, report_start_date)
        return purchase_df

    def _process_purchase_data(self, df, report_start_date):
        """Обработка данных о закупках"""
        
        # Чтение и обработка lpc_transf_df
        dtype_lpc = {"Документ": str, "Тип документа": str, "Артикул": str, "Продукт + упаковка": str, 
                                "Сумма переноса": float, "Сумма 1С": float, "Артикул Компл": str}
        lpc_transf_df = pd.read_excel(AddCosts_File, sheet_name="Перенос себ-ти", dtype=dtype_lpc)
        lpc_transf_df["Дата"] = pd.to_datetime(lpc_transf_df["Дата"], format="%d.%m.%Y")
        lpc_transf_df["Имп/Лок"] = "нет"
        lpc_transf_df["Валюта"] = "RUB"
        lpc_transf_df["Единица измерения"] = "шт"
        lpc_transf_df["Склад"] = "-"
        lpc_transf_df["% НДС"] = "20%"
        lpc_transf_df["Курс взаиморасчетов"] = 1.0

        df = df.rename(columns={"Регистратор номер": "Документ", 
                                                    "Ссылка.Вид операции": "Вид операции",
                                                    "Сумма без НДС": "Сумма 1С", 
                                                    "Номер документа сторонней организации": "Suppl Inv N"})
    
        df["Контрагент"] = df['Контрагент'].str.replace('не исп_', '', regex=False)
        df = df[df["Документ"] != "Итого"]
        df['Вид операции'] = df['Вид операции'].fillna('-')
        
        df = df[(df["Контрагент.Код"] != "ОП-001636")]

        df["Документ основание"] = df["Документ основание"].astype(str)
        split_columns = df["Документ основание"].str.split(" ", expand=True)
        
        df["ДокОсн"] = split_columns.get(4, pd.Series([None] * len(df)))
        df["Дата ДокОсн"] = split_columns.get(6, pd.Series([None] * len(df)))

        df["Дата"] = pd.to_datetime(df["Дата"], format="%d.%m.%Y", errors="coerce")
        df["Дата ДокОсн"] = pd.to_datetime(df["Дата ДокОсн"], format="%d.%m.%Y", errors="coerce")

        df["doc"] = np.where(pd.isna(df["Количество"]) & pd.isna(df["Сумма 1С"]), "yes",  "no")
        df = df[df["doc"] != "yes"]
        df["Код"] = df["Код"].str.strip()
        
        df = df[df["Дата"] >= report_start_date]
        lpc_transf_df = lpc_transf_df[lpc_transf_df["Дата"] >= report_start_date]
        
        if not lpc_transf_df.empty:
            lpc_transf_df = lpc_transf_df.dropna(axis=1, how='all')
            df = pd.concat([df, lpc_transf_df], axis=0, ignore_index=True)
            
        df["Статус"] = np.where(df["Тип документа"].str.contains("Поступление"), "Закуп", "Склад")
            
        # Получение ID типа документа
        df['DocType_id'] = df.apply(lambda row: self._get_doc_type_id(row.get('Вид документа', ''), row.get('Вид операции', ''), row.get('Тип документа', '')), axis=1)
        df['Количество'] = np.where(df['Тип документа'] == '7.0. Передача в переработку', -df['Количество'], df['Количество'])

        # Проверка продуктов
        self._check_products(df)
        
        # Проверка поставщиков
        self._check_suppliers(df, 'Контрагент.Код')
        
        # Переименование колонок согласно соответствию
        column_mapping = {
            'Документ': 'Document',
            'Дата': 'Date',
            'Статус': 'Status',
            'ДокОсн': 'Doc_based',
            'Дата ДокОсн': 'Date_Doc_based',
            'Контрагент.Код': 'Supplier_id',
            'Контрагент': 'Supplier_Name',
            'Код': 'Material_id',
            'Склад': 'Stock',
            'Валюта': 'Currency',
            '% НДС': 'VAT',
            'Страна происхождения': 'Country',
            'Номер ГТД': 'GTD',
            'Курс взаиморасчетов': 'FX_rate_1C',
            'Количество': 'Qty',
            'Сумма 1С': 'Amount_1C'
        }
        
        df = df.rename(columns=column_mapping)

        return df

    def read_sales_data(self, report_start_date):
        
        """Чтение данных о продажах"""
        sales_df = pd.DataFrame()
        dtypes = {"Контрагент.ИНН": str, "Артикул": str, "Код дилера HYUNDAI": str, "Курс взаиморасчетов": float, "Цена": float,
                    "% НДС": str, "Количество": float, "Сумма без НДС": float, "Процент пост оплаты": float,
                    "Заполнен на основании документа.Номер": str, "Сумма включая НДС": float, "Сборка": str}
        
        # Определяем файлы для чтения на основе года из date_start
        target_year = report_start_date.year
        files_to_read = []
        
        for root, dirs, files in os.walk(Sales_folder):
            for name in files:
                if name.startswith("Продажи_") and name.endswith(".xlsx"):
                    try:
                        file_year = int(name.split("_")[1].split(".")[0])
                        if file_year >= target_year:
                            files_to_read.append(os.path.join(root, name))
                    except (IndexError, ValueError):
                        continue
        
        frames = []
        for file_path in files_to_read:
            try:
                data = pd.read_excel(file_path, skiprows=5, dtype=dtypes)
                frames.append(data)
            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}")
        
        if frames:
            sales_df = pd.concat(frames, axis=0, ignore_index=True)
        
        if sales_df.empty:
            return pd.DataFrame()
        
        # Обработка данных
        sales_df = self._process_sales_data(sales_df, report_start_date)
        return sales_df

    def _process_sales_data(self, df, report_start_date):
        """Обработка данных о продажах с использованием данных из БД"""
        # Чтение данных коррекции
        dtype_SD = {"Сборка_корр": str}
        корр_Сборка = pd.read_excel(CustDelivery_File, sheet_name="Корр-ка Сборки", dtype=dtype_SD)
        корр_Сборка = корр_Сборка.drop(columns=["Дата", "Счет", 'Дата счета', "Контрагент"])

        sales_corr = pd.read_excel(AddCosts_File, sheet_name="Корр-ка реал-ий")
        sales_corr["Дата"] = pd.to_datetime(sales_corr["Дата"], format="%d.%m.%Y", errors="coerce")
        sales_corr = sales_corr[sales_corr["Документ"] != "-"].drop(columns=["Контрагент"]).drop_duplicates(subset=["Документ", "Дата"])
        
        # Переименование колонок
        df = df.rename(columns={
            "Регистратор номер": "Документ",
            "Счет на оплату покупателю номер": "Счет",
            "Счет на оплату покупателю дата": "Дата счета",
            "Счет на оплату.Способ доставки": "Способ доставки",
            "Сумма без НДС": "Сумма 1С",
            "Процент пост оплаты": "Постоплата%",
            "Грузополучатель код": "Грузополучатель.Код",
            "Заполнен на основании документа.Номер": "Сборка",
            "Заполнен на основании документа.Плановая дата отгрузки": "ПланДатаОтгр",
            "Счет на оплату.Приоритет резервирования": "Приоритет"
        })

        # Обработка данных
        df["Договор"] = df["Договор"].fillna("blank")
        df["Условие оплаты"] = df["Условие оплаты"].fillna("blank")
        df["Грузополучатель.Код"] = df["Грузополучатель.Код"].fillna("-")

        df["Документ основание"] = df["Документ основание"].str.replace("Реализация отгруженных товаров", "Реализация (акт, накладная, УПД)")
        df["Документ основание"] = df["Документ основание"].str.replace("Корректировка реализации", "Реализация (акт, накладная, УПД)")
        
        split_columns = df["Документ основание"].str.split(" ", expand=True, n=7)
        df["ДокОсн"] = split_columns.get(4, pd.Series([None] * len(df)))
        df["Дата ДокОсн"] = split_columns.get(6, pd.Series([None] * len(df)))
        
        df["ПланДатаОтгр"] = np.where(pd.isnull(df["ПланДатаОтгр"]), df["Дата"], df["ПланДатаОтгр"])

        # Преобразование дат
        date_columns = ["Дата", "Дата счета", "Дата ДокОсн", "Плановая дата оплаты", "ПланДатаОтгр"]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], format="%d.%m.%Y", errors="coerce")
        
        # Фильтрация по дате
        df = df[df["Дата"] >= report_start_date]
        
        df['Артикул'] = df['Артикул'].fillna('-')
        
        # Фильтрация исключений
        df = df[
            (df["Документ"] != "Итого") &
            (~df["Контрагент.Код"].isin(["ОЛ-000220", "ОП-007777", "ОП-001518", "ОП-001217", "ОП-041292", "ОП-041302", "ОП-000220"])) &
            (df["Код"] != "НМ-00003477") &
            (df["Номенклатура"] != "агентские услуги")
        ]

        # Удаление пустых документов
        df["doc"] = np.where(pd.isnull(df["Количество"]) & pd.isnull(df["Сумма 1С"]), "yes", "no")
        df = df[df["doc"] != "yes"]

        doc_types = db.query(DOCType).all()

        doc_type_df = pd.DataFrame([{
            'DocType_id': item.id,
            'Document': item.Document, 
            'Transaction': item.Transaction,
            'Тип документа': item.Doc_type} for item in doc_types])
        doc_type_df
        # Merge с df
        df = pd.merge(df, doc_type_df,
            left_on=['Вид документа', 'Вид операции'],
            right_on=['Document', 'Transaction'],how='left').drop(['Document', 'Transaction'], axis=1)

        # Расчет цены 1С
        df["Цена 1С"] = np.where(df["Количество"] != 0.0, round(df["Сумма 1С"] / df["Количество"], 2), 0.0)
        df["Код"] = df["Код"].str.strip()
        
        # Коррекция имен контрагентов
        corr_name = {
            "Розничный покупатель": "Yandex", 
            "ЯНДЕКС ООО": "Yandex", 
            "ЯНДЕКС МАРКЕТ ООО": "Yandex",
            "ВАЙЛДБЕРРИЗ ООО": "Wildberries", 
            "РВБ ООО": "Wildberries", 
            "ИНТЕРНЕТ РЕШЕНИЯ ООО": "OZON",
            "МАРКЕТПЛЕЙС ООО": "СберМегаМаркет"
        }
        df["Контрагент"] = df["Контрагент"].replace(corr_name)

        # Фильтрация marketplace данных
        conditions = (
            (((df["Вид документа"] == "Отчет комиссионера (агента)") | (df["Вид операции"] == "Услуги") | (df["Вид операции"] == "Выкуп комиссионером") ) 
                        & (df["Контрагент.Код"] == "ОП-000160")) |   # ozon
            ((df["Контрагент.Код"] == "ОП-000105") |   # yandex
            (df["Контрагент.Код"] == "ОП-041776") |   # yandex
            (df["Контрагент.Код"] == "ОП-000155") | (df["Контрагент.Код"] == "ОП-001773")))     # WB

        df["check"] = np.where(conditions, "del", "-")
        df = df[df["check"] != "del"]
        df = df[df["Тип документа"] != "4.0. Реализация (компенсация ОЗОН)"]
        
        # Определение типа документа
        doc_type_conditions = [
            (df["Контрагент.Код"] == "ОП-000160") & # ozon
            (df["Вид документа"] == "Реализация (акт, накладная, УПД)") & 
            (df["Вид операции"] == "Товары"),
            
            (df["Контрагент.Код"] == "ОП-000163") & # yandex
            (df["Вид документа"] == "Реализация отгруженных товаров"),
            
            (df["Контрагент.Код"] == "ОП-000163") & # yandex
            ((df["Вид документа"] == "Корректировка реализации") | 
            (df["Вид документа"] == "Возврат товаров от покупателя"))
        ]

        doc_type_choices = ["4.0. Реализация (ОЗОН 1P)", "4.0. Реализация (Yandex)", "4.0. Реализация (корр-ка Yandex)"]
        df["Тип документа"] = np.select(doc_type_conditions, doc_type_choices, default=df["Тип документа"])
        
        operation_conditions = [
            df["Тип документа"] == "4.0. Реализация (ОЗОН 1P)",
            df["Тип документа"] == "4.0. Реализация (Yandex)",
            df["Тип документа"] == "4.0. Реализация (корр-ка Yandex)"
        ]

        # Определяем соответствующие значения для "Вид операции"
        operation_choices = [
            "Товары ОЗОН 1P",
            "Товары Yandex", 
            "Товары Yandex"
        ]

        # Применяем условия с помощью np.select
        df["Вид операции"] = np.select(operation_conditions, operation_choices, default=df["Вид операции"])

        # Объединение с коррекцией
        df = df.merge(sales_corr, how="left", on=["Документ", "Дата", "Контрагент.Код"])
        df["Курс взаиморасчетов"] = df["Курс взаиморасчетов_corr"].fillna(df["Курс взаиморасчетов"])
        df = df.drop(columns=["Курс взаиморасчетов_corr", "НДС"])
        
        df['data_source'] = '1C'

        marketplace_df = self.get_marketplace_data(report_start_date)
        if not marketplace_df.empty:
            marketplace_df['Дата'] = pd.to_datetime(marketplace_df['Дата'], errors='coerce')
            
            df = pd.concat([df, marketplace_df], ignore_index=True)

        # Заполнение пустых значений
        df[["Курс взаиморасчетов", "Валюта", "% НДС"]] = df[["Курс взаиморасчетов", "Валюта", "% НДС"]].fillna({
            "Курс взаиморасчетов": 1.0, 
            "Валюта": "RUB", 
            "% НДС": "20%"
        })

        # Коррекция сборки
        df = df.merge(корр_Сборка, how="left", on=["Документ", "Контрагент.Код"])
        df["Сборка_корр"] = df["Сборка_корр"].fillna("-")
        df["Сборка"] = np.where(df["Сборка_корр"] != "-", df["Сборка_корр"], df["Сборка"])

        # Условия оплаты
        conditions_pay_terms = [
            (df["Договор"] == "КЭШ"), 
            (df["Контрагент.Код"] == "ОП-000897")  # АВТОДОК
        ]
        choices_pay_terms = ["Аванс 100% через 0 к.д.", "Постоплата 100% через 7 к.д."]
        df["Условие оплаты"] = np.select(conditions_pay_terms, choices_pay_terms, default=df["Условие оплаты"])
        df["Плановая дата оплаты"] = np.where(df["Договор"] == "КЭШ", df["Дата"], df["Плановая дата оплаты"])
        
        # Преобразование дат
        df["Плановая дата оплаты"] = pd.to_datetime(df["Плановая дата оплаты"], errors='coerce')
        df["Дата ДокОсн"] = pd.to_datetime(df["Дата ДокОсн"], errors='coerce')

        # Расчет дней на оплату
        conditions_plan_pay_date = [
            (df["Договор"] == "blank") | (df["Условие оплаты"] == "blank"),
            (df["Тип документа"] == "4.1. Реализация (корр-ка)") & (df["ДокОсн"] != "-"),
            (df["Контрагент.Код"] == "ОП-000897")  # АВТОДОК
        ]

        choices_plan_pay_date = [
            30, 
            (df["Плановая дата оплаты"] - df["Дата ДокОсн"]).dt.days, 
            7
        ]

        df["Кол-во дней на оплату"] = np.select(
            conditions_plan_pay_date, 
            choices_plan_pay_date,
            default=(pd.to_datetime(df["Плановая дата оплаты"]) - pd.to_datetime(df["Дата"])).dt.days
        )
        
        # Заполнение пустых значений
        df["Сборка"] = df["Сборка"].fillna("-")
        df["Счет"] = df["Счет"].fillna("-")
        df["Статус"] = "Факт"

        # Дополнительная коррекция
        df = df.merge(sales_corr, how="left", on=["Документ", "Дата", "Контрагент.Код"])
        df["Курс взаиморасчетов"] = df["Курс взаиморасчетов_corr"].fillna(df["Курс взаиморасчетов"])
        df = df.drop(columns=["Курс взаиморасчетов_corr"])

        # Проверка продуктов
        self._check_products(df)
        
        # Проверка клиентов
        self._check_customers(df, 'Контрагент.Код')
        
        # Проверка HYUNDAI дилеров
        self._check_hyundai_dealers(df)
        
        # Проверка договоров
        self._check_contracts(df, 'Договор.Код', 'Контрагент.Код')
        
        # Дополнительная обработка (сохраненная часть)
        df['Цена 1С'] = np.round(df['Цена 1С'], 2).fillna(0).astype(float)
        df["Счет"] = df["Счет"].fillna("-")
        df["Дата счета"] = df["Дата счета"].fillna(df["Дата"])
        
        # Группировка данных
        agg_columns = ['Количество', 'Сумма 1С']
        group_columns = ['Документ', 'Дата', 'Тип документа', 'Счет', "Контрагент.Код", 'Код', 'Цена 1С']
        other_columns = df.columns.difference(group_columns + agg_columns)
        sales_grouped = df.groupby(group_columns, as_index=False).agg({'Количество': 'sum', 'Сумма 1С': 'sum'})

        for col in other_columns:
            sales_grouped[col] = df.groupby(group_columns)[col].first().values
        
        df = sales_grouped.copy()

        СпецЗаказы = self.read_special_orders(AddCosts_File)
        # Анализ специальных заказов
        error_file_name = "ERRORs_Spec_Orders_Sales.xlsx"
        keys_spec = set(zip(СпецЗаказы['Счет'], СпецЗаказы['Дата счета'], СпецЗаказы['Код']))
        mask = df.apply(lambda row: (row['Счет'], row['Дата счета'], row['Код']) in keys_spec, axis=1)
        
        df_to_process = df[mask].copy()
        processed_df = self.analyze_special_deliveries(df_to_process, СпецЗаказы, error_file_name)
        df_not_processed = df[~mask].copy()

        df = pd.concat([processed_df, df_not_processed], ignore_index=True)

        columns_to_check = [
            'к_Транспорт (перемещ), л',
            'к_Хранение, л',
            'к_Ст-ть Денег, л'
        ]

        for col in columns_to_check:
            if col not in df.columns:
                df[col] = pd.Series(dtype=float)
                
        df.loc[:, "columns_to_check"] = df["columns_to_check"].astype(float).fillna(1.0)

        df["Дата"] = pd.to_datetime(df["Дата"], format='%d.%m.%Y', errors="coerce")
        df["Дата счета"] = pd.to_datetime(df["Дата счета"], format='%d.%m.%Y', errors="coerce")
        df["Дата ДокОсн"] = pd.to_datetime(df["Дата ДокОсн"], format='%d.%m.%Y', errors="coerce")
        df["Дата Поставки"] = pd.to_datetime(df["Дата Поставки"], format='%d.%m.%Y', errors="coerce")
        df["Order N Поставки"] = df["Order N Поставки"].astype(str)
        
        df["Приоритет"] = df["Приоритет"].fillna("-")

        # ПОДБОР ТОЛЬКО ДЛЯ ДАННЫХ ИЗ 1С (НЕ ИЗ MARKETPLACE)
        is_1c_data = df['data_source'] == '1C'
        
        # Подбор DocType_id только для данных из 1С
        if is_1c_data.any():
            df.loc[is_1c_data, 'DocType_id'] = df[is_1c_data].apply(
                lambda row: self._get_doc_type_id(row.get('Вид документа', ''), row.get('Вид операции', ''), row.get('Тип документа', '')), axis=1)
        
        # Подбор Manager_id только для данных из 1С
        if is_1c_data.any() and 'Договор.Менеджер' in df.columns:
            managers = db.query(Manager.AM_1C_Name, Manager.id).all()
            manager_dict = {m.AM_1C_Name: m.id for m in managers if m.AM_1C_Name}
            
            df.loc[is_1c_data, 'Manager_id'] = df[is_1c_data]['Договор.Менеджер'].map(manager_dict)
        
        # Удаляем временный столбец
        df = df.drop(columns=['data_source'])
        
        column_mapping = {
            'Документ': 'Document',
            'Дата': 'Date',
            'Статус': 'Status',
            'Счет': 'Bill',
            'Дата счета': 'Bill_Date',
            'ДокОсн': 'Doc_based',
            'Дата ДокОсн': 'Date_Doc_based',
            'Контрагент.Код': 'Customer_id',
            'Контрагент': 'Customer_Name',
            'Код': 'Material_id',
            'Склад': 'Stock',
            'Способ доставки': 'Delivery_method',
            'Валюта': 'Currency',
            'Курс взаиморасчетов': 'FX_rate_1C',
            'Количество': 'Qty',
            'Сумма 1С': 'Amount_1C',
            '% НДС': 'VAT',
            'Грузополучатель': 'Recipient',
            'Грузополучатель.Код': 'Recipient_code',
            'Договор.Код': 'Contract_id',
            'Договор.Менеджер': 'Manager',
            'Кол-во дней на оплату': 'Days_for_Pay',
            'ПланДатаОтгр': 'Plan_Delivery_Day',
            'Плановая дата оплаты': 'Plan_Pay_Day',
            'Постоплата%': 'Post_payment',
            'Условие оплаты': 'Payment_term',
            'Приоритет': 'Priority',
            'Регистратор.Комментарий': 'Comment',
            'Сборка': 'Sborka',
            'Спец поставка': 'Spec_Order',
            'Док Поставки': 'Purchase_doc',
            'Дата Поставки': 'Purchase_date',
            'Поставщик.Код': 'Supplier_id',
            'Order N Поставки': 'Order',
            'к_Транспорт (перемещ), л': 'k_Movement',
            'к_Хранение, л': 'k_Storage',
            'к_Ст-ть Денег, л': 'k_Money'
        }
        
        df = df.rename(columns=column_mapping)
        df.to_excel('test_sales.xlsx')
        return df
    
    def read_orders_data(self):
        """Чтение данных о заказах"""
        max_date = db.query(temp_Sales.Date).order_by(temp_Sales.Date.desc()).first()
        if max_date:
            sales_max_date = max_date[0]
            sales_max_date = pd.to_datetime(sales_max_date)
        else:
            report_start_date = datetime.datetime.now()
            report_start_date = pd.to_datetime(report_start_date)
        
        dtypes = {
            "Номер": str, "ИНН": str, "Номенклатура1 артикул": str,
            "Процент пост оплаты": float, "Заказ.Курс взаиморасчетов": float, "Сумма расчетов": float,
            "% НДС": str, "Сумма": float, "Заказано количество": float, "Старый резерв количество": float,
            "Новый резерв количество": float, "Реализация количество": float,
            "Остаток отгрузки по Заказу (т.е. Заказ-Реализация)": float}
        
        try:
            ord_df = pd.read_excel(Orders_file, dtype=dtypes)
        except Exception as e:
            self.show_error_message(f"Ошибка при чтении файла заказов {Orders_file}: {e}")
        
        # Чтение файла резервов
        try:
            reserve_df = pd.read_excel(Reserve_file, dtype=dtypes)
        except Exception as e:
            self.show_error_message(f"Ошибка при чтении файла резервов {Reserve_file}: {e}")
        
        """Обработка данных о заказах"""
        
        ord_df = ord_df.rename(columns={"Номер": "Счет", "Дата": "Дата счета", "Заказ контрагент код": "Контрагент.Код",
                                                            "ИНН": "Контрагент.ИНН", "Заказ грузополучатель код": "Грузополучатель.Код",
                                                            "Номенклатура1 артикул": "Артикул", "Номенклатура1 код": "Код", "Номенклатура1": "Номенклатура",
                                                            "Номенклатура.Единица": "Единица измерения", 
                                                            "Комментарий": "Заказ.Комментарий",
                                                            "Заказ договор контрагента код": "Договор.Код", 
                                                            "Процент пост оплаты": "Постоплата%", "Статус": "Статус оплаты",
                                                            "Сумма расчетов": "Сумма оплаты", 
                                                            "ОсталосьОтгрузить": "ОстЗак",
                                                            "Приоритет резервирования": "Приоритет"})
        
        ord_df = ord_df.drop(columns=["Менеджер"])
        ord_df = ord_df[(ord_df["Заказано"] != "Заказано количество") & (ord_df["Счет"] != "Итого")]

        ord_df["Код"] = ord_df["Код"].str.strip()
        ord_df["Договор"] = ord_df["Договор"].fillna("blank")
        ord_df["Условие оплаты"] = ord_df["Условие оплаты"].fillna("blank")
        ord_df["Грузополучатель.Код"] = ord_df["Грузополучатель.Код"].fillna("-")
        ord_df["Статус оплаты"] = ord_df["Статус оплаты"].fillna("Не оплачен")
        ord_df["Склад"] = ""
        ord_df[["Сумма", "Заказано", "Отгружено", "ОстЗак"]] = ord_df[["Сумма", "Заказано", "Отгружено", "ОстЗак"]].astype(float).fillna(0.0)
        ord_df["Дата счета"] = pd.to_datetime(ord_df["Дата счета"], format="%d.%m.%Y")
        ord_df["Плановая дата оплаты"] = pd.to_datetime(ord_df["Плановая дата оплаты"], format="%d.%m.%Y", errors="coerce")
        
        reserve_df = reserve_df.rename(columns={"Заказ.Номер": "Счет", "Заказ.Дата": "Дата счета", "Заказ контрагент код": "Контрагент.Код",
                                                                        "Заказ грузополучатель код": "Грузополучатель.Код",
                                                                        "Номенклатура1 артикул": "Артикул", "Номенклатура1 код": "Код", "Номенклатура1": "Номенклатура",
                                                                        "Склад резерва": "Склад", 
                                                                        "Номенклатура единица измерения": "Единица измерения", 
                                                                        "Заказ договор контрагента код": "Договор.Код", 
                                                                        "Старый резерв количество": "СтарРезерв", "Новый резерв количество": "НовРезерв",
                                                                        "Первый резерв": "Дата резерва" })
    
        reserve_df = reserve_df[reserve_df["Счет"] != "Итого"]
        reserve_df["Дата счета"] = pd.to_datetime(reserve_df["Дата счета"], format="%d.%m.%Y", errors="coerce")
        reserve_df["Дата резерва"] = pd.to_datetime(reserve_df["Дата резерва"], format="%d.%m.%Y", errors="coerce")
        reserve_df[["СтарРезерв", "НовРезерв", ]] = reserve_df[["СтарРезерв", "НовРезерв", ]].astype(float).fillna(0.0)
        reserve_df["Резерв"] = reserve_df["СтарРезерв"] + reserve_df["НовРезерв"]
        reserve_df = reserve_df[reserve_df["НовРезерв"] > 0]
        reserve_df["Статус"] = "Резерв"
        
        reserve_for_check = reserve_df.groupby(["Счет", "Дата счета", "Контрагент.Код", "Договор.Код", "Код"])["Резерв"].sum().reset_index()
        
        report_day = sales_max_date + datetime.timedelta(days=1)
        
        ord_w_reserve = reserve_df.merge(ord_df, how="left", on=["Счет", "Дата счета", "Контрагент.Код", "Договор.Код", "Код"])
        ord_w_reserve = ord_w_reserve.rename(columns={"Склад_x": "Склад", "Единица измерения_x": "Единица измерения"})
        ord_w_reserve.drop(columns=["Склад_y", ], inplace=True)
        ord_w_reserve = ord_w_reserve.rename(columns={"Резерв": "Количество"})
        ord_w_reserve["Дата"] = report_day
        ord_w_reserve["Дни резерва"] = (ord_w_reserve["Дата"] - ord_w_reserve["Дата резерва"]).dt.days
        ord_w_reserve["Сумма 1С"] = ord_w_reserve["Сумма"] / ord_w_reserve["Заказано"] * ord_w_reserve["Количество"]

        ord_wo_reserve = ord_df.merge(reserve_for_check, how="left", on=["Счет", "Дата счета", "Контрагент.Код", "Договор.Код", "Код"])
        ord_wo_reserve[["ОстЗак", "Резерв"]] = ord_wo_reserve[["ОстЗак", "Резерв"]].astype(float).fillna(0.0)
        conditions = [
                ord_wo_reserve["Резерв"] == 0,
                ord_wo_reserve["Резерв"] == ord_wo_reserve["ОстЗак"]
            ]
        choices = [
                ord_wo_reserve["ОстЗак"],
                0
            ]
        ord_wo_reserve["Остаток"] = np.select(conditions, choices, default=ord_wo_reserve["ОстЗак"] - ord_wo_reserve["Резерв"])
            
        ord_wo_reserve = ord_wo_reserve[ord_wo_reserve["Остаток"] > 0]
        ord_wo_reserve["Статус"] = "Заказ"
        ord_wo_reserve = ord_wo_reserve.rename(columns={"Остаток": "Количество"})
        ord_wo_reserve["Дата"] = datetime.date.today()
        ord_wo_reserve["Дата"] = ord_wo_reserve["Дата"] + pd.offsets.MonthBegin(1)
        ord_wo_reserve.loc[ord_wo_reserve["Дата"] < report_day, "Дата"] = report_day
        ord_wo_reserve["Сумма 1С"] = ord_wo_reserve["Сумма"] / ord_wo_reserve["Заказано"] * ord_wo_reserve["Количество"]

        df = pd.concat([ord_w_reserve, ord_wo_reserve], axis=0)
        
        exclude_codes = ["ОЛ-000220", "ОП-007777", "ОП-001518", "ОП-000220"]
        exclude_kod = ["НМ-00003477", "НМ-00004559", "ОП-000040", "ОП-000041", "ОП-000042", "ОП-000043"]

        filters = (~df["Контрагент.Код"].isin(exclude_codes) & 
                (df["Контрагент"] != "тест") & 
                (df["Пометка удаления"] != "Да") & 
                (df["Проведен"] != "Нет") &
                (df["Статус оплаты"] != "Отменен") & 
                (df["Технический счет"] != "Да") & 
                (df["Закрытие заказа"] != "Да") & 
                (~df["Код"].isin(exclude_kod)) & 
                (df["Номенклатура"] != "агентские услуги"))

        df = df[filters]
        
        cols_to_check = ["Счет", "Код"]
        df = df[~df[cols_to_check].isnull().apply(lambda row: all(row), axis=1)]
        
        df["Цена 1С"] = np.round(df["Сумма 1С"] / df["Количество"], 2).fillna(0).astype(float)
        df["Документ"] = "-"
        
        corr_name = {"Розничный покупатель": "Yandex", 
                            "ЯНДЕКС ООО": "Yandex", 
                            "ЯНДЕКС МАРКЕТ ООО": "Yandex", 
                            "ВАЙЛДБЕРРИЗ ООО": "Wildberries", 
                            "РВБ ООО": "Wildberries", 
                            "ИНТЕРНЕТ РЕШЕНИЯ ООО": "OZON", 
                            "МАРКЕТПЛЕЙС ООО": "СберМегаМаркет" }
        df["Контрагент"] = df["Контрагент"].replace(corr_name)
        
        df["Курс взаиморасчетов"] = df["Курс взаиморасчетов"].fillna(1.0)
    
        conditions = [df["Вид номенклатуры"] == "Услуги",
                                (df["Контрагент"].str.strip() == "OZON") & (df["Договор.Код"].str.strip() == "ОП-000644") & (df["Статус"] == "Заказ"),
                                (df["Контрагент"].str.strip() == "OZON") & (df["Договор.Код"].str.strip() == "ОП-000953") & (df["Статус"] == "Заказ"),
                                (df["Контрагент"].str.strip() != "OZON") & (df["Статус"] == "Резерв"),]
        
        choices = ["9.0. Счет (услуги)", 
                            "9.0. Счет (ОЗОН комм-р)", 
                            "9.0. Счет (ОЗОН 1P)",
                            "9.0. Счет (резерв)"]
        df["Тип документа"] = np.select(conditions, choices, default="9.0. Счет (не отгружено)")
        df['Вид документа'] = 'Счет'
        
        conditions = [
            df["Тип документа"] == "9.0. Счет (не отгружено)",
            df["Тип документа"] == "9.0. Счет (услуги)",
            df["Тип документа"] == "9.0. Счет (резерв)",
            df["Тип документа"] == "9.0. Счет (ОЗОН 1P)",
            df["Тип документа"] == "9.0. Счет (ОЗОН комм-р)"]

        choices = [
            "Заказ",
            'Услуги',
            'Резерв',
            "ОЗОН 1P", 
            "ОЗОН комиссионер"]

        df["Вид операции"] = np.select(conditions, choices, default="")

        df["Кол-во дней на оплату"] = np.where( 
                (df["Договор"] == "blank") | (df["Условие оплаты"] == "blank"),
                30, 
                (pd.to_datetime(df["Плановая дата оплаты"]) - pd.to_datetime(df["Дата счета"])).dt.days 
            )
        
        agg_columns = ['Количество', 'Сумма 1С']
        group_columns = ['Счет', 'Дата счета', 'Код', 'Цена 1С']

        # Определяем остальные колонки
        other_columns = df.columns.difference(group_columns + agg_columns)
        df_grouped = df.groupby(group_columns, as_index=False).agg({'Количество': 'sum', 'Сумма 1С': 'sum'})
        
        for col in other_columns:
            df_grouped[col] = df.groupby(group_columns)[col].first().values

        df = df_grouped.copy()
        
        # Проверка продуктов
        self._check_products(df)
        
        # Проверка клиентов
        self._check_customers(df, 'Контрагент.Код')
        
        # Проверка HYUNDAI дилеров
        self._check_hyundai_dealers(df)
        
        # Проверка договоров
        self._check_contracts(df, 'Договор.Код', 'Контрагент.Код')
        
        df["ДокОсн"] = "-"
        df["Дата ДокОсн"] = None
        df["Сборка"] = "-"
        df["Приоритет"] = df["Приоритет"].fillna("-")
        
        СпецЗаказы = self.read_special_orders(AddCosts_File)
        
        error_file_name = "ERRORs_Spec_Orders_Orders.xlsx"
        keys_spec = set(zip(СпецЗаказы['Счет'], СпецЗаказы['Дата счета'], СпецЗаказы['Код']))
        mask = df.apply(lambda row: (row['Счет'], row['Дата счета'], row['Код']) in keys_spec, axis=1)

        df_to_process = df[mask].copy()
        processed_df = self.analyze_special_deliveries(df_to_process, СпецЗаказы, error_file_name)
        df_not_processed = df[~mask].copy()

        df = pd.concat([processed_df, df_not_processed], ignore_index=True)

        columns_to_check = [
            'к_Транспорт (перемещ), л',
            'к_Хранение, л',
            'к_Ст-ть Денег, л'
        ]

        for col in columns_to_check:
            if col not in df.columns:
                df[col] = pd.Series(dtype='float64')

        df[columns_to_check] = df[columns_to_check].fillna(1.0).astype(float)
        
        df["Дата"] = pd.to_datetime(df["Дата"], format='%d.%m.%Y', errors="coerce")
        df["Дата счета"] = pd.to_datetime(df["Дата счета"], format='%d.%m.%Y', errors="coerce")
        df["Дата ДокОсн"] = pd.to_datetime(df["Дата ДокОсн"], format='%d.%m.%Y', errors="coerce")
        df["Дата Поставки"] = pd.to_datetime(df["Дата Поставки"], format='%d.%m.%Y', errors="coerce")
        df["Order N Поставки"] = df["Order N Поставки"].astype(str)
        
        df['DocType_id'] = df.apply(lambda row: self._get_doc_type_id(row.get('Вид документа', ''), row.get('Вид операции', ''), row.get('Тип документа', '')), axis=1)
        
        # ДОБАВИТЬ ПОДБОР Manager_id (после подбора DocType_id)
        if 'Договор.Менеджер' in df.columns:
            managers = db.query(Manager.AM_1C_Name, Manager.id).all()
            manager_dict = {m.AM_1C_Name: m.id for m in managers if m.AM_1C_Name}
            
            df['Manager_id'] = df['Договор.Менеджер'].map(manager_dict)

        column_mapping = {
            'Счет': 'Bill',
            'Дата счета': 'Bill_Date',
            'Статус': 'Status',
            'Контрагент.Код': 'Customer_id',
            'Контрагент': 'Customer_Name',
            'Код': 'Material_id',
            'Количество': 'Qty',
            'Сумма 1С': 'Amount_1C',
            '% НДС': 'VAT',
            'Валюта': 'Currency',
            'Грузополучатель': 'Recipient',
            'Грузополучатель.Код': 'Recipient_code',
            'Дата резерва': 'Reserve_date',
            'Дни резерва': 'Reserve_days',
            'Договор': 'Contract',
            'Договор.Код': 'Contract_id',
            'Договор.Менеджер': 'Manager',
            'Документ': 'Document',
            'Дата': 'Date',
            'Заказ.Комментарий': 'Comment',
            'Кол-во дней на оплату': 'Days_for_Pay',
            'Курс взаиморасчетов': 'FX_rate_1C',
            'Плановая дата оплаты': 'Plan_Pay_Day',
            'Постоплата%': 'Post_payment',
            'Приоритет': 'Priority',
            'Склад': 'Stock',
            'Способ доставки': 'Delivery_method',
            'Статус оплаты': 'Pay_status',
            'Условие оплаты': 'Payment_term',
            'ДокОсн': 'Doc_based',
            'Дата ДокОсн': 'Date_Doc_based',
            'Сборка': 'Sborka',
            'Спец поставка': 'Spec_Order',
            'Док Поставки': 'Purchase_doc',
            'Дата Поставки': 'Purchase_date',
            'Поставщик.Код': 'Supplier_id',
            'Order N Поставки': 'Order'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Преобразование дат
        date_columns = ['Bill_Date', 'Reserve_date', 'Date', 'Plan_Pay_Day', 'Date_Doc_based', 'Purchase_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df

    def read_purchase_order_data(self):
        """Чтение данных о заказах поставщиков"""
        purchase_order_df = pd.DataFrame()
        
        purch_types = {
            "Suppl Inv N": str, "Order N": str, "Артикул": str, "Упаковка": float, 
            "Вес Нетто кг": float, "% НДС": str, "Кол-во, шт": float, "Кол-во, л": float, 
            "Курс оплаты": float, "Цена шт, у.е.": float, "Цена л, у.е.": float, 
            "Цена без НДС, руб/л": float, "Количество": float, "Сумма без НДС, руб": float, 
            "Транспорт м.н.": float, "Тамож. Пошлина": float, "Тамож. оформление": float, 
            "Комиссия банка": float, "Агентские": float, "Доп услуги": float, 
            "Акциз": float, "ЭкоСбор": float, "Погрузка/Выгрузка": float, 
            "Себ-ть л": float, "Себ-ть шт": float, "Себ-ть партии": float, 
            "итого Себ-ть л с НДС": float, "итого Себ-ть шт с НДС": float, 
            "итого Себ-ть партии с НДС": float, "Себ-ть л c деньгами и": float, 
            "Себ-ть шт c деньгами и складом": float, 
            "Себ-ть партии c деньгами и складом": float, "Статус": str, 
            "Кол-во после спец поставки": float
        }
        
        try:
            purchase_order_df = pd.read_excel(AddCosts_File, sheet_name="Закупки в пути", skiprows=1, dtype=purch_types)
            purchase_order_df = purchase_order_df[purchase_order_df["Статус"] == "transit"]
            purchase_order_df = purchase_order_df.drop(columns=["Дата"])
            purchase_order_df["Дата"] = datetime.date.today()
            purchase_order_df["Дата"] = pd.to_datetime(purchase_order_df["Дата"])
        except Exception as e:
            self.show_error_message(f"Ошибка при чтении файла заказов поставщиков: {e}")
            return pd.DataFrame()
        
        if purchase_order_df.empty:
            return pd.DataFrame()
        
        # Обработка данных
        purchase_order_df = self._process_purchase_order_data(purchase_order_df)
        return purchase_order_df

    def _process_purchase_order_data(self, df):
        """Обработка данных о заказах поставщиков"""
        # Переименование колонок согласно соответствию
        df = df[df['Статус'].isin(['transit', 'order'])].assign(
                Status=lambda x: x['Статус'].map({
                    'transit': 'Закупки (транзит)', 
                    'order': 'Закупки (заказ)'
                })
            )
        print(df)
        # Проверка продуктов
        self._check_products(df)
        
        column_mapping = {
            'Дата': 'Date',
            'Документ': 'Document',
            'Контрагент.Код': 'Supplier_id',
            'Контрагент': 'Supplier_Name_report',
            'Supplier 1': 'Supplier1',
            'Supplier 2': 'Supplier2',
            'Order N': 'Order',
            'Shipment #': 'Shipment',
            'Код': 'Material_id',
            '% НДС': 'VAT',
            'Валюта': 'Currency',
            'Количество': 'Qty',
            'Сумма 1С': 'Amount_1C',
            'Цена 1С': 'Price_1C',
            'Кол-во, шт': 'Qty_pcs',
            'Кол-во, л': 'Qty_lt',
            'Курс оплаты': 'Payment_FX',
            'Цена шт, у.е.': 'Price_pcs_Curr',
            'Цена л, у.е.': 'Price_lt_Curr',
            'Цена без НДС, руб/л': 'Price_wo_VAT_Rub',
            'Сумма без НДС, руб': 'Amount_wo_VAT_Rub',
            'Транспорт м.н.': 'Transport_mn',
            'Тамож. Пошлина': 'Customs_fee',
            'Тамож. оформление': 'Customs_docs',
            'Комиссия банка': 'Bank_fee',
            'Агентские': 'Agency',
            'Доп услуги': 'Add_Services',
            'Акциз': 'ED',
            'ЭкоСбор': 'Eco_fee',
            'Перемещ': 'Movement_fee',
            'Погрузка/Выгрузка': 'Load_Unload',
            'Себ-ть л': 'LPC_purchase_lt',
            'Себ-ть шт': 'LPC_purchase_pcs',
            'Себ-ть партии': 'LPC_purchase_amount',
            'Кол-во после спец поставки': 'Qty_after_spec_order',
            'Себ-ть партии после спец поставки': 'LPC_purchase_after_spec_order'
        }
        
        df = df.rename(columns=column_mapping)
        print(df)
        # Преобразование дат
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        df['DocType_id'] = df.apply(lambda row: self._get_doc_type_id(
            document="Закупка",
            transaction="Транзит" if row["Status"] == "Закупки (транзит)" else "Заказ",
            doc_type="1.0. Поступление (транзит)" if row["Status"] == "Закупки (транзит)" else "1.0. Поступление (заказ)"
        ), axis=1)
        
        # Проверка поставщиков
        df = self._check_suppliers(df, 'Supplier_id')
        
        return df

    def read_special_orders(self, AddCosts_File):
        """Чтение данных специальных заказов из Excel"""
        dtype_спецзак = {"Артикул": str, "Order N": str}
        СпецЗаказы = pd.read_excel(AddCosts_File, sheet_name="Заказы исключения", dtype=dtype_спецзак)
        СпецЗаказы["Дата счета"] = pd.to_datetime(СпецЗаказы["Дата счета"], format="%d.%m.%Y", errors="coerce")
        СпецЗаказы["Дата Поставки"] = pd.to_datetime(СпецЗаказы["Дата Поставки"], format="%d.%m.%Y", errors="coerce")
        СпецЗаказы = СпецЗаказы.drop(columns=["merge сч-прод"])
        СпецЗаказы[["к_Транспорт (перемещ), л", "к_Хранение, л", "к_Ст-ть Денег, л"]] = СпецЗаказы[["к_Транспорт (перемещ), л", "к_Хранение, л", "к_Ст-ть Денег, л"]].fillna(0).astype(float)
        СпецЗаказы = СпецЗаказы.sort_values(by=["Счет", "Дата счета", "Артикул", "СФ", "Кол-во в заказе, шт"], ascending=[True, True, True, True, True])
        
        return СпецЗаказы
    
    def analyze_special_deliveries(self, df, СпецЗаказы, error_file_name):
        """
        Анализирует специальные поставки, сопоставляя данные из DataFrame (df) с данными из DataFrame СпецЗаказы.
        """
        # Инициализация колонок
        df['Спец поставка'] = 'нет'
        df['Док Поставки'] = None
        df['Дата Поставки'] = None
        df['Поставщик.Код'] = None
        df['Поставщик'] = None
        df['Order N Поставки'] = None
        df['к_Транспорт (перемещ), л'] = None
        df['к_Хранение, л'] = None
        df['к_Ст-ть Денег, л'] = None

        # 1. Создаем мультииндекс в СпецЗаказы
        СпецЗаказы = СпецЗаказы.set_index(['Счет', 'Дата счета', 'Код'], drop=False)
        СпецЗаказы = СпецЗаказы.sort_index()

        new_rows = []
        rows_to_drop = []
        matched_data = []  # Список для хранения подобранных данных для записи в Excel

        # Итерируемся по строкам DataFrame напрямую, используя iterrows()
        for index, row in df.iterrows():
            try:
                счет = row['Счет']
                дата_счета = row['Дата счета']
                код = row['Код']
                # Проверяем, есть ли соответствия в СпецЗаказы по счету, дате счета, и коду
                try:
                    group = СпецЗаказы.loc[(счет, дата_счета, код)]
                    if isinstance(group, pd.Series):  # Обработка, если возвращается Series (одна строка)
                        group = pd.DataFrame([group])  # Преобразуем в DataFrame
                except KeyError:
                    # Нет соответствий в СпецЗаказы, оставляем 'Спец поставка' = 'нет'
                    continue

                num_rows = len(group)  # Количество строк для данного счета, даты и кода

                if num_rows == 1:
                    # 1. Если для счета только одна строка
                    spec_row = group.iloc[0]
                    # Обновляем исходный df напрямую
                    df.loc[index, 'Док Поставки'] = spec_row['Док Поставки']
                    df.loc[index, 'Дата Поставки'] = spec_row['Дата Поставки']
                    df.loc[index, 'Поставщик.Код'] = spec_row['Поставщик.Код']
                    df.loc[index, 'Поставщик'] = spec_row['Поставщик']
                    df.loc[index, 'Order N Поставки'] = spec_row['Order N Поставки']
                    df.loc[index, 'к_Транспорт (перемещ), л'] = spec_row['к_Транспорт (перемещ), л']
                    df.loc[index, 'к_Хранение, л'] = spec_row['к_Хранение, л']
                    df.loc[index, 'к_Ст-ть Денег, л'] = spec_row['к_Ст-ть Денег, л']
                    # Определяем 'Спец поставка'
                    if spec_row['Поставщик.Код'] != 'no':
                        df.loc[index, 'Спец поставка'] = 'да'
                    else:
                        df.loc[index, 'Спец поставка'] = 'нет'
                    # print(f"1стр  {row['Документ']} : {spec_row['Кол-во в заказе, шт']}")
                else:
                    # 2. Если для счета больше одной строки
                    row_processed = False
                    remaining_quantity = row['Количество']  # Сколько осталось "распределить" из исходной строки

                    # 2.1 Обработка строк с  СФ != '-'
                    valid_specs = group[group['СФ'] != '-']

                    if not valid_specs.empty:
                        #  Проверяем соответствие "Документ" и "СФ" (Счет-фактура) и "Дата"
                        matching_specs = valid_specs[
                            (row['Документ'] == valid_specs['СФ']) &
                            (row['Дата'] == valid_specs['Дата'])
                        ]
                        # print(f"{row['Документ']} {row['Счет']} {row['Код']} ")
                        if not matching_specs.empty:
                            # 2.1.1 Если есть подходящие строки
                            # Создаем новые строки
                            for i, spec_row in matching_specs.iterrows():
                                # Создаем новую строку на основе текущей строки df
                                new_row = row.copy()
                                new_row['Количество'] = spec_row['Кол-во в заказе, шт']
                                new_row['Сумма 1С'] = row['Сумма 1С'] / row['Количество'] * spec_row['Кол-во в заказе, шт']
                                # Подтягиваем данные из СпецЗаказы
                                new_row['Док Поставки'] = spec_row['Док Поставки']
                                new_row['Дата Поставки'] = spec_row['Дата Поставки']
                                new_row['Поставщик.Код'] = spec_row['Поставщик.Код']
                                new_row['Поставщик'] = spec_row['Поставщик']
                                new_row['Order N Поставки'] = spec_row['Order N Поставки']
                                new_row['к_Транспорт (перемещ), л'] = spec_row['к_Транспорт (перемещ), л']
                                new_row['к_Хранение, л'] = spec_row['к_Хранение, л']
                                new_row['к_Ст-ть Денег, л'] = spec_row['к_Ст-ть Денег, л']
                                # print(f"сф != -  кол и спец равны {row['Документ']} {row['Счет']} {row['Код']}: {new_row['Количество']}")
                                # Определяем 'Спец поставка'
                                if spec_row['Поставщик.Код'] != 'no':
                                    new_row['Спец поставка'] = 'да'
                                else:
                                    new_row['Спец поставка'] = 'нет'

                                new_rows.append(new_row)
                                rows_to_drop.append(index)
                                remaining_quantity -= spec_row['Кол-во в заказе, шт']
                                # Устанавливаем флаг, что строка была обработана
                                row_processed = True

                    # 2.2 Обработка строк с СФ == '-' (ВЫПОЛНЯЕТСЯ ТОЛЬКО, ЕСЛИ СТРОКА ЕЩЕ НЕ БЫЛА ОБРАБОТАНА)
                    if not row_processed:

                        no_sf_specs = group[group['СФ'] == '-'].copy()

                        for spec_index, spec_row in no_sf_specs.iterrows():  # Перебираем каждую строку СпецЗаказы
                            spec_quantity = spec_row['Кол-во в заказе, шт']

                            if remaining_quantity <= 0:
                                break  # Если все количество уже распределено, выходим из цикла

                            new_row = row.copy()  # Создаем новую строку для каждой строки из СпецЗаказы

                            # Определяем, сколько взять из оставшегося количества
                            quantity_to_take = min(remaining_quantity, spec_quantity)
                            new_row['Количество'] = quantity_to_take
                            new_row['Сумма 1С'] = row['Сумма 1С'] / row['Количество'] * quantity_to_take

                            new_row['Док Поставки'] = spec_row['Док Поставки']
                            new_row['Дата Поставки'] = spec_row['Дата Поставки']
                            new_row['Поставщик.Код'] = spec_row['Поставщик.Код']
                            new_row['Поставщик'] = spec_row['Поставщик']
                            new_row['Order N Поставки'] = spec_row['Order N Поставки']
                            new_row['к_Транспорт (перемещ), л'] = spec_row['к_Транспорт (перемещ), л']
                            new_row['к_Хранение, л'] = spec_row['к_Хранение, л']
                            new_row['к_Ст-ть Денег, л'] = spec_row['к_Ст-ть Денег, л']
                            
                            if spec_row['Поставщик.Код'] != 'no':
                                new_row['Спец поставка'] = 'да'
                            else:
                                new_row['Спец поставка'] = 'нет'

                            # print(f"сф = - кол-во : {new_row['Количество']}, Спец = {spec_quantity}")
                            new_rows.append(new_row)

                            remaining_quantity -= quantity_to_take  # Уменьшаем оставшееся количество
                            rows_to_drop.append(index)
            except Exception as e:
                print(f"Произошла ошибка на индексе {index}: {e}")

        # Удаляем старые строки из ИСХОДНОГО DataFrame (df)
        if rows_to_drop:
            df.drop(rows_to_drop, inplace=True)

        # Добавляем новые строки в df
        if new_rows:
            df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

        # Создаем DataFrame из списка matched_data и записываем в Excel
        if matched_data:
            matched_df = pd.DataFrame(matched_data)
            matched_df.to_excel(error_file_name, index=False)
            self.show_error_message("В специальных заказах не найдены счет-фактуры. Проверьте файл ошибок.")

        # Возвращаем DataFrame
        return df
    
    def get_marketplace_data(self, start_date):
        """Получение данных Marketplace с информацией из DOCType и переименованными колонками"""
        try:
            # Получаем ВСЕ данные из Marketplace с фильтром по дате
            marketplace_data = db.query(Marketplace).filter(
                Marketplace.Date >= start_date
            ).all()
            
            # Получаем словарь DocType для быстрого доступа
            doc_types = db.query(DOCType).all()
            doc_type_dict = {dt.id: dt for dt in doc_types}
            
            managers = db.query(Manager).all()
            manager_dict = {m.id: m for m in managers}
            
            # Преобразуем в список словарей ВСЕ поля из Marketplace + добавляем информацию из DOCType
            marketplace_list = []
            for m in marketplace_data:
                doc_type_info = doc_type_dict.get(m.DocType_id)
                manager_info = manager_dict.get(m.Manager_id)
                
                marketplace_list.append({
                    # Основные поля Marketplace
                    'Document': m.Document,  # Документ
                    'Date': m.Date,  # Дата
                    'Qty': self.convert_decimal_to_float(m.Qty),  # Количество
                    'Amount_1C': self.convert_decimal_to_float(m.Amount_1C),  # Сумма 1С
                    'Price_1C': self.convert_decimal_to_float(m.Price_1C),  # Цена 1С
                    'Payment_terms': m.Payment_terms,  # Условие оплаты
                    'Post_payment': self.convert_decimal_to_float(m.Post_payment),  # Постоплата%
                    'Plan_pay_Date': m.Plan_pay_Date,  # Плановая дата оплаты
                    'Stock': m.Stock,  # Склад
                    'UoM': m.UoM,  # Единица измерения
                    'Currency': m.Currency,  # Валюта
                    'FX_rate': self.convert_decimal_to_float(m.FX_rate),  # Курс взаиморасчетов
                    'VAT': m.VAT,  # % НДС
                    
                    # Внешние ключи
                    'Material_id': m.Material_id,
                    'Customer_id': m.Customer_id,
                    'Manager_id': m.Manager_id,
                    'Contract_id': m.Contract_id,
                    'DocType_id': m.DocType_id,
                    'Договор.Менеджер': manager_info.AM_1C_Name if manager_info else None,
                    # Информация из DOCType
                    'Вид документа': doc_type_info.Document if doc_type_info else None,
                    'Вид операции': doc_type_info.Transaction if doc_type_info else None,
                    'Тип документа': doc_type_info.Doc_type if doc_type_info else None,
                    
                })
            
            # Создаем DataFrame
            if marketplace_list:
                marketplace_df = pd.DataFrame(marketplace_list)
                
                # Переименовываем колонки согласно комментариям
                column_mapping = {
                    'Document': 'Документ',
                    'Date': 'Дата',
                    'Qty': 'Количество',
                    'Amount_1C': 'Сумма 1С',
                    'Price_1C': 'Цена 1С',
                    'Payment_terms': 'Условие оплаты',
                    'Post_payment': 'Постоплата%',
                    'Plan_pay_Date': 'Плановая дата оплаты',
                    'Stock': 'Склад',
                    'UoM': 'Единица измерения',
                    'Currency': 'Валюта',
                    'FX_rate': 'Курс взаиморасчетов',
                    'VAT': '% НДС',

                    'Material_id': 'Код',
                    'Customer_id': 'Контрагент.Код',
                    'Manager_id': 'Manager_id',
                    'Contract_id': 'Договор.Код',
                }
                
                marketplace_df = marketplace_df.rename(columns=column_mapping)
                marketplace_df[['Количество', 'Сумма 1С', 'Цена 1С', 'Курс взаиморасчетов', 'Постоплата%']] = marketplace_df[[
                        'Количество', 'Сумма 1С', 'Цена 1С', 'Курс взаиморасчетов', 'Постоплата%']].astype(float)
                
                return marketplace_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            self.show_error_message(f"Ошибка при получении данных Marketplace: {str(e)}")
            return pd.DataFrame()

    def _check_hyundai_dealers(self, sales_df):
        """Проверка HYUNDAI дилеров"""
        try:
            # Чтение данных о дилерах из БД
            dealers = db.query(Hyundai_Dealer).all()
            dealer_codes = {dealer.Dealer_code: dealer.Name for dealer in dealers}
            
            # Проверка для контрагента ОП-000291
            hyundai_sales = sales_df[sales_df["Контрагент.Код"] == "ОП-000291"]
            error_find = hyundai_sales[
                (hyundai_sales["Грузополучатель.Код"] != "-") & 
                (~hyundai_sales["Грузополучатель.Код"].isin(dealer_codes.keys()))
            ]
            
            if not error_find.empty:
                self.show_error_message("В продажах найден новый дилер HYUNDAI. Проверьте файл ERRORs_Sales_new_HYUNDAI.xlsx")
                error_find = error_find.drop_duplicates(subset=["Грузополучатель.Код"])[
                    ["Грузополучатель.Код", "Грузополучатель", "Регистратор.Комментарий"]
                ]
                error_find.to_excel("ERRORs_Sales_new_HYUNDAI.xlsx", index=False)
                
        except Exception as e:
            self.show_error_message(f"Ошибка при проверке HYUNDAI дилеров: {e}")

    def _check_products(self, df):
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
        missing_products = missing_df[['Артикул', 'Код', 'Продукт + упаковка']].drop_duplicates()
        
        # Формируем сообщение с информацией об отсутствующих продуктах
        msg = "Следующие продукты отсутствуют в БД:\n\n"
        msg += "\n".join(f"{row['Артикул']}, {row['Код']}, {row['Продукт + упаковка']}" 
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
                    still_missing_products = still_missing_df[['Артикул', 'Код', 'Продукт + упаковка']].drop_duplicates()
                    
                    msg = "Следующие продукты все еще отсутствуют в БД и будут пропущены:\n\n"
                    msg += "\n".join(f"{row['Артикул']}, {row['Код']}, {row['Продукт + упаковка']}" 
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

    def _check_customers(self, df, customer_id_column):
        """Проверка клиентов в БД с автоматическим обновлением из файлов"""
        try:
            # Получение всех клиентов из БД
            customers = db.query(Customer.id, Customer.Customer_name).all()
            customer_dict = {cust[0]: cust[1] for cust in customers}
            
            # Проверяем, есть ли столбец с ID клиента в DataFrame
            if customer_id_column not in df.columns:
                self.show_error_message(f"Столбец {customer_id_column} не найден в DataFrame")
                return df
            
            # Создаем временный столбец для проверки
            df["Контрагент.ALLDATA"] = df[customer_id_column].map(customer_dict)
            df["Контрагент.ALLDATA"] = df["Контрагент.ALLDATA"].fillna("не найден")
            
            # Проверка новых клиентов
            error_find = df[df["Контрагент.ALLDATA"] == "не найден"]
            
            if not error_find.empty:
                # Получаем уникальные ID отсутствующих клиентов
                missing_customer_ids = error_find[customer_id_column].unique()
                
                # ИСПРАВЛЕНИЕ: проверяем длину массива вместо самого массива
                if len(missing_customer_ids) > 0:
                    # ПЕРВЫЙ ЭТАП: Проверяем в файле All_data_file
                    try:
                        df_all_data = pd.read_excel(All_data_file, sheet_name='Customers', dtype={'Контрагент.ИНН': str})
                        
                        # Ищем отсутствующих клиентов в файле All_data_file
                        found_in_all_data = df_all_data[df_all_data['Контрагент.Код'].isin(missing_customer_ids)]
                        
                        if not found_in_all_data.empty:
                            # Подготовка данных из All_data_file
                            column_map_all_data = {
                                'Контрагент.ИНН': 'INN',
                                'Контрагент.Код': 'id',
                                'Контрагент': 'Customer_name',
                                'Сектор': 'Sector',
                                'Тип цен': 'Price_type',
                                'Холдинг': 'Holding'
                            }
                            
                            # Отбираем только нужные колонки, если они существуют
                            available_columns = [col for col in column_map_all_data.keys() if col in found_in_all_data.columns]
                            column_map_filtered = {k: v for k, v in column_map_all_data.items() if k in available_columns}
                            
                            df_cust_to_save = found_in_all_data.rename(columns=column_map_filtered)[list(column_map_filtered.values())]
                            
                            # Очистка данных
                            df_cust_to_save["Customer_name"] = df_cust_to_save['Customer_name'].str.replace('не исп_', '', regex=False)
                            if 'Holding' in df_cust_to_save.columns:
                                df_cust_to_save["Holding"] = df_cust_to_save['Holding'].str.replace('не исп_', '', regex=False)
                            
                            # Заполняем пропущенные значения
                            if 'Sector' in df_cust_to_save.columns:
                                df_cust_to_save['Sector'] = df_cust_to_save['Sector'].fillna("-")
                            if 'Price_type' in df_cust_to_save.columns:
                                df_cust_to_save['Price_type'] = df_cust_to_save['Price_type'].fillna("-")
                            if 'Holding' in df_cust_to_save.columns:
                                df_cust_to_save["Holding"] = df_cust_to_save["Holding"].fillna(df_cust_to_save['Customer_name'])
                            
                            print("Данные для сохранения из All_data_file:")
                            print(df_cust_to_save.head())
                            
                            # ВАЖНОЕ ИСПРАВЛЕНИЕ: используем прямые методы сохранения вместо CustomerPage
                            self._save_customer_data(df_cust_to_save.to_dict('records'))
                            
                            # Обновляем список найденных ID
                            found_ids = found_in_all_data['Контрагент.Код'].unique()
                            missing_customer_ids = list(set(missing_customer_ids) - set(found_ids))
                            print("Осталось найти после All_data_file:", missing_customer_ids)
                            
                    except Exception as e:
                        self.show_error_message(f"Ошибка при чтении файла All_data_file: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    # ВТОРОЙ ЭТАП: Если еще есть отсутствующие клиенты, проверяем в файле 1С
                    if len(missing_customer_ids) > 0:
                        try:
                            df_cust1c = pd.read_excel(Customer_file, sheet_name=0, dtype={'ИНН': str})
                            
                            # ИСПРАВЛЕНО: используем отдельные условия вместо & в одном выражении
                            mask1 = df_cust1c["Это группа"] == 'Нет'
                            mask2 = df_cust1c['Код'].isin(missing_customer_ids)
                            df_cust1c = df_cust1c[mask1 & mask2]
                            
                            if not df_cust1c.empty:
                                # Подготовка данных 1С
                                column_map_1c = {
                                    'Код': 'id',
                                    'Наименование в программе': 'Customer_name',
                                    'ИНН': 'INN',
                                    'Холдинг': 'Holding',
                                    'Сектор': 'Sector',
                                    'Тип цен': 'Price_type',
                                }
                                
                                # Отбираем только нужные колонки, если они существуют
                                available_columns = [col for col in column_map_1c.keys() if col in df_cust1c.columns]
                                column_map_filtered = {k: v for k, v in column_map_1c.items() if k in available_columns}
                                
                                df_cust1c = df_cust1c.rename(columns=column_map_filtered)[list(column_map_filtered.values())]
                                
                                # Очистка данных
                                df_cust1c["Customer_name"] = df_cust1c['Customer_name'].str.replace('не исп_', '', regex=False)
                                if 'Holding' in df_cust1c.columns:
                                    df_cust1c["Holding"] = df_cust1c['Holding'].str.replace('не исп_', '', regex=False)
                                
                                # Заполняем пропущенные значения
                                if 'Sector' in df_cust1c.columns:
                                    df_cust1c['Sector'] = df_cust1c['Sector'].fillna("-")
                                if 'Price_type' in df_cust1c.columns:
                                    df_cust1c['Price_type'] = df_cust1c['Price_type'].fillna("-")
                                if 'Holding' in df_cust1c.columns:
                                    df_cust1c["Holding"] = df_cust1c["Holding"].fillna(df_cust1c['Customer_name'])
                                
                                # ВАЖНОЕ ИСПРАВЛЕНИЕ: используем прямые методы сохранения вместо CustomerPage
                                self._save_customer_data(df_cust1c.to_dict('records'))
                                
                                error_df.to_excel("ERRORs_Customer_New.xlsx", index=False)
                                self.show_message(f"Обнаружены новые клиенты.\n"
                                        f"Данные сохранены в файл ERRORs_Customer_New.xlsx")
                                # Обновляем список найденных ID
                                found_ids = df_cust1c['id'].unique()
                                missing_customer_ids = list(set(missing_customer_ids) - set(found_ids))

                        
                        except Exception as e:
                            self.show_error_message(f"Ошибка при чтении файла клиентов 1С: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    # Обновляем словарь клиентов после сохранения
                    customers = db.query(Customer.id, Customer.Customer_name).all()
                    customer_dict = {cust[0]: cust[1] for cust in customers}
                    
                    # ВАЖНО: ОБНОВЛЯЕМ ДАННЫЕ В ТЕКУЩЕМ DataFrame
                    df["Контрагент.ALLDATA"] = df[customer_id_column].map(customer_dict)
                    df["Контрагент.ALLDATA"] = df["Контрагент.ALLDATA"].fillna("не найден")
                    
                    # Теперь проверяем актуальное состояние
                    current_missing = df[df["Контрагент.ALLDATA"] == "не найден"]
                    if len(current_missing) > 0:
                        # Сохраняем оставшиеся ошибки
                        error_data = []
                        for _, row in current_missing.iterrows():
                            error_row = {
                                'Контрагент.Код': row[customer_id_column],
                                'Контрагент': row.get('Контрагент', 'неизвестно'),
                                'Контрагент.ИНН': row.get('Контрагент.ИНН', 'неизвестно'),
                                'Холдинг': row.get('Холдинг', 'неизвестно'),
                                'Сектор': row.get('Сектор', 'неизвестно'),
                                'Договор.Менеджер': row.get('Договор.Менеджер', 'неизвестно')
                            }
                            error_data.append(error_row)
                        
                        error_df = pd.DataFrame(error_data)
                        error_df = error_df.drop_duplicates(subset=[customer_id_column])
                        error_df.to_excel("ERRORs_Customer_NotFound.xlsx", index=False)
                        
                        # Показываем сообщение
                        missing_count = len(current_missing[customer_id_column].unique())
                        self.show_message(f"Обнаружено {missing_count} новых клиентов. Данные обновлены из файлов.\n"
                                        f"Не найденные клиенты сохранены в файл ERRORs_Customer_NotFound.xlsx")
                        
                        # Удаляем строки с отсутствующими клиентами из конечного DataFrame
                        df = df[df["Контрагент.ALLDATA"] != "не найден"]
            
            # Удаляем временный столбец
            df = df.drop(columns=["Контрагент.ALLDATA"])
            
            return df
            
        except Exception as e:
            self.show_error_message(f"Ошибка при проверке клиентов: {e}")
            import traceback
            traceback.print_exc()
            return df

    def _check_contracts(self, df, contract_id_column, customer_id_column):
        """Проверка договоров с использованием функций из customer.py"""
        try:
            # Получение существующих договоров
            existing_contracts = {contract.id for contract in db.query(Contract).all()}
            
            # Поиск отсутствующих договоров
            missing_contracts = df[
                (df[contract_id_column].notna()) & 
                (~df[contract_id_column].isin(existing_contracts)) &
                (df[contract_id_column] != "blank")
            ]
            
            if not missing_contracts.empty:
                # Получаем уникальные ID отсутствующих договоров
                missing_contract_ids = missing_contracts[contract_id_column].unique()
                
                contract_update = CustomerPage()
                # Используем готовые функции из customer.py
                contract_data = contract_update.read_contract_file(Contract_file)
                contract_df = pd.DataFrame(contract_data)
                
                # Фильтруем только отсутствующие договоры
                contract_df = contract_df[contract_df['id'].isin(missing_contract_ids)]
                
                if not contract_df.empty:
                    # Сохраняем договоры в БД
                    contract_update.save_Contract(contract_df.to_dict('records'))
                    
                    # Обновляем список существующих договоров
                    existing_contracts = {contract.id for contract in db.query(Contract).all()}
                    
                    # Повторно проверяем отсутствующие договоры
                    missing_contracts = df[
                        (df[contract_id_column].notna()) & 
                        (~df[contract_id_column].isin(existing_contracts)) &
                        (df[contract_id_column] != "blank")
                    ]
            
            # Если все еще есть отсутствующие договоры
            if not missing_contracts.empty:
                # Сохраняем ошибки в файл
                error_find = missing_contracts.drop_duplicates(
                    subset=[customer_id_column, contract_id_column, "Документ", "Дата"]
                )[[customer_id_column, "Контрагент", "Контрагент.ИНН", 'Договор.Код', "Договор"]]
                
                error_find.to_excel("ERRORs_Contract.xlsx", index=False)
                
                # Показываем сообщение
                missing_count = len(missing_contracts[contract_id_column].unique())
                self.show_message(f"Обнаружено {missing_count} новых договоров. Данные обновлены из файла 1С.\n"
                                f"Не найденные договоры сохранены в файл ERRORs_Contract.xlsx")
                
                # Удаляем строки с отсутствующими договорами
                df = df[~df[contract_id_column].isin(missing_contracts[contract_id_column])]
                    
            return df
            
        except Exception as e:
            self.show_error_message(f"Ошибка при проверке договоров: {e}")
            return df

    def _save_customer_data(self, data):
        """Сохранение данных клиентов в БД"""
        if not data:
            return
        
        try:
            # Создаем экземпляр CustomerPage, но передаем текущую сессию
            cust_update = CustomerPage()
            
            # Вызываем методы с текущим контекстом БД
            cust_update.save_Sector(data)
            cust_update.save_Holding(data) 
            cust_update.save_Customer(data)
            
            # Явно коммитим изменения
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения клиентов: {str(e)}")

    def _check_suppliers(self, df, supplier_id_column):
        """Проверка наличия поставщиков в БД. Пропускает проверку, если столбец пустой или отсутствует."""
        # Если столбец не существует в DataFrame, пропускаем проверку
        if supplier_id_column not in df.columns:
            print(f"Столбец {supplier_id_column} отсутствует, проверка поставщиков пропущена.")
            return df
            
        # Если все значения в столбце пустые (NaN/null), пропускаем проверку
        if df[supplier_id_column].isnull().all():
            print(f"Столбец {supplier_id_column} пуст, проверка поставщиков пропущена.")
            return df
            
        # Фильтруем только строки с непустыми значениями поставщиков для проверки
        non_empty_suppliers = df[df[supplier_id_column].notna()]
        empty_suppliers = df[df[supplier_id_column].isna()]
        
        # Получаем список всех кодов поставщиков из БД
        try:
            existing_suppliers = {str(s[0]) for s in db.query(Supplier.id).all()}
        except Exception as e:
            self.show_error_message(f"Ошибка при проверке поставщиков в БД: {str(e)}")
            return pd.DataFrame()
            
        # Находим отсутствующих поставщиков только среди непустых значений
        non_empty_suppliers.loc[:, supplier_id_column] = non_empty_suppliers[supplier_id_column].astype(str)
        missing_suppliers = set(non_empty_suppliers[supplier_id_column].unique()) - existing_suppliers
        
        if missing_suppliers:
            # Показываем диалог с отсутствующими поставщиками (только реальные коды, не NaN)
            valid_missing_suppliers = [code for code in missing_suppliers if code != 'nan' and code != 'None']
            
            if valid_missing_suppliers:
                msg = f"Следующие поставщики отсутствуют в БД:\n\n"
                msg += "\n".join(f"{code}" for code in valid_missing_suppliers)
                msg += "\n\nПропустить эти записи?"
                
                reply = QMessageBox.question(
                    self, 
                    "Отсутствующие поставщики", 
                    msg,
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.No:
                    return pd.DataFrame()
                else:
                    # Удаляем строки с отсутствующими поставщиками (только реальные коды)
                    non_empty_suppliers = non_empty_suppliers[~non_empty_suppliers[supplier_id_column].isin(valid_missing_suppliers)]
        
        # Объединяем обратно отфильтрованные непустые поставщики с пустыми
        df = pd.concat([non_empty_suppliers, empty_suppliers], ignore_index=True)
        
        return df

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

    @lru_cache(maxsize=128)
    def _get_manager_id(self, manager_name):
        """Получение ID менеджера с кэшированием"""
        try:
            manager = db.query(Manager).filter(Manager.Manager_name == manager_name).first()
            if manager:
                return manager.id
            else:
                # Создаем нового менеджера, если не найден
                new_manager = Manager(Manager_name=manager_name)
                db.add(new_manager)
                db.commit()
                return new_manager.id
                
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка при получении/создании менеджера: {e}")
            return None

    def _get_model_for_table(self, table_name):
        """Получение модели SQLAlchemy по имени таблицы"""
        models = {
            "Закупки": temp_Purchase,
            "Продажи": temp_Sales,
            "Заказы клиентов": temp_Orders,
            "Заказы поставщиков": Purchase_Order
        }
        return models.get(table_name)

    def _update_temp_purchase_in_db(self, df, report_start_date):
        """Обновление временной таблицы закупок в БД с добавлением данных из Complects"""
        try:
            # Чтение данных из таблицы Complects
            complects_data = db.query(Complects).filter(Complects.Date >= report_start_date).all()
            manual_data = db.query(Complects_manual).filter(Complects_manual.Date >= report_start_date).all()
            # Преобразование данных Complects
            complects_list = [{
                'Document': c.Document,
                'Date': c.Date,
                'DocType_id': c.DocType_id,
                'Status': 'Склад',
                'Material_id': c.Material_id,
                'Stock': c.Stock,
                'Qty': self.convert_decimal_to_float(c.Qty),
                'Amount_1C': 0,
                'Currency': 'RUB',
                'VAT': '20%',
                'FX_rate_1C': 1.0,} for c in complects_data]
            
            manual_list = [{
                'Document': c.Document,
                'Date': c.Date,
                'DocType_id': c.DocType_id,
                'Status': 'Склад',
                'Material_id': c.Material_id,
                'Stock': c.Stock,
                'Qty': self.convert_decimal_to_float(c.Qty),
                'Amount_1C': 0,
                'Currency': 'RUB',
                'VAT': '20%',
                'FX_rate_1C': 1.0,} for c in manual_data]
            
            # Объединение данных
            if complects_list:
                complects_df = pd.DataFrame(complects_list)
                complects_df['Qty'] = complects_df['Qty'].astype(float)
                if not complects_df.empty:
                    df = pd.concat([df, complects_df], axis=0, ignore_index=True)
                    
            if manual_list:
                manual_df = pd.DataFrame(manual_list)
                manual_df['Qty'] = manual_df['Qty'].astype(float)
                if not manual_df.empty:
                    df = pd.concat([df, manual_df], axis=0, ignore_index=True)
            
            # Обработка числовых колонок
            numeric_columns = ['FX_rate_1C', 'Qty', 'Amount_1C']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    
            df = self._clean_dataframe(df)
                
            # Удаляем старые данные
            db.query(temp_Purchase).delete()
            
            # Подготовка данных для bulk вставки
            purchase_data = []
            for _, row in df.iterrows():
                purchase_data.append({
                    'Document': row.get('Document'),
                    'Date': row.get('Date'),
                    'DocType_id':row.get('DocType_id'),
                    'Status': row.get('Status'),
                    'Doc_based': row.get('Doc_based'),
                    'Date_Doc_based': row.get('Date_Doc_based'),
                    'Supplier_id': row.get('Supplier_id'),
                    'Material_id': row.get('Material_id'),
                    'Stock': row.get('Stock'),
                    'Currency': row.get('Currency'),
                    'VAT': row.get('VAT'),
                    'Country': row.get('Country'),
                    'GTD': row.get('GTD'),
                    'FX_rate_1C': row.get('FX_rate_1C'),
                    'Qty': row.get('Qty'),
                    'Amount_1C': row.get('Amount_1C')})
            
            # Bulk вставка
            if purchase_data:
                db.bulk_insert_mappings(temp_Purchase, purchase_data)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка при обновлении temp_Purchase: {str(e)}")
            return

    def _update_temp_sales_in_db(self, df):
        """Обновление временной таблицы продаж в БД"""
        try:
            df = self._clean_dataframe(df)
            
            db.query(temp_Sales).delete()
            
            # Подготовка данных для bulk вставки
            sales_data = []
            for _, row in df.iterrows():
                sales_data.append({
                    'Document': row.get('Document'),
                    'Date': row.get('Date'),
                    'DocType_id': row.get('DocType_id'),
                    'Status': row.get('Status'),
                    'Bill': row.get('Bill'),
                    'Bill_Date': row.get('Bill_Date'),
                    'Doc_based': row.get('Doc_based'),
                    'Date_Doc_based': row.get('Date_Doc_based'),
                    'Customer_id': row.get('Customer_id'),
                    'Customer_Name': row.get('Customer_Name'),
                    'Material_id': row.get('Material_id'),
                    'Stock': row.get('Stock'),
                    'Delivery_method': row.get('Delivery_method'),
                    'Currency': row.get('Currency'),
                    'FX_rate_1C': row.get('FX_rate') or row.get('FX_rate_1C'),
                    'Qty': row.get('Qty'),
                    'Amount_1C': row.get('Amount_1C'),
                    'VAT': row.get('VAT'),
                    'Recipient': row.get('Recipient'),
                    'Recipient_code': row.get('Recipient_code'),
                    'Contract_id': row.get('Contract_id'),
                    'Manager_id':row.get('Manager_id'),
                    'Days_for_Pay': row.get('Days_for_Pay'),
                    'Plan_Delivery_Day': row.get('Plan_Delivery_Day'),
                    'Plan_Pay_Day': row.get('Plan_Pay_Day'),
                    'Post_payment': row.get('Post_payment'),
                    'Payment_term': row.get('Payment_terms'),
                    'Priority': row.get('Priority'),
                    'Comment': row.get('Comment'),
                    'Sborka': row.get('Sborka'),
                    'Spec_Order': row.get('Spec_Order'),
                    'Purchase_doc': row.get('Purchase_doc'),
                    'Purchase_date': row.get('Purchase_date'),
                    'Order': row.get('Order'),
                    'k_Movement': row.get('k_Movement'),
                    'k_Storage': row.get('k_Storage'),
                    'k_Money': row.get('k_Money')
                })
            
            # Bulk вставка
            if sales_data:
                db.bulk_insert_mappings(temp_Sales, sales_data)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка при обновлении temp_Sales: {str(e)}")
            return

    def _update_temp_orders_in_db(self, df):
        """Обновление временной таблицы заказов в БД"""
        try:
            df = self._clean_dataframe(df)
            # Удаляем старые данные
            db.query(temp_Orders).delete()
            
            # Подготовка данных для bulk вставки
            orders_data = []
            for _, row in df.iterrows():
                orders_data.append({
                    'Bill': row.get('Bill'),
                    'Bill_Date': row.get('Bill_Date'),
                    'Status': row.get('Status'),
                    'Customer_id': row.get('Customer_id'),
                    'Customer_Name': row.get('Customer_Name'),
                    'Material_id': row.get('Material_id'),
                    'Qty': row.get('Qty'),
                    'Amount_1C': row.get('Amount_1C'),
                    'VAT': row.get('VAT'),
                    'Currency': row.get('Currency'),
                    'Recipient': row.get('Recipient'),
                    'Recipient_code': row.get('Recipient_code'),
                    'Reserve_date': row.get('Reserve_date'),
                    'Reserve_days': row.get('Reserve_days'),
                    'Contract': row.get('Contract'),
                    'Contract_id': row.get('Contract_id'),
                    'Manager': row.get('Manager'),
                    'Document': row.get('Document'),
                    'Date': row.get('Date'),
                    'Comment': row.get('Comment'),
                    'Days_for_Pay': row.get('Days_for_Pay'),
                    'FX_rate_1C': row.get('FX_rate_1C'),
                    'Plan_Pay_Day': row.get('Plan_Pay_Day'),
                    'Post_payment': row.get('Post_payment'),
                    'Priority': row.get('Priority'),
                    'Stock': row.get('Stock'),
                    'Delivery_method': row.get('Delivery_method'),
                    'Pay_status': row.get('Pay_status'),
                    'Payment_term': row.get('Payment_term'),
                    'Doc_based': row.get('Doc_based'),
                    'Date_Doc_based': row.get('Date_Doc_based'),
                    'Sborka': row.get('Sborka'),
                    'Spec_Order': row.get('Spec_Order'),
                    'Purchase_doc': row.get('Purchase_doc'),
                    'Purchase_date': row.get('Purchase_date'),
                    'Supplier_id': row.get('Supplier_id'),
                    'Order': row.get('Order'),
                    'DocType_id':row.get('DocType_id'),
                    'k_Movement': row.get('k_Movement'),
                    'k_Storage': row.get('k_Storage'),
                    'k_Money': row.get('k_Money')
                })
            
            # Bulk вставка
            if orders_data:
                db.bulk_insert_mappings(temp_Orders, orders_data)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка при обновлении temp_Orders: {str(e)}")
            return

    def _update_purchase_order_in_db(self, df):
        """Обновление таблицы заказов поставщиков в БД"""
        try:
            df = self._clean_dataframe(df)
            # Удаляем старые данные
            db.query(Purchase_Order).delete()
            
            # Подготовка данных для bulk вставки
            purchase_order_data = []
            for _, row in df.iterrows():
                purchase_order_data.append({
                    'Status': row.get('Status'),
                    'Date': row.get('Date'),
                    'Document': row.get('Document'),
                    'Supplier_id': row.get('Supplier_id'),
                    'Supplier_Name_report': row.get('Supplier_Name_report'),
                    'Supplier1': row.get('Supplier1'),
                    'Supplier2': row.get('Supplier2'),
                    'Order': row.get('Order'),
                    'Shipment': row.get('Shipment'),
                    'Material_id': row.get('Material_id'),
                    'VAT': row.get('VAT'),
                    'Currency': row.get('Currency'),
                    'Qty': row.get('Qty'),
                    'Amount_1C': row.get('Amount_1C'),
                    'Price_1C': row.get('Price_1C'),
                    'Qty_pcs': row.get('Qty_pcs'),
                    'Qty_lt': row.get('Qty_lt'),
                    'Payment_FX': row.get('Payment_FX'),
                    'Price_pcs_Curr': row.get('Price_pcs_Curr'),
                    'Price_lt_Curr': row.get('Price_lt_Curr'),
                    'Price_wo_VAT_Rub': row.get('Price_wo_VAT_Rub'),
                    'Amount_wo_VAT_Rub': row.get('Amount_wo_VAT_Rub'),
                    'Transport_mn': row.get('Transport_mn'),
                    'Customs_fee': row.get('Customs_fee'),
                    'Customs_docs': row.get('Customs_docs'),
                    'Bank_fee': row.get('Bank_fee'),
                    'Agency': row.get('Agency'),
                    'Add_Services': row.get('Add_Services'),
                    'ED': row.get('ED'),
                    'Eco_fee': row.get('Eco_fee'),
                    'Movement_fee': row.get('Movement_fee'),
                    'Load_Unload': row.get('Load_Unload'),
                    'LPC_purchase_lt': row.get('LPC_purchase_lt'),
                    'LPC_purchase_pcs': row.get('LPC_purchase_pcs'),
                    'LPC_purchase_amount': row.get('LPC_purchase_amount'),
                    'Qty_after_spec_order': row.get('Qty_after_spec_order'),
                    'LPC_purchase_after_spec_order': row.get('LPC_purchase_after_spec_order'),
                    'DocType_id':row.get('DocType_id')
                })
            
            # Bulk вставка
            if purchase_order_data:
                db.bulk_insert_mappings(Purchase_Order, purchase_order_data)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка при обновлении Purchase_Order: {str(e)}")
            return

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

    def convert_decimal_to_float(self, value):
        """Безопасное преобразование Decimal в float"""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

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





