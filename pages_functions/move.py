# moves.py
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from PySide6.QtWidgets import QFileDialog, QMessageBox, QHeaderView, QTableWidget, QMenu, QApplication, QTableWidgetItem, QWidget
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
        self.ui.btn_refresh.clicked.connect(self.refresh_data)
    
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
        """Заполнение списка месяцев"""
        try:
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            year = self.ui.line_Year.currentText()
            
            if table == "-" or year == "-":
                self._fill_combobox(self.ui.line_Mnth, ["-"])
                return
                
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_Mnth, ["-"])
                return
                
            query = db.query(extract('month', model.Date).label('month')).filter(
                extract('year', model.Date) == int(year))
                
            if doc_type != "-":
                query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                
            months = query.distinct()
            months_list = sorted(list({m[0] for m in months if m[0] is not None}))
            months_list = [str(m) for m in months_list]
            
            self._fill_combobox(self.ui.line_Mnth, ["-"] + months_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка месяцев: {str(e)}")
            self._fill_combobox(self.ui.line_Mnth, ["-"])

    def fill_customer_list(self):
        """Заполнение списка контрагентов с учетом типа документа"""
        try:
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()
            
            if table == "-":
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
                
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
                
            # Определяем типы документов, которые используют Supplier
            supplier_doc_types = [
                "1.0. Поступление",
                "1.0. Поступление (перераб)",
                "1.1. Поступление (корр-ка)",
                "7.0. Передача в переработку"
            ]
            
            # Для Movements определяем тип контрагента (Supplier или Customer)
            if model == Movements:
                if doc_type in supplier_doc_types:
                    # Используем Supplier для указанных типов документов
                    query = db.query(
                        Supplier.id.label('code'),
                        Supplier.Supplier_Name.label('name')
                    ).join(model.supplier)
                else:
                    # Для остальных типов документов используем Customer
                    query = db.query(
                        Customer.id.label('code'),
                        Customer.Customer_name.label('name')
                    ).join(model.customer)
                
                # Применяем фильтры по типу документа, году и месяцу
                if doc_type != "-":
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                
                if year != "-":
                    query = query.filter(extract('year', model.Date) == int(year))
                
                if month != "-":
                    query = query.filter(extract('month', model.Date) == int(month))
                
                customers = query.distinct().all()
                
            elif table == "WriteOff":
                # Для WriteOff всегда используем Supplier
                query = db.query(
                    Supplier.id.label('code'),
                    Supplier.Supplier_Name.label('name')
                ).join(model.supplier)
                
                if doc_type != "-":
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                
                if year != "-":
                    query = query.filter(extract('year', model.Date) == int(year))
                
                if month != "-":
                    query = query.filter(extract('month', model.Date) == int(month))
                
                customers = query.distinct().all()
                
            else:
                # Для других таблиц не заполняем список контрагентов
                self._fill_combobox(self.ui.line_customer, ["-"])
                return
            
            # Формируем список для комбобокса в формате "Код - Название"
            customers_list = [f"{c.code} - {c.name}" for c in customers if c.code is not None and c.name is not None]
            customers_list = sorted(list(set(customers_list)))  # Удаляем дубликаты
            
            self._fill_combobox(self.ui.line_customer, ["-"] + customers_list)
            
        except Exception as e:
            print(f"Ошибка при загрузке списка контрагентов: {str(e)}")
            self._fill_combobox(self.ui.line_customer, ["-"])

    def fill_product_list(self):
        """Заполнение списка продуктов с учетом типа документа и контрагента"""
        try:
            table = self.ui.line_table.currentText()
            doc_type = self.ui.line_doc_type.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()
            customer = self.ui.line_customer.currentText()
            
            if table == "-":
                self._fill_combobox(self.ui.line_product, ["-"])
                return
                
            model = self._get_model_for_table(table)
            if not model:
                self._fill_combobox(self.ui.line_product, ["-"])
                return

            # Определяем типы документов, которые используют Supplier
            supplier_doc_types = [
                "1.0. Поступление",
                "1.0. Поступление (перераб)",
                "1.1. Поступление (корр-ка)",
                "7.0. Передача в переработку"
            ]
                
            query = db.query(Product_Names.Product_name).join(Materials, Product_Names.materials)
            
            # В зависимости от модели используем правильную связь
            if model == Movements:
                query = query.join(model, Materials.movements)
                
                # Фильтр по типу документа
                if doc_type != "-":
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                    
                    # Если тип документа требует Supplier, меняем условие фильтрации
                    if doc_type in supplier_doc_types:
                        if customer != "-":
                            query = query.join(model.supplier).filter(Supplier.Supplier_Name == customer)
                    else:
                        if customer != "-":
                            query = query.join(model.customer).filter(Customer.Customer_name == customer)
                            
            elif model == WriteOff:
                query = query.join(model, Materials.write_off)
                
                if doc_type != "-":
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
                    
                if customer != "-":
                    query = query.join(model.supplier).filter(Supplier.Supplier_Name == customer)
                    
            elif model == Complects_manual:
                query = query.join(model, Materials.complects_manual)
                
                if doc_type != "-":
                    query = query.join(model.doc_type).filter(DOCType.Doc_type == doc_type)
            else:
                self._fill_combobox(self.ui.line_product, ["-"])
                return
            
            # Общие фильтры для всех моделей
            if year != "-":
                query = query.filter(extract('year', model.Date) == int(year))
            
            if month != "-":
                query = query.filter(extract('month', model.Date) == int(month))
            
            products = query.distinct()
            products_list = sorted([p[0] for p in products if p[0] is not None])
            
            self._fill_combobox(self.ui.line_product, ["-"] + products_list)
            
        except Exception as e:
            print(f"Ошибка при загрузке списка продуктов: {str(e)}")
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
                    (Supplier.id.like(f"%{cust_id}%"))
                )
        
        # Специфичные фильтры для WriteOff
        elif model == WriteOff:
            if customer != "-":
                query = query.filter(Supplier.Supplier_Name == customer)
            
            if cust_id:
                query = query.filter(Supplier.id.like(f"%{cust_id}%"))
        
        return query

    def _calculate_pcs(self, row):
        """Рассчитывает количество в штуках"""
        if row.Package_type == "комплект":
            return float(row.Qty) * float(row.Items_per_Set)
        elif row.UoM == "шт":
            return float(row.Qty)
        elif row.UoM == "т":
            return float(row.Qty) * 1000 / float(row.Package_Volume)
        else:
            return float(row.Qty) / float(row.Package_Volume)

    def _calculate_liters(self, row):
        """Рассчитывает количество в литрах"""
        if row.Package_type == "комплект":
            return float(row.Qty) * float(row.Package_Volume)
        else:
            return self._calculate_pcs(row) * float(row.Package_Volume)

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
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                if df.columns[col_idx] in numeric_cols:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    if pd.notna(value):
                        if df.columns[col_idx] == "Кол-во, шт":
                            item.setText(f"{int(value):,}".replace(",", " "))
                        else:
                            item.setText(f"{float(value):,.2f}".replace(",", " ").replace(".", ","))
                
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

    def refresh_data(self):
        """Обновление данных из файлов и загрузка в БД"""
        try:
            date_start = self.ui.date_Start.date()
            move_df = self.read_movement_data(date_start)
            
            if move_df.empty:
                self.show_message("Нет данных для обновления")
                return
            
            # Проверка наличия документов в AddSupplCost для поступлений
            self._check_purchases_in_add_suppl_cost(move_df)
            
            # Обновление данных в БД
            self._update_moves_in_db(move_df)
            
            # Обработка комплектаций и списаний
            self._process_complectations(move_df)
            self._process_write_offs(move_df)
            
            self.show_message("Данные успешно обновлены")
            self.refresh_all_comboboxes()
            
        except Exception as e:
            self.show_error_message(f"Ошибка при обновлении данных: {str(e)}")
            traceback.print_exc()

    def read_movement_data(self, date_start: QDate):
        """Чтение данных о движениях из файлов"""
        report_start_date = date_start.toPython()
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
            "Код.2": "Грузополучатель.Код"
        })
        
        # Фильтрация данных
        move_df = move_df.loc[
            (move_df["Приход"] != "Количество приход") & 
            (move_df["Приход"] != "Приход") & 
            (move_df["Дата_Время"] != "Итого")
        ]
        
        # Очистка данных
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
        
        # Фильтрация по дате
        move_df = move_df[(move_df["Дата"] >= report_start_date)]
        
        # Расчет количества
        move_df["Количество"] = np.where(move_df["Приход"].isnull(), move_df["Расход"] * -1, move_df["Приход"])
        
        # Корректировка типа документа для недостач/утилизаций
        move_df.loc[(move_df["Склад"].str.contains("Недостача")) & (~move_df["Тип документа"].isin(["2.0. Комплектация", "4.0. Реализация"])), "Тип документа"] = "5.0. Списание (недостача)"
        move_df.loc[(move_df["Склад"].str.contains("Утилизация")) & (~move_df["Тип документа"].isin(["2.0. Комплектация", "4.0. Реализация"])), "Тип документа"] = "5.0. Списание (утилизация)"
        
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

    def _check_purchases_in_add_suppl_cost(self, move_df):
        """Проверка наличия поступлений в AddSupplCost"""
        purchases = move_df[(move_df["Тип документа"] == "1.0. Поступление") & (move_df["Контрагент.Код"] != "ОП-001636")]
        
        if purchases.empty:
            return
            
        # Проверяем наличие документов в AddSupplCost
        doc_dates = purchases[["Документ", "Дата", "Контрагент.Код"]].drop_duplicates()
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
            
            error_msg = "Найдены новые поступления, отсутствующие в AddSupplCost:\n\n"
            error_msg += "\n".join(
                f"{row['Документ']}, {row['Дата']}, {row['Контрагент.Код']}" 
                for _, row in error_df.iterrows()
            )
            error_msg += "\n\nОшибки сохранены в файл ERRORs_Purchase_new.xlsx"
            
            self.show_error_message(error_msg)
            sys.exit(1)

    def _update_moves_in_db(self, move_df):
        """Обновление данных Movements в БД"""
        try:
            # Определяем тип контрагента (Supplier или Customer) на основе типа документа
            supplier_doc_types = [
                "1.0. Поступление",
                "1.0. Поступление (перераб)",
                "1.1. Поступление (корр-ка)",
                "7.0. Передача в переработку"]
            
            # Удаляем старые данные за тот же период
            min_date = move_df['Дата'].min()
            db.query(Movements).filter(Movements.Date >= min_date).delete()
            
            # Подготавливаем данные для вставки
            records = []
            for _, row in move_df.iterrows():
                record = {
                    'Date_Time': row['Дата_Время'],
                    'Document': row['Документ'],
                    'Date': row['Дата'],
                    'Doc_based': row['ДокОсн'],
                    'Date_Doc_based': row['Дата ДокОсн'],
                    'Stock': row['Склад'],
                    'Qty': row['Количество'],
                    'Recipient_code': row['Грузополучатель.Код'],
                    'Recipient': row['Грузополучатель'],
                    'Bill': row['Счет'],
                    'Bill_date': row['Дата счета'],
                    'DocType_id': self._get_doc_type_id(row['Вид документа'], row['Вид операции'], row['Тип документа']),
                    'Material_id': row['Код']}
                
                # Определяем тип контрагента
                if row['Тип документа'] in supplier_doc_types:
                    record['Supplier_id'] = row['Контрагент.Код']
                else:
                    record['Customer_id'] = row['Контрагент.Код']
                
                records.append(record)
            
            # Массовая вставка
            db.bulk_insert_mappings(Movements, records)
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления данных Movements в БД: {e}")

    def _process_complectations(self, move_df):
        """Обработка данных о комплектациях"""
        # Обрабатываем автоматические комплектации
        complect_df = move_df[
            (move_df['Тип документа'] == '2.0. Комплектация') | 
            (move_df['Тип документа'] == '5.0. Списание') | 
            (move_df['Тип документа'] == '6.0. Расход') | 
            (move_df['Тип документа'] == '7.0. Передача в переработку')
        ]
        
        if not complect_df.empty:
            self._update_complects_in_db(complect_df)
        
        # Обрабатываем ручные комплектации
        try:
            manual_complect_df = pd.read_excel(Complectation_file, sheet_name="Ручные_комплектации")
            manual_complect_df["Код"] = manual_complect_df["Код"].str.strip()
            manual_complect_df["Дата"] = pd.to_datetime(manual_complect_df["Дата"], format="%d.%m.%Y")
            manual_complect_df["Дата_Время"] = pd.to_datetime(manual_complect_df["Дата_Время"], format="%d.%m.%Y %H:%M:%S")
            manual_complect_df = manual_complect_df.astype({"Количество": "float64"})
            
            self._update_complects_manual_in_db(manual_complect_df)
        except Exception as e:
            print(f"Ошибка при обработке ручных комплектаций: {str(e)}")

    def _update_complects_in_db(self, df):
        """Обновление данных о комплектациях в БД"""
        try:
            # Удаляем старые данные за тот же период
            min_date = df['Дата'].min()
            db.query(Complects).filter(Complects.Date >= min_date).delete()
            
            # Подготавливаем данные для вставки
            records = []
            for _, row in df.iterrows():
                record = {
                    'Date_Time': row['Дата_Время'],
                    'Document': row['Документ'],
                    'Date': row['Дата'],
                    'Stock': row['Склад'],
                    'Qty': row['Количество'],
                    'DocType_id': self._get_doc_type_id(row['Вид документа'], row['Вид операции'], row['Тип документа']),
                    'Material_id': row['Код'],
                    'Complect_type': 'Автоматическая'
                }
                records.append(record)
            
            # Массовая вставка
            db.bulk_insert_mappings(Complects, records)
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления данных Complects в БД: {e}")

    def _update_complects_manual_in_db(self, df):
        """Обновление данных о ручных комплектациях в БД"""
        try:
            # Удаляем старые данные за тот же период
            min_date = df['Дата'].min()
            db.query(Complects_manual).filter(Complects_manual.Date >= min_date).delete()
            
            # Подготавливаем данные для вставки
            records = []
            for _, row in df.iterrows():
                record = {
                    'Date_Time': row['Дата_Время'],
                    'Document': row['Документ'],
                    'Date': row['Дата'],
                    'Stock': row['Склад'],
                    'Qty': row['Количество'],
                    'DocType_id': self._get_doc_type_id('Ручная комплектация', None, '2.0. Комплектация'),
                    'Material_id': row['Код'],
                    'Complect_type': 'Ручная'
                }
                records.append(record)
            
            # Массовая вставка
            db.bulk_insert_mappings(Complects_manual, records)
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления данных Complects_manual в БД: {e}")

    def _process_write_offs(self, move_df):
        """Обработка данных о списаниях с проверкой новых записей"""
        try:
            # Выбираем только списания из move_df
            write_off_mask = ((move_df["Склад"].str.contains("Недостача|Утилизация", na=False)) & (~move_df["Тип документа"].isin(["2.0. Комплектация", "4.0. Реализация"])))
            new_write_offs = move_df[write_off_mask].copy()
            
            if new_write_offs.empty:
                return

            try:
                dtype_compl = {"Артикул": str, "Упаковка": float, "Кол-во в упак": float, "Количество": float}
                
                existing_write_offs_df = pd.read_excel(Complectation_file, sheet_name="Недостачи_Утилизации", dtype=dtype_compl)
                
                # Обработка существующих данных
                existing_write_offs_df["Код"] = existing_write_offs_df["Код"].str.strip()
                existing_write_offs_df["Дата"] = pd.to_datetime(existing_write_offs_df["Дата"], format="%d.%m.%Y")
                
                # Создаем ключи для сравнения
                new_write_offs["merge_key"] = (
                    new_write_offs["Документ"] + "_" + 
                    new_write_offs["Дата"].astype(str) + "_" + 
                    new_write_offs["Код"] + "_" + 
                    new_write_offs["Склад"])
                
                existing_write_offs_df["merge_key"] = (
                    existing_write_offs_df["Документ"] + "_" + 
                    existing_write_offs_df["Дата"].astype(str) + "_" + 
                    existing_write_offs_df["Код"] + "_" + 
                    existing_write_offs_df["Склад"])
                
                # Находим действительно новые списания
                truly_new_write_offs = new_write_offs[~new_write_offs["merge_key"].isin(existing_write_offs_df["merge_key"])]
                
                if not truly_new_write_offs.empty:
                    output_columns = [
                        "Дата_Время", "Документ", "Дата", "Код", "Артикул", 
                        "Продукт + упаковка", "Склад", "Приход", "Расход", 
                        "Количество", "Комментарий", "Тип документа"]
                    
                    truly_new_write_offs[output_columns].to_excel("ERRORs_Write_OFF_new.xlsx", index=False,sheet_name="Новые списания")

                    msg = f"Обнаружено {len(truly_new_write_offs)} новых списаний. Данные сохранены в файл ERRORs_Write_OFF_new.xlsx"
                    self.show_message(msg)

                self._update_write_off_in_db(new_write_offs)
                
            except Exception as e:
                error_msg = f"Ошибка при чтении файла списаний: {str(e)}"
                print(error_msg)
                self.show_error_message(error_msg)
                traceback.print_exc()
                
                # Если не удалось прочитать файл, просто обновляем все списания
                self._update_write_off_in_db(new_write_offs)
                
        except Exception as e:
            error_msg = f"Ошибка при обработке списаний: {str(e)}"
            print(error_msg)
            self.show_error_message(error_msg)
            traceback.print_exc()

    def _update_write_off_in_db(self, write_off_df):
        """Обновление данных о списаниях в БД"""
        try:
            # Удаляем старые данные за тот же период
            min_date = write_off_df['Дата'].min()
            db.query(WriteOff).filter(WriteOff.Date >= min_date).delete()

            # Подготавливаем данные для вставки
            records = []
            for _, row in write_off_df.iterrows():
                record = {
                    'Date_Time': row['Дата_Время'],
                    'Document': row['Документ'],
                    'Date': row['Дата'],
                    'Stock': row['Склад'],
                    'Comment': row.get('Комментарий', ''),
                    'inComing': row.get('Приход', 0),
                    'outComing': row.get('Расход', 0),
                    'Qty': row['Количество'],
                    'Reporting': row.get('Отчет', ''),
                    'Doc_based': row.get('ДокОсн', ''),
                    'Date_Doc_based': row.get('Дата ДокОсн'),
                    'Order': row.get('Order N', ''),
                    'Shipment': row.get('Shipment #', ''),
                    'Suppl_Inv_N': row.get('Вход. док-т', ''),
                    'Bill': row.get('Счет', ''),
                    'Bill_date': row.get('Дата счета'),
                    'DocType_id': self._get_doc_type_id(
                        row.get('Вид документа', ''),
                        row.get('Вид операции', ''),
                        row.get('Тип документа', '')
                    ),
                    'Material_id': row['Код'],
                    'Supplier_id': row['Контрагент.Код']
                }
                records.append(record)

            # Массовая вставка
            db.bulk_insert_mappings(WriteOff, records)
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления данных WriteOff в БД: {e}")

    @lru_cache(maxsize=128)
    def _get_doc_type_id(self, document: str, transaction: str, doc_type: str) -> int:
        """Получение ID типа документа"""
        if not document:
            return None
        
        doc_type = db.query(DOCType.id).filter(
            DOCType.Document == document,
            DOCType.Transaction == transaction,
            DOCType.Doc_type == doc_type
        ).first()
        
        return doc_type[0] if doc_type else None

    def show_message(self, text):
        """Показать информационное сообщение"""
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setMinimumSize(400, 200)
        
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
        msg.setText(text)
        msg.setMinimumSize(400, 200)
        
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        def copy_text():
            QApplication.clipboard().setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()