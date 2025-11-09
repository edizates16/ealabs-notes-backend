import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from logging.config import fileConfig
from app.db.base import Base

from alembic import context

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL ortam değişkeni ayarlanmamış!")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# migrations/env.py (dosyanın sonundaki bölümü bununla değiştirin)


def do_run_migrations(connection):
    """
    Migration'ları senkron bir şekilde çalıştıran yardımcı fonksiyon.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # ... diğer ayarlar eklenebilir
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    'Online' modda asenkron olarak migration'ları çalıştırır.
    """
    # Asenkron bir motor oluştur
    connectable = create_async_engine(DATABASE_URL, poolclass=NullPool)

    # Asenkron bağlantı içinde senkron 'do_run_migrations' fonksiyonunu çalıştır
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Motoru kapat
    await connectable.dispose()


# Alembic'in ana çalışma mantığı
if context.is_offline_mode():
    # Offline mod (SQL script üretmek için) şu an kapsam dışı
    # run_migrations_offline()
    print("Offline mod desteklenmiyor.")
else:
    # Online mod (veritabanına bağlanarak)
    asyncio.run(run_migrations_online())
