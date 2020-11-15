import json

from rip.ripping_guide_schema import RIPPING_GUIDE_SCHEMA


def test_ripping_guide_schema_in_sync():
    schema_dict_from_file = None
    with open('rip/ripping-guide-schema.json') as schema_file:
        schema_dict_from_file = json.load(schema_file)
    assert schema_dict_from_file == RIPPING_GUIDE_SCHEMA
