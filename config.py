from datetime import timedelta
import os



basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///Report_db.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost:5432/report_db'

SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from pathlib import Path

# Основная папка проекта (где находится скрипт)
# MAIN_FOLDER = Path(__file__).parent.absolute()
MAIN_FOLDER = Path("C:\\работа\\My_Work_Phoenix\\Daily_Report\\")
# Альтернативный вариант, если скрипт не в корне проекта:
# MAIN_FOLDER = Path(os.getcwd())

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Основные файлы
All_data_file = MAIN_FOLDER / "! All DATA !.xlsx"
AddCosts_File = MAIN_FOLDER / "! ДопРасходы !.xlsx"
CustDelivery_File = MAIN_FOLDER / "! Доставка клиентам !.xlsx"

# Файлы реестров
Material_file = MAIN_FOLDER / "Выгрузки" / "Реестры" / "Реестр номенклатур XLSX.xlsx"
Customer_file = MAIN_FOLDER / "Выгрузки" / "Реестры" / "Реестр контрагентов XLSX.xlsx"
Contract_file = MAIN_FOLDER / "Выгрузки" / "Реестры" / "Реестр договоров XLSX.xlsx"

# Файлы отчетов
Collection_file = MAIN_FOLDER / "! Сборщик отчета !.xlsx"
Complectation_file = MAIN_FOLDER / "! Комплектации !.xlsx"
new_Complectation_file = MAIN_FOLDER / "ERRORs_Compectations_new.xlsx"

Macro_File_Path = MAIN_FOLDER / "macro_for_report.xlsm"

# Папки
Movement_folder = MAIN_FOLDER / "Выгрузки" / "Движение"
Purchase_folder = MAIN_FOLDER / "Выгрузки" / "Закупки"
Sales_folder = MAIN_FOLDER / "Выгрузки" / "Продажи"

# Файлы счетов
Orders_file = MAIN_FOLDER / "Выгрузки" / "Счета" / "Заказы.xlsx"
Reserve_file = MAIN_FOLDER / "Выгрузки" / "Счета" / "Резервы.xlsx"

# WorkFiles
OZON_file = MAIN_FOLDER / "WorkFiles" / "ОЗОН.xlsm"
OZON_folder = MAIN_FOLDER / "WorkFiles" / "OZON" / "Отчет по товарам_нов"
Yandex_file = MAIN_FOLDER / "WorkFiles" / "Яндекс.xlsx"
WB_file = MAIN_FOLDER / "WorkFiles" / "WB.xlsx"
Sber_file = MAIN_FOLDER / "WorkFiles" / "СберМегаМаркет.xlsx"
cash_file = MAIN_FOLDER / "WorkFiles" / "Реестр заказов СПЕЦ УСЛОВИЯ.xlsx"
BMW_comm = MAIN_FOLDER / "WorkFiles" / "Комиссии BMW дилеры.xlsx"







# Final_Report_file = MAIN_FOLDER + "Daily_Report.xlsb"

# KAM_Report_template = MAIN_FOLDER + "Template\\Daily_Report_template.xlsx"
# OpenOrder_template = MAIN_FOLDER + "Template\\Открытые заказы_template.xlsx"
# CSC_Report_template = MAIN_FOLDER + "Template\\Счета и Резервы_template.xlsx"
# BMW_Valv_Report_template = MAIN_FOLDER + "Template\\BMW_Valv_template.xlsx"

# main_report_new_path = MAIN_FOLDER + "Reports"
# reports_folder_path = main_folder + "Reports\\" + str(report_day)
# BMW_Valv_folder_path = main_folder + "Reports\\"+ str(year_for_report) + '_w' + str(week_for_report)