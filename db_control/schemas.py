# render用に作り直すので一旦無視

# # Lv2
# # ライブラリのインポート
# from pydantic import BaseModel
# from typing import List, Optional


# # ProductBaseの定義
# class ProductBase(BaseModel):
#     code: str
#     name: str
#     price: int

# # Productの定義
# class Product(ProductBase):
#     prd_id: int
    
#     # SQLAlchemyモデルと連携
#     class Config:
#         from_attributes = True

# # ItemCreateの定義
# class ItemCreate(BaseModel):
#     prd_id: int
#     prd_code: str
#     prd_name: str
#     prd_price: int
#     quantity: int

# # TransactionCreateの定義
# class TransactionCreate(BaseModel):
#     emp_cd: Optional[str] = "9999999999"
#     items: List[ItemCreate]

# # TransactionResponseの定義
# class TransactionResponse(BaseModel):
#     success: bool
#     trd_id: int
#     total_amt: int
#     ttl_amt_ex_tax: int

# # TransactionHeaderBaseの定義
# class TransactionHeaderBase(BaseModel):
#     emp_cd: str
#     store_cd: str
#     pos_no: str
#     total_amt: int
#     ttl_amt_ex_tax: int

# # TransactionHeaderの定義
# class TransactionHeader(TransactionHeaderBase):
#     trd_id: int
#     datetime: str

#     class Config:
#         from_attributes = True

# # TransactionDetailBaseの定義
# class TransactionDetailBase(BaseModel):
#     prd_id: int
#     prd_code: str
#     prd_name: str
#     prd_price: int
#     quantity: int
#     tax_cd: str

# # TransactionDetailCreateの定義
# class TransactionDetailCreate(TransactionDetailBase):
#     trd_id: int
#     dtl_id: int

# class TransactionDetail(TransactionDetailBase):
#     trd_id: int
#     dtl_id: int

#     class Config:
#         from_attributes = True


    
    