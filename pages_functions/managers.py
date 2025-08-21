import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget,
                              QTableWidgetItem, QWidget, QApplication, QTextEdit)
from PySide6.QtCore import Qt
from functools import lru_cache

from db import db, engine
from models import TeamLead, STL, Manager
from wind.pages.managers_ui import Ui_Form
from config import All_data_file


class ManagersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._setup_ui()
        self._setup_connections()
        self._initialize_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.table = self.ui.table
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.line_tl.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.btn_open_file_manager.clicked.connect(self.get_file)
        self.ui.btn_upload_file_manager.clicked.connect(self.upload_data)
        self.ui.btn_find_KAM.clicked.connect(lambda: self._find_data('KAM'))
        self.ui.btn_find_STL.clicked.connect(lambda: self._find_data('STL'))
        self.ui.btn_find_TL.clicked.connect(lambda: self._find_data('TL'))

    def _initialize_comboboxes(self):
        """Инициализация выпадающих списков"""
        self.fill_in_kam_list()
        self.fill_in_stl_list()
        self.fill_in_tl_list()

    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Выберите файл ALL DATA', 
            '', 
            'Excel Files (*.xlsx *.xls)'
        )
        if file_path:
            self.ui.label_manager_File.setText(file_path)

    def upload_data(self):
        """Загрузка данных в базу"""
        file_path = self.ui.label_manager_File.text()
        if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
            file_path = All_data_file

        try:
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")

            try:
                self._process_upload(file_path)
                db.commit()
                self.show_message('Данные менеджеров загружены!')
                self._refresh_comboboxes()
            except Exception as e:
                db.rollback()
                raise
            finally:
                db.close()

        except Exception as e:
            self._handle_upload_error(e, "продуктов")

    def _handle_upload_error(self, error):
        """Обработка ошибок загрузки"""
        if "transaction is already begun" in str(error):
            msg = "Ошибка БД. Закройте программу и попробуйте снова."
        elif "required columns" in str(error).lower():
            msg = "Файл не содержит всех необходимых столбцов."
        else:
            msg = f"Ошибка загрузки данных менеджеров: {str(error)}"
        self.show_error_message(msg)

    def _process_upload(self, file_path):
        """Обработка и сохранение данных из файла"""
        tl_data = self._read_excel_sheet(file_path, 'TL_emails')
        stl_data = self._read_excel_sheet(file_path, 'STL_emails')
        am_data = self._read_excel_sheet(file_path, 'AM_emails')

        self._save_team_leads(tl_data)
        self._save_stls(stl_data)
        self._save_managers(am_data)

    def _read_excel_sheet(self, file_path, sheet_name):
        """Чтение листа Excel"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            if sheet_name == 'AM_emails':
                column_map = {
                    'AM': 'Manager_name',
                    'Team Lead': 'TeamLead_name',
                    'STL': 'STL_name',
                    'Отчет': 'Has_report',
                    'AM_1C name': 'AM_1C_Name',
                    'Ссылка на отчет': 'Report_link'
                }
            elif sheet_name == 'STL_emails':
                column_map = {
                    'STL': 'STL_name',
                    'Ссылка на отчет': 'Report_link'
                }
            elif sheet_name == 'TL_emails':
                column_map = {
                    'Team Lead': 'TeamLead_name',
                    'Отчет': 'Has_report',
                    'Ссылка на отчет': 'Report_link'
                }
            else:
                column_map = {}

            df = df.rename(columns=column_map)
            return df.where(pd.notnull(df), None).to_dict('records')

        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла {sheet_name}: {str(e)}")
            return []

    def _save_team_leads(self, data):
        """Сохранение TeamLead"""
        self._save_data(
            model=TeamLead,
            data=data,
            name_field='TeamLead_name',
            extra_fields={
                'Email': 'email',
                'Has_report': 'Has_report',
                'Report_link': 'Report_link'
            }
        )

    def _save_stls(self, data):
        """Сохранение STL"""
        self._save_data(
            model=STL,
            data=data,
            name_field='STL_name',
            extra_fields={
                'Email': 'email',
                'Report_link': 'Report_link'
            }
        )

    def _save_managers(self, data):
        """Сохранение менеджеров"""
        if not data:
            return

        existing_managers = {m.Manager_name: m for m in db.query(Manager).all()}
        to_insert = []
        to_update = []

        for row in data:
            manager_name = row.get('Manager_name')
            if not manager_name or manager_name in ('-', 'no'):
                continue

            stl_id = self._get_id(STL, 'STL_name', row.get('STL_name'))
            teamlead_id = self._get_id(TeamLead, 'TeamLead_name', row.get('TeamLead_name'))

            manager_data = {
                'Manager_name': manager_name,
                'Email': row.get('email'),
                'STL_id': stl_id,
                'TeamLead_id': teamlead_id,
                'Has_report': row.get('Has_report'),
                'AM_1C_Name': row.get('AM_1C_Name'),
                'Report_link': row.get('Report_link')
            }

            if manager_name in existing_managers:
                manager_data['id'] = existing_managers[manager_name].id
                to_update.append(manager_data)
            else:
                to_insert.append(manager_data)

        try:
            if to_insert:
                db.bulk_insert_mappings(Manager, to_insert)
            if to_update:
                db.bulk_update_mappings(Manager, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения менеджеров: {str(e)}")
        finally:
            db.close()

    def _save_data(self, model, data, name_field, extra_fields=None):
        """Общий метод для сохранения данных"""
        if not data:
            return

        extra_fields = extra_fields or {}
        existing_names = {getattr(item, name_field): item.id for item in db.query(model).all()}
        to_insert = []
        to_update = []

        for row in data:
            name = row.get(name_field)
            if not name or name in ('-', 'no'):
                continue

            item_data = {
                name_field: name,
                **{k: row.get(v) for k, v in extra_fields.items()}
            }

            if name in existing_names:
                item_data['id'] = existing_names[name]
                to_update.append(item_data)
            else:
                to_insert.append(item_data)

        try:
            if to_insert:
                db.bulk_insert_mappings(model, to_insert)
            if to_update:
                db.bulk_update_mappings(model, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения данных: {str(e)}")
        finally:
            db.close()

    @lru_cache(maxsize=32)
    def _get_id(self, model, name_field, name):
        """Получение ID по имени"""
        if not name or name in ('-', 'no'):
            return None

        item = db.query(model).filter(getattr(model, name_field) == name).first()
        return item.id if item else None

    def _refresh_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self.fill_in_kam_list()
        self.fill_in_stl_list()
        self.fill_in_tl_list()

    def get_all_managers_data(self):
        """Получение всех данных менеджеров из базы"""
        query = db.query(
            Manager.id,
            Manager.Manager_name,
            Manager.Email,
            Manager.Has_report,
            Manager.Report_link,
            Manager.AM_1C_Name,
            STL.id.label('STL_id'),
            STL.STL_name,
            STL.Email.label('email_STL'),
            TeamLead.id.label('TeamLead_id'),
            TeamLead.TeamLead_name,
            TeamLead.Email.label('email_TL')
        ).outerjoin(STL, Manager.STL_id == STL.id)\
         .outerjoin(TeamLead, Manager.TeamLead_id == TeamLead.id)

        df = pd.read_sql(query.statement, db.bind)
        return df.where(pd.notnull(df), None)

    def _find_data(self, data_type):
        """Поиск данных по типу (KAM, STL, TL)"""
        self.table.clearContents()
        self.table.setRowCount(0)

        try:
            df = self.get_all_managers_data()
            if df.empty:
                raise ValueError('Нет данных в базе')

            df = self._filter_data(df, data_type)
            self._display_data(df)

        except Exception as e:
            self.show_error_message(f'Ошибка при поиске данных: {str(e)}')

    def _filter_data(self, df, data_type):
        """Фильтрация данных"""
        kam = self.ui.line_kam.currentText()
        stl = self.ui.line_stl.currentText()
        tl = self.ui.line_tl.currentText()

        if data_type == 'KAM':
            if kam != '-':
                df = df[df['Manager_name'] == kam]
            elif stl != '-':
                df = df[df['STL_name'] == stl]
            elif tl != '-':
                df = df[df['TeamLead_name'] == tl]
            return df[['Manager_name', 'Email', 'Has_report', 'STL_name', 'TeamLead_name']]
        
        elif data_type == 'STL':
            if stl != '-':
                df = df[df['STL_name'] == stl]
            elif tl != '-':
                df = df[df['TeamLead_name'] == tl]
            return df[['STL_name', 'email_STL', 'TeamLead_name']].drop_duplicates(subset=['STL_name'])
        
        else:  # TL
            if tl != '-':
                df = df[df['TeamLead_name'] == tl]
            return df[['TeamLead_name', 'email_TL']].drop_duplicates(subset=['TeamLead_name'])

    def _display_data(self, df):
        """Отображение данных в таблице"""
        self.table.clear()
        self.table.setColumnCount(len(df.columns))

        if df.empty:
            self.show_error_message('Ничего не найдено')
            return
        
        # Подготовка данных
        df = df.fillna('')
        headers = df.columns.tolist()
        
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(df))

        for i in range(len(df)):
            for j, col in enumerate(headers):
                value = df.iloc[i][col]
                value_str = str(value)

                item = QTableWidgetItem(value_str)

                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(i, j, item)

    def _fill_combobox(self, combobox, column):
        """Заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')

        if column == 'Manager_name':
            items = db.query(Manager.Manager_name).distinct().all()
        elif column == 'STL_name':
            items = db.query(STL.STL_name).distinct().all()
        elif column == 'TeamLead_name':
            items = db.query(TeamLead.TeamLead_name).distinct().all()
        else:
            return

        valid_items = sorted([item[0] for item in items if item[0]])
        if valid_items:
            combobox.addItems(valid_items)

    def fill_in_kam_list(self):
        """Заполнение списка менеджеров"""
        self._fill_combobox(self.ui.line_kam, 'Manager_name')

    def fill_in_stl_list(self):
        """Заполнение списка STL"""
        self._fill_combobox(self.ui.line_stl, 'STL_name')

    def fill_in_tl_list(self):
        """Заполнение списка TeamLead"""
        self._fill_combobox(self.ui.line_tl, 'TeamLead_name')

    def show_message(self, text):
            """Показать компактное информационное сообщение"""
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setIcon(QMessageBox.Information)
            msg.setText(text)
            
            # Уменьшаем размер окна
            msg.setMinimumSize(400, 200)
            
            # Добавляем кнопку Copy
            copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
            ok_button = msg.addButton(QMessageBox.Ok)
            
            # Настройка буфера обмена
            clipboard = QApplication.clipboard()
            
            # Обработчики кнопок
            def copy_text():
                clipboard.setText(text)
            
            copy_button.clicked.connect(copy_text)
            
            # Показываем сообщение
            msg.exec_()

    def show_error_message(self, text):
        """Показать компактное сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        
        # Уменьшаем размер окна
        msg.setMinimumSize(400, 200)
        
        # Добавляем кнопку Copy
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        # Настройка буфера обмена
        clipboard = QApplication.clipboard()
        
        # Обработчики кнопок
        def copy_text():
            clipboard.setText(text)
        
        copy_button.clicked.connect(copy_text)
        
        # Показываем сообщение
        msg.exec_()
        
     
        