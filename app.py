# ライブラリのインポート
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from db_control.mymodels import Base, Product, Transaction, TransactionDetail
from db_control.crud import get_product_by_code, create_transaction, add_transaction_details
from db_control.connect import SessionLocal
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
import requests
import json
import uuid


# MySQLテーブル作成
from db_control.create_tables import init_db

#アプリケーション初期化時にテーブル作成
init_db()


# アプリの設定
app = FastAPI()


# CORSMiddlewareの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DBセッション管理
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# トップページ用ルート確認
@app.get("/")
def root():
    return{"message": "POS backend is running"}


# 商品検索エンドポイント
@app.get("/product")
def product_search(code: str, db: Session = Depends(get_db)):
    product = get_product_by_code(db, code)
    if not product:
        return None
    return{
        "PRD_ID":product.PRD_ID,
        "CODE":product.CODE,
        "NAME":product.NAME,
        "PRICE":product.PRICE,
    }


#購入処理エンドポイント
@app.post("/purchase")
def purchase(emp_cd: str, items: list[dict], db: Session= Depends(get_db)):
    transaction = create_transaction(db, emp_cd)
    total = add_transaction_details(db, transaction.TRD_ID, items)
    return {"success":True, "total": total}
 