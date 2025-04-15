from typing import Union, List
from abc import ABCMeta
from struct import unpack, pack
import string
from datetime import datetime, timezone, timedelta

import numpy as np

from pysegd.decoding import TypeDecoder
from pysegd.headerfields import OPERATING_MODES


PRINTABLE_ASCII_VALUES = list(map(ord, string.printable))
GPS_EPOCH = datetime(
            year=1980, month=1, day=6,
            hour=0, minute=0, second=0,
            microsecond=0,  # < _gps_microseconds here may lead to Overflow
            tzinfo=timezone.utc)


class NoDecoder(TypeDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in:bytes) -> bytes:
        return bytes_in

    def encode(self, value: bytes) -> bytes:
        return value


# ============ "STANDARD" DATA TYPES
class BCDDecoder(TypeDecoder, metaclass=ABCMeta):
    """
    Decode Binary Code Decimals of arbitrary length
    """

    def decode(self, bytes_in: bytes) -> int:
        """Decode arbitrary length binary code decimals."""
        try:
            # in bcd all hexadecimal digits (4 bits) correspond to numbers between 0 and 9
            # so the hexadecimal representation of the byte correspond to the desired number
            # assumming that heaxdecimal caraters a to f are not used => otherwise ValueError
            value = int(bytes_in.hex())

        except ValueError:
            raise ValueError(f"{bytes_in} is not a binary code decimal")

        return value

    def encode(self, value: int) -> bytes:
        # convert to string : 2 digits per byte, pad with zeros
        fmt = f"%0{self.byte_number * 2}d"
        try:
            bytes_out = bytes().fromhex(fmt % value)
        except ValueError:
            raise ValueError(self.__class__, value, fmt % value, )
        return bytes_out


class LeftBCDDecoder(BCDDecoder, metaclass=ABCMeta):
    """
    Decode the leftmost 4 bits of a byte as Binary Code Decimal
    """
    r1: int = 0
    def decode(self, bytes_in: bytes) -> int:
        assert len(bytes_in) == 1
        self.r1 = bytes_in[0] & 0x0F
        return BCDDecoder.decode(self, bytes_in=bytes([bytes_in[0] >> 4]))

    def encode(self, value: int) -> bytes:
        # convert to string : 2 digits per byte, pad with zeros
        if not 0 <= value <= 9:
            raise ValueError(int)
        fmt = f"%1d" + bytes([self.r1]).hex()[-1]  # replace the backed up right side of the byte
        try:
            bytes_out = bytes().fromhex(fmt % value)
        except ValueError:
            raise ValueError(self.__class__, value, fmt % value, )
        return bytes_out


class RightBCDDecoder(BCDDecoder, metaclass=ABCMeta):
    """
    Decode the rightmost 4 bits of a byte as Binary Code Decimal
    """
    def decode(self, bytes_in: bytes) -> int:
        assert len(bytes_in) == 1
        return BCDDecoder.decode(self, bytes_in=bytes([bytes_in[0] & 0x0F]))

    def encode(self, value: int) -> bytes:
        # convert to string : 2 digits per byte, pad with zeros
        if not 0 <= value <= 9:
            raise ValueError(int)
        fmt = f"0%1d"
        try:
            bytes_out = bytes().fromhex(fmt % value)
        except ValueError:
            raise ValueError(self.__class__, value, fmt % value, )
        return bytes_out


class UIntDecoder(TypeDecoder, metaclass=ABCMeta):
    """
    Decode unsigned integer of arbitrary length, big endian
    """
    def decode(self, bytes_in: bytes) -> int:
        """Decode unsigned integer of arbitrary length, big endian"""
        return int.from_bytes(bytes_in, byteorder="big", signed=False)

    def encode(self, value: int) -> bytes:
        """Re-encode unsigned integer
        using self.byte_number
        big endian"""
        return int.to_bytes(value, length=self.byte_number, byteorder="big", signed=False)


