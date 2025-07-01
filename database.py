# ライブラリのインポート
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# SupabaseのDB接続URLを.envファイルから取得
DATABASE_URL = os.environ["DATABASE_URL"]

# エンジンを作成（SQLAlchemyがDBと接続するためのオブジェクト）
engine = create_engine(DATABASE_URL)

# セッションローカル（DBとの接続セッションを管理）
SessionLocal = sessionmaker(
    autocommit=False,  # 自動コミットしない（明示的に commit() を使う）
    autoflush=False,   # セッション内の変更を自動でDBに送らない
    bind=engine        # 使用するエンジンを指定
)

# models.py で定義した Base をインポート（テーブル定義の親）
from models import Base
