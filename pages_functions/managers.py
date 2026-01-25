import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QMessageBox, QHeaderView, QTableWidget,
                              QTableWidgetItem, QWidget, QApplication, QMenu)
from PySide6.QtCore import Qt
from functools import lru_cache

from db import db, engine
from models import TeamLead, STL, Manager, Team
from wind.pages.managers_ui import Ui_Form
from config import All_data_file


class ManagersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._updating_table = False
        self._original_values = {}
        self._pending_changes = {}
        
        self._setup_ui()
        self._setup_connections()
        self._initialize_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.table = self.ui.table
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)
        
        # Настройка контекстного меню
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        """Показ контекстного меню"""
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        delete_action = menu.addAction("Удалить строку")
        apply_action = menu.addAction("Применить изменения")
        revert_action = menu.addAction("Отменить изменения")
        
        copy_action.triggered.connect(self.copy_selected_data)
        delete_action.triggered.connect(self.delete_selected_row)
        apply_action.triggered.connect(self.apply_pending_changes)
        revert_action.triggered.connect(self.revert_changes)
        
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def copy_selected_data(self):
        """Копирование выделенных данных"""
        selected_items = self.table.selectedItems()
        if selected_items:
            clipboard = QApplication.clipboard()
            if len(selected_items) == 1:
                text = selected_items[0].text()
            else:
                # Копирование нескольких ячеек
                rows = {}
                for item in selected_items:
                    row = item.row()
                    col = item.column()
                    if row not in rows:
                        rows[row] = {}
                    rows[row][col] = item.text()
                
                sorted_rows = sorted(rows.items())
                text = ""
                for row, cols in sorted_rows:
                    sorted_cols = sorted(cols.items())
                    text += "\t".join([text for col, text in sorted_cols]) + "\n"
            
            clipboard.setText(text.strip())

    def delete_selected_row(self):
        """Удаление выбранной строки из базы данных"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            return
            
        # Подтверждение удаления
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить {len(selected_rows)} строк?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
            
        try:
            for row in sorted(selected_rows, reverse=True):
                # Получаем данные строки
                row_data = {}
                for col in range(self.table.columnCount()):
                    header = self.table.horizontalHeaderItem(col).text()
                    item = self.table.item(row, col)
                    if item:
                        row_data[header] = item.text()
                
                # Определяем тип данных и удаляем
                data_type = self._get_current_data_type()
                if data_type == 'KAM':
                    manager_name = row_data.get('Manager_name')
                    if manager_name:
                        manager = db.query(Manager).filter(Manager.Manager_name == manager_name).first()
                        if manager:
                            db.delete(manager)
                elif data_type == 'STL':
                    stl_name = row_data.get('STL_name')
                    if stl_name:
                        stl = db.query(STL).filter(STL.STL_name == stl_name).first()
                        if stl:
                            db.delete(stl)
                elif data_type == 'TL':
                    tl_name = row_data.get('TeamLead_name')
                    if tl_name:
                        tl = db.query(TeamLead).filter(TeamLead.TeamLead_name == tl_name).first()
                        if tl:
                            db.delete(tl)
            
            db.commit()
            self.show_message(f'Удалено {len(selected_rows)} строк')
            
            # Обновляем таблицу и комбобоксы
            self._refresh_comboboxes()
            if hasattr(self, '_current_data_type'):
                self._find_data(self._current_data_type)
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f'Ошибка удаления: {str(e)}')

    def on_item_changed(self, item):
        """Обработчик изменения данных в таблице"""
        if self._updating_table:
            return
        
        try:
            row = item.row()
            column = item.column()
            header = self.table.horizontalHeaderItem(column).text()
            
            # Получаем уникальный идентификатор строки
            row_id = self._get_row_id(row)
            if not row_id:
                return
                
            new_value = item.text()
            
            # Сохраняем изменение
            if row_id not in self._pending_changes:
                self._pending_changes[row_id] = {}
            
            self._pending_changes[row_id][header] = new_value
            
            # Подсвечиваем измененную ячейку
            item.setBackground(Qt.yellow)
            
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")

    def _get_row_id(self, row):
        """Получение уникального идентификатора строки"""
        data_type = getattr(self, '_current_data_type', 'KAM')
        
        if data_type == 'KAM':
            item = self.table.item(row, 0)  # Manager_name
        elif data_type == 'STL':
            item = self.table.item(row, 0)  # STL_name
        elif data_type == 'TL':
            item = self.table.item(row, 0)  # TeamLead_name
        else:
            return None
            
        return item.text() if item else None

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.table.itemChanged.connect(self.on_item_changed)
        self.ui.line_tl.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find_KAM.clicked.connect(lambda: self._find_data('KAM'))
        self.ui.btn_find_STL.clicked.connect(lambda: self._find_data('STL'))
        self.ui.btn_find_TL.clicked.connect(lambda: self._find_data('TL'))

    def _initialize_comboboxes(self):
        """Инициализация выпадающих списков"""
        self.fill_in_kam_list()
        self.fill_in_stl_list()
        self.fill_in_tl_list()

    def upload_data(self):
        """Загрузка данных менеджеров в базу"""
        try:
            # Используем файл из конфига
            file_path = All_data_file
            
            if not os.path.exists(file_path):
                raise Exception(f"Файл {os.path.basename(file_path)} не найден")

            # Обработка загрузки
            self._process_upload(file_path)
            
            # Показываем сообщение в label
            self.show_message('Данные менеджеров обновлены успешно!')
            
            # Обновляем комбобоксы
            self._refresh_comboboxes()
            
        except Exception as e:
            self.show_error_message(f"Ошибка загрузки: {str(e)}")

    def _process_upload(self, file_path):
        """Обработка и сохранение данных из файла"""
        try:
            # Читаем все листы
            tl_data = self._read_excel_sheet(file_path, 'TL_emails')
            stl_data = self._read_excel_sheet(file_path, 'STL_emails')
            am_data = self._read_excel_sheet(file_path, 'AM_emails')
            
            # Сохраняем данные в правильном порядке
            self._save_teams(am_data, stl_data, tl_data)  # Сначала команды
            self._save_team_leads(tl_data)
            self._save_stls(stl_data)
            self._save_managers(am_data)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise

    def _read_excel_sheet(self, file_path, sheet_name):
        """Чтение листа Excel"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Маппинг колонок для каждого листа
            if sheet_name == 'AM_emails':
                column_map = {
                    'AM': 'Manager_name',
                    'email': 'Email',
                    'STL': 'STL_name',
                    'Team Lead': 'TeamLead_name',
                    'Команда': 'Team_name',
                    'Шаблон': 'Template',
                    'Отчет': 'Has_report',
                    'AM_1C name': 'AM_1C_Name',
                    'Ссылка на отчет': 'Report_link'
                }
            elif sheet_name == 'STL_emails':
                column_map = {
                    'STL': 'STL_name',
                    'email': 'Email',
                    'Шаблон': 'Template',
                    'Отчет': 'Has_report',
                    'Ссылка на отчет': 'Report_link'
                }
            elif sheet_name == 'TL_emails':
                column_map = {
                    'Team Lead': 'TeamLead_name',
                    'email': 'Email',
                    'Команда': 'Team_name',
                    'Шаблон': 'Template',
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

    def _save_teams(self, am_data, stl_data, tl_data):
        """Сохранение команд из всех источников"""
        team_names = set()
        
        # Собираем имена команд из всех данных
        for row in am_data:
            if row.get('Team_name'):
                team_names.add(row['Team_name'])
        
        for row in tl_data:
            if row.get('Team_name'):
                team_names.add(row['Team_name'])
        
        if not team_names:
            return
            
        existing_teams = {t.Team: t for t in db.query(Team).all()}
        to_insert = []
        
        for team_name in team_names:
            if team_name not in existing_teams and team_name not in ('-', 'no', None):
                to_insert.append({'Team': team_name})
        
        if to_insert:
            try:
                db.bulk_insert_mappings(Team, to_insert)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                raise Exception(f"Ошибка сохранения команд: {str(e)}")

    def _get_team_id(self, team_name):
        """Получение ID команды по имени"""
        if not team_name or team_name in ('-', 'no'):
            return None
            
        team = db.query(Team).filter(Team.Team == team_name).first()
        return team.id if team else None

    def _save_team_leads(self, data):
        """Сохранение TeamLead"""
        if not data:
            return
            
        existing_tls = {tl.TeamLead_name: tl for tl in db.query(TeamLead).all()}
        to_insert = []
        to_update = []
        
        for row in data:
            tl_name = row.get('TeamLead_name')
            if not tl_name or tl_name in ('-', 'no'):
                continue
                
            team_id = self._get_team_id(row.get('Team_name'))
            
            tl_data = {
                'TeamLead_name': tl_name,
                'Email': row.get('Email'),
                'Team_id': team_id,
                'Template': row.get('Template'),
                'Has_report': row.get('Has_report'),
                'Report_link': row.get('Report_link')
            }
            
            if tl_name in existing_tls:
                tl_data['id'] = existing_tls[tl_name].id
                to_update.append(tl_data)
            else:
                to_insert.append(tl_data)
        
        try:
            if to_insert:
                db.bulk_insert_mappings(TeamLead, to_insert)
            if to_update:
                db.bulk_update_mappings(TeamLead, to_update)
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка сохранения TeamLead: {str(e)}")

    def _save_stls(self, data):
        """Сохранение STL"""
        if not data:
            return
            
        existing_stls = {stl.STL_name: stl for stl in db.query(STL).all()}
        to_insert = []
        to_update = []
        
        for row in data:
            stl_name = row.get('STL_name')
            if not stl_name or stl_name in ('-', 'no'):
                continue
            
            # Для STL берем команду из связанных менеджеров
            team_name = None
            # Можно добавить логику для определения команды STL
            
            team_id = self._get_team_id(team_name)
            
            stl_data = {
                'STL_name': stl_name,
                'Email': row.get('Email'),
                'Team_id': team_id,
                'Template': row.get('Template'),
                'Has_report': row.get('Has_report'),
                'Report_link': row.get('Report_link')
            }
            
            if stl_name in existing_stls:
                stl_data['id'] = existing_stls[stl_name].id
                to_update.append(stl_data)
            else:
                to_insert.append(stl_data)
        
        try:
            if to_insert:
                db.bulk_insert_mappings(STL, to_insert)
            if to_update:
                db.bulk_update_mappings(STL, to_update)
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка сохранения STL: {str(e)}")

    def _save_managers(self, data):
        """Сохранение менеджеров"""
        if not data:
            return

        existing_managers = {m.Manager_name: m for m in db.query(Manager).all()}
        to_insert = []
        to_update = []
        
        # Получаем маппинг имен на ID
        tl_name_to_id = {tl.TeamLead_name: tl.id for tl in db.query(TeamLead).all()}
        stl_name_to_id = {stl.STL_name: stl.id for stl in db.query(STL).all()}

        for row in data:
            manager_name = row.get('Manager_name')
            if not manager_name or manager_name in ('-', 'no'):
                continue

            # Получаем ID связанных сущностей
            stl_id = stl_name_to_id.get(row.get('STL_name'))
            teamlead_id = tl_name_to_id.get(row.get('TeamLead_name'))
            team_id = self._get_team_id(row.get('Team_name'))

            manager_data = {
                'Manager_name': manager_name,
                'Email': row.get('Email'),
                'STL_id': stl_id,
                'TeamLead_id': teamlead_id,
                'Team_id': team_id,
                'Template': row.get('Template'),
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
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка сохранения менеджеров: {str(e)}")

    def apply_pending_changes(self):
        """Применение всех ожидающих изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для применения")
            return
            
        try:
            data_type = getattr(self, '_current_data_type', 'KAM')
            applied_changes = 0
            
            for row_id, changes in self._pending_changes.items():
                for header, new_value in changes.items():
                    if data_type == 'KAM':
                        success = self._update_manager(row_id, header, new_value)
                    elif data_type == 'STL':
                        success = self._update_stl(row_id, header, new_value)
                    elif data_type == 'TL':
                        success = self._update_teamlead(row_id, header, new_value)
                    
                    if success:
                        applied_changes += 1
            
            db.commit()
            
            # Очищаем pending changes
            self._pending_changes.clear()
            
            # Сбрасываем подсветку
            self._reset_table_colors()
            
            # Обновляем таблицу
            self._find_data(data_type)
            
            self.show_message(f"Успешно применено {applied_changes} изменений")
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка применения изменений: {str(e)}")

    def _update_manager(self, manager_name, field, value):
        """Обновление данных менеджера"""
        try:
            manager = db.query(Manager).filter(Manager.Manager_name == manager_name).first()
            if not manager:
                return False
            
            field_mapping = {
                'Manager_name': 'Manager_name',
                'Email': 'Email',
                'STL_name': 'STL_id',
                'TeamLead_name': 'TeamLead_id',
                'Team_name': 'Team_id',
                'Template': 'Template',
                'Has_report': 'Has_report',
                'AM_1C_Name': 'AM_1C_Name',
                'Report_link': 'Report_link'
            }
            
            db_field = field_mapping.get(field)
            if not db_field:
                return False
            
            # Для связанных полей нужно получить ID
            if field == 'STL_name':
                stl = db.query(STL).filter(STL.STL_name == value).first()
                value = stl.id if stl else None
            elif field == 'TeamLead_name':
                tl = db.query(TeamLead).filter(TeamLead.TeamLead_name == value).first()
                value = tl.id if tl else None
            elif field == 'Team_name':
                team = db.query(Team).filter(Team.Team == value).first()
                value = team.id if team else None
            
            setattr(manager, db_field, value)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка обновления менеджера: {str(e)}")

    def _update_stl(self, stl_name, field, value):
        """Обновление данных STL"""
        try:
            stl = db.query(STL).filter(STL.STL_name == stl_name).first()
            if not stl:
                return False
            
            field_mapping = {
                'STL_name': 'STL_name',
                'Email': 'Email',
                'Team_name': 'Team_id',
                'Template': 'Template',
                'Has_report': 'Has_report',
                'Report_link': 'Report_link'
            }
            
            db_field = field_mapping.get(field)
            if not db_field:
                return False
            
            if field == 'Team_name':
                team = db.query(Team).filter(Team.Team == value).first()
                value = team.id if team else None
            
            setattr(stl, db_field, value)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка обновления STL: {str(e)}")

    def _update_teamlead(self, tl_name, field, value):
        """Обновление данных TeamLead"""
        try:
            tl = db.query(TeamLead).filter(TeamLead.TeamLead_name == tl_name).first()
            if not tl:
                return False
            
            field_mapping = {
                'TeamLead_name': 'TeamLead_name',
                'Email': 'Email',
                'Team_name': 'Team_id',
                'Template': 'Template',
                'Has_report': 'Has_report',
                'Report_link': 'Report_link'
            }
            
            db_field = field_mapping.get(field)
            if not db_field:
                return False
            
            if field == 'Team_name':
                team = db.query(Team).filter(Team.Team == value).first()
                value = team.id if team else None
            
            setattr(tl, db_field, value)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка обновления TeamLead: {str(e)}")

    def _reset_table_colors(self):
        """Сброс цвета ячеек таблицы"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(Qt.white)

    def revert_changes(self):
        """Отмена изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для отмены")
            return
            
        try:
            # Сбрасываем изменения в таблице
            self._reset_table_colors()
            self._pending_changes.clear()
            
            # Перезагружаем данные
            if hasattr(self, '_current_data_type'):
                self._find_data(self._current_data_type)
            
            self.show_message("Изменения отменены")
            
        except Exception as e:
            self.show_error_message(f"Ошибка отмены изменений: {str(e)}")

    def _get_current_data_type(self):
        """Определение текущего типа отображаемых данных"""
        return getattr(self, '_current_data_type', 'KAM')

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
            Manager.Template,
            Manager.Has_report,
            Manager.Report_link,
            Manager.AM_1C_Name,
            STL.id.label('STL_id'),
            STL.STL_name,
            STL.Email.label('email_STL'),
            TeamLead.id.label('TeamLead_id'),
            TeamLead.TeamLead_name,
            TeamLead.Email.label('email_TL'),
            Team.Team.label('Team_name')
        ).outerjoin(STL, Manager.STL_id == STL.id)\
         .outerjoin(TeamLead, Manager.TeamLead_id == TeamLead.id)\
         .outerjoin(Team, Manager.Team_id == Team.id)

        df = pd.read_sql(query.statement, db.bind)
        return df.where(pd.notnull(df), None)

    def _find_data(self, data_type):
        """Поиск данных по типу (KAM, STL, TL)"""
        self.table.clearContents()
        self.table.setRowCount(0)
        self._current_data_type = data_type

        try:
            df = self.get_all_managers_data()
            if df.empty:
                raise ValueError('Нет данных в базе')

            df = self._filter_data(df, data_type)
            self._display_data(df, data_type)

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
            return df[['Manager_name', 'Email', 'Team_name', 'Has_report', 'STL_name', 'TeamLead_name', 'AM_1C_Name', 'Report_link', 'Template']]
        
        elif data_type == 'STL':
            if stl != '-':
                df = df[df['STL_name'] == stl]
            elif tl != '-':
                df = df[df['TeamLead_name'] == tl]
            
            # Получаем уникальные STL с данными
            stl_query = db.query(
                STL.STL_name,
                STL.Email,
                STL.Template,
                STL.Has_report,
                STL.Report_link,
                Team.Team.label('Team_name')
            ).outerjoin(Team, STL.Team_id == Team.id)
            
            stl_df = pd.read_sql(stl_query.statement, db.bind)
            
            # Применяем фильтры
            if stl != '-':
                stl_df = stl_df[stl_df['STL_name'] == stl]
            elif tl != '-':
                # Для фильтрации по TL нужно получить связанных STL
                pass
            
            return stl_df.where(pd.notnull(stl_df), None)
        
        else:  # TL
            if tl != '-':
                df = df[df['TeamLead_name'] == tl]
            
            # Получаем уникальные TL с данными
            tl_query = db.query(
                TeamLead.TeamLead_name,
                TeamLead.Email,
                TeamLead.Template,
                TeamLead.Has_report,
                TeamLead.Report_link,
                Team.Team.label('Team_name')
            ).outerjoin(Team, TeamLead.Team_id == Team.id)
            
            tl_df = pd.read_sql(tl_query.statement, db.bind)
            
            # Применяем фильтры
            if tl != '-':
                tl_df = tl_df[tl_df['TeamLead_name'] == tl]
            
            return tl_df.where(pd.notnull(tl_df), None)

    def _display_data(self, df, data_type):
        """Отображение данных в таблице"""
        self._updating_table = True
        
        self.table.clear()
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(0)

        if df.empty:
            self.show_message('Ничего не найдено')
            self._updating_table = False
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
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Сохраняем оригинальное значение
                row_id = str(df.iloc[i][headers[0]])  # Первая колонка - идентификатор
                if row_id not in self._original_values:
                    self._original_values[row_id] = {}
                self._original_values[row_id][col] = value_str

                self.table.setItem(i, j, item)
        
        self.table.resizeColumnsToContents()
        self._updating_table = False

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

        valid_items = sorted([item[0] for item in items if item[0] and item[0] not in ('-', 'no')])
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
        """Показать успешное сообщение в label_msg"""
        self.ui.label_msg.setText(text)
        self.ui.label_msg.setStyleSheet("""
            QLabel {
                background-color: #CCFF99;
                color: #12501A;
                border: 2px solid #12501A;
                border-radius: 5px;
                padding: 8px;
                font: 10pt "Tahoma";
                margin: 2px;
            }
        """)
        self.ui.label_msg.setVisible(True)

    def clear_message(self):
        """Очистить сообщение"""
        self.ui.label_msg.setText("")
        self.ui.label_msg.setStyleSheet("")

    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        
        msg.setMinimumSize(400, 200)
        
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        def copy_text():
            QApplication.clipboard().setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()