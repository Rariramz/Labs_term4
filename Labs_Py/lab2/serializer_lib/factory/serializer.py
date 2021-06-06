from serializer_lib.serializer.serializer import serialize_obj, deserialize_obj


class Serializer:
    @staticmethod
    def serialize_obj(self, obj: object):
        return serialize_obj(obj)

    @staticmethod
    def deserialize_obj(self, obj: dict):
        return deserialize_obj(obj)
