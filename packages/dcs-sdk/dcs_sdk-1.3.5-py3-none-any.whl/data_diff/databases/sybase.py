#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Any, ClassVar, Dict, List, Optional, Tuple, Type

import attrs

from data_diff.abcs.database_types import (
    JSON,
    Boolean,
    ColType_UUID,
    Date,
    DbPath,
    Decimal,
    Float,
    Integer,
    Native_UUID,
    NumericType,
    String_UUID,
    TemporalType,
    Text,
    Time,
    Timestamp,
    TimestampTZ,
)
from data_diff.databases.base import (
    CHECKSUM_HEXDIGITS,
    CHECKSUM_OFFSET,
    BaseDialect,
    ConnectError,
    QueryError,
    QueryResult,
    ThreadedDatabase,
    import_helper,
)


@import_helper("sybase")
def import_sybase():
    import pyodbc

    return pyodbc


@attrs.define(frozen=False)
class Dialect(BaseDialect):
    name = "Sybase"
    ROUNDS_ON_PREC_LOSS = True
    SUPPORTS_PRIMARY_KEY: ClassVar[bool] = True
    SUPPORTS_INDEXES = True
    TYPE_CLASSES = {
        # Timestamps
        "datetimeoffset": TimestampTZ,
        "datetime2": Timestamp,
        "smalldatetime": Timestamp,
        "date": Date,
        "time": Time,
        "timestamp with time zone": TimestampTZ,
        # Numbers
        "float": Float,
        "real": Float,
        "decimal": Decimal,
        "money": Decimal,
        "smallmoney": Decimal,
        # "numeric": Decimal,
        # int
        "int": Integer,
        "bigint": Integer,
        "tinyint": Integer,
        "smallint": Integer,
        "integer": Integer,
        "unsigned big int": Integer,
        "unsigned int": Integer,
        "unsigned small int": Integer,
        # Text
        "varchar": Text,
        "char": Text,
        "text": Text,
        "ntext": Text,
        "nvarchar": Text,
        "nchar": Text,
        "binary": Text,
        "varbinary": Text,
        "xml": Text,
        # UUID
        "uniqueidentifier": Native_UUID,
        # Bool
        "bit": Boolean,
        "varbit": Boolean,
        # JSON
        "json": JSON,
    }

    def quote(self, s: str) -> str:
        if s in self.TABLE_NAMES and self.default_schema:
            return f"[{self.default_schema}].[{s}]"
        return f"[{s}]"

    def set_timezone_to_utc(self) -> str:
        raise NotImplementedError("Sybase does not support a session timezone setting.")

    def current_timestamp(self) -> str:
        return "GETDATE()"

    def current_database(self) -> str:
        return "DB_NAME()"

    def current_schema(self) -> str:
        return """default_schema_name
        FROM sys.database_principals
        WHERE name = CURRENT_USER"""

    def to_string(self, s: str) -> str:
        # Sybase IQ does not support VARCHAR(MAX), so use VARCHAR(255) instead
        return f"cast({s} as varchar)"

    def type_repr(self, t) -> str:
        try:
            return {bool: "bit", str: "text"}[t]
        except KeyError:
            return super().type_repr(t)

    def random(self) -> str:
        return "rand()"

    def is_distinct_from(self, a: str, b: str) -> str:
        # IS (NOT) DISTINCT FROM is available only since SQLServer 2022.
        # See: https://stackoverflow.com/a/18684859/857383
        return f"(({a}<>{b} OR {a} IS NULL OR {b} IS NULL) AND NOT({a} IS NULL AND {b} IS NULL))"

    def limit_select(
        self,
        select_query: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        has_order_by: Optional[bool] = None,
    ) -> str:
        import re

        def safe_trim(match):
            column_name = match.group(1)
            return f"TRIM(cast({column_name} as varchar))"

        select_query = re.sub(r"TRIM\(\[([\w]+)\]\)", safe_trim, select_query)

        select_query = re.sub(r"TRIM\(([\w]+)\)", safe_trim, select_query)

        if limit is not None:
            select_query = select_query.replace("SELECT", f"SELECT TOP {limit}", 1)

        if not has_order_by:
            select_query += " ORDER BY 1"
        return select_query

    def constant_values(self, rows) -> str:
        values = ", ".join("(%s)" % ", ".join(self._constant_value(v) for v in row) for row in rows)
        return f"VALUES {values}"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        # if coltype.precision > 0:
        #     formatted_value = (
        #         f"CONVERT(VARCHAR(20), {value}, 120) + '.' + "
        #         f"SUBSTRING(CONVERT(VARCHAR(7), {value}, 109), 1, {coltype.precision})"
        #     )
        # else:
        #     formatted_value = f"CONVERT(VARCHAR(20), {value}, 120)"

        # return formatted_value
        return f"CAST({value} AS VARCHAR)"

    def normalize_number(self, value: str, coltype: NumericType) -> str:
        # if coltype.precision == 0:
        #     return f"CAST(FLOOR({value}) AS VARCHAR)"

        return f"CAST({value} AS VARCHAR)"

        # return f"FORMAT({value}, 'N{coltype.precision}')"

    def md5_as_int(self, s: str) -> str:
        """Returns an MD5 hash of the input string as an integer for Sybase IQ."""
        return f"CAST(HEXTOINT(LEFT(CAST(HASH({s}, 'MD5') AS VARCHAR(32)), 8)) AS BIGINT) - 140737488355327"

    def md5_as_hex(self, s: str) -> str:
        return f"HashBytes('MD5', {s})"

    def concat(self, items: List[str]) -> str:
        """Provide SQL for concatenating multiple columns into a string for Sybase IQ."""
        assert len(items) > 1, "At least two columns are required for concatenation."
        return " || ".join(items)

    def normalize_uuid(self, value: str, coltype: ColType_UUID) -> str:
        if isinstance(coltype, String_UUID):
            # return f"LTRIM(RTRIM({value}))"
            return f"CAST({value} AS VARCHAR)"  # ONLY THIS WORKS
        return f"CONVERT(VARCHAR(36), {value})"

    def parse_table_name(self, name: str) -> DbPath:
        "Parse the given table name into a DbPath"
        self.TABLE_NAMES.append(name.split(".")[-1])
        return tuple(name.split("."))


