# Copyright (C) 2025, IQMO Corporation [support@iqmo.com]
# All Rights Reserved

import logging
import os
from dataclasses import dataclass

import pyodbc
from pandas import DataFrame, read_sql

from ... import IqlExtension, SubQuery, register_extension
from ...datamodel import cache

logger = logging.getLogger(__name__)

# https://github.com/pymssql/pymssql
# https://pymssql.readthedocs.io/en/stable/


# The connection cache is either connections **or** options to create a connection
_CONNECTION_CACHE: dict[str, pyodbc.Connection | dict] = {}


def _get_connection_from_options(connection_string: str, **kwargs) -> pyodbc.Connection:
    return pyodbc.connect(connection_string, **kwargs)


def _get_connection(connection_name: str) -> pyodbc.Connection:
    existing_conn: pyodbc.Connection | dict = _CONNECTION_CACHE[connection_name]
    if isinstance(existing_conn, dict):
        return _get_connection_from_options(**existing_conn)
    else:
        return existing_conn


def _execute_query(conn: pyodbc.Connection, query: str, parameters: dict | None = None) -> DataFrame:
    return read_sql(sql=query, con=conn, params=parameters)


@dataclass
class SqlServerExtensionPyMssqlConnect(IqlExtension):
    def executeimpl(self, sq: SubQuery) -> DataFrame:
        connection_name: str = sq.options.get("name", "default")  # type: ignore
        connection_string: str = sq.options["connection_string"]  # type: ignore

        eager = sq.options.get("eager", True)
        conn_options = {
            k: v for k, v in sq.options.items() if k != "name" and k != "eager" and k != "connection_string"
        }

        if eager:
            _CONNECTION_CACHE[connection_name] = _get_connection_from_options(
                connection_string=connection_string, **conn_options
            )
        else:
            _CONNECTION_CACHE[connection_name] = conn_options

        return DataFrame({"success": [True], "message": ["Connection Successful"]})


@dataclass
class SqlServerExtensionPyMssql(IqlExtension):
    @cache.iql_cache
    def executeimpl(self, sq: SubQuery) -> DataFrame:
        connection_name: str = sq.options.get("name", "default")  # type: ignore

        conn: pyodbc.Connection = _get_connection(connection_name)

        query: str = sq.get_query()  # type: ignore

        parameters: dict = sq.options.get("PARAMETERS", None)  # type: ignore

        return _execute_query(conn, query, parameters=parameters)


def register(keyword: str):
    cache_maxage = os.environ.get("IQL_MSSQL_CACHE_MAXAGE", None)
    if cache_maxage is not None:
        cache_maxage = int(cache_maxage)

    extension = SqlServerExtensionPyMssqlConnect(keyword=keyword, subword="pyodbc_connect")
    register_extension(extension)

    extension = SqlServerExtensionPyMssql(keyword=keyword, subword="pyodbc")
    extension.cache = cache.MemoryCache(max_age=cache_maxage, min_cost=2)
    register_extension(extension)

    extension = SqlServerExtensionPyMssql(keyword=keyword, subword="None")
    extension.cache = cache.MemoryCache(max_age=cache_maxage, min_cost=2)
    register_extension(extension)
