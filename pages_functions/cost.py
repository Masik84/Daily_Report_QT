import numpy as np
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db
# from models import LPC, Batch_data, Products, Stock, Stock_data, oCOGS
from wind.pages.costs_ui import Ui_Form


class Costs(QWidget):
    def __init__(self):
        super(Costs, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.table = self.ui.table
        self.ui.table.resizeColumnsToContents()
        
        self.ui.btn_lpc_open_file.setToolTip('выбери файл ! ALL DATA !.xlsx')
        # self.ui.btn_lpc_open_file.clicked.connect(self.get_lpc_file)
        # self.ui.btn_lpc_upload_file.clicked.connect(self.upload_lpc_data)
        
        self.ui.btn_stock_open_file.setToolTip('выбери файл с Остатками')
        # self.ui.btn_stock_open_file.clicked.connect(self.get_stock_file)
        # self.ui.btn_stock_upload_file.clicked.connect(self.upload_stock_data)
        
        self.ui.btn_batch_open_file.setToolTip('выбери файл с Партиями')
        # self.ui.btn_batch_open_file.clicked.connect(self.get_batch_file)
        # self.ui.btn_batch_upload_file.clicked.connect(self.upload_batch_data)
        
        self.ui.btn_st_type_open_file.setToolTip('выбери файл с Типами Скодов')
        # self.ui.btn_st_type_open_file.clicked.connect(self.get_stock_type_file)
        # self.ui.btn_st_type_upload_file.clicked.connect(self.upload_stock_type_data)
        # self.ui.btn_ocogs_create.clicked.connect(self.create_ocogs)
        # self.ui.btn_update_tab.clicked.connect(self.update_table)


    def get_lpc_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_lpc_file.setText(get_file[0])
            

    # def upload_lpc_data(self, LPC_file_xls):
    #     LPC_file_xls = self.ui.label_lpc_file.text()
    #     if LPC_file_xls == 'File Path' or LPC_file_xls == 'Database was updated successfully':
    #             msg = QMessageBox()
    #             msg.setWindowTitle('Programm Error')
    #             msg.setText('!!! Please choose the file with LPC Data !!!')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 12pt  \"Segoe UI\";"
    #                             "color: #ff0000;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #     else:
    #         lpc_data = self.read_lpc_file(LPC_file_xls)
    #         self.update_lpc_db(lpc_data)
    #         msg = QMessageBox()
    #         msg.setText('Database was updated successfully')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Information)
    #         x = msg.exec_()
    #         self.ui.label_lpc_file.setText('File Path')


    # def read_lpc_file(self, LPC_file_xls):
    #     LPC_df = pd.read_excel(LPC_file_xls, sheet_name='LPC_Full')
    #     LPC_df = LPC_df[['КССС мат', 'Period', 'LPC_price']]
    #     LPC_df.rename(columns={'КССС мат' : 'KSSS_prod'}, inplace = True)
    #     LPC_df['merge'] = LPC_df['KSSS_prod'].astype(str) + LPC_df['Period'].astype(str)
    #     LPC_df['KSSS_prod'] = LPC_df['KSSS_prod'].astype(int)
    #     LPC_df['LPC_price'] = LPC_df['LPC_price'].astype(float)

    #     LPC_data = LPC_df.to_dict('records')

    #     return LPC_data


    # def update_lpc_db(self, data):
    #     lpc_for_create = []
    #     lpc_for_update = []
    #     for row in data:
    #         lpc_exists = LPC.query.filter(LPC.merge == str(row['merge'])).count()
    #         if lpc_exists == 0:
    #             lpc_list = {'merge' : str(row['merge']),
    #                             'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                             'Period' : row['Period'],
    #                             'LPC_price' : row['LPC_price']}
    #             lpc_for_create.append(lpc_list)

    #         elif lpc_exists > 0:
    #             lpc_list = {'id' : self.get_id_LPC(str(row['merge'])),
    #                             'merge' : str(row['merge']),
    #                             'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                             'Period' : row['Period'],
    #                             'LPC_price' : row['LPC_price']}
    #             lpc_for_update.append(lpc_list)
                
    #     db.bulk_insert_mappings(LPC, lpc_for_create)
    #     db.bulk_update_mappings(LPC, lpc_for_update)

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
    #     return lpc_for_create


    # def get_id_LPC(self, merge):
    #     db_data = LPC.query.filter(LPC.merge == merge).first()
    #     lpc_id = db_data.id

    #     return lpc_id


    # def get_stock_file(self):
    #     get_file = QFileDialog.getOpenFileName(self, 'Choose File')
    #     if get_file:
    #         self.ui.label_stock_file.setText(get_file[0])
            

    # def upload_stock_data(self, stock_file_xls):
    #     stock_file_xls = self.ui.label_stock_file.text()
    #     if stock_file_xls == 'File Path' or stock_file_xls == 'Database was updated successfully':
    #             msg = QMessageBox()
    #             msg.setWindowTitle('Programm Error')
    #             msg.setText('!!! Please choose the file with Stock Data !!!')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 12pt  \"Segoe UI\";"
    #                             "color: #ff0000;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #     else:
    #         stock_data = self.read_stock_file(stock_file_xls)
    #         self.update_Stock_data(stock_data)
    #         msg = QMessageBox()
    #         msg.setText('Database was updated successfully')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Information)
    #         x = msg.exec_()
    #         self.ui.label_stock_file.setText('File Path')


    # def read_stock_file(self, stock_file_xls):
    #     # stock_df = pd.read_excel(stock_file_xls, skiprows = 11, thousands='.', decimal=',')
    #     stock_df = pd.read_excel(stock_file_xls, sheet_name='Sheet1', thousands='.', decimal=',')

    #     stock_df = stock_df[['Период:с', 'КодКССС', 'Завод(код)', 'СклдХранен', 'Партия', 'ГодВрбтк', 
    #                         'МесВрбтк', 'Завод', 'Наименованиепроизводителя', 
    #                         'ОстНаНач', 'ОстНачСбЕИ', 'ОстНаКонец', 'ОстКнцСбЕд']]
        
    #     stock_df.rename(columns={'Период:с' : 'Period',
    #                                 'КодКССС' : 'KSSS_prod',
    #                                 'Наименованиематериала' : 'Product_Name',
    #                                 'Завод(код)' : 'Stock_code',
    #                                 'СклдХранен' : 'Stock_Name',
    #                                 'Партия' : 'Batch',
    #                                 'ГодВрбтк' : 'Year',
    #                                 'МесВрбтк' : 'Mnth',
    #                                 'Завод' : 'Plant',
    #                                 'Наименованиепроизводителя' : 'Plant_Name',
    #                                 'ОстНаНач' : 'Qty_start',
    #                                 'ОстНачСбЕИ' : 'Amount_start',
    #                                 'ОстНаКонец' : 'Qty_end',
    #                                 'ОстКнцСбЕд' : 'Amount_end'}, inplace = True)
        
    #     stock_df = stock_df[(stock_df['KSSS_prod'] > 0)]
    #     stock_df['KSSS_prod'] = stock_df['KSSS_prod'].astype(int)
    #     stock_df['Year'] = stock_df['Year'].astype(int)
    #     stock_df['Mnth'] = stock_df['Mnth'].astype(int)
    #     stock_df['Batch'] = stock_df['Batch'].astype(str)

    #     stock_df['Plant'] = stock_df['Plant'].fillna('-')
    #     stock_df['Plant_Name'] = stock_df['Plant_Name'].fillna('-')

    #     stock_df['Qty_start'] = stock_df['Qty_start'].replace(np.nan, 0)
    #     stock_df['Qty_end'] = stock_df['Qty_end'].replace(np.nan, 0)
    #     stock_df['check'] = stock_df.apply(self.alert, axis=1)
    #     stock_df = stock_df[(stock_df['check'] != 'for_del')]
    #     stock_df.pop('check')

    #     stock_df['Stock_code'] = stock_df['Stock_code'].astype(str)
    #     stock_df['Plant'] = stock_df['Plant'].astype(str)
    #     stock_df['Batch'] = stock_df['Batch'].astype(str)
    #     stock_df['Amount_start'] = stock_df['Amount_start'].astype(float)
    #     stock_df['Amount_end'] = stock_df['Amount_end'].astype(float)
    #     stock_df['Qty_start'] = stock_df['Qty_start'].astype(float)
    #     stock_df['Qty_end'] = stock_df['Qty_end'].astype(float)

    #     stock_df['Stock_code'] = stock_df.apply(self.correct_Stock, axis=1)
    #     stock_df['Plant'] = stock_df.apply(self.correct_Plant, axis=1)

    #     stock_df['merge'] = stock_df['Period'].astype(str) + stock_df['KSSS_prod'].astype(str) + stock_df['Stock_code'].astype(str) + stock_df['Batch'].astype(str)

    #     stock_data = stock_df.to_dict('records')

    #     return stock_data


    # def correct_Stock(self, row):
    #     if row['Stock_code'].isdigit() == True:
    #         if int(row['Stock_code']) < 10:
    #             return '0' + row['Stock_code']
    #     else:
    #         return row['Stock_code']
        
        
    # def correct_Plant(self, row):
    #     if row['Plant'].isdigit() == True:
    #         if int(row['Plant']) < 10:
    #             return '0' + row['Plant']
    #     else:
    #         return row['Plant']


    # def update_Stock_data(self, data):
    #     stock_for_create = []
    #     stock_for_update = []
    #     for row in data:
    #         stock_exists = Stock_data.query.filter(Stock_data.merge == str(row['merge'])).count()
    #         if stock_exists == 0:
    #             stock_list = {'merge' : str(row['merge']),
    #                                 'Period' : row['Period'],
    #                                 'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                 'stock_id' : self.get_id_stock_type(row['Stock_code']),
    #                                 'Batch' : row['Batch'],
    #                                 'Year' : row['Year'],
    #                                 'Mnth' : row['Mnth'],
    #                                 'Plant' : row['Plant'],
    #                                 'Plant_Name' : row['Plant_Name'],
    #                                 'Qty_start' : row['Qty_start'],
    #                                 'Amount_start' : row['Amount_start'],
    #                                 'Qty_end' : row['Qty_end'],
    #                                 'Amount_end' : row['Amount_end']}
    #             stock_for_create.append(stock_list)

    #         elif stock_exists > 0:
    #             stock_list = {'id' : self.get_id_Stock_data(str(row['merge'])),
    #                                 'merge' : row['merge'],
    #                                 'Period' : row['Period'],
    #                                 'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                 'stock_id' : self.get_id_stock_type(row['Stock_code']),
    #                                 'Batch' : row['Batch'],
    #                                 'Year' : row['Year'],
    #                                 'Mnth' : row['Mnth'],
    #                                 'Plant' : row['Plant'],
    #                                 'Plant_Name' : row['Plant_Name'],
    #                                 'Qty_start' : row['Qty_start'],
    #                                 'Amount_start' : row['Amount_start'],
    #                                 'Qty_end' : row['Qty_end'],
    #                                 'Amount_end' : row['Amount_end']}
    #             stock_for_update.append(stock_list)
                
    #     db.bulk_insert_mappings(Stock_data, stock_for_create)
    #     db.bulk_update_mappings(Stock_data, stock_for_update)

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
    #     return stock_for_create


    # def get_batch_file(self):
    #     get_file = QFileDialog.getOpenFileName(self, 'Choose File')
    #     if get_file:
    #         self.ui.label_batch_file.setText(get_file[0])
            

    # def upload_batch_data(self, batch_file_xls):
    #     batch_file_xls = self.ui.label_batch_file.text()
    #     if batch_file_xls == 'File Path' or batch_file_xls == 'Database was updated successfully':
    #             msg = QMessageBox()
    #             msg.setWindowTitle('Programm Error')
    #             msg.setText('!!! Please choose the file with Batch Data !!!')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 12pt  \"Segoe UI\";"
    #                             "color: #ff0000;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #     else:
    #         batch_data = self.read_batch_file(batch_file_xls)
    #         self.update_Batch_data(batch_data)
    #         msg = QMessageBox()
    #         msg.setText('Database was updated successfully')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Information)
    #         x = msg.exec_()
    #         self.ui.label_batch_file.setText('File Path')


    # def read_batch_file(self, batch_file_xls):
    #     batch_df = pd.read_excel(batch_file_xls, sheet_name='Лист1')
    #     batch_df = batch_df[['Партия', 'КССС Мтрл', 'Количество', 'Сумма']]
    #     batch_df.rename(columns={'Партия' : 'Batch',
    #                                 'КССС Мтрл' : 'KSSS_prod',
    #                                 'Количество' : 'Qty',
    #                                 'Сумма' : 'Proceeds'}, inplace = True)
        
    #     batch_df['KSSS_prod'] = batch_df['KSSS_prod'].astype(int)
    #     batch_df['Batch'] = batch_df['Batch'].astype(str)

    #     reques = db.query(Stock_data, Products).join(Products
    #                                                      ).with_entities(Products.KSSS_prod, Stock_data.Batch, Stock_data.Qty_start, 
    #                                                                      Stock_data.Qty_end, Stock_data.Amount_start, Stock_data.Amount_end)
    #     db_stock = pd.DataFrame(reques)

    #     db_stock['Amount_start'] = db_stock['Amount_start'].astype(float)
    #     db_stock['Amount_end'] = db_stock['Amount_end'].astype(float)
    #     db_stock['Qty_start'] = db_stock['Qty_start'].astype(float)
    #     db_stock['Qty_end'] = db_stock['Qty_end'].astype(float)

    #     db_stock['Amount'] = db_stock.apply(self.check_Amount, axis=1)
    #     db_stock.pop('Amount_start')
    #     db_stock.pop('Amount_end')

    #     db_stock['Qty'] = db_stock.apply(self.check_Qty, axis=1)
    #     db_stock.pop('Qty_start')
    #     db_stock.pop('Qty_end')

    #     db_stock['Proceeds'] = (db_stock['Amount'] * (db_stock['Qty']/1000)).round(2)
    #     db_stock.pop('Amount')
        
    #     frames = [batch_df, db_stock]
    #     batch_df = pd.concat(frames)

    #     batch_df['merge'] = batch_df['Batch'].astype(str) + batch_df['KSSS_prod'].astype(str)
    #     batch_df['merge'] = batch_df['merge'].astype(str)
    #     batch_df = batch_df.groupby(['merge', 'Batch', 'KSSS_prod']).sum().reset_index()
    #     batch_df = batch_df[batch_df['Qty'] != 0]

    #     batch_df['Amount'] = (batch_df['Proceeds']/(batch_df['Qty']/1000)).round(2)
    #     batch_df.pop('Qty')
    #     batch_df.pop('Proceeds')

    #     batch_data = batch_df.to_dict('records')

    #     return batch_data


    # def update_Batch_data(self, data):
    #     batch_for_create = []
    #     batch_for_update = []
    #     for row in data:
    #         batch_exists = Batch_data.query.filter(Batch_data.merge == row['merge']).count()
    #         if batch_exists == 0:
    #             batch_list = {'merge' : str(row['merge']),
    #                                 'Batch' : row['Batch'],
    #                                 'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                 'Amount' : row['Amount']}
    #             batch_for_create.append(batch_list)

    #         elif batch_exists > 0:
    #             batch_list = {'id' : self.get_id_Batch_data(row['merge']),
    #                                 'merge' : str(row['merge']),
    #                                 'Batch' : row['Batch'],
    #                                 'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                 'Amount' : row['Amount']}
    #             batch_for_update.append(batch_list)
                
    #     db.bulk_insert_mappings(Batch_data, batch_for_create)
    #     db.bulk_update_mappings(Batch_data, batch_for_update)

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
    #     return batch_for_create


    # def create_ocogs(self):
    #     year = self.ui.line_ed_year.text()
    #     ed_amount = self.ui.line_ed_amount.text()
    #     eco_amount = self.ui.line_eco_amount.text()

    #     ocogs_for_create = []
    #     ocogs_for_update = []
    #     ocogs_exists = oCOGS.query.filter(oCOGS.year == int(year)).count()
    #     if ocogs_exists == 0:
    #         ocogs_list = {'year' : int(year),
    #                                 'ED' : float(ed_amount),
    #                                 'EcoFee' : float(eco_amount)}
    #         ocogs_for_create.append(ocogs_list)

    #     elif ocogs_exists > 0:
    #         ocogs_list = {'id' : self.get_id_oCOGS(int(year)),
    #                                 'year' : int(year),
    #                                 'ED' : float(ed_amount),
    #                                 'EcoFee' : float(eco_amount)}
    #         ocogs_for_update.append(ocogs_list)
                
    #     db.bulk_insert_mappings(oCOGS, ocogs_for_create)
    #     db.bulk_update_mappings(oCOGS, ocogs_for_update)
    #     db.commit()
    #     self.ui.line_ed_year.clear()
    #     self.ui.line_ed_amount.clear()
    #     self.ui.line_eco_amount.clear()

    #     return ocogs_for_create


    # def get_stock_type_file(self):
    #     get_file = QFileDialog.getOpenFileName(self, 'Choose File')
    #     if get_file:
    #         self.ui.label_st_type_file.setText(get_file[0])
            
            
    # def upload_stock_type_data(self, st_type_file_xls):
    #     st_type_file_xls = self.ui.label_st_type_file.text()
    #     if st_type_file_xls == 'File Path' or st_type_file_xls == 'Database was updated successfully':
    #             msg = QMessageBox()
    #             msg.setWindowTitle('Programm Error')
    #             msg.setText('!!! Please choose the file with Stock Type Data !!!')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 12pt  \"Segoe UI\";"
    #                             "color: #ff0000;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #     else:
    #         st_type_data = self.read_stock_type_file(st_type_file_xls)
    #         self.update_stock(st_type_data)
    #         msg = QMessageBox()
    #         msg.setText('Database was updated successfully')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Information)
    #         x = msg.exec_()
    #         self.ui.label_st_type_file.setText('File Path')
            
            
    # def read_stock_type_file(self, st_type_file_xls):
    #     st_type_df = pd.read_excel(st_type_file_xls)
    #     st_type_df = st_type_df[['ПОтг', 'Пункт отгрузки', 'без согласования']]

    #     st_type_df.rename(columns={'ПОтг' : 'Stock_code', 'Пункт отгрузки' : 'Stock_Name', 'без согласования' : 'Type'}, inplace = True)
        
    #     st_type_df['Stock_code'] = st_type_df['Stock_code'].astype(str)
    #     st_type_df.drop_duplicates(subset=['Stock_code'], inplace = True)
    #     st_type_df['Stock_Name'] = st_type_df['Stock_Name'].str.replace('"', '')
        
    #     st_type_df['Type'] = st_type_df.apply(self.check_Type, axis=1)

    #     st_type_data = st_type_df.to_dict('records')

    #     return st_type_data


    # def update_stock(self, data):
    #     st_type_for_create = []
    #     st_type_for_update = []
    #     for row in data:
    #         st_type_exists = Stock.query.filter(Stock.Stock == row['Stock_code']).count()

    #         if st_type_exists == 0:
    #             st_type_list = {'Stock' : row['Stock_code'], 
    #                                     'Stock_Name' : row['Stock_Name'],
    #                                     'Type' : row['Type']}
    #             st_type_for_create.append(st_type_list)

    #         elif st_type_exists > 0:
    #             st_type_list = {'id' : self.get_id_stock_type(row['Stock_code']), 
    #                                     'Stock' : row['Stock_code'], 
    #                                     'Stock_Name' : row['Stock_Name'],
    #                                     'Type' : row['Type']}
    #             st_type_for_update.append(st_type_list)
                
    #     db.bulk_insert_mappings(Stock, st_type_for_create)
    #     db.bulk_update_mappings(Stock, st_type_for_update)

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
    #     return st_type_for_create


    # def get_id_stock_type(self, Stock_code):
    #     db_data = Stock.query.filter(Stock.Stock == Stock_code).first()
    #     st_type_id = db_data.id

    #     return st_type_id


    # def check_Type(self, row):
    #     if row['Type'] == '+':
    #         return 'yes'
    #     else:
    #         return 'no'


    # def get_id_Stock_data(self, merge):
    #     db_data = Stock_data.query.filter(Stock_data.merge == merge).first()
    #     stock_data_id = db_data.id

    #     return stock_data_id


    # def get_id_Batch_data(self, merge):
    #     db_data = Batch_data.query.filter(Batch_data.merge == merge).first()
    #     batch_data_id = db_data.id

    #     return batch_data_id


    # def get_id_oCOGS(self, year):
    #     db_data = oCOGS.query.filter(oCOGS.year == year).first()
    #     ocogs_data_id = db_data.id

    #     return ocogs_data_id


    # def alert(self, row):
    #     if row['Qty_start'] == 0.0 and row['Qty_end'] == 0.0:
    #         return 'for_del'
    #     else:
    #         return 'ok'


    # def check_Amount(self, row):
    #     if row['Amount_start'] == 0.0:
    #         return row['Amount_end']
    #     else:
    #         return row['Amount_start']


    # def check_Qty(self, row):
    #     if row['Qty_start'] == 0:
    #         return row['Qty_end']
    #     else:
    #         return row['Qty_start']


    # def update_table(self):
    #     ocogs_reques = db.execute(select(oCOGS.year, oCOGS.ED, oCOGS.EcoFee)).all()
    #     ocogs_data = pd.DataFrame(ocogs_reques)
    #     ocogs_data['year'] = ocogs_data['year'].astype(int)
    #     ocogs_data['ED'] = ocogs_data['ED'].astype(int)
    #     ocogs_data['EcoFee'] = ocogs_data['EcoFee'].astype(int)

    #     if ocogs_data.empty == True:
    #         msg = QMessageBox()
    #         msg.setText('There is no COGS data in Database. \n'
    #                             'Close the program and open agan!\n'
    #                             'Then update Database')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 12pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Critical)
    #         x = msg.exec_()
    #     else:
    #         self.table.setColumnCount(len(ocogs_data.columns))
    #         self.table.setRowCount(len(ocogs_data.index))
            
    #         for i in range(len(ocogs_data.index)):
    #             for j in range(len(ocogs_data.columns)):
    #                 self.table.setItem(i,j,QTableWidgetItem(str(ocogs_data.iloc[i, j])))


    # def get_id_Product(self, KSSS_prod):
    #     if KSSS_prod != 'nan':
    #         db_data = Products.query.filter(Products.KSSS_prod == KSSS_prod).first()
    #         product_id = db_data.id
    #     else:
    #         product_id = None

    #     return product_id