class Uint32ArrayDecoder(UIntDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> np.ndarray:
        assert not len(bytes_in) % 4
        return np.frombuffer(bytes_in, dtype=np.dtype('>i4'))

    def encode(self, value: np.ndarray) -> bytes:
        bytes_out = bytes()
        for _ in value:
            bytes_out += int.to_bytes(int(_), length=4, byteorder="big", signed=True)

        return bytes_out


class BoolDecoder(TypeDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> bool:
        """Decode unsigned ints as booleans."""
        return int.from_bytes(bytes_in, byteorder="big", signed=False) > 0

    def encode(self, value: bool) -> bytes:
        if value:
            return b'\x01'.rjust(self.byte_number, b'\x00')
        else:
            return self.byte_number * b'\x00'


class IntDecoder(TypeDecoder, metaclass=ABCMeta):
    """Two's complement signed integer bigendian"""

    def decode(self, bytes_in: bytes) -> int:
        """Decode two's complement signed integer of arbitrary length, big endian"""
        return int.from_bytes(bytes_in, byteorder="big", signed=True)

    def encode(self, value: int) -> bytes:
        return int.to_bytes(value, length=self.byte_number, byteorder="big", signed=True)


class FractionDecoder(TypeDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> float:
        """Decode positive binary fractions.
        """
        assert len(bytes_in) == 2
        if int.from_bytes(bytes_in, signed=False, byteorder="big") != 0:
            raise NotImplementedError(
                'unsure about the unpacking of fractional numbers, ok only if it is 0 for now')

        # version from Claudio Satriano (ML unsure)
        bit = ''.join('{:08b}'.format(b) for b in bytes_in)
        return sum(int(x) * 2 ** -n for n, x in enumerate(bit, 1))

    def encode(self, value: float) -> bytes:
        assert 0 <= value <= 1.0, ValueError()
        if value != 0.:
            raise NotImplementedError(
                'unsure about the unpacking of fractional numbers, ok only if it is 0 for now')
        else:
            return b'\x00\x00'


class IntThenFractionDecoder(IntDecoder, FractionDecoder, metaclass=ABCMeta):
    def decode(self, bytes_in: bytes) -> float:
        assert len(bytes_in) == 5
        value = 1.0 * IntDecoder.decode(self, bytes_in[:3])
        value += FractionDecoder.decode(self, bytes_in[3:])
        return value

    def encode(self, value: int) -> bytes:
        bytes_out = bytearray(b'\x00' * 5)
        bytes_out[:3] = IntDecoder.encode(self, int(value))[-3:]
        bytes_out[3:] = FractionDecoder.encode(self, (value % 1.0))[:2]
        return bytes(bytes_out)


class FloatDecoder(TypeDecoder, metaclass=ABCMeta):
    def decode(self, bytes_in: bytes) -> Union[float, None]:
        """Decode single-precision floats."""
        # TODO : not tested completely

        if not isinstance(bytes_in, bytes):
            raise TypeError(f"expect bytes, got {type(bytes_in)}")

        if not 1 <= len(bytes_in) <= 4:
            raise ValueError(f"bytes_in must have 1 to 4 bytes")

        f = unpack('>f', bytes_in.rjust(4, b'\x00'))[0]
        if np.isnan(f):
            f = None

        return f

    def encode(self, value: Union[float, None]) -> bytes:
        if value is None:
            bytes_out = b'\xff' * 4
        else:
            bytes_out = pack('>f', value)
            # assert len(bytes_out) == 4
            # if self.byte_number != 4:
            #     print(bytes_out, self.byte_number)
            #     bytes_out = bytes_out[-self.byte_number:]  # unsure

        return bytes_out


class DoubleDecoder(TypeDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> float:
        """Decode double-precision floats."""
        # TODO : not tested

        return unpack('>d', bytes_in)[0]

    def encode(self, value: float) -> bytes:
        return pack('>d', value)


class AsciiDecoder(TypeDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> Union[None, str]:
        """Decode ascii."""
        # TODO : not tested
        s = ''.join(chr(x) for x in bytes_in if x in PRINTABLE_ASCII_VALUES)
        if not s:
            s = None
        return s

    def encode(self, value: Union[None, str]) -> bytes:
        if value is None:
            bytes_out = b'\x00' * self.byte_number

        else:
            bytes_out = bytes(ord(_) for _ in value).ljust(self.byte_number, b'\x00')

        return bytes_out


class GPSTimeOfAcquisitionDecoder(TypeDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> datetime:
        gps_microseconds = unpack('>Q', bytes_in)[0]

        gps_time_of_acquisition = GPS_EPOCH +\
            timedelta(seconds=gps_microseconds / 1e6)
        return gps_time_of_acquisition

    def encode(self, value: datetime) -> bytes:
        gps_microseconds = (value - GPS_EPOCH).total_seconds() * 1e6
        gps_microseconds = int(gps_microseconds)
        bytes_out = pack('>Q', gps_microseconds)
        return bytes_out


class ArrayDecoder(TypeDecoder):

    def __init__(self, npts: int):
        super().__init__(byte_start=0, byte_number=4 * npts)


class TraceData32bitIEEEDemulDecoder(ArrayDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> np.ndarray:
        return np.frombuffer(bytes_in, dtype=np.dtype('>f4'))

    def encode(self, value: np.ndarray) -> bytes:

        bytes_out = pack('>%df' % len(value), *value)
        return bytes_out

    @property
    def npts(self):
        """a dynamic control of the number of samples"""
        if self.is_encoded:
            return len(self._value // 4)

        else:
            return len(self._value)


# ============ "SPECIFIC" DATA TYPES
class RevisionBCDDecoder(BCDDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> float:
        major = BCDDecoder.decode(self, bytes_in=bytes_in[0:1])
        minor = BCDDecoder.decode(self, bytes_in=bytes_in[1:2])
        return 1.0 * major + 0.1 * minor

    def encode(self, value: float) -> bytes:

        bytes_out = bytearray(b'\x00\x00')
        bytes_out[0:1] = BCDDecoder.encode(self, value=int(value))[1:]  # major
        bytes_out[1:2] = BCDDecoder.encode(self, value=int((value * 10) % 10))[1:]  # minor
        return bytes(bytes_out)


class StackSignUIntDecoder(UIntDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> int:
        value = UIntDecoder.decode(self, bytes_in)
        if value == 2:
            value = -1
        return value

    def encode(self, value: int) -> bytes:
        if value == -1:
            value = 2
        return UIntDecoder.encode(self, value)


class OperatingModeUIntDecoder(UIntDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> List[str]:

        operating_mode_code = UIntDecoder.decode(self, bytes_in)
        value = []
        for operating_mode_bytemask, operating_mode in OPERATING_MODES.items():
            if (operating_mode_code & operating_mode_bytemask):
                value.append(operating_mode)

        return value

    def encode(self, value: List[str]) -> bytes:
        # value = ['microseismic']  # test
        operating_mode_code = 0  # b'\x00' * 4

        keys = OPERATING_MODES.values()
        for v in value:
            assert v in keys, (v, keys)

        for operating_mode_bytemask, operating_mode in OPERATING_MODES.items():
            if operating_mode in value:
                operating_mode_code |= operating_mode_bytemask

        operating_mode_code = int.to_bytes(operating_mode_code, length=4, byteorder="big", signed=False)
        return operating_mode_code

class FirstTimeingWordDecoder(UIntDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> float:
        return UIntDecoder.decode(self, bytes_in) / 256.0

    def encode(self, value: float) -> bytes:
        return UIntDecoder.encode(self, value=int(round(value * 256.0)))


class TimeBreakWindowDecoder(UIntDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> float:
        assert len(bytes_in) == 3
        return 1.0 * UIntDecoder.decode(self, bytes_in[:2]) \
               + 0.01 * UIntDecoder.decode(self, bytes_in[2:3])

    def encode(self, value: float) -> bytes:
        b1 = int.to_bytes(int(value), length=2, byteorder="big", signed=False)
        b2 = int.to_bytes(int(value * 100. % 100.), length=1, byteorder="big", signed=False)
        bytes_out = b1 + b2
        return bytes_out


class TimeDecoder(BCDDecoder, metaclass=ABCMeta):
    l1: int = 0  # backup the left part (4 first digits) of byte 1

    def decode(self, bytes_in: bytes) -> datetime:
        b_year = bytes_in[0: 1]
        # cancels the leftmost half of the byte 1 (n_additional_blocks)
        self.l1: int = bytes_in[1] & 0xF0  # save the left most part of byte1
        b_jday = bytes([bytes_in[1] & 0x0F]) + bytes_in[2:3]
        b_hour = bytes_in[3: 4]
        b_min = bytes_in[4: 5]
        b_sec = bytes_in[5: 6]

        year = BCDDecoder.decode(self, b_year) + 2000
        jday = BCDDecoder.decode(self, b_jday)
        hour = BCDDecoder.decode(self, b_hour)
        minute = BCDDecoder.decode(self, b_min)
        second = BCDDecoder.decode(self, b_sec)

        value = datetime(
            year=year, month=1, day=1,  # cannot set julday at initiation
            hour=hour, minute=minute, second=second, microsecond=0,
            tzinfo=timezone.utc)
        value += timedelta(seconds=(jday - 1) * 24. * 3600.)
        assert value.year == year, "the julian day must agrees with the number of days in the current year"
        return value

    def encode(self, value: datetime) -> bytes:

        begin_of_year = datetime(
            year=value.year, month=1, day=1,
            hour=value.hour, minute=value.minute, second=value.second, microsecond=0,
            tzinfo=timezone.utc)
        delta: timedelta = value - begin_of_year

        decoder1 = BCDDecoder(byte_number=1)
        decoder2 = BCDDecoder(byte_number=2)
        b_year = decoder1.encode(value.year - 2000)
        b_jday = decoder2.encode(delta.days + 1)  # leftmost half of the first byte to be completed
        b_jday = bytes([self.l1 | b_jday[0], b_jday[1]])  # restore the backed up byte data
        b_hour = decoder1.encode(value.hour)
        b_min = decoder1.encode(value.minute)
        b_sec = decoder1.encode(value.second)
        return b_year + b_jday + b_hour + b_min + b_sec


class FileNumberDecoder(BCDDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> int:

        if bytes_in == b'\xff\xff':
            # if file number larger than 9999 -> 65535 (overflow)
            return 0xFFFF  # = 65535

        return BCDDecoder.decode(self, bytes_in)

    def encode(self, value: int) -> bytes:
        if value == 65535:
            return b'\xff\xff'

        return BCDDecoder.encode(self, value)


class GeneralConstantsDecoder(BCDDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> List[int]:
        return [BCDDecoder.decode(self, bytes([b])) for b in bytes_in]

    def encode(self, value: List[int]) -> bytes:
        bytes_out = bytes()
        decoder = BCDDecoder(byte_number=1)
        for intvalue in value:
            bytes_out += decoder.encode(intvalue)
        return bytes_out


class BaseScanIntervalDecoder(BCDDecoder, metaclass=ABCMeta):

    def decode(self, bytes_in: bytes) -> float:
        value = BCDDecoder.decode(self, bytes_in)
        if value < 10:
            value = 1. / value
        else:
            value /= 10.
        return value

    def encode(self, value: float) -> bytes:
        """unsure !!! """
        if value < 1:
            value = int(1. / value)
        else:
            value = int(value * 10)
        return BCDDecoder.encode(self, value)


class RecLenUintDecoder(UIntDecoder, metaclass=ABCMeta):
    l1: int = 0
    def decode(self, bytes_in: bytes) -> int:
        self.l1 = bytes_in[0] & 0xF0
        value = UIntDecoder.decode(self, bytes([bytes_in[0] & 0x0F]) + bytes_in[1:2])
        if value == 0xFFF:
            value = None
        return value

    def encode(self, value) -> bytes:
        if value is None:
            bytes_out = bytes([0x0F | self.l1, 0xFF])
        else:
            raise NotImplementedError("not tested")
            bytes_out = UIntDecoder.encode(self, value)

        return bytes_out


