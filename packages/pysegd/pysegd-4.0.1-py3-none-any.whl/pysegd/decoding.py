class TypeDecoder(object):
    """
    The root class to decode any data type used in the pysegd file
    the class is not supposed to be used as is, please subclass
    """

    # =========================== private methods
    # please overwrite only for specific uses
    def __init__(self,
                 byte_start: int = 0, byte_number: int = 4,
                 flip_byte: bool = False,
                 table=None, raise_on_key_error: bool = True):
        """
        initiate the decoder object with the positions in the buffer
        :param byte_start: starting position of the encoded variable in the bytes object provided to self.from_buffer
        :param byte_number: the number of bytes to read from the input bytes
        :param flip_byte: reverse the byte order, used only for 1 specific case
        :param table: once decoded, the value is replaced by the corresponding entry in this dictionary if provided
        :param raise_on_key_error: whether to raise an exception if the header field is missing
        """
        self.byte_start = byte_start
        self.byte_number = byte_number
        self.flip_byte = flip_byte

        self.is_encoded = True  # encoding state of self._value
        self._value = None  # the encoded or decoded value
        self.table = table  # dictionary of correspondences is appropriate
        self.raise_on_key_error = raise_on_key_error

    def from_buffer(self, buffer: bytes):
        """
        get the binary value from an input buffer
        """
        self._value = buffer[self.byte_start: self.byte_start + self.byte_number]
        if self.flip_byte:
            self._value = self._value[::-1]

        if not len(self._value) == self.byte_number:
            raise ValueError(
                f'could not read bytes from positions '
                f'{self.byte_start} to {self.byte_start + self.byte_number - 1} '
                f'because the buffer length is {len(buffer)}')

        return self

    def _decode(self):
        """
        This is the private decoding method, the subclasses are suposed to implement the public method decode below
        """
        if not self.is_encoded:
            return

        if not isinstance(self._value, bytes):
            raise TypeError(f"expect bytes, got {type(self._value)}")

        # call the user defined decoder
        self._value = self.decode(self._value)

        # replace the decoded value by the corresp entry in the provided table
        if self.table is not None:

            try:
                self._value = self.table[self._value]

            except KeyError as err:
                err.args = (f'code {self._value} not found in {list(self.table.keys())}',)
                if self.raise_on_key_error:
                    # crash
                    raise err

        # toggle encoding variable
        self.is_encoded = False

    def _encode(self):
        """
        This is the private encoding method, the subclasses are supposed to implement the public method encode below
        """
        if self.is_encoded:
            return

        # if isinstance(self._value, bytes):
        #     raise TypeError('already a bytes object ??')  # yes for NoDecoder it is ok

        if self.table is not None:
            # replace the value by the corresponding key in self.table
            for key, value in self.table.items():
                if self._value == value:
                    self._value = key
                    break
            else:
                if self.raise_on_key_error:
                    raise Exception(f"{self._value} not in the values of {type(self)}.table {self.table}")
                else:
                    pass

        try:
            self._value = self.encode(self._value)
        except (TypeError, NotImplementedError) as err:
            err.args = (f'could not encode {self._value} as {type(self)}, reason : {str(err)}', )
            raise err
        except Exception as err:
            err.args = (f'unexpected exception type', type(err), str(err))
            raise err

        # toggle encoding variable
        self.is_encoded = True

    @property
    def decoded_value(self):
        """
        An alias that will run the decoding method if not already done
        """
        if self.is_encoded:
            self._decode()
        return self._value

    @property
    def encoded_value(self):
        """
        An alias that will run the encoding method if required
        """
        if not self.is_encoded:
            self._encode()
        return self._value

    # =========================== public methods
    # please implement these methods for any subclass
    def decode(self, bytes_in: bytes):
        """please just return the decoded value of bytes_in"""
        raise NotImplementedError('this method must be implemented in each subclass')

    def encode(self, value):
        """please just return the encoded value of value"""
        raise NotImplementedError('this method must be implemented in each subclass')