@attrs.define(frozen=False, init=False, kw_only=True)
class Sybase(ThreadedDatabase):
    DIALECT_CLASS: ClassVar[Type[BaseDialect]] = Dialect
    CONNECT_URI_HELP = "sybase://<user>:<password>@<host>/<database>/<schema>"
    CONNECT_URI_PARAMS = ["database", "schema"]

    default_database: str
    _args: Dict[str, Any]
    _sybase: Any

    def __init__(self, host, port, user, password, *, database, thread_count, **kw) -> None:
        super().__init__(thread_count=thread_count)
        args = dict(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            **kw,
        )
        self._args = {k: v for k, v in args.items() if v}
        if self._args.get("odbc_driver", None) is not None:
            self._args["driver"] = self._args.pop("odbc_driver")
        else:
            self._args["driver"] = "FreeTDS"

        try:
            self.default_database = self._args["database"]
            self.default_schema = self._args["schema"]
            self.dialect.default_schema = self.default_schema
        except KeyError:
            raise ValueError("Specify a default database and schema.")

        self._sybase = None

    def create_connection(self):
        self._sybase = import_sybase()
        try:
            if "iq" in self._args.get("driver", "").lower():
                host = self._args.get("host", None)
                port = self._args.get("port", None) or 2638
                server = self._args.get("server", None)
                key = {}
                if host:
                    key["HOST"] = f"{host}:{port}"
                else:
                    key["SERVER"] = server
                conn_dict = {
                    "DRIVER": self._args.get("driver"),
                    **key,
                    "DATABASE": self.default_database,
                    "UID": self._args["user"],
                    "PWD": self._args["password"],
                }
                connection = self._sybase.connect(**conn_dict)
            else:
                if "freetds" in self._args.get("driver", "").lower():
                    self._args.pop("server", None)
                connection = self._sybase.connect(**self._args)
            return connection
        except self._sybase.Error as error:
            raise ConnectError(*error.args) from error

    def select_table_schema(self, path: DbPath) -> str:
        database, schema, name = self._normalize_table_path(path)
        if "iq" in self._args.get("driver", "").lower():
            return (
                f"SELECT c.column_name, d.domain_name AS data_type, "
                f"CASE WHEN d.domain_name IN ('DECIMAL', 'NUMERIC') THEN c.scale ELSE NULL END AS numeric_scale, "
                f"CASE WHEN d.domain_name IN ('DECIMAL', 'NUMERIC') THEN c.width ELSE NULL END AS numeric_precision, "
                f"CASE WHEN d.domain_name IN ('DATE', 'TIME', 'TIMESTAMP') THEN c.scale ELSE NULL END AS datetime_precision, "
                f"NULL AS collation_name, c.width AS character_maximum_length "
                f"FROM {database}.SYS.SYSTABLE t "
                f"JOIN {database}.SYS.SYSCOLUMN c ON t.table_id = c.table_id "
                f"JOIN {database}.SYS.SYSDOMAIN d ON c.domain_id = d.domain_id "
                f"JOIN {database}.SYS.SYSUSER u ON t.creator = u.user_id "
                f"WHERE t.table_name = '{name}' "
                f"AND u.user_name = '{schema}'"
            )
        if "freetds" in self._args.get("driver", "").lower():
            return (
                f"SELECT c.name AS column_name, t.name AS data_type, "
                f"c.prec AS numeric_precision, c.scale AS numeric_scale, "
                f"CASE WHEN c.type IN (61, 111) THEN c.prec ELSE NULL END AS datetime_precision, "
                f"NULL AS collation_name, c.length AS character_maximum_length "
                f"FROM {database}.dbo.sysobjects o "
                f"JOIN {database}.dbo.syscolumns c ON o.id = c.id "
                f"JOIN {database}.dbo.systypes t ON c.usertype = t.usertype "
                f"WHERE o.name = '{name}'"
            )

        return (
            f"SELECT c.name AS column_name, t.name AS data_type, "
            f"c.prec AS numeric_precision, c.scale AS numeric_scale, "
            f"CASE WHEN c.type IN (61, 111) THEN c.prec ELSE NULL END AS datetime_precision, "
            f"NULL AS collation_name, c.length AS character_maximum_length "
            f"FROM {database}..sysobjects o "
            f"JOIN {database}..syscolumns c ON o.id = c.id "
            f"JOIN {database}..systypes t ON c.usertype = t.usertype "
            f"JOIN {database}..sysusers u ON o.uid = u.uid "
            f"WHERE o.name = '{name}' "
            f"AND u.name = '{schema}'"
        )

    def _normalize_table_path(self, path: DbPath) -> DbPath:
        if len(path) == 1:
            return self.default_database, self.default_schema, path[0]
        elif len(path) == 2:
            return self.default_database, path[0], path[1]
        elif len(path) == 3:
            return path

        raise ValueError(
            f"{self.name}: Bad table path for {self}: '{'.'.join(path)}'. Expected format: table, schema.table, or database.schema.table"
        )

    def _query_cursor(self, c, sql_code):
        try:
            c.execute(sql_code)
            if sql_code.lower().startswith(("select", "explain", "show")):
                columns = c.description and [col[0] for col in c.description]
                return QueryResult(c.fetchall(), columns)
            elif sql_code.lower().startswith(("create", "drop")):
                try:
                    c.connection.commit()
                except AttributeError:
                    ...
        except Exception as _e:
            try:
                c.connection.rollback()
            except Exception as rollback_error:
                print("Rollback failed:", rollback_error)
            raise
