from serializer_lib.factory.extensions.json import Json
from serializer_lib.factory.extensions.toml import Toml
from serializer_lib.factory.extensions.yaml import Yaml

EXTENSIONS = {
    "json": Json,
    "toml": Toml,
    "yaml": Yaml
}


class ParserFactory(object):
    @staticmethod
    def create_serializer(file_format: str):
        parser = EXTENSIONS.get(file_format.lower(), None)
        if not parser:
            raise ValueError(f'File format \'{file_format}\' is not supported, sorry')
        return parser()
