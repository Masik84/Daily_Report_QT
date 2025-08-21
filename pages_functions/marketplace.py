import pandas as pd
import numpy as np
import xlwings as xw
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QMenu,
                              QApplication, QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from functools import lru_cache
import traceback
import os
import re
import sys
from datetime import datetime

from db import db
from models import (Marketplace, Calendar, Materials, Customer, Manager, Contract, 
                   Holding, Sector, DOCType, Product_Names)

from config import OZON_file, OZON_folder, Yandex_file, WB_file, Sber_file, cash_file
from wind.pages.marketplace_ui import Ui_Form
from pages_functions.product import ProductsPage

class MarketplacePage(QWidget):
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
        self.ui.line_marketPl.currentTextChanged.connect(self.on_marketplace_changed)
        self.ui.line_Year.currentTextChanged.connect(self.on_year_changed)
        self.ui.line_Mnth.currentTextChanged.connect(self.on_month_changed)
        
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_marketplace_data)
        self.ui.btn_refresh.clicked.connect(self.refresh_excel)
    
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
    
    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self._fill_combobox(self.ui.line_marketPl, ["OZON", "Wildberries", "Yandex", "СберМегаМаркет", "КЭШ"])
        self.fill_year_list()
        self.fill_month_list()
        self.fill_date_list()
        self.fill_doc_type_list()
        self.fill_product_list()
        self.fill_pack_list()
    
    def on_marketplace_changed(self):
        """Обработчик изменения маркетплейса"""
        # Обновляем все списки, которые зависят от маркетплейса
        self.fill_year_list()
        self.fill_month_list()
        self.fill_date_list()
        self.fill_doc_type_list()
        self.fill_product_list()
        self.fill_pack_list()

    def on_year_changed(self):
        """Обработчик изменения года"""
        # Обновляем списки, которые зависят от года
        self.fill_month_list()
        self.fill_date_list()
        self.fill_doc_type_list()
        self.fill_product_list()
        self.fill_pack_list()

    def on_month_changed(self):
        """Обработчик изменения месяца"""
        # Обновляем списки, которые зависят от месяца
        self.fill_date_list()
        self.fill_doc_type_list()
        self.fill_product_list()
        self.fill_pack_list()
    
    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса с проверкой на дубликаты"""
        current_text = combobox.currentText()
        combobox.clear()
        
        # Фильтрация: удаляем None, пустые строки и дубликаты
        filtered_items = [str(item) for item in items if item is not None and str(item).strip()]
        unique_items = sorted(list(set(filtered_items)))
        
        # Всегда добавляем "-" в начало списка, если его там нет
        if not unique_items or unique_items[0] != "-":
            unique_items = ["-"] + [item for item in unique_items if item != "-"]
        
        combobox.addItems(unique_items)
        
        # Восстанавливаем предыдущее значение, если оно есть в новом списке
        if current_text in unique_items:
            combobox.setCurrentText(current_text)
        else:
            combobox.setCurrentText("-")

    def fill_year_list(self):
        """Заполнение списка годов с учетом фильтра маркетплейса"""
        try:
            market_pl = self.ui.line_marketPl.currentText()
            if market_pl == "-":
                self._fill_combobox(self.ui.line_Year, ["-"])
                return
                
            query = db.query(Marketplace.Date)
            
            if market_pl == "КЭШ":
                query = query.filter(Marketplace.contract.has(Contract.Contract == "КЭШ"))
            else:
                query = query.filter(Marketplace.holding.has(Holding_name=market_pl))
            
            years = query.distinct()
            years_list = sorted(list({y[0].year for y in years if y[0] is not None}), reverse=True)
            years_list = [str(y) for y in years_list]
            
            self._fill_combobox(self.ui.line_Year, ["-"] + years_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка годов: {str(e)}")
            self._fill_combobox(self.ui.line_Year, ["-"])

    def fill_month_list(self):
        """Заполнение списка месяцев с учетом фильтров"""
        try:
            market_pl = self.ui.line_marketPl.currentText()
            year = self.ui.line_Year.currentText()
            
            if market_pl == "-" or year == "-" or not year:
                self._fill_combobox(self.ui.line_Mnth, ["-"])
                return
            
            query = db.query(Marketplace.Date).filter(
                func.extract('year', Marketplace.Date) == int(year)
            )
            
            if market_pl == "КЭШ":
                query = query.filter(Marketplace.contract.has(Contract.Contract == "КЭШ"))
            else:
                query = query.filter(Marketplace.holding.has(Holding_name=market_pl))
            
            months = query.distinct()
            months_list = sorted(list({m[0].month for m in months if m[0] is not None}))
            months_list = [str(m) for m in months_list]
            
            self._fill_combobox(self.ui.line_Mnth, ["-"] + months_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка месяцев: {str(e)}")
            self._fill_combobox(self.ui.line_Mnth, ["-"])

    def fill_date_list(self):
        """Заполнение списка дат с учетом всех фильтров"""
        try:
            market_pl = self.ui.line_marketPl.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()
            
            if market_pl == "-" or year == "-" or month == "-" or not year or not month:
                self._fill_combobox(self.ui.line_Date, ["-"])
                return
            
            query = db.query(Marketplace.Date).filter(
                func.extract('year', Marketplace.Date) == int(year),
                func.extract('month', Marketplace.Date) == int(month)
            )
            
            if market_pl == "КЭШ":
                query = query.filter(Marketplace.contract.has(Contract.Contract == "КЭШ"))
            else:
                query = query.filter(Marketplace.holding.has(Holding_name=market_pl))
            
            dates = query.distinct()
            dates_list = sorted([d[0].strftime("%d.%m.%Y") for d in dates if d[0] is not None])
            
            self._fill_combobox(self.ui.line_Date, ["-"] + dates_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка дат: {str(e)}")
            self._fill_combobox(self.ui.line_Date, ["-"])

    def fill_doc_type_list(self):
        """Заполнение списка типов документов"""
        try:
            market_pl = self.ui.line_marketPl.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()
            date = self.ui.line_Date.currentText()
            
            if market_pl == "-":
                self._fill_combobox(self.ui.line_doc_type, ["-"])
                return
                
            query = db.query(DOCType.Doc_type)
            
            if market_pl != "-":
                query = query.join(Marketplace)
                if market_pl == "КЭШ":
                    query = query.filter(Marketplace.contract.has(Contract.Contract == "КЭШ"))
                else:
                    query = query.filter(Marketplace.holding.has(Holding_name=market_pl))
                
                if year != "-":
                    try:
                        query = query.filter(func.extract('year', Marketplace.Date) == int(year))
                    except ValueError:
                        pass
                
                if month != "-":
                    try:
                        query = query.filter(func.extract('month', Marketplace.Date) == int(month))
                    except ValueError:
                        pass
                
                if date != "-":
                    try:
                        date_obj = datetime.strptime(date, "%d.%m.%Y").date()
                        query = query.filter(Marketplace.Date == date_obj)
                    except ValueError:
                        pass
            
            doc_types = query.distinct()
            doc_types_list = sorted([d[0] for d in doc_types if d[0] is not None])
            
            self._fill_combobox(self.ui.line_doc_type, ["-"] + doc_types_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка типов документов: {str(e)}")
            self._fill_combobox(self.ui.line_doc_type, ["-"])

    def fill_product_list(self):
        """Заполнение списка продуктов с учетом всех фильтров"""
        try:
            query = db.query(Product_Names.Product_name
                            ).join(Materials, Product_Names.materials
                            ).join(Marketplace, Materials.marketplace_entries)
            
            market_pl = self.ui.line_marketPl.currentText()
            if market_pl != "-":
                if market_pl == "КЭШ":
                    query = query.filter(Marketplace.contract.has(Contract.Contract == "КЭШ"))
                else:
                    query = query.filter(Marketplace.holding.has(Holding_name=market_pl))
            
            year = self.ui.line_Year.currentText()
            if year != "-" and year:
                query = query.filter(func.extract('year', Marketplace.Date) == int(year))
            
            month = self.ui.line_Mnth.currentText()
            if month != "-" and month:
                query = query.filter(func.extract('month', Marketplace.Date) == int(month))
            
            date = self.ui.line_Date.currentText()
            if date != "-" and date:
                try:
                    date_obj = datetime.strptime(date, "%d.%m.%Y").date()
                    query = query.filter(Marketplace.Date == date_obj)
                except ValueError:
                    pass
            
            doc_type = self.ui.line_doc_type.currentText()
            if doc_type != "-" and doc_type:
                query = query.filter(Marketplace.doc_type.has(Doc_type=doc_type))
            
            products = query.distinct()
            products_list = sorted([p[0] for p in products if p[0] is not None])
            
            self._fill_combobox(self.ui.line_product, ["-"] + products_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка продуктов: {str(e)}")
            self._fill_combobox(self.ui.line_product, ["-"])

    def fill_pack_list(self):
        """Заполнение списка типов упаковки с учетом всех фильтров"""
        try:
            query = db.query(Materials.Package_type
                            ).join(Marketplace, Materials.marketplace_entries)
            
            market_pl = self.ui.line_marketPl.currentText()
            if market_pl != "-":
                if market_pl == "КЭШ":
                    query = query.filter(Marketplace.contract.has(Contract.Contract == "КЭШ"))
                else:
                    query = query.filter(Marketplace.holding.has(Holding_name=market_pl))
            
            year = self.ui.line_Year.currentText()
            if year != "-" and year:
                query = query.filter(func.extract('year', Marketplace.Date) == int(year))
            
            month = self.ui.line_Mnth.currentText()
            if month != "-" and month:
                query = query.filter(func.extract('month', Marketplace.Date) == int(month))
            
            date = self.ui.line_Date.currentText()
            if date != "-" and date:
                try:
                    date_obj = datetime.strptime(date, "%d.%m.%Y").date()
                    query = query.filter(Marketplace.Date == date_obj)
                except ValueError:
                    pass
            
            doc_type = self.ui.line_doc_type.currentText()
            if doc_type != "-" and doc_type:
                query = query.filter(Marketplace.doc_type.has(Doc_type=doc_type))
            
            product = self.ui.line_product.currentText()
            if product != "-" and product:
                query = query.join(Product_Names).filter(Product_Names.Product_name == product)
            
            packs = query.distinct()
            packs_list = sorted([p[0] for p in packs if p[0] is not None])
            
            self._fill_combobox(self.ui.line_pack, ["-"] + packs_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка упаковок: {str(e)}")
            self._fill_combobox(self.ui.line_pack, ["-"])

    def safe_int_convert(value, default=None):
        """Безопасное преобразование в целое число"""
        try:
            return int(value) if value and value != "-" else default
        except ValueError:
            return default
    
    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с данными маркетплейса')
        if file_path:
            self.ui.label_plan_File.setText(file_path)
    
    def upload_data(self):
        """Основной метод загрузки данных в БД"""
        market_place = self.ui.line_marketPl.currentText()
        
        if market_place == "-":
            self.show_error_message("Пожалуйста, выберите маркетплейс для обновления")
            return
        
        try:
            # Получаем данные для выбранного маркетплейса
            if market_place == "КЭШ":
                df = self.read_cash_data()
            else:
                df = self._get_marketplace_data(market_place)

            # Подготавливаем и сохраняем данные
            prepared_df = self._prepare_marketplace_data(df)
            self._update_marketplace_data(prepared_df, market_place)
            
            self.show_message(f"Данные для {market_place} успешно обновлены")
            self.refresh_all_comboboxes()
            
        except Exception as e:
            error_msg = f'Ошибка загрузки данных: {str(e)}'
            traceback.print_exc()
            self.show_error_message(error_msg)

    def _get_marketplace_data(self, market_place):
        """Возвращает данные для указанного маркетплейса с проверкой продуктов в БД"""
        # Базовый dtype для всех маркетплейсов
        base_dtype = {
            "Количество": float,
            "Сумма 1С": float,
            "Контрагент.Код": str,
            "Договор.Код": str,
            "Постоплата%": float
        }
        
        readers = {
            "OZON": {"file": OZON_file, "sheet": "OZON для отчета", "dtype": base_dtype, "filters": None},
            "Wildberries": {"file": WB_file, "sheet": "WB для отчета", "dtype": base_dtype, "filters": None},
            "Yandex": {"file": Yandex_file, "sheet": "Продажи", "dtype": base_dtype, "filters": {"коммент": "удалить"}},
            "СберМегаМаркет": {"file": Sber_file, "sheet": "Сбер для отчета", "dtype": base_dtype, "filters": None}
        }
        
        if market_place not in readers:
            raise ValueError(f"Неизвестный маркетплейс: {market_place}")
        
        config = readers[market_place]
        
        # Читаем данные из файла
        df = self._read_marketplace_file(
            file_path=config["file"],
            sheet_name=config["sheet"],
            market_place_name=market_place,
            dtype=config["dtype"],
            special_filters=config["filters"]
        )

        # Проверяем наличие продуктов в БД
        df = self._check_products_in_db(df)

        return df

    def _read_marketplace_file(self, file_path, sheet_name, market_place_name, dtype, special_filters=None):
        """Общая функция для чтения и первичной обработки файла маркетплейса"""
        # Чтение файла
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=dtype)
        
        # Применение специальных фильтров
        if special_filters:
            for column, value in special_filters.items():
                df = df[df[column] != value]
        
        required_columns = [
            'Документ', 'Дата', 'Код',  'Артикул', 'Продукт', 'Количество', 'Сумма 1С',
            'Контрагент.Код', 'Менеджер', 'Договор.Код', 'ХОЛДИНГ',
            'SECTOR', 'Условие оплаты', 'Постоплата%', 'Плановая дата оплаты',
            'Вид документа', 'Вид операции', 'Тип документа']
        
        # Оставляем только нужные колонки
        df = df[[col for col in required_columns if col in df.columns]]
        # Стандартная обработка данных
        df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")
        df["Плановая дата оплаты"] = pd.to_datetime(df["Плановая дата оплаты"], errors="coerce")
        df["Количество"] = df["Количество"].fillna(0)
        df["Сумма 1С"] = df["Сумма 1С"].fillna(0)
        
        # Добавление стандартных значений
        df["Склад"] = market_place_name
        df["Единица измерения"] = "шт"
        df["Валюта"] = "RUB"
        df["Курс взаиморасчетов"] = 1.0
        df["% НДС"] = "20%"
        df["Код"] = df["Код"].str.strip()
        
        if df.empty:
            raise ValueError("DataFrame пустой после чтения файла. Проверьте исходные данные.")
    
        # Определение колонок для группировки
        numeric_cols = ["Количество", "Сумма 1С"]
        group_cols = [col for col in df.columns if col not in numeric_cols]
        
        df = df.groupby(group_cols, as_index=False)[numeric_cols].sum()
        
        return df
        
    def read_cash_data(self):
        """Обновление данных КЭШ в БД с полной обработкой колонок"""
        dtype_cash = {
            "Количество": float,
            "Сумма 1С": float,
            "Контрагент.Код": str,
            "Код": str,
        }
        
        try:
            # Чтение данных из Excel с исходными названиями колонок
            cash_df = pd.read_excel(cash_file, sheet_name="КЭШ", dtype=dtype_cash)
            
            # Проверка наличия всех необходимых колонок в исходных данных
            required_original_columns = ['Документ', 'Дата', 'Код', 'Количество', 'Сумма 1С', 'Контрагент.Код', 'Менеджер']
            missing_columns = [col for col in required_original_columns 
                            if col not in cash_df.columns]
            
            if missing_columns:
                self.show_error_message(f"В файле КЭШ отсутствуют обязательные колонки: {', '.join(missing_columns)}")
                return pd.DataFrame()
            
            # Выбираем только нужные колонки
            cash_df = cash_df[required_original_columns + ['Артикул', 'Продукт']]
            
            # Проверка продуктов с исходными названиями колонок
            cash_df = self._check_products_in_db(cash_df)

            if cash_df.empty:
                self.show_error_message("Нет данных для загрузки после проверки продуктов")
                return pd.DataFrame()
            
            # Переименование колонок после проверки продуктов
            cash_df = cash_df.rename(columns={
                'Документ': 'Document',
                'Дата': 'Date',
                'Код': 'Material_id',
                'Количество': 'Qty',
                'Сумма 1С': 'Amount_1C',
                'Контрагент.Код': 'Customer_id',
                'Менеджер': 'Manager_name'
            })
            
            # Обработка данных
            cash_df["Date"] = pd.to_datetime(cash_df["Date"], errors="coerce")
            cash_df["Qty"] = cash_df["Qty"].fillna(0)
            cash_df["Amount_1C"] = cash_df["Amount_1C"].fillna(0)
            cash_df["Price_1C"] = np.where(
                cash_df["Qty"] != 0, 
                round(cash_df["Amount_1C"] / cash_df["Qty"], 2), 
                0
            )
            
            # Добавляем стандартные значения для КЭШ
            cash_df["Stock"] = "-"
            cash_df["Contract"] = "КЭШ"
            cash_df["UoM"] = "шт"
            cash_df["Currency"] = "RUB"
            cash_df["FX_rate"] = 1.0
            cash_df["VAT"] = "20%"
            cash_df["Payment_terms"] = "Аванс 100% за 0 к.д."
            cash_df["Post_payment"] = 0
            cash_df["Plan_pay_Date"] = cash_df["Date"]
            cash_df["Document_type"] = "КЭШ"
            cash_df["Transaction_type"] = "КЭШ"
            cash_df["Doc_type"] = "4.0. Реализация (кэш)"
            cash_df["Material_id"] = cash_df["Material_id"].str.strip()

            customer_ids = cash_df["Customer_id"].unique().tolist()
            
            try:
                customers_data = db.query(
                    Customer.id,
                    Holding.Holding_name,
                    Sector.Sector_name
                ).join(Customer.holding
                ).join(Customer.sector
                ).filter(Customer.id.in_(customer_ids)
                ).all()

                customer_info = {
                    customer.id: (customer.Holding_name, customer.Sector_name) 
                    for customer in customers_data
                }
                
                cash_df["Holding_name"] = cash_df["Customer_id"].map(lambda x: customer_info.get(x, ("-", "-"))[0])
                cash_df["Sector_name"] = cash_df["Customer_id"].map(lambda x: customer_info.get(x, ("-", "-"))[1])
                
                cash_df["Contract_id"] = self._generate_cash_contracts(cash_df)

            except Exception as e:
                print(f"Полная трассировка ошибки: {traceback.format_exc()}")  # Добавьте эту строку
                self.show_error_message(f"Ошибка при получении данных о клиентах: {str(e)}")
                return pd.DataFrame()
            
            return cash_df

        except Exception as e:
            self.show_error_message(f"Ошибка при чтении файла КЭШ: {str(e)}")
            return pd.DataFrame()
    
    def _check_products_in_db(self, df):
        """Проверяет наличие продуктов в БД и обрабатывает отсутствующие"""
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
        missing_products = missing_df[['Артикул', 'Код', 'Продукт']].drop_duplicates()
        
        # Формируем сообщение с информацией об отсутствующих продуктах
        msg = "Следующие продукты отсутствуют в БД:\n\n"
        msg += "\n".join(f"{row['Артикул']}, {row['Код']}, {row['Продукт']}" 
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
            product_updater = ProductsPage()
            product_updater.upload_data()
            
            # Повторно проверяем наличие продуктов после обновления
            try:
                existing_codes = {str(m[0]) for m in db.query(Materials.Code).all()}
                still_missing = set(df['Код'].unique()) - existing_codes
                
                if still_missing:
                    # Формируем сообщение о продуктах, которые все еще отсутствуют
                    still_missing_df = df[df['Код'].isin(still_missing)]
                    still_missing_products = still_missing_df[['Артикул', 'Код', 'Продукт']].drop_duplicates()
                    
                    msg = "Следующие продукты все еще отсутствуют в БД и будут пропущены:\n\n"
                    msg += "\n".join(f"{row['Артикул']}, {row['Код']}, {row['Продукт']}" 
                                    for _, row in still_missing_products.iterrows())
                    self.show_message(msg)
                    
                    # Удаляем строки с отсутствующими продуктами
                    df = df[~df['Код'].isin(still_missing)]
            except Exception as e:
                self.show_error_message(f"Ошибка при повторной проверке продуктов: {str(e)}")
                return pd.DataFrame()
        else:
            # Пользователь отказался обновлять - просто удаляем отсутствующие продукты
            df = df[~df['Код'].isin(missing_codes)]
        
        return df
    
    def _generate_cash_contracts(self, df):
        """Генерация кодов договоров для КЭШ с проверкой в БД"""
        contracts = []
        
        for _, row in df.iterrows():
            manager = row["Manager_name"]
            customer_id = row["Customer_id"]
            contract_code = row.get("Contract_id", None)
            
            # Если договор указан и существует в БД - используем его
            if contract_code:
                contracts.append(contract_code)
                continue
                
            # Ищем существующий договор КЭШ для этого менеджера и клиента
            existing_contract = db.query(Contract.id).filter(
                Contract.Contract == "КЭШ",
                Contract.Manager_id == self._get_id(Manager, Manager_name=manager),
                Contract.Customer_id == customer_id
            ).first()
            
            if existing_contract:
                contracts.append(existing_contract[0])
            else:
                # Генерируем новый уникальный код договора
                max_num = db.query(func.max(Contract.id)).filter(Contract.Contract == "КЭШ").scalar()
                
                if max_num:
                    last_num = int(max_num.split("-")[-1])
                    new_num = last_num + 1
                else:
                    new_num = 1
                    
                new_code = f"ОП-КЭШ-{new_num:03d}"
                
                # Проверяем, не существует ли уже такой код
                while db.query(Contract).filter(Contract.id == new_code).first():
                    new_num += 1
                    new_code = f"ОП-КЭШ-{new_num:03d}"
                
                # Создаем новый договор в БД
                try:
                    new_contract = Contract(
                        id=new_code,
                        Contract="КЭШ",
                        Contract_Type="С покупателем",
                        Price_Type="Крупный опт",
                        Payment_Condition="Аванс 100% за 0 к.д.",
                        Customer_id=customer_id,
                        Manager_id=self._get_id(Manager, Manager_name=manager)
                    )
                    db.add(new_contract)
                    db.commit()
                    contracts.append(new_code)
                except Exception as e:
                    db.rollback()
                    print(f"Ошибка при создании договора: {str(e)}")
                    # Используем сгенерированный код, даже если не удалось сохранить в БД
                    contracts.append(new_code)
        
        return contracts

    def _prepare_marketplace_data(self, df):
        """Подготовка данных для вставки в таблицу Marketplace"""
        # Переименование колонок
        df = df.rename(columns={
            "Документ": "Document",
            "Дата": "Date",
            "Код": "Material_id",
            "Количество": "Qty",
            "Сумма 1С": "Amount_1C",
            "Контрагент.Код": "Customer_id",
            "Менеджер": "Manager_name",
            "Договор.Код": "Contract_id",
            "ХОЛДИНГ": "Holding_name",
            "SECTOR": "Sector_name",
            "Условие оплаты": "Payment_terms",
            "Постоплата%": "Post_payment",
            "Плановая дата оплаты": "Plan_pay_Date",
            "Вид документа": "Document_type",
            "Вид операции": "Transaction_type",
            "Тип документа": "Doc_type",
            "Склад": "Stock",
            "Единица измерения": "UoM",
            "Валюта": "Currency",
            "Курс взаиморасчетов": "FX_rate",
            "% НДС": "VAT"
        })
        
        df["Price_1C"] = np.where(df["Qty"] != 0, round(df["Amount_1C"] / df["Qty"], 2), 0)
        
        # Оставляем только нужные колонки
        df = df[[
            "Document", "Date", "Material_id", "Qty", "Amount_1C", "Price_1C",
            "Customer_id", "Manager_name", "Contract_id", "Holding_name",
            "Sector_name", "Payment_terms", "Post_payment", "Plan_pay_Date",
            "Document_type", "Transaction_type", "Doc_type", "Stock", "UoM",
            "Currency", "FX_rate", "VAT"
        ]]
        
        # Замена NaN на None
        df = df.where(pd.notnull(df), None)
        
        # Преобразование типов
        for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = df[col].astype('float32')
            elif df[col].dtype == 'int64':
                if df[col].isnull().any():
                    df[col] = df[col].replace({np.nan: None})
                df[col] = df[col].astype('Int32')
            elif df[col].dtype == '<M8[ns]':  # Datetime columns
                if df[col].isnull().any():
                    df[col] = df[col].replace({pd.NaT: None})
        
        return df
    
    def _update_marketplace_data(self, df, marketplace_name):
        """Обновление данных в таблице Marketplace с проверкой уникальности"""
        try:
            # Создаем индекс для быстрого поиска существующих записей
            existing_records = {
                (r.Document, r.Date, r.Material_id, r.Customer_id, r.Manager_id, r.DocType_id): r.id 
                for r in db.query(
                    Marketplace.Document, 
                    Marketplace.Date, 
                    Marketplace.Material_id,
                    Marketplace.Customer_id,
                    Marketplace.Manager_id,
                    Marketplace.DocType_id,
                    Marketplace.id
                ).filter(Marketplace.holding.has(Holding_name=marketplace_name))
            }
            
            new_records = []
            updated_records = []
            
            for _, row in df.iterrows():
                # Получаем ключ для проверки уникальности
                record_key = (
                    row['Document'],
                    row['Date'],
                    row['Material_id'],
                    row['Customer_id'],
                    self._get_id(Manager, Manager_name=row['Manager_name']),
                    self._get_doc_type_id(row['Document_type'], row['Transaction_type'], row['Doc_type'])
                )
                
                # Получаем ID связанных сущностей с помощью универсального _get_id
                calendar_id = self._get_id(Calendar, Day=row['Date'])
                material_id = row['Material_id']
                customer_id = row['Customer_id']
                manager_id = self._get_id(Manager, Manager_name=row['Manager_name'])
                contract_id = row['Contract_id']
                holding_id = self._get_id(Holding, Holding_name=row['Holding_name'])
                sector_id = self._get_id(Sector, Sector_name=row['Sector_name'])
                doc_type_id = self._get_doc_type_id(row['Document_type'], row['Transaction_type'], row['Doc_type'])
                
                if record_key in existing_records:
                    # Обновляем существующую запись
                    record_id = existing_records[record_key]
                    db.query(Marketplace).filter(Marketplace.id == record_id).update({
                        'Qty': row['Qty'],
                        'Amount_1C': row['Amount_1C'],
                        'Price_1C': row['Price_1C'],
                        'Payment_terms': row['Payment_terms'],
                        'Post_payment': row['Post_payment'],
                        'Plan_pay_Date': row['Plan_pay_Date'],
                        'Stock': row['Stock'],
                        'UoM': row['UoM'],
                        'Currency': row['Currency'],
                        'FX_rate': row['FX_rate'],
                        'VAT': row['VAT'],
                        'Calendar_id': calendar_id,
                        'Contract_id': contract_id,
                        'Sector_id': sector_id
                    })
                    updated_records.append(record_id)
                else:
                    # Создаем новую запись
                    new_records.append(Marketplace(
                        Document=row['Document'],
                        Date=row['Date'],
                        Qty=row['Qty'],
                        Amount_1C=row['Amount_1C'],
                        Price_1C=row['Price_1C'],
                        Payment_terms=row['Payment_terms'],
                        Post_payment=row['Post_payment'],
                        Plan_pay_Date=row['Plan_pay_Date'],
                        Stock=row['Stock'],
                        UoM=row['UoM'],
                        Currency=row['Currency'],
                        FX_rate=row['FX_rate'],
                        VAT=row['VAT'],
                        Calendar_id=calendar_id,
                        Material_id=material_id,
                        Customer_id=customer_id,
                        Manager_id=manager_id,
                        Contract_id=contract_id,
                        Holding_id=holding_id,
                        Sector_id=sector_id,
                        DocType_id=doc_type_id
                    ))
            
            # Массовое добавление новых записей
            if new_records:
                db.bulk_save_objects(new_records)
            
            # Удаляем записи, которых нет в новых данных
            records_to_delete = set(existing_records.values()) - set(updated_records)
            if records_to_delete:
                db.query(Marketplace).filter(Marketplace.id.in_(records_to_delete)).delete(synchronize_session=False)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления данных {marketplace_name} в базе данных: {e}")
        finally:
            db.close()

    @lru_cache(maxsize=128)
    def _get_id(self, model, **filters):
        """Универсальная функция для получения ID с кэшированием"""
        if not all(filters.values()):
            return None
        
        item = db.query(model).filter_by(**{k: v for k, v in filters.items() if v is not None}).first()
        return item.id if item else None

    def _get_doc_type_id(self, document, transaction, doc_type):
        """Получение ID типа документа (без создания новых записей)"""
        if not document:
            return None
        
        # Просто получаем ID существующего типа документа
        return self._get_id(DOCType, Document=document, Transaction=transaction, Doc_type=doc_type)
    
    def refresh_excel(self):
        """Обновление Excel файла для выбранного маркетплейса"""
        market_place = self.ui.line_marketPl.currentText()
        
        if market_place == "-":
            self.show_error_message("Пожалуйста, выберите маркетплейс для обновления")
            return
        
        try:
            if market_place == "OZON":
                self.OZON_excel_update()
            elif market_place == "Wildberries":
                self.WB_excel_update()
            elif market_place == "Яндекс":
                self.Yandex_excel_update()
            elif market_place == "СберМегаМаркет":
                self.Sber_excel_update()
            elif market_place == "КЭШ":
                self.Cash_excel_update()
            
            self.show_message(f"Excel файл для {market_place} успешно обновлен")
            
        except Exception as e:
            error_msg = f'Ошибка обновления Excel: {str(e)}'
            traceback.print_exc()
            self.show_error_message(error_msg)
    
    def write_ozon_product_errors(self, df):
        """Проверка отсутствующих продуктов и вывод сообщения пользователю"""
        error_find = df[(df["НАЗВАНИЕ"] == "-") & (df["Ozon SKU"] != "-")].drop_duplicates(subset=["Артикул", "Ozon SKU"])
        if not error_find.empty:
            error_msg = "В ОЗОН не найдены следующие продукты:\n\n"
            error_find = error_find[["Ozon SKU", "Артикул", "Название товара"]].drop_duplicates()
            
            # Сохраняем ошибки в файл
            error_find.to_excel("ERRORs_OZON_Products.xlsx", index=False, engine="openpyxl")
            
            # Формируем сообщение для пользователя
            error_msg += "\n".join(f"SKU: {row['Ozon SKU']}, Артикул: {row['Артикул']}, Название: {row['Название товара']}" 
                                for _, row in error_find.iterrows())
            error_msg += "\n\nПодробности сохранены в файл ERRORs_OZON_Products.xlsx"
            
            # Показываем сообщение пользователю
            self.show_error_message(error_msg)
            return True  # Возвращаем флаг ошибки
        return False  # Ошибок не обнаружено

    def OZON_excel_update(self):
        """Обновление Excel файла для OZON"""
        try:
            dtypes_folder = {"ID начисления": str, "Ozon SKU": str, "SKU": str, "Артикул": str, "Название товара": str, "Количество": float,
                            "Цена продавца": float, "Вознаграждение Ozon, %": str, "Индекс локализации, %": float,
                            "Сумма итого, руб": float, "Сумма итого, руб.": float }

            dtypes_codes = {"Код товара OZON": str, "Артикул": str, "TRIM code": str}

            # Чтение файла с кодами
            ozon_codes = pd.read_excel(OZON_file, sheet_name="Коды", dtype=dtypes_codes)
            ozon_codes["merge"] = ozon_codes["Код товара OZON"].astype(str) + "_" + ozon_codes["Артикул"].astype(str)
            ozon_codes = ozon_codes[["merge", "НАЗВАНИЕ"]].drop_duplicates(subset=["merge"])

            # Установка даты для фильтрации
            date_remove_comp = datetime.strptime("01.11.2024", "%d.%m.%Y")

            # Чтение и объединение данных из файлов
            frames = []
            for root, dirs, files in os.walk(OZON_folder):
                for name in files:
                    fpath = os.path.join(root, name)
                    print(name)
                    data = pd.read_excel(fpath, sheet_name="Начисления", dtype=dtypes_folder, skiprows=1)
                    
                    # Переименовываем колонки по регулярному выражению
                    data = data.rename(columns=lambda x: "Итого" if re.match(r'Сумма итого, руб\.?', str(x)) else x)
                    
                    if "SKU" in data.columns:
                        data = data.rename(columns={"SKU": "Ozon SKU"})
                    
                    data["file_name"] = name
                    frames.append(data)

            ozon_df = pd.concat(frames, ignore_index=True)

            ozon_df = ozon_df.fillna({"ID начисления": "-", "Ozon SKU": "-", "Артикул": "-",  })
            ozon_df = ozon_df.rename(columns={"ID начисления": "Номер заказа"})

            ozon_df["Номер заказа"] = ozon_df["Номер заказа"].where(~ozon_df["Номер заказа"].str.startswith("bx", na=False), None)

            date_pattern = r"(\d{4}-\d{2}-\d{2})\s*-\s*(\d{4}-\d{2}-\d{2})"
            ozon_df[["start_date", "Дата"]] = ozon_df["file_name"].str.extract(date_pattern)

            ozon_df["Дата"] = pd.to_datetime(ozon_df["Дата"], format="%Y-%m-%d")

            # Фильтрация и расчет итогов
            ozon_df.loc[(ozon_df["Дата"] >= date_remove_comp) & (ozon_df["Группа услуг"] == "Компенсации и декомпенсации"), "Итого"] = 0
            ozon_df["merge"] = ozon_df["Ozon SKU"].astype(str) + "_" + ozon_df["Артикул"].astype(str)
            
            ozon_df = ozon_df.merge(ozon_codes, on="merge", how="left").drop(columns=["merge"])
            ozon_df["НАЗВАНИЕ"] = ozon_df["НАЗВАНИЕ"].fillna("-")

            # Проверка ошибок в продуктах
            if self.write_ozon_product_errors(ozon_df):
                return

            # Преобразование условий для колонки "Кол-во"
            conditions = [
                (ozon_df["Группа услуг"] == "Возвраты") & (ozon_df["Тип начисления"] == "За продажу или возврат до вычета комиссий и услуг"),
                (ozon_df["Группа услуг"] == "Возвраты") & (ozon_df["Тип начисления"] == "Возврат выручки"),
                (ozon_df["Группа услуг"] == "Продажи") & (ozon_df["Тип начисления"] == "За продажу или возврат до вычета комиссий и услуг") & (ozon_df["Цена продавца"] > 0),
                (ozon_df["Группа услуг"] == "Продажи") & (ozon_df["Тип начисления"] == "За продажу или возврат до вычета комиссий и услуг") & (ozon_df["Цена продавца"] < 0),
                (ozon_df["Группа услуг"] == "Продажи") & (ozon_df["Тип начисления"] == "Выручка") & (ozon_df["Цена продавца"] > 0),
                (ozon_df["Группа услуг"] == "Продажи") & (ozon_df["Тип начисления"] == "Выручка") & (ozon_df["Цена продавца"] < 0)
            ]

            choices = [
                ozon_df["Количество"] * (-1),
                ozon_df["Количество"] * (-1),
                ozon_df["Количество"],
                ozon_df["Количество"] * (-1),
                ozon_df["Количество"],
                ozon_df["Количество"] * (-1)
            ]

            ozon_df["Кол-во"] = pd.Series(np.select(conditions, choices, default=0.0))

            # Разделение колонки "Номер заказа"
            ozon_df[["field_0", "field_1", "field_2"]] = ozon_df["Номер заказа"].str.split("-", expand=True, n=2)
            ozon_df["Номер заказа_сокр"] = np.where(ozon_df["field_0"] != "-", ozon_df["field_0"] + "-" + ozon_df["field_1"], ozon_df["field_0"])

            # Добавление колонок "Year" и "Month"
            ozon_df["Year"] = ozon_df["Дата"].dt.year
            ozon_df["Month"] = ozon_df["Дата"].dt.month
            ozon_df["Номер заказа"] = ozon_df["Номер заказа"].fillna("-")

            # Группировка и агрегация данных
            ozon_df = ozon_df[["Year", "Month", "Дата", "Номер заказа", "Ozon SKU", "Артикул", "НАЗВАНИЕ", "Кол-во", "Итого"]]
            ozon_df = ozon_df.groupby(["Year", "Month", "Дата", "Номер заказа", "Ozon SKU", "Артикул", "НАЗВАНИЕ"]).sum().reset_index()

            # Фильтрация данных
            ozon_wo_blanks = ozon_df[ozon_df["Ozon SKU"] != "-"]
            ozon_qty_by_order = ozon_wo_blanks.groupby(["Дата", "Номер заказа"])["Кол-во"].sum().reset_index()
            ozon_full_qty = ozon_wo_blanks.groupby(["Дата"])["Кол-во"].sum().reset_index()

            ozon_blank = ozon_df[ozon_df["Ozon SKU"] == "-"][["Дата", "Номер заказа", "Итого"]]

            # Обработка данных с пустыми "Ozon SKU"
            ozon_blank_w_order = ozon_blank[ozon_blank["Номер заказа"] != "-"]
            ozon_blank_w_order = ozon_blank_w_order.merge(ozon_qty_by_order, on=["Дата", "Номер заказа"], how="left")
            ozon_blank_w_order["Кол-во"] = ozon_blank_w_order["Кол-во"].fillna("-")

            move_to_blank = ozon_blank_w_order[ozon_blank_w_order["Кол-во"] == "-"].drop(columns=["Кол-во", "Номер заказа"])
            ozon_blank_w_order = ozon_blank_w_order[ozon_blank_w_order["Кол-во"] != "-"].drop(columns=["Кол-во"])

            ozon_blank_w_order = ozon_blank_w_order.groupby(["Дата", "Номер заказа"]).sum().reset_index()
            ozon_blank_w_order = ozon_blank_w_order.merge(ozon_qty_by_order, on=["Дата", "Номер заказа"], how="left")
            ozon_blank_w_order["amount_by_order"] = ozon_blank_w_order["Итого"] / ozon_blank_w_order["Кол-во"]
            ozon_blank_w_order = ozon_blank_w_order[["Дата", "Номер заказа", "amount_by_order"]]

            ozon_blank_wo_order = ozon_blank[ozon_blank["Номер заказа"] == "-"].drop(columns=["Номер заказа"])
            ozon_blank_wo_order = pd.concat([ozon_blank_wo_order, move_to_blank], ignore_index=True).groupby(["Дата"]).sum().reset_index()

            ozon_blank_wo_order = ozon_blank_wo_order.merge(ozon_full_qty, on=["Дата"], how="left")
            ozon_blank_wo_order["amount_by_date"] = ozon_blank_wo_order["Итого"] / ozon_blank_wo_order["Кол-во"]
            ozon_blank_wo_order = ozon_blank_wo_order[["Дата", "amount_by_date"]]

            ozon_df = ozon_wo_blanks.merge(ozon_blank_w_order, on=["Дата", "Номер заказа"], how="left")
            ozon_df = ozon_df.merge(ozon_blank_wo_order, on=["Дата"], how="left")

            # Вычисление итоговых сумм
            ozon_df["amount_by_order"] = (ozon_df["amount_by_order"] * ozon_df["Кол-во"]).fillna(0.0).astype(float)
            ozon_df["amount_by_date"] = (ozon_df["amount_by_date"] * ozon_df["Кол-во"]).fillna(0.0).astype(float)
            ozon_df["Фин. Сумма без НДС"] = ((ozon_df["Итого"] + ozon_df["amount_by_order"] + ozon_df["amount_by_date"]) / 1.2)
            ozon_df["Фин. Сумма без НДС"] = np.round(ozon_df["Фин. Сумма без НДС"], decimals = 2)  

            ozon_df = ozon_df.sort_values(by=["Дата", "НАЗВАНИЕ", "Ozon SKU"], ascending=[True, True, True])
            ozon_df = ozon_df[["Year", "Month", "Дата", "Номер заказа", "Ozon SKU", "Артикул", "НАЗВАНИЕ", "Итого", "Кол-во", "Фин. Сумма без НДС"]]
            
            ozon_wo_order = ozon_df.drop(columns=["Номер заказа"])
            ozon_wo_order = ozon_wo_order.sort_values(by=["Дата", "НАЗВАНИЕ"], ascending=[True, True])
            ozon_wo_order = ozon_wo_order[["Year", "Month", "Дата", "Ozon SKU", "Артикул", "НАЗВАНИЕ", "Итого", "Кол-во", "Фин. Сумма без НДС"]]
            ozon_wo_order = ozon_wo_order.groupby(["Year", "Month", "Дата", "Ozon SKU", "Артикул", "НАЗВАНИЕ"]).sum().reset_index()

            ozon_w_order = ozon_df.copy()
            ozon_w_order["Фин. Сумма без НДС"] = np.round(ozon_w_order['Фин. Сумма без НДС'], decimals=2)
            ozon_wo_order = ozon_wo_order.copy()
            ozon_wo_order["Фин. Сумма без НДС"] = np.round(ozon_wo_order['Фин. Сумма без НДС'], decimals=2)
            
            dtypes_ozonfile = {"Year": int, "Month": int, "Ozon SKU": str, "Артикул": str}
            ozon_w_order_old = pd.read_excel(OZON_file, sheet_name="Отчет_сокр (с заказом)", dtype=dtypes_ozonfile)
            ozon_wo_order_old = pd.read_excel(OZON_file, sheet_name="Отчет_сокр", dtype=dtypes_ozonfile)
            
            unique_dates = ozon_w_order["Дата"].unique()
            ozon_w_order_old = ozon_w_order_old[~ozon_w_order_old["Дата"].isin(unique_dates)]
            ozon_w_order = pd.concat([ozon_w_order_old, ozon_w_order], ignore_index=True)
            ozon_w_order = ozon_w_order.sort_values(by=["Дата", "НАЗВАНИЕ"], ascending=[True, True])
            ozon_w_order = ozon_w_order[["Year", "Month", "Дата", "Номер заказа", "Ozon SKU", "Артикул", "НАЗВАНИЕ", "Итого", "Кол-во", "Фин. Сумма без НДС"]]

            ozon_wo_order_old = ozon_wo_order_old[~ozon_wo_order_old["Дата"].isin(unique_dates)]
            ozon_wo_order = pd.concat([ozon_wo_order_old, ozon_wo_order], ignore_index=True)
            ozon_wo_order = ozon_wo_order.sort_values(by=["Дата", "НАЗВАНИЕ"], ascending=[True, True])
            ozon_wo_order = ozon_wo_order[["Year", "Month", "Дата", "Ozon SKU", "Артикул", "НАЗВАНИЕ", "Итого", "Кол-во", "Фин. Сумма без НДС"]]
            
            ozon_ord_rep = "Отчет_сокр (с заказом)"
            ozon_wo_ord_rep = "Отчет_сокр"

            with xw.App(add_book=False, visible=False) as app:
                wb = app.books.open(OZON_file, update_links=False, read_only=False)
                
                ws = wb.sheets[ozon_ord_rep]
                ord_num_col = ws.range("A2").end("right").column
                ord_num_row = ws.range("A" + str(wb.sheets[ws].cells.last_cell.row)).end("up").row
                ws.range("A2:J" + str(ord_num_row)).delete()

                ord_cells_num = ozon_w_order.shape[0] + 1
                ws.range("A2:B" + str(ord_cells_num)).number_format = "0"
                ws.range("C3:C" + str(ord_cells_num)).number_format = "ДД.ММ.ГГГГ"
                ws.range("D2:G" + str(ord_cells_num)).number_format = "@"
                ws.range("H3:J" + str(ord_cells_num)).number_format = "# ##0,00_ ;[Red]-# ##0,00_ ;""-"""

                ws.range((2, 1), (ord_cells_num, ord_num_col)).options(index=False, header=False).value = ozon_w_order
                
                ws2 = wb.sheets[ozon_wo_ord_rep]
                ws2.api.AutoFilter.ShowAllData()
                wo_ord_num_col = ws2.range("A2").end("right").column
                wo_ord_num_row = ws2.range("A" + str(wb.sheets[ws2].cells.last_cell.row)).end("up").row
                ws2.range("A2:I" + str(wo_ord_num_row)).delete()
                
                wo_ord_cells_num = ozon_wo_order.shape[0] + 1
                ws2.range("A2:B" + str(wo_ord_cells_num)).number_format = "0"
                ws2.range("C2:C" + str(wo_ord_cells_num)).number_format = "ДД.ММ.ГГГГ"
                ws2.range("D2:F" + str(wo_ord_cells_num)).number_format = "@"
                ws2.range("G2:I" + str(wo_ord_cells_num)).number_format = "# ##0,00_ ;[Red]-# ##0,00_ ;""-"""
                ws2.range("K2:K" + str(wo_ord_cells_num)).number_format = "# ##0,00_ ;[Red]-# ##0,00_ ;""-"""
                ws2.range("M2:M" + str(wo_ord_cells_num)).number_format = "# ##0,00_ ;[Red]-# ##0,00_ ;""-"""

                ws2.range((2, 1), (wo_ord_cells_num, wo_ord_num_col)).options(index=False, header=False).value = ozon_wo_order
                
                macro_name = wb.app.macro("Ckeck_Vol_macro")
                macro_name()
                
                wb.save()
                wb.close()

        except Exception as e:
            self.show_error_message(f"Ошибка при обновлении файла OZON: {str(e)}")
            traceback.print_exc()

    def WB_excel_update(self):
        """Обновление Excel файла для Wildberries (заглушка)"""
        pass

    def Yandex_excel_update(self):
        """Обновление Excel файла для Яндекс (заглушка)"""
        pass

    def Sber_excel_update(self):
        """Обновление Excel файла для СберМегаМаркет (заглушка)"""
        pass

    def find_marketplace_data(self):
        """Поиск данных маркетплейсов по заданным критериям"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        try:
            # Импортируем extract из sqlalchemy
            from sqlalchemy import extract
            
            # Создаем базовый запрос
            query = db.query(
                DOCType.Doc_type.label("Тип документа"),
                Marketplace.Document.label("Документ"),
                Marketplace.Date.label("Дата"),
                Materials.Article.label("Артикул"),
                Product_Names.Product_name.label("Продукт"),
                Marketplace.Qty.label("Кол-во, шт"),
                (Marketplace.Qty * Materials.Package_Volume).label("Кол-во, л"),
                Marketplace.Price_1C.label("Цена без НДС, руб/л"),
                Marketplace.Amount_1C.label("Сумма без НДС, руб"),
                Customer.Customer_name.label("Контрагент"),
                Manager.Manager_name.label("Менеджер"),
                Marketplace.Payment_terms.label("Условие оплаты"),
                Marketplace.Post_payment.label("Постоплата%"),
                Marketplace.Plan_pay_Date.label("Плановая дата оплаты")
            ).join(Marketplace.material
            ).join(Materials.product_name
            ).join(Marketplace.customer
            ).join(Marketplace.manager
            ).join(Marketplace.doc_type
            )
            
            # Применяем фильтры
            market_place = self.ui.line_marketPl.currentText()
            if market_place != "-":
                if market_place == "КЭШ":
                    query = query.filter(DOCType.Doc_type == "4.0. Реализация (кэш)")
                else:
                    query = query.filter(Marketplace.holding.has(Holding_name=market_place))
            
            year = self.ui.line_Year.currentText()
            if year != "-":
                query = query.filter(extract('year', Marketplace.Date) == int(year))
            
            month = self.ui.line_Mnth.currentText()
            if month != "-":
                query = query.filter(extract('month', Marketplace.Date) == int(month))
            
            date = self.ui.line_Date.currentText()
            if date != "-":
                date_obj = datetime.strptime(date, "%d.%m.%Y").date()
                query = query.filter(Marketplace.Date == date_obj)
            
            doc_type = self.ui.line_doc_type.currentText()
            if doc_type != "-":
                query = query.filter(DOCType.Doc_type == doc_type)
            
            article = self.ui.line_article.text()
            if article:
                query = query.filter(Materials.Article.like(f"%{article}%"))
            
            product = self.ui.line_product.currentText()
            if product != "-":
                query = query.filter(Product_Names.Product_name == product)
            
            pack = self.ui.line_pack.currentText()
            if pack != "-":
                query = query.filter(Materials.Package_type == pack)
            
            # Выполняем запрос
            result = query.all()
            
            if not result:
                self.show_message("Данные не найдены")
                return
            
            data = []
            for row in result:
                data.append({
                    "Тип документа": row[0],
                    "Документ": row[1],
                    "Дата": row[2].strftime("%d.%m.%Y") if row[2] else "",
                    "Артикул": row[3],
                    "Продукт": row[4],
                    "Кол-во, шт": int(row[5]) if row[5] else 0,
                    "Кол-во, л": float(row[6]) if row[6] else 0.0,
                    "Цена без НДС, руб/л": float(row[7]) if row[7] else 0.0,
                    "Сумма без НДС, руб": float(row[8]) if row[8] else 0.0,
                    "Контрагент": row[9],
                    "Менеджер": row[10],
                    "Условие оплаты": row[11],
                    "Постоплата%": float(row[12]) if row[12] else 0.0,
                    "Плановая дата оплаты": row[13].strftime("%d.%m.%Y") if row[13] else ""
                })
            
            df = pd.DataFrame(data)

            # Отображаем данные в таблице
            self._display_data(df)
            
            # Обновляем сводную информацию
            self._update_summary(df)
            
        except Exception as e:
            self.show_error_message(f"Ошибка при поиске данных: {str(e)}")
            traceback.print_exc()
    
    def _display_data(self, df):
        """Отображение данных в таблице"""
        self.table.clearContents()
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        # Форматирование числовых колонок
        numeric_cols = ["Кол-во, шт", "Кол-во, л", "Цена без НДС, руб/л", "Сумма без НДС, руб", "Постоплата%"]
        
        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                # Выравнивание чисел по правому краю
                if df.columns[col_idx] in numeric_cols:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                # Форматирование числовых значений
                if df.columns[col_idx] == "Кол-во, шт":
                    item.setText(f"{int(value):,}".replace(",", " "))
                elif df.columns[col_idx] in ["Кол-во, л", "Цена без НДС, руб/л", "Сумма без НДС, руб"]:
                    item.setText(f"{float(value):,.2f}".replace(",", " ").replace(".", ","))
                elif df.columns[col_idx] == "Постоплата%":
                    item.setText(f"{float(value):.0f}%")
                
                self.table.setItem(row_idx, col_idx, item)
        
        # Автоматическое растягивание колонок
        self.table.resizeColumnsToContents()
    
    def _update_summary(self, df):
        """Обновление сводной информации"""
        if df.empty:
            volume = revenue = 0
        else:
            volume = df["Кол-во, л"].sum()
            revenue = df["Сумма без НДС, руб"].sum()
        
        # Форматирование чисел
        def format_number(value):
            return f"{float(value):,.2f}".replace(",", " ").replace(".", ",")
        
        self.ui.label_Volume.setText(f"{format_number(volume)} л." if volume != 0 else "0,00 л.")
        self.ui.label_Revenue.setText(f"{format_number(revenue)} р" if revenue != 0 else "0,00 р.")
    
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



