import random

import pytest

from pybinary.binary_types import ArrayTypes, Types, ZeroTerminatedString
from pybinary.serializable import BinarySerializable


def test_simple_class():
    class Test(BinarySerializable):
        s8 = Types.s8
        u8 = Types.u8
        s16 = Types.s16
        u16 = Types.u16
        s32 = Types.s32
        u32 = Types.u32
        s64 = Types.s64
        u64 = Types.u64
        float = Types.float
        double = Types.double
    obj = Test()
    for field_name, field_value in obj._get_properties().items():
        value = random.randint(0, 255)
        setattr(obj, field_name, value)
        assert getattr(obj, field_name) == value


def test_simple_serialize():
    class Test(BinarySerializable):
        s8 = Types.s8
        u8 = Types.u8
        s16 = Types.s16
        u16 = Types.u16
        s32 = Types.s32
        u32 = Types.u32
        s64 = Types.s64
        u64 = Types.u64
        float = Types.float
        double = Types.double

    assert Test.size() == 1 + 1 + 2 + 2 + 4 + 4 + 8 + 8 + 4 + 8
    data = random.randbytes(Test.size())
    obj = Test.deserialize(data)
    assert obj.serialize() == data


def test_inheritance():
    class TestBase(BinarySerializable):
        s8 = Types.s8
        s16 = Types.s16

    class Test(TestBase):
        s32 = Types.s32

    assert Test.size() == 1 + 2 + 4
    data = random.randbytes(Test.size())
    obj = Test.deserialize(data)
    assert obj.serialize() == data


def test_name_collision():
    class TestBase(BinarySerializable):
        s8 = Types.s8
        s16 = Types.s16
        s32 = Types.s32

    with pytest.raises(TypeError):
        class Test(TestBase):
            s16 = Types.s32


def test_bytearray():
    size = random.randint(1, 100)

    class Test(BinarySerializable):
        bytearray = ArrayTypes.bytearray(size)

    assert Test.size() == size
    data = random.randbytes(size)
    obj =  Test.deserialize(data)
    assert obj.serialize() == data


def test_offset():
    class Test(BinarySerializable):
        s8 = Types.s8
        u8 = Types.u8
        s16 = Types.s16
        u16 = Types.u16

    assert Test.offset(Test.s16) == 2

def test_zstring():
    class Test(BinarySerializable):
        s8 = Types.s8
        zstring = ZeroTerminatedString.zstring
        u8 = Types.u8

    obj = Test()
    test_string = 'aaaaa'
    obj.zstring = test_string
    assert obj.serialize() == b'\0' + test_string.encode() + b'\0\0'
    obj2 = Test.deserialize(b'\0test\0\xff')
    assert obj2.s8 == 0
    assert obj2.zstring == 'test'
    assert obj2.u8 == 0xff


def test_zstring2():
    class Test(BinarySerializable):
        s8 = Types.s8
        zstring = ZeroTerminatedString.zstring
        u8 = Types.u8

    obj2 = Test.deserialize(b'\0test\0\xff')
    obj2.zstring = '12345\x00678'
    assert obj2.zstring == '12345'
    assert obj2.serialize() == b'\x0012345\x00\xff'

def test_zstring3():
    class Test(BinarySerializable):
        s8 = Types.s8
        zstring = ZeroTerminatedString.zstring
        u8 = Types.u8
    obj3 = Test()
    data = obj3.serialize()
    assert Test.deserialize(data).zstring == obj3.zstring
