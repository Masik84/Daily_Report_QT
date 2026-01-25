
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

import sqlalchemy
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Index, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from db import Base, engine


class Team(Base):
    __tablename__ = 'team'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Team = Column(String)
    
    # Добавляем связи со всеми моделями
    managers = relationship("Manager", back_populates="team")
    stls = relationship("STL", back_populates="team")
    team_leads = relationship("TeamLead", back_populates="team")

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Manager_name = Column(String)
    Email = Column(String)
    AM_1C_Name = Column(String)
    Has_report = Column(String)  # 'да' или 'нет'
    Report_link = Column(String)
    Template = Column(String)

    # Внешние ключи
    STL_id = Column(Integer, ForeignKey('stls.id', name='fk_manager_stl'))
    TeamLead_id = Column(Integer, ForeignKey('team_leads.id', name='fk_manager_teamlead'))
    Team_id = Column(Integer, ForeignKey('team.id', name='fk_manager_team'))  # Добавляем связь с Team

    # Связи
    stl = relationship("STL", back_populates="managers")
    team_lead = relationship("TeamLead", back_populates="managers")
    team = relationship("Team", back_populates="managers")  # Добавляем связь с Team
    contracts = relationship("Contract", back_populates="manager")  # мн. число
    hyundai_dealers = relationship("Hyundai_Dealer", back_populates="manager")  # мн. число
    customer_plans = relationship("CustomerPlan", back_populates="manager")
    marketplace_entries = relationship("Marketplace", back_populates="manager")
    temp_sales_orders = relationship("temp_Sales_Orders", back_populates="manager")

class STL(Base):
    __tablename__ = 'stls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    STL_name = Column(String)
    Email = Column(String)
    Has_report = Column(String)  # 'да' или 'нет'
    Report_link = Column(String)
    Template = Column(String)
    
    Team_id = Column(Integer, ForeignKey('team.id', name='fk_stl_team'))  # Добавляем связь с Team

    # Связи
    team = relationship("Team", back_populates="stls")  # Добавляем связь с Team
    managers = relationship("Manager", back_populates="stl")
    customer_plans = relationship("CustomerPlan", back_populates="stl")

class TeamLead(Base):
    __tablename__ = 'team_leads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    TeamLead_name = Column(String)
    Email = Column(String)
    Has_report = Column(String)  # 'да' или 'нет'
    Report_link = Column(String)
    Template = Column(String)
    
    Team_id = Column(Integer, ForeignKey('team.id', name='fk_teamlead_team'))  # Добавляем связь с Team

    # Связи
    team = relationship("Team", back_populates="team_leads")  # Добавляем связь с Team
    managers = relationship("Manager", back_populates="team_lead")
    company_plans = relationship("CompanyPlan", back_populates="team_lead")
    customer_plans = relationship("CustomerPlan", back_populates="team_lead")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True)  
    Customer_code = Column(String) # Контрагент.Код (например "ОП-041205")
    Customer_name = Column(String) # Контрагент
    INN = Column(String) # Контрагент.ИНН
    Price_type = Column(String)  # Тип цен
    Region = Column(String)  # Регион
    City = Column(String)  # Город
    Customer_status = Column(String)  # Статус клиента

    Sector_id = Column(Integer, ForeignKey('sectors.id', name='fk_customer_sector'))
    Holding_id = Column(Integer, ForeignKey('holdings.id', name='fk_customer_holding'))

    # Связи
    sector = relationship("Sector", back_populates="customers")
    holding = relationship("Holding", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")
    marketplace_entries = relationship("Marketplace", back_populates="customer")
    movements = relationship("Movements", back_populates="customer")
    temp_sales_orders = relationship("temp_Sales_Orders", back_populates="customer")
    commissions = relationship("Commission", back_populates="customer")  # мн. число

class Holding(Base):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Holding_name = Column(String, unique=True, nullable=False)  # Название холдинга

    customers = relationship("Customer", back_populates="holding")
    customer_plans = relationship("CustomerPlan", back_populates="holding")
    marketplace_entries = relationship("Marketplace", back_populates="holding")

class Sector(Base):
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Sector_name = Column(String, unique=True, nullable=False)

    customers = relationship("Customer", back_populates="sector")
    customer_plans = relationship("CustomerPlan", back_populates="sector")
    marketplace_entries = relationship("Marketplace", back_populates="sector")

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(String, primary_key=True)  # ДоговорКод (например "ОП-002494")
    Contract = Column(String)
    Contract_Type = Column(String)  # "С покупателем"
    Price_Type = Column(String)
    Payment_Condition = Column(String)

    # Внешние ключи
    Customer_id = Column(String, ForeignKey('customers.id', name='fk_contract_customer'))
    Manager_id = Column(Integer, ForeignKey('managers.id', name='fk_contract_manager'))

    # Связи
    customer = relationship("Customer", back_populates="contracts")
    manager = relationship("Manager", back_populates="contracts")
    marketplace_entries = relationship("Marketplace", back_populates="contract")
    temp_sales_orders = relationship("temp_Sales_Orders", back_populates="contract")

class Hyundai_Dealer(Base):
    __tablename__ = 'hyundai_dealers'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Внутренний ID (автоинкремент)
    Dealer_code = Column(String, unique=True)  # "Код дилера HYUNDAI" (может быть NULL)
    Hyundai_code = Column(String, unique=True, nullable=False)  # "Код в HYUNDAI" (обязателен)
    Name = Column(String)  # "Наим дилера HYUNDAI"
    City = Column(String)  # "Город"
    INN = Column(String)  # "ИНН"

    # Связь с менеджером
    Manager_id = Column(Integer, ForeignKey('managers.id', name='fk_dealer_manager'))
    manager = relationship("Manager", back_populates="hyundai_dealers")  # ед. число

    __table_args__ = (
        Index('idx_hyundai_code_unique', 'Hyundai_code', unique=True),
        Index('idx_dealer_code_unique', 'Dealer_code', unique=True),
    )

    @hybrid_property
    def HasDealerCode(self):
        return self.Dealer_code is not None

class TNVED(Base):
    __tablename__ = 'tnved'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)  # ТН ВЭД код

    # Связи
    product_groups = relationship("Product_Group", back_populates="tnved")
    ecofee_amounts = relationship("EcoFee_amount", back_populates="tnved")
    ecofee_standards = relationship("EcoFee_standard", back_populates="tnved")
    customs_rates = relationship("Customs_Rate", back_populates="tnved")

