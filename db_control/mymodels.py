#ライブラリのインポート
from sqlalchemy import String, Integer, CHAR, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


#DeclarativeBase
class Base(DeclarativeBase):
    pass

#商品マスタDB
class Product(Base):
    __tablename__ = "product_master"
    PRD_ID: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    CODE: Mapped[str]= mapped_column(CHAR(13), unique=True)
    NAME: Mapped[str]= mapped_column(String(50))
    PRICE: Mapped[int]= mapped_column()

#取引DB
class Transaction(Base):
    __tablename__ = "transactions"
    TRD_ID: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    DATETIME: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    EMP_CD: Mapped[str]= mapped_column(CHAR(10), default='9999999999')
    STORE_CD: Mapped[str]= mapped_column(CHAR(5), default='30')
    POS_NO: Mapped[str]= mapped_column(CHAR(3), default='90')
    TOTAL_AMT: Mapped[int]= mapped_column(default=0)
    
#取引明細DB
class TransactionDetail(Base):
    __tablename__ = "transaction_details"
    TRD_ID: Mapped[int]= mapped_column(ForeignKey("transactions.TRD_ID"), primary_key=True)
    DTL_ID: Mapped[int]= mapped_column(primary_key=True)
    PRD_ID: Mapped[int]= mapped_column(ForeignKey("product_master.PRD_ID"))
    PRD_CODE: Mapped[str]= mapped_column(CHAR(13))
    PRD_NAME: Mapped[str]= mapped_column(String(50))
    PRD_PRICE: Mapped[int]= mapped_column()

