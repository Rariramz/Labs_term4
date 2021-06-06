from serializer_lib.factory.parser_factory import ParserFactory
from serializer_lib.factory.serializer import serialize_obj, deserialize_obj
from test_objects import *
import unittest


def serialize_and_compare_obj(obj, tester):
    ser = serialize_obj(obj)
    des = deserialize_obj(ser)
    tester.assertEqual(des, obj)


def serialize_and_compare_func(func, tester):
    ser = serialize_obj(func)
    des = deserialize_obj(ser)
    tester.assertEqual(des(7), func(7))


def parse_and_compare_obj(obj, format, tester):
    parser = ParserFactory.create_serializer(format)
    format = "yml" if format.lower() == "yaml" else format.lower()
    file = f"output.{format}"
    parser.dump(serialize_obj(obj), file)
    result = deserialize_obj(parser.load(file))
    tester.assertEqual(obj, obj)


def parse_and_compare_func(func, format, tester):
    parser = ParserFactory.create_serializer(format)
    format = "yml" if format.lower() == "yaml" else format.lower()
    file = f"output.{format}"
    parser.dump(serialize_obj(func), file)
    result = deserialize_obj(parser.load(file))
    tester.assertEqual(result(5), func(5))


class TestClass(unittest.TestCase):
    def test_serialization_obj(self):
        serialize_and_compare_obj(some_list, self)
        serialize_and_compare_obj(some_dict, self)

    def test_serialization_func(self):
        serialize_and_compare_func(inc, self)
        serialize_and_compare_func(fibonacci, self)
        serialize_and_compare_func(get_vars, self)

    def test_parse_json(self):
        parse_and_compare_obj(some_list, "json", self)
        parse_and_compare_obj(some_list, "jSoN", self)
        parse_and_compare_func(inc, "json", self)
        parse_and_compare_func(inc, "jSoN", self)

    def test_parse_yaml(self):
        parse_and_compare_obj(some_list, "yaml", self)
        parse_and_compare_obj(some_list, "YAMl", self)
        parse_and_compare_func(inc, "yaml", self)
        parse_and_compare_func(inc, "YAMl", self)

    def test_parse_toml(self):
        parse_and_compare_func(inc, "toml", self)
        parse_and_compare_func(inc, "toMl", self)