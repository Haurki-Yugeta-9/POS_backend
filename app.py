# Lv2
# ライブラリのインポート
from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from db_control.router import router, read_product, create_transaction
from db_control.connect import engine, Base, get_db
from db_control.mymodels import ProductMaster, Transaction, TransactionDetail
from sqlalchemy.orm import Session
import os


app = FastAPI(
    title="POS API",
    description="ポップアップストア向け簡易POSシステムAPI",
    version="0.1.0"
)

# 許可するドメインリスト
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "https://app-step4-62.azurewebsites.net,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials= True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# セキュリティヘッダーを追加するミドルウェア
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# レート制限を実装するミドルウェア
@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    response = await call_next(request)
    return response

app.include_router(router, prefix="/api", tags=["Products"])
app.include_router(router, prefix="/api", tags=["Transactions"])

# トップページのエンドポイント
@app.get("/")
async def root():
    return {"message": "Welcome to POS API"}

# データベース接続テスト用のエンドポイント
@app.get("/api/test-db")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        # 最初の5つの商品を取得
        from db_control.crud import get_product_by_code
        result= []

        # 商品コードをいくつか試す
        test_codes = ["4901681328413", "490168531219", "490168531233"]
        for code in test_codes:
            product = get_product_by_code(db, code)
            if product:
                result.append({
                    "code": product.CODE,
                    "name": product.NAME,
                    "price": product.PRICE
                })
        
        return {
            "success": True,
            "message": "データベース接続は正常です",
            "products_found": len(result),
            "products": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"データベース接続エラー：{str(e)}"
        }

# 開発時のUvicornで実行用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




# # Lv1
# # ライブラリのインポート
# from fastapi import FastAPI, HTTPException, Query, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from db_control.mymodels import Base, Product, Transaction, TransactionDetail
# from db_control.crud import get_product_by_code, create_transaction, add_transaction_details
# from db_control.connect import SessionLocal
# from sqlalchemy.orm import Session, sessionmaker
# from pydantic import BaseModel
# import requests
# import json
# import uuid


# # MySQLテーブル作成
# from db_control.create_tables import init_db

# #アプリケーション初期化時にテーブル作成
# init_db()


# # アプリの設定
# app = FastAPI()


# # CORSMiddlewareの設定
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # DBセッション管理
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # トップページ用ルート確認
# @app.get("/")
# def root():
#     return{"message": "POS backend is running"}


# # 商品検索エンドポイント
# @app.get("/product")
# def product_search(code: str, db: Session = Depends(get_db)):
#     product = get_product_by_code(db, code)
#     if not product:
#         return None
#     return{
#         "PRD_ID":product.PRD_ID,
#         "CODE":product.CODE,
#         "NAME":product.NAME,
#         "PRICE":product.PRICE,
#     }


# #購入処理エンドポイント
# @app.post("/purchase")
# def purchase(emp_cd: str, items: list[dict], db: Session= Depends(get_db)):
#     transaction = create_transaction(db, emp_cd)
#     total = add_transaction_details(db, transaction.TRD_ID, items)
#     return {"success":True, "total": total}
 