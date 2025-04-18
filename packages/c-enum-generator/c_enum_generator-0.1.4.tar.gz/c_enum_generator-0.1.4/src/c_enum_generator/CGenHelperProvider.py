from argparse import Namespace
from typing import Any

from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider


class CGenHelper:
    def validate_enum_desc(self):
        pass

    def update_values(self, enum_item):
        curr_val = 0
        for entry in enum_item['entries']:
            curr_val = entry.get('value', curr_val + 1)
            entry['value'] = curr_val
        return enum_item['entries']


class CGenHelperProvider(AbstractHelperProvider):
    def get_helper_object(self) -> Any:
        return CGenHelper()

    def get_helper_ns(self) -> str:
        return 'cenum'

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
