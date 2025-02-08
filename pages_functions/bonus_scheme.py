import numpy as np
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db
# from models import Bonus_Scheme
from wind.pages.bonus_scheme_ui import Ui_Form

pd.options.display.float_format = '{:,.2f}'.format


class Bon_Scheme(QWidget):
    def __init__(self):
        super(Bon_Scheme, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        
        # self.fill_in_year()
        
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        # self.ui.btn_find.clicked.connect(self.find_Scheme)
        # self.ui.btn_download.clicked.connect(self.dowload_Scheme)
        
        
    def get_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_bonus_File.setText(get_file[0])
 
    
    def upload_data(self, bonus_file_xls):
        bonus_file_xls = self.ui.label_bonus_File.text()
        if bonus_file_xls == 'File Path' or bonus_file_xls == 'Database was updated successfully':
            msg = QMessageBox()
            msg.setWindowTitle('Programm Error')
            msg.setText('!!! Please choose the file with Bonus Scheme Data !!!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                                            "font: 12pt  \"Segoe UI\";"
                                            "color: #ff0000;\n"
                                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        else:
            bonus_sc_data = self.read_bonus_file(bonus_file_xls)
            self.update_Bonus_Scheme(bonus_sc_data)

            msg = QMessageBox()
            msg.setText('Database was updated successfully')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Segoe UI\";"
                            "color: #4b0082;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            self.ui.label_bonus_File.setText('File Path')    


    def read_bonus_file(self, bonus_file_xls):
        bon_sch_df = pd.read_excel(bonus_file_xls, sheet_name='Scheme')

        bon_sch_df['Year'] = bon_sch_df['Year'].astype(int)
        bon_sch_df['Plan'] = bon_sch_df['Plan'].astype(float)
        bon_sch_df['Bonus_M'] = bon_sch_df['Bonus_M'].astype(float)
        bon_sch_df['Bonus_Q'] = bon_sch_df['Bonus_Q'].astype(float)
        bon_sch_df['Bonus_Y'] = bon_sch_df['Bonus_Y'].astype(float)
        bon_sch_df['Bonus_Add'] = bon_sch_df['Bonus_Add'].astype(float)
        bon_sch_df['Max_Bonus'] = bon_sch_df['Max_Bonus'].astype(float)
        
        bon_sch_df['Brand'] = bon_sch_df['Brand'].replace(np.nan, '').astype(str)
        bon_sch_df['LoB'] = bon_sch_df['LoB'].replace(np.nan, '').astype(str)
        bon_sch_df['Segment'] = bon_sch_df['Segment'].replace(np.nan, '').astype(str)
        bon_sch_df['Product_group'] = bon_sch_df['Product_group'].replace(np.nan, '').astype(str)
        bon_sch_df['Product_Name'] = bon_sch_df['Product_Name'].replace(np.nan, '').astype(str)
        bon_sch_df['Pack_group'] = bon_sch_df['Pack_group'].replace(np.nan, '').astype(str)
        bon_sch_df['Pack_group2'] = bon_sch_df['Pack_group2'].replace(np.nan, '').astype(str)
        bon_sch_df['Production'] = bon_sch_df['Production'].replace(np.nan, '').astype(str)


        bon_sch_df['bon_sch_merge'] = bon_sch_df['Year'].astype(str) + bon_sch_df['Brand'].astype(str) + bon_sch_df['LoB'].astype(str) + bon_sch_df['Segment'].astype(str) + bon_sch_df['Product_group'].astype(str) + bon_sch_df['Product_Name'].astype(str) + bon_sch_df['Pack_group'].astype(str) + bon_sch_df['Pack_group2'].astype(str) + bon_sch_df['Production'].astype(str) + bon_sch_df['Plan'].astype(str)
        bon_sch_df = bon_sch_df.drop_duplicates(subset=['bon_sch_merge'])

        bon_data = bon_sch_df.to_dict('records')

        return bon_data


    # def update_Bonus_Scheme(self, data):
    #     bon_sc_for_create = []
    #     bon_sc_for_update = []
    #     for row in data:
    #         bon_sc_exists = Bonus_Scheme.query.filter(Bonus_Scheme.bon_sch_merge == str(row['bon_sch_merge'])).count()

    #         if bon_sc_exists == 0:
    #             bon_sc_list = {'bon_sch_merge' : row['bon_sch_merge'],
    #                                     'Year' : row['Year'],
    #                                     'Brand' : row['Brand'],
    #                                     'LoB' : row['LoB'],
    #                                     'Segment' : row['Segment'],
    #                                     'Product_group' : row['Product_group'],
    #                                     'Product_Name' : row['Product_Name'],
    #                                     'Pack_group' : row['Pack_group'],
    #                                     'Pack_group2' : row['Pack_group2'],
    #                                     'Production' : row['Production'],
    #                                     'Plan' : row['Plan'],
    #                                     'Bonus_M' : row['Bonus_M'],
    #                                     'Bonus_Q' : row['Bonus_Q'],
    #                                     'Bonus_Y' : row['Bonus_Y'],
    #                                     'Bonus_Add' : row['Bonus_Add'],
    #                                     'Max_Bonus' : row['Max_Bonus']}
    #             bon_sc_for_create.append(bon_sc_list)

    #         elif bon_sc_exists > 0:
    #             bon_sc_list = {'id' : self.get_id_Bonus_Scheme(row['bon_sch_merge']),
    #                                     'bon_sch_merge' : row['bon_sch_merge'],
    #                                     'Year' : row['Year'],
    #                                     'Brand' : row['Brand'],
    #                                     'LoB' : row['LoB'],
    #                                     'Segment' : row['Segment'],
    #                                     'Product_group' : row['Product_group'],
    #                                     'Product_Name' : row['Product_Name'],
    #                                     'Pack_group' : row['Pack_group'],
    #                                     'Pack_group2' : row['Pack_group2'],
    #                                     'Production' : row['Production'],
    #                                     'Plan' : row['Plan'],
    #                                     'Bonus_M' : row['Bonus_M'],
    #                                     'Bonus_Q' : row['Bonus_Q'],
    #                                     'Bonus_Y' : row['Bonus_Y'],
    #                                     'Bonus_Add' : row['Bonus_Add'],
    #                                     'Max_Bonus' : row['Max_Bonus']}
    #             bon_sc_for_update.append(bon_sc_list)
                
    #     db.bulk_insert_mappings(Bonus_Scheme, bon_sc_for_create)
    #     db.bulk_update_mappings(Bonus_Scheme, bon_sc_for_update)

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
        
    #     self.ui.line_Year.clear()
    #     self.fill_in_year()

    #     return bon_sc_for_create
    
    
    # def get_id_Bonus_Scheme(self, bon_sch_merge):
    #     db_data = db.query(Bonus_Scheme).filter(Bonus_Scheme.bon_sch_merge == bon_sch_merge).first()
    #     bonus_sch_id = db_data.id

    #     return bonus_sch_id


    # def fill_in_year(self):      
    #     period_request = db.execute(select(Bonus_Scheme.Year, Bonus_Scheme.Brand, Bonus_Scheme.LoB)).all()
    #     year_date = pd.DataFrame(period_request)

    #     Brand = self.ui.line_Brand.currentText()
    #     LoB = self.ui.line_LoB.currentText()

    #     if year_date.empty == True:
    #         self.ui.line_Year.addItem('-')
            
    #     elif Brand == '-' and LoB == '-':
    #         year_date = year_date[['Year']]
    #         year_date = year_date.drop_duplicates(subset='Year')
    #         year_date = year_date.sort_values(by='Year')     
    #         year_date['Year'] = year_date['Year'].astype(str) 
    #         year_date_list = year_date['Year'].astype(str).tolist()
    #         year_date_list.insert(0, '-')
    #         self.ui.line_Year.addItems(year_date_list)
            
    #     elif Brand != '-' and LoB == '-':
    #         year_date = year_date[['Year', 'Brand']]
    #         year_date = year_date[(year_date['Brand'] == Brand)]
    #         year_date = year_date.drop_duplicates(subset='Year')
    #         year_date = year_date.sort_values(by='Year')     
    #         year_date['Year'] = year_date['Year'].astype(str) 
    #         year_date_list = year_date['Year'].astype(str).tolist()
    #         year_date_list.insert(0, '-')
    #         self.ui.line_Year.addItems(year_date_list)
        
    #     elif Brand != '-' and LoB != '-':
    #         year_date = year_date[['Year', 'Brand', 'LoB']]
    #         year_date = year_date[(year_date['Brand'] == Brand)]
    #         year_date = year_date[(year_date['LoB'] == LoB)]
    #         year_date = year_date.drop_duplicates(subset='Year')
    #         year_date = year_date.sort_values(by='Year')     
    #         year_date['Year'] = year_date['Year'].astype(str) 
    #         year_date_list = year_date['Year'].astype(str).tolist()
    #         year_date_list.insert(0, '-')
    #         self.ui.line_Year.addItems(year_date_list)
        
    #     elif Brand == '-' and LoB != '-':
    #         year_date = year_date[['Year', 'Brand', 'LoB']]
    #         year_date = year_date[(year_date['LoB'] == LoB)]
    #         year_date = year_date.drop_duplicates(subset='Year')
    #         year_date = year_date.sort_values(by='Year')     
    #         year_date['Year'] = year_date['Year'].astype(str) 
    #         year_date_list = year_date['Year'].astype(str).tolist()
    #         year_date_list.insert(0, '-')
    #         self.ui.line_Year.addItems(year_date_list)


    # def find_Scheme(self):
    #     while (self.table.rowCount() > 0):
    #         self.table.removeRow(0)
                
    #     bonus_request = db.execute(select(Bonus_Scheme.Year, Bonus_Scheme.Brand, Bonus_Scheme.LoB, Bonus_Scheme.Segment, 
    #                                                             Bonus_Scheme.Product_group, Bonus_Scheme.Product_Name, Bonus_Scheme.Pack_group, 
    #                                                             Bonus_Scheme.Pack_group2, Bonus_Scheme.Production, Bonus_Scheme.KSSS_prod, 
    #                                                             Bonus_Scheme.Plan, Bonus_Scheme.Bonus_M, Bonus_Scheme.Bonus_Q, Bonus_Scheme.Bonus_Y, 
    #                                                             Bonus_Scheme.Bonus_Add, Bonus_Scheme.Max_Bonus)).all()
    #     bonus_data = pd.DataFrame(bonus_request)
        
    #     Year = self.ui.line_Year.currentText()
    #     Brand = self.ui.line_Brand.currentText()
    #     LoB = self.ui.line_LoB.currentText()
        
    #     if bonus_data.empty == True:
    #         msg = QMessageBox()
    #         msg.setText('There is no Bonus Scheme in Database\n'
    #                             'Close the program and open agan!\n'
    #                             'Then update Database')
    #         msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                         "font: 10pt  \"Segoe UI\";"
    #                         "color: #4b0082;\n"
    #                         " ")
    #         msg.setIcon(QMessageBox.Critical)
    #         x = msg.exec_()

    #     else:          
    #         bonus_data['Plan'] = bonus_data['Plan'].astype(float)
    #         bonus_data['Bonus_M'] = bonus_data['Bonus_M'].astype(float)
    #         bonus_data['Bonus_Q'] = bonus_data['Bonus_Q'].astype(float)
    #         bonus_data['Bonus_Y'] = bonus_data['Bonus_Y'].astype(float)
    #         bonus_data['Bonus_Add'] = bonus_data['Bonus_Add'].astype(float)
    #         bonus_data['Max_Bonus'] = bonus_data['Max_Bonus'].astype(float)
            
    #         if Year == '-' and Brand == '-' and LoB == '-':
    #             bonus_data = bonus_data
            
    #         elif Year != '-' and Brand == '-' and LoB == '-':
    #             Year = int(Year)
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['Year'] == Year)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)
            
    #         elif Year != '-' and Brand != '-' and LoB == '-':
    #             Year = int(Year)
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['Year'] == Year)]
    #             bonus_data = bonus_data[(bonus_data['Brand'] == Brand)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)
                
    #         elif Year != '-' and Brand == '-' and LoB != '-':
    #             Year = int(Year)
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['Year'] == Year)]
    #             bonus_data = bonus_data[(bonus_data['LoB'] == LoB)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)
            
    #         elif Year != '-' and Brand != '-' and LoB != '-':
    #             Year = int(Year)
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['Year'] == Year)]
    #             bonus_data = bonus_data[(bonus_data['Brand'] == Brand)]
    #             bonus_data = bonus_data[(bonus_data['LoB'] == LoB)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)
            
    #         elif Year == '-' and Brand != '-' and LoB != '-':
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['Brand'] == Brand)]
    #             bonus_data = bonus_data[(bonus_data['LoB'] == LoB)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)

    #         elif Year == '-' and Brand != '-' and LoB == '-':
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['Brand'] == Brand)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)
        
    #         elif Year == '-' and Brand == '-' and LoB != '-':
    #             bonus_data['Year'] = bonus_data['Year'].astype(int)
    #             bonus_data = bonus_data[(bonus_data['LoB'] == LoB)]
    #             bonus_data = bonus_data.reset_index()
    #             bonus_data = bonus_data.drop(['index'], axis = 1)
            
    #         nan_value = float("NaN")
    #         bonus_data.replace("", nan_value, inplace=True)
    #         bonus_data.replace(0, nan_value, inplace=True)
    #         bonus_data.dropna(how='all', axis=1, inplace=True)

    #         headers = bonus_data.columns.values.tolist()

    #         self.table.setColumnCount(len(headers))
    #         self.table.setHorizontalHeaderLabels(headers)

    #         for i, row in bonus_data.iterrows():
    #             # Добавление строки
    #             self.table.setRowCount(self.table.rowCount() + 1)

    #             for j in range(self.table.columnCount()):
    #                 self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

    #         self.table.show()


    # def dowload_Scheme(self):
    #     savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Bonus Scheme.xlsx', 'Excel Workbook (*.xlsx)')
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





