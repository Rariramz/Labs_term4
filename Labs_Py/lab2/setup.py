from setuptools import setup

setup(
    name="serializer_lib",
    packages=[
        "serializer_lib",
        "serializer_lib/serializer",
        "serializer_lib/parsers",
        "serializer_lib/factory",
        "serializer_lib/factory/extensions",
        "serializer_lib/parsers/json",
        "serializer_lib/parsers/toml",
        "serializer_lib/parsers/yaml",
    ],
    version="1.0.0",
    author="rariramz",
    description='console serializer',
    scripts=["bin/console_serializer"]
)
