from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Text
from sqlalchemy.orm import relationship

from db import Base, engine


class TeamLead(Base):
    __tablename__ = 'teamlead'

    id = Column(Integer, primary_key=True)
    TeamLead = Column(String, unique=True, nullable=False)
    email = Column(String)


class STL(Base):
    __tablename__ = 'stl'

    id = Column(Integer, primary_key=True)
    STL = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, default=False)


class Manager(Base):
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True)
    AM = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, nullable=False)
    Report = Column(String)

    STL_id = Column(Integer, ForeignKey(STL.id), index=True)
    TeamLead_id = Column(Integer, ForeignKey(TeamLead.id), index=True)

    STL_Table = relationship('STL', backref="AM_Table")
    TeamLead_Table = relationship('TeamLead', )


class Manager_Prev(Base):
    __tablename__ = 'manager_prev'

    id = Column(Integer, primary_key=True)
    AM_prev = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, nullable=False)
    Report = Column(String)

    STL_id = Column(Integer, ForeignKey(STL.id), index=True)
    TeamLead_id = Column(Integer, ForeignKey(TeamLead.id), index=True)

    STL_prev_Table = relationship('STL', backref="AM_prev_Table")
    TeamLead_Table = relationship('TeamLead')


class Sector(Base):
    __tablename__ = 'sector'

    id = Column(Integer, primary_key=True)
    Sector = Column(String, index=True, unique=True, nullable=False)


class Holding(Base):
    __tablename__ = 'holding'

    id = Column(Integer, primary_key=True)
    Holding = Column(String, index=True, unique=True, nullable=False)
    AM_id = Column(Integer, ForeignKey(Manager.id), index=True)
    AM_prev_id = Column(Integer, ForeignKey(Manager_Prev.id), index=True)
    Sector_id = Column(Integer, ForeignKey(Sector.id), index=True)
    
    AM_Table = relationship('Manager')
    AM_prev_Table = relationship('Manager_Prev')
    Sector_Table = relationship('Sector')


class Customer(Base):
    __tablename__ = 'сustomer'

    id = Column(Text, primary_key=True)
    Customer_Name = Column(String)
    INN = Column(String)
    Holding_id = Column(Integer, ForeignKey(Holding.id), index=True)
    Status = Column(String)
    PriceList = Column(String)
    Delivery = Column(String)

    Holding_Table = relationship('Holding')
    
    
class Cust_Plans(Base):
    __tablename__ = 'cust_plans'

    id = Column(Integer, primary_key=True)
    merge = Column(String)
    Year = Column(Integer)
    Quarter = Column(Integer)
    Month = Column(Integer)
    Holding_id = Column(Integer, ForeignKey(Holding.id), index=True)
    
    Volume_target = Column(Numeric)
    Margin_target = Column(Numeric)
    

class Comp_Plans(Base):
    __tablename__ = 'comp_plans'

    id = Column(Integer, primary_key=True)
    merge = Column(String)
    Year = Column(Integer)
    Quarter = Column(Integer)
    Month = Column(Integer)
    Week_of_Year = Column(Integer)
    TeamLead_id = Column(Integer, ForeignKey(TeamLead.id), index=True)
    Prod_cat = Column(String)
    
    Volume_Target_total = Column(Numeric)
    Revenue_Target_total = Column(Numeric)
    Margin_Target_total = Column(Numeric)
    
    TeamLead_Table = relationship('TeamLead')
    

class Material(Base):
    __tablename__ = 'material'

    id = Column(Text, primary_key=True, index=True, unique=True, nullable=False)
    prod_art = Column(String, index=True)
    prod_art_for_price = Column(String, index=True)
    Material_Name = Column(String, nullable=False)
    Product_Name = Column(String)
    Type = Column(String)
    Category = Column(String)
    Brand = Column(String)
    Family = Column(String)
    UoM = Column(String)
    UoM_1C = Column(String)
    Pack_type = Column(String)
    Pack_for_name = Column(Numeric)
    Pack = Column(Numeric)
    Pack_qty = Column(Numeric)
    ED_type = Column(String)
    Ecofee_type = Column(String)
    Density = Column(Numeric)
    Net_Weight = Column(Numeric)
    Pack_weight = Column(Numeric)
    Gross_weight = Column(Numeric)
    TNVED = Column(String)
    Cntr_of_origin = Column(String)
    Stock_strategy = Column(String)
    Status = Column(String)
    Full_name = Column(String)
    Material_Name_engl = Column(String)
    Comment = Column(String)
    ABC = Column(String)


class Supplier(Base):
    __tablename__ = 'supplier'
    
    id = Column(Text, primary_key=True)
    Supplier_Name = Column(String)
    Imp_Loc = Column(String)
    
    
class TaxFee(Base):
    __tablename__ = 'taxfee'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String)
    Year = Column(Integer)
    Month = Column(Integer)
    ED = Column(Numeric)
    Cust_docs = Column(Numeric)
    Bank_fee = Column(Numeric)
    Moving = Column(Numeric)
    Storing = Column(Numeric)
    Money = Column(Numeric)
    Add_money = Column(Numeric)
    
class EcoFee_amount(Base):
    __tablename__ = 'ecofee_amount'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String)
    TNVED = Column(String)
    Year = Column(Integer)
    Amount = Column(Numeric)
    
    
class EcoFee_standard(Base):
    __tablename__ = 'ecofee_standard'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String)
    TNVED = Column(String)
    Year = Column(Integer)
    Standard = Column(Numeric)


class DOCType(Base):
    __tablename__ = 'doctype'
    
    id = Column(Integer, primary_key=True)
    merge = Column(String)
    Document = Column(String)
    Transaction = Column(String)
    Doc_type = Column(String)
    

class HYUNDAI(Base):
    __tablename__ = 'hyundai'
    
    id = Column(Integer, primary_key=True)
    HYUNDAI_id = Column(String)
    Hyu_code = Column(String)
    Dealer_Name = Column(String)
    City = Column(String)
    INN = Column(String)
    AM_id = Column(Integer, ForeignKey(Manager.id), index=True)
    
    AM_Table = relationship('Manager')
    