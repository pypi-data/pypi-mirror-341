from c_enum_generator.CGenSchemaProvider import CGenSchemaProvider
from c_enum_generator.schema.CEnumsSchema import CENUM_SCHEMA_ID_V1


def test_get_available_schemas() -> None:
    prov = CGenSchemaProvider()
    schemas = prov.get_available_schemas()
    assert CENUM_SCHEMA_ID_V1 in schemas

    assert len(schemas) == 1


def test_get_schema_none() -> None:
    prov = CGenSchemaProvider()
    schemas = prov.get_schema("")
    assert schemas is None

def test_get_schema_v1() -> None:
    prov = CGenSchemaProvider()
    schema = prov.get_schema(CENUM_SCHEMA_ID_V1)
    assert schema is not  None
    assert schema['$id'] == CENUM_SCHEMA_ID_V1