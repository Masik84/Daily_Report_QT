import os
import pandas as pd
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QWidget, QHeaderView, QApplication
from PySide6.QtCore import Qt

from db import db
from models import Fees, EcoFee_amount, EcoFee_standard, TNVED
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
            # Определяем путь к файлу
            file_path = self.ui.label_tax_File.text()
            if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
                file_path = All_data_file

            # Проверка существования файла
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {os.path.basename(file_path)} не найден")

            try:
                # Основные операции выполняем в отдельной сессии
                db.begin()
                
                try:
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
    
    def _upload_fees_data(self, file_path):
        """Загрузка данных о тарифах"""
        try:
            dtype_fees = {"Год": int, "Месяц": int}
            df = pd.read_excel(file_path, sheet_name="TaxFee", dtype=dtype_fees)
            
            column_map = {
                "Год": "Year", "Месяц": "Month", "Акциз": "Excise",
                "Тамож. оформление": "Customs_clearance", "Комиссия банка": "Bank_commission",
                "Эко сбор ст-ть": "Eco_fee_amount", "Эко сбор норм": "Eco_fee_standard",
                "Транспорт (перемещ), л": "Transportation", "Хранение, л": "Storage",
                "Ст-ть Денег": "Money_cost", "Доп% денег": "Additional_money_percent"
            }
            df = df.rename(columns=column_map)
            
            # Обработка процентов
            percent_cols = ["Bank_commission", "Eco_fee_standard", "Money_cost", "Additional_money_percent"]
            for col in percent_cols:
                if col in df.columns:
                    df[col] = df[col].str.rstrip('%').astype(float) / 100
            
            records = df.to_dict('records')
            
            existing = {(f.Year, f.Month) for f in db.query(Fees.Year, Fees.Month).all()}
            
            to_insert = []
            to_update = []
            
            for record in records:
                key = (record['Year'], record['Month'])
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
        finally:
            db.close()
    
    def _upload_ecofee_data(self, file_path):
        """Загрузка данных об экосборах"""
        try:
            dtype_tnved = {"Код ТНВЭД": str}
            
            # Чтение данных о ставках
            df_amount = pd.read_excel(file_path, sheet_name="экосбор_ставки", dtype=dtype_tnved, skiprows=1)
            df_amount_long = df_amount.melt(id_vars=["Код ТНВЭД", "признак", "группа"], var_name="Год", value_name="Сумма")
            df_amount_long["Год"] = df_amount_long["Год"].astype(int)
            
            # Чтение данных о нормативах
            df_standard = pd.read_excel(file_path, sheet_name="экосбор_норматив", dtype=dtype_tnved, skiprows=1)
            df_standard_long = df_standard.melt(id_vars=["Код ТНВЭД", "признак", "группа"], var_name="Год", value_name="Норма")
            df_standard_long["Год"] = df_standard_long["Год"].astype(int)
            df_standard_long["Норма"] = df_standard_long["Норма"].str.rstrip('%').astype(float) / 100
            
            # Добавляем новые коды ТНВЭД
            existing_tnved = {t.code for t in db.query(TNVED.code).all()}
            new_tnved = set(df_amount_long["Код ТНВЭД"].unique()) - existing_tnved
            
            if new_tnved:
                db.bulk_insert_mappings(TNVED, [{"code": code} for code in new_tnved])
            
            # Получаем ID всех ТНВЭД
            tnved_ids = {t.code: t.id for t in db.query(TNVED).all()}
            
            # Подготовка данных для вставки
            amount_data = []
            for _, row in df_amount_long.iterrows():
                tnved_id = tnved_ids.get(row["Код ТНВЭД"])
                if tnved_id:
                    amount_data.append({
                        "TNVED_id": tnved_id,
                        "Year": row["Год"],
                        "ECO_amount": row["Сумма"],
                        "merge": f"{row['Код ТНВЭД']}_{row['Год']}"
                    })
            
            standard_data = []
            for _, row in df_standard_long.iterrows():
                tnved_id = tnved_ids.get(row["Код ТНВЭД"])
                if tnved_id:
                    standard_data.append({
                        "TNVED_id": tnved_id,
                        "Year": row["Год"],
                        "ECO_standard": row["Норма"],
                        "merge": f"{row['Код ТНВЭД']}_{row['Год']}"
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
        finally:
            db.close()
    
    def find_cost(self):
        """Поиск данных по заданным критериям с учетом всех условий"""
        try:
            data_type = self.ui.line_taxfee_type.currentText()
            
            # Условие 1: Проверка выбранного типа данных
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
                
                # Условие 3: Все данные если нет фильтров
                if tnved_code == "-" and year == "-":
                    data = self._get_ecofee_data()
                    self._display_ecofee_data(data)
                    return
                    
                # Условие 4: Проверки для ТНВЭД
                if tnved_code:
                    # 4.a: Проверка на цифры
                    if not tnved_code.isdigit():
                        self.show_error_message("В поле должны быть только цифры")
                        return
                    
                    # 4.b: Проверка существования ТНВЭД
                    try:
                        exists = db.query(TNVED).filter(TNVED.code == tnved_code).first() is not None
                        if not exists:
                            self.show_error_message("Такого кода ТНВЭД в базе не существует")
                            return
                    except Exception as e:
                        self.show_error_message(f"Ошибка проверки кода ТНВЭД: {str(e)}")
                        return
                    finally:
                        if db.is_active:
                            db.close()
                
                # Применяем фильтры
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
            query = db.query(Fees)
            
            if year and year != '-':
                query = query.filter(Fees.Year == int(year))
            if month and month != '-':
                query = query.filter(Fees.Month == int(month))
            
            fees = query.order_by(Fees.Year, Fees.Month).all()
            
            result = []
            for fee in fees:
                result.append({
                    "Год": fee.Year,
                    "Месяц": fee.Month,
                    "Акциз": fee.Excise,
                    "Тамож. оформление": fee.Customs_clearance,
                    "Комиссия банка": fee.Bank_commission,
                    "Эко сбор ст-ть": fee.Eco_fee_amount,
                    "Эко сбор норм": fee.Eco_fee_standard,
                    "Транспорт (перемещ), л": fee.Transportation,
                    "Хранение, л": fee.Storage,
                    "Ст-ть Денег": fee.Money_cost,
                    "Доп% денег": fee.Additional_money_percent
                })
            
            return result
        except Exception as e:
            self.show_error_message(f"Ошибка получения данных тарифов: {str(e)}")
            return []
        finally:
            if db.is_active:
                db.close()

    def _get_ecofee_data(self, tnved_code=None, year=None):
        """Получение данных об экосборах с фильтрацией"""
        try:
            query = (
                db.query(
                    TNVED.code.label("ТНВЭД"),
                    EcoFee_amount.Year.label("Год"),
                    EcoFee_amount.ECO_amount.label("Эко Ставка"),
                    EcoFee_standard.ECO_standard.label("Эко Норматив")
                )
                .join(EcoFee_amount, EcoFee_amount.TNVED_id == TNVED.id)
                .join(EcoFee_standard, and_(
                    EcoFee_standard.TNVED_id == TNVED.id,
                    EcoFee_standard.Year == EcoFee_amount.Year
                ))
            )
            
            if tnved_code:
                query = query.filter(TNVED.code == tnved_code)
            if year:
                query = query.filter(EcoFee_amount.Year == int(year))
            
            ecofee_data = query.order_by(TNVED.code, EcoFee_amount.Year).all()
            
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
        finally:
            if db.is_active:
                db.close()

    def _validate_tnved_code(self, tnved_code):
        """Проверка кода ТНВЭД"""
        if not tnved_code.isdigit():
            return False, "В поле должны быть только цифры"
        
        try:
            exists = db.query(TNVED).filter(TNVED.code == tnved_code).first() is not None
            if not exists:
                return False, "Такого кода ТНВЭД в базе не существует"
            return True, None
        except Exception as e:
            return False, f"Ошибка проверки кода ТНВЭД: {str(e)}"
        finally:
            if db.is_active:
                db.close()
    
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
            # Получаем года из Fees
            years_fees = {y[0] for y in db.query(Fees.Year).distinct().all()}
            
            # Получаем года из EcoFee_amount
            years_ecofee = {y[0] for y in db.query(EcoFee_amount.Year).distinct().all()}
            
            # Объединяем и сортируем
            all_years = sorted(years_fees.union(years_ecofee))
            
            self._fill_combobox(self.ui.line_Year, all_years)
        except Exception as e:
            self.show_error_message(f"Ошибка при загрузке списка годов: {str(e)}")
            self._fill_combobox(self.ui.line_Year, [])
        finally:
            if db.is_active:
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

    def show_message(self, text):
        """Показать информационное сообщение с кнопкой копирования"""
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

        clipboard = QApplication.clipboard()
        copy_button = msg.addButton("Copy msg", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        copy_button.clicked.connect(lambda: None)

        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке с кнопкой копирования"""
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

        clipboard = QApplication.clipboard()
        copy_button = msg.addButton("Copy msg", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: clipboard.setText(text))
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        copy_button.clicked.connect(lambda: None)

        msg.exec_()



