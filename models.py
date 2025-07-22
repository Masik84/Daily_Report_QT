from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, Date, Index, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property

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
    STL_id = Column(Integer, ForeignKey('stls.id'))
    TeamLead_id = Column(Integer, ForeignKey('team_leads.id'))
    
    # Связи
    STL = relationship("STL", back_populates="Managers")
    TeamLead = relationship("TeamLead", back_populates="Managers")
    Contracts = relationship("Contract", back_populates="Manager")
    Hyundai_Dealers = relationship("Hyundai_Dealer", back_populates="Manager")


class STL(Base):
    __tablename__ = 'stls'
    
    id = Column(Integer, primary_key=True)
    STL_name = Column(String)
    Email = Column(String)
    Report_link = Column(String)
    
    Managers = relationship("Manager", back_populates="STL")


class TeamLead(Base):
    __tablename__ = 'team_leads'
    
    id = Column(Integer, primary_key=True)
    TeamLead_name = Column(String)
    Email = Column(String)
    Has_report = Column(String)  # 'да' или 'нет'
    Report_link = Column(String)
    
    Managers = relationship("Manager", back_populates="TeamLead")


class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(String, primary_key=True)  # КонтрагентКод (например "ОП-041205")
    Customer_name = Column(String)
    INN = Column(String)
    Price_type = Column(String)
    
    # Внешние ключи
    Sector_id = Column(String, ForeignKey('sectors.Sector_name'))
    Holding_id = Column(Integer, ForeignKey('holdings.id'))
    
    # Связи
    Sector = relationship("Sector", back_populates="Customers")
    Holding = relationship("Holding", back_populates="Customers")
    Contracts = relationship("Contract", back_populates="Customer")
    
    
class Holding(Base):
    __tablename__ = 'holdings'
    
    id = Column(Integer, primary_key=True)
    Holding_name = Column(String, unique=True, nullable=False)  # Название холдинга
    
    Customers = relationship("Customer", back_populates="Holding")


class Sector(Base):
    __tablename__ = 'sectors'
    
    id = Column(Integer, primary_key=True)
    Sector_name = Column(String, unique=True, nullable=False)
    
    Customers = relationship("Customer", back_populates="Sector")


class Contract(Base):
    __tablename__ = 'contracts'
    
    id = Column(String, primary_key=True)  # ДоговорКод (например "ОП-002494")
    Contract = Column(String)
    Contract_Type = Column(String)  # "С покупателем"
    Price_Type = Column(String)
    Payment_Condition = Column(String)
    
    # Внешние ключи
    Customer_id = Column(String, ForeignKey('customers.id'))  # Контрагент.Код
    Manager_id = Column(Integer, ForeignKey('managers.id'))
    
    # Связи
    Customer = relationship("Customer", back_populates="Contracts")
    Manager = relationship("Manager", back_populates="Contracts")


class Hyundai_Dealer(Base):
    __tablename__ = 'hyundai_dealers'
    
    id = Column(Integer, primary_key=True)  # Внутренний ID (автоинкремент)
    Dealer_code = Column(String, nullable=True, unique=True)  # "Код дилера HYUNDAI" (может быть NULL)
    Hyundai_code = Column(String, unique=True, nullable=False)  # "Код в HYUNDAI" (обязателен)
    Name = Column(String)  # "Наим дилера HYUNDAI"
    City = Column(String)  # "Город"
    INN = Column(String)  # "ИНН"
    
    # Связь с менеджером
    Manager_id = Column(Integer, ForeignKey('managers.id'))
    Manager = relationship("Manager", back_populates="Hyundai_Dealers")
    

    # Уникальный индекс для случая, когда DealerCode есть
    # Определение индексов (без предупреждений)
    __table_args__ = (
        Index('idx_hyundai_code_unique', Hyundai_code, unique=True),
        Index('idx_dealer_code_unique', Dealer_code, unique=True),
    )
    
    @hybrid_property
    def HasDealerCode(self):
        return self.Dealer_code is not None
    

    
class Material(Base):
    __tablename__ = 'material'

    Code = Column(String, primary_key=True)
    Article = Column(String)
    Material_Name = Column(String, nullable=False, index=True)
    Full_name = Column(String)
    Brand = Column(String)
    Family = Column(String)
    Product_name = Column(String)
    Product_type = Column(String)
    UoM = Column(String)
    Report_UoM = Column(String)
    Package_type = Column(String)
    Items_per_Package = Column(Integer)
    Items_per_Set = Column(Integer)
    Package_Volume = Column(Numeric)
    Net_weight = Column(Numeric)
    Gross_weight = Column(Numeric)
    Density = Column(Numeric)
    TNVED = Column(String)
    Excise = Column(String)
    
    ABC = relationship("ABC_cat", back_populates="Material")


class ABC_cat(Base):
    __tablename__ = 'abc_cat'
    
    id = Column(Integer, primary_key=True)
    Product_name = Column(String, ForeignKey('material.Material_Name'))  # Связь по названию
    Start_date = Column(Date)
    End_date = Column(Date)
    ABC_category = Column(String)
    
    # Связь с материалом
    Material = relationship("Material", back_populates="ABC")


class Supplier(Base):
    __tablename__ = 'supplier'
    
    id = Column(String, primary_key=True)
    Supplier_Name = Column(String)
    Imp_Loc = Column(String)
    Customs = Column(String)
    
    
class TaxFee(Base):
    __tablename__ = 'taxfee'
    
    __table_args__ = (
        UniqueConstraint('Year', 'Month', name='uq_year_month'),  # Уникальность по году и месяцу
    )
    
    id = Column(Integer, primary_key=True)
    Year = Column(Integer)                  # Год
    Month = Column(Integer)                 # Месяц
    Excise = Column(Numeric)                # Акциз
    Customs_clearance = Column(Numeric)     # Тамож. оформление
    Bank_commission = Column(Numeric)       # Комиссия банка
    Transportation = Column(Numeric)        # Транспорт (перемещ), л
    Storage = Column(Numeric)               # Хранение, л
    Money_cost = Column(Numeric)            # Ст-ть Денег
    Additional_money_percent = Column(Numeric)  # Доп% денег
    
    
class EcoFee_amount(Base):
    __tablename__ = 'ecofee_amount'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String, unique=True)
    TNVED = Column(String)
    Year = Column(Integer)
    ECO_amount = Column(Numeric)
    
    
class EcoFee_standard(Base):
    __tablename__ = 'ecofee_standard'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String, unique=True)
    TNVED = Column(String)
    Year = Column(Integer)
    ECO_standard = Column(Numeric)


class Customs_Rate(Base):
    __tablename__ = 'customs_rate'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String, unique=True)
    TNVED = Column(String)
    Cust_rate = Column(Numeric(5, 2))
    

class DOCType(Base):
    __tablename__ = 'doc_type'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String)
    Document = Column(String)
    Transaction = Column(String)
    Doc_type = Column(String)
    













