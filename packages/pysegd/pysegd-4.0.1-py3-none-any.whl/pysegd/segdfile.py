"""
Read/Write SEG D

:copyright:
    Claudio Satriano (satriano@ipgp.fr)
    Maximilien Lehujeur (maximilien.lehujeur@univ.eiffel)

:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)

:modification 2021: Maximilien Lehujeur
    - drop support to python2
    - rename the field names slightly to avoid charcacters like "/" "-" ...
    - do not remove the un-used fields (replace by None)
    - convert errors due to missing subunit_type or control_unit_type into warnings
    - start headlonly and single trace reading options
    - add source point index

:modification 2022: Maximilien Lehujeur
    - drop dependency to obspy
    - Rewrite the code completely using object oriented syntax
      The header fields and data arrays are decoded only on demand,
      while being transparent for the user

      - TypeDecoder : Base class to handle encoded variables
            Subclasses are used to handle every specific data type used in the headers

      - BlockDecoder : Base class to handle a sequence of bytes in the segdfile as
                       a dictionary whose fields are TypeDecoders
                       this object behaves as a dictionary in a transparent way
                       but internally it decodes the attributes when requested by the user
            Subclasses are used to handle all specific header blocks in the file

      - SegdFile : The main class that contains all the BlockDecoders of the header
                   plus the traces stored as a list of SegdTraces

"""
import os.path
from typing import List, Dict, Optional

import numpy as np

from pysegd.blockdecoders import \
    BlockDecoder,\
    GeneralHeaderBlock1Decoder, GeneralHeaderBlock2Decoder, GeneralHeaderBlock3Decoder, \
    ScanTypeHeaderBlockDecoder, ExtendedHeaderBlockDecoder, ExternalHeaderBlockDecoder, \
    TraceHeaderBlockDecoder, TraceHeaderExternalBlock1Decoder, \
    TraceHeaderExternalBlock2Decoder, TraceHeaderExternalBlock3Decoder, \
    TraceHeaderExternalBlock4Decoder, TraceHeaderExternalBlock5Decoder, \
    TraceHeaderExternalBlock6Decoder, TraceHeaderExternalBlock7Decoder, \
    TraceDataBlockDecoder


class SegdFileFormatError(Exception):
    pass


class SegdTraceHeader(BlockDecoder):
    """
    Unlike other Blockdecoders, this object has several sub-blockdecoders
    __getitem__ is adjusted so that used won't notice
    """
    def __init__(self, fid):
        BlockDecoder.__init__(self, buffer=b'', buffer_start=fid.tell())
        _decoders = {
            1: TraceHeaderExternalBlock1Decoder,
            2: TraceHeaderExternalBlock2Decoder,
            3: TraceHeaderExternalBlock3Decoder,
            4: TraceHeaderExternalBlock4Decoder,
            5: TraceHeaderExternalBlock5Decoder,
            6: TraceHeaderExternalBlock6Decoder,
            7: TraceHeaderExternalBlock7Decoder}

        self.trace_header_block = TraceHeaderBlockDecoder(fid.read(20), buffer_start=fid.tell() - 20)
        trace_header_extension = self.trace_header_block.trace_header_extension
        if trace_header_extension >= 8:
            raise SegdFileFormatError(f'unexpected trace_header_extension = {trace_header_extension} ??')

        self.trace_header_external_blocks = {}
        for n in range(1, trace_header_extension + 1):
            kwargs = {}
            if n == 7:
                # for block 7, take the subunit type from trace header block 6
                kwargs = {'subunit_type': self.trace_header_external_blocks[6].subunit_type}

            self.trace_header_external_blocks[n] =\
                _decoders[n](fid.read(32),
                            buffer_start = fid.tell() - 32,
                            **kwargs)

    def decode_all(self):
        """overwrite default behavior"""
        self.trace_header_block.decode_all()
        for trace_header_external_block in self.trace_header_external_blocks.values():
            trace_header_external_block.decode_all()

    def bytes(self):
        """overwrite default behavior"""
        bytes_out = self.trace_header_block.bytes()
        for trace_header_external_block in self.trace_header_external_blocks.values():
            bytes_out += trace_header_external_block.bytes()

        return bytes_out

    def __getitem__(self, item):
        """overwrite default behavior"""
        try:
            return self.trace_header_block[item]
        except KeyError:
            for trace_header_external_block in self.trace_header_external_blocks.values():
                try:
                    return trace_header_external_block[item]
                except KeyError:
                    continue

        raise KeyError(item)

    def items(self):
        """overwrite default behavior"""
        for item in self.trace_header_block.items():
            yield item

        for trace_header_external_block in self.trace_header_external_blocks.values():
            for item in trace_header_external_block.items():
                yield item

    def __str__(self):
        """overwrite default behavior"""
        s = str(self.trace_header_block)
        for trace_header_external_block in self.trace_header_external_blocks.values():
            s += str(trace_header_external_block)
        return s


