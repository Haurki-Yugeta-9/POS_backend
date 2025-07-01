# ライブラリのインポート
from sqlalchemy import Column, Integer, String, DateTime, CHAR
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemyのBaseクラスを定義（全モデルの親になる）
Base = declarative_base()

# 商品マスタテーブル（商品情報を保持）
class ProductMaster(Base):
    __tablename__ = 'product_master'  # テーブル名：product_master

    PRD_ID = Column(Integer, primary_key=True, index=True)       # 商品一意ID（主キー）
    CODE = Column(String(25), unique=True, nullable=False)       # 商品コード（JANコードなど）
    NAME = Column(String(50), nullable=False)                    # 商品名
    PRICE = Column(Integer, nullable=False)                      # 税込価格（単位は円）

# 取引テーブル（購入1回分のまとめ情報）
class Transaction(Base):
    __tablename__ = 'transactions'  # テーブル名：transactions

    TRD_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 取引ID（主キー、自動採番）
    DATETIME = Column(DateTime, nullable=False)             # 取引日時
    EMP_CD = Column(CHAR(10), nullable=False)               # 従業員コード（固定10桁）
    STORE_CD = Column(CHAR(5), nullable=False)              # 店舗コード（固定5桁）
    POS_NO = Column(CHAR(3), nullable=False)                # POS端末番号（固定3桁）
    TOTAL_AMT = Column(Integer, nullable=False, default=0)  # 合計金額（税込）
    TTL_AMT_EX_TAX = Column(Integer, nullable=False, default=0)  # 合計金額（税抜）

# 取引明細テーブル（購入1件ごとの商品情報）
class TransactionDetail(Base):
    __tablename__ = 'transaction_details'  # テーブル名：transaction_details

    TRD_ID = Column(Integer, primary_key=True)              # 外部キー：取引ID（親テーブルと対応）
    DTL_ID = Column(Integer, primary_key=True)              # 明細番号（1, 2, 3,...）※複合主キー
    PRD_ID = Column(Integer, nullable=False)                # 商品ID（ProductMasterと紐づける）
    PRD_CODE = Column(CHAR(13), nullable=False)             # 商品コード（JANコードなど）
    PRD_NAME = Column(String(50), nullable=False)           # 商品名
    PRD_PRICE = Column(Integer, nullable=False)             # 商品価格（税込）
    TAX_CD = Column(CHAR(2), nullable=False)                # 税コード（例: '10' = 10%）