class Product_Family(Base):
    __tablename__ = 'product_family'

    id = Column(String, primary_key=True)
    Product_family = Column(String)  # Family
    
    # Связи
    product_groups = relationship("Product_Group", back_populates="product_family")
    bonuses = relationship("Bonus", back_populates="product_family")

class Product_Group(Base):
    __tablename__ = 'product_group'

    id = Column(String, primary_key=True)  # Код группы
    Product_name = Column(String)  # Product name
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_product_group_tnved'))  # Ссылка на ТН ВЭД
    Product_Family_id = Column(String, ForeignKey('product_family.id', name='fk_product_group_family'))  # Добавляем связь с Product_Family

    # Связи
    tnved = relationship("TNVED", back_populates="product_groups")
    product_family = relationship("Product_Family", back_populates="product_groups")
    product_names = relationship("Product_Names", back_populates="product_group")
    commissions = relationship("Commission", back_populates="product_group")

class Product_Names(Base):
    __tablename__ = 'product_names'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Product_name = Column(String, unique=True, nullable=False)
    Product_Group_id = Column(String, ForeignKey('product_group.id', name='fk_product_names_product_group'))

    # Связи
    product_group = relationship("Product_Group", back_populates="product_names")
    materials = relationship("Materials", back_populates="product_name")
    abc_cat = relationship("ABC_cat", back_populates="product_name")

class Materials(Base):
    __tablename__ = 'material'

    Code = Column(String, primary_key=True)  # Код
    Article = Column(String)  # Артикул
    Full_name = Column(String)  # Полное наименование
    Brand = Column(String)
    Product_type = Column(String)  # Type
    UoM = Column(String)  # Единица
    Report_UoM = Column(String)  # Единица измерения отчетов
    Package_type = Column(String)  # Вид упаковки
    Items_per_Package = Column(Integer)  # Количество в упаковке
    Items_per_Set = Column(Integer)  # Шт в комплекте
    Package_Volume = Column(Numeric)  # Упаковка(Литраж)
    Net_weight = Column(Numeric)  # Нетто
    Gross_weight = Column(Numeric)  # Брутто
    Density = Column(Numeric)  # Плотность
    Excise = Column(String)  # Акциз
    Ecofee = Column(String)  # Экосбор
    Labling = Column(String)  # ЧЗ
    Status = Column(String)

    Product_Names_id = Column(Integer, ForeignKey('product_names.id', name='fk_materials_product_names'))

    # Связи
    product_name = relationship("Product_Names", back_populates="materials")
    marketplace_entries = relationship("Marketplace", back_populates="material")
    movements = relationship("Movements", back_populates="material")
    complects_manual = relationship("Complects_manual", back_populates="material")
    write_off = relationship("WriteOff", back_populates="material")
    complects = relationship("Complects", back_populates="material")
    temp_purchases = relationship("temp_Purchase", back_populates="material")
    temp_sales_orders = relationship("temp_Sales_Orders", back_populates="material")
    purchase_orders = relationship("Purchase_Order", back_populates="material")
    commissions = relationship("Commission", back_populates="material")  # мн. число

class ABC_list(Base):
    __tablename__ = 'abc_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ABC_category = Column(String(10), unique=True, nullable=False)  # 'A', 'B', 'C', 'D'

    # Связи
    abc_cat = relationship("ABC_cat", back_populates="abc_list")  # Изменили с abc_records на abc_cat
    company_plans = relationship("CompanyPlan", back_populates="ABC_category")

class ABC_cat(Base):
    __tablename__ = 'abc_cat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name_id = Column(Integer, ForeignKey('product_names.id', name='fk_abc_cat_product_names'))
    abc_list_id = Column(Integer, ForeignKey('abc_list.id', name='fk_abc_cat_abc_list'))
    Start_date = Column(sqlalchemy.Date())
    End_date = Column(sqlalchemy.Date())

    # Связи
    product_name = relationship("Product_Names", back_populates="abc_cat")
    abc_list = relationship("ABC_list", back_populates="abc_cat")

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(String, primary_key=True)  # Контрагент.Код (например "ОП-041205")
    Supplier_Name = Column(String)         # Контрагент (краткое название)
    Full_Suppl_name = Column(String)       # Полное наименование
    Imp_Loc = Column(String)               # Имп/Лок (да/нет)
    Customs = Column(String)               # Тамож. Пошлина (да/нет)
    Movement = Column(String)              # Перемещ (да/нет)
    Country = Column(String)               # Страна Рег-ии

    # Связи
    schemes = relationship("SupplScheme", back_populates="supplier", cascade="all, delete-orphan")
    add_suppl_costs = relationship("AddSupplCost", back_populates="supplier")
    movements = relationship("Movements", back_populates="supplier")
    write_off = relationship("WriteOff", back_populates="supplier")
    temp_purchases = relationship("temp_Purchase", back_populates="supplier")
    temp_sales_orders = relationship("temp_Sales_Orders", back_populates="supplier")
    purchase_orders = relationship("Purchase_Order", back_populates="supplier")
    bonuses = relationship("Bonus", back_populates="supplier")

