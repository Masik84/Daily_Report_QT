import pandas as pd
import polars as pl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget, QHeaderView
from sqlalchemy.exc import SQLAlchemyError

from db import db, engine
from models import Brand, ProdName, Material
from wind.pages.products_ui import Ui_Form

from config import All_data_file


class Product(QWidget):
    def __init__(self):
        super(Product, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive) # Allow manual resizing
        self.table.horizontalHeader().setStretchLastSection(True) # Stretch last column
        # self.resizeEvent = self.onResize # Connect resize event

        self.fill_in_prod_brand_list()
        self.fill_in_prod_fam_list()
        self.fill_in_prod_name_list()

        self.ui.line_Brand.currentTextChanged.connect(self.fill_in_prod_fam_list)
        self.ui.line_Prod_Fam.currentTextChanged.connect(self.fill_in_prod_name_list)

        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_Product)
        # self.ui.btn_download.clicked.connect(self.dowload_Products)
        

    def onResize(self, event):
        # Resize columns proportionally to available width
        width = self.table.width()
        num_cols = self.table.columnCount()
        col_width = width // num_cols  # Integer division for even distribution
        for i in range(num_cols):
            self.table.setColumnWidth(i, col_width)
        # Adjust last column to fill remaining space
        self.table.setColumnWidth(num_cols - 1, width - (col_width * (num_cols - 1)))


    def get_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_Prod_File.setText(get_file[0])


    def upload_data(self, prod_file_xls):
        prod_file_xls = self.ui.label_Prod_File.text()

        if prod_file_xls == 'Выбери файл или нажми Upload, файл будет взят из основной папки' \
            or prod_file_xls == 'База данных обновлена!'\
            or prod_file_xls == '':
            self.run_product_func(All_data_file)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else:
            self.run_product_func(prod_file_xls)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            
            self.fill_in_prod_brand_list()
            self.fill_in_prod_fam_list()
            self.fill_in_prod_name_list()
        
            self.ui.label_Prod_File.setText("Выбери файл или нажми Upload, файл будет взят из основной папки")


    def run_product_func(self, data_file_xls):
        data = self.read_product_file(data_file_xls)
        self.save_Brand(data)
        self.save_ProdName(data)
        self.save_Material(data)
    
    
    def read_product_file(self, prod_file_xls):
        dict_types_prod = {'Артикул': pl.String, 'Упаковка': pl.Float32, 'Вес Нетто кг': pl.Float32,'Пошлина': pl.Float32, 'ЭкоСбор ставка': pl.Float32, 'Кол-во в упак': pl.Float32, 'Плотность': pl.Float32 }

        prod_df_oil = pl.read_excel(prod_file_xls, sheet_name='Oils', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, schema_overrides = dict_types_prod)
        prod_df_shape = pl.read_excel(prod_file_xls, sheet_name='Other', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, schema_overrides = dict_types_prod)

        columns = ['Упаковка для названия', 'Упаковка', 'Плотность', 'Вес Нетто кг', 'Кол-во в упак', 'Вес Брутто кг', 'Пошлина', 'ЭкоСбор ставка']

        prod_df_oil = prod_df_oil.with_columns(pl.col(columns).cast(pl.Float32))
        prod_df_shape = prod_df_shape.with_columns(pl.col(columns).cast(pl.Float32))

        prod_df = pl.concat([prod_df_oil, prod_df_shape], how="diagonal")
        prod_df = prod_df.rename({'Артикул': 'prod_art', 
                                                    'ID 1C': 'id', 
                                                    'Продукт + упаковка': 'Material_Name', 
                                                    'Product name': 'Product_Name', 
                                                    'Type': 'Type', 
                                                    'Категория': 'Category', 
                                                    'Brand': 'Brand', 
                                                    'Family': 'Family', 
                                                    'Артикул для комплектов': 'prod_art_for_price', 
                                                    'ЕИ в 1С': 'UoM_1C', 
                                                    'ЕИ': 'UoM', 
                                                    'Вид упаковки': 'Pack_type', 
                                                    'Акциз (да/нет)': 'ED_type', 
                                                    'ЭкоСбор (да/нет)': 'Ecofee_type', 
                                                    'Упаковка для названия': 'Pack_for_name', 
                                                    'Упаковка': 'Pack', 
                                                    'Кол-во в упак': 'Pack_qty', 
                                                    'Плотность': 'Density', 
                                                    'Вес Нетто кг': 'Net_Weight', 
                                                    'Вес упаковки': 'Pack_weight', 
                                                    'Вес Брутто кг': 'Gross_weight', 
                                                    'Код ТНВЭД': 'TNVED', 
                                                    'Страна происх.': 'Cntr_of_origin', 
                                                    'Stock strategy': 'Stock_strategy', 
                                                    'Статус': 'Status', 
                                                    'Полное наименование': 'Full_name', 
                                                    'Английское наименование продукта': 'Material_Name_engl', 
                                                    'Комментарий': 'Comment', 
                                                    'ABC': 'ABC', 
                                                    })
        prod_df = prod_df.with_columns(pl.col('id').str.strip_chars()).filter(pl.col('id') != "-")
        
        prod_df = prod_df.to_dicts()
        
        return prod_df


    def save_Material(self, data):
        processed = []
        prod_unique = []

        for row in data:
            if row['id'] not in processed:
                prod = {'id': row['id'],
                            'prod_art': str(row['prod_art']),
                            'prod_art_for_price': str(row['prod_art_for_price']),
                            'Material_Name': row['Material_Name'],
                            "Product_Name" : row['Product_Name'],
                            "Type" : row['Type'],
                            "Category" : row['Category'],
                            "Brand" : row['Brand'],
                            "Family" : row['Family'],
                            'UoM': row['UoM'],
                            'UoM_1C': row['UoM_1C'],
                            'Pack_type': row['Pack_type'],
                            'Pack_for_name': row['Pack_for_name'],
                            'Pack': row['Pack'],
                            'Pack_qty': row['Pack_qty'],
                            'ED_type': row['ED_type'],
                            'Ecofee_type': row['Ecofee_type'],
                            'Density': row['Density'],
                            'Net_Weight': row['Net_Weight'],
                            'Pack_weight': row['Pack_weight'],
                            'Gross_weight': row['Gross_weight'],
                            'TNVED': row['TNVED'],
                            'Cntr_of_origin': row['Cntr_of_origin'],
                            'Stock_strategy': row['Stock_strategy'],
                            'Status': row['Status'],
                            'Full_name': row['Full_name'],
                            'Material_Name_engl': row['Material_Name_engl'],
                            'Comment': row['Comment'],
                            'ABC': row['ABC'],
                            }
                prod_unique.append(prod)
                processed.append(row['id'])

        prod_for_upload = []
        prod_for_update = []
        for mylist in prod_unique:
            prod_exists = Material.query.filter(Material.id == mylist['id']).count()
            if prod_exists == 0 or prod_exists is None:
                new_prod = {'id': mylist['id'],
                                    'prod_art': str(mylist['prod_art']),
                                    'prod_art_for_price': str(mylist['prod_art_for_price']),
                                    'Material_Name': mylist['Material_Name'],
                                    "Product_Name" : mylist['Product_Name'],
                                    "Type" : mylist['Type'],
                                    "Category" : mylist['Category'],
                                    "Brand" : mylist['Brand'],
                                    "Family" : mylist['Family'],
                                    'UoM': mylist['UoM'],
                                    'UoM_1C': mylist['UoM_1C'],
                                    'Pack_type': mylist['Pack_type'],
                                    'Pack_for_name': mylist['Pack_for_name'],
                                    'Pack': mylist['Pack'],
                                    'Pack_qty': mylist['Pack_qty'],
                                    'ED_type': mylist['ED_type'],
                                    'Ecofee_type': mylist['Ecofee_type'],
                                    'Density': mylist['Density'],
                                    'Net_Weight': mylist['Net_Weight'],
                                    'Pack_weight': mylist['Pack_weight'],
                                    'Gross_weight': mylist['Gross_weight'],
                                    'TNVED': mylist['TNVED'],
                                    'Cntr_of_origin': mylist['Cntr_of_origin'],
                                    'Stock_strategy': mylist['Stock_strategy'],
                                    'Status': mylist['Status'],
                                    'Full_name': mylist['Full_name'],
                                    'Material_Name_engl': mylist['Material_Name_engl'],
                                    'Comment': mylist['Comment'],
                                    'ABC': mylist['ABC'],
                                    }
                prod_for_upload.append(new_prod)
            elif prod_exists > 0:
                new_prod = {'id': mylist['id'],
                                    'prod_art': str(mylist['prod_art']),
                                    'prod_art_for_price': str(mylist['prod_art_for_price']),
                                    'Material_Name': mylist['Material_Name'],
                                    "Product_Name" : mylist['Product_Name'],
                                    "Type" : mylist['Type'],
                                    "Category" : mylist['Category'],
                                    "Brand" : mylist['Brand'],
                                    "Family" : mylist['Family'],
                                    'UoM': mylist['UoM'],
                                    'UoM_1C': mylist['UoM_1C'],
                                    'Pack_type': mylist['Pack_type'],
                                    'Pack_for_name': mylist['Pack_for_name'],
                                    'Pack': mylist['Pack'],
                                    'Pack_qty': mylist['Pack_qty'],
                                    'ED_type': mylist['ED_type'],
                                    'Ecofee_type': mylist['Ecofee_type'],
                                    'Density': mylist['Density'],
                                    'Net_Weight': mylist['Net_Weight'],
                                    'Pack_weight': mylist['Pack_weight'],
                                    'Gross_weight': mylist['Gross_weight'],
                                    'TNVED': mylist['TNVED'],
                                    'Cntr_of_origin': mylist['Cntr_of_origin'],
                                    'Stock_strategy': mylist['Stock_strategy'],
                                    'Status': mylist['Status'],
                                    'Full_name': mylist['Full_name'],
                                    'Material_Name_engl': mylist['Material_Name_engl'],
                                    'Comment': mylist['Comment'],
                                    'ABC': mylist['ABC'],
                                    }
                prod_for_update.append(new_prod)
        db.bulk_insert_mappings(Material, prod_for_upload)
        db.bulk_update_mappings(Material, prod_for_update)
        
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

        return prod_unique


    def get_all_Products_from_db(self):
        prod_reques = db.query(Material)
        prod_data = pl.read_database(query=prod_reques.statement, connection=engine)
        
        if prod_data.is_empty() == False:
            prod_data = prod_data
        else:
            prod_data = pl.DataFrame()

        return prod_data


    def find_Product(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        prod_df = self.get_all_Products_from_db()
        
        prod_id = self.ui.line_ID.text()
        prod_art = self.ui.line_Artical.text()
        Product_Name = self.ui.line_Prod_name.currentText()
        Product_Family = self.ui.line_Prod_Fam.currentText()
        Brand = self.ui.line_Brand.currentText()

        if prod_df.is_empty() == True:
            msg = QMessageBox()
            msg.setText('There is no Product data in Database\n'
                                'Close the program and open agan!\n'
                                'Then update Database')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            
        elif prod_id != '':
            prod_df = prod_df.filter(pl.col("id") == prod_id)
            
        elif prod_art != "":
            prod_df = prod_df.filter(pl.col("prod_art") == str(prod_art))

        elif Brand == '-' and Product_Family == '-' and Product_Name == '-':
            prod_df

        elif Brand != '-' and Product_Family == '-' and Product_Name == '-':
            prod_df = prod_df.filter(pl.col("Brand") == Brand)
            
        elif Product_Family != '-' and Product_Name == '-':
            prod_df = prod_df.filter(pl.col("Family") == Product_Family)

        elif Product_Name != '-':
            prod_df = prod_df.filter(pl.col("Product_Name") == Product_Name)

        prod_df = prod_df.to_pandas()
        headers = prod_df.columns.values.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        for i, row in prod_df.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)
            
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(prod_df.iloc[i, j])))
                    

    def fill_in_prod_brand_list(self):
        prod_df = self.get_all_Products_from_db()

        self.ui.line_Brand.clear()

        if prod_df.is_empty() == True:
            prod_brand_list = ['-']
            self.ui.line_Prod_Fam.addItems(prod_brand_list)
        else:
            prod_df = prod_df[['Brand']]
            prod_df = prod_df.unique(subset="Brand").sort("Brand", descending=[False,])
            prod_brand_list = prod_df['Brand'].to_list()
            prod_brand_list.insert(0, '-')
            self.ui.line_Brand.addItems(prod_brand_list)


    def fill_in_prod_fam_list(self):
        prod_df = self.get_all_Products_from_db()

        self.ui.line_Prod_Fam.clear()
        brand = self.ui.line_Brand.currentText()

        if prod_df.is_empty() == True:
            prod_fam_list = ['-']
            self.ui.line_Prod_Fam.addItems(prod_fam_list)
        else:
            prod_df = prod_df[['Brand', 'Family']]

            if brand == '-':
                prod_fam = prod_df[['Family']]
                prod_fam = prod_fam.unique(subset="Family").sort("Family", descending=[False,])
                prod_fam_list = prod_fam['Family'].to_list()
                prod_fam_list.insert(0, '-')
                self.ui.line_Prod_Fam.addItems(prod_fam_list)
            else:
                prod_fam = prod_df[['Brand', 'Family']]
                prod_fam = prod_fam.filter(pl.col("Brand") == brand)
                prod_fam = prod_fam.unique(subset="Family").sort("Family", descending=[False,])
                prod_fam_list = prod_fam['Family'].to_list()
                prod_fam_list.insert(0, '-')
                self.ui.line_Prod_Fam.addItems(prod_fam_list)


    def fill_in_prod_name_list(self):
        prod_in_db = self.get_all_Products_from_db()

        self.ui.line_Prod_name.clear()
        family = self.ui.line_Prod_Fam.currentText()

        if prod_in_db.is_empty() == True:
            prod_name_list = ['-']
            self.ui.line_Prod_name.addItems(prod_name_list)
        else:
            prod_in_db = prod_in_db[['Family', 'Product_Name']]

            if family != '-':
                prod_name = prod_in_db[['Family', 'Product_Name']]
                prod_name = prod_name.filter(pl.col("Family") == family)
                prod_name = prod_name.unique(subset="Product_Name").sort("Product_Name", descending=[False,])
                prod_name_list = prod_name['Product_Name'].to_list()
                prod_name_list.insert(0, '-')
                self.ui.line_Prod_name.addItems(prod_name_list)
                
            else:
                prod_name = prod_in_db[['Product_Name']]
                prod_name = prod_name.unique(subset="Product_Name").sort("Product_Name", descending=[False,])
                prod_name_list = prod_name['Product_Name'].to_list()
                prod_name_list.insert(0, '-')
                self.ui.line_Prod_name.addItems(prod_name_list)


    def dowload_Products(self):
        savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Products.xlsx', 'Excel Workbook (*.xlsx)')
        col_count = self.ui.table.columnCount()
        row_count = self.ui.table.rowCount()
        headers = [str(self.ui.table.horizontalHeaderItem(i).text()) for i in range(col_count)]

        df_list = []
        for row in range(row_count):
            df_list2 = []
            for col in range(col_count):
                table_item = self.ui.table.item(row, col)
                df_list2.append(
                    '' if table_item is None else str(table_item.text()))
            df_list.append(df_list2)

        df = pd.DataFrame(df_list, columns=headers)
        df.to_excel(savePath[0], index=False)

        msg = QMessageBox()
        msg.setText('Report was saved successfully')
        msg.setStyleSheet("background-color: #f8f8f2;\n"
                          "font: 12pt  \"Segoe UI\";"
                          "color: #4b0082;\n"
                          " ")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
