# ライブラリのインポート
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal           
import crud                                 
from schemas import PurchaseIn, PurchaseResult  

# APIルーターを作成（このファイルのエンドポイント群をまとめる）
router = APIRouter()

# DBセッションを提供する依存関数（リクエストごとに呼ばれる）
def get_db():
    db = SessionLocal()     # セッション開始
    try:
        yield db            # 呼び出し先にセッションを提供
    finally:
        db.close()          # 処理終了後にセッションを閉じる（リソース解放）

# 購入処理エンドポイント（POST）
@router.post("/purchase", response_model=PurchaseResult)
def post_purchase(purchase: PurchaseIn, db: Session = Depends(get_db)):
    """
    商品購入リクエストを受け取り、DBに取引と明細を登録し、
    結果として取引ID・合計金額などを返す。
    """
    try:
        result = crud.create_transaction(db, purchase)  # 購入処理ロジックを呼び出し
        return result                                   # 正常なら結果を返却
    except Exception as e:
        # 例外が発生したら、HTTP 500 エラーとして返す（サーバーエラー）
        raise HTTPException(status_code=500, detail=str(e))
