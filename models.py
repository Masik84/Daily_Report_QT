
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import CheckConstraint

from db import Base, engine


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True)
    Manager_name = Column(String)
    Email = Column(String)
    AM_1C_Name = Column(String)
    Has_report = Column(String)  # 'да' или 'нет'
    Report_link = Column(String)

    # Внешние ключи
    STL_id = Column(Integer, ForeignKey('stls.id', name='fk_manager_stl'))
    TeamLead_id = Column(Integer, ForeignKey('team_leads.id', name='fk_manager_teamlead'))

    # Связи
    stl = relationship("STL", back_populates="managers")
    team_lead = relationship("TeamLead", back_populates="managers")
    contracts = relationship("Contract", back_populates="manager")  # мн. число
    hyundai_dealers = relationship("Hyundai_Dealer", back_populates="manager")  # мн. число
    customer_plans = relationship("CustomerPlan", back_populates="manager")


class STL(Base):
    __tablename__ = 'stls'

    id = Column(Integer, primary_key=True)
    STL_name = Column(String)
    Email = Column(String)
    Report_link = Column(String)

    managers = relationship("Manager", back_populates="stl")
    customer_plans = relationship("CustomerPlan", back_populates="stl")


class TeamLead(Base):
    __tablename__ = 'team_leads'

    id = Column(Integer, primary_key=True)
    TeamLead_name = Column(String)
    Email = Column(String)
    Has_report = Column(String)  # 'да' или 'нет'
    Report_link = Column(String)

    managers = relationship("Manager", back_populates="team_lead")
    company_plans = relationship("CompanyPlan", back_populates="team_lead")
    customer_plans = relationship("CustomerPlan", back_populates="team_lead")


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True)  # КонтрагентКод (например "ОП-041205")
    Customer_name = Column(String)
    INN = Column(String)
    Price_type = Column(String)

    Sector_id = Column(Integer, ForeignKey('sectors.id', name='fk_customer_sector'))
    Holding_id = Column(Integer, ForeignKey('holdings.id', name='fk_customer_holding'))

    # Связи
    sector = relationship("Sector", back_populates="customers")
    holding = relationship("Holding", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")


class Holding(Base):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True)
    Holding_name = Column(String, unique=True, nullable=False)  # Название холдинга

    customers = relationship("Customer", back_populates="holding")
    customer_plans = relationship("CustomerPlan", back_populates="holding")


class Sector(Base):
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True)
    Sector_name = Column(String, unique=True, nullable=False)

    customers = relationship("Customer", back_populates="sector")
    customer_plans = relationship("CustomerPlan", back_populates="sector")


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
    manager = relationship("Manager", back_populates="contracts")  # ед. число


class Hyundai_Dealer(Base):
    __tablename__ = 'hyundai_dealers'

    id = Column(Integer, primary_key=True)  # Внутренний ID (автоинкремент)
    Dealer_code = Column(String, nullable=True, unique=True)  # "Код дилера HYUNDAI" (может быть NULL)
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

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)  # ТН ВЭД код

    # Связи
    product_groups = relationship("Product_Group", back_populates="tnved")
    ecofee_amounts = relationship("EcoFee_amount", back_populates="tnved")
    ecofee_standards = relationship("EcoFee_standard", back_populates="tnved")
    customs_rates = relationship("Customs_Rate", back_populates="tnved")


class Product_Group(Base):
    __tablename__ = 'product_group'

    id = Column(String, primary_key=True)  # Код группы
    Product_name = Column(String)  # Product name
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_product_group_tnved'))  # Ссылка на ТН ВЭД

    # Связи
    tnved = relationship("TNVED", back_populates="product_groups")
    product_names = relationship("Product_Names", back_populates="product_group")


class Product_Names(Base):
    __tablename__ = 'product_names'

    id = Column(Integer, primary_key=True)
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
    Family = Column(String)
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
    Status = Column(String)

    Product_Names_id = Column(Integer, ForeignKey('product_names.id', name='fk_materials_product_names'))

    # Связи
    product_name = relationship("Product_Names", back_populates="materials")


class ABC_list(Base):
    __tablename__ = 'abc_list'

    id = Column(Integer, primary_key=True)
    ABC_category = Column(String(10), unique=True, nullable=False)  # 'A', 'B', 'C', 'D'

    # Связи
    abc_cat = relationship("ABC_cat", back_populates="abc_list")  # Изменили с abc_records на abc_cat
    company_plans = relationship("CompanyPlan", back_populates="ABC_category")


class ABC_cat(Base):
    __tablename__ = 'abc_cat'

    id = Column(Integer, primary_key=True)
    product_name_id = Column(Integer, ForeignKey('product_names.id', name='fk_abc_cat_product_names'))
    abc_list_id = Column(Integer, ForeignKey('abc_list.id', name='fk_abc_cat_abc_list'))
    Start_date = Column(Date)
    End_date = Column(Date)

    # Связи
    product_name = relationship("Product_Names", back_populates="abc_cat")
    abc_list = relationship("ABC_list", back_populates="abc_cat")


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(String, primary_key=True)
    Supplier_Name = Column(String)
    Imp_Loc = Column(String)
    Customs = Column(String)


class EcoFee_amount(Base):  # экосбор_ставки
    __tablename__ = 'ecofee_amount'

    id = Column(Integer, primary_key=True)
    merge = Column(String, unique=True)
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_ecofee_amount_tnved'))
    year_id = Column(Integer, ForeignKey('years.id', name='fk_ecofee_amount_year'))
    ECO_amount = Column(Numeric)

    tnved = relationship("TNVED", back_populates="ecofee_amounts")
    year = relationship("Year", back_populates="ecofee_amounts")


