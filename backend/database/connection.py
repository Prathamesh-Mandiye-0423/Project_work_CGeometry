from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from backend.config import get_settings
import logging

logger= logging.getLogger(__name__)
settings=get_settings()


engine = create_engine(
    settings.DATABASE_URL,
    echo= settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    poolClass=QueuePool,
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=utc"
    }
)

SessionLocal = sessionmaker(
    autocommit= False, 
    autoflush = False, 
    bind= engine,
    expire_on_commit=False)
Base = declarative_base()
def get_db()->Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        from backend.database import models
        Base.metadata.create_all(bind=engine)
        logger.info("Database table created successfully")

        table_names= Base.metadata.tables.keys()
        logger.info(f"Db tables:{', '.join(table_names)}")
    except Exception as e:
        logger.error(f"Error creating db: {e}")
        raise

def check_db_connection() -> bool:
    try:
        db=SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("Databse Connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def drop_all_tables()->bool:
    if not settings.DEBUG:
        logger.error("Drop all tables operation is only allowed in DEBUG mode")
        return False
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"Error dropping tables:{e}")
        return False

def reset_db()->bool:
    if not settings.DEBUG:
        logger.error("DB reset allowed in Debug mode")
        return False
    logger.warning("Reset db")
    drop_all_tables()
    init_db()
    logger.info("DB reset successful")
    return True


def get_db_health()->dict:
    try:
        is_connected=check_db_connection()

        return{
            "status": "healthy" if is_connected else "unhealthy",
            "connected": is_connected,
            "pool_Size":engine.pool.size(),
            "checked_out_connections": engine.pool.checkedout(),
            "overflow": engine.pool.overflow(),
            "database_url":settings.DATABASE_URL.split("@")[1] if @ in settings.DATABASE_URL else "unknown"

        }
    except Exception as e:
        logger.error(f"Error getting db health:{e}")

        return {
            "status":"unhealthy",
            "connected":False,
            "error": str(e)
        }