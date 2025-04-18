from dataclasses import field, dataclass
from typing import List, Optional

from marshmallow import Schema

CENUM_SCHEMA_NAME = 'https://gitlab.com/maciej.matuszak/c-enum-generator/cenum.schema'

CENUM_SCHEMA_VERSION_1 = 1
CENUM_SCHEMA_VERSION = CENUM_SCHEMA_VERSION_1

CENUM_SCHEMA_ID_V1 = f'{CENUM_SCHEMA_NAME}_v{CENUM_SCHEMA_VERSION}'
CENUM_SCHEMA_ID = CENUM_SCHEMA_ID_V1

CENUM_SCHEMA_METADATA = {
    '$id': CENUM_SCHEMA_ID,
    'title': 'C enum generator data schema',
    'description': 'Describes the C enum generator schema'
}


@dataclass
class EnumEntryDescriptor(Schema):
    name: str = field(metadata=dict(description='Name of enum entry. has to be proper c identifier'))
    doco: Optional[str] = field(metadata=dict(description='Doco string for enum entry'))
    display_value: Optional[str] = field(metadata=dict(description='Display string for enum entry'))
    value: Optional[int] = field(metadata=dict(description='Enum entry value'))


@dataclass
class EnumDescriptor(Schema):
    name: str = field(metadata=dict(description='Name of enum. Has to be valid c identifier'))
    doco: Optional[str] = field(
        metadata=dict(description='Doco string for this enum. Can be multiline, separated by line separator'))
    display_value_default: Optional[str] = field(metadata=dict(
        description='If set the it will be used in "xxx_to_display_str(...)" function if the input is invalid'))
    name_value_default: Optional[str] = field(metadata=dict(
        description='If set the it will be used in "xxx_to_name_str(...)" function if the input is invalid'))
    entry_prefix: Optional[str] = field(
        metadata=dict(description='Prefix for enum entries. If not set the "name" will be used'))
    continuous: bool = field(metadata=dict(
        description='Assumes the values of enum are continuous without breaks. Raises error if this is the enum entries are not continuous'))
    min_entry: bool = field(
        metadata=dict(description='Adds special enum "_min" entry with minimum value of all entries'))
    max_entry: bool = field(
        metadata=dict(description='Adds special enum "_max" entry with maximum value of all entries'))
    count_entry: bool = field(metadata=dict(
        description='Adds special enum "_count" entry with number of all normal (excludes "_max", "_min") entries'))
    entries: List[EnumEntryDescriptor] = field(default_factory=list,
                                               metadata=dict(description='List of enum entry descriptors'))
    capitalise: bool = field(default=True,
                             metadata=dict(description='If set to true the enum entry names will be capitalised'))
    unique: bool = field(default=True, metadata=dict(
        description='If set to true the enum entry will be check for uniqueness. Special entries like "_max", "_min", "_count" are ignored for this purpose'))


@dataclass
class ModuleDescriptor(Schema):
    module_name: str = field(metadata=dict(description='C module name (file name)'))
    copyright_file: Optional[str] = field(metadata=dict(
        description='Path to file containing copyright statement to insert into header files. Can be empty'))
    project_name: Optional[str] = field(metadata=dict(description='Used to generate header guard'))
    enums: List[EnumDescriptor] = field(default_factory=list, metadata=dict(description='List of enum descriptors'))


@dataclass
class CEnumsSchema(Schema):
    modules: List[ModuleDescriptor] = field(default_factory=list,
                                            metadata=dict(description='List of C module descriptors'))