class SupplScheme(Base):
    __tablename__ = 'suppl_schemes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Supplier1 = Column(String)             # Supplier 1
    Country = Column(String)               # Страна
    Supplier2 = Column(String)             # Supplier 2
    Supplier_id = Column(String, ForeignKey('suppliers.id', name='fk_scheme_supplier'))  # Контрагент.Код
    Supplier_Name_report = Column(String, unique=True)  # Контрагент для отчета # уникальное поле)
    Agency = Column(Numeric)                # Агентские
    Re_export = Column(Numeric)             # Re-export
    Delivery = Column(Numeric)              # Доставка
    Comment = Column(String)               # Комментарий
    
    # Связи
    supplier = relationship("Supplier", back_populates="schemes")

class AddSupplCost(Base):
    """Модель дополнительных расходов поставщиков"""
    __tablename__ = 'add_suppl_cost'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date())  # Дата
    Supplier_id = Column(String, ForeignKey('suppliers.id'))  # Контрагент.Код
    Supplier_Name_report = Column(String)  # Контрагент (отчетное название)
    Supplier1 = Column(String)  # Supplier 1
    Supplier2 = Column(String)  # Supplier 2
    Order = Column(String)  # Order N
    Shipment = Column(String)  # Shipment #
    Container = Column(String)  # Container
    Suppl_Inv_N = Column(String)  # Suppl Inv N
    Storage = Column(String)  # Склад
    Imp_Loc = Column(String)  # Имп/Лок
    Movement = Column(String)  # Перемещ
    Bonus = Column(String)  # Бонус
    Labling_Stock = Column(String)   # Склад маркировки
    Volume = Column(Numeric)  # Объем
    First_Invoice_Amount = Column(Numeric)  # Сумма 1го Поставщика
    Final_Invoice_Amount = Column(Numeric)  # Сумма 1С
    GTD_doc = Column(String)  # Номер ГТД
    Status = Column(String)  # Статус
    Currency = Column(String)  # Валюта
    Payment_FX = Column(Numeric)  # Курс оплаты
    Load_Unload = Column(Numeric)  # Погрузка/Выгрузка
    Commission = Column(Numeric)  # Комиссия платежному агенту
    Agency = Column(Numeric)  # Агентские
    Transport_mn = Column(Numeric)  # Транспорт м.н.
    Transport_loc = Column(Numeric)  # Транспорт лок.
    Add_Services = Column(Numeric)  # Доп услуги
    Comment = Column(String)  # Комментарий
    Transp_VED = Column(Numeric)  # Ст-ть трансп ВЭД
    Customs_date = Column(sqlalchemy.Date(), nullable=True)  # Тамож. дата
    Date_arrival = Column(sqlalchemy.Date(), nullable=True)  # Дата прихода
    Carrier = Column(String)  # м/н перевозчик
    Carrier_orders = Column(String)  # Счета
    merge_id = Column(String, unique=True)  # Уникальный идентификатор для проверки

    # Связи
    supplier = relationship("Supplier", back_populates="add_suppl_costs")
    purchase_orders = relationship("Purchase_Order", back_populates="add_suppl_cost")

class EcoFee_amount(Base):  # экосбор_ставки
    __tablename__ = 'ecofee_amount'

    id = Column(Integer, primary_key=True, autoincrement=True)
    merge = Column(String, unique=True)
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_ecofee_amount_tnved'))
    year_id = Column(Integer, ForeignKey('years.id', name='fk_ecofee_amount_year'))
    ECO_amount = Column(Numeric)

    tnved = relationship("TNVED", back_populates="ecofee_amounts")
    year = relationship("Year", back_populates="ecofee_amounts")

class EcoFee_standard(Base):  # экосбор_норматив
    __tablename__ = 'ecofee_standard'

    id = Column(Integer, primary_key=True, autoincrement=True)
    merge = Column(String, unique=True)
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_ecofee_standard_tnved'))
    year_id = Column(Integer, ForeignKey('years.id', name='fk_ecofee_standard_year'))
    ECO_standard = Column(Numeric)

    tnved = relationship("TNVED", back_populates="ecofee_standards")
    year = relationship("Year", back_populates="ecofee_standards")

class Customs_Rate(Base):
    __tablename__ = 'customs_rate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_customs_rate_tnved'))
    Cust_rate = Column(Numeric)

    tnved = relationship("TNVED", back_populates="customs_rates")

    def __repr__(self):
        return f"<Customs_Rate(TNVED_id={self.TNVED_id}, Cust_rate={self.Cust_rate})>"

class Labling(Base):
    __tablename__ = 'labling'

    # Уникальность по году и месяцу
    __table_args__ = (UniqueConstraint('year_id', 'month_id', name='uq_labling_year_month'), )

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_id = Column(Integer, ForeignKey('years.id', name='fk_labling_year'))  # Ссылка на год
    month_id = Column(Integer, ForeignKey('months.id', name='fk_labling_month'))  # Ссылка на месяц

    чехов_1 = Column(Numeric)
    чехов_5 = Column(Numeric)
    чехов_25 = Column(Numeric)
    чехов_60 = Column(Numeric)
    чехов_230 = Column(Numeric)
    тлтк_1 = Column(Numeric)
    тлтк_5 = Column(Numeric)
    тлтк_25 = Column(Numeric)
    тлтк_60 = Column(Numeric)
    тлтк_230 = Column(Numeric)
    баррус_1 = Column(Numeric)
    баррус_5 = Column(Numeric)
    баррус_25 = Column(Numeric)
    баррус_60 = Column(Numeric)
    баррус_230 = Column(Numeric)
    дельта_1 = Column(Numeric)
    дельта_5 = Column(Numeric)
    дельта_25 = Column(Numeric)
    дельта_60 = Column(Numeric)
    дельта_230 = Column(Numeric)
    
    # Связи
    year = relationship("Year", back_populates="lablings")
    month = relationship("Month", back_populates="lablings")
    
