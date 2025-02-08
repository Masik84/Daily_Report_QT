from datetime import datetime

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db, engine
# from models import Brands, Contracts, Customers_ALL, Delivery, Orders, Packs, Products, Stock
from wind.pages.delivery_ui import Ui_Form as Del_Form
from wind.pages.report_cols_ui import Ui_Form as Cols_Form


class Rep_Delivery(QWidget):
    def __init__(self):
        super(Rep_Delivery, self).__init__()
        self.ui = Del_Form()
        self.ui.setupUi(self)
        
        # self.fill_in_prod_group()
        # self.fill_in_del_date()
        # self.fill_in_ord_date()
        
        # self.ui.line_brand.currentTextChanged.connect(self.fill_in_prod_group)
        # self.ui.line_segment.currentTextChanged.connect(self.fill_in_prod_group)
        
        
        self.ui.btn_select_cols.setToolTip('выбери колонки для отчета')
        self.ui.btn_select_cols.clicked.connect(self.go_to_Select_Cols)
        
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        # self.ui.btn_download.clicked.connect(self.dowload_Delivery)
        
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
            self.ui.label_delivery_File.setText(get_file[0])
 
            
    def upload_data(self, deliv_file_xls):
        deliv_file_xls = self.ui.label_delivery_File.text()
        if deliv_file_xls == 'File Path' or deliv_file_xls == 'Database was updated successfully':
            msg = QMessageBox()
            msg.setWindowTitle('Programm Error')
            msg.setText('!!! Please choose the file with Delivery Data !!!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                                            "font: 12pt  \"Segoe UI\";"
                                            "color: #ff0000;\n"
                                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            deliv_data = self.read_deliv_file(deliv_file_xls)
            self.update_Delivery(deliv_data)

            msg = QMessageBox()
            msg.setText('Database was updated successfully')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Segoe UI\";"
                            "color: #4b0082;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            self.ui.label_delivery_File.setText('File Path')
 
            
    # def read_deliv_file(self, deliv_file_xls):
    #     deliv_df = pd.read_excel(deliv_file_xls, sheet_name='Лист1')
    #     deliv_df = deliv_df[['Реестр.№дог', 'ТипД', 'ПОтг', 'КССС Пок.', 'Имя Покупателя', 
    #                                     'Заказ Покупателя', 'Д/зкзПок.', 'ЕжмР', 'КСССмат', 'ДатаЦены(Р)', 
    #                                     'Поставка', 'Накладная', 'ДатаОтгр.', 'БУ-документ', 
    #                                     'Номер счета-фактуры:', 'Фактура', 'Дата фактуры', 
    #                                     'ПартияПоставки', 'Дата партии', 'Условие отгрузки', 'ИнкТм', 
    #                                     'НСН', 'Пункт отгрузки', 'КССС ГрП.', 'Имя Грузополучателя', 'Тип договора', 'ЦенаЕжмР(безНДС)', 
    #                                     'Влт(Р)', 'за(Р)', 'ЦенаФактуры(безНДС)', 'Влт(Ф)', 'за(Ф)', 'Объем поставки']]

    #     deliv_df.rename(columns={
    #                                                 'Реестр.№дог' : 'Contract_N',
    #                                                 'ТипД' : 'CType',
    #                                                 'ПОтг' : 'Stock',
    #                                                 'КССС Пок.' : 'KSSS_cust',
    #                                                 'Имя Покупателя' : 'Customer_Name',
    #                                                 'Заказ Покупателя' : 'ord_CRM',
    #                                                 'Д/зкзПок.' : 'ord_Date',
    #                                                 'ЕжмР' : 'ord_SAP',
    #                                                 'КСССмат' : 'KSSS_prod',
    #                                                 'ДатаЦены(Р)' : 'Price_Date',
    #                                                 'Поставка' : 'Supply_doc',
    #                                                 'Накладная' : 'Delivery_doc',
    #                                                 'ДатаОтгр.' : 'Delivery_Date',
    #                                                 'БУ-документ' : 'Account_doc',
    #                                                 'Номер счета-фактуры:' : 'Invoice',
    #                                                 'Фактура' : 'Account_doc2',
    #                                                 'Дата фактуры' : 'Invoice_Date',
    #                                                 'ПартияПоставки' : 'Batch',
    #                                                 'Дата партии' : 'Batch_Date',
    #                                                 'Условие отгрузки' : 'Delivery_type',
    #                                                 'ИнкТм' : 'InkTm',
    #                                                 'НСН' : 'Country',
    #                                                 'Пункт отгрузки' : 'Stock_Name',
    #                                                 'КССС ГрП.' : 'KSSS_Shipto',
    #                                                 'Имя Грузополучателя' : 'Shipto_Name',
    #                                                 'Тип договора' : 'Contract_type',
    #                                                 'ЦенаЕжмР(безНДС)' : 'ord_Price',
    #                                                 'Влт(Р)' : 'ord_Curr',
    #                                                 'за(Р)' : 'for_ord',
    #                                                 'ЦенаФактуры(безНДС)' : 'inv_Price',
    #                                                 'Влт(Ф)' : 'inv_Curr',
    #                                                 'за(Ф)' : 'for_inv',
    #                                                 'Объем поставки' : 'Volume'}, inplace = True)
        
    #     deliv_df = deliv_df[(deliv_df['Contract_type'] != 'Перемещение')]
    #     deliv_df = deliv_df[(deliv_df['Contract_type'] != 'Битумы')]
        
    #     deliv_df['KSSS_prod'] = deliv_df['KSSS_prod'].fillna('-')
    #     deliv_df = deliv_df.loc[~deliv_df['KSSS_prod'].str.contains(r'[^\d\.]')]
    #     deliv_df = deliv_df[(deliv_df['KSSS_prod'] != '-')]

    #     deliv_df['ord_CRM'] = deliv_df['ord_CRM'].fillna('-')
    #     deliv_df = deliv_df[(deliv_df['ord_CRM'] != '-')]

    #     deliv_df['Stock_Name'] = deliv_df['Stock_Name'].str.replace('"', '')
    #     deliv_df['Customer_Name'] = deliv_df['Customer_Name'].str.replace('"', '')
    #     deliv_df['Shipto_Name'] = deliv_df['Shipto_Name'].str.replace('"', '')


    #     deliv_df['Account_doc'] = deliv_df['Account_doc'].astype(str)
    #     deliv_df['Account_doc'] = deliv_df['Account_doc'].str[:-2]
    #     deliv_df['Account_doc2'] = deliv_df['Account_doc2'].astype(str)
    #     deliv_df['Account_doc2'] = deliv_df['Account_doc2'].str[:-2]

    #     deliv_df['Stock'] = deliv_df['Stock'].astype(str)
    #     deliv_df['Supply_doc'] = deliv_df['Supply_doc'].fillna('').astype(str)
    #     deliv_df['Delivery_doc'] = deliv_df['Delivery_doc'].fillna('').astype(str)
    #     deliv_df['Batch'] = deliv_df['Batch'].fillna('').astype(str)
    #     deliv_df['Invoice'] = deliv_df['Invoice'].fillna('').astype(str)
    #     deliv_df['ord_Curr'] = deliv_df['ord_Curr'].fillna('0').astype(str)
    #     deliv_df['inv_Curr'] = deliv_df['inv_Curr'].fillna('0').astype(str)

    #     deliv_df['KSSS_cust'] = deliv_df['KSSS_cust'].replace(np.nan, 0).astype(int)
    #     deliv_df['ord_SAP'] = deliv_df['ord_SAP'].replace(np.nan, 0).astype(int)
    #     deliv_df['KSSS_Shipto'] = deliv_df['KSSS_Shipto'].replace(np.nan, 0).astype(int)
    #     deliv_df['KSSS_prod'] = deliv_df['KSSS_prod'].astype(int)

    #     period = self.ui.rep_date.dateTime()
    #     period = period.toString('yyyy-MM-dd')
    #     period = datetime.strptime(period, '%Y-%m-%d')
    #     if period.day != 1:
    #         period = datetime(period.year, period.month, 1).strftime('%Y-%m-%d')
    #     else:
    #         period = period
            
    #     deliv_df.insert(0, 'Period', period)

    #     deliv_df['Period'] =pd.to_datetime(deliv_df['Period'], format='%Y-%m-%d')
    #     deliv_df['Period'] = pd.to_datetime(deliv_df['Period'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     deliv_df['ord_Date'] = pd.to_datetime(deliv_df['ord_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     deliv_df['Price_Date'] = pd.to_datetime(deliv_df['Price_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     deliv_df['Delivery_Date'] = pd.to_datetime(deliv_df['Delivery_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     deliv_df['Invoice_Date'] = pd.to_datetime(deliv_df['Invoice_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     deliv_df['Batch_Date'] = pd.to_datetime(deliv_df['Batch_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})

    #     reques = db.execute(select(Products.KSSS_prod, Products.Product_Name)).all()
    #     product_df = pd.DataFrame(reques)
    #     product_df['KSSS_prod'] = product_df['KSSS_prod'].astype(int)

    #     deliv_df = pd.merge(deliv_df, product_df, how='left', on='KSSS_prod')
        
    #     deliv_df['Product_Name'] = deliv_df['Product_Name'].fillna('-')
    #     deliv_df = deliv_df[(deliv_df.Product_Name != '-')]
    #     deliv_df = deliv_df.drop(['Product_Name'], axis = 1)

    #     deliv_df['del_merge'] = deliv_df['ord_SAP'].astype (str) + deliv_df['KSSS_prod'].astype (str) + deliv_df['Supply_doc'].astype (str) + deliv_df['Delivery_doc'].astype (str) + deliv_df['Batch'].astype (str)

    #     deliv_df['ord_Price'] = np.where(deliv_df['for_ord'] == 1, deliv_df['ord_Price'] * 1000, deliv_df['ord_Price'])
    #     deliv_df['inv_Price'] = np.where(deliv_df['for_inv'] == 1, deliv_df['inv_Price'] * 1000, deliv_df['inv_Price'])
        
    #     deliv_df['Price'] = deliv_df.apply(self.check_Price, axis=1)
    #     deliv_df.pop('ord_Price')
    #     deliv_df.pop('inv_Price')

    #     deliv_df['Curr'] = deliv_df.apply(self.check_Curr, axis=1)
    #     deliv_df.pop('for_ord')
    #     deliv_df.pop('for_inv')

    #     deliv_df['DocType'] = 'Delivery'

    #     deliv_df = deliv_df.groupby(['del_merge', 'DocType', 'Period', 'Contract_N', 'CType', 'Stock', 'KSSS_cust', 'Customer_Name', 
    #                                                     'ord_CRM', 'ord_Date', 'ord_SAP', 'KSSS_prod', 'Price_Date', 'Supply_doc', 'Delivery_doc', 
    #                                                     'Delivery_Date', 'Account_doc', 'Invoice', 'Account_doc2', 'Invoice_Date', 'Batch', 
    #                                                     'Batch_Date', 'Delivery_type', 'InkTm', 'Country', 'Stock_Name', 'KSSS_Shipto', 
    #                                                     'Shipto_Name', 'Contract_type', 'Price', 'Curr']).sum().reset_index()

    #     deliv_data = deliv_df.to_dict('records')

    #     return deliv_data


    # def update_Delivery(self, data):
    #     deliv_for_create = []
    #     deliv_for_update = []
    #     for row in data:
    #         deliv_exists = Delivery.query.filter(Delivery.del_merge == str(row['del_merge'])).count()
    #         if row['Invoice_Date'] == '':
    #             row['Invoice_Date'] = None
    #         else:
    #             row['Invoice_Date'] = row['Invoice_Date']

    #         if row['Batch_Date'] == '':
    #             row['Batch_Date'] = None
    #         else:
    #             row['Batch_Date'] = row['Batch_Date']

    #         if deliv_exists == 0:
    #             deliv_list = {'del_merge' : str(row['del_merge']),
    #                                 'DocType' : row['DocType'],
    #                                 'Period' : row['Period'],
    #                                 'Contract_N' : row['Contract_N'],
    #                                 'CType' : row['CType'],
    #                                 'Stock' : row['Stock'],
    #                                 'KSSS_cust' : row['KSSS_cust'],
    #                                 'Customer_Name' : row['Customer_Name'],
    #                                 'ord_CRM' : row['ord_CRM'],
    #                                 'ord_Date' : row['ord_Date'],
    #                                 'ord_SAP' : row['ord_SAP'],
    #                                 'KSSS_prod' : row['KSSS_prod'],
    #                                 'Price_Date' : row['Price_Date'],
    #                                 'Supply_doc' : row['Supply_doc'],
    #                                 'Delivery_doc' : row['Delivery_doc'],
    #                                 'Delivery_Date' : row['Delivery_Date'],
    #                                 'Account_doc' : row['Account_doc'],
    #                                 'Invoice' : row['Invoice'],
    #                                 'Account_doc2' : row['Account_doc2'],
    #                                 'Invoice_Date' : row['Invoice_Date'],
    #                                 'Batch' : row['Batch'],
    #                                 'Batch_Date' : row['Batch_Date'],
    #                                 'Delivery_type' : row['Delivery_type'],
    #                                 'InkTm' : row['InkTm'],
    #                                 'Country' : row['Country'],
    #                                 'Stock_Name' : row['Stock_Name'],
    #                                 'KSSS_Shipto' : row['KSSS_Shipto'],
    #                                 'Shipto_Name' : row['Shipto_Name'],
    #                                 'Contract_type' : row['Contract_type'],
    #                                 'Price' : row['Price'],
    #                                 'Curr' : row['Curr'],
    #                                 'Volume' : row['Volume']}
    #             deliv_for_create.append(deliv_list)

    #         elif deliv_exists > 0:
    #             deliv_list = {'id' : self.get_id_Delivery(row['del_merge']),
    #                                 'del_merge' : str(row['del_merge']),
    #                                 'DocType' : row['DocType'],
    #                                 'Period' : row['Period'],
    #                                 'Contract_N' : row['Contract_N'],
    #                                 'CType' : row['CType'],
    #                                 'Stock' : row['Stock'],
    #                                 'KSSS_cust' : row['KSSS_cust'],
    #                                 'Customer_Name' : row['Customer_Name'],
    #                                 'ord_CRM' : row['ord_CRM'],
    #                                 'ord_Date' : row['ord_Date'],
    #                                 'ord_SAP' : row['ord_SAP'],
    #                                 'KSSS_prod' : row['KSSS_prod'],
    #                                 'Price_Date' : row['Price_Date'],
    #                                 'Supply_doc' : row['Supply_doc'],
    #                                 'Delivery_doc' : row['Delivery_doc'],
    #                                 'Delivery_Date' : row['Delivery_Date'],
    #                                 'Account_doc' : row['Account_doc'],
    #                                 'Invoice' : row['Invoice'],
    #                                 'Account_doc2' : row['Account_doc2'],
    #                                 'Invoice_Date' : row['Invoice_Date'],
    #                                 'Batch' : row['Batch'],
    #                                 'Batch_Date' : row['Batch_Date'],
    #                                 'Delivery_type' : row['Delivery_type'],
    #                                 'InkTm' : row['InkTm'],
    #                                 'Country' : row['Country'],
    #                                 'Stock_Name' : row['Stock_Name'],
    #                                 'KSSS_Shipto' : row['KSSS_Shipto'],
    #                                 'Shipto_Name' : row['Shipto_Name'],
    #                                 'Contract_type' : row['Contract_type'],
    #                                 'Price' : row['Price'],
    #                                 'Curr' : row['Curr'],
    #                                 'Volume' : row['Volume']}
    #             deliv_for_update.append(deliv_list)
                
    #     db.bulk_insert_mappings(Delivery, deliv_for_create)
    #     db.bulk_update_mappings(Delivery, deliv_for_update)

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
        
        
    #     self.ui.line_del_year.clear()
    #     self.ui.line_del_qtr.clear()
    #     self.ui.line_del_mnth.clear()
        
    #     self.ui.line_ord_year.clear()
    #     self.ui.line_ord_qtr.clear()
    #     self.ui.line_ord_mnth.clear()
        
    #     self.ui.line_pr_group.clear()
        
    #     self.fill_in_prod_group()
    #     self.fill_in_del_date()
    #     self.fill_in_ord_date()
        
    #     return deliv_for_create


    # def get_id_Delivery(self, del_merge):
    #     db_data = Delivery.query.filter(Delivery.del_merge == del_merge).first()
    #     delivery_id = db_data.id

    #     return delivery_id


    # def get_all_Delivery_from_db(self):
    #     deliv_reques = db.query(Delivery)
    #     deliv_data = pd.read_sql_query(deliv_reques.statement, engine)
        
    #     order_request = db.execute(select(Orders.id, Orders.ord_merge, Orders.ord_CRM, Orders.ord_Date, Orders.ord_SAP,
    #                                 Orders.ord_Origin, Orders.ord_Orig_Date, Orders.Price_Date, Orders.PrTp)).all()
    #     order_data = pd.DataFrame(order_request)
        
    #     cust_reques = db.query(Customers_ALL, Contracts).join(Contracts
    #                                     ).with_entities(Customers_ALL.id, Customers_ALL.Customer_Name, Contracts.Contract_N)
    #     cust_data = pd.DataFrame(cust_reques)
        
    #     prod_reques = db.query(Products, Packs, Brands
    #                      ).join(Packs).join(Brands
    #                                         ).with_entities(Products.id, Products.KSSS_prod, Products.Product_Name, Products.Product_group,
    #                                                         Products.LoB, Products.Segment, Products.BO_type, Products.Production,
    #                                                         Products.Production_type, Packs.Pack, Packs.Pack_group,
    #                                                         Packs.Pack_group2, Packs.Pack_group3, Brands.Brand)
    #     prod_data = pd.DataFrame(prod_reques)
        
    #     stock_reques = db.query(Stock)
    #     stock_data = pd.read_sql_query(stock_reques.statement, engine)
    #     stock_data = stock_data[['id', 'Stock', 'Stock_Name']]

    #     deliv_data = pd.merge(deliv_data, cust_data, how='left', left_on='cust_id', right_on='id')
    #     deliv_data = pd.merge(deliv_data, prod_data, how='left', left_on='prod_id', right_on='id')
    #     deliv_data = deliv_data.drop(columns=['id_x', 'ord_merge', 'contr_id', 'cust_id', 'prod_id', 'id_y', 'id'])
    #     deliv_data = pd.merge(deliv_data, stock_data, how='left', left_on='stock_id', right_on='id')
    #     deliv_data = deliv_data.drop(columns=['stock_id', 'id'])
    #     deliv_data = pd.merge(deliv_data, order_data, how='left', left_on='order_id', right_on='id')
    #     deliv_data = deliv_data.fillna('')

    #     return order_data


    # def fill_in_del_date(self):
    #     period_request = db.execute(select(Delivery.Period, Delivery.KSSS_prod, Delivery.KSSS_cust)).all()
    #     deliv_date = pd.DataFrame(period_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Brand, Products.Segment, Products.Product_group)).all()
    #     prod_data = pd.DataFrame(prod_request)

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()

    #     if deliv_date.empty == True or prod_data.empty == True:
    #         self.ui.line_del_year.addItem('-')
    #         self.ui.line_del_qtr.addItem('-')
    #         self.ui.line_del_mnth.addItem('-')
            
    #     else:
    #         deliv_date = pd.merge(deliv_date, prod_data, how='left', on='KSSS_prod')
    #         deliv_date = deliv_date.drop_duplicates(subset='KSSS_prod')
    #         deliv_date['year'] = pd.DatetimeIndex(deliv_date['Period']).year
    #         deliv_date['mnth'] = pd.DatetimeIndex(deliv_date['Period']).month
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
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
            
    #         elif Brand == '-' and Product_Segment != '-' and Product_group == '-':
    #             deliv_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             deliv_date = deliv_date[(deliv_date['Segment'] == Product_Segment)]
    #             df_year = deliv_date[['year']]
    #             df_qtr = deliv_date[['qtr']]
    #             df_mnth = deliv_date[['mnth']]
                
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
    #             self.ui.line_del_year.addItems(df_year_list)
    #             self.ui.line_del_qtr.addItems(df_qtr_list)
    #             self.ui.line_del_mnth.addItems(df_mnth_list)
                
        
    # def fill_in_ord_date(self):      
    #     period_request = db.execute(select(Delivery.ord_Date, Delivery.KSSS_prod, Delivery.KSSS_cust)).all()
    #     order_date = pd.DataFrame(period_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Brand, Products.Segment, Products.Product_group)).all()
    #     prod_data = pd.DataFrame(prod_request)

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     d_year = self.ui.line_del_year.currentText()
    #     d_qtr = self.ui.line_del_qtr.currentText()
    #     d_mnth = self.ui.line_del_mnth.currentText()

    #     if order_date.empty == True or prod_data.empty == True:
    #         self.ui.line_ord_year.addItem('-')
    #         self.ui.line_ord_qtr.addItem('-')
    #         self.ui.line_ord_mnth.addItem('-')
            
    #     elif d_year != '-' or d_qtr != '-' or d_mnth != '-':
    #         self.ui.line_ord_year.addItem('-')
    #         self.ui.line_ord_qtr.addItem('-')
    #         self.ui.line_ord_mnth.addItem('-')
                 
    #     else:
    #         order_date = pd.merge(order_date, prod_data, how='left', on='KSSS_prod')
    #         order_date = order_date.drop_duplicates(subset='KSSS_prod')
    #         order_date['year'] = pd.DatetimeIndex(order_date['ord_Date']).year
    #         order_date['mnth'] = pd.DatetimeIndex(order_date['ord_Date']).month
    #         order_date['qtr'] = order_date.apply(self.check_Quarter, axis=1)

    #         if Brand == '-' and Product_Segment == '-' and Product_group == '-':
    #             df_year = order_date[['year']]
    #             df_qtr = order_date[['qtr']]
    #             df_mnth = order_date[['mnth']]

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
                
    #             self.ui.line_ord_year.addItems(df_year_list)
    #             self.ui.line_ord_qtr.addItems(df_qtr_list)
    #             self.ui.line_ord_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment == '-' and Product_group == '-':
    #             order_date = [['year', 'qtr', 'mnth', 'Brand']]
    #             order_date = order_date[(order_date['Brand'] == Brand)]

    #             df_year = order_date[['year']]
    #             df_qtr = order_date[['qtr']]
    #             df_mnth = order_date[['mnth']]

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
    #             self.ui.line_ord_year.addItems(df_year_list)
    #             self.ui.line_ord_qtr.addItems(df_qtr_list)
    #             self.ui.line_ord_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group == '-':
    #             order_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             order_date = order_date[(order_date['Brand'] == Brand)]
    #             order_date = order_date[(order_date['Segment'] == Product_Segment)]

    #             df_year = order_date[['year']]
    #             df_qtr = order_date[['qtr']]
    #             df_mnth = order_date[['mnth']]

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
    #             self.ui.line_ord_year.addItems(df_year_list)
    #             self.ui.line_ord_qtr.addItems(df_qtr_list)
    #             self.ui.line_ord_mnth.addItems(df_mnth_list)
            
    #         elif Brand == '-' and Product_Segment != '-' and Product_group == '-':
    #             order_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             order_date = order_date[(order_date['Segment'] == Product_Segment)]

    #             df_year = order_date[['year']]
    #             df_qtr = order_date[['qtr']]
    #             df_mnth = order_date[['mnth']]

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
    #             self.ui.line_ord_year.addItems(df_year_list)
    #             self.ui.line_ord_qtr.addItems(df_qtr_list)
    #             self.ui.line_ord_mnth.addItems(df_mnth_list)
            
    #         elif Brand != '-' and Product_Segment == '-' and Product_group != '-':
    #             order_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             order_date = order_date[(order_date['Brand'] == Brand)]
    #             order_date = order_date[(order_date['Product_group'] == Product_group)]

    #             df_year = order_date[['year']]
    #             df_qtr = order_date[['qtr']]
    #             df_mnth = order_date[['mnth']]

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
    #             self.ui.line_ord_year.addItems(df_year_list)
    #             self.ui.line_ord_qtr.addItems(df_qtr_list)
    #             self.ui.line_ord_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group != '-':
    #             order_date = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             order_date = order_date[(order_date['Brand'] == Brand)]
    #             order_date = order_date[(order_date['Segment'] == Product_Segment)]
    #             order_date = order_date[(order_date['Product_group'] == Product_group)]

    #             df_year = order_date[['year']]
    #             df_qtr = order_date[['qtr']]
    #             df_mnth = order_date[['mnth']]

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
    #             self.ui.line_ord_year.addItems(df_year_list)
    #             self.ui.line_ord_qtr.addItems(df_qtr_list)
    #             self.ui.line_ord_mnth.addItems(df_mnth_list)
      
            
    # def fill_in_prod_group(self):
    #     group_request = db.execute(select(Delivery.KSSS_prod)).all()
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
    #     group_request = db.execute(select(Delivery.KSSS_prod)).all()
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

    
    # def dowload_Delivery(self):
    #     savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Delivery.xlsx', 'Excel Workbook (*.xlsx)')
        
    #     deliv_request = db.execute(select(Delivery.Period, Delivery.Contract_N, Delivery.CType, Delivery.Stock, Delivery.KSSS_cust, 
    #                                                             Delivery.Customer_Name, Delivery.ord_CRM, Delivery.ord_Date, Delivery.ord_SAP, 
    #                                                             Delivery.KSSS_prod, Delivery.Price_Date, Delivery.Supply_doc, Delivery.Delivery_doc, 
    #                                                             Delivery.Delivery_Date, Delivery.Account_doc, Delivery.Invoice, Delivery.Account_doc2, 
    #                                                             Delivery.Invoice_Date, Delivery.Batch, Delivery.Batch_Date, Delivery.Delivery_type, 
    #                                                             Delivery.InkTm, Delivery.Country, Delivery.Pack_group2, Delivery.Stock_Name, 
    #                                                             Delivery.KSSS_Shipto, Delivery.Shipto_Name, Delivery.Contract_type, Delivery.Price, 
    #                                                             Delivery.Curr, Delivery.Volume)).all()
    #     deliv_data = pd.DataFrame(deliv_request)
        
    #     prod_request = db.execute(select(Products.KSSS_prod, Products.Product_Name, Products.Pack, Products.Pack_group, 
    #                                                             Products.Brand, Products.Production, Products.Product_group, Products.Segment, 
    #                                                             Products.LoB, Products.BO_type, Products.Pack_group2, Products.Production_type)).all()
    #     prod_data = pd.DataFrame(prod_request)
        
    #     cust_request = db.execute(select(Customers.KSSS_cust, Customers.Customer_Name, Customers.merge, Customers.Cust_type, 
    #                                                             Customers.AM, Customers.STL, Customers.SM)).all()
    #     cust_data = pd.DataFrame(cust_request)
        
    #     d_year = self.ui.line_del_year.currentText()
    #     d_qtr = self.ui.line_del_qtr.currentText()
    #     d_mnth = self.ui.line_del_mnth.currentText()
        
    #     o_year = self.ui.line_ord_year.currentText()
    #     o_qtr = self.ui.line_ord_qtr.currentText()
    #     o_mnth = self.ui.line_ord_mnth.currentText()
        
    #     Brand = self.ui.line_brand.currentText()
    #     Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     KSSS_Cust = self.ui.line_cust_ksss.text()
        
                
    #     if deliv_data.empty == True:
    #         msg = QMessageBox()
    #         msg.setText('There is no Delivery data in Database')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Critical)
    #         x = msg.exec_()
            
    #     else:
    #         cust_data['KSSS_cust'] = cust_data['KSSS_cust'].astype(int)
    #         cust_data['merge'] = cust_data['merge'].astype(str)
            
    #         deliv_data['KSSS_cust'] = deliv_data['KSSS_cust'].astype(int)
    #         deliv_data['KSSS_prod'] = deliv_data['KSSS_prod'].astype(int)
    #         deliv_data['KSSS_Shipto'] = deliv_data['KSSS_Shipto'].astype(int)
    #         deliv_data['Price'] = deliv_data['Price'].astype(float)
    #         deliv_data['Volume'] = deliv_data['Volume'].astype(float)
            
    #         deliv_data['d_year'] = pd.DatetimeIndex(deliv_data['Delivery_Date']).year
    #         deliv_data['d_mnth'] = pd.DatetimeIndex(deliv_data['Delivery_Date']).month
    #         deliv_data['d_qtr'] = deliv_data.apply(self.check_d_Quarter, axis=1)
            
    #         deliv_data['o_year'] = pd.DatetimeIndex(deliv_data['ord_Date']).year
    #         deliv_data['o_mnth'] = pd.DatetimeIndex(deliv_data['ord_Date']).month
    #         deliv_data['o_qtr'] = deliv_data.apply(self.check_o_Quarter, axis=1)
            
    #         deliv_data = pd.merge(deliv_data, prod_data, how='left', on='KSSS_prod')
    #         deliv_data['LoB'] = deliv_data.apply(self.check_prod_LoB, axis=1)
            
    #         cust_df = cust_data[['KSSS_cust', 'Cust_type']]
    #         cust_df = cust_df.drop_duplicates(subset='KSSS_cust')
            
    #         deliv_data = pd.merge(deliv_data, cust_df, how='left', on='KSSS_cust')
    #         deliv_data['Cust_type'] = deliv_data['Cust_type'].fillna('other_LLK')
    #         deliv_data['Cust_type'] = deliv_data.apply(self.check_Cust_type, axis=1)
            
    #         cust_df1 = cust_data[['merge', 'AM', 'STL', 'SM']]
    #         cust_df2 = cust_data[['KSSS_cust', 'AM', 'STL', 'SM']]
            
    #         deliv_data['merge'] = deliv_data['KSSS_cust'].astype(str) + deliv_data['LoB']
            
    #         deliv_data1 = pd.merge(deliv_data, cust_df1, how='left', on='merge')
    #         deliv_data1['AM'] = deliv_data1['AM'].fillna('-')
    #         deliv_data1['STL'] = deliv_data1['STL'].fillna('-')
    #         deliv_data1['SM'] = deliv_data1['SM'].fillna('-')
    #         deliv_data1 = deliv_data1[(deliv_data1['AM'] != '-')]
            
    #         deliv_data2 = pd.merge(deliv_data, cust_df2, how='left', on='KSSS_cust')
    #         deliv_data2['AM'] = deliv_data2['AM'].fillna('-')
    #         deliv_data2['STL'] = deliv_data2['STL'].fillna('-')
    #         deliv_data2['SM'] = deliv_data2['SM'].fillna('-')
            
    #         frames = [deliv_data1, deliv_data2]
    #         deliv_data = pd.concat(frames)
            
    #         deliv_data = deliv_data.drop(['merge'], axis=1)
            
    #         deliv_data_cust = pd.DataFrame()
            
    #         if self.ui.check_teb_dealer.isChecked() == True:
    #             t_deal = deliv_data[(deliv_data['Cust_type'] == 'Dealer_TEBOIL')]
    #             frame2 = [deliv_data_cust, t_deal]
    #             deliv_data_cust = pd.concat(frame2)
                
    #         if self.ui.check_teb_direct.isChecked() == True:
    #             t_dir = deliv_data[(deliv_data['Cust_type'] == 'Direct_TEBOIL')]
    #             frame2 = [deliv_data_cust, t_dir]
    #             deliv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_teb_fws.isChecked() == True:
    #             t_fws = deliv_data[(deliv_data['Cust_type'] == 'FWS_TEBOIL')]
    #             frame2 = [deliv_data_cust, t_fws]
    #             deliv_data_cust = pd.concat(frame2)
                        
    #         if self.ui.check_teb_market.isChecked() == True:
    #             t_mp = deliv_data[(deliv_data['Cust_type'] == 'MarketPlace_TEBOIL')]
    #             frame2 = [deliv_data_cust, t_mp]
    #             deliv_data_cust = pd.concat(frame2)

    #         if self.ui.check_luk_dealer.isChecked() == True:
    #             l_deal = deliv_data[(deliv_data['Cust_type'] == 'Dealer_LLK')]
    #             frame2 = [deliv_data_cust, l_deal]
    #             deliv_data_cust = pd.concat(frame2)

    #         if self.ui.check_luk_direct.isChecked() == True:
    #             l_dir = deliv_data[(deliv_data['Cust_type'] == 'Direct_LLK')]
    #             frame2 = [deliv_data_cust, l_dir]
    #             deliv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_fws.isChecked() == True:
    #             l_fws = deliv_data[(deliv_data['Cust_type'] == 'FWS_LLK')]
    #             frame2 = [deliv_data_cust, l_fws]
    #             deliv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_market.isChecked() == True:
    #             l_mp = deliv_data[(deliv_data['Cust_type'] == 'MarketPlace_LLK')]
    #             frame2 = [deliv_data_cust, l_mp]
    #             deliv_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_other.isChecked() == True:
    #             l_oth = deliv_data[(deliv_data['Cust_type'] == 'other_LLK')]
    #             frame2 = [deliv_data_cust, l_oth]
    #             deliv_data_cust = pd.concat(frame2)
                 
    #         if deliv_data_cust.empty == True:
    #             deliv_data
    #         else:
    #             deliv_data = deliv_data_cust
            
    #         #check Order Date
    #         if d_year != '-' or d_qtr != '-' or d_mnth != '-':
    #             msg = QMessageBox()
    #             msg.setText('Сhoose either Delivery date or Order date')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 10pt  \"Segoe UI\";"
    #                             "color: #4b0082;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
            
    #         elif o_year == '-' and o_qtr == '-' and o_mnth == '-':
    #             deliv_data
    #         elif o_year != '-' and o_qtr == '-' and o_mnth == '-':
    #             o_year = int(o_year)
    #             deliv_data = deliv_data[(deliv_data['o_year'] == o_year)]
    #         elif o_year != '-' and o_qtr != '-' and o_mnth == '-':
    #             o_year = int(o_year)
    #             deliv_data = deliv_data[(deliv_data['o_year'] == o_year)]
    #             deliv_data = deliv_data[(deliv_data['o_qtr'] == o_qtr)]
    #         elif o_year != '-' and o_mnth != '-':
    #             o_year = int(o_year)
    #             o_mnth = int(o_mnth)
    #             deliv_data = deliv_data[(deliv_data['o_year'] == o_year)]
    #             deliv_data = deliv_data[(deliv_data['o_mnth'] == o_mnth)]
    #         elif o_year == '-' and o_qtr != '-' and o_mnth != '-':
    #             o_mnth = int(o_mnth)
    #             deliv_data = deliv_data[(deliv_data['o_qtr'] == o_qtr)]
    #             deliv_data = deliv_data[(deliv_data['o_mnth'] == o_mnth)]
    #         elif o_year == '-' and o_qtr == '-' and o_mnth == '-':
    #             o_mnth = int(o_mnth)
    #             deliv_data = deliv_data[(deliv_data['o_mnth'] == o_mnth)]

    #         #check Delivery Date
    #         elif o_year != '-' or o_qtr != '-' or o_mnth != '-':
    #             msg = QMessageBox()
    #             msg.setText('Сhoose either Delivery date or Order date')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 10pt  \"Segoe UI\";"
    #                             "color: #4b0082;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #         elif d_year == '-' and d_qtr == '-' and d_mnth == '-':
    #             deliv_data
    #         elif d_year != '-' and d_qtr == '-' and d_mnth == '-':
    #             d_year = int(d_year)
    #             deliv_data = deliv_data[(deliv_data['d_year'] == d_year)]
    #         elif d_year != '-' and d_qtr != '-' and d_mnth == '-':
    #             d_year = int(d_year)
    #             deliv_data = deliv_data[(deliv_data['d_year'] == d_year)]
    #             deliv_data = deliv_data[(deliv_data['d_qtr'] == d_qtr)]
    #         elif d_year != '-' and d_mnth != '-':
    #             d_year = int(d_year)
    #             d_mnth = int(d_mnth)
    #             deliv_data = deliv_data[(deliv_data['d_year'] == d_year)]
    #             deliv_data = deliv_data[(deliv_data['d_mnth'] == d_mnth)]
    #         elif d_year == '-' and d_qtr != '-' and d_mnth != '-':
    #             d_mnth = int(d_mnth)
    #             deliv_data = deliv_data[(deliv_data['d_qtr'] == d_qtr)]
    #             deliv_data = deliv_data[(deliv_data['d_mnth'] == d_mnth)]
    #         elif d_year == '-' and d_qtr == '-' and d_mnth != '-':
    #             d_mnth = int(d_mnth)
    #             deliv_data = deliv_data[(deliv_data['d_mnth'] == d_mnth)]
            
      
    #         elif Brand == '-' and Segment == '-' and Product_group == '-':
    #             deliv_data
    #         elif Brand != '-' and Segment == '-' and Product_group == '-':
    #             deliv_data = deliv_data[(deliv_data['Brand'] == Brand)]
    #         elif Brand != '-' and Segment != '-' and Product_group == '-':
    #             deliv_data = deliv_data[(deliv_data['Brand'] == Brand)]
    #             deliv_data = deliv_data[(deliv_data['Segment'] == Segment)]
    #         elif Brand != '-' and Segment != '-' and Product_group != '-':
    #             deliv_data = deliv_data[(deliv_data['Brand'] == Brand)]
    #             deliv_data = deliv_data[(deliv_data['Segment'] == Segment)]
    #             deliv_data = deliv_data[(deliv_data['Product_group'] == Product_group)]
    #         elif Brand != '-' and Segment == '-' and Product_group != '-':
    #             deliv_data = deliv_data[(deliv_data['Brand'] == Brand)]
    #             deliv_data = deliv_data[(deliv_data['Product_group'] == Product_group)]
    #         elif Brand == '-' and Segment == '-' and Product_group != '-':
    #             deliv_data = deliv_data[(deliv_data['Product_group'] == Product_group)]
            
    #         if KSSS_Cust != '':
    #             KSSS_Cust = int(KSSS_Cust)
    #             deliv_data = deliv_data[(deliv_data['KSSS_Cust'] == KSSS_Cust)]


    #     deliv_data['d_year'] = deliv_data.drop(['d_year'], axis=1)
    #     deliv_data['d_qtr'] = deliv_data.drop(['d_qtr'], axis=1)
    #     deliv_data['d_mnth'] = deliv_data.drop(['d_mnth'], axis=1)
        
    #     deliv_data['o_year'] = deliv_data.drop(['o_year'], axis=1)
    #     deliv_data['o_qtr'] = deliv_data.drop(['o_qtr'], axis=1)
    #     deliv_data['o_mnth'] = deliv_data.drop(['o_mnth'], axis=1)
        

    #     deliv_data.to_excel(savePath[0], index=False)

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
 
 
    # def check_d_Quarter(self, row):
    #     if row['d_mnth'] >= 1 and row['d_mnth'] <= 3:
    #         return '1 кв.'
    #     elif row['d_mnth'] >= 4 and row['d_mnth'] <= 6:
    #         return '2 кв.'
    #     elif row['d_mnth'] >= 7 and row['d_mnth'] <= 9:
    #         return '3 кв.'
    #     elif row['d_mnth'] >= 10 and row['d_mnth'] <= 12:
    #         return '4 кв.'
        
        
    # def check_o_Quarter(self, row):
    #     if row['o_mnth'] >= 1 and row['o_mnth'] <= 3:
    #         return '1 кв.'
    #     elif row['o_mnth'] >= 4 and row['o_mnth'] <= 6:
    #         return '2 кв.'
    #     elif row['o_mnth'] >= 7 and row['o_mnth'] <= 9:
    #         return '3 кв.'
    #     elif row['o_mnth'] >= 10 and row['o_mnth'] <= 12:
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


    # def get_id_Delivery(self, del_merge):
    #     db_data = Delivery.query.filter(Delivery.del_merge == del_merge).first()
    #     delivery_id = db_data.id

    #     return delivery_id


    # def check_Price(self, row):
    #     if row['ord_Price'] == row['inv_Price']:
    #         return row['ord_Price']
    #     elif row['inv_Price'] == 0:
    #         return row['ord_Price']
    #     else:
    #         return row['inv_Price']


    # def check_Curr(self, row):
        if row['ord_Curr'] == row['inv_Curr']:
            return row['inv_Curr']
        elif row['inv_Curr'] == 0:
            return row['ord_Curr']
        else:
            return row['inv_Curr']