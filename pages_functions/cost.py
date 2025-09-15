
import os
import pandas as pd
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, 
                              QWidget, QHeaderView, QApplication, QMenu)
from PySide6.QtCore import Qt
from functools import lru_cache
import math  # Import the math module

from db import db
from models import Fees, EcoFee_amount, EcoFee_standard, TNVED, Year, Month, Customs_Rate
from config import All_data_file
from wind.pages.taxfees_ui import Ui_Form

class CostsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.line_taxfee_type.clear()
        self.ui.line_taxfee_type.addItems(["-", "Тарифы", "Эко Сбор", "Пошлины"])

        self._setup_ui()
        self._setup_connections()
        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса таблицы"""
        self.table = self.ui.table

        # Базовые настройки таблицы
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # Выделение отдельных ячеек
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Запрет редактирования
        self.table.setAlternatingRowColors(True)  # Чередование цветов строк
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Изменяемые размеры
        self.table.horizontalHeader().setStretchLastSection(True)  # Растягивание последнего столбца
        self.table.verticalHeader().setVisible(False)  # Скрытие вертикальных заголовков
        self.table.setSortingEnabled(True)  # Сортировка по клику на заголовок
        self.table.setWordWrap(False)  # Запрет переноса слов
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)  # Обрезка длинного текста

        # Настройка контекстного меню для копирования
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        # Стилизация таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                selection-background-color: #3daee9;
                selection-color: black;
            }
            QTableWidget::item {
                padding: 3px;
            }
        """)

    def show_context_menu(self, position):
        """Показ контекстного меню для копирования"""
        menu = QMenu()
        copy_action = menu.addAction("Копировать")
        copy_action.triggered.connect(self.copy_cell_content)
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def copy_cell_content(self):
        """Копирование содержимого выделенных ячеек"""
        selected_items = self.table.selectedItems()
        if selected_items:
            clipboard = QApplication.clipboard()
            # Если выделена одна ячейка - копируем только ее
            if len(selected_items) == 1:
                text = selected_items[0].text()
            else:
                # Если выделено несколько ячеек - копируем с разделением табуляцией и переносом строк
                rows = {}
                for item in selected_items:
                    row = item.row()
                    col = item.column()
                    if row not in rows:
                        rows[row] = {}
                    rows[row][col] = item.text()

                # Сортируем ячейки по строкам и столбцам
                sorted_rows = sorted(rows.items())
                text = ""
                for row, cols in sorted_rows:
                    sorted_cols = sorted(cols.items())
                    text += "\t".join([text for col, text in sorted_cols]) + "\n"

            clipboard.setText(text.strip())

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

            # Начинаем транзакцию
            db.begin()
            
            try:
                # 1. Обновляем календарные таблицы
                try:
                    calendar_df = pd.read_excel(file_path, sheet_name="Календарь")
                    self._update_calendar_tables(calendar_df)
                except Exception as e:
                    raise Exception(f"Ошибка обновления календаря: {str(e)}")

                # 2. Загружаем данные тарифов
                try:
                    success_fees, msg_fees = self._upload_fees_data(file_path)
                    if not success_fees:
                        raise Exception(msg_fees)
                except Exception as e:
                    raise Exception(f"Ошибка загрузки тарифов: {str(e)}")

                # 3. Загружаем данные экосборов
                try:
                    success_eco, msg_eco = self._upload_ecofee_data(file_path)
                    if not success_eco:
                        raise Exception(msg_eco)
                except Exception as e:
                    raise Exception(f"Ошибка загрузки экосборов: {str(e)}")
                
                # 4. Загружаем данные пошлин
                try:
                    success_customs, msg_customs = self._upload_customs_rates_data(file_path)
                    if not success_customs:
                        raise Exception(msg_customs)
                except Exception as e:
                    raise Exception(f"Ошибка загрузки пошлин: {str(e)}")

                # Если все успешно - коммитим
                db.commit()
                
                # Показываем успешное сообщение
                success_msg = "Все данные успешно загружены!\n"
                success_msg += f"Тарифы: {msg_fees}\n"
                success_msg += f"Экосборы: {msg_eco}\n"
                success_msg += f"Пошлины: {msg_customs}"
                
                self.show_message(success_msg)
                self.refresh_all_comboboxes()

            except Exception as e:
                db.rollback()
                error_msg = f"Ошибка при загрузке данных:\n{str(e)}\n\n"
                error_msg += "Все изменения отменены (rollback выполнен)."
                self.show_error_message(error_msg)
                
        except FileNotFoundError as e:
            self.show_error_message(f"Файл не найден: {str(e)}")
        except Exception as e:
            error_msg = f"Критическая ошибка при загрузке:\n{str(e)}\n\n"
            error_msg += "Проверьте:\n1. Формат файла\n2. Наличие всех листов\n3. Данные в файле"
            self.show_error_message(error_msg)
        finally:
            if db.is_active:
                db.close()

    def _update_calendar_tables(self, data):
        """Обновление таблиц Year, Month для Costs"""
        try:
            # Получаем уникальные года и месяцы, преобразуя numpy.int64 в int
            years = [int(year) for year in data['Year'].unique()]
            months = [int(month) for month in data['Month'].unique()]

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
                "Ст-ть Денег": "Money_cost", "Доп% денег": "Additional_money_percent",
                "Оклейка остатков": 'Okleyka'
            }
            df = df.rename(columns=column_map)

            # Получаем ID для года и месяца
            df['year_id'] = df['year_id'].apply(lambda x: self._get_id(Year, 'Year', int(x) if not pd.isna(x) else None)) # Modified line
            df['month_id'] = df['month_id'].apply(lambda x: self._get_id(Month, 'Month', int(x) if not pd.isna(x) else None)) # Modified line

            records = df.to_dict('records')

            # Fetch all existing Fees records as objects
            existing_fees = db.query(Fees).filter(Fees.year_id.in_([r['year_id'] for r in records if r['year_id'] is not None]),
                                                Fees.month_id.in_([r['month_id'] for r in records if r['month_id'] is not None])).all()
            existing_dict = {(f.year_id, f.month_id): f for f in existing_fees}

            to_insert = []
            to_update = []

            for record in records:
                # Handle NaN values for year_id and month_id before inserting/updating
                if pd.isna(record['year_id']) or pd.isna(record['month_id']):
                    continue  # Skip this record if year_id or month_id is NaN

                record['year_id'] = int(record['year_id'])  # Ensure it's an integer
                record['month_id'] = int(record['month_id'])  # Ensure it's an integer

                key = (record['year_id'], record['month_id'])
                if key in existing_dict:
                    # Add the ID to the record being updated
                    fee_object = existing_dict[key]
                    record['id'] = fee_object.id
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

            # Добавляем новые коды ТНВЭД
            existing_tnved = {t.code for t in db.query(TNVED.code).all()}
            new_tnved = set(df_amount_long["Код ТНВЭД"].unique()) - existing_tnved

            if new_tnved:
                db.bulk_insert_mappings(TNVED, [{"code": code} for code in new_tnved])
                db.commit()

            # Получаем ID всех ТНВЭД и годов
            tnved_ids = {t.code: t.id for t in db.query(TNVED).all()}
            year_ids = {y.Year: y.id for y in db.query(Year).all()}

            # Подготовка данных для amount вставки
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

            # Подготовка данных для standard вставки
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

            # Fetch existing EcoFee_amount records as objects
            existing_amounts = db.query(EcoFee_amount).filter(EcoFee_amount.merge.in_([d["merge"] for d in amount_data])).all()
            existing_amount_dict = {e.merge: e for e in existing_amounts}

            # Создаем списки для вставки и обновления (amount)
            to_insert_amount = []
            to_update_amount = []

            # Populate the `to_update_amount` and `to_insert_amount` lists correctly
            for d in amount_data:
                if d["merge"] in existing_amount_dict:
                    ecofee_amount_object = existing_amount_dict[d["merge"]]
                    d["id"] = ecofee_amount_object.id  # Add the ID
                    to_update_amount.append(d)
                else:
                    to_insert_amount.append(d)

            # Fetch existing EcoFee_standard records as objects (Corrected table name)
            existing_standards = db.query(EcoFee_standard).filter(EcoFee_standard.merge.in_([d["merge"] for d in standard_data])).all()
            existing_standard_dict = {e.merge: e for e in existing_standards}

            # Создаем списки для вставки и обновления (standard)
            to_insert_standard = []
            to_update_standard = []

            # Populate the `to_update_standard` and `to_insert_standard` lists correctly
            for d in standard_data:
                if d["merge"] in existing_standard_dict:
                    ecofee_standard_object = existing_standard_dict[d["merge"]]
                    d["id"] = ecofee_standard_object.id  # Add the ID
                    to_update_standard.append(d)
                else:
                    to_insert_standard.append(d)

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
    
    def _upload_customs_rates_data(self, file_path):
        """Загрузка данных о пошлинах из Excel"""
        try:
            dtype_tnved = {"Код ТНВЭД": str, "Пошлина": float}
            df = pd.read_excel(file_path, sheet_name="Пошлины", dtype=dtype_tnved)
            
            # Фильтруем строки с NaN в коде ТНВЭД
            df = df.dropna(subset=["Код ТНВЭД"])
            
            # Также фильтруем строки, где код ТНВЭД равен строке "NaN"
            df = df[df["Код ТНВЭД"].str.lower() != "nan"]
            
            # Добавляем новые коды ТНВЭД, если их нет
            existing_tnved = {t.code for t in db.query(TNVED.code).all()}
            new_tnved = set(df["Код ТНВЭД"].unique()) - existing_tnved
            
            if new_tnved:
                # Дополнительная фильтрация - только валидные коды
                valid_new_tnved = [code for code in new_tnved 
                                if code and str(code).strip() and str(code).lower() != 'nan']
                
                if valid_new_tnved:
                    db.bulk_insert_mappings(TNVED, [{"code": code} for code in valid_new_tnved])
                    db.commit()
            
            # Получаем ID всех ТНВЭД
            tnved_ids = {t.code: t.id for t in db.query(TNVED).all()}
            
            # Подготовка данных для вставки
            customs_data = []
            for _, row in df.iterrows():
                tnved_code = row["Код ТНВЭД"]
                # Пропускаем невалидные коды
                if pd.isna(tnved_code) or str(tnved_code).lower() == 'nan' or not str(tnved_code).strip():
                    continue
                    
                tnved_id = tnved_ids.get(str(tnved_code).strip())
                if tnved_id:
                    customs_data.append({
                        "TNVED_id": tnved_id,
                        "Cust_rate": row["Пошлина"]
                    })
            
            # Получаем существующие записи
            existing_rates = db.query(Customs_Rate).filter(Customs_Rate.TNVED_id.in_([d["TNVED_id"] for d in customs_data])).all()
            existing_dict = {r.TNVED_id: r for r in existing_rates}
            
            # Разделяем на вставку и обновление
            to_insert = []
            to_update = []
            
            for d in customs_data:
                if d["TNVED_id"] in existing_dict:
                    rate_object = existing_dict[d["TNVED_id"]]
                    d["id"] = rate_object.id
                    to_update.append(d)
                else:
                    to_insert.append(d)
            
            # Выполняем операции
            if to_insert:
                db.bulk_insert_mappings(Customs_Rate, to_insert)
            if to_update:
                db.bulk_update_mappings(Customs_Rate, to_update)
            
            return True, "Данные пошлин успешно обновлены"
        except Exception as e:
            return False, f"Ошибка загрузки данных пошлин: {str(e)}"

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

                if tnved_code and tnved_code != "-":
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

                tnved_filter = tnved_code if tnved_code != "-" and tnved_code else None
                year_filter = year if year != "-" else None

                data = self._get_ecofee_data(tnved_code=tnved_filter, year=year_filter)
                self._display_ecofee_data(data)

            elif data_type == "Пошлины":
                tnved_code = self.ui.lineEdit_TNVED.text().strip()
                
                if tnved_code and tnved_code != "-":
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

                tnved_filter = tnved_code if tnved_code != "-" and tnved_code else None
                data = self._get_customs_rates_data(tnved_code=tnved_filter)
                self._display_customs_rates_data(data)

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
                Fees.Transportation,
                Fees.Storage,
                Fees.Money_cost,
                Fees.Additional_money_percent,
                Fees.Okleyka
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
                    "Транспорт (перемещ), л": row.Transportation,
                    "Хранение, л": row.Storage,
                    "Ст-ть Денег": row.Money_cost,
                    "Доп% денег": row.Additional_money_percent,
                    'Оклейка остатков': row.Okleyka
                })
            
            return result
        except Exception as e:
            print(f"Ошибка в _get_fees_data: {e}")  # Добавьте логирование
            self.show_error_message(f"Ошибка получения данных тарифов: {str(e)}")
            return []

    def _get_ecofee_data(self, tnved_code=None, year=None):
        """Получение данных об экосборах с фильтрацией"""
        try:
            query = (
                db.query(
                    TNVED.code.label("ТНВЭД"),
                    Year.Year.label("Год"),
                    EcoFee_amount.ECO_amount.label("Эко_Ставка"),  # Изменено с "Эко Ставка" на "Эко_Ставка"
                    EcoFee_standard.ECO_standard.label("Эко_Норматив")  # Изменено с "Эко Норматив" на "Эко_Норматив"
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
                    "Эко Ставка": row.Эко_Ставка,  # Используем правильные имена атрибутов
                    "Эко Норматив": row.Эко_Норматив
                })
            
            return result
        except Exception as e:
            self.show_error_message(f"Ошибка получения данных экосборов: {str(e)}")
            return []

    def _get_customs_rates_data(self, tnved_code=None):
        """Получение данных о пошлинах с фильтрацией"""
        try:
            query = db.query(
                TNVED.code.label("ТНВЭД"),
                Customs_Rate.Cust_rate.label("Пошлина")
            ).join(Customs_Rate.tnved)
            
            if tnved_code:
                query = query.filter(TNVED.code == tnved_code)
            
            customs_data = query.order_by(TNVED.code).all()
            
            result = []
            for row in customs_data:
                result.append({
                    "ТНВЭД": row.ТНВЭД,
                    "Пошлина": row.Пошлина
                })
            
            return result
        except Exception as e:
            self.show_error_message(f"Ошибка получения данных пошлин: {str(e)}")
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
                
                if value is None or (hasattr(value, 'is_nan') and value.is_nan()):
                    display_value = ""
                elif col_name in ["Комиссия банка", "Ст-ть Денег", "Доп% денег"]:
                    # Вариант 1: Если в БД 0.0108 → умножаем на 100
                    display_value = f"{float(value) * 100:.2f}%".replace(".", ",")
                    
                    # Вариант 2: Если в БД уже 1.08 → просто добавляем %
                    # display_value = f"{float(value):.2f}%".replace(".", ",")
                elif col_name == "Год":
                    display_value = str(int(value)) if value is not None else ""
                elif col_name == "Месяц":
                    display_value = str(int(value)) if value is not None else ""
                else:
                    display_value = f"{float(value):,.2f}".replace(",", " ").replace(".", ",") if value is not None else ""
                
                item = QTableWidgetItem(display_value)
                self.table.setItem(row_idx, col_idx, item)
        
        self.table.resizeColumnsToContents()

    def _display_ecofee_data(self, data):
        """Отображение данных об экосборах (ставки и нормативы)"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if not data:
            self.show_message("Нет данных об экосборах для отображения")
            return

        # Устанавливаем заголовки
        headers = ["ТНВЭД", "Год", "Эко Ставка", "Эко Норматив"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            # ТНВЭД
            tnved_item = QTableWidgetItem(str(row_data.get("ТНВЭД", "")))
            self.table.setItem(row_idx, 0, tnved_item)
            
            # Год
            year_item = QTableWidgetItem(str(row_data.get("Год", "")))
            self.table.setItem(row_idx, 1, year_item)
            
            # Эко Ставка (число, форматируем с 2 знаками)
            eco_amount = row_data.get("Эко Ставка")
            eco_amount_display = f"{float(eco_amount):,.2f}".replace(",", " ").replace(".", ",") if eco_amount is not None else ""
            amount_item = QTableWidgetItem(eco_amount_display)
            self.table.setItem(row_idx, 2, amount_item)
            
            # Эко Норматив (процент, умножаем на 100)
            eco_standard = row_data.get("Эко Норматив")
            if eco_standard is not None:
                # Проверяем, нужно ли умножать на 100 (если значение < 1)
                eco_standard_val = float(eco_standard)
                if eco_standard_val < 1:
                    eco_standard_display = f"{eco_standard_val * 100:.2f}%".replace(".", ",")
                else:
                    eco_standard_display = f"{eco_standard_val:.2f}%".replace(".", ",")
            else:
                eco_standard_display = ""
            standard_item = QTableWidgetItem(eco_standard_display)
            self.table.setItem(row_idx, 3, standard_item)
        
        self.table.resizeColumnsToContents()
                
    def _display_customs_rates_data(self, data):
        """Отображение данных о пошлинах"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if not data:
            self.show_message("Нет данных о пошлинах для отображения")
            return
        
        headers = ["ТНВЭД", "Пошлина"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            # ТНВЭД
            item_tnved = QTableWidgetItem(str(row_data["ТНВЭД"]))
            self.table.setItem(row_idx, 0, item_tnved)
            
            # Пошлина (умножаем на 100 для отображения в процентах)
            rate = row_data["Пошлина"]
            if rate is not None:
                display_rate = f"{float(rate)*100:.2f}%".replace(".", ",")
            else:
                display_rate = ""
                
            item_rate = QTableWidgetItem(display_rate)
            self.table.setItem(row_idx, 1, item_rate)
        
        self.table.resizeColumnsToContents()
                
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
        months = list(range(1, 13))
        self._fill_combobox(self.ui.line_Mnth, months)
    
    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        combobox.clear()
        combobox.addItem('-')
        if items:
            if all(isinstance(item, (int, float)) for item in items):
                sorted_items = sorted(items)
            else:
                sorted_items = sorted(items)

            combobox.addItems([str(item) for item in sorted_items])

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