class Fees(Base):
    __tablename__ = 'taxfee'

    __table_args__ = (
        UniqueConstraint('year_id', 'month_id', name='uq_taxfee_year_month'),  # Уникальность по году и месяцу
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_id = Column(Integer, ForeignKey('years.id', name='fk_fees_year'))  # Ссылка на год
    month_id = Column(Integer, ForeignKey('months.id', name='fk_fees_month'))  # Ссылка на месяц
    Excise = Column(Numeric)  # Акциз
    Customs_clearance = Column(Numeric)  # Тамож. оформление
    Bank_commission = Column(Numeric)  # Комиссия банка
    Transportation = Column(Numeric)  # Транспорт (перемещ), л
    Storage = Column(Numeric)  # Хранение, л
    Money_cost = Column(Numeric)  # Ст-ть Денег
    Additional_money_percent = Column(Numeric)  # Доп% денег
    Lable = Column(Numeric)  # Марка
    Okleyka = Column(Numeric)   # Оклейка остатков
    Storage_Teboil = Column(Numeric)   # Хранение Тебойл
    Transport_Teboil = Column(Numeric)   # Трансп Тебойл
    
    # Связи
    year = relationship("Year", back_populates="fees")
    month = relationship("Month", back_populates="fees")

class Bonus(Base):
    __tablename__ = 'bonus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Start_date = Column(sqlalchemy.Date(), nullable=False)
    End_date = Column(sqlalchemy.Date(), nullable=False)
    Supplier_id = Column(String, ForeignKey('suppliers.id'))  # Контрагент.Код
    Price_type = Column(String)  # Вид цены
    Product_Type = Column(String)  # Type
    Product_Family = Column(String)  # Family
    Material_name = Column(String)  # Продукт + упаковка
    Article = Column(String)   # Артикул
    Bonus_pers = Column(Numeric)  # Бонус, %
    Bonus_rub = Column(Numeric)  # Бонус, р/кг
    
    # Связи
    supplier = relationship("Supplier", back_populates="bonus")
    
class DOCType(Base):
    __tablename__ = 'doc_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Document = Column(String) # Вид документа
    Transaction = Column(String) # Вид операции
    Doc_type = Column(String) # Тип документа
    
    marketplace_entries = relationship("Marketplace", back_populates="doc_type")
    movements = relationship("Movements", back_populates="doc_type")
    complects_manual = relationship("Complects_manual", back_populates="doc_type")
    write_off = relationship("WriteOff", back_populates="doc_type")
    complects = relationship("Complects", back_populates="doc_type")
    temp_purchases = relationship("temp_Purchase", back_populates="doc_type")
    temp_sales_orders = relationship("temp_Sales_Orders", back_populates="doc_type")
    purchase_orders = relationship("Purchase_Order", back_populates="doc_type")

class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Year = Column(Integer, unique=True, nullable=False)  # Год

    company_plans = relationship("CompanyPlan", back_populates="year")
    customer_plans = relationship("CustomerPlan", back_populates="year")
    calendar_entries = relationship("Calendar", back_populates="year")
    ecofee_amounts = relationship("EcoFee_amount", back_populates="year")
    ecofee_standards = relationship("EcoFee_standard", back_populates="year")
    fees = relationship("Fees", back_populates="year")
    lablings = relationship("Labling", back_populates="year")

class Month(Base):
    __tablename__ = 'months'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Month = Column(Integer, nullable=False)  # 1-12
    Quarter_id = Column(Integer, ForeignKey('quarters.id', name='fk_months_Quarter_id_quarters'), nullable=False)

    company_plans = relationship("CompanyPlan", back_populates="month")  # Строковая
    customer_plans = relationship("CustomerPlan", back_populates="month")  # Строковая
    quarter = relationship("Quarter", back_populates="months")  # Строковая
    calendar_entries = relationship("Calendar", back_populates="month")  # Строковая
    fees = relationship("Fees", back_populates="month")  # Строковая
    lablings = relationship("Labling", back_populates="month")  # Строковая

class Quarter(Base):
    __tablename__ = 'quarters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Quarter = Column(Integer, nullable=False)  # 1-4

    months = relationship("Month", back_populates="quarter")  # Строковая ссылка
    calendar_entries = relationship("Calendar", back_populates="quarter")  # Строковая ссылка

class Week(Base):
    __tablename__ = 'weeks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Week_of_Year = Column(Integer, nullable=False)  # 1-53
    Week_of_Month = Column(Integer, nullable=False)  # 1-5

    company_plans = relationship("CompanyPlan", back_populates="week")  # Строковая
    customer_plans = relationship("CustomerPlan", back_populates="week")  # Строковая
    calendar_entries = relationship("Calendar", back_populates="week")  # Строковая

class Calendar(Base):
    __tablename__ = 'calendar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Day = Column(sqlalchemy.Date(), nullable=False, unique=True)
    Year_id = Column(Integer, ForeignKey('years.id', name='fk_calendar_Year_id_years'), nullable=False)
    Quarter_id = Column(Integer, ForeignKey('quarters.id', name='fk_calendar_Quarter_id_quarters'), nullable=False)
    Month_id = Column(Integer, ForeignKey('months.id', name='fk_calendar_Month_id_months'), nullable=False)
    Week_id = Column(Integer, ForeignKey('weeks.id', name='fk_calendar_Week_id_weeks'), nullable=False)
    NETWORKDAYS = Column(Integer, nullable=False)

    year = relationship("Year", back_populates="calendar_entries")
    quarter = relationship("Quarter", back_populates="calendar_entries")
    month = relationship("Month", back_populates="calendar_entries")
    week = relationship("Week", back_populates="calendar_entries")
    marketplace_entries = relationship("Marketplace", back_populates="calendar")

class CompanyPlan(Base):
    __tablename__ = 'company_plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Work_Days = Column(Integer)
    Month_vol = Column(Numeric)
    Month_Revenue = Column(Numeric)
    Month_Margin = Column(Numeric)
    Volume_Target_total = Column(Numeric)
    Revenue_Target_total = Column(Numeric)
    Margin_Target_total = Column(Numeric)
    Status = Column(String, default='План')

    # Связи с периодами
    Year_id = Column(Integer, ForeignKey('years.id', name='fk_company_plans_Year_id_years'))
    Month_id = Column(Integer, ForeignKey('months.id', name='fk_company_plans_Month_id_months'))
    Week_id = Column(Integer, ForeignKey('weeks.id', name='fk_company_plans_Week_id_weeks'))

    # Остальные связи
    TeamLead_id = Column(Integer, ForeignKey('team_leads.id', name='fk_company_plans_TeamLead_id_team_leads'))
    ABC_category_id = Column(Integer, ForeignKey('abc_list.id', name='fk_company_plans_ABC_category_id_abc_list'))

    # Отношения с back_populates
    year = relationship("Year", back_populates="company_plans")
    month = relationship("Month", back_populates="company_plans")
    week = relationship("Week", back_populates="company_plans")
    team_lead = relationship("TeamLead", back_populates="company_plans")
    ABC_category = relationship("ABC_list", back_populates="company_plans")

class CustomerPlan(Base):
    __tablename__ = 'customer_plans'
    
    __table_args__ = (
        UniqueConstraint('Year_id', 'Month_id', 'Week_id', 'Holding_id', 'Manager_id', 
                       name='uq_customer_plan_unique'),)
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Volume_Target_cust = Column(Numeric)
    Revenue_Target_cust = Column(Numeric)
    Margin_C3_Target_cust = Column(Numeric)
    Margin_C4_Target_cust = Column(Numeric)
    Status = Column(String, default='План')

    # Связи с периодами
    Year_id = Column(Integer, ForeignKey('years.id', name='fk_customer_plans_Year_id_years'))
    Month_id = Column(Integer, ForeignKey('months.id', name='fk_customer_plans_Month_id_months'))
    Week_id = Column(Integer, ForeignKey('weeks.id', name='fk_customer_plans_Week_id_weeks'))

    # Связи со справочниками
    Holding_id = Column(Integer, ForeignKey('holdings.id', name='fk_customer_plans_Holding_id_holdings'))
    Manager_id = Column(Integer, ForeignKey('managers.id', name='fk_customer_plans_Manager_id_managers'))
    Sector_id = Column(Integer, ForeignKey('sectors.id', name='fk_customer_plans_Sector_id_sectors'))
    STL_id = Column(Integer, ForeignKey('stls.id', name='fk_customer_plans_STL_id_stls'))
    TeamLead_id = Column(Integer, ForeignKey('team_leads.id', name='fk_customer_plans_TeamLead_id_team_leads'))

    # Отношения
    year = relationship("Year", back_populates="customer_plans")  # строчная
    month = relationship("Month", back_populates="customer_plans")  # строчная
    week = relationship("Week", back_populates="customer_plans")  # строчная
    holding = relationship("Holding", back_populates="customer_plans")  # строчная
    manager = relationship("Manager", back_populates="customer_plans")  # строчная
    sector = relationship("Sector", back_populates="customer_plans")  # строчная
    stl = relationship("STL", back_populates="customer_plans")  # строчная
    team_lead = relationship("TeamLead", back_populates="customer_plans")  # строчная

class Marketplace(Base):
    __tablename__ = 'marketplace'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date())  # Дата
    Qty = Column(Numeric)  # Количество
    Amount_1C = Column(Numeric)  # Сумма 1С
    Price_1C = Column(Numeric)  # Цена 1С (рассчитывается как Amount_1C / Qty)
    Payment_terms = Column(String)  # Условие оплаты
    Post_payment = Column(Numeric)  # Постоплата%
    Plan_pay_Date = Column(sqlalchemy.Date(), nullable=True)  # Плановая дата оплаты
    Stock = Column(String)  # Склад
    UoM = Column(String)  # Единица измерения
    Currency = Column(String)  # Валюта
    FX_rate = Column(Numeric)  # Курс взаиморасчетов
    VAT = Column(String)  # % НДС
    
    # Внешние ключи
    Calendar_id = Column(Integer, ForeignKey('calendar.id', name='fk_marketplace_calendar'))
    Material_id = Column(String, ForeignKey('material.Code', name='fk_marketplace_material'))
    Customer_id = Column(String, ForeignKey('customers.id', name='fk_marketplace_customer'))
    Manager_id = Column(Integer, ForeignKey('managers.id', name='fk_marketplace_manager'))
    Contract_id = Column(String, ForeignKey('contracts.id', name='fk_marketplace_contract'))
    Holding_id = Column(Integer, ForeignKey('holdings.id', name='fk_marketplace_holding'))
    Sector_id = Column(Integer, ForeignKey('sectors.id', name='fk_marketplace_sector'))
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_marketplace_doctype'))
    
    # Связи
    calendar = relationship("Calendar", back_populates="marketplace_entries")
    material = relationship("Materials", back_populates="marketplace_entries")
    customer = relationship("Customer", back_populates="marketplace_entries")
    manager = relationship("Manager", back_populates="marketplace_entries")
    contract = relationship("Contract", back_populates="marketplace_entries")
    holding = relationship("Holding", back_populates="marketplace_entries")
    sector = relationship("Sector", back_populates="marketplace_entries")
    doc_type = relationship("DOCType", back_populates="marketplace_entries")
    
    __table_args__ = (
        Index('idx_marketplace_document', 'Document'),
        Index('idx_marketplace_date', 'Date'),
        Index('idx_marketplace_material', 'Material_id'),
        Index('idx_marketplace_holding', 'Holding_id'),
    )

