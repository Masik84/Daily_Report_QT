import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db, engine
# from models import Base_PL, Brands, PL_chng, Packs, Products
from wind.pages.base_price_ui import Ui_Form


class BasePL(QWidget):
    def __init__(self):
        super(BasePL, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.fill_in_pl_type()        
        # self.fill_in_prod_list()
        # self.fill_in_chng_date_list()
        
        # self.ui.line_brand.currentTextChanged.connect(self.fill_in_prod_list)
        # self.ui.line_prod_name.currentTextChanged.connect(self.fill_in_chng_date_list)
        # self.ui.line_PL_type.currentTextChanged.connect(self.fill_in_chng_date_list)

        self.table = self.ui.table
        self.ui.table.resizeColumnsToContents()

        self.ui.btn_open_file.setToolTip('выбери файл ! ALL DATA !.xlsx')
        # self.ui.btn_open_file.clicked.connect(self.get_file)
        # self.ui.btn_upload_file.clicked.connect(self.upload_data)
        # self.ui.btn_find.clicked.connect(self.find_Prices)
        # self.ui.btn_download.clicked.connect(self.dowload_Prices)


    def get_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_Price_File.setText(get_file[0])
            

    def upload_data(self, PL_file_xls):
        PL_file_xls = self.ui.label_Price_File.text()
        if PL_file_xls == 'File Path' or PL_file_xls == 'Database was updated successfully':
            msg = QMessageBox()
            msg.setWindowTitle('Programm Error')
            msg.setText('!!! Please choose the file with Base Prices !!!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 12pt  \"Segoe UI\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            chng_data = self.read_pl_chng_file(PL_file_xls)
            self.update_pl_chng_data(chng_data)

            price_data = self.read_base_pl_file(PL_file_xls)
            self.update_base_pl_data(price_data)
            msg = QMessageBox()
            msg.setText('Database was updated successfully')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Segoe UI\";"
                            "color: #4b0082;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            
            self.fill_in_chng_date_list()
            self.fill_in_prod_list()
        
            self.ui.label_Price_File.setText('File Path')


    # def read_pl_chng_file(self, PL_file_xls):
    #     pl_change_df = pd.read_excel(PL_file_xls, sheet_name='PL_Changes')
    #     pl_change_df = pl_change_df[['Date', 'chng_Dealers', 'chng_AZS']]
    #     pl_change_df['Date'] = pd.to_datetime(pl_change_df['Date'])

    #     chng_data = pl_change_df.to_dict('records')

    #     return chng_data


    # def read_base_pl_file(self, PL_file_xls):
    #     base_pl_df = pd.read_excel(PL_file_xls, sheet_name='PL_list')
    #     base_pl_df['KSSS_prod'] = base_pl_df['KSSS_prod'].astype(int)
    #     base_pl_df['Date'] = pd.to_datetime(base_pl_df['Date'])
    #     price_data = base_pl_df.to_dict('records')

    #     return price_data


    # def update_pl_chng_data(self, data):
    #     chng_for_create = []
    #     chng_for_update = []
    #     for row in data:
    #         chng_exists = PL_chng.query.filter(PL_chng.Date == row['Date']).count()
    #         if chng_exists == 0:
    #             chng_list = {'Date' : row['Date'], 
    #                                 'chng_Dealers' : row['chng_Dealers'],
    #                                 'chng_AZS' : row['chng_AZS']}
    #             chng_for_create.append(chng_list)

    #         elif chng_exists > 0:
    #             chng_list = {'id' : self.get_id_PL_chng(row['Date']),
    #                                 'Date' : row['Date'], 
    #                                 'chng_Dealers' : row['chng_Dealers'],
    #                                 'chng_AZS' : row['chng_AZS']}
    #             chng_for_update.append(chng_list)
                
    #     db.bulk_insert_mappings(PL_chng, chng_for_create)
    #     db.bulk_update_mappings(PL_chng, chng_for_update)

    #     try:
    #         db.commit()
    #     except SQLAlchemyError as e:
    #         print_error(row, "Ошибка целостности данных: {}", e)
    #         db.rollback()
    #         raise
    #     except ValueError as e:
    #         print_error(row, "Неправильный формат данных: {}", e)
    #         db.rollback()
    #         raise
    #     return chng_for_create


    # def update_base_pl_data(self, data):
    #     base_pl_for_create = []
    #     base_pl_for_update = []
    #     for row in data:
    #         base_pl_exists = Base_PL.query.filter(Base_PL.merge == str(row['merge'])).count()
    #         if base_pl_exists == 0:
    #             base_pl_list = {'merge' : row['merge'],
    #                                     'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                     'PL_type' : row['PL_type'],
    #                                     'Date' : row['Date'],
    #                                     'Price' : row['Price'],
    #                                     'Change' : row['Change']}
    #             base_pl_for_create.append(base_pl_list)

    #         elif base_pl_exists > 0:
    #             base_pl_list = {'id' : self.get_id_base_PL_data(str(row['merge'])),
    #                                     'merge' : row['merge'],
    #                                     'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                     'PL_type' : row['PL_type'],
    #                                     'Date' : row['Date'],
    #                                     'Price' : row['Price'],
    #                                     'Change' : row['Change']}
    #             base_pl_for_update.append(base_pl_list)
                
    #     db.bulk_insert_mappings(Base_PL, base_pl_for_create)
    #     db.bulk_update_mappings(Base_PL, base_pl_for_update)

    #     try:
    #         db.commit()
    #     except SQLAlchemyError as e:
    #         print_error(row, "Ошибка целостности данных: {}", e)
    #         db.rollback()
    #         raise
    #     except ValueError as e:
    #         print_error(row, "Неправильный формат данных: {}", e)
    #         db.rollback()
    #         raise
    #     return base_pl_for_create


    # def get_id_PL_chng(self, date):
    #     db_data = PL_chng.query.filter(PL_chng.Date == date).first()
    #     pl_chnge_id = db_data.id
            
    #     return pl_chnge_id


    # def get_id_Product(self, KSSS_prod):
    #     if KSSS_prod != 'nan':
    #         db_data = Products.query.filter(Products.KSSS_prod == KSSS_prod).first()
    #         product_id = db_data.id
    #     else:
    #         product_id = None

    #     return product_id


    # def get_id_base_PL_data(self, merge):
    #     if merge != 'nan':
    #         db_data = Base_PL.query.filter(Base_PL.merge == merge).first()
    #         base_pl_id = db_data.id
    #     else:
    #         base_pl_id = None
    #     return base_pl_id


    # def find_Prices(self):
    #     price_data = self.get_all_prices_from_db()
        
    #     KSSS_prod = self.ui.line_KSSS.text()
    #     Product_Name = self.ui.line_prod_name.currentText()
    #     PL_type = self.ui.line_PL_type.currentText()
    #     Date = self.ui.line_date.currentText()
    #     Brand = self.ui.line_brand.currentText()

    #     if price_data.empty == True:
    #         msg = QMessageBox()
    #         msg.setText('There is no Price data in Database\n'
    #                             'Close the program and open agan!\n'
    #                             'Then update Database')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Critical)
    #         x = msg.exec_()


    #     elif PL_type != '-' and KSSS_prod == '' and Product_Name == '-' and Brand == 'All' and Date == '-':
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
            
    #     elif PL_type != '-' and KSSS_prod == '' and Product_Name == '-' and Brand == 'All' and Date != '-':
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)
                   
    #     elif PL_type == '-' and KSSS_prod != '' and Date == '-':
    #         KSSS_prod = int(KSSS_prod)
    #         price_data = price_data[(price_data['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)

    #     elif PL_type != '-' and KSSS_prod != '' and Date == '-':
    #         KSSS_prod = int(KSSS_prod)
    #         price_data = price_data[(price_data['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
            
    #     elif PL_type == '-' and KSSS_prod != '' and Date != '-':
    #         KSSS_prod = int(KSSS_prod)
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)

    #     elif PL_type != '-' and KSSS_prod != '' and Date != '-':
    #         KSSS_prod = int(KSSS_prod)
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)
        
    #     elif PL_type == '-' and Product_Name != '-' and Date == '-':
    #         price_data = price_data[(price_data['Product_Name'] == Product_Name)]

    #     elif PL_type != '-' and Product_Name != '-' and Date == '-':
    #         price_data = price_data[(price_data['Product_Name'] == Product_Name)]
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
            
    #     elif PL_type == '-' and Product_Name != '-' and Date != '-':
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['Product_Name'] == Product_Name)]
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)

    #     elif PL_type != '-' and Product_Name != '-' and Date != '-':
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['Product_Name'] == Product_Name)]
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)
            
    #     elif PL_type == '-' and Product_Name == '-' and Date == '-':
    #         price_data = price_data[(price_data['Brand'] == Brand)].reset_index(drop=True)
        
    #     elif PL_type != '-' and Product_Name == '-' and Date == '-':
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Brand'] == Brand)].reset_index(drop=True)
         
    #     elif PL_type == '-' and Brand != 'All' and Product_Name == '-' and Date != '-':
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['Brand'] == Brand)]
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)
        
    #     elif PL_type != '-' and Brand != 'All' and Product_Name == '-' and Date != '-':
    #         price_data['Date'] = price_data['Date'].astype(str)
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Brand'] == Brand)]
    #         price_data = price_data[(price_data['Date'] == Date)].reset_index(drop=True)           
                
    #     elif PL_type == '-' and Brand != 'All' and Product_Name == '-' and Date == '-':
    #         price_data = price_data[(price_data['Brand'] == Brand)].reset_index(drop=True)  
        
    #     elif PL_type != '-' and Brand != 'All' and Product_Name == '-' and Date == '-':
    #         price_data = price_data[(price_data['PL_type'] == PL_type)].reset_index(drop=True)
    #         price_data = price_data[(price_data['Brand'] == Brand)].reset_index(drop=True)  

    #     else:
    #         price_data
            
    #         price_data = price_data.sort_values(by=['Product_Name', 'Pack', 'Date'])
    #         price_data['Date'] = price_data['Date'].astype(str)

    #     headers = price_data.columns.values.tolist()
        
    #     self.table.setColumnCount(len(headers))
    #     self.table.setHorizontalHeaderLabels(headers)
    #     self.table.setColumnCount(len(price_data.columns))
        
    #     for i, row in price_data.iterrows():
    #         self.table.setRowCount(self.table.rowCount() + 1)
            
    #         for j in range(self.table.columnCount()):
    #             self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

    
    # def get_all_prices_from_db(self):
    #     price_request = db.query(Base_PL, Products).join(Products
    #                                                      ).with_entities(Products.KSSS_prod, Products.Product_Name, 
    #                                                                      Base_PL.PL_type, Base_PL.Date, Base_PL.Price)
    #     price_data = pd.DataFrame(price_request)
        
    #     prod_request = db.query(Products, Brands, Packs).join(Brands).join(Packs)
    #     prod_data = pd.read_sql_query(prod_request.statement, engine)
        
    #     if price_data.empty == False and prod_data.empty == False:
    #         price_data['Price'] = price_data['Price'].astype(float)
    #         price_data['Price'] = price_data['Price'].round(2)
    #         prod_data = prod_data[['KSSS_prod', 'Pack', 'Brand']]

    #         price_data = pd.merge(price_data, prod_data, how='left')
    #         price_data = price_data[['Brand', 'KSSS_prod', 'Product_Name', 'Pack', 'PL_type', 'Date', 'Price']]
        
    #     return price_data
        
        
    # def fill_in_chng_date_list(self):
    #     price_data = self.get_all_prices_from_db()
        
    #     Brand = self.ui.line_brand.currentText()
    #     PL_type = self.ui.line_PL_type.currentText()
    #     Product_Name = self.ui.line_prod_name.currentText()
    #     KSSS_prod = self.ui.line_KSSS.text()

    #     if price_data.empty == True:
    #         self.ui.line_date.addItem('-')
            
    #     else:
    #         price_data['KSSS_prod'] = price_data['KSSS_prod'].astype(int)
    #         self.ui.line_date.clear()
            
    #         if PL_type == '-' and Brand == 'All' and Product_Name == '-' and KSSS_prod == '':
    #             chng_date = price_data.sort_values(by=['Date'])
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)
            
    #         elif PL_type != '-' and Brand == 'All' and Product_Name == '-' and KSSS_prod == '':
    #             chng_date = price_data[['Date', 'PL_type']]
    #             chng_date = chng_date[(chng_date['PL_type'] == PL_type)]
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)

    #         elif PL_type == '-' and Brand != 'All' and Product_Name == '-' and KSSS_prod == '':
    #             chng_date = price_data[['Brand', 'Date']]
    #             chng_date = chng_date[(chng_date['Brand'] == Brand)].reset_index(drop=True)
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = pd.to_datetime(chng_date['Date'])
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)
            
    #         elif PL_type != '-' and Brand != 'All' and Product_Name == '-' and KSSS_prod == '':
    #             chng_date = price_data[['Brand', 'Date', 'PL_type']]
    #             chng_date = chng_date[(chng_date['PL_type'] == PL_type)].reset_index(drop=True)
    #             chng_date = chng_date[(chng_date['Brand'] == Brand)].reset_index(drop=True)
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = pd.to_datetime(chng_date['Date'])
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)

    #         elif PL_type == '-' and Product_Name != '-' and KSSS_prod == '':
    #             chng_date = price_data[['Product_Name', 'Date']]
    #             chng_date = chng_date[(chng_date['Product_Name'] == Product_Name)].reset_index(drop=True)
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = pd.to_datetime(chng_date['Date'])
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)
                
    #         elif PL_type != '-' and Product_Name != '-' and KSSS_prod == '':
    #             chng_date = price_data[['Product_Name', 'Date', 'PL_type']]
    #             chng_date = chng_date[(chng_date['PL_type'] == PL_type)].reset_index(drop=True)
    #             chng_date = chng_date[(chng_date['Product_Name'] == Product_Name)].reset_index(drop=True)
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = pd.to_datetime(chng_date['Date'])
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)

    #         elif PL_type == '-' and KSSS_prod != '':
    #             KSSS_prod = int(KSSS_prod)
    #             chng_date = price_data[['KSSS_prod', 'Date']]
    #             chng_date = chng_date[(chng_date['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = pd.to_datetime(chng_date['Date'])
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)
            
    #         elif PL_type != '-' and KSSS_prod != '':
    #             KSSS_prod = int(KSSS_prod)
    #             chng_date = price_data[['KSSS_prod', 'Date', 'PL_type']]
    #             chng_date = chng_date[(chng_date['PL_type'] == PL_type)].reset_index(drop=True)
    #             chng_date = chng_date[(chng_date['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #             chng_date = chng_date.drop_duplicates(subset=['Date'])
    #             chng_date['Date'] = pd.to_datetime(chng_date['Date'])
    #             chng_date = chng_date.sort_values(by=['Date'])
    #             chng_date['Date'] = chng_date['Date'].astype(str)
    #             chng_date_list = chng_date['Date'].tolist()
    #             chng_date_list.insert(0, '-')
    #             self.ui.line_date.addItems(chng_date_list)


    # def fill_in_prod_list(self):
    #     price_data = self.get_all_prices_from_db()
        
    #     PL_type = self.ui.line_PL_type.currentText()
    #     Brand = self.ui.line_brand.currentText()
    #     KSSS_prod = self.ui.line_KSSS.text()

    #     if price_data.empty == True:
    #         self.ui.line_prod_name.addItem('-')
            
    #     else:
    #         self.ui.line_prod_name.clear()
               
    #         if PL_type == '-' and Brand == 'All' and KSSS_prod == '':
    #             prod_name = price_data[['Product_Name']]
    #             prod_name = prod_name.sort_values(by=['Product_Name'])
    #             prod_name = prod_name.drop_duplicates(subset=['Product_Name'])
    #             prod_name_list = prod_name['Product_Name'].tolist()
    #             prod_name_list.insert(0, '-')
    #             self.ui.line_prod_name.addItems(prod_name_list)
            
    #         elif PL_type != '-' and Brand == 'All' and KSSS_prod == '':
    #             prod_name = price_data[['Product_Name', 'PL_type']]
    #             prod_name = prod_name[(prod_name['PL_type'] == PL_type)].reset_index(drop=True)
    #             prod_name = prod_name.sort_values(by=['Product_Name'])
    #             prod_name = prod_name.drop_duplicates(subset=['Product_Name'])
    #             prod_name_list = prod_name['Product_Name'].tolist()
    #             prod_name_list.insert(0, '-')
    #             self.ui.line_prod_name.addItems(prod_name_list)

    #         elif PL_type == '-' and Brand != 'All' and KSSS_prod == '':
    #             prod_name = price_data[['Brand', 'Product_Name']]
    #             prod_name = prod_name[(prod_name['Brand'] == Brand)].reset_index(drop=True)
    #             prod_name = prod_name.drop_duplicates(subset=['Product_Name'])
    #             prod_name = prod_name.sort_values(by=['Product_Name'])
    #             prod_name_list = prod_name['Product_Name'].tolist()
    #             prod_name_list.insert(0, '-')
    #             self.ui.line_prod_name.addItems(prod_name_list)
            
    #         elif PL_type != '-' and Brand != 'All' and KSSS_prod == '':
    #             prod_name = price_data[['Brand', 'Product_Name', 'PL_type']]
    #             prod_name = prod_name[(prod_name['PL_type'] == PL_type)].reset_index(drop=True)
    #             prod_name = prod_name[(prod_name['Brand'] == Brand)].reset_index(drop=True)
    #             prod_name = prod_name.drop_duplicates(subset=['Product_Name'])
    #             prod_name = prod_name.sort_values(by=['Product_Name'])
    #             prod_name_list = prod_name['Product_Name'].tolist()
    #             prod_name_list.insert(0, '-')
    #             self.ui.line_prod_name.addItems(prod_name_list)

    #         elif PL_type == '-' and KSSS_prod != '':
    #             prod_name = price_data[['KSSS_prod', 'Product_Name']]
    #             prod_name = prod_name[(prod_name['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #             prod_name = prod_name.drop_duplicates(subset=['Product_Name'])
    #             prod_name = prod_name.sort_values(by=['Product_Name'])
    #             prod_name_list = prod_name['Product_Name'].tolist()
    #             prod_name_list.insert(0, '-')
    #             self.ui.line_prod_name.addItems(prod_name_list)
                
    #         elif PL_type != '-' and KSSS_prod != '':
    #             prod_name = price_data[['KSSS_prod', 'Product_Name', 'PL_type']]
    #             prod_name = prod_name[(prod_name['PL_type'] == PL_type)].reset_index(drop=True)
    #             prod_name = prod_name[(prod_name['KSSS_prod'] == KSSS_prod)].reset_index(drop=True)
    #             prod_name = prod_name.drop_duplicates(subset=['Product_Name'])
    #             prod_name = prod_name.sort_values(by=['Product_Name'])
    #             prod_name_list = prod_name['Product_Name'].tolist()
    #             prod_name_list.insert(0, '-')
    #             self.ui.line_prod_name.addItems(prod_name_list)
            

    # def fill_in_pl_type(self):
    #     pl_type_data = self.get_all_prices_from_db()

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Name = self.ui.line_prod_name.currentText()
    #     KSSS_prod = self.ui.line_KSSS.text()

    #     if pl_type_data.empty == True:
    #         self.ui.line_PL_type.addItem('-')
            
    #     else:
    #         pl_type_data = pl_type_data[['PL_type']]
    #         pl_type_data = pl_type_data.sort_values(by=['PL_type'])
    #         pl_type_data = pl_type_data.drop_duplicates(subset=['PL_type'])
    #         pl_type_list = pl_type_data['PL_type'].tolist()
    #         pl_type_list.insert(0, '-')
    #         self.ui.line_PL_type.addItems(pl_type_list)

        
    # def dowload_Prices(self):
    #     savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Base Prices.xlsx', 'Excel Workbook (*.xlsx)')
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

