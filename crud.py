# ライブラリのインポート
from sqlalchemy.orm import Session
from models import ProductMaster, Transaction, TransactionDetail
from schemas import PurchaseIn
from datetime import datetime

# 商品マスタ検索（商品コードで1件取得）
def get_product_by_code(db: Session, code: str):
    return db.query(ProductMaster).filter(ProductMaster.CODE == code).first()
    # 商品マスタテーブルからCODEが一致する最初のレコードを取得

# 購入処理メイン関数
def create_transaction(db: Session, purchase: PurchaseIn):
    # 1-1: 取引テーブルへ登録（Transaction）
    new_transaction = Transaction(
        DATETIME=datetime.now(),                         # 登録日時
        EMP_CD=purchase.EMP_CD or '9999999999',          # 従業員コード（未指定ならデフォルト）
        STORE_CD=purchase.STORE_CD or '30',              # 店舗コード（未指定なら30）
        POS_NO=purchase.POS_NO or '90',                  # POS端末番号（未指定なら90）
        TOTAL_AMT=0,                                      # 合計金額（税込）※後で更新
        TTL_AMT_EX_TAX=0                                  # 合計金額（税抜）※後で更新
    )
    db.add(new_transaction)     # セッションに追加
    db.commit()                 # 一旦コミットしてTRD_IDを確定
    db.refresh(new_transaction) # TRD_IDを取得可能にする（オブジェクトを最新状態に）

    total = 0           # 税込合計
    total_ex_tax = 0    # 税抜合計

    # 1-2: 取引明細テーブル（TransactionDetail）に各商品を登録
    for idx, item in enumerate(purchase.items, start=1):
        tax_cd = '10'                           # 税コード（仮に「10%」とする）
        price = item.PRICE                     # 税込価格
        price_ex_tax = int(price / 1.1)        # 簡易的に税抜価格を算出（10%消費税前提）

        detail = TransactionDetail(
            TRD_ID=new_transaction.TRD_ID,     # 外部キー：親取引のID
            DTL_ID=idx,                        # 明細番号（1, 2, 3,...）
            PRD_ID=item.PRD_ID,                # 商品ID
            PRD_CODE=item.CODE,                # 商品コード
            PRD_NAME=item.NAME,                # 商品名
            PRD_PRICE=item.PRICE,              # 税込価格
            TAX_CD=tax_cd                      # 税コード
        )
        db.add(detail)                         # 明細をセッションに追加
        total += price                         # 税込合計に加算
        total_ex_tax += price_ex_tax           # 税抜合計に加算

    db.commit()  # 明細をDBに反映

    # 1-4: 取引テーブル（Transaction）に合計金額をセットして更新
    new_transaction.TOTAL_AMT = total
    new_transaction.TTL_AMT_EX_TAX = total_ex_tax
    db.commit()  # 更新内容を確定

    # 1-5: 処理結果を辞書で返す（PurchaseResultスキーマと同じ構造）
    return {
        "success": True,                    # 成功フラグ
        "TRD_ID": new_transaction.TRD_ID,  # 登録された取引ID
        "total": total,                    # 合計金額（税込）
        "total_ex_tax": total_ex_tax       # 合計金額（税抜）
    }
