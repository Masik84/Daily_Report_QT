from datetime import datetime

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget, QListWidgetItem
from PySide6 import QtCore
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db, engine
# from models import Base_PL, Brands, Contracts, Customers_ALL, Orders, PL_chng, Packs, Products, Stock
from wind.pages.orders_ui import Ui_Form as Ord_Form
from wind.pages.report_cols_ui import Ui_Form as Cols_Form


class WindowSelectCols(QWidget, Cols_Form):
    def __init__(self):
        super(WindowSelectCols, self).__init__()
        self.setupUi(self)
    
        
        self.cols_list = []
        # orders_db = self.get_all_Orders_from_db()
        # if orders_db.empty == False:
        #     orders_db = orders_db[sorted(orders_db.columns )]
        #     cols = orders_db.columns.values.tolist()
        
        # for col in cols:
        #     item = QListWidgetItem(col)
        #     item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        #     item.setCheckState(QtCore.Qt.Unchecked)
        #     self.columns_list.addItem(item)
                
        # self.btn_clear.clicked.connect(self.clear_cols_list)        
        # self.btn_select.clicked.connect(self.get_columns)
      
    def get_columns(self):
        self.cols_list = []
        for i in range(self.columns_list.count()):
            item = self.columns_list.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                item = item.text()
                self.cols_list.append(item)

        # print(f'def get_columns():  {self.cols_list}')                   #
        self.hide()                                                      # +++
        return self.cols_list

    # def clear_cols_list(self):
    #     for i in range(self.columns_list.count()):
    #         item = self.columns_list.item(i)
    #         if item.checkState() == QtCore.Qt.Checked:
    #             item.setCheckState(QtCore.Qt.Unchecked)
    #     self.cols_list = []
    
    # def get_all_Orders_from_db(self):
    #     order_reques = db.query(Orders)
    #     order_data = pd.read_sql_query(order_reques.statement, engine)
        
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

    #     order_data = pd.merge(order_data, cust_data, how='left', left_on='cust_id', right_on='id')
    #     order_data = pd.merge(order_data, prod_data, how='left', left_on='prod_id', right_on='id')
    #     order_data = order_data.drop(columns=['id_x', 'ord_merge', 'contr_id', 'cust_id', 'prod_id', 'id_y', 'id'])
    #     order_data = pd.merge(order_data, stock_data, how='left', left_on='stock_id', right_on='id')
    #     order_data = order_data.drop(columns=['stock_id', 'id'])
    #     order_data = order_data.fillna('')

    #     return order_data



