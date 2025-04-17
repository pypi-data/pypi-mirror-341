import functools
import logging
from contextlib import contextmanager
from typing import Any, Callable, Iterator, List, TypeVar, Union

import pandas as pd
from sqlalchemy import MetaData, Result, TextClause, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from camel_database_agent.database_base import SQLExecutionError, timing

T = TypeVar("T")

logger = logging.getLogger(__name__)

read_only_message = (
    "Operation rejected: This SQL contains statements that "
    "could modify data or schema (DROP, DELETE, UPDATE, etc.)"
    " which is not allowed in read-only mode."
)


@contextmanager
def session_scope(session_maker: sessionmaker) -> Iterator[Session]:
    """Context manager for database session handling."""
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(func: Callable) -> Callable:
    """Decorator that handles session creation and cleanup."""

    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        with session_scope(self.Session) as session:
            return func(self, session, *args, **kwargs)

    return wrapper


class DatabaseManager:
    def __init__(self, db_url: str, read_only_model: bool = True):
        self.db_url = db_url
        self.read_only_model = read_only_model
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        with self.engine.connect():
            logger.info(f"Successfully connected to database: {db_url}")

    @timing
    @with_session
    def select(
        self, session: Session, sql: str, bind_pd: bool = False
    ) -> Union[List[dict], pd.DataFrame]:
        """Execute Query SQL"""
        self._check_sql(sql)
        try:
            result: Result = session.execute(text(sql))
            if bind_pd:
                return pd.DataFrame(result.fetchall(), columns=list(result.keys()))
            else:
                # 转换结果为列表字典格式
                column_names = result.keys()
                rows = [dict(zip(column_names, row)) for row in result]
                return rows
        except OperationalError as e:
            raise SQLExecutionError(sql, str(e))

    @with_session
    def execute(
        self, session: Session, sql: Union[str, List[str]], ignore_sql_check: bool = False
    ) -> bool:
        """Execute one or more UPDATE/INSERT/DELETE statements."""
        if not ignore_sql_check:
            self._check_sql(sql)
        if isinstance(sql, str):
            for statement in sql.split(";"):
                if statement.strip():
                    session.execute(text(statement))
        else:
            for statement in sql:
                if statement.strip():
                    session.execute(text(statement.strip()))
        return True

    def dialect_name(self) -> str:
        return self.engine.dialect.name

    def get_metadata(self) -> MetaData:
        self.metadata.reflect(bind=self.engine)
        return self.metadata

    def _check_sql(self, sql: Union[str, List[str]]) -> None:
        """Check if SQL is safe to execute (non-destructive)."""
        if self.read_only_model:
            dangerous_keywords = {
                # Standalone keywords that modify data/schema
                "DROP": True,
                "TRUNCATE": True,
                "DELETE": True,
                "UPDATE": True,
                "INSERT": True,
                "ALTER": True,
                "RENAME": True,
                "REPLACE": True,
                # CREATE is special case - some forms are read-only
                "CREATE": {"SAFE_PREFIXES": ["SHOW CREATE"]},
            }

            statements = []
            if isinstance(sql, str):
                statements = [stmt.strip().upper() for stmt in sql.split(";") if stmt.strip()]
            elif isinstance(sql, TextClause):
                statements = [stmt.strip().upper() for stmt in sql.text if stmt.strip()]
            else:
                statements = [stmt.strip().upper() for stmt in sql if stmt.strip()]

            # Check each statement for dangerous keywords
            for stmt in statements:
                stmt_upper = stmt.upper()
                for keyword, config in dangerous_keywords.items():
                    if isinstance(config, bool) and config:
                        if keyword in stmt_upper.split():
                            raise SQLExecutionError('\n'.join(statements), read_only_message)
                    elif isinstance(config, dict):
                        # Handle special cases with exceptions
                        if keyword in stmt_upper.split():
                            is_safe = False
                            for safe_prefix in config.get("SAFE_PREFIXES", []):
                                if stmt_upper.startswith(safe_prefix):
                                    is_safe = True
                                    break
                            if not is_safe:
                                raise SQLExecutionError('\n'.join(statements), read_only_message)