class TypeDecoderBuilder(object):
    """avoid storing an instantiated class
    TypeDecoderBuilder(SomeDecoderClass, 0, 12) contains all necessary items
    to generate mydecoder = SomeDecoderClass(0, 12), but the object is not instantiated yet
    use get_decoder to instantiate the decoder
    """
    def __init__(self, decoder_type: type, *args, **kwargs):
        """
        decoder_type : the class to use e.g. BCDDecoder
        args, kwargs : the arguments to pass to the __init__ method of decoder_type at initiation
        """
        self.decoder_type = decoder_type
        self.args = args
        self.kwargs = kwargs

    def init_decoder(self) -> TypeDecoder:
        return self.decoder_type(*self.args, **self.kwargs)


class BlockDecoder(dict):

    buffer_structure = {
        # e.g. 'value1': TypeDecoderBuilder(TypeDecoder, 0, 4),
        # e.g. 'value2': TypeDecoderBuilder(TypeDecoder, 4, 4),
    }
    buffer_length = 0
    buffer_start = 0  # first position of this buffer in the file

    def __init__(self, buffer: bytes, buffer_start: int=0):

        # init the dict class, i.e. create an empty dict
        super(BlockDecoder, self).__init__()
        self.buffer_length = len(buffer)
        self.buffer_start = buffer_start

        # for every entry in the block,
        for attribute_name, buffer_entry in self.buffer_structure.items():
            if not isinstance(buffer_entry, TypeDecoderBuilder):
                raise ValueError('the BufferDecoder must include BufferEntry objects only')

            # initiate the decoder and store it as an attribute of this object
            self[attribute_name] = buffer_entry.init_decoder().from_buffer(buffer)

    # ============ NOTE : all conventional accesses to items of this object will force the decoding
    def get_decoder(self, item):
        # because getitem and getattr are bypassed
        decoder = dict.__getitem__(self, item)
        return decoder

    def __getitem__(self, item):
        """
        When the user request an attribute in this class,
        The decoder checks if the value is decoded and decode it if not
        """
        decoder = self.get_decoder(item)
        return decoder.decoded_value

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        """let user modify a field,
        assume he provides decoded values, with the right data type !!!
        """
        try:
            decoder = self.get_decoder(key)
            decoder._value = value  # place the new value,
            decoder.is_encoded = False  # notice that the decoder is not encoded
        except KeyError:
            dict.__setattr__(self, key, value)  # regular attributes

    def items(self):
        """items forces the decoding"""
        for attribute_name, decoder in dict.items(self):
            yield attribute_name, decoder.decoded_value

    def decode_all(self):
        list(self.items())

    # ============
    def bytes(self) -> bytes:
        """
        reconstitute the buffer from self, the default behavior
        consists in (re)encoding all decoders in dict.items(self)
        it will leave the block re-encoded
        warning:
            using self.items implies asking for decoded attributes,
            use dict.items(self) to access the decoders
        """

        bytes_out = bytearray(b'\x00' * self.buffer_length)

        for attribute_name, decoder in dict.items(self):
            # bytes_out += decoder.encoded_value  # force encoding !!
            decoder: TypeDecoder
            b = decoder.encoded_value
            if decoder.flip_byte:
                b = b[::-1]
            bytes_out[decoder.byte_start: decoder.byte_start + decoder.byte_number] = b
            # print(self.buffer_length, len(bytes_out), attribute_name)
        return bytes(bytes_out)

    # ============ Note : display as is (encoded or decoded)
    def __str__(self):
        s = ""  # f"------------------------------------ {self.__class__.__name__}\n"
        for attribute_name, decoder in dict.items(self):
            # s += f"[{decoder.byte_start:4d},{decoder.byte_number:3d}]"  # add positions in the buffer
            s += f"[{self.buffer_start + decoder.byte_start:4d},{decoder.byte_number:3d}]"  # add positions in the file, assumes buffer start is provided
            s += f"{attribute_name:>50s}"
            if decoder.is_encoded:
                assert isinstance(decoder._value, bytes)
                s += "* : "
                s += "\\x"
                if len(decoder._value) > 10:
                    s += decoder._value[:5].hex() + "..."
                    s += decoder._value[-5:].hex() + "\n"

                else:
                    s += decoder._value.hex() + "\n"

            else:
                s += f"  : {decoder._value}\n"

        return s

    def __repr__(self):
        # otherwise repr calls items that forces the decoding
        return self.__str__()
