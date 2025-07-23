import numpy as np
import pandas as pd
import polars as pl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import locale

from db import db, engine
from models import Comp_Plans, Cust_Plans, TeamLead, Holding, Sector, Manager, Manager_Prev
from config import All_data_file
from wind.pages.plans_ui import Ui_Form

pd.options.display.float_format = '{:,.2f}'.format

# locale.setlocale(locale.LC_ALL, '')
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
locale._override_localeconv = {'mon_thousands_sep': '.'}

class Plans(QWidget):
    def __init__(self):
        super(Plans, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        
        self.fill_in_year_list()
        self.fill_in_qtr_list()
        self.fill_in_mnth_list()
        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_hold_list()
        self.fill_in_categ_list()
        
        self.ui.line_tl.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.line_kam.currentTextChanged.connect(self.fill_in_hold_list)
        
        self.ui.btn_open_file.setToolTip('выбери файл')
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_Plans)
        # self.ui.btn_download.clicked.connect(self.dowload_Plans)
        
        
    def get_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_plan_File.setText(get_file[0])
 

    def upload_data(self, plan_file_xls):
        plan_file_xls = self.ui.label_plan_File.text()
        if plan_file_xls == 'Выбери файл или нажми Upload, файл будет взят из основной папки' \
            or plan_file_xls == 'База данных обновлена!'\
            or plan_file_xls == '':
            self.run_plans_update(All_data_file)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else:
            self.run_plans_update(plan_file_xls)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            
        self.fill_in_year_list()
        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_hold_list()
        self.fill_in_categ_list()
        
        self.ui.label_plan_File.setText("Выбери файл или нажми Upload, файл будет взят из основной папки")


    def run_plans_update(self, All_data_file):
        comp_plan = self.read_comp_plan(All_data_file)
        self.update_comp_plan(comp_plan)
        
        cust_plan = self.read_cust_plan(All_data_file)
        self.update_cust_plan(cust_plan)
        
    
    def read_comp_plan(self, All_data_file):
        targ_comp_dtypes = {'Year': pl.Int64, 'Quarter': pl.Int64, 'Month': pl.Int64, 'Week of Year': pl.Int64, 'Week of Month': pl.Int64, }
        
        target_by_company = pl.read_excel(All_data_file, sheet_name='Планы ОБЩИЕ', engine='xlsx2csv', 
                                                                engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, 
                                                                schema_overrides=targ_comp_dtypes)
        target_by_company = target_by_company[['Year', 'Quarter', 'Month', 'Week of Year', 'Team Lead', 'ABC', 'Volume Target total', 'Revenue Target total', 'Margin Target total']]
        target_by_company = target_by_company.rename({
                                                                'Week of Year': 'Week_of_Year',
                                                                'Team Lead': 'TeamLead',
                                                                'ABC': 'Prod_cat',
                                                                'Volume Target total': 'Volume_Target_total',
                                                                'Revenue Target total': 'Revenue_Target_total',
                                                                'Margin Target total': 'Margin_Target_total'})
        target_by_company = target_by_company.with_columns(pl.concat_str([pl.col('Year'), pl.col("Month"), pl.col('Week_of_Year'), pl.col('TeamLead'), pl.col('Prod_cat'),], separator='_', ignore_nulls=True).alias('merge'))
        target_by_company = target_by_company.with_columns(pl.col(["Volume_Target_total", "Revenue_Target_total", "Margin_Target_total"]).round(2))
        target_by_company = target_by_company.to_dicts()
        return target_by_company


    def read_cust_plan(self, All_data_file):
        targer_dtypes = {'Year': pl.Int64,  'Quarter': pl.Int64, 'Month': pl.Int64, 'Volume Target': pl.Float32, 'Margin Target': pl.Float32, }
        target_by_sales = pl.read_excel(All_data_file, sheet_name='Планы по Холдингам', engine='xlsx2csv', 
                                                            engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, 
                                                            schema_overrides=targer_dtypes)
        target_by_sales = target_by_sales[['Year', 'Quarter', 'Month', 'ХОЛДИНГ', 'Менеджер', 'Менеджер_prev', 'SECTOR', 'STL', 'Team Lead', 'Volume Target cust', 'Margin Target cust']]
        target_by_sales = target_by_sales.rename({
                                                                'ХОЛДИНГ': 'Holding',
                                                                'SECTOR': 'Sector',
                                                                'Менеджер': 'AM',
                                                                'Менеджер_prev': 'AM_prev',
                                                                'Volume Target cust': 'Volume_target',
                                                                'Margin Target cust': 'Margin_target'})
        target_by_sales = target_by_sales.with_columns(pl.concat_str([pl.col('Year'), pl.col('Month'), pl.col('Holding')], separator='_', ignore_nulls=True).alias('merge'))
        target_by_sales = target_by_sales.with_columns(pl.col(["Volume_target", "Margin_target"]).round(2))
        target_by_sales = target_by_sales.to_dicts()
        return target_by_sales

            
    def update_comp_plan(self, data):
            processed = []
            comp_plan_unique = []
            for row in data:
                if row['merge'] not in processed:
                    comp_plan = {'merge': row['merge'],
                                            'Year': row['Year'],
                                            'Quarter': row['Quarter'],
                                            'Month': row['Month'],
                                            'Week_of_Year': row['Week_of_Year'],
                                            'TeamLead_id': self.get_id_TeamLead(row['TeamLead']),
                                            'Prod_cat': row['Prod_cat'],
                                            'Volume_Target_total': row['Volume_Target_total'],
                                            'Revenue_Target_total': row['Revenue_Target_total'],
                                            'Margin_Target_total': row['Margin_Target_total']
                                            }
                    comp_plan_unique.append(comp_plan)
                    processed.append(comp_plan['merge'])

            comp_plan_for_upload = []
            comp_plan_for_update = []
            for mylist in comp_plan_unique:
                comp_plan_exists = Comp_Plans.query.filter(Comp_Plans.merge == mylist['merge']).count()
                if comp_plan_exists == 0:
                    new_comp_plan = {'merge': mylist['merge'],
                                                    'Year': mylist['Year'],
                                                    'Quarter': mylist['Quarter'],
                                                    'Month': mylist['Month'],
                                                    'Week_of_Year': mylist['Week_of_Year'],
                                                    'TeamLead_id': mylist['TeamLead_id'],
                                                    'Prod_cat': mylist['Prod_cat'],
                                                    'Volume_Target_total': mylist['Volume_Target_total'],
                                                    'Revenue_Target_total': mylist['Revenue_Target_total'],
                                                    'Margin_Target_total': mylist['Margin_Target_total']
                                                    }
                    comp_plan_for_upload.append(new_comp_plan)

                elif comp_plan_exists >0:
                    new_comp_plan = {'id': self.get_id_Comp_Plan(mylist['merge']), 
                                                    'merge': mylist['merge'],
                                                    'Year': mylist['Year'],
                                                    'Quarter': mylist['Quarter'],
                                                    'Month': mylist['Month'],
                                                    'Week_of_Year': mylist['Week_of_Year'],
                                                    'TeamLead_id': mylist['TeamLead_id'],
                                                    'Prod_cat': mylist['Prod_cat'],
                                                    'Volume_Target_total': mylist['Volume_Target_total'],
                                                    'Revenue_Target_total': mylist['Revenue_Target_total'],
                                                    'Margin_Target_total': mylist['Margin_Target_total']
                                                    }
                    print(new_comp_plan)
                    comp_plan_for_update.append(new_comp_plan)

            db.bulk_insert_mappings(Comp_Plans, comp_plan_for_upload)
            db.bulk_update_mappings(Comp_Plans, comp_plan_for_update)
            
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
            return comp_plan_unique


    def update_cust_plan(self, data):
        processed = []
        cust_plan_unique = []
        for row in data:
            if row['merge'] not in processed:
                cust_plan = {'merge': row['merge'],
                                        'Year': row['Year'],
                                        'Quarter': row['Quarter'],
                                        'Month': row['Month'],
                                        'Holding_id': self.get_id_Holding(row['Holding']),
                                        'Volume_target': row['Volume_target'],
                                        'Margin_target': row['Margin_target']
                                        }
                cust_plan_unique.append(cust_plan)
                processed.append(cust_plan['merge'])

        cust_plan_for_upload = []
        cust_plan_for_update = []
        for mylist in cust_plan_unique:
            cust_plan_exists = Cust_Plans.query.filter(Cust_Plans.merge == mylist['merge']).count()
            if cust_plan_exists == 0:
                new_cust_plan = {'merge': mylist['merge'],
                                            'Year': mylist['Year'],
                                            'Quarter': mylist['Quarter'],
                                            'Month': mylist['Month'],
                                            'Holding_id': mylist['Holding_id'],
                                            'Volume_target': mylist['Volume_target'],
                                            'Margin_target': mylist['Margin_target']
                                            }
                cust_plan_for_upload.append(new_cust_plan)

            elif cust_plan_exists >0:
                new_cust_plan = {'id': self.get_id_Cust_Plan(mylist['merge']), 
                                            'merge': mylist['merge'],
                                            'Year': mylist['Year'],
                                            'Quarter': mylist['Quarter'],
                                            'Month': mylist['Month'],
                                            'Holding_id': mylist['Holding_id'],
                                            'Volume_target': mylist['Volume_target'],
                                            'Margin_target': mylist['Margin_target']
                                            }
                cust_plan_for_update.append(new_cust_plan)

        db.bulk_insert_mappings(Cust_Plans, cust_plan_for_upload)
        db.bulk_update_mappings(Cust_Plans, cust_plan_for_update)
        
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
        return cust_plan_unique
      
    
    def get_comp_plan_from_db(self):
        comp_plan_reques = db.query(Comp_Plans, TeamLead).join(TeamLead)
        comp_plan_data_db = pl.read_database(query=comp_plan_reques.statement, connection=engine)
        
        if comp_plan_data_db.is_empty() == False:
            comp_plan_data_db = comp_plan_data_db[["Year", "Quarter", "Month", "Week_of_Year", "TeamLead", "Prod_cat", "Volume_Target_total", "Revenue_Target_total", "Margin_Target_total"]]
            comp_plan_data_db = (comp_plan_data_db.sort("Year", "Quarter", "Month", "Week_of_Year", descending=[False, False, False, False])
                                                                                .with_columns(pl.col("Volume_Target_total", "Revenue_Target_total", "Margin_Target_total").cast(pl.Float32)))
            
        
        else:
            comp_plan_data_db = pl.DataFrame()
        
        return comp_plan_data_db


    def get_cust_plan_from_db(self):
        cust_plan_reques = db.query(Cust_Plans)
        cust_plan_data_db = pl.read_database(query=cust_plan_reques.statement, connection=engine)
        
        if cust_plan_data_db.is_empty() == False:
            holding_request = db.query(Holding)
            holding_data_db = pl.read_database(query=holding_request.statement, connection=engine)
            
            sector_request = db.query(Sector)
            sector_data_db = pl.read_database(query=sector_request.statement, connection=engine)
            
            kam_request = db.query(Manager, TeamLead).join(TeamLead)
            kam_data_db = pl.read_database(query=kam_request.statement, connection=engine)
            
            cust_plan_data_db = cust_plan_data_db.join(holding_data_db, how="left", left_on="Holding_id", right_on="id")
            cust_plan_data_db = cust_plan_data_db.join(kam_data_db, how="left", left_on="AM_id", right_on="id")
            cust_plan_data_db = cust_plan_data_db.join(sector_data_db, how="left", left_on="Sector_id", right_on="id")
            cust_plan_data_db = cust_plan_data_db[["Year", "Quarter", "Month", "Holding", "Sector", "TeamLead", "AM", "Volume_target", "Margin_target"]]
            cust_plan_data_db = (cust_plan_data_db.sort("Year", "Quarter", "Month", "Holding", descending=[False, False, False, False])
                                                                            .with_columns(pl.col("Volume_target", "Margin_target").cast(pl.Float32)))
        
        else:
            cust_plan_data_db = pl.DataFrame()
        
        return cust_plan_data_db
    
    
    def find_Plans(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
                
        comp_plan_df = self.get_comp_plan_from_db()
        cust_plan_df = self.get_cust_plan_from_db()
        
        Plan_type = self.ui.line_plan_type.currentText()
        Year = self.ui.line_Year.currentText()
        Qtr = self.ui.line_Qtr.currentText()
        Mnth = self.ui.line_Mnth.currentText()
        TL = self.ui.line_tl.currentText()
        AM = self.ui.line_kam.currentText()
        Hold = self.ui.line_Holding.currentText()
        Prod_cat = self.ui.line_ABC.currentText()
        
        if Plan_type == "-":
            msg = QMessageBox()
            msg.setText('Выбери тип Плана!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            plan_df = pl.DataFrame()
        
        else:
            if Plan_type == "План Общий":
                if comp_plan_df.is_empty() == True:
                    msg = QMessageBox()
                    msg.setText('Нет данных в БД')
                    msg.setStyleSheet("background-color: #f8f8f2;\n"
                                    "font: 10pt  \"Tahoma\";"
                                    "color: #ff0000;\n"
                                    " ")
                    msg.setIcon(QMessageBox.Critical)
                    x = msg.exec_()
                    
                if Year != '-' and Qtr == '-' and Mnth == '-' and TL == '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Prod_cat") == Prod_cat))

                elif Year != '-' and Qtr != '-' and Mnth == '-' and TL == '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Quarter") == int(Qtr)) & 
                                                                    (pl.col("Prod_cat") == Prod_cat))
                    
                elif Year != '-' and Mnth != '-' and TL == '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) &
                                                                    (pl.col("Prod_cat") == Prod_cat))
                    
                elif Year != '-' and Mnth != '-' and TL != '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) &
                                                                    (pl.col("TeamLead") == TL) &
                                                                    (pl.col("Prod_cat") == Prod_cat))
                    
                elif Year != '-' and Mnth != '-' and TL != '-' and Prod_cat != '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) &
                                                                    (pl.col("TeamLead") == TL) & 
                                                                    (pl.col("Prod_cat") == Prod_cat) )
                #============================================================================
                elif Year != '-' and TL != '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("TeamLead") == TL) &
                                                                    (pl.col("Prod_cat") == Prod_cat))
                    
                elif Year != '-' and TL != '-' and Prod_cat != '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("TeamLead") == TL) & 
                                                                    (pl.col("Prod_cat") == Prod_cat) )
                    
                elif Year != '-' and TL == '-' and Prod_cat != '-' :
                    plan_df = comp_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Prod_cat") == Prod_cat) )
                #============================================================================
                elif Year == '-' and Qtr != '-' and Mnth == '-' and TL == '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Quarter") == int(Qtr))  )
                    
                elif Year == '-' and Qtr != '-' and Mnth == '-' and TL != '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Quarter") == int(Qtr)) & 
                                                                    (pl.col("TeamLead") == TL) )
                
                elif Year == '-' and Qtr != '-' and Mnth == '-' and TL != '-' and Prod_cat != '-' :
                    plan_df = comp_plan_df.filter((pl.col("Quarter") == int(Qtr)) & 
                                                                    (pl.col("TeamLead") == TL) & 
                                                                    (pl.col("Prod_cat") == Prod_cat) )
                #============================================================================
                elif Year == '-' and Mnth != '-' and TL == '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Month") == int(Mnth))  )
                    
                elif Year == '-' and Mnth != '-' and TL != '-' and Prod_cat == '-' :
                    plan_df = comp_plan_df.filter((pl.col("Month") == int(Mnth)) & 
                                                                    (pl.col("TeamLead") == TL) )
                
                elif Year == '-' and Mnth != '-' and TL != '-' and Prod_cat != '-' :
                    plan_df = comp_plan_df.filter((pl.col("Month") == int(Mnth)) & 
                                                                    (pl.col("TeamLead") == TL) & 
                                                                    (pl.col("Prod_cat") == Prod_cat) )
                #============================================================================
                else:
                    plan_df = comp_plan_df
                
            elif Plan_type == "План КАМ-Клиент":
                if Year != '-' and Qtr == '-' and Mnth == '-' and TL == '-' and AM == '-' and Hold == '-':
                    plan_df = cust_plan_df.filter(pl.col("Year") == int(Year))

                elif Year != '-' and Qtr != '-' and Mnth == '-' and TL == '-' and AM == '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Quarter") == int(Qtr)))
                
                elif Year != '-' and Qtr != '-' and Mnth == '-' and TL != '-' and AM == '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Quarter") == int(Qtr)) & 
                                                                    (pl.col("TeamLead") == TL))
                    
                elif Year != '-' and Qtr != '-' and Mnth == '-' and AM != '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Quarter") == int(Qtr)) & 
                                                                    (pl.col("AM") == AM) )
                
                elif Year != '-' and Qtr != '-' and Mnth == '-' and Hold != '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Quarter") == int(Qtr)) & 
                                                                    (pl.col("Holding") == Hold) )
                    
                elif Year != '-' and Mnth != '-' and TL == '-' and AM == '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)))
                
                elif Year != '-' and Mnth != '-' and TL != '-' and AM == '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) & 
                                                                    (pl.col("TeamLead") == TL))
                    
                elif Year != '-' and Mnth != '-' and AM != '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) & 
                                                                    (pl.col("AM") == AM) )
                
                elif Year != '-' and Mnth != '-' and Hold != '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) & 
                                                                    (pl.col("Holding") == Hold) )
                #============================================================================
                elif Year != '-' and TL != '-' and AM == '-' and Hold == '-' :
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("TeamLead") == TL) )
                    
                elif Year != '-' and AM != '-' and Hold == '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("AM") == AM) )
                    
                elif Year != '-' and Hold != '-':
                    plan_df = cust_plan_df.filter((pl.col("Year") == int(Year)) & 
                                                                    (pl.col("Month") == int(Mnth)) &
                                                                    (pl.col("Holding") == Hold) )
                
                else:
                    plan_df = cust_plan_df

            else:
                plan_df = pl.concat([comp_plan_df, cust_plan_df], how='diagonal')

                plan_df = plan_df.to_pandas()

            if Plan_type == "План Общий":
                sum_pl_vol = plan_df['Volume_Target_total'].sum()
                sum_pl_vol = locale._format("%.0f", sum_pl_vol, grouping=True)
                self.ui.label_Volume.setText(f'{sum_pl_vol} л.')
                
                sum_pl_rev = plan_df['Revenue_Target_total'].sum()
                sum_pl_rev = locale._format("%.0f", sum_pl_rev, grouping=True)
                self.ui.label_Revenue.setText(f'{sum_pl_rev} р')
                
                sum_pl_c3 = plan_df['Margin_Target_total'].sum()
                sum_pl_c3 = locale._format("%.0f", sum_pl_c3, grouping=True)
                self.ui.label_Margin.setText(f'{sum_pl_c3} р')
                
                sum_pl_uc3 = float(plan_df['Margin_Target_total'].sum()) / float(plan_df['Volume_Target_total'].sum())
                sum_pl_uc3 = locale._format("%.0f", sum_pl_uc3, grouping=True)
                self.ui.label_uC3.setText(f'{sum_pl_uc3} р/л')

            elif Plan_type == "План КАМ-Клиент":
                sum_pl_vol = plan_df['Volume_target'].sum()
                sum_pl_vol = locale._format("%.0f", sum_pl_vol, grouping=True)
                self.ui.label_Volume.setText(f'{sum_pl_vol} л.')
                
                sum_pl_rev = 0
                self.ui.label_Revenue.setText(f'{sum_pl_rev} р')
                
                sum_pl_c3 = plan_df['Margin_target'].sum()
                sum_pl_c3 = locale._format("%.0f", sum_pl_c3, grouping=True)
                self.ui.label_Margin.setText(f'{sum_pl_c3} р')
                
                sum_pl_uc3 = float(plan_df['Margin_target'].sum()) / float(plan_df['Volume_target'].sum())
                sum_pl_uc3 = locale._format("%.0f", sum_pl_uc3, grouping=True)
                self.ui.label_uC3.setText(f'{sum_pl_uc3} р/л')
            
            else:
                self.ui.label_Volume.setText(f'0 л')
                self.ui.label_Revenue.setText(f'0 р')
                self.ui.label_Margin.setText(f'0 р')
                self.ui.label_uC3.setText(f'0 р/л')
            
            plan_df = plan_df.to_pandas()
            headers = plan_df.columns.values.tolist()
            
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)

            for i, row in plan_df.iterrows():
                self.table.setRowCount(self.table.rowCount() + 1)
                
                for j in range(self.table.columnCount()):
                    self.table.setItem(i, j, QTableWidgetItem(str(plan_df.iloc[i, j])))

    def fill_in_year_list(self):
        period_request = db.execute(select(Comp_Plans.Year)).all()
        year_date = pl.DataFrame(period_request)
        
        self.ui.line_Year.clear()

        if year_date.is_empty() == True:
            self.ui.line_Year.addItem('-')
            
        else:
            year_date = year_date[['Year']]
            year_date = year_date.unique(subset="Year").sort("Year", descending=[False,])
            year_date = year_date.with_columns(pl.col("Year").cast(pl.String))
            year_date_list = year_date['Year'].to_list()
            year_date_list.insert(0, '-')
            self.ui.line_Year.addItems(year_date_list)

    def fill_in_qtr_list(self):      
        qtr_date = ["-", "1", "2", "3", "4"]
        self.ui.line_Qtr.addItems(qtr_date)
    
    def fill_in_mnth_list(self):      
        qtr_date = ["-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",]
        self.ui.line_Mnth.addItems(qtr_date)

    def fill_in_kam_list(self):
        KAM_data = self.get_cust_plan_from_db()
        
        self.ui.line_kam.clear()

        if KAM_data.is_empty() == True:
            self.ui.line_kam.addItem('-')

        else:
            KAM_data = KAM_data[['AM']]
            KAM_data = KAM_data.unique(subset="AM").sort("AM", descending=[False,])
            KAM_list = KAM_data['AM'].to_list()
            KAM_list.insert(0, '-')
            self.ui.line_kam.addItems(KAM_list)     
            
    def fill_in_tl_list(self):
        reques = db.query(TeamLead)
        TL_data = pl.read_database(query=reques.statement, connection=engine)
        
        self.ui.line_tl.clear()

        if TL_data.is_empty() == True:
            self.ui.line_tl.addItem('-')

        else:
            TL_data = TL_data[['TeamLead']]
            TL_data = TL_data.unique(subset="TeamLead").sort("TeamLead", descending=[False,])
            TL_list = TL_data['TeamLead'].to_list()
            # TL_list.insert(0, '-')
            self.ui.line_tl.addItems(TL_list)

    def fill_in_hold_list(self):
        Hold_data = self.get_cust_plan_from_db()
        
        self.ui.line_Holding.clear()
        
        TL = self.ui.line_tl.currentText()
        AM = self.ui.line_kam.currentText()

        if Hold_data.is_empty() == True:
            self.ui.line_Holding.addItem('-')
            
        elif TL != '-':
            Hold_data = Hold_data[['Holding', 'TeamLead']]
            Hold_data = Hold_data.filter(pl.col('TeamLead') == TL)
            Hold_data = Hold_data.unique(subset="Holding").sort("Holding", descending=[False,])
            Hold_list = Hold_data['Holding'].to_list()
            Hold_list.insert(0, '-')
            self.ui.line_Holding.addItems(Hold_list)
        
        elif AM != '-':
            Hold_data = Hold_data[['Holding', 'AM']]
            Hold_data = Hold_data.filter(pl.col('AM') == AM)
            Hold_data = Hold_data.unique(subset="Holding").sort("Holding", descending=[False,])
            Hold_list = Hold_data['Holding'].to_list()
            Hold_list.insert(0, '-')
            self.ui.line_Holding.addItems(Hold_list)
            
        else:
            Hold_data = Hold_data[['Holding']]
            Hold_data = Hold_data.unique(subset="Holding").sort("Holding", descending=[False,])
            Hold_list = Hold_data['Holding'].to_list()
            Hold_list.insert(0, '-')
            self.ui.line_Holding.addItems(Hold_list)     
            
    def fill_in_categ_list(self):
        cat_data = self.get_comp_plan_from_db()
        
        self.ui.line_ABC.clear()

        if cat_data.is_empty() == True:
            self.ui.line_ABC.addItem('-')
            
        else:
            cat_data = cat_data[['Prod_cat', ]]
            cat_data = cat_data.unique(subset="Prod_cat").sort("Prod_cat", descending=[False,])
            cat_list = cat_data['Prod_cat'].to_list()
            # cat_list.insert(0, '-')
            self.ui.line_ABC.addItems(cat_list)
        

    def dowload_Plans(self):
        savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Bonus Plans.xlsx', 'Excel Workbook (*.xlsx)')
        col_count = self.ui.table.columnCount()
        row_count = self.ui.table.rowCount()
        headers = [str(self.ui.table.horizontalHeaderItem(i).text()) for i in range(col_count)]

        df_list = []
        for row in range(row_count):
            df_list2 = []
            for col in range(col_count):
                table_item = self.ui.table.item(row,col)
                df_list2.append('' if table_item is None else str(table_item.text()))
            df_list.append(df_list2)

        df = pd.DataFrame(df_list, columns=headers)
        df.to_excel(savePath[0], index=False)

        msg = QMessageBox()
        msg.setText('Report was saved successfully')
        msg.setStyleSheet("background-color: #f8f8f2;\n"
                        "font: 12pt  \"Tahoma\";"
                        "color: #4b0082;\n"
                        " ")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()


    def get_id_Comp_Plan(self, merge):
        db_data = Comp_Plans.query.filter(Comp_Plans.merge == merge).first()
        comp_pl_id = db_data.id
        return comp_pl_id


    def get_id_TeamLead(self, TeamLead_name):
        db_data = TeamLead.query.filter(TeamLead.TeamLead == TeamLead_name).first()
        tl_id = db_data.id

        return tl_id


    def get_id_Cust_Plan(self, merge):
        db_data = Cust_Plans.query.filter(Cust_Plans.merge == merge).first()
        comp_pl_id = db_data.id
        return comp_pl_id


    def get_id_Holding(self, holding):
        db_data = Holding.query.filter(Holding.Holding == holding).first()
        holding_id = db_data.id
        return holding_id


    def get_id_Sector(self, sector):
        db_data = Sector.query.filter(Sector.Sector == sector).first()
        sector_id = db_data.id

        return sector_id


    def get_id_AM(self, AM_name):
        db_data = Manager.query.filter(Manager.AM == AM_name).first()
        am_id = db_data.id

        return am_id


    def get_id_AM_prev(self, AM_name):
        db_data = Manager_Prev.query.filter(Manager_Prev.AM_prev == AM_name).first()
        am_prev_id = db_data.id

        return am_prev_id
  