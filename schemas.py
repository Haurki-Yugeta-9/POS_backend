# ライブラリのインポート
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 商品情報の出力モデル
class ProductOut(BaseModel):
    PRD_ID: int       # 商品一意ID（主キー）
    CODE: str         # 商品コード（JANコードなど）
    NAME: str         # 商品名
    PRICE: int        # 商品価格（税込）

    class Config:
        orm_mode = True  # ORM（例：SQLAlchemy）からの自動変換を許可

# 購入時の商品1件分の入力モデル
class PurchaseItem(BaseModel):
    PRD_ID: int       # 商品一意ID
    CODE: str         # 商品コード
    NAME: str         # 商品名
    PRICE: int        # 商品価格（税込）

# 購入処理のリクエスト全体の入力モデル
class PurchaseIn(BaseModel):
    EMP_CD: Optional[str] = '9999999999'  # 従業員コード（省略時は固定値）
    STORE_CD: Optional[str] = '30'        # 店舗コード（省略時は店舗ID30）
    POS_NO: Optional[str] = '90'          # POS端末番号（省略時は90）
    items: List[PurchaseItem]             # 購入商品のリスト（複数可）

# 購入処理の結果の出力モデル
class PurchaseResult(BaseModel):
    success: bool       # 処理が成功したかどうか
    TRD_ID: int         # 登録された取引ID（例：transactionテーブル主キー）
    total: int          # 合計金額（税込）
    total_ex_tax: int   # 合計金額（税抜）
