# ライブラリのインポート
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal       
import crud                             
from schemas import ProductOut          

# APIルーターを作成（このファイルに含まれる全APIに共通のパスなどを設定できる）
router = APIRouter()

# DBセッションを取得するための依存関数
def get_db():
    db = SessionLocal()     # セッションを生成
    try:
        yield db            # 呼び出し元に返す（yieldはジェネレータ）
    finally:
        db.close()          # 処理が終わったらセッションを閉じる（リソース解放）

# 商品コードで商品を取得するGET API
@router.get("/product", response_model=ProductOut)
def get_product(code: str, db: Session = Depends(get_db)):
    """
    商品コード（code）をクエリパラメータで受け取り、該当商品情報を返す。
    見つからなければ 404 を返す。
    """
    product = crud.get_product_by_code(db, code)  # DBから商品を検索
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")  # 見つからなければエラー
    return product  # 見つかればスキーマに従ってJSONで返却