class SegdTrace(object):
    def __init__(self,
                 trace_header: SegdTraceHeader,
                 trace_data: TraceDataBlockDecoder):
        self.trace_header = trace_header
        self.trace_data = trace_data

    def bytes(self):
        return self.trace_header.bytes() + self.trace_data.bytes()

    @property
    def npts(self):
        return self.trace_data.npts


class SegdFile(object):
    # declare the types of the attributes
    general_header_block1: GeneralHeaderBlock1Decoder
    general_header_block2: GeneralHeaderBlock2Decoder
    general_header_block3: GeneralHeaderBlock3Decoder
    scan_types_header: Dict[int, ScanTypeHeaderBlockDecoder]
    extended_header: ExtendedHeaderBlockDecoder
    external_header: ExternalHeaderBlockDecoder
    segd_traces: List[SegdTrace]
    _detrend_coeffs: Optional[List[np.ndarray]]

    def __init__(self, filename: str, verbose: bool=False):

        self.verbose = verbose
        with open(filename, 'rb') as fid:
            if verbose: print("general_header start position", fid.tell())
            self.read_general_header(fid)

            if verbose: print("scan_types start position", fid.tell())
            self.read_scan_types_header(fid)

            if verbose: print("extended_header start position", fid.tell())
            self.read_extended_header(fid)

            if verbose: print("external_header start position", fid.tell())
            self.read_external_header(fid)

            if verbose: print("trace_headers start position", fid.tell())
            self.read_segd_traces(fid)

    @property
    def n_channel_sets_per_record(self):
        """shortcut"""
        return self.general_header_block1.n_channel_sets_per_record

    @property
    def extended_header_length(self):
        """shortcut"""
        return self.general_header_block1.extended_header_length

    @property
    def external_header_length(self):
        """shortcut"""
        external_header_length = self.general_header_block1.external_header_length
        if external_header_length == 0xFF:
            external_header_length = self.general_header_block2.external_header_blocks
        return external_header_length

    def read_general_header(self, fid):
        self.general_header_block1 = GeneralHeaderBlock1Decoder(fid.read(32), buffer_start=fid.tell()-32)
        self.general_header_block2 = GeneralHeaderBlock2Decoder(fid.read(32), buffer_start=fid.tell()-32)
        self.general_header_block3 = GeneralHeaderBlock3Decoder(fid.read(32), buffer_start=fid.tell()-32)

    def read_scan_types_header(self, fid):
        self.scan_types_header = {}

        for _ in range(1, self.n_channel_sets_per_record + 1):

            scan_type_header_block = \
                ScanTypeHeaderBlockDecoder(fid.read(32), buffer_start=fid.tell()-32)

            if scan_type_header_block.scan_type_header == 0:
                # assume that this block is not used (all 0)
                continue

            channel_set_number = scan_type_header_block.channel_set_number
            self.scan_types_header[channel_set_number] = scan_type_header_block

    def read_extended_header(self, fid):
        self.extended_header = \
            ExtendedHeaderBlockDecoder(
                fid.read(self.extended_header_length * 32),
                buffer_start=fid.tell() - self.extended_header_length * 32)

    def read_external_header(self, fid):
        self.external_header = \
            ExternalHeaderBlockDecoder(
                fid.read(self.external_header_length * 32),
                buffer_start=fid.tell() - self.external_header_length * 32)

    def read_segd_traces(self, fid):

        number_of_samples_in_trace = self.extended_header.number_of_samples_in_trace
        total_number_of_traces = self.extended_header.total_number_of_traces
        sampling_interval_in_sec = self.extended_header.sample_interval_in_microsec * 1e-6
        gps_time_of_acquisition = self.extended_header.gps_time_of_acquisition

        self.segd_traces = []
        for ntrace in range(total_number_of_traces):
            trace_header = SegdTraceHeader(fid)
            trace_data_decoder = TraceDataBlockDecoder(
                fid.read(4 * number_of_samples_in_trace),
                buffer_start=fid.tell() - 4 * number_of_samples_in_trace)

            segd_trace = SegdTrace(
                trace_header=trace_header,
                trace_data=trace_data_decoder)

            # segd_trace.obspy_header = {
            #     # gps_time_of_acquisition is more accurate than
            #     # self.general_header_block1.time if available
            #     "starttime": gps_time_of_acquisition,
            #     "delta": sampling_interval_in_sec,
            #     "npts": number_of_samples_in_trace,
            #     }

            self.segd_traces.append(segd_trace)

    def decode_all(self):
        self.general_header_block1.decode_all()
        self.general_header_block2.decode_all()
        self.general_header_block3.decode_all()
        for channel_set_number, scan_type_header in self.scan_types_header.items():
            scan_type_header.decode_all()
        self.extended_header.decode_all()
        self.external_header.decode_all()
        for segd_trace in self.segd_traces:
            segd_trace.trace_header.decode_all()
            segd_trace.trace_data.decode_all()

    def bytes(self):

        bytes_out = self.general_header_block1.bytes()
        bytes_out += self.general_header_block2.bytes()
        bytes_out += self.general_header_block3.bytes()

        for channel_set_number in range(1, self.n_channel_sets_per_record + 1, 1):
            try:
                bytes_out += self.scan_types_header[channel_set_number].bytes()
            except KeyError:
                # scan_type_header block was not kept because it was all 0
                bytes_out += b"\x00" * 32

        # extended_header_length = self.general_header_block1.extended_header_length
        # self.extended_header = ExtendedHeaderBlockDecoder(fid.read(extended_header_length * 32))
        bytes_out += self.extended_header.bytes()
        bytes_out += self.external_header.bytes()

        for segd_trace in self.segd_traces:
            bytes_out += segd_trace.bytes()

        return bytes_out

    def __str__(self):
        s = "#" * 50 + " GENERAL_HEADER\n"
        s += "=" * 30 + " GENERAL_HEADER_BLOCK1\n"
        s += str(self.general_header_block1)

        s += "=" * 30 + " GENERAL_HEADER_BLOCK2\n"
        s += str(self.general_header_block2)

        s += "=" * 30 + " GENERAL_HEADER_BLOCK3\n"
        s += str(self.general_header_block3)

        s += "#" * 50 + " SCAN_TYPES_HEADER\n"
        for channel_set_number, scan_type_header_block in self.scan_types_header.items():
            s += "=" * 30 + f" SCAN_TYPES_HEADER[CHANNEL_SET_NUMBER={channel_set_number}]\n"

            s += str(scan_type_header_block)

        s += "#" * 50 + " EXTENDED_HEADER\n"
        s += str(self.extended_header)

        s += "#" * 50 + " EXTERNAL_HEADER\n"
        s += str(self.external_header)

        s += "#" * 50 + " TRACES\n"
        for ntrace, trace in enumerate(self.segd_traces):
            s += "=" * 30 + f' TRACE_{ntrace}\n'
            s += str(trace.trace_header)
            s += str(trace.trace_data)
            # for key, val in trace.obspy_header.items():
            #     s += f"{'(' + key + ')': >51s} : {val}\n"

        return s

    def write(self, filename: str, allow_overwrite: bool = False):

        if os.path.exists(filename):
            if not allow_overwrite:
                raise IOError(f'{filename} exists, use allow_overwrite=True, or use another filename')

        if not filename.endswith('.segd'):
            raise IOError(f'filename, must end with ".segd", got {filename}')

        # force total_number_of_traces to match the actual number of traces
        npts0 = self.segd_traces[0].trace_data.npts
        for trace in self.segd_traces[1:]:
            assert trace.trace_data.npts == npts0

        # force total_number_of_traces to match the actual number of traces
        self.extended_header.total_number_of_traces = len(self.segd_traces)
        self.extended_header.number_of_samples_in_trace = npts0

        for ntrace, trace in enumerate(self.segd_traces):
            # leave trace number as is.
            # force number of samples to match the array length in the trace header
            trace.trace_header.trace_header_external_blocks[1].number_of_samples_per_trace = npts0

        with open(filename, 'wb') as fid:
            fid.write(self.bytes())

    def detrend(self):
        """
        remove the linear trend of each trace
        """
        total_number_of_traces = self.extended_header.total_number_of_traces
        number_of_samples_in_trace = self.extended_header.number_of_samples_in_trace
        sampling_interval_in_sec = self.extended_header.sample_interval_in_microsec * 1e-6
        dtype = self.segd_traces[0].trace_data.data_array.dtype

        t = np.arange(number_of_samples_in_trace) * sampling_interval_in_sec
        for trace in self.segd_traces:
            coeffs = np.polyfit(t, trace.trace_data.data_array, deg=1)
            fit = np.polyval(coeffs, t).astype(dtype)
            trace.trace_data.data_array = (trace.trace_data.data_array - fit).astype(dtype)
            assert trace.trace_data.data_array.dtype == dtype

    def decimate(self, decim_rate: int,
                 detrend: bool=True, retrend: bool=True, pad: int=256,
                 anti_alias=0.95, anti_alias_order=4.0, anti_alias_zerophase=True):
        """
        more accurate than downsamp because the decimation rate is provided by the user.
        provides better control on the output sampling rate
        """

        try:
            # scipy is not an official dependency of this package
            from scipy.signal import butter, sosfilt, sosfiltfilt
        except ImportError as err:
            err.args = (str(err), "please install scipy to decimate data")

        assert decim_rate >= 2
        assert isinstance(decim_rate, int)  # assert decim_rate % 1.0 == 0.

        total_number_of_traces = self.extended_header.total_number_of_traces
        number_of_samples_in_trace = self.extended_header.number_of_samples_in_trace
        sampling_interval_in_sec = self.extended_header.sample_interval_in_microsec * 1e-6
        dtype = self.segd_traces[0].trace_data.data_array.dtype

        current_nyquist = 0.5 / sampling_interval_in_sec
        new_nyquist = 0.5 / (sampling_interval_in_sec * decim_rate)

        time_array = np.arange(number_of_samples_in_trace) * sampling_interval_in_sec
        data_array = np.asarray([trace.trace_data.data_array for trace in self.segd_traces]).astype(dtype)

        fit = 0.
        if detrend:
            if False:
                # linear regression : first column a, second column b
                coeffs = np.asarray([np.polyfit(time_array, data_trace, deg=1) for data_trace in data_array])
            else:
                # edge detrend
                v0 = data_array[:, :100].mean(axis=1)[:, np.newaxis]
                v1 = data_array[:, -100:].mean(axis=1)[:, np.newaxis]
                t0 = time_array[:100].mean()
                t1 = time_array[-100:].mean()

                a = (v1 - v0) / (t1 - t0)
                b = v0 - a * t0

                coeffs = np.concatenate((a, b), axis=1)
            fit = (coeffs[:, 0:1] * time_array + coeffs[:, 1:2]).astype(dtype)
            assert fit.shape == data_array.shape
            data_array -= fit
            assert data_array.dtype == dtype

        if pad:
            # padding can be helpfull to mitigate edge effects without taper
            assert detrend, "padding without detrend is not implemented, use non zero value for padding?"
            npad = 256
            data_array = np.concatenate((data_array, np.zeros((total_number_of_traces, npad), dtype)), axis=1)

        if anti_alias:
            assert 0.0 <= anti_alias <= 1.0, anti_alias

            # upper frequency to use for lowpass
            freqmax = anti_alias * new_nyquist

            #ratio to pass to butter
            ratio = freqmax / current_nyquist

            sos = butter(anti_alias_order,
                         [ratio],  # upper freq expressed as the ratio of the nyquist frequency
                         output="sos", btype="low")

            if not anti_alias_zerophase:
                filtered_data = sosfilt(sos=sos, x=data_array, axis=-1)
            else:
                filtered_data = sosfiltfilt(sos=sos, x=data_array, axis=-1)

        else:
            raise Exception('not allowed')

        if pad:
            assert npad
            assert detrend
            filtered_data = filtered_data[:, :-npad]

        # it is now safe to decimate
        data_array = filtered_data[..., ::decim_rate].astype(dtype)

        if detrend and retrend:
            data_array += fit[..., ::decim_rate]

        assert data_array.dtype == dtype

        # set the new attributes
        self.extended_header.sample_interval_in_microsec = self.extended_header.sample_interval_in_microsec * decim_rate
        self.extended_header.number_of_samples_in_trace = data_array.shape[-1]

        for ntrace, trace in enumerate(self.segd_traces):
            trace.trace_data.data_array = data_array[ntrace, ...]