class Movements(Base):
    __tablename__ = 'movements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date_Time = Column(DateTime)  # Дата_Время
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date())  # Дата
    Doc_based = Column(String, nullable=True)  # ДокОсн
    Date_Doc_based = Column(sqlalchemy.Date(), nullable=True)  # Дата ДокОсн
    Stock = Column(String)  # Склад
    Qty = Column(Numeric)  # Количество
    Recipient_code = Column(String)  # Грузополучатель.Код
    Recipient = Column(String)  # Грузополучатель
    Bill = Column(String)  # Счет
    Bill_date = Column(sqlalchemy.Date(), nullable=True)  # Дата счета
    
    # Внешние ключи
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_movements_doctype'))  # Тип документа
    Material_id = Column(String, ForeignKey('material.Code', name='fk_movements_material'))  # Код материала
    Customer_id = Column(String, ForeignKey('customers.id', name='fk_movements_customer'), nullable=True)  # Контрагент.Код (Customer)
    Supplier_id = Column(String, ForeignKey('suppliers.id', name='fk_movements_supplier'), nullable=True)  # Контрагент.Код (Supplier)
    
    # Связи
    doc_type = relationship("DOCType", back_populates="movements")
    material = relationship("Materials", back_populates="movements")
    customer = relationship("Customer", back_populates="movements")
    supplier = relationship("Supplier", back_populates="movements")

