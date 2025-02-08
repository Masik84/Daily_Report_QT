from datetime import datetime

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db
# from models import Base_PL, Customers_ALL, Invoices, PL_chng, Products
from wind.pages.invoice_ui import Ui_Form as Inv_Form
from wind.pages.report_cols_ui import Ui_Form as Cols_Form


class Rep_Invoices(QWidget):
    def __init__(self):
        super(Rep_Invoices, self).__init__()
        self.ui = Inv_Form()
        self.ui.setupUi(self)
        
        # self.fill_in_prod_group()
        # self.fill_in_inv_date()
        # self.fill_in_del_date()
        
        # self.ui.line_brand.currentTextChanged.connect(self.fill_in_prod_group)
        # self.ui.line_segment.currentTextChanged.connect(self.fill_in_prod_group)
        
        # self.ui.btn_select_cols.setToolTip('выбери колонки для отчета')
        # self.ui.btn_select_cols.clicked.connect(self.go_to_Select_Cols)
        
        # self.ui.btn_open_file.clicked.connect(self.get_file)
        # self.ui.btn_upload_file.clicked.connect(self.upload_data)
        # self.ui.btn_download.clicked.connect(self.dowload_Invoices)
        
        self.ui.rep_date.setCalendarPopup(True)

        
    def onDateChanged(self,date):
        period = date.toString('yyyy-MM-dd')
        return period
        
        
    def go_to_Select_Cols(self):
        self.columns_form = QWidget()
        self.columns = Cols_Form()
        self.columns.setupUi(self.columns_form)
        self.columns_form.show()
        self.columns.btn_select.clicked.connect(self.get_columns)
        
        # self.columns_form.close()


    def get_columns(self):
        pass
 
    
    def get_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_invoice_File.setText(get_file[0])
 
            
    def upload_data(self, inv_file_xls):
        inv_file_xls = self.ui.label_invoice_File.text()
        if inv_file_xls == 'File Path' or inv_file_xls == 'Database was updated successfully':
            msg = QMessageBox()
            msg.setWindowTitle('Programm Error')
            msg.setText('!!! Please choose the file with Invoice Data !!!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                                            "font: 12pt  \"Segoe UI\";"
                                            "color: #ff0000;\n"
                                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            inv_data = self.read_inv_file(inv_file_xls)
            self.update_Invoices(inv_data)

            msg = QMessageBox()
            msg.setText('Database was updated successfully')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Segoe UI\";"
                            "color: #4b0082;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            self.ui.label_invoice_File.setText('File Path')
 
            
    # def read_inv_file(self, inv_file_xls):
    #     inv_df = pd.read_excel(inv_file_xls, sheet_name='Лист1')
    #     inv_df = inv_df[['№ докум.', 'ПОтг', 'З-д', 'Дата фактуры', 'Код КССС плательщика', 'Номер дебитора', 
    #                                 '№ договора', 'КСССмат.', 'Накладная', 'Фактура', 'ВФакт', 'ДатаСоздан', 'ДатаДокум', 
    #                                 'Д/проводки', 'Партия', 'ДатаОтгр.', 'Дата ППС', 'Кол-во по фактуре', 'ЕИ', 'Цена (без НДС)', 'Вал.']]
        
    #     inv_df.rename(columns={'№ докум.' : 'Account_doc',
    #                                                 'ПОтг' : 'Stock',
    #                                                 'З-д' : 'Plant',
    #                                                 'Дата фактуры' : 'Invoice_Date',
    #                                                 'Код КССС плательщика' : 'KSSS_cust',
    #                                                 'Номер дебитора' : 'Customer_Name',
    #                                                 '№ договора' : 'Contract_N',
    #                                                 'КСССмат.' : 'KSSS_prod',
    #                                                 'Накладная' : 'Delivery_doc',
    #                                                 'Фактура' : 'Account_doc2',
    #                                                 'ВФакт' : 'Inv_type',
    #                                                 'ДатаСоздан' : 'Creation_Date',
    #                                                 'ДатаДокум' : 'Document_Date',
    #                                                 'Д/проводки' : 'Transaction_Date',
    #                                                 'Партия' : 'Batch',
    #                                                 'ДатаОтгр.' : 'Delivery_Date',
    #                                                 'Дата ППС' : 'Date_PPS',
    #                                                 'Кол-во по фактуре' : 'Volume',
    #                                                 'ЕИ' : 'EA',
    #                                                 'Цена (без НДС)' : 'Price',
    #                                                 'Вал.' : 'Curr'}, inplace = True)
        
    #     inv_df['KSSS_prod'] = inv_df['KSSS_prod'].fillna('-')
    #     inv_df = inv_df.loc[~inv_df['KSSS_prod'].str.contains(r'[^\d\.]')]
    #     inv_df = inv_df[(inv_df['KSSS_prod'] != '-')]
    #     inv_df['KSSS_prod'] = inv_df['KSSS_prod'].astype(int)
        
    #     inv_df['Delivery_doc'] = inv_df['Delivery_doc'].fillna('-')
    #     inv_df = inv_df[(inv_df['Delivery_doc'] != '-')]
        
    #     reques = db.execute(select(Products.KSSS_prod, Products.Product_Name, Products.Brand)).all()
    #     product_df = pd.DataFrame(reques)
    #     product_df['KSSS_prod'] = product_df['KSSS_prod'].astype(int)

    #     inv_df = pd.merge(inv_df, product_df, how='left', on='KSSS_prod')
        
    #     inv_df['Product_Name'] = inv_df['Product_Name'].fillna('-')
    #     inv_df = inv_df[(inv_df.Product_Name != '-')]
    #     inv_df = inv_df.drop(['Product_Name'], axis = 1)

    #     inv_df['KSSS_cust'] = inv_df['KSSS_cust'].replace(np.nan, 0).astype(int)
    #     inv_df['KSSS_prod'] = inv_df['KSSS_prod'].replace(np.nan, 0).astype(int)
        
    #     inv_df['Customer_Name'] = inv_df['Customer_Name'].str.replace('"', '')

    #     inv_df['Plant'] = inv_df['Plant'].astype(str)
    #     inv_df['Stock'] = inv_df['Stock'].astype(str)
    #     inv_df['Account_doc'] = inv_df['Account_doc'].astype(str)
    #     inv_df['Account_doc2'] = inv_df['Account_doc2'].astype(str)
    #     inv_df['Delivery_doc'] = inv_df['Delivery_doc'].astype(str)
    #     inv_df['Batch'] = inv_df['Batch'].astype(str)

    #     inv_df['Volume'] = inv_df['Volume'].replace(np.nan, 0).astype(float)
    #     inv_df['Price'] = inv_df['Price'].replace(np.nan, 0).astype(float)
    #     inv_df['Proceeds'] = (inv_df['Price'] * (inv_df['Volume']/1000)).round(2)
    #     inv_df = inv_df.drop(['Price'], axis = 1)

    #     # исправление формата дат
    #     inv_df['Invoice_Date'] = pd.to_datetime(inv_df['Invoice_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     inv_df['Creation_Date'] = pd.to_datetime(inv_df['Creation_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     inv_df['Document_Date'] = pd.to_datetime(inv_df['Document_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     inv_df['Transaction_Date'] = pd.to_datetime(inv_df['Transaction_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     inv_df['Delivery_Date'] = pd.to_datetime(inv_df['Delivery_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     inv_df['Date_PPS'] = pd.to_datetime(inv_df['Date_PPS'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
        
    #     inv_df['inv_merge'] = inv_df['Account_doc'] + inv_df['KSSS_prod'].astype (str) + inv_df['Delivery_doc'].astype (str) + inv_df['Account_doc2'].astype(str) + inv_df['Batch'].astype(str)
        
    #     inv_df = inv_df.groupby(['inv_merge', 'Account_doc', 'Stock', 'Plant', 'Invoice_Date', 'KSSS_cust', 'Customer_Name', 'Contract_N', 
    #                                             'KSSS_prod', 'Delivery_doc', 'Account_doc2', 'Inv_type', 'Creation_Date', 'Document_Date', 
    #                                             'Transaction_Date', 'Batch', 'Delivery_Date', 'Date_PPS', 'EA', 'Curr']).sum().round(2).reset_index()
        
    #     inv_df['Price'] = ((inv_df['Proceeds'] / inv_df['Volume'])*1000).round(2)
    #     inv_df = inv_df.drop(['Proceeds'], axis = 1)

    #     inv_data = inv_df.to_dict('records')

    #     return inv_data


    # def update_Invoices(self, data):
    #     inv_for_create = []
    #     inv_for_update = []
    #     for row in data:
    #         inv_exists = Invoices.query.filter(Invoices.inv_merge == str(row['inv_merge'])).count()
    #         if row['Date_PPS'] == '':
    #             row['Date_PPS'] = None
    #         else:
    #             row['Date_PPS'] = row['Date_PPS']

    #         if inv_exists == 0:
    #             inv_list = {'inv_merge' : row['inv_merge'],
    #                                 'Account_doc' : row['Account_doc'],
    #                                 'Stock' : row['Stock'],
    #                                 'Plant' : row['Plant'],
    #                                 'Invoice_Date' : row['Invoice_Date'],
    #                                 'KSSS_cust' : row['KSSS_cust'],
    #                                 'Customer_Name' : row['Customer_Name'],
    #                                 'Contract_N' : row['Contract_N'],
    #                                 'KSSS_prod' : row['KSSS_prod'],
    #                                 'Delivery_doc' : row['Delivery_doc'],
    #                                 'Account_doc2' : row['Account_doc2'],
    #                                 'Inv_type' : row['Inv_type'],
    #                                 'Creation_Date' : row['Creation_Date'],
    #                                 'Document_Date' : row['Document_Date'],
    #                                 'Transaction_Date' : row['Transaction_Date'],
    #                                 'Batch' : row['Batch'],
    #                                 'Delivery_Date' : row['Delivery_Date'],
    #                                 'Date_PPS' : row['Date_PPS'],
    #                                 'Volume' : row['Volume'],
    #                                 'EA' : row['EA'],
    #                                 'Price' : row['Price'],
    #                                 'Curr' : row['Curr']}
    #             inv_for_create.append(inv_list)

    #         elif inv_exists > 0:
    #             inv_list = {'id' : self.get_id_Invoice(row['inv_merge']),
    #                                 'inv_merge' : row['inv_merge'],
    #                                 'Account_doc' : row['Account_doc'],
    #                                 'Stock' : row['Stock'],
    #                                 'Plant' : row['Plant'],
    #                                 'Invoice_Date' : row['Invoice_Date'],
    #                                 'KSSS_cust' : row['KSSS_cust'],
    #                                 'Customer_Name' : row['Customer_Name'],
    #                                 'Contract_N' : row['Contract_N'],
    #                                 'KSSS_prod' : row['KSSS_prod'],
    #                                 'Delivery_doc' : row['Delivery_doc'],
    #                                 'Account_doc2' : row['Account_doc2'],
    #                                 'Inv_type' : row['Inv_type'],
    #                                 'Creation_Date' : row['Creation_Date'],
    #                                 'Document_Date' : row['Document_Date'],
    #                                 'Transaction_Date' : row['Transaction_Date'],
    #                                 'Batch' : row['Batch'],
    #                                 'Delivery_Date' : row['Delivery_Date'],
    #                                 'Date_PPS' : row['Date_PPS'],
    #                                 'Volume' : row['Volume'],
    #                                 'EA' : row['EA'],
    #                                 'Price' : row['Price'],
    #                                 'Curr' : row['Curr']}
    #             inv_for_update.append(inv_list)
                
    #     db.bulk_insert_mappings(Invoices, inv_for_create)
    #     db.bulk_update_mappings(Invoices, inv_for_update)

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
        
    #     self.ui.line_inv_year.clear()
    #     self.ui.line_inv_qtr.clear()
    #     self.ui.line_inv_mnth.clear()
        
    #     self.ui.line_del_year.clear()
    #     self.ui.line_del_qtr.clear()
    #     self.ui.line_del_mnth.clear()
        
    #     self.ui.line_pr_group.clear()
        
    #     self.fill_in_prod_group()
    #     self.fill_in_inv_date()
    #     self.fill_in_del_date()
        
        
    #     return inv_for_create

        
    # def get_id_Invoice(self, inv_merge):
    #     db_data = Invoices.query.filter(Invoices.inv_merge == inv_merge).first()
    #     invoice_id = db_data.id

    #     return invoice_id


    # def fill_in_inv_date(self):
    #     period_request = db.execute(select(Invoices.Invoice_Date, Invoices.KSSS_prod, Invoices.KSSS_cust)).all()
    #     inv_date = pd.DataFrame(period_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Brand, Products.Segment, Products.Product_group)).all()
    #     prod_data = pd.DataFrame(prod_request)

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()

    #     if inv_date.empty == True or prod_data.empty == True:
    #         self.ui.line_inv_year.addItem('-')
    #         self.ui.line_inv_qtr.addItem('-')
    #         self.ui.line_inv_mnth.addItem('-')
            
    #     else:
    #         inv_date = pd.merge(inv_date, prod_data, how='left', on='KSSS_prod')
    #         inv_date = inv_date.drop_duplicates(subset='KSSS_prod')
    #         inv_date['year'] = pd.DatetimeIndex(inv_date['Invoice_Date']).year
    #         inv_date['mnth'] = pd.DatetimeIndex(inv_date['Invoice_Date']).month
    #         inv_date['qtr'] = inv_date.apply(self.check_Quarter, axis=1)
        
    #         if Brand == '-' and Product_Segment == '-' and Product_group == '-':
    #             df_year = inv_date[['year']]
    #             df_qtr = inv_date[['qtr']]
    #             df_mnth = inv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_inv_year.addItems(df_year_list)
    #             self.ui.line_inv_qtr.addItems(df_qtr_list)
    #             self.ui.line_inv_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment == '-' and Product_group == '-':
    #             inv_date = [['year', 'qtr', 'mnth', 'Brand']]
    #             inv_date = inv_date[(inv_date['Brand'] == Brand)]
    #             df_year = inv_date[['year']]
    #             df_qtr = inv_date[['qtr']]
    #             df_mnth = inv_date[['mnth']]
                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_inv_year.addItems(df_year_list)
    #             self.ui.line_inv_qtr.addItems(df_qtr_list)
    #             self.ui.line_inv_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group == '-':
    #             inv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             inv_date = inv_date[(inv_date['Brand'] == Brand)]
    #             inv_date = inv_date[(inv_date['Segment'] == Product_Segment)]
    #             df_year = inv_date[['year']]
    #             df_qtr = inv_date[['qtr']]
    #             df_mnth = inv_date[['mnth']]
                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_inv_year.addItems(df_year_list)
    #             self.ui.line_inv_qtr.addItems(df_qtr_list)
    #             self.ui.line_inv_mnth.addItems(df_mnth_list)
            
    #         elif Brand == '-' and Product_Segment != '-' and Product_group == '-':
    #             inv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             inv_date = inv_date[(inv_date['Segment'] == Product_Segment)]
    #             df_year = inv_date[['year']]
    #             df_qtr = inv_date[['qtr']]
    #             df_mnth = inv_date[['mnth']]
                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_inv_year.addItems(df_year_list)
    #             self.ui.line_inv_qtr.addItems(df_qtr_list)
    #             self.ui.line_inv_mnth.addItems(df_mnth_list)
            
    #         elif Brand != '-' and Product_Segment == '-' and Product_group != '-':
    #             inv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             inv_date = inv_date[(inv_date['Brand'] == Brand)]
    #             inv_date = inv_date[(inv_date['Product_group'] == Product_group)]
    #             df_year = inv_date[['year']]
    #             df_qtr = inv_date[['qtr']]
    #             df_mnth = inv_date[['mnth']]
                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_inv_year.addItems(df_year_list)
    #             self.ui.line_inv_qtr.addItems(df_qtr_list)
    #             self.ui.line_inv_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group != '-':
    #             inv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             inv_date = inv_date[(inv_date['Brand'] == Brand)]
    #             inv_date = inv_date[(inv_date['Segment'] == Product_Segment)]
    #             inv_date = inv_date[(inv_date['Product_group'] == Product_group)]
    #             df_year = inv_date[['year']]
    #             df_qtr = inv_date[['qtr']]
    #             df_mnth = inv_date[['mnth']]
                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_inv_year.addItems(df_year_list)
    #             self.ui.line_inv_qtr.addItems(df_qtr_list)
    #             self.ui.line_inv_mnth.addItems(df_mnth_list)
                
        
    # def fill_in_del_date(self):      
    #     period_request = db.execute(select(Invoices.Delivery_Date, Invoices.KSSS_prod, Invoices.KSSS_cust)).all()
    #     deliv_date = pd.DataFrame(period_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Brand, Products.Segment, Products.Product_group)).all()
    #     prod_data = pd.DataFrame(prod_request)

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     i_year = self.ui.line_inv_year.currentText()
    #     i_qtr = self.ui.line_inv_qtr.currentText()
    #     i_mnth = self.ui.line_inv_mnth.currentText()

    #     if deliv_date.empty == True or prod_data.empty == True:
    #         self.ui.line_del_year.addItem('-')
    #         self.ui.line_del_qtr.addItem('-')
    #         self.ui.line_del_mnth.addItem('-')
            
    #     elif i_year != '-' or i_qtr != '-' or i_mnth != '-':
    #         self.ui.line_del_year.addItem('-')
    #         self.ui.line_del_qtr.addItem('-')
    #         self.ui.line_del_mnth.addItem('-')
                 
    #     else:
    #         deliv_date = pd.merge(deliv_date, prod_data, how='left', on='KSSS_prod')
    #         deliv_date = deliv_date.drop_duplicates(subset='KSSS_prod')
    #         deliv_date['year'] = pd.DatetimeIndex(deliv_date['Delivery_Date']).year
    #         deliv_date['mnth'] = pd.DatetimeIndex(deliv_date['Delivery_Date']).month
    #         deliv_date['qtr'] = deliv_date.apply(self.check_Quarter, axis=1)

    #         if Brand == '-' and Product_Segment == '-' and Product_group == '-':
    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment == '-' and Product_group == '-':
    #             deliv_date = [['year', 'qtr', 'mnth', 'Brand']]
    #             deliv_date = deliv_date[(deliv_date['Brand'] == Brand)]

    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group == '-':
    #             deliv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             deliv_date = deliv_date[(deliv_date['Brand'] == Brand)]
    #             deliv_date = deliv_date[(deliv_date['Segment'] == Product_Segment)]

    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
            
    #         elif Brand == '-' and Product_Segment != '-' and Product_group == '-':
    #             deliv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             deliv_date = deliv_date[(deliv_date['Segment'] == Product_Segment)]

    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
            
    #         elif Brand != '-' and Product_Segment == '-' and Product_group != '-':
    #             deliv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             deliv_date = deliv_date[(deliv_date['Brand'] == Brand)]
    #             deliv_date = deliv_date[(deliv_date['Product_group'] == Product_group)]

    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group != '-':
    #             deliv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             deliv_date = deliv_date[(deliv_date['Brand'] == Brand)]
    #             deliv_date = deliv_date[(deliv_date['Segment'] == Product_Segment)]
    #             deliv_date = deliv_date[(deliv_date['Product_group'] == Product_group)]

    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]

    #             df_year = df_year.drop_duplicates(subset='year')
    #             df_qtr = df_qtr.drop_duplicates(subset='qtr')
    #             df_mnth = df_mnth.drop_duplicates(subset='mnth')
    #             df_year = df_year.sort_values(by='year')
    #             df_qtr = df_qtr.sort_values(by='qtr')
    #             df_mnth = df_mnth.sort_values(by='mnth')
                                
    #             df_year['year'] = df_year['year'].astype(str)
    #             df_qtr['qtr'] = df_qtr['qtr'].astype(str)
    #             df_mnth['mnth'] = df_mnth['mnth'].astype(str)
    #             df_mnth['mnth'] = df_mnth.apply(self.chng_nmth_formate, axis=1)
                
    #             df_year_list = df_year['year'].astype(str).tolist()
    #             df_qtr_list = df_qtr['qtr'].tolist()
    #             df_mnth_list = df_mnth['mnth'].tolist()
    #             df_year_list.insert(0, '-')
    #             df_qtr_list.insert(0, '-')
    #             df_mnth_list.insert(0, '-')
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
      
            
    # def fill_in_prod_group(self):      
    #     group_request = db.execute(select(Invoices.KSSS_prod)).all()
    #     group_data = pd.DataFrame(group_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Brand, Products.Segment, Products.Product_group)).all()
    #     prod_data = pd.DataFrame(prod_request)
        
    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
        
    #     if group_data.empty == True or prod_data.empty == True:
    #         self.ui.line_pr_group.addItem('-')
        
    #     else:
    #         group_data = pd.merge(group_data, prod_data, how='left', on='KSSS_prod')
    #         group_data = group_data[(group_data['Brand'] != '-')]
            
    #         if Brand == '-' and Product_Segment == '-':
    #             group_data = group_data[['Product_group']]
    #             group_data = group_data.drop_duplicates(subset='Product_group')
    #             group_data = group_data.sort_values(by='Product_group')
    #             group_data_list = group_data['Product_group'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    #         elif Brand != '-' and Product_Segment == '-':
    #             group_data = group_data[['Product_group', 'Brand']]
    #             group_data = group_data[(group_data['Brand'] == Brand)]
    #             group_data = group_data.drop_duplicates(subset='Product_group')
    #             group_data = group_data.sort_values(by='Product_group')
    #             group_data_list = group_data['Product_group'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    #         elif Brand != '-' and Product_Segment != '-':
    #             group_data = group_data[['Product_group', 'Brand', 'Segment']]
    #             group_data = group_data[(group_data['Brand'] == Brand)]
    #             group_data = group_data[(group_data['Segment'] == Product_Segment)]
    #             group_data = group_data.drop_duplicates(subset='Product_group')
    #             group_data = group_data.sort_values(by='Product_group')
    #             group_data_list = group_data['Product_group'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    #         elif Brand == '-' and Product_Segment != '-':
    #             group_data = group_data[['Product_group', 'Segment']]
    #             group_data = group_data[(group_data['Segment'] == Product_Segment)]
    #             group_data = group_data.drop_duplicates(subset='Product_group')
    #             group_data = group_data.sort_values(by='Product_group')
    #             group_data_list = group_data['Product_group'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)
        
    
    # def fill_in_prod_segment(self):
    #     self.ui.line_segment.addItem('-')
        
    #     group_request = db.execute(select(Invoices.KSSS_prod)).all()
    #     group_data = pd.DataFrame(group_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Brand, Products.Segment, Products.Product_group)).all()
    #     prod_data = pd.DataFrame(prod_request)
        
    #     Brand = self.ui.line_brand.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     if group_data.empty == True or prod_data.empty == True:
    #         self.ui.line_pr_group.addItem('-')
        
    #     else:
    #         group_data = pd.merge(group_data, prod_data, how='left', on='KSSS_prod')
            
    #         if Brand == '-' and Product_group == '-':
    #             group_data = group_data[['Segment']]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    #         elif Brand != '-' and Product_group == '-':
    #             group_data = group_data[['Segment', 'Brand']]
    #             group_data = group_data[(group_data['Brand'] == Brand)]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    #         elif Brand != '-' and Product_group != '-':
    #             group_data = group_data[['Segment', 'Brand', 'Segment']]
    #             group_data = group_data[(group_data['Brand'] == Brand)]
    #             group_data = group_data[(group_data['Product_group'] == Product_group)]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    #         elif Brand == '-' and Product_group != '-':
    #             group_data = group_data[['Product_group', 'Segment']]
    #             group_data = group_data[(group_data['Product_group'] == Product_group)]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_pr_group.addItems(group_data_list)

    
    # def dowload_Invoices(self):
    #     savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Invoices.xlsx', 'Excel Workbook (*.xlsx)')
        
    #     inv_request = db.execute(select(Invoices.Account_doc, Invoices.Stock, Invoices.Plant, Invoices.Invoice_Date, 
    #                                                             Invoices.KSSS_cust, Invoices.Customer_Name, Invoices.Contract_N, Invoices.KSSS_prod, 
    #                                                             Invoices.Delivery_doc, Invoices.Account_doc2, Invoices.Inv_type, Invoices.Creation_Date, 
    #                                                             Invoices.Document_Date, Invoices.Transaction_Date, Invoices.Batch, Invoices.Delivery_Date, 
    #                                                             Invoices.Date_PPS, Invoices.Volume, Invoices.EA, Invoices.Price, Invoices.Curr)).all()
    #     inv_data = pd.DataFrame(inv_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Product_Name, Products.Pack, Products.Pack_group, 
    #                                                             Products.Brand, Products.Production, Products.Product_group, Products.Segment, 
    #                                                             Products.LoB, Products.BO_type, Products.Pack_group2, Products.Production_type)).all()
    #     prod_data = pd.DataFrame(prod_request)
        
    #     cust_request = db.execute(select(Customers.KSSS_cust, Customers.Customer_Name, Customers.merge, Customers.Cust_type, 
    #                                                             Customers.AM, Customers.STL, Customers.SM)).all()
    #     cust_data = pd.DataFrame(cust_request)
        
    #     i_year = self.ui.line_inv_year.currentText()
    #     i_qtr = self.ui.line_inv_qtr.currentText()
    #     i_mnth = self.ui.line_inv_mnth.currentText()
        
    #     d_year = self.ui.line_del_year.currentText()
    #     d_qtr = self.ui.line_del_qtr.currentText()
    #     d_mnth = self.ui.line_del_mnth.currentText()
        
    #     Brand = self.ui.line_brand.currentText()
    #     Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     KSSS_Cust = self.ui.line_cust_ksss.text()
        
                
    #     if inv_data.empty == True:
    #         msg = QMessageBox()
    #         msg.setText('There is no Invoices data in Database')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Critical)
    #         x = msg.exec_()
            
    #     else:
    #         cust_data['KSSS_cust'] = cust_data['KSSS_cust'].astype(int)
    #         cust_data['merge'] = cust_data['merge'].astype(str)
            
    #         inv_data['KSSS_cust'] = inv_data['KSSS_cust'].astype(int)
    #         inv_data['KSSS_prod'] = inv_data['KSSS_prod'].astype(int)
    #         inv_data['Price'] = inv_data['Price'].astype(float)
    #         inv_data['Volume'] = inv_data['Volume'].astype(float)
            
    #         inv_data['i_year'] = pd.DatetimeIndex(inv_data['Invoice_Date']).year
    #         inv_data['i_mnth'] = pd.DatetimeIndex(inv_data['Invoice_Date']).month
    #         inv_data['i_qtr'] = inv_data.apply(self.check_i_Quarter, axis=1)
            
    #         inv_data['o_year'] = pd.DatetimeIndex(inv_data['Delivery_Date']).year
    #         inv_data['o_mnth'] = pd.DatetimeIndex(inv_data['Delivery_Date']).month
    #         inv_data['o_qtr'] = inv_data.apply(self.check_d_Quarter, axis=1)
            
    #         inv_data = pd.merge(inv_data, prod_data, how='left', on='KSSS_prod')
    #         inv_data['LoB'] = inv_data.apply(self.check_prod_LoB, axis=1)
            
    #         cust_df = cust_data[['KSSS_cust', 'Cust_type']]
    #         cust_df = cust_df.drop_duplicates(subset='KSSS_cust')
            
    #         inv_data = pd.merge(inv_data, cust_df, how='left', on='KSSS_cust')
    #         inv_data['Cust_type'] = inv_data['Cust_type'].fillna('other_LLK')
    #         inv_data['Cust_type'] = inv_data.apply(self.check_Cust_type, axis=1)
            
    #         cust_df1 = cust_data[['merge', 'AM', 'STL', 'SM']]
    #         cust_df2 = cust_data[['KSSS_cust', 'AM', 'STL', 'SM']]
            
    #         inv_data['merge'] = inv_data['KSSS_cust'].astype(str) + inv_data['LoB']
            
    #         inv_data1 = pd.merge(inv_data, cust_df1, how='left', on='merge')
    #         inv_data1['AM'] = inv_data1['AM'].fillna('-')
    #         inv_data1['STL'] = inv_data1['STL'].fillna('-')
    #         inv_data1['SM'] = inv_data1['SM'].fillna('-')
    #         inv_data1 = inv_data1[(inv_data1['AM'] != '-')]
            
    #         inv_data2 = pd.merge(inv_data, cust_df2, how='left', on='KSSS_cust')
    #         inv_data2['AM'] = inv_data2['AM'].fillna('-')
    #         inv_data2['STL'] = inv_data2['STL'].fillna('-')
    #         inv_data2['SM'] = inv_data2['SM'].fillna('-')
            
    #         frames = [inv_data1, inv_data2]
    #         inv_data = pd.concat(frames)
            
    #         inv_data = inv_data.drop(['merge'], axis=1)
            
    #         inv_data_cust = pd.DataFrame()
            
    #         if self.ui.check_teb_dealer.isChecked() == True:
    #             t_deal = inv_data[(inv_data['Cust_type'] == 'Dealer_TEBOIL')]
    #             frame2 = [inv_data_cust, t_deal]
    #             inv_data_cust = pd.concat(frame2)
                
    #         if self.ui.check_teb_direct.isChecked() == True:
    #             t_dir = inv_data[(inv_data['Cust_type'] == 'Direct_TEBOIL')]
    #             frame2 = [inv_data_cust, t_dir]
    #             inv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_teb_fws.isChecked() == True:
    #             t_fws = inv_data[(inv_data['Cust_type'] == 'FWS_TEBOIL')]
    #             frame2 = [inv_data_cust, t_fws]
    #             inv_data_cust = pd.concat(frame2)
                        
    #         if self.ui.check_teb_market.isChecked() == True:
    #             t_mp = inv_data[(inv_data['Cust_type'] == 'MarketPlace_TEBOIL')]
    #             frame2 = [inv_data_cust, t_mp]
    #             inv_data_cust = pd.concat(frame2)

    #         if self.ui.check_luk_dealer.isChecked() == True:
    #             l_deal = inv_data[(inv_data['Cust_type'] == 'Dealer_LLK')]
    #             frame2 = [inv_data_cust, l_deal]
    #             inv_data_cust = pd.concat(frame2)

    #         if self.ui.check_luk_direct.isChecked() == True:
    #             l_dir = inv_data[(inv_data['Cust_type'] == 'Direct_LLK')]
    #             frame2 = [inv_data_cust, l_dir]
    #             inv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_fws.isChecked() == True:
    #             l_fws = inv_data[(inv_data['Cust_type'] == 'FWS_LLK')]
    #             frame2 = [inv_data_cust, l_fws]
    #             inv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_market.isChecked() == True:
    #             l_mp = inv_data[(inv_data['Cust_type'] == 'MarketPlace_LLK')]
    #             frame2 = [inv_data_cust, l_mp]
    #             inv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_other.isChecked() == True:
    #             l_oth = inv_data[(inv_data['Cust_type'] == 'other_LLK')]
    #             frame2 = [inv_data_cust, l_oth]
    #             inv_data_cust = pd.concat(frame2)
                 
    #         if inv_data_cust.empty == True:
    #             inv_data
    #         else:
    #             inv_data = inv_data_cust
            
    #         #check Invoice Date
    #         if i_year != '-' or i_qtr != '-' or i_mnth != '-':
    #             msg = QMessageBox()
    #             msg.setText('Сhoose either Delivery date or Invoice date')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 10pt  \"Segoe UI\";"
    #                             "color: #4b0082;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
            
    #         elif d_year == '-' and d_qtr == '-' and d_mnth == '-':
    #             inv_data
    #         elif d_year != '-' and d_qtr == '-' and d_mnth == '-':
    #             d_year = int(d_year)
    #             inv_data = inv_data[(inv_data['d_year'] == d_year)]
    #         elif d_year != '-' and d_qtr != '-' and d_mnth == '-':
    #             d_year = int(d_year)
    #             inv_data = inv_data[(inv_data['d_year'] == d_year)]
    #             inv_data = inv_data[(inv_data['d_qtr'] == d_qtr)]
    #         elif d_year != '-' and d_mnth != '-':
    #             d_year = int(d_year)
    #             d_mnth = int(d_mnth)
    #             inv_data = inv_data[(inv_data['d_year'] == d_year)]
    #             inv_data = inv_data[(inv_data['d_mnth'] == d_mnth)]
    #         elif d_year == '-' and d_qtr != '-' and d_mnth != '-':
    #             d_mnth = int(d_mnth)
    #             inv_data = inv_data[(inv_data['d_qtr'] == d_qtr)]
    #             inv_data = inv_data[(inv_data['d_mnth'] == d_mnth)]
    #         elif d_year == '-' and d_qtr == '-' and d_mnth == '-':
    #             d_mnth = int(d_mnth)
    #             inv_data = inv_data[(inv_data['d_mnth'] == d_mnth)]

    #         #check Delivery Date
    #         elif d_year != '-' or d_qtr != '-' or d_mnth != '-':
    #             msg = QMessageBox()
    #             msg.setText('Сhoose either Delivery date or Invoice date')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 10pt  \"Segoe UI\";"
    #                             "color: #4b0082;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #         elif i_year == '-' and i_qtr == '-' and i_mnth == '-':
    #             inv_data
    #         elif i_year != '-' and i_qtr == '-' and i_mnth == '-':
    #             i_year = int(i_year)
    #             inv_data = inv_data[(inv_data['i_year'] == i_year)]
    #         elif i_year != '-' and i_qtr != '-' and i_mnth == '-':
    #             i_year = int(i_year)
    #             inv_data = inv_data[(inv_data['i_year'] == i_year)]
    #             inv_data = inv_data[(inv_data['i_qtr'] == i_qtr)]
    #         elif i_year != '-' and i_mnth != '-':
    #             i_year = int(i_year)
    #             i_mnth = int(i_mnth)
    #             inv_data = inv_data[(inv_data['i_year'] == i_year)]
    #             inv_data = inv_data[(inv_data['i_mnth'] == i_mnth)]
    #         elif i_year == '-' and i_qtr != '-' and i_mnth != '-':
    #             i_mnth = int(i_mnth)
    #             inv_data = inv_data[(inv_data['i_qtr'] == i_qtr)]
    #             inv_data = inv_data[(inv_data['i_mnth'] == i_mnth)]
    #         elif i_year == '-' and i_qtr == '-' and i_mnth != '-':
    #             i_mnth = int(i_mnth)
    #             inv_data = inv_data[(inv_data['i_mnth'] == i_mnth)]
            
      
    #         elif Brand == '-' and Segment == '-' and Product_group == '-':
    #             inv_data
    #         elif Brand != '-' and Segment == '-' and Product_group == '-':
    #             inv_data = inv_data[(inv_data['Brand'] == Brand)]
    #         elif Brand != '-' and Segment != '-' and Product_group == '-':
    #             inv_data = inv_data[(inv_data['Brand'] == Brand)]
    #             inv_data = inv_data[(inv_data['Segment'] == Segment)]
    #         elif Brand != '-' and Segment != '-' and Product_group != '-':
    #             inv_data = inv_data[(inv_data['Brand'] == Brand)]
    #             inv_data = inv_data[(inv_data['Segment'] == Segment)]
    #             inv_data = inv_data[(inv_data['Product_group'] == Product_group)]
    #         elif Brand != '-' and Segment == '-' and Product_group != '-':
    #             inv_data = inv_data[(inv_data['Brand'] == Brand)]
    #             inv_data = inv_data[(inv_data['Product_group'] == Product_group)]
    #         elif Brand == '-' and Segment == '-' and Product_group != '-':
    #             inv_data = inv_data[(inv_data['Product_group'] == Product_group)]
            
    #         if KSSS_Cust != '':
    #             KSSS_Cust = int(KSSS_Cust)
    #             inv_data = inv_data[(inv_data['KSSS_Cust'] == KSSS_Cust)]


    #     inv_data['i_year'] = inv_data.drop(['i_year'], axis=1)
    #     inv_data['i_qtr'] = inv_data.drop(['i_qtr'], axis=1)
    #     inv_data['i_mnth'] = inv_data.drop(['i_mnth'], axis=1)
        
    #     inv_data['d_year'] = inv_data.drop(['d_year'], axis=1)
    #     inv_data['d_qtr'] = inv_data.drop(['d_qtr'], axis=1)
    #     inv_data['d_mnth'] = inv_data.drop(['d_mnth'], axis=1)
        

    #     inv_data.to_excel(savePath[0], index=False)

    #     msg = QMessageBox()
    #     msg.setText('Report was saved successfully')
    #     msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                     "font: 12pt  \"Segoe UI\";"
    #                     "color: #4b0082;\n"
    #                     " ")
    #     msg.setIcon(QMessageBox.Information)
    #     x = msg.exec_()
            
    
    # def check_Cust_type(self, row):
    #     if row['Brand'] == 'TEBOIL' or row['Brand'] == 'Shell':
    #         return row['Cust_type']
    #     else:
    #         if row['Brand'] == 'Лукойл' or row['Brand'] == 'GPO':
    #             if row['Cust_type'] == 'Dealer_TEBOIL':
    #                 return 'Dealer_LLK'
    #             elif row['Cust_type'] == 'Dir_TEBOIL':
    #                 return 'Dir_LLK'
    #             elif row['Cust_type'] == 'FWS_TEBOIL':
    #                 return 'FWS_LLK'
    #         else:
    #             return 'other_LLK'
        
        
    # def check_Quarter(self, row):
    #     if row['mnth'] >= 1 and row['mnth'] <= 3:
    #         return '1 кв.'
    #     elif row['mnth'] >= 4 and row['mnth'] <= 6:
    #         return '2 кв.'
    #     elif row['mnth'] >= 7 and row['mnth'] <= 9:
    #         return '3 кв.'
    #     elif row['mnth'] >= 10 and row['mnth'] <= 12:
    #         return '4 кв.'
 
 
    # def check_i_Quarter(self, row):
    #     if row['i_mnth'] >= 1 and row['i_mnth'] <= 3:
    #         return '1 кв.'
    #     elif row['i_mnth'] >= 4 and row['i_mnth'] <= 6:
    #         return '2 кв.'
    #     elif row['i_mnth'] >= 7 and row['i_mnth'] <= 9:
    #         return '3 кв.'
    #     elif row['i_mnth'] >= 10 and row['i_mnth'] <= 12:
    #         return '4 кв.'
        
        
    # def check_d_Quarter(self, row):
    #     if row['d_mnth'] >= 1 and row['d_mnth'] <= 3:
    #         return '1 кв.'
    #     elif row['d_mnth'] >= 4 and row['d_mnth'] <= 6:
    #         return '2 кв.'
    #     elif row['d_mnth'] >= 7 and row['d_mnth'] <= 9:
    #         return '3 кв.'
    #     elif row['d_mnth'] >= 10 and row['d_mnth'] <= 12:
    #         return '4 кв.'       
    
    
    # def check_prod_LoB(self, row):
    #     if row['LoB'] == 'B2B/B2C':
    #         return 'B2B'
    #     else:
    #         return row['LoB']
        

    # def chng_nmth_formate(self, row):
    #     if row['mnth'] == '1':
    #         return row['mnth'].replace('1','01')
    #     elif row['mnth'] == '2':
    #         return row['mnth'].replace('2','02')
    #     elif row['mnth'] == '3':
    #         return row['mnth'].replace('3','03')
    #     elif row['mnth'] == '4':
    #         return row['mnth'].replace('4','04')
    #     elif row['mnth'] == '5':
    #         return row['mnth'].replace('5','05')
    #     elif row['mnth'] == '6':
    #         return row['mnth'].replace('6','06')
    #     elif row['mnth'] == '7':
    #         return row['mnth'].replace('7','07')
    #     elif row['mnth'] == '8':
    #         return row['mnth'].replace('8','08')
    #     elif row['mnth'] == '9':
    #         return row['mnth'].replace('9','09')
    #     else:
    #         return row['mnth']


    # def get_id_Invoice(self, inv_merge):
    #     db_data = Invoices.query.filter(Invoices.inv_merge == inv_merge).first()
    #     invoice_id = db_data.id

    #     return invoice_id


    # def check_Price(self, row):
    #     if row['ord_Price'] == row['inv_Price']:
    #         return row['ord_Price']
    #     elif row['inv_Price'] == 0:
    #         return row['ord_Price']
    #     else:
    #         return row['inv_Price']


    # def check_Curr(self, row):
    #     if row['ord_Curr'] == row['inv_Curr']:
    #         return row['inv_Curr']
    #     elif row['inv_Curr'] == 0:
    #         return row['ord_Curr']
    #     else:
    #         return row['inv_Curr']








