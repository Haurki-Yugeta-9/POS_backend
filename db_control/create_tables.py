# #Lv1 
# # ライブラリのインポート
# from db_control.mymodels import Base, Product, Transaction, TransactionDetail
# from db_control.connect import engine
# from sqlalchemy import inspect

# # uname()error回避
# import platform
# print("platform:",platform.uname())

# # アプリ初期化時のテーブル作成
# def init_db():
#     inspector = inspect(engine)
#     # 既存テーブルの取得
#     existing_tables = inspector.get_table_names()
#     print("Checking tables...")

#     # transactionテーブルが存在しない場合は作成
#     if "transactions" not in existing_tables:
#         print("Creating tables >>> ")
#         try:
#             Base.metadata.create_all(bind=engine)
#             print("Table created successfully!")
#         except Exception as e:
#             print(f"Error creating tables: {e}")
#             raise
#     else:
#         print("Tables already exist.")