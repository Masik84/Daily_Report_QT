import os
import pandas as pd
import numpy as np
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QApplication, 
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
        """Загрузка данных"""
        if self.current_upload_step == 0:
            self._upload_customer_data()
        else:
            self._upload_contract_data()

    def _upload_customer_data(self):
        """Загрузка данных Customer и Holding"""
        file_path = self.cust_file_path or Customer_file
        
        try:
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")
                
            try:
                self.run_customer_func(file_path, All_data_file)
                db.commit()
                self.show_message('Данные загружены!')
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()
                
        except Exception as e:
            self._handle_upload_error(e, "клиентов")

    def _upload_contract_data(self):
        """Загрузка данных Contract"""
        file_path = self.contract_file_path or Contract_file
        
        try:
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")
                
            try:
                self.run_contract_func(file_path)
                db.commit()
                self.show_message('Данные Contract загружены!')
                self.current_upload_step = 0
                self.cust_file_path = None
                self.contract_file_path = None
                self.ui.label_Cust_File.setText("Выбери файл или нажми Upload")
                self.refresh_all_comboboxes()
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()
                
        except Exception as e:
            self._handle_upload_error(e, "договоров")

    def _handle_upload_error(self, error, data_type):
        """Обработка ошибок загрузки"""
        if "transaction is already begun" in str(error):
            msg = "Ошибка БД. Закройте программу и попробуйте снова."
        elif "required columns" in str(error).lower():
            msg = "Файл не содержит всех необходимых столбцов."
        else:
            msg = f"Ошибка загрузки {data_type}: {str(error)}"
        self.show_error_message(msg)

    def run_customer_func(self, data_file_xls, all_data_file):
        """Основная функция обработки данных Customer и Holding"""
        data = self.read_customer_file(data_file_xls)
        self.save_Sector(data)
        self.save_Holding(data)
        self.save_Customer(data)
        data2 = self.read_HYUNDAI_file(all_data_file)
        self.save_HYUNDAI(data2)

    def run_contract_func(self, contract_file_xls):
        """Основная функция обработки данных Contract"""
        data = self.read_contract_file(contract_file_xls)
        self.save_Contract(data)

    def read_customer_file(self, cust_file_xls):
        """Чтение данных клиентов из Excel"""
        try:
            df = pd.read_excel(cust_file_xls, sheet_name=0, dtype={'ИНН': str})
            
            required_columns = ['Код', 'Наименование в программе', 'Холдинг']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит необходимых столбцов")
            
            column_map = {
                'ИНН': 'INN', 'Код': 'id', 
                'Наименование в программе': 'Customer_name',
                'Сектор': 'Sector', 'Тип цен': 'Price_type',
                'Холдинг': 'Holding'
            }
            
            df = df.rename(columns=column_map)[list(column_map.values())]
            df['Sector'] = df['Sector'].fillna("-")
            df["Holding"] = np.where(pd.isna(df["Holding"]) , df['Customer_name'],  df["Holding"])
            return df[df['id'] != 'n/a'].to_dict('records')
            
        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла клиентов: {str(e)}")
            return []

    def read_contract_file(self, contract_file_xls):
        """Чтение данных договоров из Excel"""
        try:
            df = pd.read_excel(contract_file_xls, sheet_name=0, dtype={'Код контрагента': str})
            
            required_columns = ['Код', 'Вид договора', 'Наименование', 'Условие оплаты']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Файл не содержит необходимых столбцов")
            
            column_map = {
                'Вид договора': 'Contract_Type', 'Код': 'id',
                'Менеджер': 'Manager_name', 'Наименование': 'Contract',
                'Тип цен': 'Price_Type', 'Условие оплаты': 'Payment_Condition',
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
        """Сохранение договоров с обновлением существующих"""
        if not data:
            return

        existing_contracts = {c.id: c for c in db.query(Contract).all()}
        to_insert = []
        to_update = []
        
        for row in data:
            contract_id = row['id']
            manager_id = self._get_id(Manager, 'Manager_name', row['Manager_name'])
            if not manager_id:
                continue
                
            contract_data = {
                'id': contract_id,
                'Contract': row['Contract'],
                'Contract_Type': row['Contract_Type'],
                'Price_Type': row['Price_Type'],
                'Payment_Condition': row['Payment_Condition'],
                'Customer_id': row['Customer_id'],
                'Manager_id': manager_id
            }
            
            if contract_id in existing_contracts:
                to_update.append(contract_data)
            else:
                to_insert.append(contract_data)
        
        try:
            if to_insert:
                db.bulk_insert_mappings(Contract, to_insert)
            if to_update:
                db.bulk_update_mappings(Contract, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            self.show_error_message(f"Ошибка сохранения договоров: {str(e)}")
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
        """Получение клиентов из базы"""
        query = db.query(
            Cust_db.id,
            Cust_db.INN,
            Cust_db.Customer_name,
            Holding.Holding_name.label('Holding'),
            Sector.Sector_name.label('Sector'),
            Cust_db.Price_type,
            Manager.Manager_name.label('AM'),
            TeamLead.TeamLead_name.label('TeamLead')
        ).join(Holding, Cust_db.Holding_id == Holding.id)\
         .join(Sector, Cust_db.Sector_id == Sector.id)\
         .outerjoin(Contract, Cust_db.id == Contract.Customer_id)\
         .outerjoin(Manager, Contract.Manager_id == Manager.id)\
         .outerjoin(TeamLead, Manager.TeamLead_id == TeamLead.id)
        
        df = pd.read_sql(query.statement, db.bind)
        return df.drop_duplicates().where(pd.notnull(df), None)

    def get_Hyundai_from_db(self):
        """Получение дилеров Hyundai из базы"""
        query = db.query(
            Hyundai_Dealer.Dealer_code.label('HYUNDAI_id'),
            Hyundai_Dealer.Hyundai_code.label('Hyu_code'),
            Hyundai_Dealer.Name.label('Dealer_Name'),
            Hyundai_Dealer.INN,
            Manager.Manager_name.label('AM'),
            TeamLead.TeamLead_name.label('TeamLead')
        ).join(Manager, Hyundai_Dealer.Manager_id == Manager.id)\
         .join(TeamLead, Manager.TeamLead_id == TeamLead.id)
        
        df = pd.read_sql(query.statement, db.bind)
        return df.where(pd.notnull(df), None)

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
        """Отображение данных в таблице"""
        if df.empty:
            self.show_error_message('Ничего не найдено')
            return
            
        headers = df.columns.tolist()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
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
        query = db.query(TeamLead.TeamLead_name)\
                 .join(Manager)\
                 .join(Hyundai_Dealer)\
                 .distinct()
        team_leads = [tl[0] for tl in query.all()]
        self._fill_combobox(self.ui.line_TL_Hyundai, team_leads)

    def fill_in_dealer_kam_list(self):
        """Заполнение списка менеджеров для дилеров"""
        tl = self.ui.line_TL_Hyundai.currentText()
        query = db.query(Manager.Manager_name)\
                 .join(Hyundai_Dealer)\
                 .join(TeamLead)
        
        if tl != '-':
            query = query.filter(TeamLead.TeamLead_name == tl)
            
        kam_names = [kam[0] for kam in query.distinct().all()]
        self._fill_combobox(self.ui.line_AM_Hyundai, kam_names)
        
    def fill_in_dealer_list(self):
        """Заполнение списка дилеров"""
        dealer_df = self.get_Hyundai_from_db()
        if dealer_df.empty:
            self.ui.line_CustName_Hyundai.clear()
            self.ui.line_CustName_Hyundai.addItem('-')
            return
            
        am = self.ui.line_AM_Hyundai.currentText()
        tl = self.ui.line_TL_Hyundai.currentText()
        
        if am != '-':
            dealer_names = dealer_df[dealer_df['AM'] == am]['Dealer_Name'].unique()
        elif tl != '-':
            dealer_names = dealer_df[dealer_df['TeamLead'] == tl]['Dealer_Name'].unique()
        else:
            dealer_names = dealer_df['Dealer_Name'].unique()
        
        self._fill_combobox(self.ui.line_CustName_Hyundai, sorted(dealer_names))

    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if items:
            combobox.addItems(sorted(items))

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
        
        # Добавляем кнопку "Copy msg" (не закрывает окно)
        copy_button = msg.addButton("Copy msg", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        
        # Основная кнопка OK
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        
        # Отключаем закрытие окна при нажатии на "Copy msg"
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
        
        # Добавляем кнопку "Copy msg" (не закрывает окно)
        copy_button = msg.addButton("Copy msg", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        
        # Основная кнопка OK
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        
        # Отключаем закрытие окна при нажатии на "Copy msg"
        copy_button.clicked.connect(lambda: None)
        
        msg.exec_()