class Complects_manual(Base):
    __tablename__ = 'complects_manual'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date_Time = Column(DateTime)  # Дата_Время
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date())  # Дата
    Stock = Column(String)  # Склад
    Qty = Column(Numeric)  # Количество
    
    # Внешние ключи
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_complects_doctype'))  # Тип документа
    Material_id = Column(String, ForeignKey('material.Code', name='fk_complects_material'))  # Код
    
    # Связи
    doc_type = relationship("DOCType", back_populates="complects_manual")
    material = relationship("Materials", back_populates="complects_manual")

class Complects(Base):
    __tablename__ = 'complects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date_Time = Column(DateTime)  # Дата_Время
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date())  # Дата
    Stock = Column(String)  # Склад
    Qty = Column(Numeric)  # Количество
    
    # Внешние ключи
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_complects_doctype'))  # Тип документа
    Material_id = Column(String, ForeignKey('material.Code', name='fk_complects_material'))  # Код материала
    
    # Связи
    doc_type = relationship("DOCType", back_populates="complects")
    material = relationship("Materials", back_populates="complects")
    
class WriteOff(Base):
    __tablename__ = 'write_off'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Date_Time = Column(DateTime)  # Дата_Время
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date())  # Дата
    Stock = Column(String)  # Склад
    Comment = Column(String)  # Комментарий
    inComing = Column(Numeric)  # Приход
    outComing = Column(Numeric)  # Расход
    Qty = Column(Numeric)  # Количество
    Reporting = Column(String)  # Отчет
    Doc_based = Column(String, nullable=True)  # ДокОсн
    Date_Doc_based = Column(sqlalchemy.Date(), nullable=True)  # Дата ДокОсн
    Order = Column(String)  # Order N
    Shipment = Column(String)  # Shipment #
    Suppl_Inv_N = Column(String)  # Вход. док-т
    Bill = Column(String)  # Счет
    Bill_date = Column(sqlalchemy.Date(), nullable=True)  # Дата счета
    
    # Внешние ключи
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_writeoff_doctype'))  # Тип документа
    Material_id = Column(String, ForeignKey('material.Code', name='fk_writeoff_material'))  # Код материала
    Supplier_id = Column(String, ForeignKey('suppliers.id', name='fk_writeoff_supplier'), nullable=True)  # Контрагент.Код
    
    # Связи
    doc_type = relationship("DOCType", back_populates="write_off")
    material = relationship("Materials", back_populates="write_off")
    supplier = relationship("Supplier", back_populates="write_off")

class temp_Purchase(Base):
    __tablename__ = 'temp_purchase'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Document = Column(String)                                                       # Документ
    Date = Column(sqlalchemy.Date())                                              # Дата
    Status = Column(String)                                                             # Статус
    Doc_based = Column(String, nullable=True)                               # ДокОсн
    Date_Doc_based = Column(sqlalchemy.Date(), nullable=True)   # Дата ДокОсн
    Stock = Column(String)                                                              # Склад
    Currency = Column(String)                                                         # Валюта
    VAT = Column(String)                                                                # % НДС
    Country = Column(String)                                                          # Страна происхождения
    GTD = Column(String)                                                                # Номер ГТД
    FX_rate_1C = Column(Numeric, nullable=True)                         # Курс взаиморасчетов
    Qty = Column(Numeric)                                                             # Количество
    Amount_1C = Column(Numeric)                                                 # Сумма 1С

    # Внешние ключи
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_temp_purchase_doctype'))
    Supplier_id = Column(String, ForeignKey('suppliers.id', name='fk_temp_purchase_supplier'), nullable=True)
    Material_id = Column(String, ForeignKey('material.Code', name='fk_temp_purchase_material'))
    
    # Связи
    doc_type = relationship("DOCType", back_populates="temp_purchases")
    supplier = relationship("Supplier", back_populates="temp_purchases")
    material = relationship("Materials", back_populates="temp_purchases")

