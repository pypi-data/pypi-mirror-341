import json
from pathlib import Path
from jsonschema import validate

from marshmallow_jsonschema import JSONSchema


def main():
    schema_path = Path(__file__).parent.parent / 'resources' / 'cenum.schema_v1.json'
    data_path = Path(__file__).parent.parent.parent.parent / 'resources' / 'data.egen'
    with schema_path.open(mode='r') as schema_f:
        with data_path.open(mode='r') as data_f:
            schema_json = json.load(schema_f)
            data_json = json.load(data_f)

            validate(instance=data_json, schema=schema_json)

            pass


if __name__ == '__main__':
    main()
