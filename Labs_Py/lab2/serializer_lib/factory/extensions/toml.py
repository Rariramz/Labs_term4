from serializer_lib.factory.extensions.parser import Parser
import serializer_lib.parsers.toml.tomlParser as TOMLParser


class Toml(Parser):
    def dump(self, obj, fp):
        return TOMLParser.dump(obj, fp)

    def dumps(self, obj):
        return TOMLParser.dumps(obj)

    def load(self, fp):
        return TOMLParser.load(fp)

    def loads(self, s):
        return TOMLParser.loads(s)
