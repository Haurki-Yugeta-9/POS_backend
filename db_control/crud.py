# unname() error回避
import platform
print("platform", platform.uname())

#ライブラリのインポート
from sqlalchemy import create_engine, insert, delete, update, select
from sqlalchemy.orm import Session, sessionmaker
import json
import pandas as pd
from db_control.connect import engine
from db_control.mymodels import Product, Transaction, TransactionDetail


# 商品マスタの検索
def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.CODE==code).first()


# 取引テーブルの登録
def create_transaction(db: Session, emp_cd: str = '9999999999') -> Transaction:
    new_transaction = Transaction(EMP_CD=emp_cd)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# 取引明細テーブルへの登録から合計金額の算出
def add_transaction_details(db: Session, trd_id: int, items: list[dict]):
    total_amt = 0
    for i, item in enumerate(items, start=1):
        detail = TransactionDetail(
            TRD_ID=trd_id,
            DTL_ID=i,
            PRD_ID=item["PRD_ID"],
            PRD_CODE=item["CODE"],
            PRD_NAME=item["NAME"],
            PRD_PRICE=item["PRICE"]
        )
        db.add(detail)
        total_amt += item["PRICE"]
    
    db.query(Transaction).filter(Transaction.TRD_ID == trd_id).update({"TOTAL_AMT": total_amt})
    db.commit()
    return total_amt

