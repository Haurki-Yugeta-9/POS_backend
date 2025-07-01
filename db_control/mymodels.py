# # render用に作り直すので一旦無視

# # LV2
# # ライブラリのインポート
# from sqlalchemy import Column, Integer, String, CHAR, ForeignKeyConstraint, TIMESTAMP, ForeignKey
# from sqlalchemy.sql import func
# from .connect import Base

# # 商品マスタテーブル
# class ProductMaster(Base):
#     __tablename__ = "product_master"
#     PRD_ID = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="商品一意キー")
#     CODE = Column(CHAR(16), unique=True, nullable=False, comment="商品JANコード（原則）")
#     NAME = Column(String(50), nullable=False, comment="商品名称")
#     PRICE = Column(Integer, nullable=False, comment="商品単価（税抜）")


# # 取引テーブル
# class Transaction(Base):
#     __tablename__ = "transactions"
#     TRD_ID = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="取引一意キー")
#     DATETIME = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="取引日時")
#     EMP_CD = Column(CHAR(10), nullable=False, server_default="9999999999", comment="レジ担当者コード")
#     STORE_CD = Column(CHAR(5), nullable=False, server_default="30", comment="店舗コード")
#     POS_NO = Column(CHAR(3), nullable=False, server_default="90", comment="POS機ID(90:モバイルレジ)")
#     TOTAL_AMT = Column(Integer, nullable=False, server_default="0", comment="合計金額（税込）")
#     TOTAL_AMT_EX_TAX = Column(Integer, nullable=False, server_default="0", comment="合計金額（税抜）")


# # 取引明細テーブル
# class TransactionDetail(Base):
#     __tablename__ = "transaction_detail"
#     TRD_ID = Column(Integer, primary_key=True, comment="取引一意キー")
#     DTL_ID = Column(Integer, primary_key=True, comment="取引明細一意キー")
#     PRD_ID = Column(Integer, nullable=False, comment="商品一意キー")
#     PRD_CODE = Column(CHAR(13), nullable=False, comment="商品JANコード")
#     PRD_NAME = Column(String(50), nullable=False, comment="商品名称")
#     PRD_PRICE = Column(Integer, nullable=False, comment="商品単価（税抜）")
#     QUANTITY = Column(Integer, nullable=False, default=1, comment="数量")
#     TAX_CD = Column(CHAR(2), nullable=False, server_default="10", comment="消費税区分（10:10%）")

#     __table_args__ =(
#         ForeignKeyConstraint(['TRD_ID'], ['transactions.TRD_ID']),
#         ForeignKeyConstraint(['PRD_ID'], ['product_master.PRD_ID']),
#     )



# # LV1
# # #ライブラリのインポート
# # from sqlalchemy import String, Integer, CHAR, TIMESTAMP, ForeignKey, DateTime, func
# # from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# # from datetime import datetime


# # #DeclarativeBase
# # class Base(DeclarativeBase):
# #     pass

# # #商品マスタDB
# # class Product(Base):
# #     __tablename__ = "product_master"
# #     PRD_ID: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
# #     CODE: Mapped[str]= mapped_column(CHAR(13), unique=True)
# #     NAME: Mapped[str]= mapped_column(String(50))
# #     PRICE: Mapped[int]= mapped_column()

# # #取引DB
# # class Transaction(Base):
# #     __tablename__ = "transactions"
# #     TRD_ID: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
# #     DATETIME: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
# #     EMP_CD: Mapped[str]= mapped_column(CHAR(10), default='9999999999')
# #     STORE_CD: Mapped[str]= mapped_column(CHAR(5), default='30')
# #     POS_NO: Mapped[str]= mapped_column(CHAR(3), default='90')
# #     TOTAL_AMT: Mapped[int]= mapped_column(default=0)
    
# # #取引明細DB
# # class TransactionDetail(Base):
# #     __tablename__ = "transaction_details"
# #     TRD_ID: Mapped[int]= mapped_column(ForeignKey("transactions.TRD_ID"), primary_key=True)
# #     DTL_ID: Mapped[int]= mapped_column(primary_key=True)
# #     PRD_ID: Mapped[int]= mapped_column(ForeignKey("product_master.PRD_ID"))
# #     PRD_CODE: Mapped[str]= mapped_column(CHAR(13))
# #     PRD_NAME: Mapped[str]= mapped_column(String(50))
# #     PRD_PRICE: Mapped[int]= mapped_column()


