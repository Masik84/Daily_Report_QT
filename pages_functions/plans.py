import os
import pandas as pd
import numpy as np

from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QApplication,
                              QTableWidgetItem, QWidget)
from PySide6.QtCore import Qt
from functools import lru_cache
import locale
import time, datetime

from db import db, engine
from models import Calendar, CompanyPlan, CustomerPlan, TeamLead, Holding, Sector, Manager, STL, ABC_list
from config import All_data_file
from wind.pages.plans_ui import Ui_Form


class Plans(QWidget):
    def __init__(self):
        super(Plans, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self._setup_ui()
        self._setup_connections()
        
        self.refresh_all_comboboxes()
    
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
        self.ui.line_kam.currentTextChanged.connect(self.fill_in_hold_list)
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_plans)
    
    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с планами')
        if file_path:
            self.ui.label_plan_File.setText(file_path)
    
    def upload_data(self):
        """Загрузка данных в БД"""
        file_path = self.ui.label_plan_File.text()
        
        if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
            file_path = All_data_file
        
        try:
            self.run_plans_update(file_path)
            self.show_message('Данные планов успешно обновлены!')
            self.refresh_all_comboboxes()
        except Exception as e:
            self.show_error_message(f'Ошибка загрузки данных: {str(e)}')
    
    def run_plans_update(self, file_path):
        """Основная функция обновления планов"""
        # Обновление календаря
        calendar_df = self.read_calendar_file(file_path)
        self.update_calendar(calendar_df)
        
        # Обновление планов по компании
        company_plans_df = self.read_company_plans(file_path)
        self.update_company_plans(company_plans_df)
        
        # Обновление планов по клиентам
        customer_plans_df = self.read_customer_plans(file_path)
        self.update_customer_plans(customer_plans_df)
    
    def get_calendar_from_db(self):
        """Получение календаря из БД через ORM"""
        if not hasattr(self, '_cached_calendar'):
            calendar_data = db.query(Calendar).all()
            self._cached_calendar = pd.DataFrame([{
                'Day': c.Day,
                'Year': c.Year,
                'Quarter': c.Quarter,
                'Month': c.Month,
                'Week_of_Year': c.Week_of_Year,
                'Week_of_Month': c.Week_of_Month,
                'NETWORKDAYS': c.NETWORKDAYS
            } for c in calendar_data])
        return self._cached_calendar.copy()

    def read_calendar_file(self, file_path):
        """Чтение и валидация данных календаря из Excel"""
        dtype_cal = {
            "Year": int, "Quarter": int, "Month": int, 
            "Week of Year": int, "Week of Month": int, "NETWORKDAYS": int
        }
        
        try:
            # Чтение данных с явным указанием формата даты
            calendar = pd.read_excel(
                file_path, 
                sheet_name="Календарь", 
                dtype=dtype_cal)
            
            # Удаление строк с некорректными датами
            calendar = calendar[calendar["День"].notna()]
            calendar["День"] = pd.to_datetime(calendar["День"], format="%d.%m.%Y", errors="coerce")

            calendar["День"] = calendar["День"].dt.normalize()
            calendar = calendar.drop_duplicates(subset=["День"])
            
            # Проверка обязательных полей
            required_columns = ["День", "Year", "Quarter", "Month", "Week of Year", "Week of Month", "NETWORKDAYS"]
            if not all(col in calendar.columns for col in required_columns):
                missing = set(required_columns) - set(calendar.columns)
                raise ValueError(f"Отсутствуют обязательные колонки: {missing}")
                
            # Переименование колонок
            calendar = calendar.rename(columns={
                "День": "Day",
                "Week of Year": "Week_of_Year",
                "Week of Month": "Week_of_Month"
            })
            
            return calendar.to_dict('records')
            
        except Exception as e:
            raise Exception(f"Ошибка чтения файла календаря: {str(e)}")
    
    def read_company_plans(self, file_path):
        """Чтение планов по компании из Excel с заменой пустых числовых значений на 0"""
        dtype_comp = {
            'Year': int, 'Quarter': int, 'Month': int, 
            'Week of Year': int, 'Week of Month': int, 'Work Days': int,
            'Month vol': float, 'Month Revenue': float, 'Month Margin': float
        }
        
        try:
            df = pd.read_excel(file_path, sheet_name='Планы ОБЩИЕ', dtype=dtype_comp)
            df = df[[
                'Year', 'Quarter', 'Month', 'Week of Year', 'Week of Month', 'Work Days',
                'Team Lead', 'ABC', 'Month vol', 'Month Revenue', 'Month Margin',
                'Volume Target total', 'Revenue Target total', 'Margin Target total'
            ]]
            
            # Переименование колонок
            df = df.rename(columns={
                'Week of Year': 'Week_of_Year',
                'Week of Month': 'Week_of_Month',
                'Team Lead': 'TeamLead',
                'Work Days': 'Work_Days',
                'Month vol': 'Month_vol',
                'Month Margin': 'Month_Margin',
                'Volume Target total': 'Volume_Target_total',
                'Revenue Target total': 'Revenue_Target_total',
                'Margin Target total': 'Margin_Target_total'
            })
            
            # Список числовых колонок для обработки
            numeric_cols = [
                'Year', 'Quarter', 'Month', 'Week_of_Year', 'Week_of_Month', 'Work_Days',
                'Month_vol', 'Month_Revenue', 'Month_Margin',
                'Volume_Target_total', 'Revenue_Target_total', 'Margin_Target_total'
            ]
            
            # Замена пустых значений в числовых колонках на 0
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            df['Status'] = 'План'
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Ошибка чтения планов по компании: {str(e)}")

    def read_customer_plans(self, file_path):
        """Чтение планов по клиентам из Excel с заменой пустых числовых значений на 0"""
        try:
            # Чтение данных за 2024 год
            df_2024 = pd.read_excel(file_path, sheet_name='Планы 2024')
            
            # Проверка обязательных колонок для 2024
            required_2024 = ['Year', 'Quarter', 'Month', 'ХОЛДИНГ', 'Менеджер', 'SECTOR', 'STL', 'Team Lead', 
                             'Volume Target cust', 'Margin C3 Target cust']
            
            # Проверяем наличие всех обязательных колонок
            missing_cols = [col for col in required_2024 if col not in df_2024.columns]
            if missing_cols:
                raise Exception(f"В листе 'Планы 2024' отсутствуют колонки: {missing_cols}")
            
            # Выбираем и переименовываем нужные колонки для 2024
            df_2024 = df_2024[required_2024].rename(columns={
                    'Team Lead': 'TeamLead', 
                    'ХОЛДИНГ': 'Holding', 
                    'Менеджер': 'Manager', 
                    'SECTOR': 'Sector',
                    'Volume Target cust': 'Volume_Target_cust',
                    'Margin C3 Target cust': 'Margin_C3_Target_cust'
                })
            
            # Добавляем отсутствующие колонки для 2024
            df_2024['Week_of_Year'] = 0
            df_2024['Week_of_Month'] = 0
            df_2024['Revenue_Target_cust'] = 0
            df_2024['Margin_C4_Target_cust'] = 0

            # Чтение данных за 2025 год
            df_2025 = pd.read_excel(file_path, sheet_name='Планы 2025 (год)')
            
            # Проверка обязательных колонок для 2025
            required_2025 = ['Year', 'ХОЛДИНГ', 'Менеджер', 'SECTOR', 'STL', 
                            'Team Lead', 'Year Volume', 'Year Revenue', 
                            'Year Margin C3', 'Year Margin C4']
            
            missing_cols = [col for col in required_2025 if col not in df_2025.columns]
            if missing_cols:
                raise Exception(f"В листе 'Планы 2025 (год)' отсутствуют колонки: {missing_cols}")
            
            df_2025 = df_2025.rename(columns={
                'Team Lead': 'TeamLead', 
                'ХОЛДИНГ': 'Holding', 
                'Менеджер': 'Manager', 
                'SECTOR': 'Sector',
            })

            df_2025 = self.calculate_weekly_plan(df_2025)

            df_2025 = df_2025.rename(columns={
                                            'Year Volume': 'Volume_Target_cust',
                                            'Year Revenue': 'Revenue_Target_cust',
                                            'Margin C3 Target cust': 'Margin_C3_Target_cust',
                                            'Margin C4 Target cust': 'Margin_C4_Target_cust'})

            # Объединение данных
            common_columns = [
                'Year', 'Quarter', 'Month', 'Week_of_Year', 'Week_of_Month',
                'Holding', 'Manager', 'Sector', 'STL', 'TeamLead',
                'Volume_Target_cust', 'Revenue_Target_cust',
                'Margin_C3_Target_cust', 'Margin_C4_Target_cust'
            ]
            
            # Убедимся, что все колонки существуют перед объединением
            df_2024 = df_2024[[col for col in common_columns if col in df_2024.columns]]
            # df_2025 = df_2025[[col for col in common_columns if col in df_2025.columns]]
            
            # df = pd.concat([df_2024, df_2025], ignore_index=True)
            df = df_2024.copy()
            numeric_cols = [
                'Year', 'Quarter', 'Month', 'Week_of_Year', 'Week_of_Month',
                'Volume_Target_cust', 'Revenue_Target_cust',
                'Margin_C3_Target_cust', 'Margin_C4_Target_cust'
            ]
            
            # Замена пустых значений в числовых колонках на 0
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
            
            df['Status'] = 'План'
            
            return df.to_dict('records')
            
        except Exception as e:
            raise Exception(f"Ошибка чтения планов по клиентам: {str(e)}")
    
    def calculate_weekly_plan(self, plans_df):
        """Преобразование годовых планов в недельные с использованием данных из БД"""
        
        try:
            # 1. Получаем данные календаря из БД
            calendar_df = self.get_calendar_from_db()
            plan_years = plans_df["Year"].unique().tolist()
            calendar_df = calendar_df[calendar_df["Year"].isin(plan_years)]
            calendar_grouped = calendar_df.groupby(["Year", "Quarter", "Month", "Week_of_Year", "Week_of_Month"])["NETWORKDAYS"].agg("sum").reset_index()
            
            plan_phasing_df = pd.read_excel(All_data_file, sheet_name="Plan phasing")
            
            monthly_plans = plans_df.copy()
            monthly_plans = pd.merge(monthly_plans, plan_phasing_df, on=["Year"], how="left")
            if monthly_plans.empty:
                print("Warning: Monthly plans DataFrame is empty after the merge. Check your merge keys.")
                return pd.DataFrame()

            # 4. Расчет месячных показателей
            def calculate_month_values(row, col_name):
                return plans_df.loc[(plans_df['Holding'] == row['Holding']) & (plans_df['Manager'] == row['Manager']), f'Year {col_name}'].sum()

            monthly_plans['Month Volume'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Volume') * row['%'], axis=1)
            monthly_plans['Month Revenue'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Revenue') * row['%'], axis=1)
            monthly_plans['Month Margin C3'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Margin C3') * row['%'], axis=1)
            monthly_plans['Month Margin C4'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Margin C4') * row['%'], axis=1)

            # 5. Объединяем с календарем для получения недельных данных
            weekly_plans = pd.merge( calendar_df, monthly_plans, on=["Year", "Month"],  how="left", )
            if weekly_plans.empty:
                print("Warning: Weekly plans DataFrame is empty after the merge. Check your merge keys.")
                return pd.DataFrame()

            # 6. Расчет еженедельных показателей
            def calculate_weekly_target(row, col_name):
                numerator = monthly_plans.loc[
                    (monthly_plans['Year'] == row['Year']) &
                    (monthly_plans['Month'] == row['Month']) &
                    (monthly_plans['Holding'] == row['Holding']) &
                    (monthly_plans['Manager'] == row['Manager']),
                    f'Month {col_name}'
                ].sum()

                denominator = calendar_grouped.loc[
                    (calendar_grouped['Year'] == row['Year']) &
                    (calendar_grouped['Month'] == row['Month']),
                    'NETWORKDAYS'
                ].sum()

                try:
                    return (numerator / denominator) * row['NETWORKDAYS']
                except ZeroDivisionError:
                    return 0

            weekly_plans['Volume Target cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Volume'), axis=1)
            weekly_plans['Revenue Target cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Revenue'), axis=1)
            weekly_plans['Margin C3 Target cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Margin C3'), axis=1)
            weekly_plans['Margin C4 Target cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Margin C4'), axis=1)

            # Заполняем нулями пропущенные значения
            weekly_plans = weekly_plans.fillna(0)
            return weekly_plans
            
        except Exception as e:
            print(f"Ошибка в calculate_weekly_plan: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def update_calendar(self, data):
        """Обновление календаря с проверкой существующих записей"""
        if not data:
            return

        try:
            # Получаем список всех дат из входных данных (уже как date объекты)
            input_dates = {pd.Timestamp(row['Day']).to_pydatetime().date() for row in data}
            
            # Запрос к базе для получения существующих дат
            existing_records = db.query(Calendar.Day).filter(Calendar.Day.in_(input_dates)).all()
            existing_dates = {record.Day for record in existing_records}
            
            # Фильтруем только новые записи
            new_records = [
                row for row in data 
                if pd.Timestamp(row['Day']).to_pydatetime().date() not in existing_dates
            ]
            
            if not new_records:
                return
                
            # Вставка с обработкой конфликтов
            stmt = insert(Calendar).values(new_records)
            stmt = stmt.on_conflict_do_nothing(index_elements=['Day'])
            db.execute(stmt)
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения календаря: {str(e)}")
        except Exception as e:
            db.rollback()
            raise Exception(f"Неожиданная ошибка: {str(e)}")
        finally:
            db.close()
                
    def update_company_plans(self, data):
        """Обновление планов компании с правильными связями"""
        if not data:
            return

        try:
            # Получаем существующие записи с join на ABC_list
            existing_plans = {
                (c.calendar.Year, c.calendar.Month, c.calendar.Week_of_Year,
                c.TeamLead_id, c.abc_list.ABC_category): c.id
                for c in db.query(CompanyPlan)
                    .join(CompanyPlan.calendar)
                    .join(CompanyPlan.abc_list)
                    .all()
            }
            
            to_insert = []
            to_update = []
            
            for row in data:
                # Ищем соответствующий календарь
                calendar = db.query(Calendar).filter(
                    Calendar.Year == row['Year'],
                    Calendar.Month == row['Month'],
                    Calendar.Week_of_Year == row['Week_of_Year']
                ).first()
                
                if not calendar:
                    print(f"Пропущена запись: не найден календарь для {row}")
                    continue
                    
                key = (
                    row['Year'],
                    row['Month'],
                    row['Week_of_Year'],
                    self._get_id(TeamLead, 'TeamLead_name', row['TeamLead']),
                    row.get('ABC')
                )
                
                plan_data = {
                    'Work_Days': row['Work_Days'],
                    'Month_vol': row.get('Month_vol', 0),
                    'Month_Revenue': row.get('Month_Revenue', 0),
                    'Month_Margin': row.get('Month_Margin', 0),
                    'Volume_Target_total': row['Volume_Target_total'],
                    'Revenue_Target_total': row['Revenue_Target_total'],
                    'Margin_Target_total': row['Margin_Target_total'],
                    'Status': row.get('Status', 'План'),
                    'TeamLead_id': self._get_id(TeamLead, 'TeamLead_name', row['TeamLead']),
                    'abc_category_id': self._get_id(ABC_list, 'ABC_category', row.get('ABC')),
                    'calendar_id': calendar.id
                }
                
                if key in existing_plans:
                    plan_data['id'] = existing_plans[key]
                    to_update.append(plan_data)
                else:
                    to_insert.append(plan_data)
            
            if to_insert:
                db.bulk_insert_mappings(CompanyPlan, to_insert)
            if to_update:
                db.bulk_update_mappings(CompanyPlan, to_update)
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения планов компании: {str(e)}")
        finally:
            db.close()
    
    def update_customer_plans(self, data):
        """Обновление планов по клиентам в БД"""
        if not data:
            return
        
        existing_plans = {
            (c.Year, c.Month, c.Week_of_Year, c.Holding_id, c.Manager_id): c.id 
            for c in db.query(CustomerPlan).all()
        }
        to_insert = []
        to_update = []
        
        for row in data:
            key = (
                row['Year'], 
                row['Month'], 
                row.get('Week_of_Year', 0),
                self._get_id(Holding, 'Holding_name', row['Holding']),
                self._get_id(Manager, 'Manager_name', row['Manager'])
            )
            
            plan_data = {
                'Year': row['Year'],
                'Quarter': row['Quarter'],
                'Month': row['Month'],
                'Week_of_Year': row.get('Week_of_Year'),
                'Week_of_Month': row.get('Week_of_Month'),
                'Volume_Target_cust': row['Volume_Target_cust'],
                'Revenue_Target_cust': row.get('Revenue_Target_cust', 0),
                'Margin_C3_Target_cust': row.get('Margin_C3_Target_cust', 0),  # Исправлено здесь
                'Margin_C4_Target_cust': row.get('Margin_C4_Target_cust', 0),  # И здесь
                'Status': row.get('Status', 'План'),
                'Holding_id': self._get_id(Holding, 'Holding_name', row['Holding']),
                'Manager_id': self._get_id(Manager, 'Manager_name', row['Manager']),
                'Sector_id': self._get_id(Sector, 'Sector_name', row.get('Sector')),
                'STL_id': self._get_id(STL, 'STL_name', row.get('STL')),
                'TeamLead_id': self._get_id(TeamLead, 'TeamLead_name', row['TeamLead'])
            }
            
            if key in existing_plans:
                plan_data['id'] = existing_plans[key]
                to_update.append(plan_data)
            else:
                to_insert.append(plan_data)
        
        try:
            if to_insert:
                db.bulk_insert_mappings(CustomerPlan, to_insert)
            if to_update:
                db.bulk_update_mappings(CustomerPlan, to_update)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения планов клиентов: {str(e)}")
        finally:
            db.close()
    
    @lru_cache(maxsize=32)
    def _get_id(self, model, name_field, name):
        """Получение ID по имени (с кэшированием)"""
        if not name or pd.isna(name) or name == '-':
            return None
        
        item = db.query(model).filter(getattr(model, name_field) == name).first()
        return item.id if item else None
    
    def find_plans(self):
        """Поиск планов по заданным критериям"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        plan_type = self.ui.line_plan_type.currentText()
        year = self.ui.line_Year.currentText()
        quarter = self.ui.line_Qtr.currentText()
        month = self.ui.line_Mnth.currentText()
        tl = self.ui.line_tl.currentText()
        kam = self.ui.line_kam.currentText()
        holding = self.ui.line_Holding.currentText()
        
        if plan_type == "План Общий":
            df = self.get_company_plans_from_db(year, quarter, month, tl)
        elif plan_type == "План КАМ-Клиент":
            df = self.get_customer_plans_from_db(year, quarter, month, tl, kam, holding)
        else:
            self.show_error_message("Выберите тип плана")
            return
        
        self._display_data(df)
        self._update_summary(df, plan_type)
    
    def get_company_plans_from_db(self, year, quarter, month, tl):
        """Получение планов компании через ORM"""
        try:
            query = db.query(
                Calendar.Year,
                Calendar.Quarter,
                Calendar.Month,
                Calendar.Week_of_Year,
                Calendar.Week_of_Month,
                TeamLead.TeamLead_name.label('TeamLead'),
                ABC_list.ABC_category.label('ABC'),
                CompanyPlan.Volume_Target_total,
                CompanyPlan.Revenue_Target_total,
                CompanyPlan.Margin_Target_total
            ).join(CompanyPlan.calendar
            ).join(CompanyPlan.team_lead
            ).join(ABC_list, CompanyPlan.abc_category_id == ABC_list.id)
            
            if year != '-':
                query = query.filter(Calendar.Year == int(year))
            if quarter != '-':
                query = query.filter(Calendar.Quarter == int(quarter))
            if month != '-':
                query = query.filter(Calendar.Month == int(month))
            if tl != '-':
                query = query.filter(TeamLead.TeamLead_name == tl)
            
            # Конвертируем результат ORM в DataFrame
            plans = query.all()
            if not plans:
                return pd.DataFrame()
                
            return pd.DataFrame([{
                'Year': p.Year,
                'Quarter': p.Quarter,
                'Month': p.Month,
                'Week_of_Year': p.Week_of_Year,
                'Week_of_Month': p.Week_of_Month,
                'TeamLead': p.TeamLead,
                'ABC': p.ABC,
                'Volume_Target_total': p.Volume_Target_total,
                'Revenue_Target_total': p.Revenue_Target_total,
                'Margin_Target_total': p.Margin_Target_total
            } for p in plans])
            
        except Exception as e:
            print(f"Ошибка при загрузке планов компании: {str(e)}")
            return pd.DataFrame()
        finally:
            db.close()

    def get_customer_plans_from_db(self, year, quarter, month, tl, kam, holding):
        """Получение планов по клиентам из БД с обработкой пустого результата"""
        try:
            query = db.query(
                Calendar.Year,
                Calendar.Quarter,
                Calendar.Month,
                Calendar.Week_of_Year,
                Calendar.Week_of_Month,
                Holding.Holding_name.label('Holding'),
                Manager.Manager_name.label('Manager'),
                STL.STL_name.label('STL'),
                TeamLead.TeamLead_name.label('TeamLead'),
                CustomerPlan.Volume_Target_cust,
                CustomerPlan.Revenue_Target_cust,
                CustomerPlan.Margin_C3_Target_cust,
                CustomerPlan.Margin_C4_Target_cust
            ).join(CustomerPlan, CustomerPlan.calendar_id == Calendar.id
            ).join(Holding, CustomerPlan.Holding_id == Holding.id
            ).join(Manager, CustomerPlan.Manager_id == Manager.id
            ).outerjoin(STL, CustomerPlan.STL_id == STL.id
            ).join(TeamLead, CustomerPlan.TeamLead_id == TeamLead.id)
            
            if year != '-':
                query = query.filter(Calendar.Year == int(year))
            if quarter != '-':
                query = query.filter(Calendar.Quarter == int(quarter))
            if month != '-':
                query = query.filter(Calendar.Month == int(month))
            if tl != '-':
                query = query.filter(TeamLead.TeamLead_name == tl)
            if kam != '-':
                query = query.filter(Manager.Manager_name == kam)
            if holding != '-':
                query = query.filter(Holding.Holding_name == holding)
            
            df = pd.read_sql(query.statement, db.bind)
            return df if not df.empty else pd.DataFrame()  # Возвращаем пустой DataFrame если нет данных
        except Exception as e:
            print(f"Ошибка при загрузке планов клиентов: {str(e)}")
            return pd.DataFrame()
        finally:
            db.close()

    def _display_data(self, df):
        """Отображение данных в таблице с обработкой пустого DataFrame"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if df.empty:
            self.show_message('Данные не найдены')
            return
        
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(row_idx, col_idx, item)

    def _update_summary(self, df, plan_type):
        """Обновление сводной информации с обработкой пустого DataFrame"""
        if df.empty:
            volume = revenue = margin = 0
        else:
            if plan_type == "План Общий":
                volume = df['Volume_Target_total'].sum()
                revenue = df['Revenue_Target_total'].sum()
                margin = df['Margin_Target_total'].sum()
            elif plan_type == "План КАМ-Клиент":
                volume = df['Volume_Target_cust'].sum()
                revenue = df.get('Revenue_Target_cust', pd.Series([0])).sum()
                margin = df['Margin_C3_Target_cust'].sum()
            else:
                volume = revenue = margin = 0
        
        self.ui.label_Volume.setText(f"{volume:,.0f} л." if volume != 0 else "0 л.")
        self.ui.label_Revenue.setText(f"{revenue:,.0f} р" if revenue != 0 else "0 р")
        self.ui.label_Margin.setText(f"{margin:,.0f} р" if margin != 0 else "0 р")
        
        if volume != 0:
            unit_margin = margin / volume
            self.ui.label_uC3.setText(f"{unit_margin:,.0f} р/л")
        else:
            self.ui.label_uC3.setText("0 р/л")
    
    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self.fill_in_year_list()
        self.fill_in_qtr_list()
        self.fill_in_mnth_list()
        self.fill_in_tl_list()
        self.fill_in_kam_list()
        self.fill_in_hold_list()
    
    def fill_in_year_list(self):
        """Заполнение списка годов через ORM"""
        try:
            years = db.query(Calendar.Year).distinct().order_by(Calendar.Year.desc()).all()
            years_list = [str(y[0]) for y in years] if years else []
            self._fill_combobox(self.ui.line_Year, years_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка годов: {str(e)}")
            self._fill_combobox(self.ui.line_Year, [])
    
    def fill_in_qtr_list(self):
        """Заполнение списка кварталов"""
        self._fill_combobox(self.ui.line_Qtr, ['-', '1', '2', '3', '4'])
    
    def fill_in_mnth_list(self):
        """Заполнение списка месяцев"""
        self._fill_combobox(self.ui.line_Mnth, ['-'] + [str(i) for i in range(1, 13)])
    
    def fill_in_tl_list(self):
        """Заполнение списка тимлидов через ORM"""
        try:
            tls = db.query(TeamLead.TeamLead_name).distinct().order_by(TeamLead.TeamLead_name).all()
            tls_list = [tl[0] for tl in tls] if tls else []
            self._fill_combobox(self.ui.line_tl, tls_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка тимлидов: {str(e)}")
            self._fill_combobox(self.ui.line_tl, [])

    def fill_in_kam_list(self):
        """Заполнение списка менеджеров через ORM"""
        try:
            tl = self.ui.line_tl.currentText()
            query = db.query(Manager.Manager_name).distinct().order_by(Manager.Manager_name)
            
            if tl != '-':
                query = query.join(TeamLead).filter(TeamLead.TeamLead_name == tl)
            
            kams = query.all()
            kams_list = [kam[0] for kam in kams] if kams else []
            self._fill_combobox(self.ui.line_kam, kams_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка менеджеров: {str(e)}")
            self._fill_combobox(self.ui.line_kam, [])

    def fill_in_hold_list(self):
        """Заполнение списка холдингов"""
        try:
            kam = self.ui.line_kam.currentText()
            query = db.query(Holding.Holding_name).distinct().order_by(Holding.Holding_name)
            
            if kam != '-':
                query = query.join(CustomerPlan).join(Manager).filter(Manager.Manager_name == kam)
            
            holdings = query.all()
            holdings_list = [h[0] for h in holdings] if holdings else []
            self._fill_combobox(self.ui.line_Holding, holdings_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка холдингов: {str(e)}")
            self._fill_combobox(self.ui.line_Holding, [])

    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса с обработкой пустого списка"""
        combobox.clear()
        combobox.addItem('-')  # Всегда добавляем "-" как первый элемент
        
        if items:  # Добавляем остальные элементы только если они есть
            combobox.addItems(items)
    
    def show_message(self, text):
        """Показать информационное сообщение (не закрывается при копировании)"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f8f8f2;
                font: 10pt "Tahoma";
            }
            QMessageBox QLabel {
                color: #237508;
            }
        """)
        msg.setIcon(QMessageBox.Information)

        # Создаем кнопку копирования
        copy_button = msg.addButton("Копировать", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)

        # Настройка буфера обмена
        clipboard = QApplication.clipboard()
        
        # Подключаем кнопку копирования
        def copy_text():
            clipboard.setText(text)
            copy_button.setText("Скопировано!")
            copy_button.setEnabled(False)
        
        copy_button.clicked.connect(copy_text)
        
        # Запускаем диалог
        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке (не закрывается при копировании)"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f8f8f2;
                font: 10pt "Tahoma";
            }
            QMessageBox QLabel {
                color: #ff0000;
            }
        """)
        msg.setIcon(QMessageBox.Critical)

        # Создаем кнопку копирования
        copy_button = msg.addButton("Копировать", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)

        # Настройка буфера обмена
        clipboard = QApplication.clipboard()
        
        # Подключаем кнопку копирования
        def copy_text():
            clipboard.setText(text)
            copy_button.setText("Скопировано!")
            copy_button.setEnabled(False)
        
        copy_button.clicked.connect(copy_text)
        
        # Запускаем диалог
        msg.exec_()