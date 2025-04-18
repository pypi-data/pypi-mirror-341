import abc
import string
import struct
import typing
from io import BytesIO


class _TypesAbstract(abc.ABC):
    def __init_subclass__(cls, **kwargs):
        def _generic_formatter(field_format: str) -> callable:
            def _format(t: str, size: int) -> _ArrayType:
                return _ArrayType(field_format.format(elements=size, inner_type=t.schema))
            return _format

        def _specific_formatter(field_format: str) -> callable:
            def _format(size: int) -> _Type:
                return _Type(field_format.format(elements=size))
            return _format

        type_prefix = '_typedef_'
        array_prefix = '_arraydef_'
        zstring_prefix = '_zstringdef_'

        simple_type_fields = {}
        array_fields = {}
        zstring_fields = {}

        for field, value in cls.__dict__.items():
            if field.startswith(type_prefix):
                new_function_name = field[len(type_prefix):]
                simple_type_fields[new_function_name] = value
            elif field.startswith(array_prefix):
                new_function_name = field[len(array_prefix):]
                array_fields[new_function_name] = value
            elif field.startswith(zstring_prefix):
                new_function_name = field[len(zstring_prefix):]
                zstring_fields[new_function_name] = value

        for field, value in simple_type_fields.items():
            setattr(cls, field, _Type(value))

        for field, value in zstring_fields.items():
            setattr(cls, field, _ZString())

        for field, value in array_fields.items():
            parameters = tuple(fn for _, fn, _, _ in string.Formatter().parse(value) if fn is not None)
            if len(parameters) == 1:
                setattr(cls, field, _specific_formatter(value))
            elif len(parameters) > 1:
                setattr(cls, field, _generic_formatter(value))


class _Type:
    def __init__(self, schema: str):
        self._schema = schema
        self._data = None
        self.raw = BytesIO(b'\x00' * self.size)

    @property
    def schema(self) -> str:
        return self._schema

    @property
    def size(self) -> int:
        return struct.calcsize(self._schema)

    @property
    def data(self) -> typing.Any:
        return self._data

    @data.setter
    def data(self, value: typing.Any):
        self._data = value

    @property
    def raw(self) -> bytes:
        return struct.pack(self._schema, self.data)

    @raw.setter
    def raw(self, value: BytesIO):
        _data = value.read(self.size)
        self._data = struct.unpack(self._schema, _data)[0]


class _ArrayType(_Type):
    @property
    def raw(self) -> bytes:
        return struct.pack(self._schema, *self.data)

    @raw.setter
    def raw(self, value: BytesIO):
        _data = value.read(self.size)
        self._data = list(struct.unpack(self._schema, _data))


class _ZString(_Type):
    def __init__(self):
        super().__init__('0s')
        self._data = ''

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, value: str):
        pos = value.find('\0')
        if pos < 0:
            pos = len(value)
        self._schema = f'{pos}s'
        self._data = value[:pos]

    @property
    def raw(self) -> bytes:
        return struct.pack(self._schema, self.data.encode()) + b'\0'

    @raw.setter
    def raw(self, value: BytesIO):
        _data = b''
        _next_byte = value.read(1)
        while _next_byte and _next_byte != b'\x00':
            _data += _next_byte
            _next_byte = value.read(1)
        if len(_data):
            self._schema = f'{len(_data)}s'
            self._data = struct.unpack(self._schema, _data)[0].decode()
        else:
            self._schema = '0s'
            self._data = ''


class Types(_TypesAbstract):
    _auto: str = ''

    _typedef_s8 = 'b'
    _typedef_u8 = 'B'
    _typedef_s16 = '<h'
    _typedef_u16 = '<H'
    _typedef_s32 = '<i'
    _typedef_u32 = '<I'
    _typedef_s64 = '<q'
    _typedef_u64 = '<Q'
    _typedef_s16be = '>h'
    _typedef_u16be = '>H'
    _typedef_s32be = '>i'
    _typedef_u32be = '>I'
    _typedef_s64be = '>q'
    _typedef_u64be = '>Q'
    _typedef_float = '<f'
    _typedef_double = '<d'

    s8 = _auto
    u8 = _auto
    s16 = _auto
    s16be = _auto
    u16 = _auto
    u16be = _auto
    s32 = _auto
    s32be = _auto
    u32 = _auto
    u32be = _auto
    s64 = _auto
    s64be = _auto
    u64 = _auto
    u64be = _auto
    float = _auto
    double = _auto


class ArrayTypes(_TypesAbstract):
    _auto: typing.Callable[[int], str]|typing.Callable[[str, int], str] = lambda elements: ''

    _arraydef_array = '{elements}{inner_type}'
    _arraydef_bytearray = '{elements}s'

    array = _auto
    bytearray = _auto


class ZeroTerminatedString(_TypesAbstract):
    _auto = ''

    _zstringdef_zstring = _auto

    zstring = _auto
