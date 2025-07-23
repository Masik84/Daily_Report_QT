from datetime import timedelta
import os



basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///Report_db.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost:5432/report_db'

SQLALCHEMY_TRACK_MODIFICATIONS = False

path = os.getcwd()
MAIN_FOLDER = 'C:\\работа\\My_Work_Phoenix\\Daily_Report\\'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}




All_data_file = MAIN_FOLDER + "! All DATA !.xlsx"
Material_file = MAIN_FOLDER + "Выгрузки_new\\Реестр номенклатур XLSX.xlsx"
Customer_file = MAIN_FOLDER + "Выгрузки_new\\Реестр контрагентов XLSX.xlsx"
Contract_file = MAIN_FOLDER + "Выгрузки_new\\Реестр договоров XLSX.xlsx"


Collection_file = MAIN_FOLDER + "! Сборщик отчета !.xlsx"
Complectation_file = MAIN_FOLDER + "! Комплектации !.xlsx" 
new_Complectation_file = MAIN_FOLDER + "ERRORs_Compectations_new.xlsx"






Macro_File_Path = MAIN_FOLDER + "macro_for_report.xlsm"

Movement_folder = MAIN_FOLDER + "Выгрузки\\Движение"
Purchase_folder = MAIN_FOLDER + "Выгрузки\\Закупки"
Sales_folder = MAIN_FOLDER + "Выгрузки\\Продажи"

Orders_file = MAIN_FOLDER + "Выгрузки\\Счета\\Заказы.xlsx"
Reserve_file = MAIN_FOLDER + "Выгрузки\\Счета\\Резервы.xlsx"
Orders_file_new = MAIN_FOLDER + "Выгрузки\\Заказы.xlsx"

OZON_file = MAIN_FOLDER + "ОЗОН.xlsm"
OZON_folder = MAIN_FOLDER + "OZON\\Отчет по товарам"
Yandex_file = MAIN_FOLDER + "Яндекс.xlsx"
WB_file = MAIN_FOLDER + "WB.xlsx"
cash_file = MAIN_FOLDER + "Реестр заказов СПЕЦ УСЛОВИЯ.xlsx"
BMW_comm = MAIN_FOLDER + "Комиссии BMW дилеры.xlsx"
production = MAIN_FOLDER + "Приход из пр-ва.xlsx"

Final_Report_file = MAIN_FOLDER + "Daily_Report.xlsb"

KAM_Report_template = MAIN_FOLDER + "Template\\Daily_Report_template.xlsx"
OpenOrder_template = MAIN_FOLDER + "Template\\Открытые заказы_template.xlsx"
CSC_Report_template = MAIN_FOLDER + "Template\\Счета и Резервы_template.xlsx"
BMW_Valv_Report_template = MAIN_FOLDER + "Template\\BMW_Valv_template.xlsx"

main_report_new_path = MAIN_FOLDER + "Reports"
# reports_folder_path = main_folder + "Reports\\" + str(report_day)
# BMW_Valv_folder_path = main_folder + "Reports\\"+ str(year_for_report) + '_w' + str(week_for_report)