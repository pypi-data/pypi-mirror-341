import json
from argparse import Namespace
from typing import Dict, Optional

from importlib_resources import files
from json2any_plugin.AbstractSchemaProvider import AbstractSchemaProvider

import c_enum_generator.resources as schemas_res

available_schemas = {}


class CGenSchemaProvider(AbstractSchemaProvider):

    def get_schema(self, schema_id: str) -> Optional[Dict[str, Dict]]:
        r_files = files('c_enum_generator.resources')
        for res in r_files.iterdir():
            if res.suffix != '.json':
                continue
            with res.open(mode='r') as f:
                schema = json.load(f)
                s_id = schema['$id']
                if s_id == schema_id:
                    return schema
        return None

    def get_available_schemas(self) -> Dict[str, str]:
        global available_schemas
        if available_schemas:
            return available_schemas

        r_files = files('c_enum_generator.resources')
        for res in r_files.iterdir():
            if res.suffix != '.json':
                continue
            with res.open(mode='r') as f:
                schema = json.load(f)
                s_id = schema['$id']
                s_title = schema['title']
                available_schemas[s_id] = s_title
        return available_schemas

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def arg_prefix(self) -> str:
        return ''

    @property
    def has_arguments(self) -> bool:
        return False

    def update_arg_parser(self, parser: '_ArgumentGroup') -> None:
        # Unused
        pass

    def process_args(self, args: Namespace) -> bool:
        return True

    def init(self, **kwargs) -> None:
        # Unused
        pass