class Rep_Orders(QWidget):
    def __init__(self):
        super(Rep_Orders, self).__init__()
        self.ui = Ord_Form()
        self.ui.setupUi(self)
        
        self.windowSelectCols = WindowSelectCols() 
        
        # self.fill_in_prod_group()
        # self.fill_in_period()
        # self.fill_in_ord_date()

        # self.ui.line_brand.currentTextChanged.connect(self.fill_in_prod_group)
        # self.ui.line_brand.currentTextChanged.connect(self.fill_in_prod_segment)
        # self.ui.line_segment.currentTextChanged.connect(self.fill_in_prod_group)
        
        self.ui.btn_select_cols.setToolTip('выбери колонки для отчета')
        self.ui.btn_select_cols.clicked.connect(self.go_to_Select_Cols)
        
        self.ui.btn_open_file.clicked.connect(self.get_file)
        # self.ui.btn_upload_file.clicked.connect(self.upload_data)
        # self.ui.btn_download.clicked.connect(self.dowload_Orders)
        
        self.ui.rep_date.setCalendarPopup(True)

        
    def onDateChanged(self,date):
        period = date.toString('yyyy-MM-dd')
        return period
        
        
    def go_to_Select_Cols(self):
        self.windowSelectCols.show()
        
        
    def get_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_orders_File.setText(get_file[0])
 
            
    def upload_data(self, order_file_xls):
        order_file_xls = self.ui.label_orders_File.text()
        if order_file_xls == 'File Path' or order_file_xls == 'Database was updated successfully':
            msg = QMessageBox()
            msg.setWindowTitle('Programm Error')
            msg.setText('!!! Please choose the file with Order Data !!!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                                            "font: 12pt  \"Segoe UI\";"
                                            "color: #ff0000;\n"
                                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            order_data = self.read_order_file(order_file_xls)
            self.update_Orders(order_data)
            # self.get_all_Orders_from_db()

            msg = QMessageBox()
            msg.setText('Database was updated successfully')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Segoe UI\";"
                            "color: #4b0082;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            self.ui.label_orders_File.setText('File Path')
 
            
    # def read_order_file(self, order_file_xls):
    #     order_df = pd.read_excel(order_file_xls)
    #     order_df = order_df[['ПОтг', 'Пункт отгрузки', 'Реестр.№дог', 'КССС Пок', 'имя Покупателя', 'ТипДог', 'Тип договора', '№ зкз.Покуп', 
    #                                         'Дат.зкз.Пок', 'ЕжмР', 'Исходный Заказ недогруза', 'Дата Заказа недогруза', 'СтКМ', 'Статус разнарядки', 
    #                                         'КССС мат', 'ДатаЦены', 'ПрЦн', 'КССС ГрП', 'имя Грузополучателя', 'Условие отгрузки', 'ИнкТм', 'Маршр.', 'Маршрут',
    #                                         'Регион Грузополуч.', 'Страна', 'Комментарий', 'Цена без НДС', 'Вал.', 'за', 'Заявлено Покупателем', 
    #                                         'ЕИ', 'Не исполнено заявки']]

    #     order_df.rename(columns={
    #                                                 'ПОтг' : 'Stock_code',
    #                                                 'Пункт отгрузки' : 'Stock_Name',
    #                                                 'Реестр.№дог' : 'Contract_N',
    #                                                 'КССС Пок' : 'KSSS_cust',
    #                                                 'имя Покупателя' : 'Customer_Name',
    #                                                 'ТипДог' : 'CType',
    #                                                 'Тип договора' : 'Contract_type',
    #                                                 '№ зкз.Покуп' : 'ord_CRM',
    #                                                 'Дат.зкз.Пок' : 'ord_Date',
    #                                                 'ЕжмР' : 'ord_SAP',
    #                                                 'Исходный Заказ недогруза' : 'ord_Origin',
    #                                                 'Дата Заказа недогруза' : 'ord_Orig_Date',
    #                                                 'СтКМ' : 'CtKm',
    #                                                 'Статус разнарядки' : 'ord_Status',
    #                                                 'КССС мат' : 'KSSS_prod',
    #                                                 'ДатаЦены' : 'Price_Date',
    #                                                 'ПрЦн' : 'PrTp',
    #                                                 'КССС ГрП' : 'Shipto',
    #                                                 'имя Грузополучателя' : 'Shipto_Name',
    #                                                 'Условие отгрузки' : 'Delivery_type',
    #                                                 'ИнкТм' : 'InkTm',
    #                                                 'Маршр.' : 'Route_code',
    #                                                 'Маршрут' : 'Route',
    #                                                 'Регион Грузополуч.' : 'Shipto_Region',
    #                                                 'Страна' : 'Country',
    #                                                 'Комментарий' : 'Comment',
    #                                                 'Цена без НДС' : 'Price',
    #                                                 'Вал.' : 'Curr',
    #                                                 'за' : 'for',
    #                                                 'Заявлено Покупателем' : 'Volume_ord',
    #                                                 'ЕИ' : 'EA',
    #                                                 'Не исполнено заявки' : 'Volume_not_del',}, inplace = True)
        
    #     order_df = order_df[(order_df['Contract_type'] != 'Перемещение')]
    #     order_df = order_df[(order_df['Contract_type'] != 'Битумы')]
    #     # order_df['Stock_code'] = order_df.apply(self.correct_Stock, axis=1)
    #     order_df['Stock_Name'] = order_df['Stock_Name'].str.replace('"', '')
    #     order_df['Customer_Name'] = order_df['Customer_Name'].str.replace('"', '')
    #     order_df['Shipto_Name'] = order_df['Shipto_Name'].str.replace('"', '')
    #     order_df['PrTp'] = order_df['PrTp'].fillna('')

    #     order_df['ord_Origin'] = order_df['ord_Origin'].replace(np.nan, 0).astype(int)
        
    #     period = self.ui.rep_date.dateTime()
    #     period = period.toString('yyyy-MM-dd')
    #     period = datetime.strptime(period, '%Y-%m-%d')
    #     if period.day != 1:
    #         period = datetime(period.year, period.month, 1).strftime('%Y-%m-%d')
    #     else:
    #         period = period
            
    #     order_df.insert(0, 'Period', period)

    #     order_df['Period'] =pd.to_datetime(order_df['Period'], format='%Y-%m-%d')

    #     order_df['ord_Date'] = pd.to_datetime(order_df['ord_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})

    #     order_df['Price_Date'] = pd.to_datetime(order_df['Price_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
    #     order_df['ord_Orig_Date'] = pd.to_datetime(order_df['ord_Orig_Date'], format='%Y%m%d', errors='coerce').dt.date.replace({pd.NaT: ''})
        
    #     order_df['Volume_not_del'] = order_df['Volume_not_del'].astype(float)

    #     prod_reques = db.query(Products, Brands).join(Brands
    #                                         ).with_entities(Products.KSSS_prod, Products.Product_Name, Brands.Brand)
    #     product_df = pd.DataFrame(prod_reques)
    #     product_df['KSSS_prod'] = product_df['KSSS_prod'].astype(str)
    #     order_df['KSSS_prod'] = order_df['KSSS_prod'].astype(str)
        
    #     order_df = pd.merge(order_df, product_df, how='left', on='KSSS_prod')
        
    #     order_df['Product_Name'] = order_df['Product_Name'].fillna('-')
    #     order_df = order_df[(order_df.Product_Name != '-')]
    #     order_df = order_df.drop(['Product_Name'], axis = 1)
        
    #     order_df['KSSS_prod'] = order_df['KSSS_prod'].astype(int)
        
    #     base_pl_request = db.execute(select(Base_PL.merge,Base_PL.Price)).all()
    #     base_pl_data = pd.DataFrame(base_pl_request)

    #     # get calendar of Base Price changes
    #     base_pl_chng_request = db.execute(select(PL_chng.Date,PL_chng.chng_Dealers)).all()
    #     base_pl_chng_data = pd.DataFrame(base_pl_chng_request)
    #     base_pl_chng_data.rename(columns={'Date' : 'Price_Date', 'chng_Dealers' : 'Change'}, inplace = True)

    #     order_df = pd.merge(order_df, base_pl_chng_data, how='left', on='Price_Date')
        
    #     # order_df['cust-t-pl'] = order_df.apply(self.change_cust_type_for_pl, axis=1)
    #     order_df['merge'] = order_df['KSSS_prod'].astype(str) + '_' + order_df['Change'].astype(str) + '_Dealer'
    #     order_df = pd.merge(order_df, base_pl_data, how='left', on='merge')

    #     order_df['PrTp'] = order_df.apply(self.check_Price_type, axis=1)

    #     order_df.rename(columns={'Price_x' : 'Price'}, inplace = True)
    #     order_df['Price'] = order_df['Price'].astype(float)
    #     order_df = order_df.drop(['merge', 'Change', 'Price_y'], axis=1)
        
    #     order_df['ord_merge'] = order_df['ord_SAP'].astype (str) + order_df['KSSS_prod'].astype(str)
    #     order_df['contr_merge'] = order_df['Contract_N'] + order_df['KSSS_cust'].astype(str)
    #     order_df['Volume_del'] = order_df['Volume_ord'] - order_df['Volume_not_del']
        
    #     order_df['Price'] = np.where(order_df['for'] == 1, order_df['Price'] * 1000, order_df['Price'])
    #     order_df['DocType'] = 'Order'
    #     order_df.to_excel('ord_test.xlsx')
    #     order_data = order_df.to_dict('records')

    #     return order_data


    # def update_Orders(self, data):
        
    #     ord_for_create = []
    #     ord_for_update = []
    #     for row in data:
    #         order_exists = Orders.query.filter(Orders.ord_merge == row['ord_merge']).count()
    #         if row['ord_Orig_Date'] == '':
    #             row['ord_Orig_Date'] = None
    #         else:
    #             row['ord_Orig_Date'] = row['ord_Orig_Date']

    #         if row['ord_Origin'] == 0:
    #             row['ord_Origin'] = None
    #         else:
    #             row['ord_Origin'] = row['ord_Origin']

    #         if order_exists == 0:
    #             order_list = {'ord_merge' : row['ord_merge'],
    #                                 'DocType' : row['DocType'],
    #                                 'Period' : row['Period'],
    #                                 'stock_id' : self.get_id_stock_code(row['Stock_code']),
    #                                 'contr_id' : self.get_id_Contract(row['contr_merge']),
    #                                 'cust_id' : self.get_id_all_Customer(row['KSSS_cust']),
    #                                 'ord_CRM' : row['ord_CRM'],
    #                                 'ord_Date' : row['ord_Date'],
    #                                 'ord_SAP' : row['ord_SAP'],
    #                                 'ord_Origin' : row['ord_Origin'],
    #                                 'ord_Orig_Date' : row['ord_Orig_Date'],
    #                                 'CtKm' : row['CtKm'],
    #                                 'ord_Status' : row['ord_Status'],
    #                                 'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                                 'Price_Date' : row['Price_Date'],
    #                                 'PrTp' : row['PrTp'],
    #                                 'KSSS_Shipto' : row['KSSS_Shipto'],
    #                                 'Shipto_Name' : row['Shipto_Name'],
    #                                 'Delivery_type' : row['Delivery_type'],
    #                                 'InkTm' : row['InkTm'],
    #                                 'Shipto_Region' : row['Shipto_Region'],
    #                                 'Country' : row['Country'],
    #                                 'Comment' : row['Comment'],
    #                                 'Price' : row['Price'],
    #                                 'Curr' : row['Curr'],
    #                                 'Volume_ord' : row['Volume_ord'],
    #                                 'Volume_not_del' : row['Volume_not_del'],
    #                                 'Volume_del' : row['Volume_del']}
    #             ord_for_create.append(order_list)

    #         elif order_exists > 0:
    #             order_list = {'id' : self.get_id_Order(row['ord_merge']),
    #                             'ord_merge' : row['ord_merge'],
    #                             'DocType' : row['DocType'],
    #                             'Period' : row['Period'],
    #                             'stock_id' : self.get_id_stock_code(row['Stock_code']),
    #                             'contr_id' : self.get_id_Contract(row['contr_merge']),
    #                             'cust_id' : self.get_id_all_Customer(row['KSSS_cust']),
    #                             'ord_CRM' : row['ord_CRM'],
    #                             'ord_Date' : row['ord_Date'],
    #                             'ord_SAP' : row['ord_SAP'],
    #                             'ord_Origin' : row['ord_Origin'],
    #                             'ord_Orig_Date' : row['ord_Orig_Date'],
    #                             'CtKm' : row['CtKm'],
    #                             'ord_Status' : row['ord_Status'],
    #                             'prod_id' : self.get_id_Product(row['KSSS_prod']),
    #                             'Price_Date' : row['Price_Date'],
    #                             'PrTp' : row['PrTp'],
    #                             'KSSS_Shipto' : row['KSSS_Shipto'],
    #                             'Shipto_Name' : row['Shipto_Name'],
    #                             'Delivery_type' : row['Delivery_type'],
    #                             'InkTm' : row['InkTm'],
    #                             'Shipto_Region' : row['Shipto_Region'],
    #                             'Country' : row['Country'],
    #                             'Comment' : row['Comment'],
    #                             'Price' : row['Price'],
    #                             'Curr' : row['Curr'],
    #                             'Volume_ord' : row['Volume_ord'],
    #                             'Volume_not_del' : row['Volume_not_del'],
    #                             'Volume_del' : row['Volume_del']}
    #             ord_for_update.append(order_list)
                
    #     db.bulk_insert_mappings(Orders, ord_for_create)
    #     db.bulk_update_mappings(Orders, ord_for_update)

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
        
    #     # self.ui.line_period_year.clear()
    #     # self.ui.line_period_qtr.clear()
    #     # self.ui.line_period_mnth.clear()
        
    #     # self.ui.line_ord_year.clear()
    #     # self.ui.line_ord_qtr.clear()
    #     # self.ui.line_ord_mnth.clear()
        
    #     # self.ui.line_pr_group.clear()
        
    #     # self.fill_in_prod_group()
    #     # self.fill_in_period()
    #     # self.fill_in_ord_date()
        
    #     return ord_for_create


    # def get_id_Order(self, ord_merge):
    #     db_data = Orders.query.filter(Orders.ord_merge == ord_merge).first()
    #     order_id = db_data.id

    #     return order_id

    
    # def get_all_Orders_from_db(self):
    #     order_reques = db.query(Orders)
    #     order_data = pd.read_sql_query(order_reques.statement, engine)
        
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

    #     order_data = pd.merge(order_data, cust_data, how='left', left_on='cust_id', right_on='id')
    #     order_data = pd.merge(order_data, prod_data, how='left', left_on='prod_id', right_on='id')
    #     order_data = order_data.drop(columns=['id_x', 'ord_merge', 'contr_id', 'cust_id', 'prod_id', 'id_y', 'id'])
    #     order_data = pd.merge(order_data, stock_data, how='left', left_on='stock_id', right_on='id')
    #     order_data = order_data.drop(columns=['stock_id', 'id'])
    #     order_data = order_data.fillna('')

    #     return order_data


    # def fill_in_period(self):
    #     period_data = self.get_all_Orders_from_db()

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()

    #     if period_data.empty == True:
    #         self.ui.line_period_year.addItem('-')
    #         self.ui.line_period_qtr.addItem('-')
    #         self.ui.line_period_mnth.addItem('-')
            
    #     else:
    #         period_data['year'] = pd.DatetimeIndex(period_data['Period']).year
    #         period_data['mnth'] = pd.DatetimeIndex(period_data['Period']).month
    #         period_data['qtr'] = period_data.apply(self.check_Quarter, axis=1)
        
    #         if Brand == '-' and Product_Segment == '-' and Product_group == '-':
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment == '-' and Product_group == '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Brand']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group == '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
            
    #         elif Brand == '-' and Product_Segment != '-' and Product_group == '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
            
    #         elif Brand != '-' and Product_Segment == '-' and Product_group != '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             period_data = period_data[(period_data['Product_group'] == Product_group)]
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]
                
    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
                
    #         elif Brand != '-' and Product_Segment != '-' and Product_group != '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]
    #             period_data = period_data[(period_data['Product_group'] == Product_group)]
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
              
    #         elif Brand == '-' and Product_Segment != '-' and Product_group != '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Segment', 'Product_group']]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]
    #             period_data = period_data[(period_data['Product_group'] == Product_group)]
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

    #             df_year = df_year.drop_duplicates()
    #             df_qtr = df_qtr.drop_duplicates()
    #             df_mnth = df_mnth.drop_duplicates()
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
    #             self.ui.line_period_year.addItems(df_year_list)
    #             self.ui.line_period_qtr.addItems(df_qtr_list)
    #             self.ui.line_period_mnth.addItems(df_mnth_list)
               
        
    # def fill_in_ord_date(self):      
    #     period_data = self.get_all_Orders_from_db()

    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     p_year = self.ui.line_period_year.currentText()
    #     p_qtr = self.ui.line_period_qtr.currentText()
    #     p_mnth = self.ui.line_period_mnth.currentText()

    #     if period_data.empty == True:
    #         self.ui.line_ord_year.addItem('-')
    #         self.ui.line_ord_qtr.addItem('-')
    #         self.ui.line_ord_mnth.addItem('-')
            
    #     elif p_year != '-' or p_qtr != '-' or p_mnth != '-':
    #         self.ui.line_ord_year.addItem('-')
    #         self.ui.line_ord_qtr.addItem('-')
    #         self.ui.line_ord_mnth.addItem('-')
                 
    #     else:
    #         period_data = period_data.drop_duplicates(subset='KSSS_prod')
    #         period_data['year'] = pd.DatetimeIndex(period_data['ord_Date']).year
    #         period_data['mnth'] = pd.DatetimeIndex(period_data['ord_Date']).month
    #         period_data['qtr'] = period_data.apply(self.check_Quarter, axis=1)

    #         if Brand == '-' and Product_Segment == '-' and Product_group == '-':
    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #             period_data = [['year', 'qtr', 'mnth', 'Brand']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]

    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]

    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment']]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]

    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             period_data = period_data[(period_data['Product_group'] == Product_group)]

    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #             period_data = [['year', 'qtr', 'mnth', 'Brand', 'Segment', 'Product_group']]
    #             period_data = period_data[(period_data['Brand'] == Brand)]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]
    #             period_data = period_data[(period_data['Product_group'] == Product_group)]

    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
            
    #         elif Brand == '-' and Product_Segment != '-' and Product_group != '-':
    #             period_data = [['year', 'qtr', 'mnth', 'Segment', 'Product_group']]
    #             period_data = period_data[(period_data['Segment'] == Product_Segment)]
    #             period_data = period_data[(period_data['Product_group'] == Product_group)]

    #             df_year = period_data[['year']]
    #             df_qtr = period_data[['qtr']]
    #             df_mnth = period_data[['mnth']]

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
    #     group_data = self.get_all_Orders_from_db()
        
    #     Brand = self.ui.line_brand.currentText()
    #     Product_Segment = self.ui.line_segment.currentText()
                
    #     if group_data.empty == True:
    #         self.ui.line_pr_group.addItem('-')
        
    #     else:
    #         self.ui.line_pr_group.clear()
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
    #     group_data = self.get_all_Orders_from_db()
        
    #     Brand = self.ui.line_brand.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     if group_data.empty == True:
    #         self.ui.line_segment.addItem('-')
        
    #     else:
    #         self.ui.line_segment.clear()
            
    #         if Brand == '-' and Product_group == '-':
    #             group_data = group_data[['Segment']]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_segment.addItems(group_data_list)

    #         elif Brand != '-' and Product_group == '-':
    #             group_data = group_data[['Segment', 'Brand']]
    #             group_data = group_data[(group_data['Brand'] == Brand)]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_segment.addItems(group_data_list)

    #         elif Brand != '-' and Product_group != '-':
    #             group_data = group_data[['Segment', 'Brand', 'Segment']]
    #             group_data = group_data[(group_data['Brand'] == Brand)]
    #             group_data = group_data[(group_data['Product_group'] == Product_group)]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_segment.addItems(group_data_list)

    #         elif Brand == '-' and Product_group != '-':
    #             group_data = group_data[['Product_group', 'Segment']]
    #             group_data = group_data[(group_data['Product_group'] == Product_group)]
    #             group_data = group_data.drop_duplicates(subset='Segment')
    #             group_data = group_data.sort_values(by='Segment')
    #             group_data_list = group_data['Segment'].tolist()
    #             group_data_list.insert(0, '-')
    #             self.ui.line_segment.addItems(group_data_list)

    
    # def dowload_Orders(self):
        
    #     # if self.windowSelectCols.cols_list:
    #     #     print(f'Колонки для отчета: {self.windowSelectCols.cols_list}') 
    #     # else:
    #     #     msg = QMessageBox.information(
    #     #         self, 
    #     #         'Внимание', 
    #     #         'Вы не выбрали колонки для отчета.')
        
    #     cols_list = self.windowSelectCols.cols_list
        
    #     if cols_list.count != 0:
    #         order_data = order_data[cols_list]
    #     else:
    #         order_data
        
    #     # savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Orders.xlsx', 'Excel Workbook (*.xlsx)')
        
    #     order_data = self.get_all_Orders_from_db()

    #     p_year = self.ui.line_period_year.currentText()
    #     p_qtr = self.ui.line_period_qtr.currentText()
    #     p_mnth = self.ui.line_period_mnth.currentText()
        
    #     o_year = self.ui.line_ord_year.currentText()
    #     o_qtr = self.ui.line_ord_qtr.currentText()
    #     o_mnth = self.ui.line_ord_mnth.currentText()
        
    #     Brand = self.ui.line_brand.currentText()
    #     Segment = self.ui.line_segment.currentText()
    #     Product_group = self.ui.line_pr_group.currentText()
        
    #     KSSS_Cust = self.ui.line_cust_ksss.text()
        
    #     if order_data.empty == True:
    #         msg = QMessageBox()
    #         msg.setText('There is no Order data in Database')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Critical)
    #         x = msg.exec_()
            
    #     else:
    #         order_data['KSSS_cust'] = order_data['KSSS_cust'].astype(int)
    #         order_data['KSSS_prod'] = order_data['KSSS_prod'].astype(int)
    #         order_data['KSSS_Shipto'] = order_data['KSSS_Shipto'].astype(int)
    #         order_data['Price'] = order_data['Price'].astype(float)
    #         order_data['Volume_ord'] = order_data['Volume_ord'].astype(float)
    #         order_data['Volume_not_del'] = order_data['Volume_not_del'].astype(float)
    #         order_data['Volume_del'] = order_data['Volume_del'].astype(float)
            
    #         order_data['p_year'] = pd.DatetimeIndex(order_data['Period']).year
    #         order_data['p_mnth'] = pd.DatetimeIndex(order_data['Period']).month
    #         order_data['p_qtr'] = order_data.apply(self.check_p_Quarter, axis=1)
            
    #         order_data['o_year'] = pd.DatetimeIndex(order_data['ord_Date']).year
    #         order_data['o_mnth'] = pd.DatetimeIndex(order_data['ord_Date']).month
    #         order_data['o_qtr'] = order_data.apply(self.check_o_Quarter, axis=1)
            
    #         order_data['LoB'] = order_data.apply(self.check_prod_LoB, axis=1)
            
    #         order_data = pd.merge(order_data, cust_df, how='left', on='KSSS_cust')
    #         order_data['Cust_type'] = order_data['Cust_type'].fillna('other_LLK')
    #         order_data['Cust_type'] = order_data.apply(self.check_Cust_type, axis=1)
            
    #         cust_df1 = cust_data[['merge', 'AM', 'STL', 'SM']]
    #         cust_df2 = cust_data[['KSSS_cust', 'AM', 'STL', 'SM']]
            
    #         order_data['merge'] = order_data['KSSS_cust'].astype(str) + order_data['LoB']
            
    #         order_data1 = pd.merge(order_data, cust_df1, how='left', on='merge')
    #         order_data1['AM'] = order_data1['AM'].fillna('-')
    #         order_data1['STL'] = order_data1['STL'].fillna('-')
    #         order_data1['SM'] = order_data1['SM'].fillna('-')
    #         order_data1 = order_data1[(order_data1['AM'] != '-')]
            
    #         order_data2 = pd.merge(order_data, cust_df2, how='left', on='KSSS_cust')
    #         order_data2['AM'] = order_data2['AM'].fillna('-')
    #         order_data2['STL'] = order_data2['STL'].fillna('-')
    #         order_data2['SM'] = order_data2['SM'].fillna('-')
            
    #         frames = [order_data1, order_data2]
    #         order_data = pd.concat(frames)
            
    #         order_data = order_data.drop(['merge'], axis=1)
            
    #         order_data_cust = pd.DataFrame()
            
    #         if self.ui.check_teb_dealer.isChecked() == True:
    #             t_deal = order_data[(order_data['Cust_type'] == 'Dealer_TEBOIL')]
    #             frame2 = [order_data_cust, t_deal]
    #             order_data_cust = pd.concat(frame2)
                
    #         if self.ui.check_teb_direct.isChecked() == True:
    #             t_dir = order_data[(order_data['Cust_type'] == 'Direct_TEBOIL')]
    #             frame2 = [order_data_cust, t_dir]
    #             order_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_teb_fws.isChecked() == True:
    #             t_fws = order_data[(order_data['Cust_type'] == 'FWS_TEBOIL')]
    #             frame2 = [order_data_cust, t_fws]
    #             order_data_cust = pd.concat(frame2)
                        
    #         if self.ui.check_teb_market.isChecked() == True:
    #             t_mp = order_data[(order_data['Cust_type'] == 'MarketPlace_TEBOIL')]
    #             frame2 = [order_data_cust, t_mp]
    #             order_data_cust = pd.concat(frame2)

    #         if self.ui.check_luk_dealer.isChecked() == True:
    #             l_deal = order_data[(order_data['Cust_type'] == 'Dealer_LLK')]
    #             frame2 = [order_data_cust, l_deal]
    #             order_data_cust = pd.concat(frame2)

    #         if self.ui.check_luk_direct.isChecked() == True:
    #             l_dir = order_data[(order_data['Cust_type'] == 'Direct_LLK')]
    #             frame2 = [order_data_cust, l_dir]
    #             order_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_fws.isChecked() == True:
    #             l_fws = order_data[(order_data['Cust_type'] == 'FWS_LLK')]
    #             frame2 = [order_data_cust, l_fws]
    #             order_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_market.isChecked() == True:
    #             l_mp = order_data[(order_data['Cust_type'] == 'MarketPlace_LLK')]
    #             frame2 = [order_data_cust, l_mp]
    #             order_data_cust = pd.concat(frame2)
                    
    #         if self.ui.check_luk_other.isChecked() == True:
    #             l_oth = order_data[(order_data['Cust_type'] == 'other_LLK')]
    #             frame2 = [order_data_cust, l_oth]
    #             order_data_cust = pd.concat(frame2)
                 
    #         if order_data_cust.empty == True:
    #             order_data
    #         else:
    #             order_data = order_data_cust
            
    #         #check Order Date
    #         if p_year != '-' or p_qtr != '-' or p_mnth != '-':
    #             msg = QMessageBox()
    #             msg.setText('Сhoose either Period or Order date')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 10pt  \"Segoe UI\";"
    #                             "color: #4b0082;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
            
    #         elif o_year == '-' and o_qtr == '-' and o_mnth == '-':
    #             order_data
    #         elif o_year != '-' and o_qtr == '-' and o_mnth == '-':
    #             o_year = int(o_year)
    #             order_data = order_data[(order_data['o_year'] == o_year)]
    #         elif o_year != '-' and o_qtr != '-' and o_mnth == '-':
    #             o_year = int(o_year)
    #             order_data = order_data[(order_data['o_year'] == o_year)]
    #             order_data = order_data[(order_data['o_qtr'] == o_qtr)]
    #         elif o_year != '-' and o_mnth != '-':
    #             o_year = int(o_year)
    #             o_mnth = int(o_mnth)
    #             order_data = order_data[(order_data['o_year'] == o_year)]
    #             order_data = order_data[(order_data['o_mnth'] == o_mnth)]
    #         elif o_year == '-' and o_qtr != '-' and o_mnth != '-':
    #             o_mnth = int(o_mnth)
    #             order_data = order_data[(order_data['o_qtr'] == o_qtr)]
    #             order_data = order_data[(order_data['o_mnth'] == o_mnth)]
    #         elif o_year == '-' and o_qtr == '-' and o_mnth == '-':
    #             o_mnth = int(o_mnth)
    #             order_data = order_data[(order_data['o_mnth'] == o_mnth)]

    #         #check Period
    #         elif o_year != '-' or o_qtr != '-' or o_mnth != '-':
    #             msg = QMessageBox()
    #             msg.setText('Сhoose either Period or Order date')
    #             msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                             "font: 10pt  \"Segoe UI\";"
    #                             "color: #4b0082;\n"
    #                             " ")
    #             msg.setIcon(QMessageBox.Critical)
    #             x = msg.exec_()
    #         elif p_year == '-' and p_qtr == '-' and p_mnth == '-':
    #             order_data
    #         elif p_year != '-' and p_qtr == '-' and p_mnth == '-':
    #             p_year = int(p_year)
    #             order_data = order_data[(order_data['p_year'] == p_year)]
    #         elif p_year != '-' and p_qtr != '-' and p_mnth == '-':
    #             p_year = int(p_year)
    #             order_data = order_data[(order_data['p_year'] == p_year)]
    #             order_data = order_data[(order_data['p_qtr'] == p_qtr)]
    #         elif p_year != '-' and p_mnth != '-':
    #             p_year = int(p_year)
    #             p_mnth = int(p_mnth)
    #             order_data = order_data[(order_data['p_year'] == p_year)]
    #             order_data = order_data[(order_data['p_mnth'] == p_mnth)]
    #         elif p_year == '-' and p_qtr != '-' and p_mnth != '-':
    #             p_mnth = int(p_mnth)
    #             order_data = order_data[(order_data['p_qtr'] == p_qtr)]
    #             order_data = order_data[(order_data['p_mnth'] == p_mnth)]
    #         elif p_year == '-' and p_qtr == '-' and p_mnth != '-':
    #             p_mnth = int(p_mnth)
    #             order_data = order_data[(order_data['p_mnth'] == p_mnth)]
            
      
    #         elif Brand == '-' and Segment == '-' and Product_group == '-':
    #             order_data
    #         elif Brand != '-' and Segment == '-' and Product_group == '-':
    #             order_data = order_data[(order_data['Brand'] == Brand)]
    #         elif Brand != '-' and Segment != '-' and Product_group == '-':
    #             order_data = order_data[(order_data['Brand'] == Brand)]
    #             order_data = order_data[(order_data['Segment'] == Segment)]
    #         elif Brand != '-' and Segment != '-' and Product_group != '-':
    #             order_data = order_data[(order_data['Brand'] == Brand)]
    #             order_data = order_data[(order_data['Segment'] == Segment)]
    #             order_data = order_data[(order_data['Product_group'] == Product_group)]
    #         elif Brand != '-' and Segment == '-' and Product_group != '-':
    #             order_data = order_data[(order_data['Brand'] == Brand)]
    #             order_data = order_data[(order_data['Product_group'] == Product_group)]
    #         elif Brand == '-' and Segment == '-' and Product_group != '-':
    #             order_data = order_data[(order_data['Product_group'] == Product_group)]
            
    #         if KSSS_Cust != '':
    #             KSSS_Cust = int(KSSS_Cust)
    #             order_data = order_data[(order_data['KSSS_Cust'] == KSSS_Cust)]

    #     order_data['p_year'] = order_data.drop(['p_year'], axis=1)
    #     order_data['p_qtr'] = order_data.drop(['p_qtr'], axis=1)
    #     order_data['p_mnth'] = order_data.drop(['p_mnth'], axis=1)
        
    #     order_data['o_year'] = order_data.drop(['o_year'], axis=1)
    #     order_data['o_qtr'] = order_data.drop(['o_qtr'], axis=1)
    #     order_data['o_mnth'] = order_data.drop(['o_mnth'], axis=1)
        
    #     self.ui.line_cust_ksss.clear()

    #     order_data.to_excel(savePath[0], index=False)

    #     msg = QMessageBox()
    #     msg.setText('Report was saved successfully')
    #     msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                     "font: 12pt  \"Segoe UI\";"
    #                     "color: #4b0082;\n"
    #                     " ")
    #     msg.setIcon(QMessageBox.Information)
    #     x = msg.exec_()
            
    
    # def check_Price_type(self, row):
    #     if row['Brand'] == 'TEBOIL':
    #         if row['Price_x'] == row['Price_y']:
    #             return row['PrTp']
    #         elif row['Price_x'] != row['Price_y'] and row['PrTp'] == '':
    #             return 'P'
    #         else:
    #             return row['PrTp']
    #     else:
    #         return row['PrTp']


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
 
 
    # def check_p_Quarter(self, row):
    #     if row['p_mnth'] >= 1 and row['p_mnth'] <= 3:
    #         return '1 кв.'
    #     elif row['p_mnth'] >= 4 and row['p_mnth'] <= 6:
    #         return '2 кв.'
    #     elif row['p_mnth'] >= 7 and row['p_mnth'] <= 9:
    #         return '3 кв.'
    #     elif row['p_mnth'] >= 10 and row['p_mnth'] <= 12:
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


    # def get_id_stock_code(self, Stock_code):
    #     db_data = Stock.query.filter(Stock.Stock == Stock_code).first()
    #     st_type_id = db_data.id

    #     return st_type_id


    # def get_id_Product(self, KSSS_prod):
    #     if KSSS_prod != 'nan':
    #         db_data = Products.query.filter(Products.KSSS_prod == KSSS_prod).first()
    #         product_id = db_data.id
    #     else:
    #         product_id = None

    #     return product_id
    
    
    # def correct_Stock(self, row):
    #     if row['Stock_code'].isdigit() == True:
    #         if int(row['Stock_code']) < 10:
    #             return '0' + row['Stock_code']
    #     else:
    #         return row['Stock_code']


    # def get_id_Contract(self, contr_merge):
    #     if contr_merge != 'nan':
    #         db_data = db.query(Contracts).filter(Contracts.merge == contr_merge).first()
    #         contract_id = db_data.id
    #     else:
    #         contract_id = None
            
    #     return contract_id


    # def get_id_all_Customer(self, KSSS_cust):
    #     if KSSS_cust != 'nan':
    #         db_data = db.query(Customers_ALL).filter(Customers_ALL.KSSS_cust == KSSS_cust).first()
    #         customer_all_id = db_data.id
    #     else:
    #         customer_all_id = None
            
    #     return customer_all_id


    # def change_cust_type_for_pl(self, row):
    #     if row['Cust_type'] == 'Dealer_AZS_TEBOIL':
    #         return 'AZS'
    #     else:
    #         return 'Dealer'




