from sqlalchemy import Column, MetaData, SmallInteger, String, Table, Text
from sqlalchemy.dialects.postgresql import ENUM


metadata = MetaData()

language = ENUM(
    "ru", "en", name="language_t_v1", create_type=False, metadata=metadata
)

level = ENUM(
    "A1", "A2", "A3", name="level_t_v1", create_type=False, metadata=metadata
)

users = Table(
    "users",
    metadata,
    Column("user_id", SmallInteger, primary_key=True),
    Column("tg_login", Text, nullable=False),
    Column("login", String(16), unique=True, nullable=False),
    Column("password", String(16), nullable=False),
    Column("words_in_lesson", SmallInteger, nullable=False),
    Column("native_language", language, nullable=False),
    Column("language_to_learn", language, nullable=False),
    Column("word_level", level, nullable=False),
)