class EcoFee_standard(Base):  # экосбор_норматив
    __tablename__ = 'ecofee_standard'

    id = Column(Integer, primary_key=True)
    merge = Column(String, unique=True)
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_ecofee_standard_tnved'))
    year_id = Column(Integer, ForeignKey('years.id', name='fk_ecofee_standard_year'))
    ECO_standard = Column(Numeric)

    tnved = relationship("TNVED", back_populates="ecofee_standards")
    year = relationship("Year", back_populates="ecofee_standards")


class Customs_Rate(Base):
    __tablename__ = 'customs_rate'

    id = Column(Integer, primary_key=True)
    # merge = Column(String, unique=True) #Убрал unique=True т.к. в задании сказано, что может быть несколько записей с одинаковым кодом
    TNVED_id = Column(Integer, ForeignKey('tnved.id', name='fk_customs_rate_tnved'))
    Cust_rate = Column(Numeric(5, 4))  #  Изменил Numeric(5, 2) на Numeric(5, 4)

    tnved = relationship("TNVED", back_populates="customs_rates")

    def __repr__(self):
        return f"<Customs_Rate(TNVED_id={self.TNVED_id}, Cust_rate={self.Cust_rate})>"


class Fees(Base):
    __tablename__ = 'taxfee'

    __table_args__ = (
        UniqueConstraint('year_id', 'month_id', name='uq_year_month'),  # Уникальность по году и месяцу
    )

    id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey('years.id', name='fk_fees_year'))  # Ссылка на год
    month_id = Column(Integer, ForeignKey('months.id', name='fk_fees_month'))  # Ссылка на месяц
    Excise = Column(Numeric)  # Акциз
    Customs_clearance = Column(Numeric)  # Тамож. оформление
    Bank_commission = Column(Numeric)  # Комиссия банка
    Transportation = Column(Numeric)  # Транспорт (перемещ), л
    Storage = Column(Numeric)  # Хранение, л
    Money_cost = Column(Numeric)  # Ст-ть Денег
    Additional_money_percent = Column(Numeric)  # Доп% денег

    year = relationship("Year", back_populates="fees")
    month = relationship("Month", back_populates="fees")


class DOCType(Base):
    __tablename__ = 'doc_type'

    id = Column(Integer, primary_key=True)
    merge = Column(String)
    Document = Column(String)
    Transaction = Column(String)
    Doc_type = Column(String)


class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    Year = Column(Integer, unique=True, nullable=False)  # Год

    company_plans = relationship("CompanyPlan", back_populates="year")
    customer_plans = relationship("CustomerPlan", back_populates="year")
    calendar_entries = relationship("Calendar", back_populates="year")
    ecofee_amounts = relationship("EcoFee_amount", back_populates="year")
    ecofee_standards = relationship("EcoFee_standard", back_populates="year")
    fees = relationship("Fees", back_populates="year")


class Quarter(Base):
    __tablename__ = 'quarters'
    id = Column(Integer, primary_key=True)
    Quarter = Column(Integer, nullable=False)  # 1-4

    months = relationship("Month", back_populates="quarter")
    calendar_entries = relationship("Calendar", back_populates="quarter")


class Month(Base):
    __tablename__ = 'months'
    id = Column(Integer, primary_key=True)
    Month = Column(Integer, nullable=False)  # 1-12
    Quarter_id = Column(Integer, ForeignKey('quarters.id', name='fk_months_Quarter_id_quarters'), nullable=False)

    company_plans = relationship("CompanyPlan", back_populates="month")
    customer_plans = relationship("CustomerPlan", back_populates="month")
    quarter = relationship("Quarter", back_populates="months")
    calendar_entries = relationship("Calendar", back_populates="month")
    fees = relationship("Fees", back_populates="month")


class Week(Base):
    __tablename__ = 'weeks'
    id = Column(Integer, primary_key=True)
    Week_of_Year = Column(Integer, nullable=False)  # 1-53
    Week_of_Month = Column(Integer, nullable=False)  # 1-5

    company_plans = relationship("CompanyPlan", back_populates="week")
    customer_plans = relationship("CustomerPlan", back_populates="week")
    calendar_entries = relationship("Calendar", back_populates="week")


class Calendar(Base):
    __tablename__ = 'calendar'
    id = Column(Integer, primary_key=True)
    Day = Column(Date, nullable=False, unique=True)
    Year_id = Column(Integer, ForeignKey('years.id', name='fk_calendar_Year_id_years'), nullable=False)
    Quarter_id = Column(Integer, ForeignKey('quarters.id', name='fk_calendar_Quarter_id_quarters'), nullable=False)
    Month_id = Column(Integer, ForeignKey('months.id', name='fk_calendar_Month_id_months'), nullable=False)
    Week_id = Column(Integer, ForeignKey('weeks.id', name='fk_calendar_Week_id_weeks'), nullable=False)
    NETWORKDAYS = Column(Integer, nullable=False)

    year = relationship("Year", back_populates="calendar_entries")  # строчная 'year'
    quarter = relationship("Quarter", back_populates="calendar_entries")
    month = relationship("Month", back_populates="calendar_entries")
    week = relationship("Week", back_populates="calendar_entries")


class CompanyPlan(Base):
    __tablename__ = 'company_plans'
    id = Column(Integer, primary_key=True)
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
    
    id = Column(Integer, primary_key=True)
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


from sqlalchemy.orm import configure_mappers

configure_mappers()