class temp_Sales_Orders(Base):
    __tablename__ = 'temp_sales_orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Document = Column(String)  # Документ (из обеих)
    Date = Column(sqlalchemy.Date())  # Дата (из обеих)
    Status = Column(String)  # Статус (из обеих)
    Bill = Column(String)  # Счет (из обеих)
    Bill_Date = Column(sqlalchemy.Date(), nullable=True)  # Дата счета (из обеих)
    Doc_based = Column(String, nullable=True)  # ДокОсн (из обеих)
    Date_Doc_based = Column(sqlalchemy.Date(), nullable=True)  # Дата ДокОсн (из обеих)
    Stock = Column(String)  # Склад (из обеих)
    Delivery_method = Column(String)  # Способ доставки (из обеих)
    Currency = Column(String)  # Валюта (из обеих)
    FX_rate_1C = Column(Numeric, nullable=True)  # Курс взаиморасчетов (из обеих)
    Qty = Column(Numeric)  # Количество (из обеих)
    Amount_1C = Column(Numeric)  # Сумма 1С (из обеих)
    VAT = Column(String)  # % НДС (из обеих)
    Recipient = Column(String, nullable=True)  # Грузополучатель (из обеих)
    Recipient_code = Column(String, nullable=True)  # Грузополучатель.Код (из обеих)
    Days_for_Pay = Column(Numeric)  # Кол-во дней на оплату (из обеих)
    Plan_Pay_Day = Column(sqlalchemy.Date(), nullable=True)  # Плановая дата оплаты (из обеих)
    Post_payment = Column(Numeric)  # Постоплата% (из обеих)
    Payment_term = Column(String)  # Условие оплаты
    Pay_status = Column(String)  # Статус оплаты
    Priority = Column(String)  # Приоритет (из обеих)
    Comment = Column(String)  # Комментарий (из обеих)
    Sborka = Column(String)  # Сборка (из обеих)
    Plan_Delivery_Day = Column(sqlalchemy.Date(), nullable=True)  # ПланДатаОтгр
    Spec_Order = Column(String, nullable=True)  # Спец поставка (из обеих)
    Reserve_date = Column(sqlalchemy.Date(), nullable=True)  # Дата резерва
    Reserve_days = Column(Integer, nullable=True)  # Дни резерва
    Purchase_doc = Column(String, nullable=True)  # Док Поставки (из обеих)
    Purchase_date = Column(sqlalchemy.Date(), nullable=True)  # Дата Поставки (из обеих)
    Order = Column(String)  # Order N Поставки (из обеих)
    k_Movement = Column(Numeric)  # к_Транспорт (перемещ), л (из обеих)
    k_Storage = Column(Numeric)  # к_Хранение, л (из обеих)
    k_Money = Column(Numeric)  # к_Ст-ть Денег, л (из обеих)
    
    # Внешние ключи
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_temp_sales_orders_doctype'))
    Customer_id = Column(String, ForeignKey('customers.id', name='fk_temp_sales_orders_customer'), nullable=True)
    Material_id = Column(String, ForeignKey('material.Code', name='fk_temp_sales_orders_material'))
    Contract_id = Column(String, ForeignKey('contracts.id', name='fk_temp_sales_orders_contract'), nullable=True)
    Supplier_id = Column(String, ForeignKey('suppliers.id', name='fk_temp_sales_orders_supplier'), nullable=True)
    Manager_id = Column(Integer, ForeignKey('managers.id', name='fk_temp_sales_orders_managers'))
    
    # Связи
    doc_type = relationship("DOCType", back_populates="temp_sales_orders")
    customer = relationship("Customer", back_populates="temp_sales_orders")
    material = relationship("Materials", back_populates="temp_sales_orders")
    contract = relationship("Contract", back_populates="temp_sales_orders")
    supplier = relationship("Supplier", back_populates="temp_sales_orders")
    manager = relationship("Manager", back_populates="temp_sales_orders")


class Purchase_Order(Base):
    __tablename__ = 'purchase_orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Status = Column(String)  # Статус
    Date = Column(sqlalchemy.Date())  # Дата
    Document = Column(String)  # Документ
    Supplier1 = Column(String)  # Supplier 1
    Supplier2 = Column(String)  # Supplier 2
    Order = Column(String)  # Order N
    Shipment = Column(String)  # Shipment #
    VAT = Column(String)  # % НДС
    Currency = Column(String)  # Валюта
    Qty = Column(Numeric)  # Количество
    Amount_1C = Column(Numeric)  # Сумма 1С
    Price_1C = Column(Numeric)  # Цена 1С
    Qty_pcs = Column(Numeric)  # Кол-во, шт
    Qty_lt = Column(Numeric)  # Кол-во, л
    Payment_FX = Column(Numeric)  # Курс оплаты
    Price_pcs_Curr = Column(Numeric)  # Цена шт, у.е.
    Price_lt_Curr = Column(Numeric)  # Цена л, у.е.
    Price_wo_VAT_Rub = Column(Numeric)  # Цена без НДС, руб/л
    Amount_wo_VAT_Rub = Column(Numeric)  # Сумма без НДС, руб
    Transport_mn = Column(Numeric)  # Транспорт м.н.
    Customs_fee = Column(Numeric)  # Тамож. Пошлина
    Customs_docs = Column(Numeric)  # Тамож. оформление
    Bank_fee = Column(Numeric)  # Комиссия банка
    Agency = Column(Numeric)  # Агентские
    Add_Services = Column(Numeric)  # Доп услуги
    ED = Column(Numeric)  # Акциз
    Eco_fee = Column(Numeric)  # ЭкоСбор
    Movement_fee = Column(Numeric)  # Перемещ
    Load_Unload = Column(Numeric)  # Погрузка/Выгрузка
    LPC_purchase_lt = Column(Numeric)  # Себ-ть л
    LPC_purchase_pcs = Column(Numeric)  # Себ-ть шт
    LPC_purchase_amount = Column(Numeric)  # Себ-ть партии
    Qty_after_spec_order = Column(Numeric)  # Кол-во после спец поставки
    LPC_purchase_after_spec_order = Column(Numeric)  # Себ-ть партии после спец поставки
    
    # Внешние ключи
    Supplier_id = Column(String, ForeignKey('suppliers.id', name='fk_purchase_orders_supplier'))  # Контрагент.Код
    Material_id = Column(String, ForeignKey('material.Code', name='fk_purchase_orders_material'))  # Код
    DocType_id = Column(Integer, ForeignKey('doc_type.id', name='fk_purchase_orders_doctype'))  # Тип документа
    AddSupplCost_id = Column(Integer, ForeignKey('add_suppl_cost.id', name='fk_purchase_orders_addsupplcost'), nullable=True)  # Связь с AddSupplCost
    
    # Связи
    supplier = relationship("Supplier", back_populates="purchase_orders")
    material = relationship("Materials", back_populates="purchase_orders")
    doc_type = relationship("DOCType", back_populates="purchase_orders")
    add_suppl_cost = relationship("AddSupplCost", back_populates="purchase_orders")


    __table_args__ = (
        
        Index('idx_purchase_order_supplier', 'Supplier_id'),
        Index('idx_purchase_order_material', 'Material_id'),
    )

