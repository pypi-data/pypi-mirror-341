from typing import List, Dict, Tuple, Any, Optional
from pymysql import connect
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from spiderpy3.dbs.db import DB


class MysqlDB(DB):

    def __init__(
            self,
            *args: Any,
            host: str = "localhost",
            port: int = 3306,
            username: Optional[str] = None,
            password: Optional[str] = None,
            dbname: str,
            charset: str = "utf8mb4",
            **kwargs: Any
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.charset = charset

        super().__init__(*args, **kwargs)

    def open(self) -> Tuple[Connection, Cursor]:
        connection = connect(
            user=self.username,
            password=self.password,
            host=self.host,
            database=self.dbname,
            port=self.port,
            charset=self.charset,
        )
        cursor = connection.cursor()
        return connection, cursor

    def close(self, connection: Connection, cursor: Cursor) -> None:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

    def _open(self) -> None:
        self.connection, self.cursor = self.open()

    def _close(self) -> None:
        self.close(self.connection, self.cursor)

    def query(self, sql: str) -> List[Dict[str, Any]]:
        connection, cursor = self.open()

        cursor.execute(sql)
        result = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        rows = [dict(zip(columns, r)) for r in result]

        self.close(connection, cursor)
        return rows
