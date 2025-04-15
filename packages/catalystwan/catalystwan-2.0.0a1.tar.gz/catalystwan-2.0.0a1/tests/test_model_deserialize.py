from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from catalystwan.core.models.deserialize import deserialize


def test_simple_deserialize():
    @dataclass
    class Model:
        int_field: int
        bool_field: bool
        str_field: str
        literal_field: Literal["test", 1]

    data = {
        "int_field": 1,
        "bool_field": True,
        "str_field": "test",
        "literal_field": "test",
    }
    m = deserialize(Model, **data)

    assert m.int_field == 1
    assert m.bool_field is True
    assert m.str_field == "test"
    assert m.literal_field == "test"


def test_simple_cast():
    @dataclass
    class Model:
        int_field: int
        str_field: str
        literal_field: Literal["test", 1]

    data = {"int_field": "1", "str_field": 1, "literal_field": "1"}
    m = deserialize(Model, **data)

    assert m.int_field == 1
    assert m.str_field == "1"
    assert m.literal_field == 1


def test_optional():
    @dataclass
    class Model:
        int_field: Optional[int]
        str_field: Optional[str]
        bool_field: Optional[bool] = None

    data = {
        "int_field": "1",
        "str_field": None,
    }
    m = deserialize(Model, **data)

    assert m.int_field == 1
    assert m.str_field is None
    assert m.bool_field is None


def test_list():
    @dataclass
    class Model:
        list_field: List[int]

    data = {
        "list_field": [1, "2"],
    }
    m = deserialize(Model, **data)

    assert m.list_field == [1, 2]


def test_union():
    @dataclass
    class Model:
        union_field: Union[IPv6Address, IPv4Address]

    data = {"union_field": "10.0.0.1"}
    m = deserialize(Model, **data)

    assert m.union_field == IPv4Address("10.0.0.1")


def test_submodel():
    @dataclass
    class Submodel:
        int_field: int

    @dataclass
    class Model:
        submodel_field: Submodel

    data = {"submodel_field": {"int_field": 1}}

    m = deserialize(Model, **data)

    assert isinstance(m.submodel_field, Submodel) is True
    assert m.submodel_field.int_field == 1


def test_direct_init():
    @dataclass
    class Submodel:
        int_field: int

    @dataclass
    class Model:
        int_field: int
        bool_field: bool
        str_field: str
        literal_field: Literal["test", 1]
        union_field: Union[IPv6Address, IPv4Address]
        submodel_field: Submodel

    m = Model(
        int_field=1,
        bool_field=True,
        str_field="test",
        literal_field="test",
        union_field=IPv4Address("10.0.0.1"),
        submodel_field=Submodel(int_field=1),
    )

    assert m.int_field == 1
    assert m.bool_field is True
    assert m.str_field == "test"
    assert m.literal_field == "test"
    assert m.union_field == IPv4Address("10.0.0.1")
    assert m.submodel_field.int_field == 1
    assert isinstance(m.submodel_field, Submodel)
