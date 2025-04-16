import pytest

from palanystorage.engine import create_engine_sync
from palanystorage.schema import StorageConfigSchema
from rich.console import Console

console = Console()

console.print('\n\nConfig example below:', new_line_start=True, )
console.print(
    {
        "dialect": "qiniu/alioss/..",
        "driver": "pal_qiniu/..",
        "root_path": "",
        "max_can_use": 100,
        "bucket": "bucket-name",
        "access_key": "",
        "access_key_secret": "",
        "inside_endpoint": "https://xx.com/",
        "outside_endpoint": "https://yy.com/",
        "region": "NCN/..",
        "upload_url": "https://zz.com",
    },
    new_line_start=True,
)

dict_str = input("\n\nInput config dict: ")

_line = ''
for line in iter(input, _line):
    # print(f'line: {line}')
    dict_str += line

config_dict = eval(dict_str)
config_schema = StorageConfigSchema(**config_dict)


@pytest.fixture
def config(request):
    return config_schema


@pytest.fixture
def engine(request):
    my_engine = create_engine_sync(dialect_name=config_schema.dialect, driver=config_schema.driver, storage_config=config_schema)
    return my_engine

