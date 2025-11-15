from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.core.db import Base
from app.models.users import User

# Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# set target_metadata for autogenerate
target_metadata = Base.metadata

# set database URL from settings
config.set_main_option("sqlalchemy.url",
                       f"postgresql://{settings.POSTGRES_USER}:"
                       f"{settings.POSTGRES_PASSWORD}@"
                       f"{settings.POSTGRES_HOST}:"
                       f"{settings.POSTGRES_PORT}/"
                       f"{settings.POSTGRES_DB}")

def include_object(object, name, type_, reflected, compare_to):
    # skip dropping PostGIS/Tiger tables
    if type_ == "table" and name in [
        "state_lookup", "faces", "tabblock", "pagc_rules", "addr",
        "layer", "bg", "county", "zip_state_loc", "loader_lookuptables",
        "pagc_lex", "zip_state", "zip_lookup", "zip_lookup_base",
        "zip_lookup_all", "loader_platform", "tabblock20", "addrfeat",
        "state", "featnames", "geocode_settings_default", "place_lookup",
        "loader_variables", "geocode_settings", "street_type_lookup",
        "topology", "place", "pagc_gaz", "spatial_ref_sys", "edges",
        "cousub", "county_lookup", "countysub_lookup", "direction_lookup",
        "tract", "zcta5", "secondary_unit_lookup"
    ]:
        return False
    return True


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, include_object=include_object)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
