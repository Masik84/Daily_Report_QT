import pandas as pd
import polars as pl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QWidget
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import db, Base, engine

from models import TeamLead, STL, Manager, Manager_Prev
from wind.pages.managers_ui import Ui_Form

from config import All_data_file


class Managers(QWidget):
    def __init__(self):
        super(Managers, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.fill_in_kam_list()
        self.fill_in_stl_list()
        self.fill_in_tl_list()

        self.ui.line_tl.currentTextChanged.connect(self.fill_in_kam_list)
        
        self.table = self.ui.table
        self.ui.table.resizeColumnsToContents()

        self.ui.btn_open_file_manager.setToolTip('выбери файл ! ALL DATA !.xlsx')
        self.ui.btn_open_file_manager.clicked.connect(self.get_kam_file)
        self.ui.btn_upload_file_manager.clicked.connect(self.upload_data)

        self.ui.btn_find_KAM.clicked.connect(self.find_KAM)
        self.ui.btn_find_STL.clicked.connect(self.find_STL)
        self.ui.btn_find_TL.clicked.connect(self.find_TL)


    def get_kam_file(self):
        get_file = QFileDialog.getOpenFileName(self, 'Choose File')
        if get_file:
            self.ui.label_manager_File.setText(get_file[0])
            

    def upload_data(self, kam_file_xls):
        kam_file_xls = self.ui.label_manager_File.text()
        if kam_file_xls == 'Выбери файл или нажми Upload, файл будет взят из основной папки' \
            or kam_file_xls == 'База данных обновлена!'\
            or kam_file_xls == '':
            self.run_manager_func(All_data_file)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        else:
            self.run_manager_func(kam_file_xls)
            msg = QMessageBox()
            msg.setText('База данных обновлена!')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #237508;\n"
                            " ")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            
        self.fill_in_kam_list()
        self.fill_in_stl_list()
        self.fill_in_tl_list()
        
        self.ui.label_manager_File.setText("Выбери файл или нажми Upload, файл будет взят из основной папки")


    def run_manager_func(self, data_file_xls):
        TL = self.read_TeamLead(data_file_xls)
        STL = self.read_STL_file(data_file_xls)
        KAM = self.read_manager_file(data_file_xls)
        
        self.save_TeamLead(TL)
        self.save_STL(STL)
        self.save_AM(KAM)


    def read_manager_file(self, data_file_xls):
        df = pl.read_excel(data_file_xls, sheet_name='AM_emails', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, )
        df = df.rename({'Team Lead': 'TeamLead', 'Отчет': 'Report'})
        KAM_df = df.to_dicts()
        
        return KAM_df


    def read_STL_file(sefl, data_file_xls):
        df = pl.read_excel(data_file_xls, sheet_name='STL_emails', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, )
        STL_df = df.to_dicts()
        
        return STL_df


    def read_TeamLead(self, data_file_xls):
        df = pl.read_excel(data_file_xls, sheet_name='TL_emails', engine='xlsx2csv', engine_options={"skip_hidden_rows": False, "ignore_formats": ["float"]}, )
        df = df.rename({'Team Lead': 'TeamLead'})
        TL_df = df.to_dicts()
        
        return TL_df


    def save_STL(self, data):
        processed = []
        stl_unique = []
        for row in data:
            if row['STL'] not in processed:
                stl = {'STL': row['STL'], 'email': row['email'],}
                stl_unique.append(stl)
                processed.append(stl['STL'])

        stl_for_upload = []
        stl_for_upload_new = []
        for mylist in stl_unique:
            stl_exists = STL.query.filter(STL.STL == mylist['STL']).count()
            if stl_exists == 0:
                new_stl = {'STL': mylist['STL'], 'email': mylist['email']}
                stl_for_upload_new.append(new_stl)
            elif stl_exists > 0:
                new_stl = {'id': self.get_id_STL(mylist['STL']), 'STL': mylist['STL'], 'email': mylist['email']}
                stl_for_upload.append(new_stl)

        db.bulk_insert_mappings(STL, stl_for_upload_new)
        db.bulk_update_mappings(STL, stl_for_upload)
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

        return stl_unique


    def get_id_STL(self, STL_name):
        db_data = STL.query.filter(STL.STL == STL_name).first()
        stl_id = db_data.id
        return stl_id


    def save_TeamLead(self, data):
        processed = []
        tl_unique = []
        for row in data:
            if row['TeamLead'] not in processed:
                tl = {'TeamLead': row['TeamLead'], 'email': row['email'],}
                tl_unique.append(tl)
                processed.append(tl['TeamLead'])

        tl_for_upload = []
        tl_for_update = []
        for mylist in tl_unique:
            tl_exists = TeamLead.query.filter(TeamLead.TeamLead == mylist['TeamLead']).count()
            if tl_exists == 0:
                new_tl = {'TeamLead': mylist['TeamLead'], 'email': mylist['email']}
                tl_for_upload.append(new_tl)
            elif tl_exists > 0:
                new_tl = {'id': self.get_id_TeamLead(mylist['TeamLead']), 'TeamLead': mylist['TeamLead'], 'email': mylist['email']}
                tl_for_update.append(new_tl)

        db.bulk_insert_mappings(TeamLead, tl_for_upload)
        db.bulk_update_mappings(TeamLead, tl_for_update)
        
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

        return tl_unique


    def get_id_TeamLead(elf, TeamLead_name):
        db_data = TeamLead.query.filter(TeamLead.TeamLead == TeamLead_name).first()
        tl_id = db_data.id

        return tl_id


    def save_AM(self, data):
        processed = []
        am_unique = []
        for row in data:
            if row['AM'] not in processed:
                am = {'AM': row['AM'],
                            'email': row['email'],
                            'STL_id': self.get_id_STL(row['STL']),
                            'TeamLead_id': self.get_id_TeamLead(row['TeamLead']),
                            'Report': row['Report'],
                            }
                am_unique.append(am)
                processed.append(am['AM'])

        am_for_upload = []
        am_prev_for_upload = []
        am_for_update = []
        am_prev_for_update = []
        for mylist in am_unique:
            am_exists = Manager.query.filter(Manager.AM == mylist['AM']).count()
            if am_exists == 0:
                new_am = {'AM': mylist['AM'],
                                    'email': mylist['email'],
                                    'STL_id': mylist['STL_id'],
                                    'TeamLead_id': mylist['TeamLead_id'],
                                    'Report': mylist['Report'],}
                new_am_prev = {'AM_prev': mylist['AM'],
                                            'email': mylist['email'],
                                            'STL_id': mylist['STL_id'],
                                            'TeamLead_id': mylist['TeamLead_id'],
                                            'Report': mylist['Report'],}
                am_for_upload.append(new_am)
                am_prev_for_upload.append(new_am_prev)
            elif am_exists > 0:
                am_list = {'id' : self.get_id_AM(mylist['AM']),
                                    'AM': mylist['AM'],
                                    'email': mylist['email'],
                                    'STL_id': mylist['STL_id'],
                                    'TeamLead_id': mylist['TeamLead_id'],
                                    'Report': mylist['Report'],}
                am_prev_list = {'id' : self.get_id_AM_prev(mylist['AM']),
                                        'AM_prev': mylist['AM'],
                                        'email': mylist['email'],
                                        'STL_id': mylist['STL_id'],
                                        'TeamLead_id': mylist['TeamLead_id'],
                                        'Report': mylist['Report'],}
                am_for_update.append(am_list)
                am_prev_for_update.append(am_prev_list)

        db.bulk_insert_mappings(Manager, am_for_upload)
        db.bulk_insert_mappings(Manager_Prev, am_prev_for_upload)
        db.bulk_update_mappings(Manager, am_for_update)
        db.bulk_update_mappings(Manager_Prev, am_prev_for_update)
        
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

        return am_unique


    def get_id_AM(self, AM_name):
        db_data = Manager.query.filter(Manager.AM == AM_name).first()
        am_id = db_data.id

        return am_id


    def get_id_AM_prev(self, AM_name):
        db_data = Manager_Prev.query.filter(Manager_Prev.AM_prev == AM_name).first()
        am_prev_id = db_data.id

        return am_prev_id


    def get_all_kam_from_db(self):
        KAM_request = db.query(Manager, STL, TeamLead).join(STL).join(TeamLead)
        KAM_data = pl.read_database(query=KAM_request.statement, connection=engine)
        if KAM_data.is_empty() == False:
            KAM_data = KAM_data.rename({"email_1": "email_STL", "email_2": "email_TL"})
            all_KAM_data = KAM_data[['AM', 'email', 'Report', 'STL_id', 'STL', "email_STL", 'TeamLead_id', 'TeamLead', "email_TL", ]]
            all_KAM_data = all_KAM_data.sort("AM", descending=[False])
        else:
            all_KAM_data = pl.DataFrame()
            
        return all_KAM_data

            
    def find_KAM(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        KAM_df = self.get_all_kam_from_db()
        
        KAM_name = self.ui.line_kam.currentText()
        STL_name = self.ui.line_stl.currentText()
        TL_name = self.ui.line_tl.currentText()

        if KAM_df.is_empty() == True:
            msg = QMessageBox()
            msg.setText('There is no Manager data in Database\n'
                                'Close the program and open agan!\n'
                                'Then update Database')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

        elif KAM_name != '-' and STL_name == '-' and TL_name == '-' :
            KAM_df = KAM_df.filter(pl.col("AM") == KAM_name)
            
        elif KAM_name == '-' and STL_name != '-' and TL_name == '-' :
            KAM_df = KAM_df.filter(pl.col("STL") == STL_name)
            
        elif KAM_name == '-' and STL_name == '-' and TL_name != '-' :
            KAM_df = KAM_df.filter(pl.col("TeamLead") == TL_name)
            
        elif KAM_name != '-' and TL_name != '-' :
            KAM_df = KAM_df.filter(pl.col("TeamLead") == TL_name)            
        else:
            KAM_df = KAM_df
        
        KAM_df = KAM_df[['AM', 'email', 'Report', 'STL', 'TeamLead', ]]
        KAM_df = KAM_df.sort("AM", descending=[False])
        
        KAM_df = KAM_df.to_pandas()
        headers = KAM_df.columns.values.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in KAM_df.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)
            
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(KAM_df.iloc[i, j])))


    def find_STL(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        STL_df = self.get_all_kam_from_db()

        STL_name = self.ui.line_stl.currentText()
        TL_name = self.ui.line_tl.currentText()

        if STL_df.is_empty() == True:
            msg = QMessageBox()
            msg.setText('There is no STL data in Database\n'
                                'Close the program and open agan!\n'
                                'Then update Database')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            
        elif STL_name != '-' and TL_name == '-' :
            STL_df = STL_df.filter(pl.col("STL") == STL_name)  
            
        elif TL_name != '-' :
            STL_df = STL_df.filter(pl.col("TeamLead") == TL_name)
              
        else:
            STL_df = STL_df
        
        STL_df = STL_df[['STL', "email_STL", 'TeamLead', ]]        
        STL_df = STL_df.unique(subset=["STL"]).sort("STL", descending=[False])
        
        STL_df = STL_df.to_pandas()
        headers = STL_df.columns.values.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setColumnCount(len(STL_df.columns))
        
        for i, row in STL_df.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)
            
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))


    def find_TL(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        TL_df = self.get_all_kam_from_db()
        
        KAM_name = self.ui.line_kam.currentText()
        TL_name = self.ui.line_tl.currentText()

        if TL_df.is_empty() == True:
            msg = QMessageBox()
            msg.setText('There is no TL data in Database\n'
                                'Close the program and open agan!\n'
                                'Then update Database')
            msg.setStyleSheet("background-color: #f8f8f2;\n"
                            "font: 10pt  \"Tahoma\";"
                            "color: #ff0000;\n"
                            " ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            
        elif KAM_name != '-' and TL_name == '-' :
            TL_df = TL_df.filter(pl.col("AM") == KAM_name)  
            
        elif TL_name != '-' :
            TL_df = TL_df.filter(pl.col("TeamLead") == TL_name)
                
        else:
            TL_df = TL_df
        
        TL_df = TL_df[["AM", 'TeamLead', "email_TL",  ]]
        TL_df = TL_df.unique(subset=["TeamLead"]).sort("TeamLead", descending=[False])
        
        TL_df = TL_df.to_pandas()
        headers = TL_df.columns.values.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setColumnCount(len(TL_df.columns))
        
        for i, row in TL_df.iterrows():
            self.table.setRowCount(self.table.rowCount() + 1)
            
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

    
    def fill_in_kam_list(self):
        KAM_data = self.get_all_kam_from_db()
        
        self.ui.line_kam.clear()

        if KAM_data.is_empty() == True:
            self.ui.line_kam.addItem('-')

        else:
            KAM_data = KAM_data[['AM']]
            KAM_data = KAM_data.unique(subset="AM").sort("AM", descending=[False,])
            KAM_list = KAM_data['AM'].to_list()
            # KAM_list.insert(0, '-')
            self.ui.line_kam.addItems(KAM_list)
            
            
    def fill_in_stl_list(self):
        STL_data = self.get_all_kam_from_db()

        self.ui.line_stl.clear()

        if STL_data.is_empty() == True:
            self.ui.line_tl.addItem('-')

        else:
            STL_data = STL_data[['STL']]
            STL_data = STL_data.unique(subset="STL").sort("STL", descending=[False,])
            STL_list = STL_data['STL'].to_list()
            # STL_list.insert(0, '-')
            self.ui.line_stl.addItems(STL_list)
            
            
    def fill_in_tl_list(self):
        TL_data = self.get_all_kam_from_db()
        
        self.ui.line_tl.clear()

        if TL_data.is_empty() == True:
            self.ui.line_tl.addItem('-')

        else:
            TL_data = TL_data[['TeamLead']]
            TL_data = TL_data.unique(subset="TeamLead").sort("TeamLead", descending=[False,])
            TL_list = TL_data['TeamLead'].to_list()
            # TL_list.insert(0, '-')
            self.ui.line_tl.addItems(TL_list)


    # def fill_in_mnth_list(self):
    #     mnth_request = db.execute(select(Delivery_Tarif.year, Delivery_Tarif.mnth)).all()
    #     mnth_data = pd.DataFrame(mnth_request)

    #     self.ui.line_Mnth.clear()
    #     year = self.ui.line_Year.currentText()

    #     if mnth_data.empty == True:
    #         self.ui.line_Mnth.addItem('-')
            
    #     elif year != '-' or year != '':
    #         mnth_N = mnth_data[['year', 'mnth']]
    #         mnth_N['year'] = mnth_N['year'].astype(str)
    #         mnth_N = mnth_N[(mnth_N['year'] == year)]
    #         mnth_N = mnth_N.drop_duplicates(subset=['mnth'])
    #         mnth_N = mnth_N.sort_values(by=['mnth'])
    #         mnth_N['mnth'] = mnth_N['mnth'].astype(str)
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('0','00')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('1','01')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('2','02')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('3','03')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('4','04')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('5','05')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('6','06')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('7','07')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('8','08')
    #         mnth_N['mnth'] = mnth_N['mnth'].replace('9','09')
    #         # mnth_N['mnth'] = mnth_N.apply(self.check_Mnth, axis=1)
    #         mnth_N['mnth'].astype(str)
    #         mnth_N_list = mnth_N['mnth'].tolist()
    #         mnth_N_list.insert(0, '-')
    #         self.ui.line_Mnth.addItems(mnth_N_list)

    #     else:
    #         mnth_N = mnth_data[['mnth']]
    #         mnth_N = mnth_N.drop_duplicates()
    #         mnth_N = mnth_N.sort_values(by=['mnth'])
    #         mnth_N['mnth'] = mnth_N['mnth'].astype(str)
    #         mnth_N['mnth'] = mnth_N.apply(self.check_Mnth, axis=1)
    #         mnth_N_list = mnth_N['mnth'].tolist()
    #         mnth_N_list.insert(0, '-')
    #         self.ui.line_Mnth.addItems(mnth_N_list)


    # def dowload_Tarif(self):
    #     savePath = QFileDialog.getSaveFileName(None, 'Blood Hound', 'Tarif_date.xlsx', 'Excel Workbook (*.xlsx)')
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
    #     msg.setText('Database Updated')
    #     msg.setStyleSheet("background-color: #f8f8f2;\n"
    #                     "font: 12pt  \"Segoe UI\";"
    #                     "color: #4b0082;\n"
    #                     " ")
    #     msg.setIcon(QMessageBox.Information)
    #     x = msg.exec_()

