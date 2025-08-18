import os
import pandas as pd
from sqlalchemy import func
import datetime
from sqlalchemy.exc import SQLAlchemyError
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QTableWidget, QMenu, 
                              QTableWidgetItem, QWidget, QApplication)
from PySide6.QtCore import Qt
from functools import lru_cache

from wind.pages.add_costs_suppl_ui import Ui_Form
from config import AddCosts_File
from models import Supplier, SupplScheme, AddSupplCost
from db import db


class AddSupplCostsPage(QWidget):
    def __init__(self):
        super(AddSupplCostsPage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

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
        self.ui.line_Suppl1.currentTextChanged.connect(self.fill_in_suppl2_list)
        self.ui.line_Suppl1.currentTextChanged.connect(self.fill_in_suppl_rep_list)
        self.ui.line_Suppl1.currentTextChanged.connect(self.fill_in_order_list)
        self.ui.line_Suppl1.currentTextChanged.connect(self.fill_in_shipp_list)
        
        self.ui.line_Suppl2.currentTextChanged.connect(self.fill_in_suppl_rep_list)
        self.ui.line_Suppl2.currentTextChanged.connect(self.fill_in_order_list)
        self.ui.line_Suppl2.currentTextChanged.connect(self.fill_in_shipp_list)
        
        self.ui.line_Order.currentTextChanged.connect(self.fill_in_shipp_list)
        
        self.ui.btn_open_file.clicked.connect(self.get_file)
        self.ui.btn_upload_file.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_AddSupplCosts)
        
    def get_file(self):
        """Выбор файла через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с дополнительными расходами')
        if file_path:
            self.ui.label_Supplier_File.setText(file_path)

    def upload_data(self):
        """Загрузка данных дополнительных расходов в базу данных"""
        try:
            # Закрываем предыдущие сессии, если они есть
            if db.is_active:
                db.close()
            
            # Определяем путь к файлу
            file_path = self.ui.label_Supplier_File.text()
            if not file_path or file_path == 'Выбери файл или нажми Upload, файл будет взят из основной папки':
                file_path = AddCosts_File

            try:
                # Основные операции выполняем в отдельной сессии
                db.begin()
                
                try:
                    data = self.read_add_suppl_file(file_path)
                    self.save_AddSupplCost(data)
                    db.commit()
                    
                    # Обновляем интерфейс
                    self.refresh_all_comboboxes()
                    self.show_message('Данные дополнительных расходов успешно загружены!')
                    
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

    def read_add_suppl_file(self, file_path):
        """Чтение данных из Excel с обработкой значений"""
        try:
            # Чтение файла с дополнительными расходами
            df = pd.read_excel(file_path, sheet_name="ДопРасходы")
            
            # Обработка дат - просто преобразуем в datetime без замены 2999 года
            df["Дата"] = pd.to_datetime(df["Дата"], dayfirst=True, errors='coerce')
            
            # Заполнение числовых колонок нулями
            numeric_cols = ["Погрузка/Выгрузка", "Агентские", "Транспорт м.н.", 
                        "Транспорт лок.", "Доп услуги", "Комиссия платежному агенту"]
            
            # Исправление: проверяем наличие колонок перед заполнением
            existing_numeric_cols = [col for col in numeric_cols if col in df.columns]
            df[existing_numeric_cols] = df[existing_numeric_cols].fillna(0).astype(float)
            
            # Создание merge_id для проверки уникальности
            def create_merge_id(row):
                if row["Документ"] != "-":
                    date_str = row['Дата'].strftime('%d.%m.%Y') if pd.notnull(row['Дата']) else 'NULL'
                    return f"{row['Документ']}_{date_str}"
                else:
                    return f"{row['Supplier 1']}_{row['Supplier 2']}_{row['Order N']}_{row['Shipment #']}"
            
            df["merge_id"] = df.apply(create_merge_id, axis=1)
            
            # Переименование колонок для соответствия с БД
            column_map = {
                "Документ": "Document",
                "Дата": "Date",
                "Контрагент.Код": "Supplier_id",
                "Контрагент": "Supplier_Name_report",
                "Supplier 1": "Supplier1",
                "Supplier 2": "Supplier2",
                "Order N": "Order",
                "Shipment #": "Shipment",
                "Container": "Container",
                "Suppl Inv N": "Suppl_Inv_N",
                "Склад": "Storage",
                "Имп/Лок": "Imp_Loc",
                "Перемещ": "Movement",
                "Объем": "Volume",
                "Сумма 1го Поставщика": "First_Invoice_Amount",
                "Сумма 1С": "Final_Invoice_Amount",
                "Номер ГТД": "GTD_doc",
                "Статус": "Status",
                "Валюта": "Currency",
                "Курс оплаты": "Payment_FX",
                "Погрузка/Выгрузка": "Load_Unload",
                "Агентские": "Agency",
                "Транспорт м.н.": "Transport_mn",
                "Транспорт лок.": "Transport_loc",
                "Доп услуги": "Add_Services",
                "Комиссия платежному агенту": "Commission",
                "Комментарий": "Comment",
                "Ст-ть трансп ВЭД": "Transp_VED",
                "курс для транспорта": "Transp_FX",
                "Тамож. дата": "Customs_date",
                "Дата прихода": "Date_arrival",
                "м/н перевозчик": "Carrier",
                "Счета": "Carrier_orders",
                "merge_id": "merge_id"
            }
            
            # Переименовываем только существующие колонки
            df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
            
            # Преобразование дат
            date_cols = ["Date", "Customs_date", "Date_arrival"]
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
            
            # Замена NaN на None для корректной работы с БД
            df = df.where(pd.notnull(df), None)
            
            return df.to_dict('records')
            
        except Exception as e:
            self.show_error_message(f"Ошибка чтения файла дополнительных расходов: {str(e)}")
            return []

    def save_AddSupplCost(self, data):
        """Сохранение данных в таблицу AddSupplCost с удалением отсутствующих в Excel записей"""
        if not data:
            return

        try:
            # Закрываем предыдущую сессию, если она активна
            if db.is_active:
                db.close()

            # Начинаем новую сессию
            db.begin()

            try:
                # Получаем все существующие записи из БД
                existing_records = {r.merge_id: r for r in db.query(AddSupplCost).all()}
                
                # Собираем merge_id из загружаемых данных
                incoming_merge_ids = {row['merge_id'] for row in data if row.get('merge_id')}
                
                # Определяем записи для удаления (есть в БД, но нет в новых данных)
                to_delete_ids = [
                    record.id 
                    for merge_id, record in existing_records.items() 
                    if merge_id not in incoming_merge_ids
                    and merge_id and not merge_id.startswith('None_')
                ]
                
                # Определяем записи для вставки и обновления
                to_insert = []
                to_update = []
                
                for row in data:
                    if not row.get('merge_id'):
                        continue
                        
                    row_data = {k: v for k, v in row.items() if k in AddSupplCost.__table__.columns.keys()}
                    
                    if row['merge_id'] in existing_records:
                        row_data['id'] = existing_records[row['merge_id']].id
                        to_update.append(row_data)
                    else:
                        to_insert.append(row_data)
                
                # Удаляем отсутствующие записи
                if to_delete_ids:
                    delete_count = db.query(AddSupplCost).filter(AddSupplCost.id.in_(to_delete_ids)).delete(
                        synchronize_session=False
                    )
                    print(f"Удалено {delete_count} устаревших записей")
                
                # Вставляем новые записи
                if to_insert:
                    db.bulk_insert_mappings(AddSupplCost, to_insert)
                    print(f"Добавлено {len(to_insert)} новых записей")
                
                # Обновляем существующие записи
                if to_update:
                    db.bulk_update_mappings(AddSupplCost, to_update)
                    print(f"Обновлено {len(to_update)} записей")
                
                db.commit()
                
            except Exception as e:
                db.rollback()
                raise Exception(f"Ошибка при сохранении данных: {str(e)}")
                
        except SQLAlchemyError as e:
            if db.is_active:
                db.rollback()
            raise Exception(f"Ошибка базы данных: {str(e)}")
        finally:
            if db.is_active:
                db.close()

    @lru_cache(maxsize=32)
    def _get_unique_values(self, column, 
                        filter_column=None, filter_value=None,
                        filter_column2=None, filter_value2=None,
                        filter_column3=None, filter_value3=None):
        """Получение уникальных значений с фильтрацией (до 3 фильтров)"""
        try:
            query = db.query(column)
            
            # Применяем первый фильтр если он задан
            if filter_column is not None and filter_value not in (None, '-', ''):
                query = query.filter(filter_column == filter_value)
                
            # Применяем второй фильтр если он задан
            if filter_column2 is not None and filter_value2 not in (None, '-', ''):
                query = query.filter(filter_column2 == filter_value2)
                
            # Применяем третий фильтр если он задан
            if filter_column3 is not None and filter_value3 not in (None, '-', ''):
                query = query.filter(filter_column3 == filter_value3)
            
            # Получаем и сортируем уникальные значения
            result = sorted(v[0] for v in query.distinct().all() if v[0] not in (None, '-', ''))
            return result
            
        except Exception as e:
            self.show_error_message(f"Ошибка при получении уникальных значений: {str(e)}")
            return []
        finally:
            db.close()

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков"""
        self._get_unique_values.cache_clear()
        self.fill_in_suppl1_list()
        self.fill_in_suppl2_list()
        self.fill_in_suppl_rep_list()
        self.fill_in_order_list()
        self.fill_in_shipp_list()
        
        # Устанавливаем "-" в поле Container
        self.ui.line_Container.setText("-")

    def fill_in_suppl1_list(self):
        """Заполнение списка Supplier1"""
        suppliers = self._get_unique_values(SupplScheme.Supplier1)
        self._fill_combobox(self.ui.line_Suppl1, suppliers)

    def fill_in_suppl2_list(self):
        """Заполняет список Supplier2 только для выбранного Supplier1"""
        suppl1 = self.ui.line_Suppl1.currentText()
        
        if suppl1 == '-':
            # Если Supplier1 не выбран, показываем все Supplier2
            suppliers = self._get_unique_values(SupplScheme.Supplier2)
        else:
            # Фильтруем Supplier2 только для выбранного Supplier1
            suppliers = self._get_unique_values(
                SupplScheme.Supplier2,
                filter_column=SupplScheme.Supplier1,
                filter_value=suppl1
            )
        
        self._fill_combobox(self.ui.line_Suppl2, suppliers)

    def fill_in_suppl_rep_list(self):
        """Заполняет список Supplier_Name_report для выбранных Supplier1 и Supplier2"""
        suppl1 = self.ui.line_Suppl1.currentText()
        suppl2 = self.ui.line_Suppl2.currentText()
        
        if suppl1 == '-' and suppl2 == '-':
            # Если ничего не выбрано, показываем все Supplier_Name_report
            suppliers = self._get_unique_values(SupplScheme.Supplier_Name_report)
        elif suppl2 == '-':
            # Если выбран только Supplier1
            suppliers = self._get_unique_values(
                SupplScheme.Supplier_Name_report,
                filter_column=SupplScheme.Supplier1,
                filter_value=suppl1
            )
        else:
            # Если выбраны и Supplier1 и Supplier2
            suppliers = self._get_unique_values(
                SupplScheme.Supplier_Name_report,
                filter_column=SupplScheme.Supplier1,
                filter_value=suppl1,
                filter_column2=SupplScheme.Supplier2,
                filter_value2=suppl2
            )
        
        self._fill_combobox(self.ui.line_SupplRep, suppliers)

    def fill_in_order_list(self):
        """Заполняет список Order для выбранных Supplier1 и Supplier2"""
        suppl1 = self.ui.line_Suppl1.currentText()
        suppl2 = self.ui.line_Suppl2.currentText()
        
        if suppl1 == '-' and suppl2 == '-':
            # Если ничего не выбрано, показываем все Order
            orders = self._get_unique_values(AddSupplCost.Order)
        elif suppl2 == '-':
            # Если выбран только Supplier1
            orders = self._get_unique_values(
                AddSupplCost.Order,
                filter_column=AddSupplCost.Supplier1,
                filter_value=suppl1
            )
        else:
            # Если выбраны и Supplier1 и Supplier2
            orders = self._get_unique_values(
                AddSupplCost.Order,
                filter_column=AddSupplCost.Supplier1,
                filter_value=suppl1,
                filter_column2=AddSupplCost.Supplier2,
                filter_value2=suppl2
            )
        
        self._fill_combobox(self.ui.line_Order, orders)

    def fill_in_shipp_list(self):
        """Заполняет список Shipment для выбранных Supplier1, Supplier2 и Order"""
        suppl1 = self.ui.line_Suppl1.currentText()
        suppl2 = self.ui.line_Suppl2.currentText()
        order = self.ui.line_Order.currentText()
        
        if order == '-':
            # Если Order не выбран, показываем все Shipment с учетом фильтров Supplier1/2
            if suppl1 == '-' and suppl2 == '-':
                shipments = self._get_unique_values(AddSupplCost.Shipment)
            elif suppl2 == '-':
                shipments = self._get_unique_values(
                    AddSupplCost.Shipment,
                    filter_column=AddSupplCost.Supplier1,
                    filter_value=suppl1
                )
            else:
                shipments = self._get_unique_values(
                    AddSupplCost.Shipment,
                    filter_column=AddSupplCost.Supplier1,
                    filter_value=suppl1,
                    filter_column2=AddSupplCost.Supplier2,
                    filter_value2=suppl2
                )
        else:
            # Если Order выбран, применяем все три фильтра
            if suppl1 == '-' and suppl2 == '-':
                shipments = self._get_unique_values(
                    AddSupplCost.Shipment,
                    filter_column=AddSupplCost.Order,
                    filter_value=order
                )
            elif suppl2 == '-':
                shipments = self._get_unique_values(
                    AddSupplCost.Shipment,
                    filter_column=AddSupplCost.Supplier1,
                    filter_value=suppl1,
                    filter_column2=AddSupplCost.Order,
                    filter_value2=order
                )
            else:
                shipments = self._get_unique_values(
                    AddSupplCost.Shipment,
                    filter_column=AddSupplCost.Supplier1,
                    filter_value=suppl1,
                    filter_column2=AddSupplCost.Supplier2,
                    filter_value2=suppl2,
                    filter_column3=AddSupplCost.Order,
                    filter_value3=order
                )
        
        self._fill_combobox(self.ui.line_Shipp, shipments)
    
    def _fill_combobox(self, combobox, items):
        """Универсальное заполнение комбобокса"""
        current_text = combobox.currentText()
        combobox.clear()
        combobox.addItem('-')
        if items:
            combobox.addItems(sorted(items))
        
        # Восстанавливаем предыдущее значение, если оно есть в списке
        if current_text in [combobox.itemText(i) for i in range(combobox.count())]:
            combobox.setCurrentText(current_text)

    def get_AddSupplCosts_from_db(self):
        """Получение данных из таблицы AddSupplCost с фильтрацией"""
        try:
            # Базовый запрос с JOIN к SupplScheme и Supplier
            query = db.query(AddSupplCost)
        
            # Применяем фильтры из выпадающих списков
            suppl1 = self.ui.line_Suppl1.currentText()
            suppl2 = self.ui.line_Suppl2.currentText()
            suppl_rep = self.ui.line_SupplRep.currentText()
            order = self.ui.line_Order.currentText()
            shipp = self.ui.line_Shipp.currentText()
            container = self.ui.line_Container.text()
            
            if suppl1 != '-':
                query = query.filter(AddSupplCost.Supplier1 == suppl1)
            if suppl2 != '-':
                query = query.filter(AddSupplCost.Supplier2 == suppl2)
            if order != '-':
                query = query.filter(AddSupplCost.Order == order)
            if shipp != '-':
                query = query.filter(AddSupplCost.Shipment == shipp)
            if container != '-':
                query = query.filter(AddSupplCost.Container == container)
            
            # Для фильтрации по Supplier_Name_report делаем отдельный подзапрос
            if suppl_rep != '-':
                suppl_ids = db.query(Supplier.id).join(SupplScheme).filter(
                    SupplScheme.Supplier_Name_report == suppl_rep
                ).distinct()
                query = query.filter(AddSupplCost.Supplier_id.in_(suppl_ids))
            
            # Получаем данные в DataFrame
            df = pd.read_sql(query.statement, db.bind)
            
            # Переименовываем колонки для отображения как в Excel
            column_map = {
                "Document": "Документ",
                "Date": "Дата",
                "Supplier_id": "Контрагент.Код",
                "Supplier_Name_report": "Контрагент",
                "Supplier1": "Supplier 1",
                "Supplier2": "Supplier 2",
                "Order": "Order N",
                "Shipment": "Shipment #",
                "Container": "Container",
                "Suppl_Inv_N": "Suppl Inv N",
                "Storage": "Склад",
                "Imp_Loc": "Имп/Лок",
                "Movement": "Перемещ",
                "Volume": "Объем",
                "First_Invoice_Amount": "Сумма 1го Поставщика",
                "Final_Invoice_Amount": "Сумма 1С",
                "GTD_doc": "Номер ГТД",
                "Status": "Статус",
                "Currency": "Валюта",
                "Payment_FX": "Курс оплаты",
                "Load_Unload": "Погрузка/Выгрузка",
                "Agency": "Агентские",
                "Transport_mn": "Транспорт м.н.",
                "Transport_loc": "Транспорт лок.",
                "Add_Services": "Доп услуги",
                "Commission": "Комиссия платежному агенту",
                "Comment": "Комментарий",
                "Transp_VED": "Ст-ть трансп ВЭД",
                "Transp_FX": "курс для транспорта",
                "Customs_date": "Тамож. дата",
                "Date_arrival": "Дата прихода",
                "Carrier": "м/н перевозчик",
                "Carrier_orders": "Счета"
            }
            
            df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
            
            return df.where(pd.notnull(df), None)
            
        except Exception as e:
            self.show_error_message(f"Ошибка получения данных из БД: {str(e)}")
            return pd.DataFrame()
        finally:
            db.close()

    def find_AddSupplCosts(self):
        """Поиск и отображение данных в таблице"""
        self.table.clearContents()
        self.table.setRowCount(0)

        add_suppl_df = self.get_AddSupplCosts_from_db()

        if not add_suppl_df.empty:
            self._display_data(add_suppl_df)
        else:
            self.show_error_message("Нет данных для отображения")

    def _display_data(self, df):
        """Отображение данных с русским форматированием чисел"""
        self.table.clearContents()
        self.table.setRowCount(0)
        
        if df.empty:
            self.show_message('Данные не найдены')
            return
        
        # Отладочная информация
        print(f"Всего строк: {len(df)}")
        print(f"Уникальных строк: {len(df.drop_duplicates())}")
        
        # Создаем копию DataFrame для форматирования
        display_df = df.copy()
        
        # Определяем числовые колонки и их точность
        numeric_columns = {
            1: ['Объем'],  # 1 знак после запятой
            2: ['Сумма 1С', 'Агентские', 'Транспорт м.н.', 
                'Транспорт лок.', 'Доп услуги', 'Комиссия платежному агенту',
                'Ст-ть трансп ВЭД'],  # 2 знака
            4: ['курс для транспорта', 'Курс оплаты']  # 4 знака
        }
        
        # Форматируем числовые колонки
        for decimals, cols in numeric_columns.items():
            for col in cols:
                if col in display_df.columns:
                    display_df[col] = display_df[col].apply(
                        lambda x: (
                            f"{float(x):,.{decimals}f}".replace(',', ' ').replace('.', ',')
                            if pd.notnull(x) 
                            else f"0{' ' if decimals > 0 else ''},{'0'*decimals}"
                        )
                    )
        
        # Форматируем даты
        date_columns = ['Дата', 'Тамож. дата', 'Дата прихода']
        for col in date_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(
                    lambda x: x.strftime('%d.%m.%Y') 
                    if not pd.isna(x) and x is not None 
                    else ''
                )
        
        # Настраиваем таблицу
        self.table.setColumnCount(len(display_df.columns))
        self.table.setRowCount(len(display_df))
        self.table.setHorizontalHeaderLabels(display_df.columns)
        
        # Заполняем таблицу
        all_numeric_cols = [col for cols in numeric_columns.values() for col in cols if col in display_df.columns]
        
        for row_idx, row in display_df.iterrows():
            for col_idx, (col_name, value) in enumerate(row.items()):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                
                # Выравнивание чисел по правому краю
                if col_name in all_numeric_cols:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                self.table.setItem(row_idx, col_idx, item)
        
        # Автонастройка ширины столбцов
        self.table.resizeColumnsToContents()
        
        # Дополнительная проверка
        if len(df) != len(df.drop_duplicates()):
            print("ВНИМАНИЕ: В данных обнаружены дубликаты!")

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
        
        