import logging
import os
from contextlib import closing
from typing import Any
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import json
import datetime

logger = logging.getLogger('mcp_aact_server.database')

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)

class AACTDatabase:
    def __init__(self):
        logger.info("Initializing AACT database connection")
        load_dotenv()
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASSWORD")
        if not self.user or not self.password:
            raise Exception("DB_USER and DB_PASSWORD environment variables must be set")
        self.host = "aact-db.ctti-clinicaltrials.org"
        self.database = "aact"
        self._test_connection()
        logger.info("AACT database initialization complete")

    def _test_connection(self):
        logger.debug("Testing database connection to AACT")
        with closing(self._get_connection()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_database(), current_schema;")
                db, schema = cur.fetchone()
                logger.info(f"Connected to database: {db}, current schema: {schema}")

    def _get_connection(self):
        logger.debug("Creating new database connection")
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def execute_query(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        logger.debug(f"Executing query: {query}")
        if params:
            logger.debug(f"Query parameters: {params}")
        with closing(self._get_connection()) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                if params:
                    cur.execute(query, list(params.values()))
                else:
                    cur.execute(query)
                if query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
                    results = cur.fetchall()
                    logger.debug(f"Query returned {len(results)} rows")
                    return [dict(row) for row in results]
                else:
                    conn.rollback()
                    logger.warning("Attempted write operation. Rolling back.")
                    return [{"message": "Only read operations are allowed"}]