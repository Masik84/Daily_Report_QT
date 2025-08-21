import pandas as pd
import traceback


from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QApplication,
                              QTableWidgetItem, QWidget, )
from PySide6.QtCore import Qt
from functools import lru_cache


from db import db, engine
from models import (Calendar, CompanyPlan, CustomerPlan, TeamLead, Holding, Sector, Manager, STL, ABC_list, 
                                    Year, Quarter, Month, Week, Customer, Contract)
from config import All_data_file
from wind.pages.plans_ui import Ui_Form


class PlansPage(QWidget):
    def __init__(self):
        super().__init__()
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
        
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                selection-background-color: #3daee9;
                selection-color: black;
            }
        """)
    
    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.ui.line_tl.currentTextChanged.connect(self.fill_in_kam_list)
        self.ui.line_kam.currentTextChanged.connect(self.fill_in_hold_list)
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_plans)
    
    def showEvent(self, event):
        """Переопределяем метод открытия окна для сброса значений"""
        super().showEvent(event)
        self.reset_all_comboboxes()

    def reset_all_comboboxes(self):
        """Сбрасывает все выпадающие списки к значениям по умолчанию"""
        self.ui.line_plan_type.setCurrentIndex(0)  # Устанавливаем первый элемент
        self.ui.line_Year.setCurrentIndex(0)
        self.ui.line_Qtr.setCurrentIndex(0)
        self.ui.line_Mnth.setCurrentIndex(0)
        self.ui.line_tl.setCurrentIndex(0)
        self.ui.line_kam.setCurrentIndex(0)
        self.ui.line_Holding.setCurrentIndex(0)
        self.fill_in_kam_list()  # Обновляем зависимые списки
        self.fill_in_hold_list()
    
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
            plan_type = self.ui.line_plan_type.currentText()
            if not plan_type or plan_type == '-':
                self.show_error_message("Пожалуйста, выберите тип плана для обновления")
                return
            
            loaded_rows, message = self.run_plans_update(file_path)
            
            if loaded_rows > 0:
                self.show_message(f"{message}\nЗагружено строк: {loaded_rows}")
                self.refresh_all_comboboxes()
            else:
                self.show_error_message("Данные не были загружены. Проверьте файл и тип плана.")
                
        except pd.errors.EmptyDataError:
            self.show_error_message("Ошибка: Файл пуст или имеет неправильный формат")
        except KeyError as e:
            self.show_error_message(f"Ошибка: Отсутствует обязательная колонка в файле - {str(e)}")
        except ValueError as e:
            self.show_error_message(f"Ошибка в данных: {str(e)}")
        except Exception as e:
            error_msg = f'Критическая ошибка загрузки: {str(e)}'
            traceback.print_exc()  # Печать трассировки в консоль
            self.show_error_message(error_msg)

    def run_plans_update(self, file_path):
        """Основная функция обновления планов"""
        try:
            # 1. Обновляем календарь
            calendar_df = self.read_calendar_file(file_path)
            self.update_calendar_tables(calendar_df)
            
            # 2. Проверяем тип плана
            plan_type = self.ui.line_plan_type.currentText()
            if not plan_type or plan_type == '-':
                return 0, "Тип плана не выбран"
            
            # 3. Загружаем соответствующие данные
            if plan_type == "План Общий":
                try:
                    df = self.read_company_plans(file_path)  # Теперь метод существует
                    if df.empty:
                        return 0, "Файл общего плана не содержит данных"
                    
                    loaded_rows = self.update_company_plans(df)
                    return loaded_rows, "Данные общего плана успешно обновлены"
                    
                except Exception as e:
                    raise Exception(f"Ошибка загрузки общего плана: {str(e)}")
                    
            elif plan_type == "План КАМ-Клиент":
                try:
                    df = self.read_customer_plans(file_path)
                    if df.empty:
                        return 0, "Файл плана клиентов не содержит данных"
                    
                    loaded_rows = self.update_customer_plans(df)
                    return loaded_rows, "Данные плана клиентов успешно обновлены"
                    
                except Exception as e:
                    raise Exception(f"Ошибка загрузки плана клиентов: {str(e)}")
                    
            return 0, "Неизвестный тип плана"
            
        except Exception as e:
            raise Exception(f"Ошибка при обновлении планов: {str(e)}")
    
    def get_calendar_from_db(self):
        """Получение календаря из БД через ORM"""
        if not hasattr(self, '_cached_calendar'):
            calendar_data = db.query(Calendar).all()
            self._cached_calendar = pd.DataFrame([{
                'Day': c.Day,
                'Year': c.year.Year if c.year else None,  # Исправлено: обращение через связь year
                'Quarter': c.quarter.Quarter if c.quarter else None,  # Исправлено: обращение через связь quarter
                'Month': c.month.Month if c.month else None,  # Исправлено: обращение через связь month
                'Week_of_Year': c.week.Week_of_Year if c.week else None,  # Исправлено: обращение через связь week
                'Week_of_Month': c.week.Week_of_Month if c.week else None,  # Исправлено: обращение через связь week
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
        """Чтение данных общего плана из Excel с загрузкой всех строк"""
        try:
            dtype = {
                'Year': int, 'Quarter': int, 'Month': int,
                'Week of Year': int, 'Week of Month': int,
                'Work Days': int
            }
            
            df = pd.read_excel(
                file_path,
                sheet_name='Планы ОБЩИЕ',
                dtype=dtype,
                na_values=['', 'NA', 'N/A']  # Но не включаем '-' в na_values
            )
            
            # Обязательные колонки (без Team Lead и ABC, так как они могут быть '-')
            required_cols = [
                'Year', 'Quarter', 'Month', 'Week of Year', 'Week of Month'
            ]
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Отсутствуют обязательные колонки: {missing_cols}")

            # Переименование колонок
            col_mapping = {
                'Week of Year': 'Week_of_Year',
                'Week of Month': 'Week_of_Month',
                'Team Lead': 'TeamLead',
                'Work Days': 'Work_Days',
                'Month vol': 'Month_vol',
                'Month Revenue': 'Month_Revenue',
                'Month Margin': 'Month_Margin',
                'Volume Target total': 'Volume_Target_total',
                'Revenue Target total': 'Revenue_Target_total',
                'Margin Target total': 'Margin_Target_total'
            }
            
            df = df.rename(columns={k: v for k, v in col_mapping.items() if k in df.columns})
            
            # Обработка числовых колонок (заменяем только настоящие NaN, а не '-')
            numeric_cols = [
                'Month_vol', 'Month_Revenue', 'Month_Margin',
                'Volume_Target_total', 'Revenue_Target_total', 'Margin_Target_total'
            ]
            
            for col in numeric_cols:
                if col in df.columns:
                    # Заменяем только настоящие NaN, оставляя '-' как строку
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    df[col] = df[col].fillna(0)  # Заполняем только настоящие NaN
            
            # Обработка TeamLead и ABC
            if 'TeamLead' in df.columns:
                df['TeamLead'] = df['TeamLead'].fillna('-')  # Заменяем NaN на '-'
            else:
                df['TeamLead'] = '-'  # Создаем колонку, если отсутствует
                
            if 'ABC' in df.columns:
                df['ABC'] = df['ABC'].fillna('-')
            else:
                df['ABC'] = '-'
            
            df['Status'] = 'План'
            
            return df

        except Exception as e:
            error_msg = f"Ошибка чтения файла общего плана: {str(e)}\n"
            if 'df' in locals():
                error_msg += f"Первые 5 строк:\n{df.head().to_string()}"
            raise Exception(error_msg)
        
    def read_customer_plans(self, file_path):
        """Чтение планов клиентов с сохранением обработки двух листов"""
        try:
            # 1. Чтение данных за 2024 год
            df_2024 = pd.read_excel(file_path, sheet_name='Планы 2024')
            
            # Проверка обязательных колонок для 2024
            required_2024 = ['Year', 'Quarter', 'Month', 'ХОЛДИНГ', 'Менеджер', 
                            'SECTOR', 'STL', 'Team Lead', 'Volume Target cust', 
                            'Margin C3 Target cust']
            
            missing_cols = [col for col in required_2024 if col not in df_2024.columns]
            if missing_cols:
                raise ValueError(f"В листе 'Планы 2024' отсутствуют колонки: {missing_cols}")

            # Обработка df_2024
            df_2024 = df_2024.rename(columns={
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

            # 2. Чтение данных за 2025 год
            df_2025 = pd.read_excel(file_path, sheet_name='Планы 2025 (год)')

            # Проверка обязательных колонок для 2025
            required_2025 = ['Year', 'ХОЛДИНГ', 'Менеджер', 'SECTOR', 'STL', 
                            'Team Lead', 'Year Volume', 'Year Revenue', 
                            'Year Margin C3', 'Year Margin C4']
            
            missing_cols = [col for col in required_2025 if col not in df_2025.columns]
            if missing_cols:
                raise ValueError(f"В листе 'Планы 2025 (год)' отсутствуют колонки: {missing_cols}")

            # Обработка df_2025 (сохраняем вашу оригинальную логику)
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
                'Year Margin C3': 'Margin_C3_Target_cust',
                'Year Margin C4': 'Margin_C4_Target_cust'
            })

            # 3. Объединение данных
            common_columns = [
                'Year', 'Quarter', 'Month', 'Week_of_Year', 'Week_of_Month',
                'Holding', 'Manager', 'Sector', 'STL', 'TeamLead',
                'Volume_Target_cust', 'Revenue_Target_cust',
                'Margin_C3_Target_cust', 'Margin_C4_Target_cust'
            ]
            
            # Приводим колонки к единому формату
            df_2024 = df_2024[[col for col in common_columns if col in df_2024.columns]]
            df_2025 = df_2025[[col for col in common_columns if col in df_2025.columns]]

            df = pd.concat([df_2024, df_2025], ignore_index=True)

            # 4. Обработка числовых колонок
            numeric_cols = [
                'Volume_Target_cust', 'Revenue_Target_cust',
                'Margin_C3_Target_cust', 'Margin_C4_Target_cust'
            ]
            
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            df['Status'] = 'План'

            return df

        except Exception as e:
            error_msg = f"Ошибка чтения планов клиентов: {str(e)}\n"
            if 'df_2024' in locals():
                error_msg += f"Структура 2024:\n{df_2024.columns.tolist()}\n"
            if 'df_2025' in locals():
                error_msg += f"Структура 2025:\n{df_2025.columns.tolist()}"
            raise Exception(error_msg)
        
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

            # 2. Расчет месячных показателей
            def calculate_month_values(row, col_name):
                return plans_df.loc[(plans_df['Holding'] == row['Holding']) & 
                                (plans_df['Manager'] == row['Manager']), 
                                f'Year {col_name}'].sum()

            monthly_plans['Month Volume'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Volume') * row['%'], axis=1)
            monthly_plans['Month Revenue'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Revenue') * row['%'], axis=1)
            monthly_plans['Month Margin C3'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Margin C3') * row['%'], axis=1)
            monthly_plans['Month Margin C4'] = monthly_plans.apply(lambda row: calculate_month_values(row, 'Margin C4') * row['%'], axis=1)

            # 3. Объединяем с календарем для получения недельных данных
            weekly_plans = pd.merge(calendar_grouped, monthly_plans, on=["Year", "Month"], how="left")
            if weekly_plans.empty:
                print("Warning: Weekly plans DataFrame is empty after the merge. Check your merge keys.")
                return pd.DataFrame()

            # 4. Расчет еженедельных показателей
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

            weekly_plans['Volume_Target_cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Volume'), axis=1)
            weekly_plans['Revenue_Target_cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Revenue'), axis=1)
            weekly_plans['Margin_C3_Target_cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Margin C3'), axis=1)
            weekly_plans['Margin_C4_Target_cust'] = weekly_plans.apply(lambda row: calculate_weekly_target(row, 'Margin C4'), axis=1)

            # Удаляем временные колонки
            weekly_plans = weekly_plans.drop(columns=[
                'Month Volume', 'Month Revenue', 'Month Margin C3', 'Month Margin C4', 
                'Year Volume', 'Year Revenue', 'Year Margin C3', 'Year Margin C4', '%'
            ], errors='ignore')

            # Заполняем нулями пропущенные значения
            weekly_plans = weekly_plans.fillna(0)
            
            # Удаляем дубликаты
            weekly_plans = weekly_plans.drop_duplicates()
            
            return weekly_plans
            
        except Exception as e:
            print(f"Ошибка в calculate_weekly_plan: {str(e)}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def update_calendar_tables(self, data):
        """Обновление таблиц Year, Quarter, Month, Week и Calendar с обработкой процентов"""
        if not data:
            return

        try:
            for row in data:
                # Обработка процентных значений
                if 'NETWORKDAYS' in row and isinstance(row['NETWORKDAYS'], str) and '%' in row['NETWORKDAYS']:
                    row['NETWORKDAYS'] = float(row['NETWORKDAYS'].replace('%', '')) / 100
                
                # Year
                year = db.query(Year).filter(Year.Year == row['Year']).first()
                if not year:
                    year = Year(Year=row['Year'])
                    db.add(year)
                    db.commit()
                
                # Quarter
                quarter = db.query(Quarter).filter(Quarter.Quarter == row['Quarter']).first()
                if not quarter:
                    quarter = Quarter(Quarter=row['Quarter'])
                    db.add(quarter)
                    db.commit()
                
                # Month
                month = db.query(Month).filter(
                    Month.Month == row['Month'],
                    Month.Quarter_id == quarter.id).first()
                if not month:
                    month = Month(Month=row['Month'], Quarter_id=quarter.id)
                    db.add(month)
                    db.commit()
                
                # Week
                week = db.query(Week).filter(
                    Week.Week_of_Year == row['Week_of_Year'],
                    Week.Week_of_Month == row['Week_of_Month']
                ).first()
                if not week:
                    week = Week(
                        Week_of_Year=row['Week_of_Year'],
                        Week_of_Month=row['Week_of_Month']
                    )
                    db.add(week)
                    db.commit()
                
                # Calendar
                calendar = db.query(Calendar).filter(Calendar.Day == row['Day']).first()
                
                if calendar:
                    calendar.Year_id = year.id
                    calendar.Quarter_id = quarter.id
                    calendar.Month_id = month.id
                    calendar.Week_id = week.id
                    calendar.NETWORKDAYS = row['NETWORKDAYS']
                else:
                    calendar = Calendar(
                        Day=row['Day'],
                        Year_id=year.id,
                        Quarter_id=quarter.id,
                        Month_id=month.id,
                        Week_id=week.id,
                        NETWORKDAYS=row['NETWORKDAYS']
                    )
                    db.add(calendar)
                
                db.commit()
                
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Ошибка сохранения календарных данных: {str(e)}")
        finally:
            db.close()

    def update_company_plans(self, df):
        """Обновление планов компании с учетом переименованных колонок"""
        if df.empty:
            print("Предупреждение: Передан пустой DataFrame")
            return 0

        try:
            # 1. Получаем все справочники
            years = {y.Year: y.id for y in db.query(Year).all()}
            months = {m.Month: m.id for m in db.query(Month).all()}
            weeks = {(w.Week_of_Year, w.Week_of_Month): w.id for w in db.query(Week).all()}
            teamleads = {tl.TeamLead_name: tl.id for tl in db.query(TeamLead).all()}
            abc_categories = {abc.ABC_category: abc.id for abc in db.query(ABC_list).all()}

            # 2. Подготовка данных
            records_to_insert = []
            records_to_update = []
            duplicate_errors = []
            processed_rows = 0

            for idx, row in df.iterrows():
                try:
                    # Получаем ID для обязательных полей (используем переименованные колонки)
                    year_id = years.get(int(row['Year']))
                    month_id = months.get(int(row['Month']))
                    week_id = weeks.get((int(row['Week_of_Year']), int(row['Week_of_Month'])))
                    
                    # Обработка TeamLead (уже переименовано в read_company_plans)
                    teamlead_name = str(row['TeamLead'])
                    if teamlead_name == '-' or not teamlead_name:
                        teamlead_id = None
                    else:
                        teamlead = db.query(TeamLead).filter(TeamLead.TeamLead_name == teamlead_name).first()
                        if not teamlead:
                            teamlead = TeamLead(TeamLead_name=teamlead_name)
                            db.add(teamlead)
                            db.commit()
                            teamleads[teamlead_name] = teamlead.id
                        teamlead_id = teamlead.id
                    
                    # Обработка ABC (уже переименовано в read_company_plans)
                    abc_category = str(row['ABC'])
                    if abc_category == '-' or not abc_category:
                        abc_id = None
                    else:
                        abc = db.query(ABC_list).filter(ABC_list.ABC_category == abc_category).first()
                        if not abc:
                            abc = ABC_list(ABC_category=abc_category)
                            db.add(abc)
                            db.commit()
                            abc_categories[abc_category] = abc.id
                        abc_id = abc.id

                    # Формируем запись (используем переименованные колонки)
                    record = {
                        'Year_id': year_id,
                        'Month_id': month_id,
                        'Week_id': week_id,
                        'TeamLead_id': teamlead_id,
                        'ABC_category_id': abc_id,
                        'Work_Days': int(row['Work_Days']),
                        'Month_vol': float(row.get('Month_vol', 0)),
                        'Month_Revenue': float(row.get('Month_Revenue', 0)),
                        'Month_Margin': float(row.get('Month_Margin', 0)),
                        'Volume_Target_total': float(row.get('Volume_Target_total', 0)),
                        'Revenue_Target_total': float(row.get('Revenue_Target_total', 0)),
                        'Margin_Target_total': float(row.get('Margin_Target_total', 0)),
                        'Status': str(row.get('Status', 'План'))
                    }

                    # Проверка существования записи
                    existing = db.query(CompanyPlan).filter(
                        CompanyPlan.Year_id == year_id,
                        CompanyPlan.Month_id == month_id,
                        CompanyPlan.Week_id == week_id,
                        CompanyPlan.TeamLead_id == (teamlead_id if teamlead_id else None),
                        CompanyPlan.ABC_category_id == (abc_id if abc_id else None)
                    ).first()

                    if existing:
                        record['id'] = existing.id
                        records_to_update.append(record)
                    else:
                        records_to_insert.append(record)
                    
                    processed_rows += 1

                except Exception as e:
                    error_msg = f"Ошибка в строке {idx}:\n{row.to_dict()}\n{str(e)}"
                    print(error_msg)
                    duplicate_errors.append(error_msg)
                    continue

            # 3. Выполняем операции
            if records_to_update:
                db.bulk_update_mappings(CompanyPlan, records_to_update)
            if records_to_insert:
                db.bulk_insert_mappings(CompanyPlan, records_to_insert)
            
            db.commit()

            return len(records_to_insert) + len(records_to_update)

        except Exception as e:
            db.rollback()
            error_msg = f"Критическая ошибка обновления планов: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            raise Exception(error_msg)
        
        finally:
            db.close()

    def update_customer_plans(self, df):
        """Обновление планов клиентов с проверкой на дубликаты"""
        if df.empty:
            print("Предупреждение: Нет данных для обновления")
            return 0

        try:
            # Получаем справочники один раз
            years = {y.Year: y.id for y in db.query(Year).all()}
            months = {m.Month: m.id for m in db.query(Month).all()}
            weeks = {(w.Week_of_Year, w.Week_of_Month): w.id for w in db.query(Week).all()}
            holdings = {h.Holding_name: h.id for h in db.query(Holding).all()}
            managers = {m.Manager_name: m.id for m in db.query(Manager).all()}
            stls = {s.STL_name: s.id for s in db.query(STL).all()}
            teamleads = {tl.TeamLead_name: tl.id for tl in db.query(TeamLead).all()}
            sectors = {s.Sector_name: s.id for s in db.query(Sector).all()}

            records_to_insert = []
            records_to_update = []
            processed_count = 0
            problem_rows = []

            # Получаем ВСЕ существующие записи с их ID
            existing_records = db.query(CustomerPlan).all()
            
            # Создаем словарь для быстрого поиска ID по уникальным полям
            existing_ids_map = {
                (rec.Year_id, rec.Month_id, rec.Week_id, rec.Holding_id, rec.Manager_id): rec.id
                for rec in existing_records
            }

            for idx, row in df.iterrows():
                try:
                    # Получаем ID для всех полей
                    year_id = years.get(int(row['Year']))
                    month_id = months.get(int(row['Month'])) if pd.notna(row['Month']) else None
                    week_id = weeks.get((int(row['Week_of_Year']), int(row['Week_of_Month'])))
                    holding_id = holdings.get(str(row['Holding']))
                    manager_id = managers.get(str(row['Manager']))
                    stl_id = stls.get(str(row['STL'])) if pd.notna(row['STL']) else None
                    teamlead_id = teamleads.get(str(row['TeamLead'])) if pd.notna(row['TeamLead']) else None
                    sector_id = sectors.get(str(row['Sector'])) if pd.notna(row['Sector']) else None

                    # Проверяем обязательные поля
                    if None in [year_id, holding_id, manager_id]:
                        missing = []
                        if year_id is None: missing.append("Year")
                        if holding_id is None: missing.append("Holding")
                        if manager_id is None: missing.append("Manager")
                        problem_rows.append({
                            'row_number': idx,
                            'missing_fields': ', '.join(missing),
                            'row_data': row.to_dict()
                        })
                        continue

                    # Формируем ключ для проверки дубликатов
                    record_key = (year_id, month_id, week_id, holding_id, manager_id)

                    # Формируем данные записи
                    record_data = {
                        'Year_id': year_id,
                        'Month_id': month_id,
                        'Week_id': week_id,
                        'Holding_id': holding_id,
                        'Manager_id': manager_id,
                        'STL_id': stl_id,
                        'TeamLead_id': teamlead_id,
                        'Sector_id': sector_id,
                        'Volume_Target_cust': self._safe_float(row, 'Volume_Target_cust'),
                        'Revenue_Target_cust': self._safe_float(row, 'Revenue_Target_cust', 0),
                        'Margin_C3_Target_cust': self._safe_float(row, 'Margin_C3_Target_cust'),
                        'Margin_C4_Target_cust': self._safe_float(row, 'Margin_C4_Target_cust', 0),
                        'Status': str(row.get('Status', 'План'))
                    }

                    # Проверяем существование записи
                    if record_key in existing_ids_map:
                        # Для обновления добавляем ID записи
                        record_data['id'] = existing_ids_map[record_key]
                        records_to_update.append(record_data)
                    else:
                        records_to_insert.append(record_data)
                    
                    processed_count += 1

                except Exception as e:
                    print(f"Ошибка обработки строки {idx}: {str(e)}")
                    continue

            # Выполняем операции с БД
            if records_to_update:
                # Обновляем существующие записи
                db.bulk_update_mappings(CustomerPlan, records_to_update)
            
            if records_to_insert:
                # Добавляем новые записи
                db.bulk_insert_mappings(CustomerPlan, records_to_insert)
            
            db.commit()

            print(f"\nИтоги обработки:")
            print(f"Обработано строк: {processed_count}/{len(df)}")
            print(f"Добавлено новых: {len(records_to_insert)}")
            print(f"Обновлено существующих: {len(records_to_update)}")
                                # В конце функции, перед return
            if problem_rows:
                problem_df = pd.DataFrame(problem_rows)
                try:
                    problem_df.to_excel("problem_rows.xlsx", index=False, encoding="utf-8")  # Попробуйте utf-8
                except Exception as e:
                    print(f"Ошибка при записи в Excel: {e}")
                    problem_df.to_csv("problem_rows.csv", index=False, encoding="utf-8") # Если Excel не удался, сохраняем в CSV
                    print("Попытка сохранения в CSV-файл.")

                print(f"Сохранено {len(problem_rows)} проблемных строк в файл problem_rows.xlsx")

            return len(records_to_insert) + len(records_to_update)

        except Exception as e:
            db.rollback()
            print(f"Критическая ошибка: {str(e)}")
            traceback.print_exc()
            raise
        finally:
            db.close()

    def _safe_float(self, row, column_name, default=0.0):
        """Безопасное преобразование в float"""
        try:
            value = row.get(column_name, default)
            if pd.isna(value) or value == '':
                return default
            return float(value)
        except (ValueError, TypeError):
            return default

    @lru_cache(maxsize=32)
    def _get_id(self, model, name_field, name, name_field2=None, name2=None):
        """Улучшенная версия с поддержкой составных ключей"""
        if not name or pd.isna(name) or name == '-':
            return None
        
        query = db.query(model).filter(getattr(model, name_field) == name)
        
        # Добавляем условие для второго поля, если указано
        if name_field2 and name2 and not pd.isna(name2) and name2 != '-':
            query = query.filter(getattr(model, name_field2) == name2)
        
        item = query.first()
        return item.id if item else None
    
    @lru_cache(maxsize=128)
    def _get_week_id(self, week_of_year, week_of_month):
        """Получение ID недели по двум параметрам с кэшированием"""
        if pd.isna(week_of_year) or pd.isna(week_of_month):
            return None
        
        week = db.query(Week).filter(
            Week.Week_of_Year == int(week_of_year),
            Week.Week_of_Month == int(week_of_month)
        ).first()
        
        return week.id if week else None

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
        """Получение планов компании через ORM с новыми связями"""
        try:
            query = db.query(
                Year.Year.label('Year'),
                Quarter.Quarter.label('Quarter'),
                Month.Month.label('Month'),
                Week.Week_of_Year.label('Week_of_Year'),
                Week.Week_of_Month.label('Week_of_Month'),
                TeamLead.TeamLead_name.label('TeamLead'),
                ABC_list.ABC_category.label('ABC'),
                CompanyPlan.Volume_Target_total,
                CompanyPlan.Revenue_Target_total,
                CompanyPlan.Margin_Target_total
            ).select_from(CompanyPlan
            ).join(CompanyPlan.year
            ).join(CompanyPlan.month
            ).join(Quarter, Month.Quarter_id == Quarter.id  # Добавлено явное соединение с Quarter
            ).join(CompanyPlan.week
            ).outerjoin(CompanyPlan.team_lead
            ).outerjoin(ABC_list, CompanyPlan.ABC_category_id == ABC_list.id)
            
            if year != '-':
                query = query.filter(Year.Year == int(year))
            if quarter != '-':
                query = query.filter(Quarter.Quarter == int(quarter))
            if month != '-':
                query = query.filter(Month.Month == int(month))
            if tl != '-':
                query = query.filter(TeamLead.TeamLead_name == tl)
            
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
                Year.Year.label('Year'),
                Quarter.Quarter.label('Quarter'),
                Month.Month.label('Month'),
                Week.Week_of_Year.label('Week_of_Year'),
                Week.Week_of_Month.label('Week_of_Month'),
                Holding.Holding_name.label('Holding'),
                Manager.Manager_name.label('Manager'),
                STL.STL_name.label('STL'),
                TeamLead.TeamLead_name.label('TeamLead'),
                CustomerPlan.Volume_Target_cust,
                CustomerPlan.Revenue_Target_cust,
                CustomerPlan.Margin_C3_Target_cust,
                CustomerPlan.Margin_C4_Target_cust
            ).join(CustomerPlan.year
            ).join(CustomerPlan.month
            ).join(Month.quarter
            ).join(CustomerPlan.week
            ).join(CustomerPlan.holding
            ).join(Manager, CustomerPlan.manager
            ).outerjoin(STL, Manager.stl
            ).join(TeamLead, Manager.team_lead)
            
            if year != '-':
                query = query.filter(Year.Year == int(year))
            if quarter != '-':
                query = query.filter(Quarter.Quarter == int(quarter))
            if month != '-':
                query = query.filter(Month.Month == int(month))
            if tl != '-':
                query = query.filter(TeamLead.TeamLead_name == tl)
            if kam != '-':
                query = query.filter(Manager.Manager_name == kam)
            if holding != '-':
                query = query.filter(Holding.Holding_name == holding)
            
            df = pd.read_sql(query.statement, db.bind)
            return df if not df.empty else pd.DataFrame()
        except Exception as e:
            print(f"Ошибка при загрузке планов клиентов: {str(e)}")
            return pd.DataFrame()
        finally:
            db.close()

    def _display_data(self, df):
        """Отображение данных в таблице с обработкой пустого DataFrame и процентов"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if df.empty:
            self.show_message('Данные не найдены')
            return
        
        # Копируем DataFrame для преобразования данных
        display_df = df.copy()
        
        # Форматирование числовых колонок
        numeric_cols = ['Volume_Target_total', 'Revenue_Target_total', 'Margin_Target_total', 
                                    'Volume_Target_cust', 'Revenue_Target_cust',
                                    'Margin_C3_Target_cust', 'Margin_C4_Target_cust']
        for col in numeric_cols:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(
                    lambda x: f"{float(x):,.2f}".replace(',', ' ').replace('.', ',') 
                    if pd.notnull(x) else '0,00')
        
        # # Преобразуем числовые значения в проценты для отображения
        percent_columns = []  # если нужно, вписать названия колонок
        for col in percent_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(
                    lambda x: f"{float(x)*100:.2f}%".replace('.', ',') 
                    if isinstance(x, (float, int)) else str(x))
        
        # Настройка таблицы
        self.table.setColumnCount(len(display_df.columns))
        self.table.setRowCount(len(display_df))
        self.table.setHorizontalHeaderLabels(display_df.columns)
        
        for row_idx, row in display_df.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                # Выравнивание чисел по правому краю
                if any(col in self.table.horizontalHeaderItem(col_idx).text() 
                for col in numeric_cols + percent_columns):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                self.table.setItem(row_idx, col_idx, item)
        
        # Автоматическое растягивание колонок
        self.table.resizeColumnsToContents()

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
                
        # Форматирование чисел
        def format_number(value):
            return f"{float(value):,.2f}".replace(',', ' ').replace('.', ',')
        
        self.ui.label_Volume.setText(f"{format_number(volume)} л." if volume != 0 else "0,00 л.")
        self.ui.label_Revenue.setText(f"{format_number(revenue)} р" if revenue != 0 else "0,00 р")
        self.ui.label_Margin.setText(f"{format_number(margin)} р" if margin != 0 else "0,00 р")
        
        if volume != 0:
            unit_margin = margin / volume
            self.ui.label_uC3.setText(f"{format_number(unit_margin)} р/л")
        else:
            self.ui.label_uC3.setText("0,00 р/л")
    
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
            # Исправлено: запрашиваем годы из таблицы Year, а не Calendar
            years = db.query(Year.Year).distinct().order_by(Year.Year.desc()).all()
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
                # Правильный путь связей: Holding -> customers -> contracts -> manager
                query = query.join(Holding.customers)\
                            .join(Customer.contracts)\
                            .join(Contract.manager)\
                            .filter(Manager.Manager_name == kam)
            
            holdings = query.all()
            holdings_list = [h[0] for h in holdings] if holdings else []
            self._fill_combobox(self.ui.line_Holding, holdings_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка холдингов: {str(e)}")
            self._fill_combobox(self.ui.line_Holding, [])
        finally:
            db.close()

    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса с обработкой пустого списка"""
        combobox.clear()
        combobox.addItem('-')  # Всегда добавляем "-" как первый элемент
        
        if items:  # Добавляем остальные элементы только если они есть
            combobox.addItems(items)
    
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
    
     

