
import os
import pandas as pd
import numpy as np
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QApplication, QMenu,
                              QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from functools import lru_cache

from db import db, engine
from models import Manager, TeamLead, Customer as Cust_db, Sector, Holding, Hyundai_Dealer, Contract
from wind.pages.customers_ui import Ui_Form
from config import All_data_file, Customer_file, Contract_file


class Customer(QWidget):
    def __init__(self):
        super(Customer, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._setup_ui()
        self._setup_connections()

        self.current_upload_step = 0  # 0 - ожидание Customer, 1 - ожидание Contract
        self.cust_file_path = None
        self.contract_file_path = None

        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # Изменено с SelectRows на SelectItems
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
        self.ui.line_TL.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.line_AM.currentTextChanged.connect(self.fill_in_cust_list)
        self.ui.line_TL_Hyundai.currentTextChanged.connect(self.fill_in_dealer_kam_list)
        self.ui.line_AM_Hyundai.currentTextChanged.connect(self.fill_in_dealer_list)
        self.ui.btn_find_cust.clicked.connect(self.find_Customer)
        self.ui.btn_find_Hyundai.clicked.connect(self.find_Hyundai)
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)

    def get_file(self):
        """Выбор файла через диалоговое окно"""
        title = 'Выберите файл для Customer и Holding' if self.current_upload_step == 0 else 'Выберите файл для Contract'
        file_path, _ = QFileDialog.getOpenFileName(self, title)

        if file_path:
            if self.current_upload_step == 0:
                self.cust_file_path = file_path
            else:
                self.contract_file_path = file_path
            self.ui.label_Cust_File.setText(file_path)

    def upload_data(self):
        """Загрузка данных клиентов и контрактов за один шаг"""
        file_path = self.cust_file_path or Customer_file
        contract_path = self.contract_file_path or Contract_file
        
        try:
            # Проверка файлов
            if not os.path.exists(file_path):
                raise Exception(f"Файл клиентов {os.path.basename(file_path)} не найден")
            if not os.path.exists(contract_path):
                raise Exception(f"Файл контрактов {os.path.basename(contract_path)} не найден")

            # Начинаем транзакцию
            try:

                self.run_customer_func(file_path)
                self.run_contract_func(contract_path)
                
                db.commit()
                self.show_message('Данные клиентов и контрактов успешно загружены!')
                
                # Сброс состояния
                self.current_upload_step = 0
                self.cust_file_path = None
                self.contract_file_path = None
                self.ui.label_Cust_File.setText("Файлы успешно загружены")
                
                # Обновление интерфейса
                self.refresh_all_comboboxes()
                
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()

        except Exception as e:
            self._handle_upload_error(e, "клиентов и контрактов")

    def _handle_upload_error(self, error, data_type):
        """Обработка ошибок загрузки"""
        if "transaction is already begun" in str(error):
            msg = "Ошибка БД. Закройте программу и попробуйте снова."
        elif "required columns" in str(error).lower():
            msg = "Файл не содержит всех необходимых столбцов."
        else:
            msg = f"Ошибка загрузки {data_type}: {str(error)}"
        self.show_error_message(msg)

    def run_customer_func(self, data_file_xls):
        """Основная функция обработки данных Customer и Holding"""
        data = self.read_customer_file(data_file_xls)
        self.save_Sector(data)
        self.save_Holding(data)
        self.save_Customer(data)
        self.show_message('Данные клиентов загружены в БД')
        data2 = self.read_HYUNDAI_file(All_data_file)
        self.save_HYUNDAI(data2)
        self.refresh_all_comboboxes()

    def run_contract_func(self, contract_file_xls):
        """Основная функция обработки данных Contract"""
        data = self.read_contract_file(contract_file_xls)
        self.save_Contract(data)

    def read_customer_file(self, cust_file_xls):
        """Чтение данных клиентов с детализацией несоответствий"""
        try:
            # Чтение и подготовка данных
            df = pd.read_excel(All_data_file, sheet_name='Customers', dtype={'Контрагент.ИНН': str})
            
            column_map = {
                'Контрагент.ИНН': 'INN',
                'Контрагент.Код': 'id',
                'Контрагент': 'Customer_name',
                'SECTOR': 'Sector',
                'Тип цен': 'Price_type',
                'ХОЛДИНГ': 'Holding'
            }
            df = df.rename(columns=column_map)[list(column_map.values())]
            df[['Sector', 'Price_type']] = df[['Sector', 'Price_type']].fillna("-")
            
            # Удаляем записи с 'new'
            df = df[~df['id'].astype(str).str.contains('new', case=False, na=False)]
            
            # Клиенты, которые не проверяются
            excluded_customers = ["OZON", "Yandex", "Wildberries", "СберМегаМаркет"]
            ksh_mask = df['id'].astype(str).str.startswith('КШ-')
            excluded_mask = df['Customer_name'].isin(excluded_customers)
            
            # Данные для проверки
            df_to_check = df[~ksh_mask & ~excluded_mask].copy()
            
            if not df_to_check.empty:
                df_cust1c = pd.read_excel(cust_file_xls, sheet_name=0, dtype={'ИНН': str})
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
                    
                    # Добавляем колонку с несоответствиями только в df_to_check
                    merged['Несоответствия'] = ""
                    field_names = {
                        'Customer_name': 'Название',
                        'Sector': 'Сектор',
                        'Holding': 'Холдинг',
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
                    
                    # Формирование отчета только по проверенным данным
                    result_df = merged[merged['Несоответствия'] != ""]
                    if not result_df.empty:
                        output_df = result_df[['id', 'Customer_name', 'INN', 'Sector', 'Holding', 
                                            'Price_type', 'Несоответствия'] + 
                                    [f"{col}_1C" for col in field_names.keys()]]
                        output_file = "mismatches_report.xlsx"
                        output_df.to_excel(output_file, index=False)
                        self.show_message(
                            f"Найдено {len(result_df)} несоответствий.\n"
                            f"Отчет сохранен в {output_file}\n"
                            "Проверьте данные в файле клиентов"
                        )
            
            # Возвращаем все данные (кроме 'new') для загрузки в БД
            return df.to_dict('records')

        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла клиентов: {str(e)}")
            return []

    def read_contract_file(self, contract_file_xls):
        """Чтение данных договоров из Excel с обработкой NaN"""
        try:
            df = pd.read_excel(contract_file_xls, sheet_name=0, dtype={'Код контрагента': str}).replace([np.nan], [None])

            required_columns = ['Код', 'Вид договора', 'Наименование', 'Условие оплаты']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит необходимых столбцов")
            
            df["Менеджер"] = df["Менеджер"].fillna("-")
            column_map = {
                'Вид договора': 'Contract_Type', 
                'Код': 'id',
                'Менеджер': 'Manager_name', 
                'Наименование': 'Contract',
                'Тип цен': 'Price_Type', 
                'Условие оплаты': 'Payment_Condition',
                'Код контрагента': 'Customer_id'
            }

            df = df.rename(columns=column_map)[list(column_map.values())]
            return df[df['id'] != 'n/a'].to_dict('records')

        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла договоров: {str(e)}")
            return []

    def read_HYUNDAI_file(self, file_path):
        """Чтение данных дилеров Hyundai из Excel с правильным маппингом колонок"""
        try:
            df = pd.read_excel(file_path, sheet_name='HYUNDAI', dtype={
                'ИНН': str,
                'Код дилера HYUNDAI': str,
                'Код в HYUNDAI': str
            })

            # Проверка обязательных колонок
            required_columns = [
                'Код дилера HYUNDAI',
                'Наим дилера HYUNDAI',
                'Код в HYUNDAI',
                'Город',
                'ИНН',
                'SALES'  # Это колонка с менеджером
            ]

            if not all(col in df.columns for col in required_columns):
                missing = set(required_columns) - set(df.columns)
                raise ValueError(f"Отсутствуют обязательные колонки: {missing}")

            # Точное соответствие колонок Excel и модели
            column_map = {
                'Код дилера HYUNDAI': 'Dealer_code',
                'Наим дилера HYUNDAI': 'Name',
                'Код в HYUNDAI': 'Hyundai_code',
                'Город': 'City',
                'ИНН': 'INN',
                'SALES': 'Manager_name'  # Колонка с именем менеджера
            }

            # Преобразование и очистка данных
            df = df.rename(columns=column_map)
            df = df[list(column_map.values())]  # Только нужные колонки

            # Обработка пустых значений
            df['Dealer_code'] = df['Dealer_code'].replace(['', ' ', '-'], None)
            df['INN'] = df['INN'].str.strip()

            return df.to_dict('records')

        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла Hyundai: {str(e)}")
            return []

    def save_Sector(self, data):
        """Сохранение секторов с обновлением существующих"""
        if not data:
            return

        sectors = pd.DataFrame(data)[['Sector']].drop_duplicates()

        # Получаем существующие сектора
        existing_sectors = {s.Sector_name: s.id for s in db.query(Sector).all()}

        to_insert = []
        to_update = []

        for _, row in sectors.iterrows():
            sector_name = row['Sector']
            if sector_name in existing_sectors:
                to_update.append({
                    'id': existing_sectors[sector_name],
                    'Sector_name': sector_name
                })
            else:
                to_insert.append({
                    'Sector_name': sector_name
                })

        try:
            if to_insert:
                db.bulk_insert_mappings(Sector, to_insert)
            if to_update:
                db.bulk_update_mappings(Sector, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения секторов: {str(e)}")
        finally:
            db.close()

    def save_Holding(self, data):
        """Сохранение холдингов (проверяет только уникальность названия)"""
        if not data:
            return

        # Получаем все существующие холдинги (только названия)
        existing_holdings = {h[0] for h in db.query(Holding.Holding_name).all()}

        # Уникальные названия холдингов из входных данных
        holdings_names = {row['Holding'] for row in data if 'Holding' in row}

        # Фильтруем только новые холдинги
        new_holdings = [{'Holding_name': name} for name in holdings_names
                        if name not in existing_holdings]

        try:
            if new_holdings:
                db.bulk_insert_mappings(Holding, new_holdings)
                db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения холдингов: {str(e)}")
        finally:
            db.close()

    def save_Customer(self, data):
        """Сохранение клиентов с обновлением существующих"""
        if not data:
            return

        existing_customers = {c.id: c for c in db.query(Cust_db).all()}
        to_insert = []
        to_update = []

        for row in data:
            customer_id = row['id']
            customer_data = {
                'id': customer_id,
                'Customer_name': row['Customer_name'],
                'INN': str(row['INN']),
                'Holding_id': self._get_id(Holding, 'Holding_name', row['Holding']),
                'Sector_id': self._get_id(Sector, 'Sector_name', row['Sector']),
                'Price_type': row['Price_type']
            }

            if customer_id in existing_customers:
                to_update.append(customer_data)
            else:
                to_insert.append(customer_data)

        try:
            if to_insert:
                db.bulk_insert_mappings(Cust_db, to_insert)
            if to_update:
                db.bulk_update_mappings(Cust_db, to_update)
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения клиентов: {str(e)}")
        finally:
            db.close()

    def save_Contract(self, data):
        """Сохранение договоров с поиском менеджеров по AM_1C_Name"""
        if not data:
            self.show_message("Нет данных для сохранения")
            return

        stats = {
            'total': 0,
            'saved': 0,
            'no_manager': 0,
            'invalid_customer': 0,
            'missing_fields': 0,
            'skipped': []
        }

        try:
            # Получаем справочники из БД
            existing_contracts = {c.id: c for c in db.query(Contract).all()}
            
            # Важное изменение: создаем словарь для поиска менеджеров по AM_1C_Name
            managers = db.query(Manager).all()
            manager_name_to_id = {
                m.AM_1C_Name: m.id 
                for m in managers 
                if m.AM_1C_Name  # Исключаем пустые значения
            }
            
            # Дополнительный словарь для обратной совместимости (если часть данных использует Manager_name)
            manager_name_fallback = {
                m.Manager_name: m.id 
                for m in managers 
                if m.Manager_name  # Исключаем пустые значения
            }
            
            customer_ids = {c[0] for c in db.query(Cust_db.id).all()}
            
            to_insert = []
            to_update = []

            for row in data:
                stats['total'] += 1
                
                # Проверка обязательных полей
                required_fields = ['id', 'Contract', 'Contract_Type', 'Customer_id', 'Manager_name']
                if not all(field in row for field in required_fields):
                    stats['missing_fields'] += 1
                    stats['skipped'].append(f"Отсутствуют обязательные поля в строке {stats['total']}")
                    continue

                # Проверка менеджера (основная логика)
                manager_name = str(row['Manager_name']).strip()
                if not manager_name or manager_name == '-':
                    stats['no_manager'] += 1
                    stats['skipped'].append(f"{row.get('Contract', 'Без названия')} (Пустое имя менеджера)")
                    continue
                    
                # Поиск менеджера по AM_1C_Name (основной способ)
                manager_id = manager_name_to_id.get(manager_name)
                
                # Если не нашли, пробуем найти по Manager_name (для обратной совместимости)
                if not manager_id:
                    manager_id = manager_name_fallback.get(manager_name)
                
                if not manager_id:
                    stats['no_manager'] += 1
                    stats['skipped'].append(f"{row.get('Contract', 'Без названия')} (Менеджер '{manager_name}' не найден ни по AM_1C_Name, ни по Manager_name)")
                    continue

                # Проверка customer_id
                customer_id = row['Customer_id']
                if not customer_id or customer_id not in customer_ids:
                    stats['invalid_customer'] += 1
                    stats['skipped'].append(f"{row.get('Contract', 'Без названия')} (Неверный Customer_id: {customer_id})")
                    continue

                # Формирование данных договора
                contract_data = {
                    'id': row['id'],
                    'Contract': row['Contract'],
                    'Contract_Type': row['Contract_Type'],
                    'Price_Type': row.get('Price_Type'),
                    'Payment_Condition': row.get('Payment_Condition'),
                    'Customer_id': customer_id,
                    'Manager_id': manager_id
                }

                if row['id'] in existing_contracts:
                    to_update.append(contract_data)
                else:
                    to_insert.append(contract_data)
                stats['saved'] += 1

            # Сохранение данных
            if to_insert:
                db.bulk_insert_mappings(Contract, to_insert)
            if to_update:
                db.bulk_update_mappings(Contract, to_update)
            db.commit()

            # Формирование отчёта
            report = [
                f"Всего обработано: {stats['total']}",
                f"Сохранено договоров: {stats['saved']}"
            ]
            
            self.show_message("\n".join(report))

        except SQLAlchemyError as e:
            db.rollback()
            error_msg = f"Ошибка сохранения договоров: {str(e)}\n\n{stats}"
            self.show_error_message(error_msg)
        finally:
            db.close()

    def save_HYUNDAI(self, data):
        """Сохранение дилеров Hyundai с обновлением существующих"""
        if not data:
            return

        existing_dealers = {d.Hyundai_code: d.id for d in db.query(Hyundai_Dealer).all()}
        to_insert = []
        to_update = []

        for row in data:
            hyundai_code = row['Hyundai_code']
            manager_id = self._get_id(Manager, 'Manager_name', row['Manager_name'])
            if not manager_id:
                continue

            dealer_data = {
                'Dealer_code': row['Dealer_code'] if row['Dealer_code'] != '-' else None,
                'Hyundai_code': hyundai_code,
                'Name': row['Name'],
                'City': row['City'],
                'INN': row['INN'],
                'Manager_id': manager_id
            }

            if hyundai_code in existing_dealers:
                dealer_data['id'] = existing_dealers[hyundai_code]
                to_update.append(dealer_data)
            else:
                to_insert.append(dealer_data)

        try:
            if to_insert:
                db.bulk_insert_mappings(Hyundai_Dealer, to_insert)
            if to_update:
                db.bulk_update_mappings(Hyundai_Dealer, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            self.show_error_message(f"Ошибка сохранения Hyundai: {str(e)}")
        finally:
            db.close()

    @lru_cache(maxsize=32)
    def _get_id(self, model, name_field, name):
        """Получение ID по имени (с кэшированием)"""
        if not name or name in ('-', ''):
            return None

        item = db.query(model).filter(getattr(model, name_field) == name).first()
        return item.id if item else None

    def get_Customers_from_db(self):
        """Получение клиентов из базы с корректным отображением AM и TeamLead"""
        try:
            # Базовый запрос для получения информации о клиентах
            base_query = db.query(
                Cust_db.id,
                Cust_db.INN,
                Cust_db.Customer_name,
                Holding.Holding_name.label('Holding'),
                Sector.Sector_name.label('Sector'),
                Cust_db.Price_type
            ).join(Holding, Cust_db.Holding_id == Holding.id) \
            .join(Sector, Cust_db.Sector_id == Sector.id)
            
            # Получаем базовые данные о клиентах
            customers = pd.read_sql(base_query.statement, db.bind)
            
            if customers.empty:
                return customers
                
            # Отдельный запрос для получения менеджеров и тимлидов
            managers_query = db.query(
                Contract.Customer_id,
                Manager.Manager_name.label('AM'),
                TeamLead.TeamLead_name.label('TeamLead')
            ).join(Manager, Contract.Manager_id == Manager.id) \
            .outerjoin(TeamLead, Manager.TeamLead_id == TeamLead.id) \
            .filter(Contract.Customer_id.in_(customers['id'].tolist()))
            
            managers = pd.read_sql(managers_query.statement, db.bind)
            
            # Группируем менеджеров и тимлидов по клиентам
            if not managers.empty:
                grouped = managers.groupby('Customer_id').agg({
                    'AM': lambda x: ', '.join(set(filter(None, x))),
                    'TeamLead': lambda x: ', '.join(set(filter(None, x)))
                }).reset_index()
                
                # Объединяем с основными данными
                result = pd.merge(
                    customers,
                    grouped,
                    left_on='id',
                    right_on='Customer_id',
                    how='left'
                ).drop(columns=['Customer_id'])
            else:
                result = customers.copy()
                result['AM'] = None
                result['TeamLead'] = None
                
            return result.where(pd.notnull(result), None)
            
        except Exception as e:
            self.show_error_message(f"Ошибка при получении клиентов: {str(e)}")
            return pd.DataFrame()

    def get_Hyundai_from_db(self):
        """Получение дилеров Hyundai из базы"""
        query = db.query(
            Hyundai_Dealer.Dealer_code.label('HYUNDAI_id'),
            Hyundai_Dealer.Hyundai_code.label('Hyu_code'),
            Hyundai_Dealer.Name.label('Dealer_Name'),
            Hyundai_Dealer.INN,
            Manager.Manager_name.label('AM'),
            TeamLead.TeamLead_name.label('TeamLead')
        ).join(Manager, Hyundai_Dealer.Manager_id == Manager.id) \
         .join(TeamLead, Manager.TeamLead_id == TeamLead.id)

        df = pd.read_sql(query.statement, db.bind)
        df = df.drop_duplicates().where(pd.notnull(df), None)

        return df

    def find_Customer(self):
        """Поиск клиентов"""
        self.table.clearContents()
        self.table.setRowCount(0)

        cust_df = self.get_Customers_from_db()
        if cust_df.empty:
            self.show_error_message('Нет данных о клиентах')
            return

        cust_id = self.ui.line_ID.text().strip()
        cust_inn = self.ui.line_INN.text().strip()
        customer_name = self.ui.line_CustName.currentText()
        am = self.ui.line_AM.currentText()
        tl = self.ui.line_TL.currentText()

        # Фильтрация DataFrame
        if cust_id:
            cust_df = cust_df[cust_df['id'] == cust_id]
        elif cust_inn:
            cust_df = cust_df[cust_df['INN'] == cust_inn]
        elif customer_name != '-':
            cust_df = cust_df[cust_df['Customer_name'] == customer_name]
        elif am != '-':
            cust_df = cust_df[cust_df['AM'] == am]
        elif tl != '-':
            cust_df = cust_df[cust_df['TeamLead'] == tl]

        self._display_data(cust_df.sort_values('Customer_name'))

    def find_Hyundai(self):
        """Поиск дилеров Hyundai"""
        self.table.clearContents()
        self.table.setRowCount(0)

        dealer_df = self.get_Hyundai_from_db()
        if dealer_df.empty:
            self.show_error_message('Нет данных о дилерах')
            return

        dealer_id = self.ui.line_ID_Hyundai.text().strip()
        dealer_code = self.ui.line_Hyu_code.text().strip()
        dealer_name = self.ui.line_CustName_Hyundai.currentText()
        am = self.ui.line_AM_Hyundai.currentText()
        tl = self.ui.line_TL_Hyundai.currentText()

        if dealer_id:
            dealer_df = dealer_df[dealer_df['HYUNDAI_id'] == dealer_id]
        elif dealer_code:
            dealer_df = dealer_df[dealer_df['Hyu_code'] == dealer_code]
        elif dealer_name != '-':
            dealer_df = dealer_df[dealer_df['Dealer_Name'] == dealer_name]
        elif am != '-':
            dealer_df = dealer_df[dealer_df['AM'] == am]
        elif tl != '-':
            dealer_df = dealer_df[dealer_df['TeamLead'] == tl]

        self._display_data(dealer_df.sort_values('Dealer_Name'))

    def _display_data(self, df):
        """Метод отображения данных"""
        self.table.clear()
        self.table.setColumnCount(len(df.columns))
        
        if df.empty:
            self.show_error_message('Ничего не найдено')
            return
        
        df = df.fillna('')
        headers = df.columns.tolist()
        
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(df))
        
        for i in range(len(df)):
            for j, col in enumerate(headers):
                value = df.iloc[i][col]
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
        self._get_id.cache_clear()
        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_cust_list()
        self.fill_in_dealer_tl_list()
        self.fill_in_dealer_kam_list()
        self.fill_in_dealer_list()

    def fill_in_tl_list(self):
        """Заполнение списка тимлидов"""
        team_leads = db.query(TeamLead.TeamLead_name).distinct().all()
        self._fill_combobox(self.ui.line_TL, [tl[0] for tl in team_leads])
        self._fill_combobox(self.ui.line_TL_Hyundai, [tl[0] for tl in team_leads])

    def fill_in_kam_list(self):
        """Заполнение списка менеджеров"""
        tl = self.ui.line_TL.currentText()
        query = db.query(Manager.Manager_name)

        if tl != '-':
            query = query.join(TeamLead).filter(TeamLead.TeamLead_name == tl)

        kam_names = [kam[0] for kam in query.distinct().all()]
        self._fill_combobox(self.ui.line_AM, kam_names)

    def fill_in_cust_list(self):
        """Заполнение списка клиентов"""
        cust_df = self.get_Customers_from_db()
        if cust_df.empty:
            self.ui.line_CustName.clear()
            self.ui.line_CustName.addItem('-')
            return

        am = self.ui.line_AM.currentText()
        tl = self.ui.line_TL.currentText()

        if am != '-':
            cust_names = cust_df[cust_df['AM'] == am]['Customer_name'].unique()
        elif tl != '-':
            cust_names = cust_df[cust_df['TeamLead'] == tl]['Customer_name'].unique()
        else:
            cust_names = cust_df['Customer_name'].unique()

        self._fill_combobox(self.ui.line_CustName, sorted(cust_names))

    def fill_in_dealer_tl_list(self):
        """Заполнение списка тимлидов для дилеров"""
        try:
            # Получаем уникальных тимлидов, связанных с дилерами через менеджеров
            query = db.query(TeamLead.TeamLead_name).distinct() \
                    .join(Manager, Manager.TeamLead_id == TeamLead.id) \
                    .join(Hyundai_Dealer, Hyundai_Dealer.Manager_id == Manager.id)
            
            team_leads = [tl[0] for tl in query.all() if tl[0]]  # Фильтруем None
            self._fill_combobox(self.ui.line_TL_Hyundai, team_leads)
        except Exception as e:
            print(f"Ошибка при заполнении списка тимлидов для дилеров: {str(e)}")
            self._fill_combobox(self.ui.line_TL_Hyundai, [])

    def fill_in_dealer_kam_list(self):
        """Заполнение списка менеджеров для дилеров"""
        try:
            tl = self.ui.line_TL_Hyundai.currentText()
            query = db.query(Manager.Manager_name).distinct() \
                    .join(Hyundai_Dealer, Hyundai_Dealer.Manager_id == Manager.id)
            
            if tl != '-':
                query = query.join(TeamLead).filter(TeamLead.TeamLead_name == tl)
            
            kam_names = [kam[0] for kam in query.all() if kam[0]]  # Фильтруем None
            self._fill_combobox(self.ui.line_AM_Hyundai, kam_names)
        except Exception as e:
            print(f"Ошибка при заполнении списка менеджеров для дилеров: {str(e)}")
            self._fill_combobox(self.ui.line_AM_Hyundai, [])

    def fill_in_dealer_list(self):
        """Заполнение списка дилеров"""
        try:
            dealer_df = self.get_Hyundai_from_db()
            if dealer_df.empty:
                self.ui.line_CustName_Hyundai.clear()
                self.ui.line_CustName_Hyundai.addItem('-')
                return

            am = self.ui.line_AM_Hyundai.currentText()
            tl = self.ui.line_TL_Hyundai.currentText()

            # Фильтрация данных
            if am != '-':
                dealer_names = dealer_df[dealer_df['AM'] == am]['Dealer_Name'].dropna().unique()
            elif tl != '-':
                dealer_names = dealer_df[dealer_df['TeamLead'] == tl]['Dealer_Name'].dropna().unique()
            else:
                dealer_names = dealer_df['Dealer_Name'].dropna().unique()

            # Преобразование в список и фильтрация None
            dealer_names = [name for name in dealer_names if name and str(name).strip() != '']
            
            self._fill_combobox(self.ui.line_CustName_Hyundai, sorted(dealer_names))
        except Exception as e:
            print(f"Ошибка при заполнении списка дилеров: {str(e)}")
            self._fill_combobox(self.ui.line_CustName_Hyundai, [])

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
        
     
        
