from serializer_lib.factory.extensions.parser import Parser
import serializer_lib.parsers.yaml.yamlParser as YAMLParser


class Yaml(Parser):
    def dump(self, obj, fp):
        return YAMLParser.dump(obj, fp)

    def dumps(self, obj):
        return YAMLParser.dumps(obj)

    def load(self, fp):
        return YAMLParser.load(fp)

    def loads(self, s):
        return YAMLParser.loads(s)
