from serializer_lib.factory.extensions.parser import Parser
import serializer_lib.parsers.json.jsonParser as JSONParser


class Json(Parser):
    def dump(self, obj, fp):
        return JSONParser.dump(obj, fp)

    def dumps(self, obj):
        return JSONParser.dumps(obj)

    def load(self, fp):
        return JSONParser.load(fp)

    def loads(self, s):
        return JSONParser.loads(s)
