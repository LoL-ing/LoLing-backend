from __future__ import with_statement
from logging.config import fileConfig
from sqlmodel import SQLModel, create_engine, engine_from_config, pool
from sqlmodel.ext.asyncio.session import AsyncEngine
from alembic import context

import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from app.common.config import Settings

from app.common.model import (
    Champions,
    Items,
    Lines,
    Profile_icons,
    Queues,
    Runes,
    Schools,
    Tiers,
    Spells,
)  # necessarily to import something from file where your models are stored
from app.community.model import (
    Attachments,
    Boards,
    Comments,
    Posts,
    Reported_comments,
    Reported_posts,
    Reported_Users,
)  # necessarily to import something from file where your models are stored
from app.match_history.model import (
    Match_histories,
    Current_season_summaries,
)  # necessarily to import something from file where your models are stored
from app.users.model import (
    Users,
    Relationships,
    Lol_profiles,
)  # necessarily to import something from file where your models are stored

schema_names = [
    "COMMON",
    "COMMUNITY",
    "USER",
    "MATCH_HISTORY",
]

settings = Settings()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # for schema_name in schema_names:
    try:
        # print(f"Alembic online migration: {schema_name}")
        connectable = create_engine(settings.DB_URL)

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_as_batch=True,
                # include_schemas=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        raise e


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
