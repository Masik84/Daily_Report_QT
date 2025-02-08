import pandas as pd
import polars as pl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget
from sqlalchemy.exc import SQLAlchemyError

from db import db, engine
from models import Manager, TeamLead, Customer as Cust_db, Sector, Holding, Manager_Prev, HYUNDAI
from wind.pages.customers_ui import Ui_Form

from config import All_data_file


class Customer(QWidget):
    def __init__(self):
        super(Customer, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.table = self.ui.table
        self.ui.table.resizeColumnsToContents()

        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_cust_list()
        
        self.fill_in_dealer_tl_list()
        self.fill_in_dealer_kam_list()
        self.fill_in_dealer_list()
                   
        self.ui.line_TL.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.line_AM.currentTextChanged.connect(self.fill_in_cust_list)

        self.ui.line_TL_Hyundai.currentTextChanged.connect(self.fill_in_dealer_kam_list)
        self.ui.line_AM_Hyundai.currentTextChanged.connect(self.fill_in_dealer_list)
                
        self.ui.btn_find_cust.clicked.connect(self.find_Customer)
        self.ui.btn_find_Hyundai.clicked.connect(self.find_Hyundai)
        
        self.ui.btn_open_file.setToolTip('выбери файл ! ALL DATA !.xlsx')
        self.ui.btn_open_file.clicked.connect(self.get_cust_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_cust_data)
        
        # self.ui.btn_download.clicked.connect(self.dowload_Customer)


    def get_cust_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_Cust_File.setText(get_file[0])
            

    def upload_cust_data(self, cust_file_xls):
        cust_file_xls = self.ui.label_Cust_File.text()

        if cust_file_xls == 'Выбери файл или нажми Upload, файл будет взят из основной папки' \
            or cust_file_xls == 'База данных обновлена!'\
            or cust_file_xls == '':
            self.run_customer_func(All_data_file)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else:
            self.run_customer_func(cust_file_xls)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            
        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_cust_list()
        
        self.fill_in_dealer_tl_list()
        self.fill_in_dealer_kam_list()
        self.fill_in_dealer_list()
        
        self.ui.label_Cust_File.setText("Выбери файл или нажми Upload, файл будет взят из основной папки")
    
    
    def run_customer_func(self, data_file_xls):
        data = self.read_customer_file(data_file_xls)
        self.save_Sector(data)
        self.save_Holding(data)
        self.save_Customer(data)
        
        data2 = self.read_HYUNDAI_file(data_file_xls)
        self.save_HYUNDAI(data2)


    def read_customer_file(self, cust_file_xls):
        dict_types_cust = {'Контрагент.ИНН': pl.String}
        df = pl.read_excel(cust_file_xls, sheet_name='Customers', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float", "date"]}, schema_overrides = dict_types_cust)
        df = df.filter(pl.col('Контрагент.Код') != 'n/a')
        df = df.rename({'Контрагент.Код': 'id',
                                    'Контрагент': 'Customer_Name',
                                    'Контрагент.ИНН': 'INN',
                                    'ХОЛДИНГ': 'Holding',
                                    'SECTOR': 'Sector',
                                    'Менеджер': 'AM',
                                    'Менеджер_prev': 'AM_prev',
                                    'Статус клиента': 'Status',
                                    'Прайс-лист': 'PriceList',
                                    'Доставка': 'Delivery',
                                    'Team Lead': 'TeamLead' })
        df = df.with_columns(pl.col('AM_prev').fill_null("-"),)
        cust_data = df.to_dicts()
        
        return cust_data


    def save_Holding(self, data):
        processed = []
        holding_unique = []
        for row in data:
            if row['Holding'] not in processed:
                holding = {'Holding': row['Holding'],
                                    "AM_id": self.get_id_AM(row['AM']),
                                    'AM_prev_id': self.get_id_AM_prev(row['AM_prev']),
                                    'Sector_id': self.get_id_Sector(row['Sector']),
                                    }
                holding_unique.append(holding)
                processed.append(holding['Holding'])

        holding_for_upload = []
        holding_for_update = []
        for mylist in holding_unique:
            holding_exists = Holding.query.filter(Holding.Holding == mylist['Holding']).count()
            if holding_exists == 0:
                new_holding = {'Holding': mylist['Holding'],
                                            'AM_id': mylist['AM_id'],
                                            'AM_prev_id': mylist["AM_prev_id"],
                                            'Sector_id': mylist['Sector_id'],
                                            }
                holding_for_upload.append(new_holding)

            elif holding_exists >0:
                new_holding = {'id': self.get_id_Holding(mylist['Holding']), 
                                            'Holding': mylist['Holding'],
                                            'AM_id': mylist['AM_id'],
                                            'AM_prev_id': mylist["AM_prev_id"],
                                            'Sector_id': mylist['Sector_id'],
                                            }
                holding_for_update.append(new_holding)

        db.bulk_insert_mappings(Holding, holding_for_upload)
        db.bulk_update_mappings(Holding, holding_for_update)
        
        try:
            db.commit()
        except SQLAlchemyError as e:
            print_error(mylist, "Ошибка целостности данных: {}", e)
            db.rollback()
            raise
        except ValueError as e:
            print_error(mylist, "Неправильный формат данных: {}", e)
            db.rollback()
            raise
        return holding_unique


    def get_id_Holding(self, holding):
        db_data = Holding.query.filter(Holding.Holding == holding).first()
        holding_id = db_data.id
        return holding_id


    def save_Sector(self, data):
        processed = []
        sector_unique = []
        for row in data:
            if row['Sector'] not in processed:
                sector = {'Sector': row['Sector']}
                sector_unique.append(sector)
                processed.append(sector['Sector'])

        sector_for_upload = []
        sector_for_update = []
        for mylist in sector_unique:
            sector_exists = Sector.query.filter(Sector.Sector == mylist['Sector']).count()
            if sector_exists == 0:
                new_sector = {'Sector': mylist['Sector']}
                sector_for_upload.append(new_sector)
            elif sector_exists > 0:
                new_sector = {'id': self.get_id_Sector(mylist['Sector']), 'Sector': mylist['Sector']}
                sector_for_update.append(new_sector)

        db.bulk_insert_mappings(Sector, sector_for_upload)
        db.bulk_update_mappings(Sector, sector_for_update)
        
        try:
            db.commit()
        except SQLAlchemyError as e:
            print_error(mylist, "Ошибка целостности данных: {}", e)
            db.rollback()
            raise
        except ValueError as e:
            print_error(mylist, "Неправильный формат данных: {}", e)
            db.rollback()
            raise
        return sector_unique


    def get_id_Sector(self, sector):
        db_data = Sector.query.filter(Sector.Sector == sector).first()
        sector_id = db_data.id

        return sector_id


    def get_id_AM(self, AM_name):
        db_data = Manager.query.filter(Manager.AM == AM_name).first()
        if not db_data:
            self.lbl_message.configure(text = f"Не найден {AM_name} в Базе", bootstyle="danger")
            return
        else:
            return db_data.id
                  

    def get_id_AM_prev(self, AM_name):
        db_data = Manager_Prev.query.filter(Manager_Prev.AM_prev == AM_name).first()
        am_prev_id = db_data.id

        return am_prev_id


    def save_Customer(self, data):
        processed = []
        cust_unique = []

        for row in data:
            if row['id'] not in processed:
                cust = {'id': row['id'],
                            'Customer_Name': row['Customer_Name'],
                            'INN': str(row['INN']),
                            'Holding': row['Holding'],
                            'Status': row['Status'],
                            'PriceList': row['PriceList'],
                            'Delivery': row['Delivery'],
                            }
                cust_unique.append(cust)
                processed.append(row['id'])

        cust_for_upload = []
        cust_for_update = []
        for mylist in cust_unique:
            cust_exists = Cust_db.query.filter(Cust_db.id == mylist['id']).count()
            if cust_exists == 0 or cust_exists is None:
                new_cust = {'id': mylist['id'],
                                    'Customer_Name': mylist['Customer_Name'],
                                    'INN': str(mylist['INN']),
                                    'Holding_id': self.get_id_Holding(mylist['Holding']),
                                    'Status': mylist['Status'],
                                    'PriceList': mylist['PriceList'],
                                    'Delivery': mylist['Delivery'], 
                                    }
                cust_for_upload.append(new_cust)
            elif cust_exists > 0:
                new_cust = {'id': mylist['id'],
                                    'Customer_Name': mylist['Customer_Name'],
                                    'INN': str(mylist['INN']),
                                    'Holding_id': self.get_id_Holding(mylist['Holding']),
                                    'Status': mylist['Status'],
                                    'PriceList': mylist['PriceList'],
                                    'Delivery': mylist['Delivery'], 
                                    }
                cust_for_update.append(new_cust)
        db.bulk_insert_mappings(Cust_db, cust_for_upload)
        db.bulk_update_mappings(Cust_db, cust_for_update)
        
        try:
            db.commit()
        except SQLAlchemyError as e:
            print_error(mylist, "Ошибка целостности данных: {}", e)
            db.rollback()
            raise
        except ValueError as e:
            print_error(mylist, "Неправильный формат данных: {}", e)
            db.rollback()
            raise

        return cust_unique


    def read_HYUNDAI_file(self, cust_file_xls):
        dict_types_cust = {'ИНН': pl.String}
        df = pl.read_excel(cust_file_xls, sheet_name='HYUNDAI', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float", "date"]}, schema_overrides = dict_types_cust)
        df = df.filter(pl.col('Код дилера HYUNDAI') != '-')
        df = df.rename({'Код дилера HYUNDAI': 'HYUNDAI_id',
                                    'Код в HYUNDAI': 'Hyu_code',
                                    'Наим дилера HYUNDAI': 'Dealer_Name',
                                    'Город': 'City',
                                    'ИНН': 'INN', })
        df = df.with_columns(pl.col('HYUNDAI_id').fill_null("-"),)
        df = df.filter(pl.col('HYUNDAI_id') != '-')
        HYUNDAI_data = df.to_dicts()
        
        return HYUNDAI_data
    
    
    def save_HYUNDAI(self, data):
        processed = []
        hyundai_unique = []
        for row in data:
            if row['HYUNDAI_id'] not in processed:
                hyundai = {"HYUNDAI_id": row["HYUNDAI_id"],
                                    "Hyu_code": row["Hyu_code"],
                                    "Dealer_Name": row["Dealer_Name"],
                                    "City": row["City"],
                                    "INN": row["INN"],
                                    "AM_id": self.get_id_AM(row['SALES'])
                                    }
                hyundai_unique.append(hyundai)
                processed.append(hyundai['HYUNDAI_id'])

        hyundai_for_upload = []
        hyundai_for_update = []
        for mylist in hyundai_unique:
            hyundai_exists = HYUNDAI.query.filter(HYUNDAI.HYUNDAI_id == mylist['HYUNDAI_id']).count()
            if hyundai_exists == 0:
                new_hyundai = {"HYUNDAI_id": mylist["HYUNDAI_id"],
                                            "Hyu_code": mylist["Hyu_code"],
                                            "Dealer_Name": mylist["Dealer_Name"],
                                            "City": mylist["City"],
                                            "INN": mylist["INN"],
                                            "AM_id": mylist["AM_id"]
                                            }
                hyundai_for_upload.append(new_hyundai)
            elif hyundai_exists > 0:
                new_hyundai = {'id': self.get_id_HYUNDAI(mylist['HYUNDAI_id']), 
                                            "HYUNDAI_id": mylist["HYUNDAI_id"],
                                            "Hyu_code": mylist["Hyu_code"],
                                            "Dealer_Name": mylist["Dealer_Name"],
                                            "City": mylist["City"],
                                            "INN": mylist["INN"],
                                            "AM_id": mylist["AM_id"]
                                            }
                hyundai_for_update.append(new_hyundai)

        db.bulk_insert_mappings(HYUNDAI, hyundai_for_upload)
        db.bulk_update_mappings(HYUNDAI, hyundai_for_update)
        
        try:
            db.commit()
        except SQLAlchemyError as e:
            print_error(mylist, "Ошибка целостности данных: {}", e)
            db.rollback()
            raise
        except ValueError as e:
            print_error(mylist, "Неправильный формат данных: {}", e)
            db.rollback()
            raise

        return hyundai_unique
    
    
    def get_id_HYUNDAI(self, HYUNDAI_id):
        db_data = HYUNDAI.query.filter(HYUNDAI.HYUNDAI_id == HYUNDAI_id).first()
        hyu_id = db_data.id

        return hyu_id


    def get_Customers_from_db(self):
        cust_reques = db.query(Cust_db,)
        cust_data_db = pl.read_database(query=cust_reques.statement, connection=engine)
        
        if cust_data_db.is_empty() == False:
            holding_request= db.query(Holding, Sector).join(Sector)
            holding_data_db = pl.read_database(query=holding_request.statement, connection=engine)
        
            kam_request = db.query(Manager, TeamLead).join(TeamLead)
            kam_data_db = pl.read_database(query=kam_request.statement, connection=engine)

            cust_data_db = cust_data_db.join(holding_data_db, how="left", left_on="Holding_id", right_on="id")
            cust_data_db = cust_data_db.join(kam_data_db, how="left", left_on="AM_id", right_on="id")
            cust_data_db = cust_data_db[["id", "INN", "Customer_Name", "Holding", "Sector", "AM", "TeamLead", "PriceList", "Delivery"]]
            cust_data_db = cust_data_db.sort("Customer_Name", descending=False)      
        
        else:
            cust_data_db = pl.DataFrame()
        
        return cust_data_db


    def get_Hyundai_from_db(self):
        hyundai_reques = db.query(HYUNDAI)
        hyundai_data_db = pl.read_database(query=hyundai_reques.statement, connection=engine)
        
        if hyundai_data_db.is_empty() == False:
                kam_request = db.query(Manager, TeamLead).join(TeamLead)
                kam_data_db = pl.read_database(query=kam_request.statement, connection=engine)

                hyundai_data_db = hyundai_data_db.join(kam_data_db, how="left", left_on="AM_id", right_on="id")
                hyundai_data_db = hyundai_data_db[["HYUNDAI_id", "Hyu_code", "Dealer_Name", "INN", "AM", "TeamLead", ]]
                hyundai_data_db = hyundai_data_db.sort("Dealer_Name", descending=False)      
        else:
            hyundai_data_db = pl.DataFrame()
        
        return hyundai_data_db
  
    
    def find_Customer(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        cust_df = self.get_Customers_from_db()
        
        cust_id = self.ui.line_ID.text()
        cust_inn = self.ui.line_INN.text()
        Customer_Name = self.ui.line_CustName.currentText()
        AM = self.ui.line_AM.currentText()
        STL = self.ui.line_TL.currentText()

        if cust_df.is_empty() == True:
            msg = QMessageBox()
            msg.setText('There is no Customer data in Database\n'
                                'Close the program and open agan!\n'
                                'Then update Database')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            
        elif cust_id != '':
            cust_df = cust_df.filter(pl.col("id") == cust_id).sort("Customer_Name", descending=[False])

        elif cust_inn != '':
            cust_df = cust_df.filter(pl.col("INN") == cust_inn).sort("Customer_Name", descending=[False])
            
        elif Customer_Name != '-':
            cust_df = cust_df.filter(pl.col("Customer_Name") == Customer_Name).sort("Customer_Name", descending=[False])

        elif AM != '-' :
            cust_df = cust_df.filter(pl.col("AM") == AM).sort("Customer_Name", descending=[False])

        elif STL != '-':
            cust_df = cust_df.filter(pl.col("STL") == STL).sort("Customer_Name", descending=[False])
        
        else:
            cust_df = cust_df.sort("Customer_Name", descending=[False])

        cust_df = cust_df.to_pandas()
        headers = cust_df.columns.values.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        for i, row in cust_df.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)
            
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(cust_df.iloc[i, j])))
        

    def find_Hyundai(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        dealer_df = self.get_Hyundai_from_db()
        
        dealer_id = self.ui.line_ID_Hyundai.text()
        dealer_code = self.ui.line_Hyu_code.text()
        dealer_name = self.ui.line_CustName_Hyundai.currentText()
        AM = self.ui.line_AM_Hyundai.currentText()
        TL = self.ui.line_TL_Hyundai.currentText()

        if dealer_df.is_empty() == True:
            msg = QMessageBox()
            msg.setText('There is no Customer data in Database\n'
                                'Close the program and open agan!\n'
                                'Then update Database')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            
        elif dealer_id != '':
            dealer_df = dealer_df.filter(pl.col("HYUNDAI_id") == dealer_id).sort("Dealer_Name", descending=[False])

        elif dealer_code != '':
            dealer_df = dealer_df.filter(pl.col("Hyu_code") == dealer_code).sort("Dealer_Name", descending=[False])
            
        elif dealer_name != '-':
            dealer_df = dealer_df.filter(pl.col("Dealer_Name") == dealer_name).sort("Dealer_Name", descending=[False])

        elif AM != '-' :
            dealer_df = dealer_df.filter(pl.col("AM") == AM).sort("Dealer_Name", descending=[False])

        elif TL != '-':
            dealer_df = dealer_df.filter(pl.col("TeamLead") == TL).sort("Dealer_Name", descending=[False])
        
        else:
            dealer_df = dealer_df.sort("Dealer_Name", descending=[False])

        dealer_df = dealer_df.to_pandas()
        headers = dealer_df.columns.values.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        for i, row in dealer_df.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)
            
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(dealer_df.iloc[i, j])))
    
    
    def get_all_kam_from_db(self):
        KAM_request = db.query(Manager, TeamLead).join(TeamLead)
        KAM_data = pl.read_database(query=KAM_request.statement, connection=engine)
        if KAM_data.is_empty() == False:
            all_KAM_data = KAM_data[['AM', 'TeamLead', ]]
            all_KAM_data = all_KAM_data.sort("AM", descending=[False])
        else:
            all_KAM_data = pl.DataFrame()
            
        return all_KAM_data

    
    def fill_in_cust_list(self):
        cust_df = self.get_Customers_from_db()
        
        self.ui.line_CustName.clear()
        
        am = self.ui.line_AM.currentText()
        tl = self.ui.line_TL.currentText()
        
        if cust_df.is_empty() == True:
            self.ui.line_CustName.addItem('-')
                
        elif am != '-':
            cust_name = cust_df[['AM', 'Customer_Name']]
            cust_name = cust_name.filter(pl.col("AM") == am)
            cust_name = cust_name.unique(subset="Customer_Name").sort("Customer_Name", descending=[False,])
            cust_name_list = cust_name['Customer_Name'].to_list()
            cust_name_list.insert(0, '-')
            self.ui.line_CustName.addItems(cust_name_list)

        elif tl !='-':
            cust_name = cust_df[['TeamLead', 'Customer_Name']]
            cust_name = cust_name.filter(pl.col("TeamLead") == tl)
            cust_name = cust_name.unique(subset="Customer_Name").sort("Customer_Name", descending=[False,])
            cust_name_list = cust_name['Customer_Name'].to_list()
            cust_name_list.insert(0, '-')
            self.ui.line_CustName.addItems(cust_name_list)
            
        else:
            cust_name = cust_df[['Customer_Name']]
            cust_name = cust_name.unique(subset="Customer_Name").sort("Customer_Name", descending=[False,])
            cust_name_list = cust_name['Customer_Name'].to_list()
            cust_name_list.insert(0, '-')
            self.ui.line_CustName.addItems(cust_name_list)


    def fill_in_kam_list(self):
        KAM_data = self.get_all_kam_from_db()
        
        self.ui.line_AM.clear()

        if KAM_data.is_empty() == True:
            self.ui.line_AM.addItem('-')

        else:
            KAM_data = KAM_data[['AM']]
            KAM_data = KAM_data.unique(subset="AM").sort("AM", descending=[False,])
            KAM_list = KAM_data['AM'].to_list()
            self.ui.line_AM.addItems(KAM_list)

            
    def fill_in_tl_list(self):
        TL_data = self.get_all_kam_from_db()

        self.ui.line_TL.clear()

        if TL_data.is_empty() == True:
            self.ui.line_TL.addItem('-')

        else:
            TL_data = TL_data[['TeamLead']]
            TL_data = TL_data.unique(subset="TeamLead").sort("TeamLead", descending=[False,])
            TL_list = TL_data['TeamLead'].to_list()
            self.ui.line_TL.addItems(TL_list)


    def fill_in_dealer_list(self):
        dealer_df = self.get_Hyundai_from_db()
        
        self.ui.line_CustName_Hyundai.clear()
        
        am = self.ui.line_AM_Hyundai.currentText()
        tl = self.ui.line_TL_Hyundai.currentText()
        
        if dealer_df.is_empty() == True:
            self.ui.line_CustName_Hyundai.addItem('-')
                
        elif am != '-':
            dealer_name = dealer_df[['AM', 'Dealer_Name']]
            dealer_name = dealer_name.filter(pl.col("AM") == am)
            dealer_name = dealer_name.unique(subset="Dealer_Name").sort("Dealer_Name", descending=[False,])
            dealer_name_list = dealer_name['Dealer_Name'].to_list()
            dealer_name_list.insert(0, '-')
            self.ui.line_CustName_Hyundai.addItems(dealer_name_list)

        elif tl !='-':
            dealer_name = dealer_df[['TeamLead', 'Dealer_Name']]
            dealer_name = dealer_name.filter(pl.col("TeamLead") == tl)
            dealer_name = dealer_name.unique(subset="Dealer_Name").sort("Dealer_Name", descending=[False,])
            dealer_name_list = dealer_name['Dealer_Name'].to_list()
            dealer_name_list.insert(0, '-')
            self.ui.line_CustName_Hyundai.addItems(dealer_name_list)
            
        else:
            dealer_name = dealer_df[['Dealer_Name']]
            dealer_name = dealer_name.unique(subset="Dealer_Name").sort("Dealer_Name", descending=[False,])
            dealer_name_list = dealer_name['Dealer_Name'].to_list()
            dealer_name_list.insert(0, '-')
            self.ui.line_CustName_Hyundai.addItems(dealer_name_list)


    def fill_in_dealer_kam_list(self):
        KAM_data = self.get_Hyundai_from_db()
        
        self.ui.line_AM_Hyundai.clear()

        if KAM_data.is_empty() == True:
            self.ui.line_AM_Hyundai.addItem('-')

        else:
            KAM_data = KAM_data[['AM']]
            KAM_data = KAM_data.unique(subset="AM").sort("AM", descending=[False,])
            KAM_list = KAM_data['AM'].to_list()
            KAM_list.insert(0, '-')
            self.ui.line_AM_Hyundai.addItems(KAM_list)

            
    def fill_in_dealer_tl_list(self):
        TL_data = self.get_Hyundai_from_db()
        
        self.ui.line_TL_Hyundai.clear()

        if TL_data.is_empty() == True:
            self.ui.line_TL_Hyundai.addItem('-')

        else:
            TL_data = TL_data[['TeamLead']]
            TL_data = TL_data.unique(subset="TeamLead").sort("TeamLead", descending=[False,])
            TL_list = TL_data['TeamLead'].to_list()
            TL_list.insert(0, '-')
            self.ui.line_TL_Hyundai.addItems(TL_list)


    # def dowload_Customer(self):
    #     savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Customers.xlsx', 'Excel Workbook (*.xlsx)')
    #     col_count = self.ui.table.columnCount()
    #     row_count = self.ui.table.rowCount()
    #     headers = [str(self.ui.table.horizontalHeaderItem(i).text()) for i in range(col_count)]

    #     df_list = []
    #     for row in range(row_count):
    #         df_list2 = []
    #         for col in range(col_count):
    #             table_item = self.ui.table.item(row,col)
    #             df_list2.append('' if table_item is None else str(table_item.text()))
    #         df_list.append(df_list2)

    #     df = pd.DataFrame(df_list, columns=headers)
    #     df.to_excel(savePath[0], index=False)

    #     msg = QMessageBox()
    #     msg.setText('Report was saved successfully')
    #     msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                     "font: 12pt  \"Segoe UI\";"
    #                     "color: #4b0082;\n"
    #                     " ")
    #     msg.setIcon(QMessageBox.Information)
    #     x = msg.exec_()
        
        
    def error_msg(self):
        msg = QMessageBox()
        msg.setText('There is no Customer data in Database\n'
                            'Close the program and open agan!\n'
                            'Then update Database')
        msg.setStyleSheet("background-color: #f8f8f2;\n"
                        "font: 10pt  \"Tahoma\";"
                        "color: #ff0000;\n"
                        " ")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

        

