# render用に作り直すので一旦無視

# # Lv2
# # ライブラリのインポート
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# import logging
# from .crud import get_product_by_code, create_transaction
# from .schemas import ProductBase, Product, ItemCreate, TransactionCreate, TransactionResponse, TransactionHeaderBase, TransactionHeader, TransactionDetailBase, TransactionDetailCreate, TransactionDetail
# from .connect import get_db

# # ロガーの設定
# logger = logging.getLogger("api")
# router = APIRouter()


# # 商品コード取得のエンドポイント
# @router.get("/products/{product_code}", response_model=Product)
# def read_product(product_code:str, db:Session=Depends(get_db)):
#     try:
#         logger.info(f"商品コード`{product_code}`の情報を取得しています")
#         db_product = get_product_by_code(db, product_code=product_code)

#         if db_product is None:
#             logger.warning(f"商品コード`{product_code}`は見つかりませんでした")
#             raise HTTPException(status_code=404, detail=f"商品コード`{product_code}`は見つかりませんでした")
        
#         logger.info(f"商品コード`{product_code}`の情報を正常に取得しました：{db_product.NAME}")
#         return Product(
#             prd_id = db_product.PRD_ID,
#             code = db_product.CODE,
#             name = db_product.NAME,
#             price = db_product.PRICE
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"商品情報取得中にエラーが発生しました: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"データベースエラー：{str(e)}")
    

# # 取引のエンドポイント
# @router.post("/transaactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
# def create_new_transactoin(transaction: TransactionCreate, db: Session = Depends(get_db)):
#     try:
#         db_transaction, total_amt, ttl_amt_ex_tax = create_transaction(db, transaction_data=transaction)
#         return{
#             "success": True,
#             "trd_id":db_transaction.TRD_ID,
#             "total_amt": total_amt,
#             "ttl_amt_ex_tax": ttl_amt_ex_tax
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))