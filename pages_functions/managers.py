import os
import pandas as pd
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, 
                              QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from db import db, engine
from models import TeamLead, STL, Manager
from wind.pages.managers_ui import Ui_Form
from config import All_data_file


class Managers(QWidget):
    def __init__(self):
        super(Managers, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self._setup_ui()
        self._setup_connections()
        
        self._initialize_comboboxes()


    def _setup_ui(self):
        """Универсальная настройка таблицы для всех классов"""
        self.table = self.ui.table
        
        # Основные настройки таблицы
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)  # Чередование цветов строк
        
        # Настройки заголовков
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        # Оптимизация производительности
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)


    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.line_tl.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.btn_open_file_manager.setToolTip('Выбери файл ! ALL DATA !.xlsx')
        self.ui.btn_open_file_manager.clicked.connect(self.get_file)
        self.ui.btn_upload_file_manager.clicked.connect(self.upload_data)
        self.ui.btn_find_KAM.clicked.connect(lambda: self._find_data('KAM'))
        self.ui.btn_find_STL.clicked.connect(lambda: self._find_data('STL'))
        self.ui.btn_find_TL.clicked.connect(lambda: self._find_data('TL'))


    def _initialize_comboboxes(self):
        """Инициализация выпадающих списков при старте"""
        try:
            # Проверяем наличие данных в БД
            has_data = db.session.query(Manager).first() is not None
            
            if has_data:
                # Заполняем списки
                self._fill_combobox(self.ui.line_kam, 'Manager_name')
                self._fill_combobox(self.ui.line_stl, 'STL_name')
                self._fill_combobox(self.ui.line_tl, 'TeamLead_name')
            else:
                # Просто инициализируем пустые списки с "-"
                for combobox in [self.ui.line_kam, self.ui.line_stl, self.ui.line_tl]:
                    combobox.clear()
                    combobox.addItem('-')
                    
        except Exception as e:
            print(f"Ошибка инициализации списков: {e}")
            # Гарантируем, что списки будут с "-" даже при ошибке
            for combobox in [self.ui.line_kam, self.ui.line_stl, self.ui.line_tl]:
                combobox.clear()
                combobox.addItem('-')


    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Выберите файл', 
            '', 
            'Excel Files (*.xlsx *.xls)'
        )
        if file_path:
            self.ui.label_manager_File.setText(file_path)


    def upload_data(self):
        """Загрузка данных в базу"""
        file_path = self.ui.label_manager_File.text()
        
        # Используем файл по умолчанию, если не выбран конкретный
        if not file_path or file_path in ('Выбери файл или нажми Upload, файл будет взят из основной папки', 
                                        'База данных обновлена!'):
            file_path = All_data_file
        
        try:
            # Проверка существования файла (новый код)
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден. Проверьте наличие файла в папке.")
                
            # Удаляем явное создание транзакции
            self._process_upload(file_path)
            self._show_message('База данных обновлена!')
            self._refresh_comboboxes()
            
        except Exception as e:
            db.session.rollback()
            
            # Улучшенное сообщение об ошибке (новый код)
            if "transaction is already begun" in str(e):
                user_message = (
                    "Ошибка при работе с базой данных.\n\n"
                    "Пожалуйста:\n"
                    "1. Закройте программу\n"
                    "2. Откройте её снова\n"
                    "3. Попробуйте повторить операцию\n\n"
                    "Если ошибка повторяется, обратитесь в техническую поддержку."
                )
            else:
                user_message = (
                    f"Ошибка при загрузке данных: {str(e)}\n\n"
                    "Рекомендуемые действия:\n"
                    "1. Проверьте, что файл не открыт в другой программе\n"
                    "2. Проверьте правильность формата файла\n"
                    "3. Попробуйте снова"
                )
                
            self._show_message(user_message, is_error=True)
            
        finally:
            self.ui.label_manager_File.setText("Выбери файл или нажми Upload, файл будет взят из основной папки")


    def _process_upload(self, file_path):
        """Обработка и сохранение данных из файла"""
        # Чтение данных из Excel
        tl_data = self._read_excel_sheet(file_path, 'TL_emails')
        stl_data = self._read_excel_sheet(file_path, 'STL_emails')
        
        # Чтение данных менеджеров
        am_data = self._read_excel_sheet(file_path, 'AM_emails')
        
        # Сначала сохраняем STL и TeamLead, чтобы были их ID
        self._save_stls(stl_data)
        self._save_team_leads(tl_data)
        
        # Затем сохраняем менеджеров
        self._save_managers(am_data)


    def _read_excel_sheet(self, file_path, sheet_name, rename_cols=None, fillna_cols=None, fillna_value=None):
        """Чтение листа Excel с переименованием колонок и заменой пустых значений"""
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Специфичные переименования для каждого листа
        if sheet_name == 'AM_emails':
            renames = {
                'AM': 'Manager_name',
                'Team Lead': 'TeamLead_name',
                'STL': 'STL_name',
                'Отчет': 'Has_report',
                'AM_1C name': 'AM_1C_Name',
                'Ссылка на отчет': 'Report_link'
            }
        elif sheet_name == 'STL_emails':
            renames = {
                'STL': 'STL_name',
                'Ссылка на отчет': 'Report_link'
            }
        elif sheet_name == 'TL_emails':
            renames = {
                'Team Lead': 'TeamLead_name',
                'Отчет': 'Has_report',
                'Ссылка на отчет': 'Report_link'
            }
        else:
            renames = {}
        
        # Применяем переименования
        df = df.rename(columns=renames)
        
        # Дополнительные переименования, если указаны
        if rename_cols:
            df = df.rename(columns=rename_cols)
        
        # Замена пустых значений
        if fillna_cols and fillna_value is not None:
            existing_cols = [col for col in fillna_cols if col in df.columns]
            df[existing_cols] = df[existing_cols].fillna(fillna_value)
        
        return df.where(pd.notnull(df), None).to_dict('records')


    def _save_team_leads(self, data):
        """Сохранение TeamLead"""
        self._save_data(
            model=TeamLead,
            data=data,
            name_field='TeamLead_name',  # Используем точное имя поля из модели
            extra_fields={
                'Email': 'email',
                'Has_report': 'Has_report',
                'Report_link': 'Ссылка на отчет'
            }
        )


    def _save_stls(self, data):
        """Сохранение STL"""
        self._save_data(
            model=STL,
            data=data,
            name_field='STL_name',  # Используем точное имя поля из модели
            extra_fields={
                'Email': 'email',
                'Report_link': 'Ссылка на отчет'
            }
        )


    def _save_managers(self, data):
        """Сохранение менеджеров с обработкой пустых значений"""
        if not data:
            return

        unique_data = []
        processed_names = set()
        
        for row in data:
            manager_name = row.get('Manager_name')
            if not manager_name or manager_name in ('-', 'no') or manager_name in processed_names:
                continue
                
            # Обработка email
            email = row.get('email', '-')
            if email == '-':
                email = None
                
            # Получаем ID STL (если указан)
            stl_name = row.get('STL_name', '-')
            stl_id = None
            if stl_name and stl_name != '-':
                stl = db.query(STL).filter(STL.STL_name == stl_name).first()
                stl_id = stl.id if stl else None
                
            # Получаем ID TeamLead (если указан)
            teamlead_name = row.get('TeamLead_name', '-')
            teamlead_id = None
            if teamlead_name and teamlead_name != '-':
                teamlead = db.query(TeamLead).filter(TeamLead.TeamLead_name == teamlead_name).first()
                teamlead_id = teamlead.id if teamlead else None
                
            # Формируем запись для сохранения
            item = {
                'Manager_name': manager_name,
                'Email': email,
                'STL_id': stl_id,
                'TeamLead_id': teamlead_id,
                'Has_report': row.get('Has_report', 'нет') if row.get('Has_report', '-') != '-' else None,
                'AM_1C_Name': row.get('AM_1C_Name', '') if row.get('AM_1C_Name', '-') != '-' else None,
                'Report_link': row.get('Report_link', '') if row.get('Report_link', '-') != '-' else None
            }
            
            unique_data.append(item)
            processed_names.add(manager_name)

        # Сохраняем данные
        try:
            if unique_data:
                # Сначала обновляем существующие записи
                existing_names = {m[0] for m in db.query(Manager.Manager_name).all()}
                
                to_insert = []
                to_update = []
                
                for item in unique_data:
                    if item['Manager_name'] in existing_names:
                        # Получаем ID существующего менеджера
                        manager = db.query(Manager).filter(Manager.Manager_name == item['Manager_name']).first()
                        if manager:
                            item['id'] = manager.id
                            to_update.append(item)
                    else:
                        to_insert.append(item)
                
                if to_insert:
                    db.session.bulk_insert_mappings(Manager, to_insert)
                if to_update:
                    db.session.bulk_update_mappings(Manager, to_update)
                
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Ошибка при сохранении менеджеров: {str(e)}")
        finally:
            db.session.close()


    def _save_data(self, model, data, name_field, extra_fields=None):
        """
        Общий метод для сохранения данных
        :param model: SQLAlchemy модель
        :param data: список словарей с данными
        :param name_field: поле с именем (используется как есть, без добавления суффиксов)
        :param extra_fields: дополнительные поля {поле_в_модели: поле_в_данных}
        """
        if not data:
            return

        extra_fields = extra_fields or {}
        
        # Получаем существующие имена из базы
        name_column = getattr(model, name_field)  # Получаем столбец модели
        existing_names = {name[0] for name in db.query(name_column).all()}
        
        to_insert = []
        to_update = []
        
        for row in data:
            name = row[name_field]
            if not name or name in ('-', 'no'):
                continue
                
            item = {
                name_field: name,  # Используем имя поля как есть
                **{k: row.get(v, '') for k, v in extra_fields.items()}
            }
            
            if name in existing_names:
                # Получаем ID существующей записи
                item['id'] = db.query(model.id).filter(name_column == name).scalar()
                to_update.append(item)
            else:
                to_insert.append(item)

        try:
            if to_insert:
                db.session.bulk_insert_mappings(model, to_insert)
            if to_update:
                db.session.bulk_update_mappings(model, to_update)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Не удалось сохранить данные в базу: {str(e)}")
        finally:
            db.session.close()


    def _get_id(self, model, name_field, name):
        """Получение ID по имени"""
        if not name or name in ('-', 'no'):
            return None
            
        item = db.query(model).filter(getattr(model, name_field) == name).first()
        return item.id if item else None


    def _refresh_comboboxes(self):
        """Обновление всех выпадающих списков"""
        try:
            self.fill_in_kam_list()
            self.fill_in_stl_list()
            self.fill_in_tl_list()
        except Exception as e:
            print(f"Ошибка обновления списков: {e}")
            self._show_message("Ошибка обновления списков. Попробуйте снова.", is_error=True)


    def get_all_managers_data(self):
        """Получение всех данных менеджеров из базы"""
        query = select(
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
        ).join(STL, Manager.STL_id == STL.id)\
         .join(TeamLead, Manager.TeamLead_id == TeamLead.id)
        
        return pd.read_sql(query, engine)


    def _find_data(self, data_type):
        """Поиск данных по типу (KAM, STL, TL)"""
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        
        try:
            df = self.get_all_managers_data()
            if df.empty:
                raise ValueError('Нет данных в базе')
            
            df = self._filter_data(df, data_type)
            self._display_data(df, data_type)
            
        except Exception as e:
            self._show_message(
                f'Ошибка при поиске данных: {str(e)}\n'
                'Закройте программу и откройте снова!\n'
                'Затем обновите базу данных',
                is_error=True
            )


    def _filter_data(self, df, data_type):
        """Фильтрация данных в зависимости от типа"""
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
            return df[['STL_name', "email_STL", 'TeamLead_name']].drop_duplicates(subset=["STL_name"])
        
        else:  # TL
            if tl != '-':
                df = df[df['TeamLead_name'] == tl]
            return df[["Manager_name", 'TeamLead_name', "email_TL"]].drop_duplicates(subset=["TeamLead_name"])


    def _display_data(self, df, data_type):
        """Отображение данных в таблице"""
        sort_column = {
            'KAM': 'Manager_name',
            'STL': 'STL_name',
            'TL': 'TeamLead_name'
        }.get(data_type, 'Manager_name')
        
        df = df.sort_values(sort_column)
        headers = df.columns.tolist()
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))


    def _fill_combobox(self, combobox, column):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        
        try:
            # Проверяем соединение с БД
            db.session.execute(text('SELECT 1')).scalar()
            
            if column == 'Manager_name':
                items = db.session.query(Manager.Manager_name).distinct().all()
            elif column == 'STL_name':
                items = db.session.query(STL.STL_name).distinct().all()
            elif column == 'TeamLead_name':
                items = db.session.query(TeamLead.TeamLead_name).distinct().all()
            else:
                return
                
            # Фильтруем и сортируем результаты
            valid_items = sorted([item[0] for item in items if item[0]])
            if valid_items:
                combobox.addItems(valid_items)
                
        except Exception as e:
            print(f"Ошибка при заполнении комбобокса {column}: {e}")
            # В случае ошибки хотя бы оставляем "-" в списке



    def fill_in_kam_list(self):
        self._fill_combobox(self.ui.line_kam, 'Manager_name')
                
    def fill_in_stl_list(self):
        self._fill_combobox(self.ui.line_stl, 'STL_name')
                
    def fill_in_tl_list(self):
        self._fill_combobox(self.ui.line_tl, 'TeamLead_name')


    def _show_message(self, text, is_error=False):
        """Показать сообщение пользователю"""
        msg = QMessageBox()
        msg.setText(text)
        style = """
            background-color: #f8f8f2;
            font: 10pt "Tahoma";
            color: #ff0000;
        """ if is_error else """
            background-color: #f8f8f2;
            font: 10pt "Tahoma";
            color: #237508;
        """
        msg.setStyleSheet(style)
        msg.setIcon(QMessageBox.Critical if is_error else QMessageBox.Information)
        msg.exec_()