if __name__ == '__main__':
    import sys

    if False:
        sample_file = sys.argv[1]
        segdfile = SegdFile(sample_file)
        segdfile.decode_all()
        with open('toto', 'w') as fid:
            fid.write(str(segdfile))

        segdfile.detrend()
        segdfile.decimate(decim_rate=4, anti_alias=0.95, anti_alias_order=4, anti_alias_zerophase=True)
        with open('tata', 'w') as fid:
            fid.write(str(segdfile))

        segdfile.write('./toto.segd', allow_overwrite=True)


    if False:
        # generate the validation test files,
        # future test will verify that the prompt is consistent with
        # the one generated right know.

        sample_file = sys.argv[1]

        segdfile = SegdFile(sample_file)

        with open(sample_file.replace(".segd", "") + '.raw.txt', 'w') as fid:
            fid.write(str(segdfile))

        segdfile.decode_all()
        with open(sample_file.replace(".segd", "") + '.decoded.txt', 'w') as fid:
            fid.write(str(segdfile))

    if False:
        # search for dysimetries between reading and writting
        # for instsance when unused bytes are not zero in the input file
        # => a NoDecoder object might be missing
        # try gvimdiff tmpraw.txt tmpdecoded.txt and look at the positions prompted in tty

        sample_file = sys.argv[1]

        with open(sample_file, 'rb') as fid:
            fid.seek(0, 2)
            n = fid.tell()
            fid.seek(0, 0)
            c = fid.read(n)

        segdfile = SegdFile(sample_file)

        with open('tmpraw.txt', 'w') as fid:
            fid.write(str(segdfile))

        segdfile.decode_all()
        with open('tmpdecoded.txt', 'w') as fid:
            fid.write(str(segdfile))

        b = segdfile.bytes()
        with open('tmprecoded.txt', 'w') as fid:
            fid.write(str(segdfile))

        with open('tmprecoded.segd', 'wb') as fid:
            fid.write(b)

        segdfile1 = SegdFile('tmprecoded.segd')
        segdfile1.decode_all()
        with open('tmpreloaded.txt', 'w') as fid:
            fid.write(str(segdfile1))

        # print(b)
        if b == c:
            print('ok')
        else:
            for n, (i, j) in enumerate(zip(b, c)):
                if i != j:
                    print(n, i, j)  # diverging position
            print('error')
