import os
import pandas as pd
import numpy as np
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, 
                              QApplication, QMenu, QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from functools import lru_cache
import logging

from db import db, engine
from models import Manager, TeamLead, Customer as Cust_db, Sector, Holding, Hyundai_Dealer, Contract
from wind.pages.customers_ui import Ui_Form
from config import All_data_file, Customer_file, Contract_file, Customer_teboil_file, Contract_teboil_file


class CustomerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._updating_table = False
        self._original_values = {}
        self._pending_changes = {}
        
        self._setup_ui()
        self._setup_connections()
        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.table = self.ui.table
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)
        
        # Настройка контекстного меню
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        """Показ контекстного меню"""
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        delete_action = menu.addAction("Удалить строку")
        apply_action = menu.addAction("Применить изменения")
        revert_action = menu.addAction("Отменить изменения")
        
        copy_action.triggered.connect(self.copy_selected_data)
        delete_action.triggered.connect(self.delete_selected_row)
        apply_action.triggered.connect(self.apply_pending_changes)
        revert_action.triggered.connect(self.revert_changes)
        
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def copy_selected_data(self):
        """Копирование выделенных данных"""
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

    def delete_selected_row(self):
        """Удаление выбранной строки - теперь по Customer_code"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            return
            
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить {len(selected_rows)} строк?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
            
        try:
            for row in sorted(selected_rows, reverse=True):
                row_data = {}
                for col in range(self.table.columnCount()):
                    header = self.table.horizontalHeaderItem(col).text()
                    item = self.table.item(row, col)
                    if item:
                        row_data[header] = item.text()
                
                # Определяем тип данных
                if 'Customer_name' in row_data:
                    customer_code = row_data.get('Customer_code')
                    if customer_code:
                        customer = db.query(Cust_db).filter(Cust_db.Customer_code == customer_code).first()
                        if customer:
                            db.delete(customer)
                elif 'Dealer_Name' in row_data:
                    dealer_code = row_data.get('Dealer_code')
                    if dealer_code:
                        dealer = db.query(Hyundai_Dealer).filter(Hyundai_Dealer.Dealer_code == dealer_code).first()
                        if dealer:
                            db.delete(dealer)
            
            db.commit()
            self.show_message(f'Удалено {len(selected_rows)} строк')
            
            # Обновляем таблицу
            if hasattr(self, '_current_data_type'):
                if self._current_data_type == 'Customer':
                    self.find_Customer()
                else:
                    self.find_Hyundai()
            
            self.refresh_all_comboboxes()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f'Ошибка удаления: {str(e)}')

    def on_item_changed(self, item):
        """Обработчик изменения данных в таблице"""
        if self._updating_table:
            return
        
        try:
            row = item.row()
            column = item.column()
            header = self.table.horizontalHeaderItem(column).text()
            
            row_id = self._get_row_id(row)
            if not row_id:
                return
                
            new_value = item.text()
            
            if row_id not in self._pending_changes:
                self._pending_changes[row_id] = {}
            
            self._pending_changes[row_id][header] = new_value
            
            item.setBackground(Qt.yellow)
            
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")

    def _get_row_id(self, row):
        """Получение уникального идентификатора строки - теперь по Customer_code"""
        if hasattr(self, '_current_data_type'):
            if self._current_data_type == 'Customer':
                item = self.table.item(row, 0)  # Customer_code теперь первая колонка
                return item.text() if item else None
            else:
                item = self.table.item(row, 0)  # Dealer_code
                return item.text() if item else None
        return None

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.table.itemChanged.connect(self.on_item_changed)
        self.ui.line_TL.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.line_AM.currentTextChanged.connect(self.fill_in_cust_list)
        self.ui.line_TL_Hyundai.currentTextChanged.connect(self.fill_in_dealer_kam_list)
        self.ui.line_AM_Hyundai.currentTextChanged.connect(self.fill_in_dealer_list)
        self.ui.btn_find_cust.clicked.connect(self.find_Customer)
        self.ui.btn_find_Hyundai.clicked.connect(self.find_Hyundai)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)

    def upload_data(self):
        """Загрузка всех данных за один шаг"""
        try:
            self.show_message("Начинаю обновление данных...")
            
            # Обновляем данные в порядке зависимостей
            self.update_customers_in_db()
            self.update_contracts_in_db()
            self.update_hyundai_in_db()
            
            self.show_message('Все данные успешно обновлены!')
            
            self.refresh_all_comboboxes()
            
        except Exception as e:
            self.show_error_message(f"Ошибка загрузки: {str(e)}")

    def update_customers_in_db(self):
        """Обновление клиентов с проверкой несоответствий"""
        try:
            # Чтение данных
            dtype_cust = {'Контрагент.ИНН': str}
            
            # Читаем данные из двух листов
            cust_df = pd.read_excel(All_data_file, 'Customers', dtype=dtype_cust, keep_default_na=False)
            cust_teboil_df = pd.read_excel(All_data_file, 'Customers_TEBOIL', dtype=dtype_cust, keep_default_na=False)
            
            # Объединяем
            cust_df = pd.concat([cust_df, cust_teboil_df], ignore_index=True)
            cust_df = cust_df.fillna('')
            
            # Переименовываем колонки
            column_map = {
                'Контрагент.ИНН': 'INN',
                'Контрагент.Код': 'id',
                'Контрагент': 'Customer_name',
                'SECTOR': 'Sector_name',
                'Тип цен': 'Price_type',
                'ХОЛДИНГ': 'Holding_name',
                'Регион': 'Region',
                'Город': 'City',
                'Статус клиента': 'Customer_status'  # Статус клиента
            }
            
            cust_df = cust_df.rename(columns=column_map)
            
            # Оставляем только колонки, которые были переименованы
            cust_df = cust_df[[col for col in column_map.values() if col in cust_df.columns]]
            
            # Удаляем записи с пустыми ID и 'new'
            cust_df = cust_df[cust_df['id'].astype(str).str.strip() != '']
            cust_df = cust_df[~cust_df['id'].astype(str).str.contains('new', case=False, na=False)]
            
            # Дополнительная фильтрация
            cust_df = cust_df[cust_df['id'].notna()]
            cust_df = cust_df[cust_df['id'] != '']
            cust_df = cust_df[cust_df['Customer_name'].notna()]
            
            # Заполняем пустые значения
            fill_cols = ['Sector_name', 'Price_type', 'Region', 'City', 'Customer_status']
            for col in fill_cols:
                if col in cust_df.columns:
                    cust_df[col] = cust_df[col].fillna("-")
            
            # Клиенты, которые не проверяются
            excluded_customers = ["OZON", "Yandex", "Wildberries", "СберМегаМаркет"]
            ksh_mask = cust_df['id'].astype(str).str.startswith('КШ-')
            excluded_mask = cust_df['Customer_name'].isin(excluded_customers)
            
            # Данные для проверки (только те, что проверяются)
            df_to_check = cust_df[~ksh_mask & ~excluded_mask].copy()
            
            # Проверка несоответствий с файлом Customer_file
            if not df_to_check.empty and Customer_file and os.path.exists(Customer_file):
                try:
                    df_cust1c = pd.read_excel(Customer_file, sheet_name=0, dtype={'ИНН': str})
                    df_cust1c = df_cust1c[(df_cust1c["Это группа"] == 'Нет') & (df_cust1c['Код'].isin(df_to_check['id']))]
                    
                    if not df_cust1c.empty:
                        # Подготовка данных 1С
                        column_map_1c = {
                            'ИНН': 'INN_1C',
                            'Код': 'id_1C',
                            'Наименование в программе': 'Customer_name_1C',
                            'Сектор': 'Sector_1C',
                            'Тип цен': 'Price_type_1C',
                            'Холдинг': 'Holding_1C'
                        }
                        df_cust1c = df_cust1c.rename(columns=column_map_1c)[list(column_map_1c.values())]
                        df_cust1c["Customer_name_1C"] = df_cust1c['Customer_name_1C'].str.replace('не исп_', '', regex=False)
                        df_cust1c["Holding_1C"] = df_cust1c['Holding_1C'].str.replace('не исп_', '', regex=False)
                        df_cust1c[['Sector_1C', 'Price_type_1C']] = df_cust1c[['Sector_1C', 'Price_type_1C']].fillna("-")
                        df_cust1c["Holding_1C"] = np.where(pd.isna(df_cust1c["Holding_1C"]), df_cust1c['Customer_name_1C'], df_cust1c["Holding_1C"])
                        
                        # Объединение и проверка несоответствий
                        merged = pd.merge(df_to_check, df_cust1c, left_on='id', right_on='id_1C', how='left')
                        
                        # Добавляем колонку с несоответствиями
                        merged['Несоответствия'] = ""
                        field_names = {
                            'Customer_name': 'Название',
                            'Sector_name': 'Сектор',
                            'Holding_name': 'Холдинг',
                            'Price_type': 'Тип цены'
                        }
                        
                        for col in field_names.keys():
                            if col == 'Price_type':
                                mask = (
                                    ((merged['Price_type'] == "-") & (merged['Price_type_1C'] != "-")) |
                                    ((merged['Price_type'] != "-") & (merged['Price_type_1C'] != "-") & 
                                    (merged['Price_type'] != merged['Price_type_1C']))
                                )
                            else:
                                mask = (merged[col] != merged[f"{col}_1C"]) & ~pd.isna(merged[f"{col}_1C"])
                            
                            merged.loc[mask, 'Несоответствия'] = merged.loc[mask, 'Несоответствия'] + \
                                (", " if merged.loc[mask, 'Несоответствия'].any() else "") + field_names[col]
                        
                        merged['Несоответствия'] = merged['Несоответствия'].str.lstrip(", ")
                        
                        # Формирование отчета
                        result_df = merged[merged['Несоответствия'] != ""]
                        if not result_df.empty:
                            output_df = result_df[['id', 'Customer_name', 'INN', 'Sector_name', 'Holding_name', 'Price_type', 'Customer_status', 'Несоответствия'] + 
                                        [f"{col}_1C" for col in field_names.keys()]]
                            output_file = "ERRORs_Customer_mismatches.xlsx"
                            output_df.to_excel(output_file, index=False)
                            self.show_message(f"Найдены несоответствия. Отчет сохранен в {output_file}")
                except Exception as e:
                    print(f"Предупреждение: проверка несоответствий пропущена: {str(e)}")
            
            # Создаем cust_merge для всех клиентов
            cust_df['cust_merge'] = cust_df['id'].astype(str) + '_' + cust_df['INN'].astype(str)
            
            # Получаем или создаем холдинги и секторы
            holdings = self._get_or_create_holdings(cust_df['Holding_name'].unique())
            sectors = self._get_or_create_sectors(cust_df['Sector_name'].unique())
            
            # Подготовка данных для bulk вставки
            to_insert = []
            to_update = []
            existing_customers = {c.id: c for c in db.query(Cust_db).all()}
            
            for _, row in cust_df.iterrows():
                # Базовые данные
                customer_data = {
                    'id': row['cust_merge'],  # Используем cust_merge как primary key
                    'Customer_code': row['id'],  # Оригинальный код
                    'Customer_name': row['Customer_name'],
                    'INN': row['INN'],
                    'Price_type': row['Price_type'],
                    'Holding_id': holdings.get(row['Holding_name']),
                    'Sector_id': sectors.get(row['Sector_name'])
                }
                
                # Добавляем дополнительные поля если они есть в модели
                if 'Region' in row and hasattr(Cust_db, 'Region'):
                    customer_data['Region'] = row['Region']
                if 'City' in row and hasattr(Cust_db, 'City'):
                    customer_data['City'] = row['City']
                if 'Customer_status' in row and hasattr(Cust_db, 'Customer_status'):
                    customer_data['Customer_status'] = row['Customer_status']
                
                if row['cust_merge'] in existing_customers:
                    to_update.append(customer_data)
                else:
                    to_insert.append(customer_data)
            
            # Bulk операции
            if to_insert:
                db.bulk_insert_mappings(Cust_db, to_insert)
            if to_update:
                db.bulk_update_mappings(Cust_db, to_update)
            
            db.commit()
            
            report_msg = f'Клиенты: {len(to_insert)} новых, {len(to_update)} обновлено'
            self.show_message(report_msg)
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления клиентов: {str(e)}")
        finally:
            db.close()
                       
    def update_contracts_in_db(self):
        """Обновление договоров"""
        try:
            # Чтение данных
            dtype_contract = {'Контрагент.ИНН': str, 'Партнер.ИНН': str}
            
            # Основные договоры
            contracts_df = pd.read_excel(Contract_file, dtype=dtype_contract)
            contracts_df = contracts_df.rename(columns={
                'Код': 'id',
                'Наименование': 'Contract',
                'Вид договора': 'Contract_Type',
                'Тип цен': 'Price_Type',
                'Условие оплаты': 'Payment_Condition',
                'Код контрагента': 'Customer_id',
                'Менеджер': 'Manager_name'
            })
            
            # TEBOIL договоры
            contracts_teboil_df = pd.read_excel(Contract_teboil_file, dtype=dtype_contract)
            contracts_teboil_df['Менеджер'] = contracts_teboil_df['Менеджер'].fillna('no')
            contracts_teboil_df = contracts_teboil_df[contracts_teboil_df['Менеджер'] != 'Обмен']
            
            contracts_teboil_df = contracts_teboil_df.rename(columns={
                'Идентификатор': 'id',
                'Договор с контрагентом': 'Contract',
                'Цель договора': 'Contract_Type',
                'Вид цен продажи': 'Price_Type',
                'Срок оплаты': 'Payment_Condition',
                'Партнер.Код': 'Customer_id',
                'Менеджер': 'Manager_name'
            })
            
            # Получаем менеджеров TEBOIL для фильтрации
            managers_df = pd.read_excel(All_data_file, 'AM_emails')
            teboil_managers = managers_df[managers_df['Команда'].isin(['TEBOIL B2B', 'TEBOIL B2C'])]['AM_1C name']
            
            # Фильтруем TEBOIL договоры
            contracts_teboil_df = contracts_teboil_df[contracts_teboil_df['Manager_name'].isin(teboil_managers)]
            
            # Объединяем
            contracts_df = pd.concat([contracts_df, contracts_teboil_df], ignore_index=True)
            contracts_df['Manager_name'] = contracts_df['Manager_name'].fillna('-')
            
            # Получаем маппинги
            existing_contracts = {c.id for c in db.query(Contract.id).all()}
            existing_customers = {c.id for c in db.query(Cust_db.id).all()}
            
            managers = db.query(Manager).all()
            manager_name_to_id = {m.AM_1C_Name: m.id for m in managers if m.AM_1C_Name}
            manager_name_fallback = {m.Manager_name: m.id for m in managers if m.Manager_name}
            
            # Специальный менеджер для "-"
            special_manager = db.query(Manager).filter(Manager.AM_1C_Name == "-").first()
            if not special_manager:
                special_manager = Manager(Manager_name="-", AM_1C_Name="-")
                db.add(special_manager)
                db.flush()
            special_manager_id = special_manager.id
            
            to_insert = []
            to_update = []
            skipped = []
            
            for _, row in contracts_df.iterrows():
                contract_id = row['id']
                customer_id = row['Customer_id']
                manager_name = str(row['Manager_name']).strip()
                
                if not contract_id or pd.isna(contract_id):
                    continue
                
                if customer_id not in existing_customers:
                    skipped.append(f"Пропущен {contract_id}: клиент не найден")
                    continue
                
                # Определяем менеджера
                if not manager_name or manager_name == '-':
                    manager_id = special_manager_id
                else:
                    manager_id = manager_name_to_id.get(manager_name)
                    if not manager_id:
                        manager_id = manager_name_fallback.get(manager_name)
                    
                    if not manager_id:
                        skipped.append(f"Пропущен {contract_id}: менеджер не найден")
                        continue
                
                contract_data = {
                    'id': contract_id,
                    'Contract': row['Contract'],
                    'Contract_Type': row['Contract_Type'],
                    'Price_Type': row.get('Price_Type'),
                    'Payment_Condition': row.get('Payment_Condition'),
                    'Customer_id': customer_id,
                    'Manager_id': manager_id
                }
                
                if contract_id in existing_contracts:
                    to_update.append(contract_data)
                else:
                    to_insert.append(contract_data)
            
            # Bulk операции
            if to_insert:
                db.bulk_insert_mappings(Contract, to_insert)
            if to_update:
                db.bulk_update_mappings(Contract, to_update)
            
            db.commit()
            
            report = f"Договоры: {len(to_insert)} новых, {len(to_update)} обновлено"
            if skipped:
                report += f", {len(skipped)} пропущено"
            self.show_message(report)
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления договоров: {str(e)}")
        finally:
            db.close()

    def update_hyundai_in_db(self):
        """Упрощенное обновление Hyundai"""
        try:
            df = pd.read_excel(All_data_file, 'HYUNDAI', dtype={
                'ИНН': str,
                'Код дилера HYUNDAI': str,
                'Код в HYUNDAI': str
            })
            
            df = df.rename(columns={
                'Код дилера HYUNDAI': 'Dealer_code',
                'Наим дилера HYUNDAI': 'Name',
                'Код в HYUNDAI': 'Hyundai_code',
                'Город': 'City',
                'ИНН': 'INN',
                'SALES': 'Manager_name'
            })
            
            df = df[df['Dealer_code'] != "-"]
            df['Manager_name'] = df['Manager_name'].fillna('-')
            
            # Получаем маппинги
            existing_dealers = {d.Hyundai_code for d in db.query(Hyundai_Dealer.Hyundai_code).all()}
            managers = db.query(Manager).all()
            manager_name_to_id = {m.Manager_name: m.id for m in managers if m.Manager_name}
            
            to_insert = []
            to_update = []
            
            for _, row in df.iterrows():
                manager_id = manager_name_to_id.get(row['Manager_name'])
                if not manager_id:
                    manager_id = manager_name_to_id.get('-')
                
                if not manager_id:
                    continue
                
                dealer_data = {
                    'Dealer_code': row['Dealer_code'] if row['Dealer_code'] != '-' else None,
                    'Hyundai_code': row['Hyundai_code'],
                    'Name': row['Name'],
                    'City': row['City'],
                    'INN': row['INN'],
                    'Manager_id': manager_id
                }
                
                if row['Hyundai_code'] in existing_dealers:
                    to_update.append(dealer_data)
                else:
                    to_insert.append(dealer_data)
            
            # Bulk операции
            if to_insert:
                db.bulk_insert_mappings(Hyundai_Dealer, to_insert)
            if to_update:
                db.bulk_update_mappings(Hyundai_Dealer, to_update)
            
            db.commit()
            self.show_message(f'Hyundai: {len(to_insert)} новых, {len(to_update)} обновлено')
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления Hyundai: {str(e)}")
        finally:
            db.close()

    def _get_or_create_holdings(self, holding_names):
        """Получение или создание холдингов"""
        holdings = {}
        existing_holdings = {h.Holding_name: h.id for h in db.query(Holding).all()}
        
        to_create = []
        for name in holding_names:
            if pd.isna(name) or name == '-':
                continue
            if name not in existing_holdings and name not in holdings:
                to_create.append({'Holding_name': name})
        
        if to_create:
            db.bulk_insert_mappings(Holding, to_create)
            db.commit()
            # Обновляем словарь
            existing_holdings = {h.Holding_name: h.id for h in db.query(Holding).all()}
        
        for name in holding_names:
            if pd.isna(name) or name == '-':
                continue
            holdings[name] = existing_holdings.get(name)
        
        return holdings

    def _get_or_create_sectors(self, sector_names):
        """Получение или создание секторов"""
        sectors = {}
        existing_sectors = {s.Sector_name: s.id for s in db.query(Sector).all()}
        
        to_create = []
        for name in sector_names:
            if pd.isna(name) or name == '-':
                continue
            if name not in existing_sectors and name not in sectors:
                to_create.append({'Sector_name': name})
        
        if to_create:
            db.bulk_insert_mappings(Sector, to_create)
            db.commit()
            existing_sectors = {s.Sector_name: s.id for s in db.query(Sector).all()}
        
        for name in sector_names:
            if pd.isna(name) or name == '-':
                continue
            sectors[name] = existing_sectors.get(name)
        
        return sectors

    def apply_pending_changes(self):
        """Применение изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для применения")
            return
            
        try:
            data_type = getattr(self, '_current_data_type', 'Customer')
            applied = 0
            
            for row_id, changes in self._pending_changes.items():
                for header, value in changes.items():
                    if data_type == 'Customer':
                        success = self._update_customer(row_id, header, value)
                    else:
                        success = self._update_hyundai(row_id, header, value)
                    
                    if success:
                        applied += 1
            
            db.commit()
            self._pending_changes.clear()
            self._reset_table_colors()
            
            if data_type == 'Customer':
                self.find_Customer()
            else:
                self.find_Hyundai()
            
            self.show_message(f"Применено {applied} изменений")
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка: {str(e)}")

    def _update_customer(self, customer_code, field, value):
        """Обновление данных клиента по Customer_code"""
        try:
            # Находим клиента сначала по Customer_code
            customer = db.query(Cust_db).filter(Cust_db.Customer_code == customer_code).first()
            if not customer:
                return False
            
            field_mapping = {
                'Customer_name': 'Customer_name',
                'Customer_code': 'Customer_code',
                'INN': 'INN',
                'Price_type': 'Price_type',
                'Region': 'Region',
                'City': 'City',
                'Customer_status': 'Customer_status',
                'Delivery': 'Delivery',
                'Holding': 'Holding_id',
                'Sector': 'Sector_id'
            }
            
            db_field = field_mapping.get(field)
            if not db_field:
                return False
            
            # Для связанных полей нужно получить ID
            if field == 'Holding':
                holding = db.query(Holding).filter(Holding.Holding_name == value).first()
                value = holding.id if holding else None
            elif field == 'Sector':
                sector = db.query(Sector).filter(Sector.Sector_name == value).first()
                value = sector.id if sector else None
            
            # Особый случай: если меняется Customer_code или INN, нужно пересчитать cust_merge
            if field in ['Customer_code', 'INN']:
                # Обновляем поле
                setattr(customer, db_field, value)
                # Пересчитываем cust_merge
                customer.id = f"{customer.Customer_code}_{customer.INN}"
            else:
                setattr(customer, db_field, value)
            
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка обновления клиента: {str(e)}")

    def _update_hyundai(self, dealer_code, field, value):
        """Обновление Hyundai"""
        try:
            dealer = db.query(Hyundai_Dealer).filter(Hyundai_Dealer.Dealer_code == dealer_code).first()
            if not dealer:
                return False
            
            field_map = {
                'Dealer_Name': 'Name',
                'Hyundai_code': 'Hyundai_code',
                'City': 'City',
                'INN': 'INN',
                'AM': 'Manager_id'
            }
            
            db_field = field_map.get(field)
            if not db_field:
                return False
            
            if field == 'AM':
                manager = db.query(Manager).filter(Manager.Manager_name == value).first()
                value = manager.id if manager else None
            
            setattr(dealer, db_field, value)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка обновления дилера: {str(e)}")

    def _reset_table_colors(self):
        """Сброс цветов"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(Qt.white)

    def revert_changes(self):
        """Отмена изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для отмены")
            return
            
        self._pending_changes.clear()
        self._reset_table_colors()
        
        if hasattr(self, '_current_data_type'):
            if self._current_data_type == 'Customer':
                self.find_Customer()
            else:
                self.find_Hyundai()
        
        self.show_message("Изменения отменены")

    @lru_cache(maxsize=32)
    def _get_id(self, model, name_field, name):
        """Получение ID по имени"""
        if not name or name in ('-', '') or pd.isna(name):
            return None
        item = db.query(model).filter(getattr(model, name_field) == name).first()
        return item.id if item else None

    def get_Customers_from_db(self):
        """Получение клиентов из базы, возвращает Customer_code вместо id"""
        try:
            # Базовый запрос
            query = db.query(
                Cust_db.Customer_code.label('Customer_code'),
                Cust_db.id.label('cust_merge'),
                Cust_db.Customer_name,
                Cust_db.INN,
                Cust_db.Price_type,
                Holding.Holding_name.label('Holding'),
                Sector.Sector_name.label('Sector'),
                Manager.Manager_name.label('AM'),
                TeamLead.TeamLead_name.label('TeamLead')
            ).outerjoin(Holding, Cust_db.Holding_id == Holding.id) \
             .outerjoin(Sector, Cust_db.Sector_id == Sector.id) \
             .outerjoin(Contract, Contract.Customer_id == Cust_db.id) \
             .outerjoin(Manager, Contract.Manager_id == Manager.id) \
             .outerjoin(TeamLead, Manager.TeamLead_id == TeamLead.id)
            
            # Добавляем дополнительные поля если они есть в модели
            if hasattr(Cust_db, 'Region'):
                query = query.add_columns(Cust_db.Region)
            if hasattr(Cust_db, 'City'):
                query = query.add_columns(Cust_db.City)
            if hasattr(Cust_db, 'Customer_status'):
                query = query.add_columns(Cust_db.Customer_status)
            
            df = pd.read_sql(query.statement, db.bind)
            
            if not df.empty:
                # Определяем ключи для группировки
                group_keys = ['Customer_code', 'cust_merge']
                
                # Создаем словарь агрегации
                agg_dict = {
                    'Customer_name': 'first',
                    'INN': 'first',
                    'Price_type': 'first',
                    'Holding': 'first',
                    'Sector': 'first',
                    'AM': lambda x: ', '.join(set(filter(None, x))),
                    'TeamLead': lambda x: ', '.join(set(filter(None, x)))
                }
                
                # Добавляем дополнительные поля
                if 'Region' in df.columns:
                    agg_dict['Region'] = 'first'
                if 'City' in df.columns:
                    agg_dict['City'] = 'first'
                if 'Customer_status' in df.columns:
                    agg_dict['Customer_status'] = 'first'
                
                grouped = df.groupby(group_keys).agg(agg_dict).reset_index()
                
                # Переставляем колонки в удобном порядке
                column_order = ['Customer_code', 'Customer_name', 'INN', 'Price_type', 'Holding', 'Sector']
                
                # Добавляем дополнительные поля
                if 'Region' in grouped.columns:
                    column_order.append('Region')
                if 'City' in grouped.columns:
                    column_order.append('City')
                if 'Customer_status' in grouped.columns:
                    column_order.append('Customer_status')
                
                # Добавляем AM и TeamLead в конец
                column_order.extend(['AM', 'TeamLead'])
                
                # Упорядочиваем колонки
                grouped = grouped[column_order]
                
                return grouped.where(pd.notnull(grouped), None)
            else:
                return pd.DataFrame()
            
        except Exception as e:
            self.show_error_message(f"Ошибка при получении клиентов: {str(e)}")
            return pd.DataFrame()
        
    def get_Hyundai_from_db(self):
        """Получение Hyundai"""
        try:
            query = db.query(
                Hyundai_Dealer.Dealer_code,
                Hyundai_Dealer.Name.label('Dealer_Name'),
                Hyundai_Dealer.Hyundai_code.label('Hyundai_code'),
                Hyundai_Dealer.INN,
                Hyundai_Dealer.City,
                Manager.Manager_name.label('AM'),
                TeamLead.TeamLead_name.label('TeamLead')
            ).join(Manager, Hyundai_Dealer.Manager_id == Manager.id) \
             .outerjoin(TeamLead, Manager.TeamLead_id == TeamLead.id)
            
            df = pd.read_sql(query.statement, db.bind)
            return df.where(pd.notnull(df), None)
            
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")
            return pd.DataFrame()

    def find_Customer(self):
        """Поиск клиентов по Customer_code (Контрагент.Код)"""
        self.table.clearContents()
        self.table.setRowCount(0)
        self._current_data_type = 'Customer'

        try:
            cust_df = self.get_Customers_from_db()
            if cust_df.empty:
                self.show_error_message('Нет данных о клиентах')
                return

            # Получаем значение из поля поиска (это Customer_code)
            cust_code = self.ui.line_ID.text().strip()
            cust_inn = self.ui.line_INN.text().strip()
            customer_name = self.ui.line_CustName.currentText()
            am = self.ui.line_AM.currentText()
            tl = self.ui.line_TL.currentText()

            # Фильтры - основным поиском теперь является Customer_code
            if cust_code:
                cust_df = cust_df[cust_df['Customer_code'] == cust_code]
            elif cust_inn:
                cust_df = cust_df[cust_df['INN'] == cust_inn]
            elif customer_name != '-':
                cust_df = cust_df[cust_df['Customer_name'] == customer_name]
            elif am != '-':
                cust_df = cust_df[cust_df['AM'].str.contains(am, na=False)]
            elif tl != '-':
                cust_df = cust_df[cust_df['TeamLead'].str.contains(tl, na=False)]

            self._display_data(cust_df, 'Customer')

        except Exception as e:
            self.show_error_message(f'Ошибка при поиске клиентов: {str(e)}')

    def find_Hyundai(self):
        """Поиск Hyundai"""
        self.table.clearContents()
        self.table.setRowCount(0)
        self._current_data_type = 'Hyundai'

        try:
            df = self.get_Hyundai_from_db()
            if df.empty:
                self.show_error_message('Нет данных')
                return

            # Фильтры
            dealer_id = self.ui.line_ID_Hyundai.text().strip()
            dealer_code = self.ui.line_Hyu_code.text().strip()
            dealer_name = self.ui.line_CustName_Hyundai.currentText()
            am = self.ui.line_AM_Hyundai.currentText()
            tl = self.ui.line_TL_Hyundai.currentText()

            if dealer_id:
                df = df[df['Dealer_code'] == dealer_id]
            elif dealer_code:
                df = df[df['Hyundai_code'] == dealer_code]
            elif dealer_name != '-':
                df = df[df['Dealer_Name'] == dealer_name]
            elif am != '-':
                df = df[df['AM'] == am]
            elif tl != '-':
                df = df[df['TeamLead'] == tl]

            self._display_data(df, 'Hyundai')

        except Exception as e:
            self.show_error_message(f'Ошибка: {str(e)}')

    def _display_data(self, df, data_type):
        """Отображение данных в таблице"""
        self._updating_table = True
        
        self.table.clear()
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(0)

        if df.empty:
            self.show_message('Ничего не найдено')
            self._updating_table = False
            return
        
        df = df.fillna('')
        # Исключаем cust_merge из отображения, показываем только Customer_code
        if 'cust_merge' in df.columns:
            df = df.drop(columns=['cust_merge'])
        
        headers = df.columns.tolist()
        
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(df))

        for i in range(len(df)):
            for j, col in enumerate(headers):
                value = df.iloc[i][col]
                value_str = str(value)

                item = QTableWidgetItem(value_str)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Используем Customer_code как уникальный идентификатор
                row_id = str(df.iloc[i]['Customer_code']) if 'Customer_code' in df.columns else str(i)
                if row_id not in self._original_values:
                    self._original_values[row_id] = {}
                self._original_values[row_id][col] = value_str

                self.table.setItem(i, j, item)
        
        self.table.resizeColumnsToContents()
        self._updating_table = False

    def refresh_all_comboboxes(self):
        """Обновление комбобоксов"""
        self._get_id.cache_clear()
        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_cust_list()
        self.fill_in_dealer_tl_list()
        self.fill_in_dealer_kam_list()
        self.fill_in_dealer_list()

    def fill_in_tl_list(self):
        """Заполнение TL"""
        team_leads = db.query(TeamLead.TeamLead_name).distinct().all()
        items = [tl[0] for tl in team_leads if tl[0] and tl[0] not in ('-', 'no')]
        self._fill_combobox(self.ui.line_TL, items)
        self._fill_combobox(self.ui.line_TL_Hyundai, items)

    def fill_in_kam_list(self):
        """Заполнение KAM"""
        tl = self.ui.line_TL.currentText()
        query = db.query(Manager.Manager_name)

        if tl != '-':
            query = query.join(TeamLead).filter(TeamLead.TeamLead_name == tl)

        kam_names = [kam[0] for kam in query.distinct().all() if kam[0] and kam[0] not in ('-', 'no')]
        self._fill_combobox(self.ui.line_AM, kam_names)

    def fill_in_cust_list(self):
        """Заполнение списка клиентов - используем Customer_name"""
        cust_df = self.get_Customers_from_db()
        if cust_df.empty:
            self._fill_combobox(self.ui.line_CustName, [])
            return

        am = self.ui.line_AM.currentText()
        tl = self.ui.line_TL.currentText()

        if am != '-':
            cust_names = cust_df[cust_df['AM'].str.contains(am, na=False)]['Customer_name'].unique()
        elif tl != '-':
            cust_names = cust_df[cust_df['TeamLead'].str.contains(tl, na=False)]['Customer_name'].unique()
        else:
            cust_names = cust_df['Customer_name'].unique()

        cust_names = [name for name in cust_names if name and str(name).strip() != '']
        self._fill_combobox(self.ui.line_CustName, sorted(cust_names))

    def fill_in_dealer_tl_list(self):
        """Заполнение TL для дилеров"""
        try:
            query = db.query(TeamLead.TeamLead_name).distinct() \
                    .join(Manager, Manager.TeamLead_id == TeamLead.id) \
                    .join(Hyundai_Dealer, Hyundai_Dealer.Manager_id == Manager.id)
            
            team_leads = [tl[0] for tl in query.all() if tl[0] and tl[0] not in ('-', 'no')]
            self._fill_combobox(self.ui.line_TL_Hyundai, team_leads)
        except Exception as e:
            self._fill_combobox(self.ui.line_TL_Hyundai, [])

    def fill_in_dealer_kam_list(self):
        """Заполнение KAM для дилеров"""
        try:
            tl = self.ui.line_TL_Hyundai.currentText()
            query = db.query(Manager.Manager_name).distinct() \
                    .join(Hyundai_Dealer, Hyundai_Dealer.Manager_id == Manager.id)
            
            if tl != '-':
                query = query.join(TeamLead).filter(TeamLead.TeamLead_name == tl)
            
            kam_names = [kam[0] for kam in query.all() if kam[0] and kam[0] not in ('-', 'no')]
            self._fill_combobox(self.ui.line_AM_Hyundai, kam_names)
        except Exception as e:
            self._fill_combobox(self.ui.line_AM_Hyundai, [])

    def fill_in_dealer_list(self):
        """Заполнение дилеров"""
        try:
            dealer_df = self.get_Hyundai_from_db()
            if dealer_df.empty:
                self._fill_combobox(self.ui.line_CustName_Hyundai, [])
                return

            am = self.ui.line_AM_Hyundai.currentText()
            tl = self.ui.line_TL_Hyundai.currentText()

            if am != '-':
                dealer_names = dealer_df[dealer_df['AM'] == am]['Dealer_Name'].dropna().unique()
            elif tl != '-':
                dealer_names = dealer_df[dealer_df['TeamLead'] == tl]['Dealer_Name'].dropna().unique()
            else:
                dealer_names = dealer_df['Dealer_Name'].dropna().unique()

            dealer_names = [name for name in dealer_names if name and str(name).strip() != '']
            self._fill_combobox(self.ui.line_CustName_Hyundai, sorted(dealer_names))
        except Exception as e:
            self._fill_combobox(self.ui.line_CustName_Hyundai, [])

    def _fill_combobox(self, combobox, items):
        """Заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if items:
            combobox.addItems(sorted(items))

    def show_message(self, text):
        """Показать сообщение"""
        self.ui.label_msg.setText(text)
        self.ui.label_msg.setStyleSheet("""
            QLabel {
                background-color: #CCFF99;
                color: #12501A;
                border: 2px solid #12501A;
                border-radius: 5px;
                padding: 8px;
                font: 10pt "Tahoma";
                margin: 2px;
            }
        """)
        self.ui.label_msg.setVisible(True)

    def show_error_message(self, text):
        """Показать ошибку"""
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