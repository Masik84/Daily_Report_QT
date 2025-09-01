import os
import pandas as pd
import numpy as np
from sqlalchemy import or_
from PySide6.QtWidgets import (QMessageBox, QHeaderView, QTableWidget, QMenu, QTableWidgetItem, QWidget, QApplication)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from datetime import datetime, date, timedelta

from wind.pages.delivery_ui import Ui_Form
from config import CustDelivery_File, Total_DISPATCHED
from models import Delivery_to_Customer, temp_Sales, Materials
from db import db

class DeliveryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self._updating_table = False
        self._original_values = {}
        self._pending_changes = {}
        
        today = datetime.now()
        if today.day > 5:
            target_date = QDate(today.year, today.month, 1)
        else:
            # Получаем первый день прошлого месяца
            first_day_prev_month = today.replace(day=1) - timedelta(days=1)
            target_date = QDate(first_day_prev_month.year, first_day_prev_month.month, 1)

        self.ui.line_date.setDate(target_date)

        self._setup_ui()
        self._setup_connections()
        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса таблицы"""
        self.table = self.ui.table
        
        # Базовые настройки таблицы
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)
        
        # Устанавливаем высоту строки 20px
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.verticalHeader().setMinimumSectionSize(20)
        
        # Контекстное меню
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                selection-background-color: #3daee9;
                selection-color: black;
                font: 9pt "Tahoma";  /* Добавляем шрифт для всей таблицы */
            }
            QTableWidget::item {
                padding: 1px;  /* Уменьшаем отступы */
                font: 9pt "Tahoma";  /* Шрифт для ячеек */
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
        
        self._updating_table = False
        
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
        self.ui.btn_refresh.clicked.connect(self.refresh_from_delivery)
        self.ui.btn_disputch.clicked.connect(self.refresh_from_disputch)
        self.ui.btn_find.clicked.connect(self.find_delivery)

    def on_item_changed(self, item):
        """Обработчик изменения данных в таблице"""
        if self._updating_table:
            return
        
        try:
            row = item.row()
            column = item.column()
            header = self.table.horizontalHeaderItem(column).text()
            
            # Получаем уникальный идентификатор строки (Bill + Sborka + Delivery_date)
            bill_item = self.table.item(row, self._get_column_index('Bill'))
            sborka_item = self.table.item(row, self._get_column_index('Sborka'))
            date_item = self.table.item(row, self._get_column_index('Delivery_date'))
            
            if not all([bill_item, sborka_item, date_item]):
                return
                
            unique_id = f"{bill_item.text()}_{sborka_item.text()}_{date_item.text()}"
            new_value = item.text()
            
            # Сохраняем изменение
            if unique_id not in self._pending_changes:
                self._pending_changes[unique_id] = {}
            
            self._pending_changes[unique_id][header] = new_value
            
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")

    def _get_column_index(self, column_name):
        """Получение индекса колонки по имени"""
        for col in range(self.table.columnCount()):
            if self.table.horizontalHeaderItem(col).text() == column_name:
                return col
        return -1

    def apply_pending_changes(self):
        """Применение всех ожидающих изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для применения")
            return
            
        try:
            for unique_id, changes in self._pending_changes.items():
                bill, sborka, delivery_date_str = unique_id.split('_', 2)
                delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
                
                # Находим запись в БД
                delivery = db.query(Delivery_to_Customer).filter(
                    Delivery_to_Customer.Bill == bill,
                    Delivery_to_Customer.Sborka == sborka,
                    Delivery_to_Customer.Delivery_date == delivery_date
                ).first()
                
                if not delivery:
                    continue
                
                # Применяем изменения
                for header, new_value in changes.items():
                    if header == 'Delivery_amount_w_VAT':
                        delivery.Delivery_amount_w_VAT = float(new_value) if new_value else 0.0
                        # Пересчитываем ставку без НДС
                        delivery.Delivery_amount_wo_VAT = round(float(new_value) / 1.2, 2) if new_value else 0.0
                    
                    elif header == 'Sborka' or header == 'Bill':
                        # Обновляем связанные данные при изменении Sborka или Bill
                        setattr(delivery, header, new_value)
                        self._update_invoice_data(delivery)
                    
                    else:
                        # Для остальных полей просто устанавливаем значение
                        setattr(delivery, header, new_value)
            
            db.commit()
            self._pending_changes.clear()
            self.show_message("Изменения успешно применены")
            self.find_delivery()  # Обновляем таблицу
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка применения изменений: {str(e)}")

    def _update_invoice_data(self, delivery):
        """Обновление данных инвойса при изменении Sborka или Bill"""
        try:
            # Ищем данные в temp_Sales
            sales_data = db.query(temp_Sales).filter(
                temp_Sales.Bill == delivery.Bill,
                temp_Sales.Sborka == delivery.Sborka
            ).first()
            
            if sales_data:
                delivery.Invoice = sales_data.Document
                delivery.Invoice_date = sales_data.Date
                # Расчет объема
                delivery.inv_Volume = self._calculate_volume(sales_data)
            else:
                delivery.Invoice = "-"
                delivery.Invoice_date = None
                delivery.inv_Volume = 0
            
            # Обновляем проверки
            self._update_checks(delivery)
            
        except Exception as e:
            self.show_error_message(f"Ошибка обновления данных инвойса: {str(e)}")

    def _update_checks(self, delivery):
        """Обновление проверочных полей"""
        try:
            # Проверка ставки
            if delivery.new_Amount == delivery.Delivery_amount_wo_VAT:
                delivery.check_Deliv_amount = "Да"
            else:
                delivery.check_Deliv_amount = "Нет"
            
            # Проверка объема
            if delivery.inv_Volume == 0:
                delivery.check_Inv_volume = "-"
            elif delivery.inv_Volume == delivery.Order_volume:
                delivery.check_Inv_volume = "Да"
            else:
                delivery.check_Inv_volume = "Нет"
                
        except Exception as e:
            self.show_error_message(f"Ошибка обновления проверок: {str(e)}")

    def revert_changes(self):
        """Отмена изменений"""
        db.rollback()
        self.find_delivery()
        self._pending_changes.clear()
        self.show_message("Изменения отменены")

    def copy_cell_content(self):
        """Копирование содержимого ячеек"""
        selection = self.table_view.selectionModel()
        if selection.hasSelection():
            selected_indexes = selection.selectedIndexes()
            if selected_indexes:
                clipboard = QApplication.clipboard()
                rows = {}
                for index in selected_indexes:
                    row = index.row()
                    col = index.column()
                    if row not in rows:
                        rows[row] = {}
                    rows[row][col] = index.data(Qt.DisplayRole) or ""
                
                sorted_rows = sorted(rows.items())
                text = ""
                for row, cols in sorted_rows:
                    sorted_cols = sorted(cols.items())
                    text += "\t".join([text for col, text in sorted_cols]) + "\n"
                
                clipboard.setText(text.strip())

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        try:
            # Заполнение списка контрагентов
            customers = sorted([r[0] for r in db.query(Delivery_to_Customer.Customer_name).distinct().all() if r[0]])
            self._fill_combobox(self.ui.line_customer, customers)
            
            # Заполнение годов
            years = sorted([r[0] for r in db.query(Delivery_to_Customer.Year_delivery).distinct().all() if r[0]])
            self._fill_combobox(self.ui.line_Year, years)
            
            # Заполнение месяцев
            months = list(range(1, 13))
            self._fill_combobox(self.ui.line_Mnth, months)
            
            # Заполнение статусов проверок
            changes = ["-", "Да", "Нет"]
            self.ui.line_changes.clear()
            self.ui.line_changes.addItems(changes)
            
            # Установка даты по умолчанию
            self.ui.line_date.setDate(date(2022, 1, 1))
            
        except Exception as e:
            self.show_error_message(f"Ошибка обновления списков: {str(e)}")

    def _fill_combobox(self, combobox, items):
        """Заполнение комбобокса"""
        combobox.clear()
        combobox.addItem("-")
        if items:
            combobox.addItems([str(item) for item in items])

    def refresh_from_delivery(self):
        """Обновление данных из файла доставки (btn_refresh)"""
        try:
            file_path = CustDelivery_File
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {file_path} не найден")
            
            # Чтение Excel файла
            dtype_spec = {
                'ИНН клиента': str,
                'Задание на сборку.Номер': str
            }
            
            df = pd.read_excel(file_path, sheet_name="Доставка клиентам", dtype=dtype_spec)
            
            # Преобразование данных
            df = df.replace('#N/A', None)
            
            # Заполнение пустых значений
            df['Объем заказа, л'] = df['Объем заказа, л'].fillna(0.0)
            df['Ставка, руб (с НДС 20%)'] = df['Ставка, руб (с НДС 20%)'].fillna(0.0)
            
            # Расчеты
            df['Ставка без НДС'] = np.round(df['Ставка, руб (с НДС 20%)'] / 1.2, 2)
            df['CD_per_lt'] = np.where(
                df['Объем заказа, л'] != 0,
                df['Ставка без НДС'] / df['Объем заказа, л'],
                0.0
            )
            
            # Преобразование дат
            df['Дата отгр'] = pd.to_datetime(df["Дата отгр"], errors="coerce")
            df['Дата сф'] = pd.to_datetime(df["Дата сф"], errors="coerce")
            
            # Обработка каждой строки из Excel
            for _, row in df.iterrows():
                bill = row.get('Счет', '-')
                sborka = row.get('Задание на сборку.Номер', '-')
                delivery_date = row['Дата отгр']
                order_volume = float(row.get('Объем заказа, л', 0)) if pd.notna(row.get('Объем заказа, л')) else 0.0
                
                # Логика для Customer_name как в refresh_from_disputch
                kontragent = row.get('Наименование Клиента', '')
                if kontragent == "ИНТЕРНЕТ РЕШЕНИЯ ООО":
                    customer_name = "OZON"
                elif kontragent == "АВТОКОНТРАКТЫ ООО":
                    customer_name = "ПАРТКОМ"
                elif kontragent == "РВБ ООО":
                    customer_name = "Wildberries"
                else:
                    customer_name = kontragent  # Если ни одно условие не выполнено
                
                # Ищем существующую запись по УНИКАЛЬНОМУ КЛЮЧУ
                existing = db.query(Delivery_to_Customer).filter(
                    Delivery_to_Customer.Bill == bill,
                    Delivery_to_Customer.Sborka == sborka,
                    Delivery_to_Customer.Delivery_date == delivery_date.date(),
                    Delivery_to_Customer.Order_volume == order_volume
                ).first()
                
                # Правильная логика для check_Deliv_amount
                new_amount = row.get('Check Ставка')
                stavka_w_vat = row.get('Ставка, руб (с НДС 20%)')
                stavka_wo_vat = row.get('Ставка без НДС')
                
                if pd.isna(new_amount) or new_amount is None:
                    check_deliv_amount = "-"
                elif float(new_amount) == float(stavka_w_vat) if pd.notna(stavka_w_vat) else False:
                    check_deliv_amount = "Да"
                else:
                    check_deliv_amount = "Нет"
                
                data = {
                    'Customer_name': customer_name, 
                    'Delivery_date': delivery_date.date(),
                    'Bill': bill,
                    'Customer_in_logist': row.get('Наименование Клиента', '-'),
                    'INN': row.get('ИНН клиента', '-'),
                    'Carrier': row.get('Перевозчик', '-'),
                    'Sborka': sborka,
                    'Delivery_method': row.get('Способ доставки', '-'),
                    'Delivery_amount_w_VAT': float(row.get('Ставка, руб (с НДС 20%)', 0)) if pd.notna(row.get('Ставка, руб (с НДС 20%)')) else 0.0,
                    'Delivery_amount_wo_VAT': float(row.get('Ставка без НДС', 0)) if pd.notna(row.get('Ставка без НДС')) else 0.0,
                    'Order_volume': order_volume,
                    'Comment': row.get('Комментарий', ''),
                    'OZON': row.get('ОЗОН', ''),
                    'TS': row.get('ТС', '-'),
                    'CD_per_lt': float(row.get('CD_per_lt', 0)) if pd.notna(row.get('CD_per_lt')) else 0.0,
                    'new_Amount': float(new_amount) if pd.notna(new_amount) else None,
                    'check_Deliv_amount': check_deliv_amount,
                    # Временные значения, будут перезаписаны из temp_Sales
                    'inv_Volume': float(row.get('Объем СФ', 0)) if pd.notna(row.get('Объем СФ')) else 0.0,
                    'check_Inv_volume': 'Да' if row.get('true/false (объем)') == 'TRUE' else 'Нет',
                    'Invoice': row.get('СФ', '-'),
                    'Invoice_date': pd.to_datetime(row.get('Дата сф'), errors="coerce").date() if pd.notna(row.get('Дата сф')) else None,
                    'Year_delivery': int(row.get('Год отгр')) if pd.notna(row.get('Год отгр')) else None,
                    'Bill_and_Date': row.get('Счет & Дата', '')
                }
                
                if existing:
                    # Обновляем существующую запись, но НЕ трогаем временные поля
                    for key, value in data.items():
                        if key not in ['Invoice', 'Invoice_date', 'inv_Volume', 'check_Inv_volume']:
                            setattr(existing, key, value)
                else:
                    # Создаем новую запись
                    delivery = Delivery_to_Customer(**data)
                    db.add(delivery)
            
            db.commit()
            
            # ЕДИНЫЙ МЕТОД: ПЕРЕЗАПИСЫВАЕМ данные из temp_Sales
            self._update_from_temp_sales()
            
            self.show_message("Данные доставки успешно обновлены")
            self.refresh_all_comboboxes()
            self.find_delivery()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка обновления из доставки: {str(e)}")

    def _calculate_bill_and_date(self, customer_name, ozon, bill, delivery_date):
        """Расчет значения для колонки Bill_and_Date по логике Excel формулы"""
        try:
            if not delivery_date:
                return f"{bill}_"
                
            month = delivery_date.month
            year = delivery_date.year
            
            customer_name_str = str(customer_name or "").upper()
            ozon_str = str(ozon or "").upper()
            bill_str = str(bill or "")
            
            # 1. Проверка на "ЯНДЕКС"
            if "ЯНДЕКС" in customer_name_str:
                return f"fbsЯндекс_{month}_{year}"
            
            # 2. Проверка на "ВАЙЛДБЕРРИЗ ООО" и "РВБ ООО"
            if "ВАЙЛДБЕРРИЗ ООО" in customer_name_str or "РВБ ООО" in customer_name_str:
                return f"WB_{month}_{year}"
            
            # 3. Проверка на "МАРКЕТПЛЕЙС ООО"
            if "МАРКЕТПЛЕЙС ООО" in customer_name_str:
                return f"SberMP_{month}_{year}"
            
            # 4. Проверка на "ИНТЕРНЕТ РЕШЕНИЯ"
            if "ИНТЕРНЕТ РЕШЕНИЯ" in customer_name_str:
                # Проверка даты > 30.09.2024
                if delivery_date > date(2024, 9, 30):
                    if "RFBS" in ozon_str:
                        return f"realFBS_{month}_{year}"
                    elif "FBS" in ozon_str:
                        return f"fbsОЗОН_{month}_{year}"
                    elif "1P" in ozon_str or "1Р" in ozon_str:
                        return f"отгрузка1P_{month}_{year}"
                    elif "РУЧНАЯ КОРР" in ozon_str:
                        return f"ОЗОНдоп_{month}_{year}"
                    elif any(x in ozon_str for x in ["3P", "ФФСС", "ФФУ"]):
                        return f"ффсс_{month}_{year}"
                    else:
                        return "error"
                else:
                    return f"{bill_str}_{month}_{year}"
            
            # 5. Проверка на "АВТОКОНТРАКТЫ ООО" с "УАК"
            if customer_name_str == "АВТОКОНТРАКТЫ ООО" and "УАК" in ozon_str:
                return f"VMIПартком_{month}_{year}"
            
            # 6. Проверка на "VMI" в ОЗОН
            if "VMI" in ozon_str:
                return f"VMIПартком_{month}_{year}"
            
            # По умолчанию: счет_месяц_год
            return f"{bill_str}_{month}_{year}"
            
        except Exception as e:
            print(f"Ошибка расчета Bill_and_Date: {e}")
            return f"{bill}_error"

    def refresh_from_disputch(self):
        """Обновление данных из файла Disputch (btn_disputch)"""
        try:
            file_path = Total_DISPATCHED
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {file_path} не найден")

            # Чтение Excel файла
            dtype_spec = {
                'ИНН': str,
                'Задание на сборку.Номер': str,
                'Задание на доставку номер': str,
                'Заказ покупателя.Номер': str
            }
            usecols = [
                'Плановая дата отгрузки в заявке на доставку',
                'Заказ покупателя.Номер',
                'Контрагент',
                'ИНН',
                'Задание на доставку номер',
                'Перевозчик',
                'Задание на сборку.Номер',
                'Заказ покупателя.Способ доставки',
                'Количество конечный остаток литры',
                'Ставка, руб (с НДС 20%)',
                'комментарии',
                'Заказ покупателя.Инструкции по доставке'
            ]
            df = pd.read_excel(file_path, sheet_name="Фактические отгрузки", usecols=usecols, dtype=dtype_spec)

            # Преобразуем дату в правильный формат
            df['Плановая дата отгрузки в заявке на доставку'] = pd.to_datetime(
                df['Плановая дата отгрузки в заявке на доставку'],
                errors='coerce'
            )

            # Замена пустых значений
            df['Заказ покупателя.Номер'] = df['Заказ покупателя.Номер'].fillna('-')
            df['Задание на сборку.Номер'] = df['Задание на сборку.Номер'].fillna('-')
            df['Ставка, руб (с НДС 20%)'] = pd.to_numeric(
                df['Ставка, руб (с НДС 20%)'].replace(['n/a', ''], 0.0),
                errors='coerce'
            ).fillna(0.0)
            df['Количество конечный остаток литры'] = pd.to_numeric(
                df['Количество конечный остаток литры'].fillna(0.0),
                errors='coerce'
            ).fillna(0.0)

            # Переименовываем колонку для удобства
            df = df.rename(columns={'Контрагент': 'Наименование Клиента'})
            
            # Создание колонки ОЗОН
            df['ОЗОН'] = df.apply(lambda x: x['Заказ покупателя.Инструкции по доставке']
                                if 'ИНТЕРНЕТ РЕШЕНИЯ' in str(x['Наименование Клиента']) or 'АВТОКОНТРАКТЫ' in str(x['Наименование Клиента'])
                                else '', axis=1)
            
            df[['Наименование Клиента', 'Перевозчик']] = df[['Наименование Клиента', 'Перевозчик']].fillna('-')
            df[['комментарии', 'Заказ покупателя.Способ доставки']] = df[['комментарии', 'Заказ покупателя.Способ доставки']].astype(str).fillna('')

            df['Задание на доставку номер'] = df['Задание на доставку номер'].apply(lambda x: str(x).lstrip('0') if pd.notna(x) and str(x).strip() != '' else '')

            # Группировка по всем необходимым полям для уникальности
            grouped = df.groupby([
                'Плановая дата отгрузки в заявке на доставку',
                'Заказ покупателя.Номер',
                'Задание на сборку.Номер',
                'Наименование Клиента',
                'ИНН',
                'Перевозчик',
                'Заказ покупателя.Способ доставки',
                'комментарии',
                'ОЗОН',
                'Задание на доставку номер'
            ]).agg({
                'Ставка, руб (с НДС 20%)': 'sum',
                'Количество конечный остаток литры': 'sum'
            }).reset_index()
            
            # Обработка данных
            grouped['Ставка без НДС'] = np.round(grouped['Ставка, руб (с НДС 20%)'] / 1.2, 2)

            # Создаем колонку ТС
            grouped['ТС'] = '-'
            mask = (grouped['Задание на доставку номер'].notna()) & (grouped['Задание на доставку номер'] != '')
            grouped.loc[mask, 'ТС'] = grouped['Плановая дата отгрузки в заявке на доставку'].dt.year.astype(str) + '_' + grouped['Задание на доставку номер']

            # Шаг 1: Добавляем новые строки и обновляем существующие
            for _, row in grouped.iterrows():
                kontragent = row['Наименование Клиента']
                if kontragent == "ИНТЕРНЕТ РЕШЕНИЯ ООО":
                    customer_name = "OZON"
                elif kontragent == "АВТОКОНТРАКТЫ ООО":
                    customer_name = "ПАРТКОМ"
                elif kontragent == "РВБ ООО":
                    customer_name = "Wildberries"
                else:
                    customer_name = kontragent

                delivery_date = row['Плановая дата отгрузки в заявке на доставку']
                if pd.notna(delivery_date):
                    delivery_date = delivery_date.date()
                else:
                    delivery_date = None

                bill = str(row['Заказ покупателя.Номер']).strip()
                sborka = str(row['Задание на сборку.Номер']).strip()
                order_volume = float(row['Количество конечный остаток литры'])
                ozon_value = row['ОЗОН']

                # Получаем год для поля Year_delivery
                year_value = delivery_date.year if delivery_date else None

                # Рассчитываем Bill_and_Date по сложной логике
                bill_and_date = self._calculate_bill_and_date(
                    kontragent, ozon_value, bill, delivery_date
                )

                # Ищем существующую запись по УНИКАЛЬНОМУ КЛЮЧУ
                existing = db.query(Delivery_to_Customer).filter(
                    Delivery_to_Customer.Bill == bill,
                    Delivery_to_Customer.Sborka == sborka,
                    Delivery_to_Customer.Delivery_date == delivery_date,
                    Delivery_to_Customer.Order_volume == order_volume
                ).first()

                data = {
                    'Customer_name': customer_name,
                    'Delivery_date': delivery_date,
                    'Bill': bill,
                    'Customer_in_logist': row['Наименование Клиента'],
                    'INN': row['ИНН'],
                    'Carrier': row['Перевозчик'],
                    'Sborka': sborka,
                    'Delivery_method': row['Заказ покупателя.Способ доставки'],
                    'Delivery_amount_w_VAT': float(row['Ставка, руб (с НДС 20%)']),
                    'Delivery_amount_wo_VAT': float(row['Ставка без НДС']),
                    'Order_volume': order_volume,
                    'Comment': row['комментарии'],
                    'OZON': ozon_value,
                    'TS': row['ТС'],
                    'CD_per_lt': 0.0,
                    'new_Amount': float(row['Ставка без НДС']),
                    'Year_delivery': year_value,
                    'Bill_and_Date': bill_and_date  # Используем рассчитанное значение
                }

                if existing:
                    # ОБНОВЛЯЕМ существующую запись - ВСЕ поля кроме временных
                    for key, value in data.items():
                        if key not in ['Invoice', 'Invoice_date', 'inv_Volume', 'check_Inv_volume']:
                            setattr(existing, key, value)
                    
                    # Обновляем check_Deliv_amount
                    if existing.new_Amount is None:
                        existing.check_Deliv_amount = "-"
                    elif existing.new_Amount == existing.Delivery_amount_wo_VAT:
                        existing.check_Deliv_amount = "Да"
                    else:
                        existing.check_Deliv_amount = "Нет"
                else:
                    # СОЗДАЕМ новую запись со всеми полями
                    data.update({
                        'check_Deliv_amount': "Да" if data['new_Amount'] == data['Delivery_amount_wo_VAT'] else "Нет",
                        'inv_Volume': 0.0,
                        'check_Inv_volume': '-',
                        'Invoice': '-',
                        'Invoice_date': None
                    })
                    delivery = Delivery_to_Customer(**data)
                    db.add(delivery)

            db.commit()

            # Шаг 2: Обновляем данные из temp_Sales
            self._update_from_temp_sales()

            self.show_message("Данные из Disputch успешно обновлены")
            self.refresh_all_comboboxes()
            self.find_delivery()

        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка обновления из Disputch: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def _update_from_temp_sales(self):
        """Единый метод для обновления полей Invoice, Invoice_date, inv_Volume, check_Inv_volume из temp_Sales"""
        try:
            # Получаем все данные из temp_Sales
            sales_data = db.query(temp_Sales).filter(
                temp_Sales.Sborka != "-",
            ).all()
            
            # Создаем словарь для группировки данных по Bill и Sborka
            sales_data_dict = {}
            
            for sale in sales_data:
                if sale.Bill and sale.Sborka:
                    key = (sale.Bill, sale.Sborka)
                    
                    if key not in sales_data_dict:
                        sales_data_dict[key] = {
                            'Invoice': sale.Document,
                            'Invoice_date': sale.Date,
                            'Total_Volume': 0.0
                        }
                    
                    # Рассчитываем объем для текущей записи
                    material = db.query(Materials).filter(Materials.Code == sale.Material_id).first()
                    if material:
                        volume = self._calculate_volume_for_sale(sale, material)
                        sales_data_dict[key]['Total_Volume'] += float(volume)  # Приводим к float
            
            # Обновляем записи Delivery
            deliveries = db.query(Delivery_to_Customer).all()
            
            for delivery in deliveries:
                key = (delivery.Bill, delivery.Sborka)
                
                if key in sales_data_dict:
                    # Данные найдены в temp_Sales - ОБНОВЛЯЕМ
                    delivery.Invoice = sales_data_dict[key]['Invoice']
                    delivery.Invoice_date = sales_data_dict[key]['Invoice_date']
                    delivery.inv_Volume = float(sales_data_dict[key]['Total_Volume'])  # Приводим к float
                else:
                    # Данные не найдены - СБРАСЫВАЕМ
                    delivery.Invoice = "-"
                    delivery.Invoice_date = None
                    delivery.inv_Volume = 0.0  # Используем float
                
                # Обновляем check_Inv_volume на основе новых данных
                delivery_volume = float(delivery.Order_volume) if delivery.Order_volume else 0.0
                invoice_volume = float(delivery.inv_Volume) if delivery.inv_Volume else 0.0

                if invoice_volume == 0:
                    delivery.check_Inv_volume = "-"
                elif abs(invoice_volume - delivery_volume) < 0.01:
                    delivery.check_Inv_volume = "Да"
                else:
                    delivery.check_Inv_volume = "Нет"
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка обновления данных из temp_Sales: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def _calculate_volume_for_sale(self, sale, material):
        """Расчет объема в литрах для записи temp_Sales"""
        try:
            # Приводим все значения к float
            qty = float(sale.Qty) if sale.Qty else 0.0
            
            items_per_set = float(material.Items_per_Set) if material.Items_per_Set else 1.0
            package_volume = float(material.Package_Volume) if material.Package_Volume else 1.0
            
            # Условия для расчета количества в штуках
            conditions_quantity = [
                material.Product_type == 'Услуги',
                material.Package_type == 'комплект',
                material.UoM == 'шт',
                material.UoM == 'л',
                material.UoM == 'кг',
                material.UoM == 'т'
            ]

            choices_quantity = [
                0.0,  # Для услуг
                qty * items_per_set,  # Для комплектов
                qty,  # Для штук
                qty / package_volume,  # Для литров
                qty / package_volume,  # Для килограммов
                round(qty * 1000 / package_volume, 0)  # Для тонн
            ]

            # Вычисляем количество в штуках
            qty_pcs = np.select(conditions_quantity, choices_quantity, default=qty)
            
            # Вычисляем количество в литрах
            if material.UoM == 'л':
                qty_liters = qty
            elif material.UoM == 'кг':
                qty_liters = qty  # Предполагаем эквивалентность
            elif material.UoM == 'т':
                qty_liters = qty * 1000
            else:
                qty_liters = float(qty_pcs) * package_volume

            return round(float(qty_liters), 2)  # Приводим к float и округляем
            
        except Exception as e:
            print(f"Ошибка расчета объема для sale {sale.Bill}/{sale.Sborka}: {str(e)}")
            return 0.0

    def find_delivery(self):
        """Поиск данных с фильтрами"""
        try:
            # Получаем параметры фильтрации
            customer = self.ui.line_customer.currentText()
            bill = self.ui.line_bill.text().strip()
            sborka = self.ui.line_sborka.text().strip()
            changes = self.ui.line_changes.currentText()
            year = self.ui.line_Year.currentText()
            month = self.ui.line_Mnth.currentText()
            date_filter = self.ui.line_date.date().toString("yyyy-MM-dd")
            
            # Строим запрос
            query = db.query(Delivery_to_Customer)
            
            if customer != "-":
                query = query.filter(Delivery_to_Customer.Customer_name == customer)
            
            if bill:
                query = query.filter(Delivery_to_Customer.Bill.contains(bill))
            
            if sborka:
                query = query.filter(Delivery_to_Customer.Sborka.contains(sborka))
            
            if changes != "-":
                if changes == "Да":
                    query = query.filter(Delivery_to_Customer.check_Deliv_amount == "Да")
                else:
                    query = query.filter(Delivery_to_Customer.check_Deliv_amount == "Нет")
            
            if year != "-":
                query = query.filter(Delivery_to_Customer.Year_delivery == int(year))
            
            if month != "-":
                query = query.filter(Delivery_to_Customer.Delivery_date.cast('DATE').like(f"%-{int(month):02d}-%"))
            
            if date_filter != "2022-01-01":
                filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
                query = query.filter(Delivery_to_Customer.Delivery_date == filter_date)
            
            # Выполняем запрос
            results = query.all()
            
            # Отображаем результаты
            self._display_data(results)
            
        except Exception as e:
            self.show_error_message(f"Ошибка поиска: {str(e)}")

    def _display_data(self, data):
        """Отображение данных в таблице с русскими названиями колонок и правильным форматированием"""
        self.table.clear()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        
        if not data:
            self.show_message('Нет данных для отображения')
            return
        
        # Устанавливаем флаг обновления таблицы
        self._updating_table = True
        
        # Русские названия колонок
        headers = [
            'Контрагент', 'Дата отгр', 'Счет', 'Наименование Клиента', 'ИНН',
            'Перевозчик', 'Сборка', 'Способ доставки', 
            'Ставка, руб с НДС', 'Ставка без НДС', 'Объем заказа, л', 'ТС',
            'Ставка р/л', 'new_Ставка', 'true/false (ставка)', 'Объем СФ', 
            'true/false (объем)', 'Комментарий', 'ОЗОН', 'СФ', 'Дата сф', 
            'Год сф', 'Год отгр', 'Счет & Дата'
        ]
        
        # Соответствие русских названий английским полям
        column_mapping = {
            'Контрагент': 'Customer_name',
            'Дата отгр': 'Delivery_date',
            'Счет': 'Bill',
            'Наименование Клиента': 'Customer_in_logist',
            'ИНН': 'INN',
            'Перевозчик': 'Carrier',
            'Сборка': 'Sborka',
            'Способ доставки': 'Delivery_method',
            'Ставка, руб с НДС': 'Delivery_amount_w_VAT',
            'Ставка без НДС': 'Delivery_amount_wo_VAT',
            'Объем заказа, л': 'Order_volume',
            'ТС': 'TS',
            'Ставка р/л': 'CD_per_lt',
            'new_Ставка': 'new_Amount',
            'true/false (ставка)': 'check_Deliv_amount',
            'Объем СФ': 'inv_Volume',
            'true/false (объем)': 'check_Inv_volume',
            'Комментарий': 'Comment',
            'ОЗОН': 'OZON',
            'СФ': 'Invoice',
            'Дата сф': 'Invoice_date',
            'Год сф': 'Year_invoice',
            'Год отгр': 'Year_delivery',
            'Счет & Дата': 'Bill_and_Date'
        }
        
        # Создаем DataFrame для удобной сортировки
        display_data = []
        for delivery in data:
            row_data = {}
            for header, eng_field in column_mapping.items():
                value = getattr(delivery, eng_field, '')
                row_data[header] = value
            display_data.append(row_data)
        
        display_df = pd.DataFrame(display_data)
        
        # Сортируем данные как указано
        display_df = display_df.sort_values(by=['Дата отгр', 'ТС', 'Счет'], ascending=[True, True, True])
        
        # Числовые колонки для специального форматирования
        numeric_cols = [
            'Ставка, руб с НДС', 'Ставка без НДС', 'Объем заказа, л',
            'Ставка р/л', 'new_Ставка', 'Объем СФ'
        ]
        
        # Устанавливаем размеры таблицы
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(display_df))
        self.table.setHorizontalHeaderLabels(headers)
            
        # Заполняем данные
        for row_idx, (_, row) in enumerate(display_df.iterrows()):
            for col_idx, col_name in enumerate(headers):
                value = row[col_name]
                
                # Обработка пустых значений
                if pd.isna(value) or value is None or str(value) in ['None', 'nan', 'NaT']:
                    value = ''
                
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                
                # Специальное форматирование для числовых колонок
                if col_name in numeric_cols and pd.notna(value) and value != '':
                    try:
                        # Дробные значения с разделителями тысяч и запятой для дробей
                        formatted_value = f"{float(value):,.2f}".replace(",", " ").replace(".", ",")
                        item.setText(formatted_value)
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    except (ValueError, TypeError):
                        item.setText(str(value))
                        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    # Для нечисловых колонок
                    item.setText(str(value))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    
                self.table.setItem(row_idx, col_idx, item)
        
        # Автоматическая настройка ширины столбцов
        self.table.resizeColumnsToContents()
        
        # Устанавливаем минимальную ширину для некоторых колонок
        for col_idx, col_name in enumerate(headers):
            if col_name in ['Счет', 'Сборка', 'ТС']:
                self.table.setColumnWidth(col_idx, 100)
            elif col_name in numeric_cols:
                self.table.setColumnWidth(col_idx, 120)
        
        # Снимаем флаг обновления таблицы
        self._updating_table = False

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



