from serializer_lib.factory.parser_factory import ParserFactory
from serializer_lib.factory.serializer import serialize_obj, deserialize_obj


def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)


parser = ParserFactory.create_serializer("json")
file = "output.json"
parser.dump(serialize_obj(fact), file)
result = deserialize_obj(parser.load(file))
print(result(6))
