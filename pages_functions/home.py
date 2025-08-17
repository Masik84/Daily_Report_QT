from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QProgressDialog, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from datetime import datetime
from pages_functions.product import Product
from pages_functions.managers import Managers
from pages_functions.customer import Customer
from pages_functions.cost import Costs
from pages_functions.supplier import Supplier
from pages_functions.add_costs import AddSupplCosts

class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        
        self.setWindowIcon(QIcon(":/image/logo/лого_капля.ico"))
        
        self.setup_ui()
        self.setup_connections()
        
        # Создаем экземпляры классов справочников
        
        self.managers_module = Managers()
        self.customer_module = Customer()
        self.product_module = Product()
        self.cost_module = Costs()
        self.supplier_module = Supplier()
        self.addcosts_module = AddSupplCosts()
        

    def setup_ui(self):
        """Настройка интерфейса с кнопками"""
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        
        # Создаем кнопки
        self.btn_update_all = QPushButton("1. Обновить все Справочники")
        self.btn_update_purchases = QPushButton("2. Запустить обновление данных по Закупкам/Продажам")
        self.btn_update_main_report = QPushButton("3. Запустить обновление основного Отчета")
        self.btn_create_manager_files = QPushButton("4. Запустить формирование файлов для Менеджеров")
        self.btn_send_main_report = QPushButton("5. Отправить Основной Отчет")
        self.btn_send_manager_reports = QPushButton("6. Отправить Отчеты для Менеджеров")
        
        # Добавляем кнопки в layout
        self.layout.addWidget(self.btn_update_all)
        self.layout.addWidget(self.btn_update_purchases)
        self.layout.addWidget(self.btn_update_main_report)
        self.layout.addWidget(self.btn_create_manager_files)
        self.layout.addWidget(self.btn_send_main_report)
        self.layout.addWidget(self.btn_send_manager_reports)
        
        # Получаем список всех кнопок
        buttons = [
            self.btn_update_all, self.btn_update_purchases, 
            self.btn_update_main_report, self.btn_create_manager_files,
            self.btn_send_main_report, self.btn_send_manager_reports
        ]
        
        # Устанавливаем стили для кнопок
        for btn in buttons:
            # Рассчитываем ширину текста и добавляем 20 пикселей
            text_width = btn.fontMetrics().boundingRect(btn.text()).width()
            btn.setMinimumWidth(text_width + 20)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #f09d54;
                    border-radius: 5px;
                    background-color: #f8f8f2;
                    color: #964b09;
                    font: bold 12pt "Tahoma";
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #f28223;
                    color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #f28223;
                    border: 2px solid #f28223;
                    color: #ffffff;
                }
            """)    


    def setup_connections(self):
        """Настройка соединений сигналов и слотов"""
        self.btn_update_all.clicked.connect(self.update_all_references)
        self.btn_update_purchases.clicked.connect(self.update_purchases_sales)
        self.btn_update_main_report.clicked.connect(self.update_main_report)
        self.btn_create_manager_files.clicked.connect(self.create_manager_files)
        self.btn_send_main_report.clicked.connect(self.send_main_report)
        self.btn_send_manager_reports.clicked.connect(self.send_manager_reports)

    def update_all_references(self):
        """Обновляет все справочники в системе"""
        # Настройка прогресс-бара
        progress = QProgressDialog("Обновление справочников...", "Отмена", 0, 6, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        
        try:
            # 1. Обновление товаров
            progress.setLabelText("Обновление товаров...")
            QApplication.processEvents()
            if progress.wasCanceled():
                return False
                
            product = Product()
            if not product.upload_data():
                raise Exception("Ошибка обновления товаров")
            progress.setValue(1)

            # 2. Обновление менеджеров
            progress.setLabelText("Обновление менеджеров...")
            QApplication.processEvents()
            if progress.wasCanceled():
                return False
                
            managers = Managers()
            if not managers.upload_data():
                raise Exception("Ошибка обновления менеджеров")
            progress.setValue(2)

            # 3. Обновление клиентов
            progress.setLabelText("Обновление клиентов...")
            QApplication.processEvents()
            if progress.wasCanceled():
                return False
                
            customer = Customer()
            if not customer.upload_data():
                raise Exception("Ошибка обновления клиентов")
            progress.setValue(3)

            # 4. Обновление себестоимости
            progress.setLabelText("Обновление себестоимости...")
            QApplication.processEvents()
            if progress.wasCanceled():
                return False
                
            costs = Costs()
            if not costs.upload_data():
                raise Exception("Ошибка обновления себестоимости")
            progress.setValue(4)

            # 5. Обновление поставщиков
            progress.setLabelText("Обновление поставщиков...")
            QApplication.processEvents()
            if progress.wasCanceled():
                return False
                
            supplier = Supplier()
            if not supplier.upload_data():
                raise Exception("Ошибка обновления поставщиков")
            progress.setValue(5)

            # 6. Обновление дополнительных расходов
            progress.setLabelText("Обновление доп. расходов...")
            QApplication.processEvents()
            if progress.wasCanceled():
                return False
                
            add_costs = AddSupplCosts()
            if not add_costs.upload_data():
                raise Exception("Ошибка обновления дополнительных расходов")
            progress.setValue(6)

            # Успешное завершение
            progress.close()
            QMessageBox.information(
                self, 
                "Готово", 
                "Все справочники успешно обновлены!",
                QMessageBox.Ok
            )
            return True

        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка при обновлении:\n{str(e)}",
                QMessageBox.Ok
            )
            # Логирование ошибки
            with open("update_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()}: {str(e)}\n")
            return False

    def update_purchases_sales(self):
        """Обновление данных по закупкам/продажам"""
        self.show_message("Функция обновления данных по Закупкам/Продажам будет реализована позже")

    def update_main_report(self):
        """Обновление основного отчета"""
        self.show_message("Функция обновления основного Отчета будет реализована позже")

    def create_manager_files(self):
        """Формирование файлов для менеджеров"""
        self.show_message("Функция формирования файлов для Менеджеров будет реализована позже")

    def send_main_report(self):
        """Отправка основного отчета"""
        self.show_message("Функция отправки Основного Отчета будет реализована позже")

    def send_manager_reports(self):
        """Отправка отчетов для менеджеров"""
        self.show_message("Функция отправки Отчетов для Менеджеров будет реализована позже")

    def show_message(self, text):
        """Показать информационное сообщение"""
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(":/image/logo/лого_капля.ico"))
        msg.setText(text)
        msg.setStyleSheet("""
            background-color: #f8f8f2;
            font: 10pt "Tahoma";
            color: #237508;
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def show_error_message(self, text):
        """Показать сообщение об ошибке"""
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(":/image/logo/лого_капля.ico"))
        msg.setText(text)
        msg.setStyleSheet("""
            background-color: #f8f8f2;
            font: 10pt "Tahoma";
            color: #ff0000;
        """)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()