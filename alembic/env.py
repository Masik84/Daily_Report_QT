from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine, pool, text
from sqlalchemy import pool
import psycopg2

from alembic import context

from models import Base


config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        naming_convention=naming_convention,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Добавляем те же параметры, что и в online-режиме
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()

def ensure_database_exists():
    try:
        # Пробуем подключиться к целевой БД
        test_engine = create_engine('postgresql+psycopg2://postgres:qwerty@localhost:5432/report_db')
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Простой тестовый запрос
    except Exception as e:
        # Если подключение не удалось, создаем БД
        admin_engine = create_engine('postgresql+psycopg2://postgres:qwerty@localhost:5432/postgres', isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            conn.execute(text("CREATE DATABASE report_db"))
            print("База данных report_db успешно создана")

def run_migrations_online():
    ensure_database_exists()
    
    connectable = create_engine(
        'postgresql+psycopg2://postgres:qwerty@localhost:5432/report_db',
        poolclass=pool.NullPool,
        connect_args={'client_encoding': 'utf8'}
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            naming_convention=naming_convention,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()