class Delivery_to_Customer_24(Base):
    __tablename__ = 'delivery_to_customer_24'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Customer_name = Column(String)  # Контрагент
    Delivery_date = Column(sqlalchemy.Date())  # Дата отгр
    Bill = Column(String)  # Счет
    Customer_in_logist = Column(String)  # Наименование Клиента
    INN = Column(String)  # ИНН клиента
    Carrier = Column(String)  # Перевозчик
    Sborka = Column(String)  # Задание на сборку.Номер
    Delivery_method = Column(String)  # Способ доставки
    Delivery_amount_w_VAT = Column(Numeric)  # Ставка, руб (с НДС 20%)
    Delivery_amount_wo_VAT = Column(Numeric)  # Ставка без НДС
    Order_volume = Column(Numeric)  # Объем заказа, л
    Comment = Column(String)  # Комментарий
    OZON = Column(String)  # ОЗОН
    TS = Column(String)  # ТС
    CD_per_lt = Column(Numeric)  # Ставка р/л
    new_Amount = Column(Numeric)  # new_Ставка
    check_Deliv_amount = Column(String)  # true/false (ставка)
    inv_Volume = Column(Numeric)  # Объем СФ
    check_Inv_volume = Column(String)  # true/false (объем)
    Invoice = Column(String)  # СФ
    Invoice_date = Column(sqlalchemy.Date(), nullable=True)  # Дата сф
    Year_delivery = Column(Integer)  # Год отгр
    Bill_and_Date = Column(String)  # Счет & Дата

    __table_args__ = (
        Index('idx_delivery24_customer_name', 'Customer_name'),
        Index('idx_delivery24_delivery_date', 'Delivery_date'),
        Index('idx_delivery24_bill', 'Bill'),
        Index('idx_delivery24_sborka', 'Sborka'),
        Index('idx_delivery24_bill_sborka', 'Bill', 'Sborka'),
        Index('idx_delivery24_inn', 'INN'),
    )

class Delivery_to_Customer(Base):
    __tablename__ = 'delivery_to_customer'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Customer_name = Column(String)  # Контрагент
    Delivery_date = Column(sqlalchemy.Date())  # Дата отгр
    Bill = Column(String)  # Счет
    Customer_in_logist = Column(String)  # Наименование Клиента
    INN = Column(String)  # ИНН клиента
    Carrier = Column(String)  # Перевозчик
    Sborka = Column(String)  # Задание на сборку.Номер
    Delivery_method = Column(String)  # Способ доставки
    Delivery_amount_w_VAT = Column(Numeric)  # Ставка, руб (с НДС 20%)
    Delivery_amount_wo_VAT = Column(Numeric)  # Ставка без НДС
    Order_volume = Column(Numeric)  # Объем заказа, л
    Comment = Column(String)  # Комментарий
    OZON = Column(String)  # ОЗОН
    TS = Column(String)  # ТС
    CD_per_lt = Column(Numeric)  # Ставка р/л
    new_Amount = Column(Numeric)  # new_Ставка
    check_Deliv_amount = Column(String)  # true/false (ставка)
    inv_Volume = Column(Numeric)  # Объем СФ
    check_Inv_volume = Column(String)  # true/false (объем)
    Invoice = Column(String)  # СФ
    Invoice_date = Column(sqlalchemy.Date(), nullable=True)  # Дата сф
    Year_delivery = Column(Integer)  # Год отгр
    Bill_and_Date = Column(String)  # Счет & Дата
    new_Comment = Column(String)
    
    __table_args__ = (
        Index('idx_delivery_customer_name', 'Customer_name'),
        Index('idx_delivery_delivery_date', 'Delivery_date'),
        Index('idx_delivery_bill', 'Bill'),
        Index('idx_delivery_sborka', 'Sborka'),
        Index('idx_delivery_bill_sborka', 'Bill', 'Sborka'),
        Index('idx_delivery_inn', 'INN'),
    )

class Commission(Base):
    __tablename__ = 'commission'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Com_status = Column(String)  # Com status
    Start_date = Column(sqlalchemy.Date(), nullable=True)  # Дата начала
    End_date = Column(sqlalchemy.Date(), nullable=True)  # Дата окончания
    Comm_perc = Column(Numeric, nullable=True)  # Комм %
    Comm_rub = Column(Numeric, nullable=True)  # Комм Руб
    Comm_Cost_perc = Column(Numeric, nullable=True)  # Ст-ть ком-ии, %
    Comm_Cost_rub = Column(Numeric, nullable=True)  # Ст-ть ком-ии, Руб
    Document = Column(String)  # Документ
    Date = Column(sqlalchemy.Date(), nullable=True)  # Дата
    Bill = Column(String)  # Счет
    Bill_date = Column(sqlalchemy.Date(), nullable=True)  # Дата счета
    Litres_from = Column(Numeric, nullable=True)  # л от
    Litres_to = Column(Numeric, nullable=True)  # л до
    Recipient_code = Column(String)  # Грузополучатель.Код
    Recipient = Column(String)  # Грузополучатель
    Hyundai_code = Column(String)  # Код дилера
    Comment = Column(String)  # Комментарий
    
    # Внешние ключи
    Customer_id = Column(String, ForeignKey('customers.id', name='fk_commission_customer'))  # Контрагент.Код
    Material_id = Column(String, ForeignKey('material.Code', name='fk_commission_material'))  # Артикул
    Product_group_id = Column(String, ForeignKey('product_group.id', name='fk_commission_product_group'))  # Product name
    
    # Связи
    customer = relationship("Customer", back_populates="commissions")
    material = relationship("Materials", back_populates="commissions")
    product_group = relationship("Product_Group", back_populates="commissions")










from sqlalchemy.orm import configure_mappers
configure_mappers()
