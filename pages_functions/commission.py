import os
import pandas as pd
import numpy as np
from sqlalchemy import or_, and_, func
from PySide6.QtWidgets import (QMessageBox, QHeaderView, QTableWidget, QMenu, 
                               QTableWidgetItem, QWidget, QApplication, QDialog)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QShortcut, QKeySequence

from datetime import datetime, date, timedelta

from wind.pages.commission_ui import Ui_Form
from wind.pages.commission_create_form_ui import Ui_Form as CreateFormUi
from config import AddCosts_File
from models import Commission, Customer, Materials, Product_Names, Product_Group
from db import db


class CommissionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self._updating_table = False
        self._original_values = {}
        self._pending_changes = {}
        
        # Устанавливаем даты по умолчанию
        today = datetime.now()
        # self.ui.line_date_start.setDate(QDate(today.year, 1, 1))
        self.ui.line_date_start.setDate(QDate(2022, 1, 1))
        self.ui.line_date_end.setDate(QDate(today.year, 12, 31))
        
        self._setup_ui()
        self._setup_connections()
        self.refresh_all_comboboxes()

    def _setup_ui(self):
        """Настройка интерфейса таблицы"""
        self.table = self.ui.table
        
        # ВОЗВРАЩАЕМ ВЫДЕЛЕНИЕ ОТДЕЛЬНЫХ ЯЧЕЕК
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        # НО РАЗРЕШАЕМ МНОЖЕСТВЕННОЕ ВЫДЕЛЕНИЕ
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        
        # Базовые настройки таблицы
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.TextElideMode.ElideRight)
        
        # Устанавливаем высоту строки 20px
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.verticalHeader().setMinimumSectionSize(20)
        
        # Контекстное меню
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self._updating_table = False
        
        self.table.setTabKeyNavigation(True)
        self.table.setCornerButtonEnabled(False)
        
        # Добавляем горячие клавиши
        copy_shortcut = QShortcut(QKeySequence.Copy, self.table)
        copy_shortcut.activated.connect(self.copy_cell_content)

    def show_context_menu(self, position):
        """Показ контекстного меню"""
        menu = QMenu()
        
        copy_action = menu.addAction("Копировать выделенное")
        copy_row_action = menu.addAction("Копировать строку")
        copy_all_action = menu.addAction("Копировать всю таблицу")
        menu.addSeparator()
        add_row_action = menu.addAction("Добавить строку")
        menu.addSeparator()
        apply_action = menu.addAction("Применить изменения")
        revert_action = menu.addAction("Отменить изменения")
        
        copy_action.triggered.connect(self.copy_cell_content)
        copy_row_action.triggered.connect(self.copy_current_row)
        copy_all_action.triggered.connect(self.copy_whole_table)
        add_row_action.triggered.connect(self.add_new_row)
        apply_action.triggered.connect(self.apply_pending_changes)
        revert_action.triggered.connect(self.revert_changes)
        
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def add_new_row(self):
        """Добавление новой строки через форму"""
        form = CommissionCreateForm(self)
        form.exec_()
        # После закрытия формы обновляем данные
        self.find_commission()

    def copy_current_row(self):
        """Копирование всей текущей строки"""
        current_row = self.table.currentRow()
        if current_row == -1:
            return
        
        row_data = []
        for col in range(self.table.columnCount()):
            item = self.table.item(current_row, col)
            if item:
                row_data.append(item.text())
            else:
                row_data.append("")
        
        text = "\t".join(row_data)
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def copy_whole_table(self):
        """Копирование всей таблицы"""
        text = ""
        
        # Заголовки
        headers = []
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col)
            if header:
                headers.append(header.text())
            else:
                headers.append("")
        text += "\t".join(headers) + "\n"
        
        # Данные
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            text += "\t".join(row_data) + "\n"
        
        clipboard = QApplication.clipboard()
        clipboard.setText(text.strip())

    def _setup_connections(self):
        """Настройка сигналов и слотов"""
        self.table.itemChanged.connect(self.on_item_changed)
        self.ui.btn_refresh.clicked.connect(self.upload_data)
        self.ui.btn_find.clicked.connect(self.find_commission)

    def copy_cell_content(self):
        """Копирование содержимого выделенных ячеек с поддержкой строк"""
        selected_indexes = self.table.selectedIndexes()
        
        if not selected_indexes:
            return
        
        # Проверяем, выделены ли целые строки
        rows = set()
        cols = set()
        for index in selected_indexes:
            rows.add(index.row())
            cols.add(index.column())
        
        # Если выделены все колонки в строках - копируем как строки
        if len(cols) == self.table.columnCount():
            # Копируем целые строки
            text = ""
            for row in sorted(rows):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                text += "\t".join(row_data) + "\n"
        else:
            # Копируем отдельные ячейки
            rows_dict = {}
            for index in selected_indexes:
                row = index.row()
                col = index.column()
                if row not in rows_dict:
                    rows_dict[row] = {}
                rows_dict[row][col] = index.data(Qt.DisplayRole) or ""
            
            text = ""
            for row in sorted(rows_dict.keys()):
                cols_dict = rows_dict[row]
                row_text = "\t".join([cols_dict[col] for col in sorted(cols_dict.keys())])
                text += row_text + "\n"
        
        # Копируем в буфер обмена
        clipboard = QApplication.clipboard()
        clipboard.setText(text.strip())

    def on_item_changed(self, item):
        """Обработчик изменения данных в таблице"""
        if self._updating_table:
            return
        
        try:
            row = item.row()
            column = item.column()
            header = self.table.horizontalHeaderItem(column).text()
            
            # Получаем ID записи из скрытых данных
            commission_id_item = self.table.item(row, 0)  # Предполагаем, что ID в первой колонке
            if not commission_id_item:
                return
                
            commission_id = int(commission_id_item.text())
            new_value = item.text()
            
            # Сохраняем изменение
            if commission_id not in self._pending_changes:
                self._pending_changes[commission_id] = {}
            
            self._pending_changes[commission_id][header] = new_value
            
        except Exception as e:
            self.show_error_message(f"Ошибка: {str(e)}")

    def _get_column_index(self, column_name):
        """Получение индекса колонки по имени"""
        for col in range(self.table.columnCount()):
            header_text = self.table.horizontalHeaderItem(col).text()
            if header_text == column_name:
                return col
        return -1

    def apply_pending_changes(self):
        """Применение всех ожидающих изменений"""
        if not self._pending_changes:
            self.show_message("Нет изменений для применения")
            return
            
        try:
            header_mapping = {
                'Контрагент.Код': 'Customer_id',
                'Контрагент': 'customer_name',
                'Дата начала': 'Start_date',
                'Дата окончания': 'End_date',
                'Комм %': 'Comm_perc',
                'Комм Руб': 'Comm_rub',
                'Ст-ть ком-ии, %': 'Comm_Cost_perc',
                'Ст-ть ком-ии, Руб': 'Comm_Cost_rub',
                'Артикул': 'Material_id',
                'Product name': 'Product_group_id',
                'Документ': 'Document',
                'Дата': 'Date',
                'Счет': 'Bill',
                'Дата счета': 'Bill_date',
                'л от': 'Litres_from',
                'л до': 'Litres_to',
                'Грузополучатель.Код': 'Recipient_code',
                'Грузополучатель': 'Recipient',
                'Код дилера': 'Hyundai_code',
                'Комментарий': 'Comment'
            }
            
            for commission_id, changes in self._pending_changes.items():
                # Находим запись в БД
                commission = db.query(Commission).filter(Commission.id == commission_id).first()
                
                if not commission:
                    continue
                
                # Применяем изменения
                for russian_header, new_value in changes.items():
                    english_field = header_mapping.get(russian_header)
                    
                    if not english_field:
                        continue
                    
                    # Обработка специальных полей
                    if english_field == 'Material_id':
                        # Если меняется артикул, ищем материал
                        if new_value and new_value != '-':
                            material = db.query(Materials).filter(
                                Materials.Article == new_value, 
                                Materials.Status == 'активный'
                            ).first()
                            if material:
                                commission.Material_id = material.Code
                                # Если есть артикул, то Product_group_id должен быть None
                                commission.Product_group_id = None
                        else:
                            commission.Material_id = None
                    
                    elif english_field == 'Product_group_id':
                        # Если меняется Product name
                        if new_value and new_value != '-':
                            product_group = db.query(Product_Group).filter(
                                Product_Group.Product_name == new_value
                            ).first()
                            if product_group:
                                commission.Product_group_id = product_group.id
                                # Если есть Product name, то Material_id должен быть None
                                commission.Material_id = None
                        else:
                            commission.Product_group_id = None
                    
                    elif english_field == 'Customer_id':
                        # Поиск клиента по коду
                        customer = db.query(Customer).filter(Customer.id == new_value).first()
                        if customer:
                            commission.Customer_id = customer.id
                    
                    elif english_field in ['Start_date', 'End_date', 'Date', 'Bill_date']:
                        try:
                            date_value = datetime.strptime(new_value, '%Y-%m-%d').date() if new_value else None
                            setattr(commission, english_field, date_value)
                        except ValueError:
                            continue
                    
                    elif english_field in ['Comm_perc', 'Comm_rub', 'Comm_Cost_perc', 'Comm_Cost_rub', 'Litres_from', 'Litres_to']:
                        try:
                            float_value = float(new_value.replace(',', '.')) if new_value else None
                            setattr(commission, english_field, float_value)
                        except ValueError:
                            continue
                    
                    else:
                        setattr(commission, english_field, new_value)
            
            db.commit()
            self._pending_changes.clear()
            self.show_message("Изменения успешно применены")
            self.find_commission()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка применения изменений: {str(e)}")

    def revert_changes(self):
        """Отмена изменений"""
        db.rollback()
        self.find_commission()
        self._pending_changes.clear()
        self.show_message("Изменения отменены")

    def delete_commission_record(self, commission_id: int):
        """
        Удаляет запись комиссии с подтверждением пользователя
        """
        # Запрос подтверждения у пользователя
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение удаления")
        msg_box.setText("Вы уверены, что хотите удалить строку?")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        result = msg_box.exec_()
        
        if result == QMessageBox.Yes:  # Если пользователь нажал "Да"
            try:
                # Находим запись для удаления
                commission = db.query(Commission).filter(Commission.id == commission_id).first()
                
                if commission:
                    db.delete(commission)
                    db.commit()
                    self.show_message("Запись успешно удалена")
                    self.find_commission()  # Обновляем таблицу
                else:
                    self.show_error_message("Запись не найдена")
                    
            except Exception as e:
                db.rollback()
                self.show_error_message(f"Не удалось удалить запись: {str(e)}")

    def refresh_all_comboboxes(self):
        """Обновление всех выпадающих списков только данными из Commission"""
        try:
            # Заполнение списка контрагентов из Commission
            customer_codes = db.query(Commission.Customer_id).distinct().all()
            customer_codes = [code[0] for code in customer_codes if code[0]]
            
            customers = []
            for code in customer_codes:
                customer = db.query(Customer).filter(Customer.id == code).first()
                if customer and customer.Customer_name:
                    customers.append(f"{customer.Customer_name} - {customer.id}")
            
            customers = sorted(customers)
            self._fill_combobox(self.ui.line_customer, ["-"] + customers)
            
            # Заполнение статусов
            statuses = ["-", "активные", "не активные"]
            self.ui.line_status.clear()
            self.ui.line_status.addItems(statuses)
            
            # Заполнение продуктов из Commission (через Materials)
            material_ids = db.query(Commission.Material_id).distinct().all()
            material_ids = [id[0] for id in material_ids if id[0]]
            
            products = set()
            for material_id in material_ids:
                material = db.query(Materials).filter(Materials.Code == material_id).first()
                if material and material.product_name and material.product_name.Product_name:
                    products.add(material.product_name.Product_name)
            
            self._fill_combobox(self.ui.line_product, ["-"] + sorted(products))
            
            # Заполнение product groups из Commission
            group_ids = db.query(Commission.Product_group_id).distinct().all()
            group_ids = [id[0] for id in group_ids if id[0]]
            
            prod_names = set()
            for group_id in group_ids:
                group = db.query(Product_Group).filter(Product_Group.id == group_id).first()
                if group and group.Product_name:
                    prod_names.add(group.Product_name)
            
            self._fill_combobox(self.ui.line_prod_name, ["-"] + sorted(prod_names))
            
        except Exception as e:
            self.show_error_message(f"Ошибка обновления списков: {str(e)}")

    def _fill_combobox(self, combobox, items):
        """Заполнение комбобокса"""
        combobox.clear()
        combobox.addItems(items)

    def upload_data(self):
        """Обновление данных из Excel файла"""
        try:
            file_path = AddCosts_File
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {file_path} не найден")
            
            # Чтение Excel файла
            dtype_comm = {
                "Артикул": str, 
                "Комм %": float, 
                "Комм Руб": float, 
                "Ст-ть ком-ии, %": float, 
                "Ст-ть ком-ии, Руб": float, 
                "л от": float, 
                "л до": float
            }
            
            df = pd.read_excel(file_path, sheet_name="Комиссии клиентам", dtype=dtype_comm)
            
            # Заполнение пустых значений
            df[["Артикул", "Продукт + упаковка", "Product name", "Документ", "Счет", "Грузополучатель.Код"]] = \
                df[["Артикул", "Продукт + упаковка", "Product name", "Документ", "Счет", "Грузополучатель.Код"]].fillna("-")
            
            df[["Комм %", "Комм Руб", "Ст-ть ком-ии, %", "Ст-ть ком-ии, Руб", "л от", "л до"]] = \
                df[["Комм %", "Комм Руб", "Ст-ть ком-ии, %", "Ст-ть ком-ии, Руб", "л от", "л до"]].fillna(0).astype(float)
            
            # Преобразование дат
            df["Дата начала"] = pd.to_datetime(df["Дата начала"], format="%d.%m.%Y", errors="coerce")
            df["Дата окончания"] = pd.to_datetime(df["Дата окончания"], format="%d.%m.%Y", errors="coerce")
            df["Дата"] = pd.to_datetime(df["Дата"], format="%d.%m.%Y", errors="coerce")
            df["Дата счета"] = pd.to_datetime(df["Дата счета"], format="%d.%m.%Y", errors="coerce")
            
            # Обработка каждой строки из Excel
            for _, row in df.iterrows():
                # Поиск клиента
                customer_code = row.get('Контрагент.Код', '-')
                customer = db.query(Customer).filter(Customer.id == customer_code).first()
                
                if not customer:
                    continue  # Пропускаем если клиент не найден
                
                # Определяем статус комиссии (активная или неактивная)
                is_active = True
                end_date = row['Дата окончания'].date() if pd.notna(row['Дата окончания']) else None
                document = row.get('Документ', '-')
                bill = row.get('Счет', '-')
                
                # Проверяем условия для неактивной комиссии (такая же логика как в _display_data)
                if (document != "-" or bill != "-" or 
                    (end_date and end_date < datetime.now().date())):
                    is_active = False
                
                # Обработка артикула и Product name
                materials_to_process = []
                product_group_id = None
                article = row.get('Артикул', '-')
                product_name_excel = row.get('Product name', '-')
                
                # ОСНОВНОЕ ИСПРАВЛЕНИЕ: обработка строк с артикулом "-"
                if article == '-':
                    # Если артикул "-", то Material_id должен быть NULL
                    materials_to_process = [None]  # Один "пустой" материал
                    
                    # Если есть Product name, ищем группу
                    if product_name_excel != '-':
                        product_group = db.query(Product_Group).filter(Product_Group.Product_name == product_name_excel).first()
                        if product_group:
                            product_group_id = product_group.id
                        else:
                            # Если группа не найдена, пропускаем строку
                            continue
                    else:
                        # Если нет ни артикула, ни Product name, пропускаем
                        continue
                        
                elif article != '-':
                    # Если есть нормальный артикул, ищем материалы
                    if is_active:
                        # Для активной комиссии - только активные материалы
                        materials = db.query(Materials).filter(
                            Materials.Article == article, 
                            Materials.Status == 'активный'
                        ).all()
                    else:
                        # Для неактивной комиссии - все материалы с этим артикулом
                        materials = db.query(Materials).filter(
                            Materials.Article == article
                        ).all()
                    
                    if materials:
                        materials_to_process = materials
                        # Product_group_id должен быть None при наличии артикула
                        product_group_id = None
                    else:
                        # Если материалы не найдены, пропускаем строку
                        continue
                else:
                    # Если нет ни артикула, ни Product name, пропускаем
                    continue
                
                # Обрабатываем каждый найденный материал (или группу)
                for material in materials_to_process:
                    # Создаем данные для комиссии
                    commission_data = {
                        'Customer_id': customer.id,
                        'Start_date': row['Дата начала'].date() if pd.notna(row['Дата начала']) else None,
                        'End_date': end_date,
                        'Comm_perc': float(row['Комм %']) if pd.notna(row['Комм %']) else None,
                        'Comm_rub': float(row['Комм Руб']) if pd.notna(row['Комм Руб']) else None,
                        'Comm_Cost_perc': float(row['Ст-ть ком-ии, %']) if pd.notna(row['Ст-ть ком-ии, %']) else None,
                        'Comm_Cost_rub': float(row['Ст-ть ком-ии, Руб']) if pd.notna(row['Ст-ть ком-ии, Руб']) else None,
                        'Material_id': material.Code if material else None,  # Для артикула "-" будет None
                        'Product_group_id': product_group_id,
                        'Document': row['Документ'],
                        'Date': row['Дата'].date() if pd.notna(row['Дата']) else None,
                        'Bill': row['Счет'],
                        'Bill_date': row['Дата счета'].date() if pd.notna(row['Дата счета']) else None,
                        'Litres_from': float(row['л от']) if pd.notna(row['л от']) else None,
                        'Litres_to': float(row['л до']) if pd.notna(row['л до']) else None,
                        'Recipient_code': row['Грузополучатель.Код'],
                        'Recipient': row['Грузополучатель'],
                        'Hyundai_code': row['Код дилера'],
                        'Comment': row['Комментарий']
                    }
                    
                    # Ищем существующую запись по ВСЕМ ключевым полям
                    existing = db.query(Commission).filter(
                        Commission.Customer_id == commission_data['Customer_id'],
                        Commission.Start_date == commission_data['Start_date'],
                        Commission.End_date == commission_data['End_date'],
                        Commission.Material_id == commission_data['Material_id'],
                        Commission.Product_group_id == commission_data['Product_group_id'],
                        Commission.Comm_perc == commission_data['Comm_perc'],
                        Commission.Comm_rub == commission_data['Comm_rub'],
                        Commission.Comm_Cost_perc == commission_data['Comm_Cost_perc'],
                        Commission.Comm_Cost_rub == commission_data['Comm_Cost_rub'],
                        Commission.Document == commission_data['Document'],
                        Commission.Bill == commission_data['Bill'],
                        Commission.Litres_from == commission_data['Litres_from'],
                        Commission.Litres_to == commission_data['Litres_to'],
                        Commission.Recipient_code == commission_data['Recipient_code'],
                        Commission.Recipient == commission_data['Recipient'],
                        Commission.Hyundai_code == commission_data['Hyundai_code']
                    ).first()
                    
                    if existing:
                        # Обновляем существующую запись
                        for key, value in commission_data.items():
                            setattr(existing, key, value)
                    else:
                        # Создаем новую запись
                        commission = Commission(**commission_data)
                        db.add(commission)
            
            db.commit()
            self.show_message("Данные комиссий успешно обновлены")
            self.refresh_all_comboboxes()
            self.find_commission()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка обновления из Excel: {str(e)}")

    def find_commission(self):
        """Поиск данных с фильтрами"""
        try:
            # Получаем параметры фильтрации
            customer = self.ui.line_customer.currentText()
            status = self.ui.line_status.currentText()
            product = self.ui.line_product.currentText()
            date_start = self.ui.line_date_start.date().toString("yyyy-MM-dd")
            date_end = self.ui.line_date_end.date().toString("yyyy-MM-dd")
            prod_name = self.ui.line_prod_name.currentText()
            
            # Строим запрос
            query = db.query(Commission).join(Customer, Commission.Customer_id == Customer.id)
            
            if customer != "-":
                customer_id = customer.split(" - ")[1] if " - " in customer else customer
                query = query.filter(Commission.Customer_id == customer_id)
            
            if status != "-":
                if status == "активные":
                    query = query.filter(
                        or_(
                            Commission.Document == "-",
                            Commission.Bill == "-",
                            and_(
                                Commission.End_date.isnot(None),
                                Commission.End_date >= datetime.now().date()
                            )
                        )
                    )
                else:  # "не активные"
                    query = query.filter(
                        or_(
                            Commission.Document != "-",
                            Commission.Bill != "-",
                            and_(
                                Commission.End_date.isnot(None),
                                Commission.End_date < datetime.now().date()
                            )
                        )
                    )
            
            if product != "-":
                # Фильтр по продукту через Materials и Product_Names
                query = query.join(Materials, Commission.Material_id == Materials.Code)\
                            .join(Product_Names, Materials.Product_Names_id == Product_Names.id)\
                            .filter(Product_Names.Product_name == product)
            
            if prod_name != "-":
                # Фильтр по product group
                query = query.join(Product_Group, Commission.Product_group_id == Product_Group.id)\
                            .filter(Product_Group.Product_name == prod_name)
            
            if date_start != "2022-01-01":
                filter_date = datetime.strptime(date_start, "%Y-%m-%d").date()
                query = query.filter(Commission.Start_date >= filter_date)
            
            if date_end != "2022-12-31":
                filter_date = datetime.strptime(date_end, "%Y-%m-%d").date()
                query = query.filter(Commission.End_date <= filter_date)
            
            # Выполняем запрос
            results = query.all()
            
            # Отображаем результаты
            self._display_data(results)
            
        except Exception as e:
            self.show_error_message(f"Ошибка поиска: {str(e)}")

    def _display_data(self, data):
        """Отображение данных в таблице"""
        self.table.clear()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        
        if not data:
            self.show_message('Нет данных для отображения')
            return
        
        # Устанавливаем флаг обновления таблицы
        self._updating_table = True
        
        # Названия колонок
        headers = [
            'ID', 'Статус', 'Контрагент.Код', 'Контрагент', 'Дата начала', 
            'Дата окончания', 'Комм %', 'Комм Руб', 'Ст-ть ком-ии, %', 
            'Ст-ть ком-ии, Руб', 'Артикул', 'Продукт + упаковка', 
            'Product name', 'Документ', 'Дата', 'Счет', 'Дата счета', 
            'л от', 'л до', 'Грузополучатель.Код', 'Грузополучатель', 
            'Код дилера', 'Комментарий'
        ]
        
        # Устанавливаем размеры таблицы
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Скрываем колонку ID
        self.table.setColumnHidden(0, True)
            
        # Заполняем данные
        for row_idx, commission in enumerate(data):
            # Расчет статуса
            status = "активные"
            if (commission.Document != "-" or commission.Bill != "-" or 
                (commission.End_date and commission.End_date < datetime.now().date())):
                status = "не активные"
            
            # Получаем артикул из Materials
            article = ""
            product_name = ""
            if commission.Material_id:
                material = db.query(Materials).filter(Materials.Code == commission.Material_id).first()
                if material:
                    article = material.Article
                    if material.product_name:
                        product_name = material.product_name.Product_name
            
            # Получаем product group (только если нет артикула)
            product_group = ""
            if commission.Product_group_id and not commission.Material_id:
                group = db.query(Product_Group).filter(Product_Group.id == commission.Product_group_id).first()
                if group:
                    product_group = group.Product_name
            
            # Данные для отображения
            row_data = [
                str(commission.id),
                status,
                str(commission.Customer_id),
                commission.customer.Customer_name if commission.customer else "",
                commission.Start_date.strftime('%Y-%m-%d') if commission.Start_date else "",
                commission.End_date.strftime('%Y-%m-%d') if commission.End_date else "",
                str(commission.Comm_perc) if commission.Comm_perc else "",
                str(commission.Comm_rub) if commission.Comm_rub else "",
                str(commission.Comm_Cost_perc) if commission.Comm_Cost_perc else "",
                str(commission.Comm_Cost_rub) if commission.Comm_Cost_rub else "",
                article,  # Артикул
                product_name,  # Продукт + упаковка
                product_group,  # Product name
                commission.Document or "",
                commission.Date.strftime('%Y-%m-%d') if commission.Date else "",
                commission.Bill or "",
                commission.Bill_date.strftime('%Y-%m-%d') if commission.Bill_date else "",
                str(commission.Litres_from) if commission.Litres_from else "",
                str(commission.Litres_to) if commission.Litres_to else "",
                commission.Recipient_code or "",
                commission.Recipient or "",
                commission.Hyundai_code or "",
                commission.Comment or ""
            ]
            
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                
                # Выравнивание для числовых колонок
                if col_idx in [6, 7, 8, 9, 17, 18]:  # числовые колонки
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    
                self.table.setItem(row_idx, col_idx, item)
        
        # Автоматическая настройка ширины столбцов
        self.table.resizeColumnsToContents()
        
        # Снимаем флаг обновления таблицы
        self._updating_table = False

    def show_message(self, text):
        """Показать информационное сообщение"""
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setIcon(QMessageBox.Information)
        
        # Устанавливаем большой минимальный размер
        msg.setMinimumSize(900, 600)
        
        # Всегда используем detailed text для длинных сообщений
        if len(text) > 500:
            short_text = "Подробная информация ниже (используйте кнопку 'Show Details')"
            msg.setText(short_text)
            msg.setDetailedText(text)
        else:
            msg.setText(text)
        
        # Кнопки
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        def copy_text():
            QApplication.clipboard().setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setIcon(QMessageBox.Critical)
        
        # Устанавливаем большой минимальный размер
        msg.setMinimumSize(900, 600)
        
        # Всегда используем detailed text для длинных сообщений
        if len(text) > 500:
            short_text = "Произошла ошибка. Подробности ниже (используйте кнопку 'Show Details')"
            msg.setText(short_text)
            msg.setDetailedText(text)
        else:
            msg.setText(text)
        
        # Кнопки
        copy_button = msg.addButton("Copy", QMessageBox.ActionRole)
        ok_button = msg.addButton(QMessageBox.Ok)
        
        def copy_text():
            QApplication.clipboard().setText(text)
        
        copy_button.clicked.connect(copy_text)
        msg.exec_()


class CommissionCreateForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = CreateFormUi()
        self.ui.setupUi(self)
        
        self.setup_connections()
        self.load_initial_data()
        
    def setup_connections(self):
        """Настройка соединений"""
        self.ui.btn_save.clicked.connect(self.save_data)
        self.ui.btn_cancel.clicked.connect(self.reject)
        
    def load_initial_data(self):
        """Загрузка начальных данных"""
        # Устанавливаем текущие даты
        today = datetime.now()
        self.ui.line_date_start.setDate(QDate(today.year, today.month, 1))
        self.ui.line_date_end.setDate(QDate(today.year, 12, 31))
        
        # Заполняем комбобоксы
        customers = db.query(Customer).all()
        customer_items = ["-"] + [f"{c.Customer_name} - {c.id}" for c in customers]
        self.ui.line_cust_name.addItems(customer_items)
        
        products = db.query(Product_Names).all()
        product_items = ["-"] + [p.Product_name for p in products]
        self.ui.line_prod_name.addItems(product_items)
        
        groups = db.query(Product_Group).all()
        group_items = ["-"] + [g.Product_name for g in groups]
        self.ui.line_prod_group.addItems(group_items)
        
    def save_data(self):
        """Сохранение данных"""
        try:
            # Валидация данных
            if not self.validate_data():
                return
                
            # Собираем данные клиента
            customer_text = self.ui.line_cust_name.currentText()
            customer_id = None
            
            if customer_text != "-":
                if " - " in customer_text:
                    # Извлекаем только ID клиента
                    customer_id = customer_text.split(" - ")[1]
                else:
                    customer = db.query(Customer).filter(Customer.Customer_name == customer_text).first()
                    if customer:
                        customer_id = customer.id
            
            # Обработка продукта - проверка взаимоисключающих полей
            product_name_id = None
            product_group_id = None
            article = self.ui.line_article.text().strip()
            prod_code = self.ui.line_prodCode.text().strip()
            prod_name = self.ui.line_prod_name.currentText()
            prod_group = self.ui.line_prod_group.currentText()
            
            # Проверка на одновременное заполнение взаимоисключающих полей
            has_article_or_code = article or prod_code
            has_product_selection = prod_name != "-" or prod_group != "-"
            
            if has_article_or_code and has_product_selection:
                self.show_error_message("Можно заполнить либо Артикул/Код продукта, либо выбрать Продукт/Группу, но не одновременно!")
                return
            
            if prod_code:
                # Проверяем существование кода
                material = db.query(Materials).filter(Materials.Code == prod_code).first()
                if material:
                    product_name_id = material.Product_name_id
                    product_group_id = material.Product_group_id
                    article = material.Article
            elif article:
                # Ищем материалы по артикулу
                materials = db.query(Materials).filter(
                    Materials.Article == article,
                    Materials.Status == 'активный'
                ).all()
                if materials:
                    material = materials[0]  # Берем первый активный
                    product_name_id = material.Product_name_id
                    product_group_id = material.Product_group_id
            else:
                # Обработка выбора из выпадающих списков
                if prod_name != "-":
                    # Ищем продукт по имени
                    product = db.query(Product_Names).filter(Product_Names.Product_name == prod_name).first()
                    if product:
                        product_name_id = product.id
                
                if prod_group != "-":
                    # Ищем группу по имени
                    group = db.query(Product_Group).filter(Product_Group.Product_name == prod_group).first()
                    if group:
                        product_group_id = group.id
            
            # Создаем запись комиссии
            commission = Commission(
                Customer_id=customer_id,
                Start_date=self.ui.line_date_start.date().toPython(),
                End_date=self.ui.line_date_end.date().toPython(),
                Comm_perc=self.parse_float(self.ui.line_commis_pers.text()),
                Comm_rub=self.parse_float(self.ui.line_commis_rub.text()),
                Comm_Cost_perc=self.parse_float(self.ui.line_cost_perc.text()),
                Comm_Cost_rub=self.parse_float(self.ui.line_cost_rub.text()),
                Material_id=article or None,
                Product_group_id=product_group_id,
                Document="",
                Bill="",
                Comment=""
            )
            
            db.add(commission)
            db.commit()
            
            self.show_message("Комиссия успешно сохранена")
            self.accept()
            
        except Exception as e:
            db.rollback()
            self.show_error_message(f"Ошибка сохранения: {str(e)}")
    
    def parse_float(self, text):
        """Парсинг чисел с различных форматов"""
        if not text:
            return None
        
        try:
            # Удаляем пробелы и знаки %
            cleaned = text.replace(' ', '').replace('%', '').replace(',', '.')
            return float(cleaned)
        except ValueError:
            return None
    
    def validate_data(self):
        """Валидация данных"""
        # Проверка клиента
        if self.ui.line_cust_name.currentText() == "-":
            self.show_error_message("Необходимо выбрать контрагента")
            return False
        
        # Проверка числовых полей
        numeric_fields = [
            (self.ui.line_commis_pers, "Комиссия %"),
            (self.ui.line_commis_rub, "Комиссия руб"),
            (self.ui.line_cost_perc, "Стоимость комиссии %"),
            (self.ui.line_cost_rub, "Стоимость комиссии руб")
        ]
        
        for field, name in numeric_fields:
            text = field.text().strip()
            if text and self.parse_float(text) is None:
                self.show_error_message(f"Неверный формат числа в поле '{name}'")
                return False
        
        return True
    
    def show_message(self, text):
        """Показать успешное сообщение в label_msg"""
        # Устанавливаем текст сообщения
        self.ui.label_msg.setText(text)
        
        # Устанавливаем стили для успешного сообщения
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
        
        # Делаем label видимым (на случай, если был скрыт)
        self.ui.label_msg.setVisible(True)
        
        # Опционально: автоматически скрыть сообщение через 5 секунд
        # from PySide6.QtCore import QTimer
        # QTimer.singleShot(5000, self.clear_message)

    def clear_message(self):
        """Очистить сообщение"""
        self.ui.label_msg.setText("")
        self.ui.label_msg.setStyleSheet("")
    
    
    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        QMessageBox.critical(self, "Ошибка", text)





