import os
import pandas as pd
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, 
                              QWidget, QHeaderView, QApplication, QTextEdit)
from PySide6.QtCore import Qt
from functools import lru_cache

from db import db
from models import Fees, EcoFee_amount, EcoFee_standard, TNVED, Year, Month
from config import All_data_file
from wind.pages.taxfees_ui import Ui_Form

class Costs(QWidget):
    def __init__(self):
        super(Costs, self).__init__()
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
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_cost)
    
    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с данными')
        if file_path:
            self.ui.label_tax_File.setText(file_path)
        
    def upload_data(self):
        """Загрузка данных в базу - обновление всех таблиц"""
        try:
            file_path = self.ui.label_tax_File.text()
            if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
                file_path = All_data_file

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {os.path.basename(file_path)} не найден")

            try:
                db.begin()
                
                try:
                    # Обновляем календарные таблицы
                    calendar_df = pd.read_excel(file_path, sheet_name="Календарь")
                    self._update_calendar_tables(calendar_df)
                    
                    # Загружаем данные тарифов
                    success_fees, msg_fees = self._upload_fees_data(file_path)
                    # Загружаем данные экосборов
                    success_eco, msg_eco = self._upload_ecofee_data(file_path)
                    
                    if success_fees and success_eco:
                        db.commit()
                        self.show_message("Все данные успешно загружены!\n"
                            f"Тарифы: {msg_fees}\n"
                            f"Экосборы: {msg_eco}"
                        )
                        self.refresh_all_comboboxes()
                    else:
                        db.rollback()
                        error_msg = ""
                        if not success_fees:
                            error_msg += f"Ошибка тарифов: {msg_fees}\n"
                        if not success_eco:
                            error_msg += f"Ошибка экосборов: {msg_eco}"
                        self.show_error_message(error_msg)
                    
                except Exception as e:
                    db.rollback()
                    raise
                    
            except SQLAlchemyError as e:
                raise Exception(f"Ошибка базы данных: {str(e)}")
                
        except FileNotFoundError as e:
            self.show_error_message(str(e))
        except ValueError as e:
            self.show_error_message(f"Ошибка в данных: {str(e)}")
        except Exception as e:
            self.show_error_message(f"Ошибка загрузки: {str(e)}")
        finally:
            if db.is_active:
                db.close()
    
    def _update_calendar_tables(self, data):
        """Обновление таблиц Year, Month для Costs"""
        try:
            # Получаем уникальные года и месяцы
            years = data['Year'].unique()
            months = data['Month'].unique()
            
            # Добавляем новые года
            for year in years:
                if not db.query(Year).filter(Year.Year == year).first():
                    db.add(Year(Year=year))
            
            # Добавляем новые месяцы
            for month in months:
                if not db.query(Month).filter(Month.Month == month).first():
                    db.add(Month(Month=month))
            
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Ошибка обновления календарных таблиц: {str(e)}")
    
    def _upload_fees_data(self, file_path):
        """Загрузка данных о тарифах с новыми связями"""
        try:
            dtype_fees = {"Год": int, "Месяц": int}
            df = pd.read_excel(file_path, sheet_name="TaxFee", dtype=dtype_fees)
            
            column_map = {
                "Год": "year_id", "Месяц": "month_id", "Акциз": "Excise",
                "Тамож. оформление": "Customs_clearance", "Комиссия банка": "Bank_commission",
                "Эко сбор ст-ть": "Eco_fee_amount", "Эко сбор норм": "Eco_fee_standard",
                "Транспорт (перемещ), л": "Transportation", "Хранение, л": "Storage",
                "Ст-ть Денег": "Money_cost", "Доп% денег": "Additional_money_percent"
            }
            df = df.rename(columns=column_map)
            
            # Получаем ID для года и месяца
            df['year_id'] = df['year_id'].apply(lambda x: self._get_id(Year, 'Year', x))
            df['month_id'] = df['month_id'].apply(lambda x: self._get_id(Month, 'Month', x))
            
            # Обработка процентов
            percent_cols = ["Bank_commission", "Eco_fee_standard", "Money_cost", "Additional_money_percent"]
            for col in percent_cols:
                if col in df.columns:
                    df[col] = df[col].str.rstrip('%').astype(float) / 100
            
            records = df.to_dict('records')
            
            existing = {(f.year_id, f.month_id) for f in db.query(Fees.year_id, Fees.month_id).all()}
            
            to_insert = []
            to_update = []
            
            for record in records:
                key = (record['year_id'], record['month_id'])
                if key in existing:
                    to_update.append(record)
                else:
                    to_insert.append(record)
            
            if to_insert:
                db.bulk_insert_mappings(Fees, to_insert)
            if to_update:
                db.bulk_update_mappings(Fees, to_update)
            
            return True, "Данные тарифов успешно обновлены"
        except Exception as e:
            return False, f"Ошибка загрузки данных тарифов: {str(e)}"
    
    def _upload_ecofee_data(self, file_path):
        """Загрузка данных об экосборах с новыми связями"""
        try:
            dtype_tnved = {"Код ТНВЭД": str}
            
            # Чтение данных о ставках
            df_amount = pd.read_excel(file_path, sheet_name="экосбор_ставки", dtype=dtype_tnved, skiprows=1)
            df_amount_long = df_amount.melt(id_vars=["Код ТНВЭД", "признак", "группа"], var_name="year_id", value_name="ECO_amount")
            df_amount_long["year_id"] = df_amount_long["year_id"].astype(int)
            
            # Чтение данных о нормативах
            df_standard = pd.read_excel(file_path, sheet_name="экосбор_норматив", dtype=dtype_tnved, skiprows=1)
            df_standard_long = df_standard.melt(id_vars=["Код ТНВЭД", "признак", "группа"], var_name="year_id", value_name="ECO_standard")
            df_standard_long["year_id"] = df_standard_long["year_id"].astype(int)
            df_standard_long["ECO_standard"] = df_standard_long["ECO_standard"].str.rstrip('%').astype(float) / 100
            
            # Добавляем новые коды ТНВЭД
            existing_tnved = {t.code for t in db.query(TNVED.code).all()}
            new_tnved = set(df_amount_long["Код ТНВЭД"].unique()) - existing_tnved
            
            if new_tnved:
                db.bulk_insert_mappings(TNVED, [{"code": code} for code in new_tnved])
                db.commit()
            
            # Получаем ID всех ТНВЭД и годов
            tnved_ids = {t.code: t.id for t in db.query(TNVED).all()}
            year_ids = {y.Year: y.id for y in db.query(Year).all()}
            
            # Подготовка данных для вставки
            amount_data = []
            for _, row in df_amount_long.iterrows():
                tnved_id = tnved_ids.get(row["Код ТНВЭД"])
                year_id = year_ids.get(row["year_id"])
                if tnved_id and year_id:
                    amount_data.append({
                        "TNVED_id": tnved_id,
                        "year_id": year_id,
                        "ECO_amount": row["ECO_amount"],
                        "merge": f"{row['Код ТНВЭД']}_{row['year_id']}"
                    })
            
            standard_data = []
            for _, row in df_standard_long.iterrows():
                tnved_id = tnved_ids.get(row["Код ТНВЭД"])
                year_id = year_ids.get(row["year_id"])
                if tnved_id and year_id:
                    standard_data.append({
                        "TNVED_id": tnved_id,
                        "year_id": year_id,
                        "ECO_standard": row["ECO_standard"],
                        "merge": f"{row['Код ТНВЭД']}_{row['year_id']}"
                    })
            
            # Обновление существующих записей
            existing_amount = {e.merge for e in db.query(EcoFee_amount.merge).all()}
            existing_standard = {e.merge for e in db.query(EcoFee_standard.merge).all()}
            
            to_insert_amount = [d for d in amount_data if d["merge"] not in existing_amount]
            to_update_amount = [d for d in amount_data if d["merge"] in existing_amount]
            
            to_insert_standard = [d for d in standard_data if d["merge"] not in existing_standard]
            to_update_standard = [d for d in standard_data if d["merge"] in existing_standard]
            
            # Выполняем операции
            if to_insert_amount:
                db.bulk_insert_mappings(EcoFee_amount, to_insert_amount)
            if to_update_amount:
                db.bulk_update_mappings(EcoFee_amount, to_update_amount)
            
            if to_insert_standard:
                db.bulk_insert_mappings(EcoFee_standard, to_insert_standard)
            if to_update_standard:
                db.bulk_update_mappings(EcoFee_standard, to_update_standard)
            
            return True, "Данные экосборов успешно обновлены"
        except Exception as e:
            return False, f"Ошибка загрузки данных экосборов: {str(e)}"
    
    def find_cost(self):
        """Поиск данных по заданным критериям с учетом всех условий"""
        try:
            data_type = self.ui.line_taxfee_type.currentText()
            
            if data_type == "-":
                self.show_error_message("Выбери тип данных")
                return
            
            if data_type == "Тарифы":
                year = self.ui.line_Year.currentText()
                month = self.ui.line_Mnth.currentText()
                
                if year == "-" and month == "-":
                    data = self._get_fees_data()
                elif year != "-" and month == "-":
                    data = self._get_fees_data(year=year)
                elif year != "-" and month != "-":
                    data = self._get_fees_data(year=year, month=month)
                elif year == "-" and month != "-":
                    data = self._get_fees_data(month=month)
                
                self._display_fees_data(data)
                
            elif data_type == "Эко Сбор":
                tnved_code = self.ui.lineEdit_TNVED.text().strip()
                year = self.ui.line_Year.currentText()
                
                if tnved_code == "-" and year == "-":
                    data = self._get_ecofee_data()
                    self._display_ecofee_data(data)
                    return
                    
                if tnved_code:
                    if not tnved_code.isdigit():
                        self.show_error_message("В поле должны быть только цифры")
                        return
                    
                    try:
                        exists = db.query(TNVED).filter(TNVED.code == tnved_code).first() is not None
                        if not exists:
                            self.show_error_message("Такого кода ТНВЭД в базе не существует")
                            return
                    except Exception as e:
                        self.show_error_message(f"Ошибка проверки кода ТНВЭД: {str(e)}")
                        return
                
                tnved_filter = tnved_code if tnved_code != "-" else None
                year_filter = year if year != "-" else None
                
                data = self._get_ecofee_data(tnved_code=tnved_filter, year=year_filter)
                self._display_ecofee_data(data)
                
        except Exception as e:
            self.show_error_message(f"Ошибка при поиске данных: {str(e)}")
        finally:
            db.close()
            
    def _get_fees_data(self, year=None, month=None):
        """Получение данных о тарифах с фильтрацией"""
        try:
            query = db.query(
                Year.Year.label("Год"),
                Month.Month.label("Месяц"),
                Fees.Excise,
                Fees.Customs_clearance,
                Fees.Bank_commission,
                Fees.Eco_fee_amount,
                Fees.Eco_fee_standard,
                Fees.Transportation,
                Fees.Storage,
                Fees.Money_cost,
                Fees.Additional_money_percent
            ).join(Fees.year
            ).join(Fees.month)
            
            if year and year != '-':
                query = query.filter(Year.Year == int(year))
            if month and month != '-':
                query = query.filter(Month.Month == int(month))
            
            fees = query.order_by(Year.Year, Month.Month).all()
            
            result = []
            for row in fees:
                result.append({
                    "Год": row.Год,
                    "Месяц": row.Месяц,
                    "Акциз": row.Excise,
                    "Тамож. оформление": row.Customs_clearance,
                    "Комиссия банка": row.Bank_commission,
                    "Эко сбор ст-ть": row.Eco_fee_amount,
                    "Эко сбор норм": row.Eco_fee_standard,
                    "Транспорт (перемещ), л": row.Transportation,
                    "Хранение, л": row.Storage,
                    "Ст-ть Денег": row.Money_cost,
                    "Доп% денег": row.Additional_money_percent
                })
            
            return result
        except Exception as e:
            self.show_error_message(f"Ошибка получения данных тарифов: {str(e)}")
            return []
    
    def _get_ecofee_data(self, tnved_code=None, year=None):
        """Получение данных об экосборах с фильтрацией"""
        try:
            query = (
                db.query(
                    TNVED.code.label("ТНВЭД"),
                    Year.Year.label("Год"),
                    EcoFee_amount.ECO_amount.label("Эко Ставка"),
                    EcoFee_standard.ECO_standard.label("Эко Норматив")
                )
                .join(EcoFee_amount, EcoFee_amount.TNVED_id == TNVED.id)
                .join(EcoFee_amount.year)
                .join(EcoFee_standard, and_(
                    EcoFee_standard.TNVED_id == TNVED.id,
                    EcoFee_standard.year_id == EcoFee_amount.year_id
                ))
            )
            
            if tnved_code:
                query = query.filter(TNVED.code == tnved_code)
            if year:
                query = query.filter(Year.Year == int(year))
            
            ecofee_data = query.order_by(TNVED.code, Year.Year).all()
            
            result = []
            for row in ecofee_data:
                result.append({
                    "ТНВЭД": row.ТНВЭД,
                    "Год": row.Год,
                    "Эко Ставка": row.Эко_Ставка,
                    "Эко Норматив": row.Эко_Норматив
                })
            
            return result
        except Exception as e:
            self.show_error_message(f"Ошибка получения данных экосборов: {str(e)}")
            return []
    
    def _display_fees_data(self, data):
        """Отображение данных о тарифах"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if not data:
            self.show_message("Нет данных о тарифах для отображения")
            return
        
        headers = list(data[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(headers):
                value = row_data[col_name]
                
                if col_name in ["Комиссия банка", "Эко сбор норм", "Ст-ть Денег", "Доп% денег"]:
                    display_value = f"{float(value)*100:.2f}%" if value is not None else ""
                else:
                    try:
                        display_value = f"{float(value):,.2f}".replace(",", " ").replace(".", ",") if value is not None else ""
                    except (ValueError, TypeError):
                        display_value = str(value) if value is not None else ""
                
                item = QTableWidgetItem(display_value)
                item.setData(Qt.DisplayRole, value)
                self.table.setItem(row_idx, col_idx, item)
    
    def _display_ecofee_data(self, data):
        """Отображение данных об экосборах"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if not data:
            self.show_message("Нет данных об экосборах для отображения")
            return
        
        headers = ["ТНВЭД", "Год", "Эко Ставка", "Эко Норматив"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, col_name in enumerate(headers):
                value = row_data[col_name]
                
                if col_name == "Эко Норматив":
                    display_value = f"{float(value)*100:.2f}%" if value is not None else ""
                elif col_name == "Эко Ставка":
                    try:
                        display_value = f"{float(value):,.2f}".replace(",", " ").replace(".", ",") if value is not None else ""
                    except (ValueError, TypeError):
                        display_value = str(value) if value is not None else ""
                else:
                    display_value = str(value) if value is not None else ""
                
                item = QTableWidgetItem(display_value)
                item.setData(Qt.DisplayRole, value)
                self.table.setItem(row_idx, col_idx, item)

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self.fill_in_year_list()
        self.fill_in_mnth_list()
        
    def fill_in_year_list(self):
        """Заполнение списка годов"""
        try:
            # Получаем года из Year
            years = db.query(Year.Year).distinct().order_by(Year.Year.desc()).all()
            years_list = [str(y[0]) for y in years] if years else []
            self._fill_combobox(self.ui.line_Year, years_list)
        except Exception as e:
            print(f"Ошибка при загрузке списка годов: {str(e)}")
            self._fill_combobox(self.ui.line_Year, [])
        finally:
            db.close()
    
    def fill_in_mnth_list(self):
        """Заполнение списка месяцев"""
        self._fill_combobox(self.ui.line_Mnth, ['-'] + [str(i) for i in range(1, 13)])
    
    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if items:
            combobox.addItems([str(item) for item in sorted(items)])
            
    
    @lru_cache(maxsize=32)
    def _get_id(self, model, name_field, name):
        """Получение ID по имени (с кэшированием)"""
        if not name or pd.isna(name) or name == '-':
            return None
        
        item = db.query(model).filter(getattr(model, name_field) == name).first()
        return item.id if item else None

    def show_message(self, text):
        """Показать информационное сообщение"""
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setMinimumSize(400, 200)
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        clipboard = QApplication.clipboard()
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setMinimumSize(400, 200)
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        clipboard = QApplication.clipboard()
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        msg.exec_()



