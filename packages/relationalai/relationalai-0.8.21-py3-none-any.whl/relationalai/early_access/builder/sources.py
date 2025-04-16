from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import json
import re
import textwrap
from snowflake.snowpark.context import get_active_session
from . import builder as b

#--------------------------------------------------
# Source
#--------------------------------------------------

class Source(b.Producer):
    def __init__(self) -> None:
        super().__init__(None)
        self._relationships = {}

#--------------------------------------------------
# Snowflake sources
#--------------------------------------------------

SFTypes = {
    "TEXT": "String",
    "FIXED": "Number",
}

def parse_fqn(fqn:str):
    database, schema, table = fqn.split(".")
    return database, schema, table

SF_ID_REGEX = re.compile(r'^[A-Za-z_][A-Za-z0-9_$]*$')
def quoted(ident:str):
    if SF_ID_REGEX.match(ident) or ident[0] == '"':
        return ident
    return f'"{ident}"'

@dataclass
class TableInfo:
    source:SnowflakeTable|None
    fields:list[b.Field]
    raw_columns:list[dict]

class SchemaInfo:
    def __init__(self, database:str, schema:str) -> None:
        self.database = database
        self.schema = schema
        self.tables = defaultdict(lambda: TableInfo(None, [], []))
        self.fetched = False

    def fetch(self):
        self.fetched = True
        session = get_active_session()
        table_names = self.tables.keys()
        name_lookup = {x.upper(): x for x in table_names}
        tables = ", ".join([f"'{x.upper()}', '{x}'" for x in self.tables.keys()])
        columns = session.sql(textwrap.dedent(f"""
            begin
                SHOW COLUMNS IN SCHEMA {quoted(self.database)}.{quoted(self.schema)};
                let r resultset := (select "table_name", "column_name", "data_type" from table(result_scan(-1)) as t
                                    where "table_name" in ({tables}));
                return table(r);
            end;
        """))
        print(textwrap.dedent(f"""
            begin
                SHOW COLUMNS IN SCHEMA {quoted(self.database)}.{quoted(self.schema)};
                let r resultset := (select "table_name", "column_name", "data_type" from table(result_scan(-1)) as t
                                    where "table_name" in ({tables}));
                return table(r);
            end;
        """))
        columns = columns.collect()
        print(columns)
        for row in columns:
            table_name, column_name, data_type = row
            table_name = name_lookup.get(table_name, table_name)
            info = self.tables[table_name]
            type_str = SFTypes[json.loads(data_type).get("type")]
            info.fields.append(b.Field(name=column_name, type_str=type_str, is_many=False))
            info.raw_columns.append(row.as_dict())

class SnowflakeTable(Source):
    _schemas:dict[tuple[str, str], SchemaInfo] = {}

    def __init__(self, fqn:str) -> None:
        super().__init__()
        self._fqn = fqn
        self._database, self._schema, self._table = parse_fqn(fqn)
        self._inited = False
        info = self._schemas.get((self._database, self._schema))
        if not info:
            info = self._schemas[(self._database, self._schema)] = SchemaInfo(self._database, self._schema)
        info.tables[self._table].source = self

    def _lazy_init(self):
        if self._inited:
            return
        self._inited = True
        schema_info = self._schemas[(self._database, self._schema)]
        if not schema_info.fetched:
            schema_info.fetch()
        table_info = schema_info.tables[self._table]
        print(table_info.raw_columns)
        self._rel = b.Relationship(self._fqn, fields=[b.Field("row_id", "Number", False)] + table_info.fields)
        print(self._rel, self._rel._fields)



    def _compile_lookup(self, compiler:b.Compiler, ctx:b.CompilerContext):
        self._lazy_init()
        return


#--------------------------------------------------
# Convenience functions
#--------------------------------------------------

def table(name:str) -> SnowflakeTable:
    return SnowflakeTable(name)
