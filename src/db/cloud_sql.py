import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lấy DATABASE_URL từ biến môi trường (Cloud SQL)
# Ví dụ: postgresql+psycopg2://user:pass@/dbname?host=/cloudsql/INSTANCE_CONNECTION_NAME
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Khi chạy trên Cloud Run, sử dụng Unix socket
if os.getenv("CLOUD_SQL_CONNECTION_NAME"):
    DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@/{os.getenv('DB_NAME')}?host=/cloudsql/{os.getenv('CLOUD_SQL_CONNECTION_NAME')}"

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=2)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()