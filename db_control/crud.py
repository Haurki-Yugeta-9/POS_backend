# Lv2
# ライブラリのインポート
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
import logging
from .mymodels import ProductMaster, Transaction, TransactionDetail
from .schemas import ProductBase, TransactionCreate, ItemCreate

# ロガーの設定
logger = logging.getLogger("db_crud")

# 商品マスタの検索
def get_product_by_code(db:Session, product_code:str):
    try:
        logger.info(f"商品コード`{product_code}`のデータベース検索を開始します")
        # SQLAlchemyのORMで検索
        product = db.query(ProductMaster).filter(ProductMaster.CODE==product_code).first()

        if product:
            logger.info(f"商品コード`{product_code}`の商品を見つけました: {product.NAMW}")
            return product
        
        # ORMで見つからない場合、直接SQLを試行
        logger.warning(f"ORM検索で商品コード`{product_code}`の商品が見つかりませんでした。SQLを試行します")
        # 文字列の前後のスペースを削除
        triming_code = product_code.strip()
        # SQLを使用
        result = db.execute(
            text(f"SELECT * FROM PRODUCT_MASTER WHERE CODE = :code OR CODE = :triming_code"),
            {"code":product_code, "triming_code": triming_code}
        )

        row = result.fetchone()
        if row:
            logger.info(f"直接SQLで商品コード`{product_code}`の商品を見つけました")
            product = ProductMaster(
                PRD_ID = row.PRD_ID,
                CODE = row.CODE,
                NAME = row.NAME,
                PRICE = row.PRICE
            )
            return product
        
        # それでも見つからない場合、デバック情報を記録
        logger.warning(f"商品コード`{product_code}`の商品はデータベースに存在しません")
        
        # 登録商品コードのサンプルを取得（デバック用）
        sample_result = db.execute(text("SELECT CODE FROM PRODUCT_MASTER LIMIT 5"))
        sample_code = [row[0] for row in sample_result.fetchall()]

        if sample_code:
            logger.info(f"データベースに登録されている商品コード例：{str(e)}", exc_info=True)
        else:
            logger.warning("データベースに商品が登録されていません")
        return None
    except Exception as e:
        logger.error(f"商品コード`{product_code}`の検索中にエラーが発生しました：{str(e)}", exc_info=True)
        raise


# 取引テーブルと取引明細テーブルの登録
def create_transaction(db: Session, transaction_data: TransactionCreate):
    # 取引テーブルへの登録
    db_transaction = Transaction(
        EMP_CD = transaction_data.emp_cd,   #schemasでデフォルト値設定
        # DATETIMEはDB側で自動設定
        # STORE_CD, POS_NOはmymodelsのデフォルト値設定
        # TOTAL_AMT, TOTAL_AMT_EX_TAXは後ろで更新
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    trd_id = db_transaction.TRD_ID

    # 取引明細テーブルへの登録
    total_amt_ex_tax = 0
    dtl_id_counter = 1      #DTL_IDをTRD_IDごとに1から採番
    for item in transaction_data.items:
        # item.prd_codeを使ってProductMasterからPRD_IDを取得
        product_master_entry = get_product_by_code(db, product_code=item.prd_code)
        if not product_master_entry:
            raise HTTPException(status_code=404, detail=f"商品コード {item.prd_code} がマスタ内に見つかりません")

        db_transaction_detail = TransactionDetail(
            TRD_ID = trd_id,
            DTL_ID = dtl_id_counter,
            PRD_ID = product_master_entry.PRD_ID,
            PRD_CODE = item.prd_code,
            PRD_NAME = item.prd_name,
            PRD_PRICE = item.prd_price,
            QUANTITY = item.quantity,
            # TAX_CDはmymodelsのデフォルト値設定
        )
        db.add(db_transaction_detail)
        ttl_amt_ex_tax += (item.prd_price * item.quantity)
        dtl_id_counter += 1
    db.commit()

    #合計金額、税抜金額の計算
    tax = round(ttl_amt_ex_tax*0.10)
    total_amt = ttl_amt_ex_tax + tax

    # 取引テーブルの更新
    db_transaction.TOTAL_AMT = total_amt
    db_transaction.TTL_AMT_EX_TAX = ttl_amt_ex_tax
    db.commit()
    db.refresh(db_transaction)

    return db_transaction, total_amt, ttl_amt_ex_tax 











# # Lv1
# # unname() error回避
# import platform
# print("platform", platform.uname())

# #ライブラリのインポート
# from sqlalchemy import create_engine, insert, delete, update, select
# from sqlalchemy.orm import Session, sessionmaker
# import json
# import pandas as pd
# from db_control.connect import engine
# from db_control.mymodels import Product, Transaction, TransactionDetail


# # 商品マスタの検索
# def get_product_by_code(db: Session, code: str):
#     return db.query(Product).filter(Product.CODE==code).first()


# # 取引テーブルの登録
# def create_transaction(db: Session, emp_cd: str = '9999999999') -> Transaction:
#     new_transaction = Transaction(EMP_CD=emp_cd)
#     db.add(new_transaction)
#     db.commit()
#     db.refresh(new_transaction)
#     return new_transaction

# # 取引明細テーブルへの登録から合計金額の算出
# def add_transaction_details(db: Session, trd_id: int, items: list[dict]):
#     total_amt = 0
#     for i, item in enumerate(items, start=1):
#         detail = TransactionDetail(
#             TRD_ID=trd_id,
#             DTL_ID=i,
#             PRD_ID=item["PRD_ID"],
#             PRD_CODE=item["CODE"],
#             PRD_NAME=item["NAME"],
#             PRD_PRICE=item["PRICE"]
#         )
#         db.add(detail)
#         total_amt += item["PRICE"]
    
#     db.query(Transaction).filter(Transaction.TRD_ID == trd_id).update({"TOTAL_AMT": total_amt})
#     db.commit()
#     return total_amt

