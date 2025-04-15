"""
Code tables (SERCEL format)
"""

FORMAT_CODES = {
    8058: "32 bit IEEE demultiplexed",
    # Not Implemented in this version
    # 8015: "20 bit binary demultiplexed",
    # 8022: "8 bit quaternary demultiplexed",
    # 8024: "16 bit quaternary demultiplexed",
    # 8036: "24 bit 2's compliment integer demultiplexed",
    # 8038: "32 bit 2's compliment integer demultiplexed",
    # 8042: "8 bit hexadecimal demultiplexed",
    # 8044: "16 bit hexadecimal demultiplexed",
    # 8048: "32 bit hexadecimal demultiplexed",
    #  200: "Illegal, do not use",
    # 0000: "Illegal, do not use",
    }

DESCALE_MULTIPLIER = {
    0xAF6D: 1600,
    0xB76D: 400,
    0xAD03: 2500,
    0xB503: 650,
    # sanity value:
    0: 1,
    }

RECORD_TYPES = {
    8: 'normal',
    2: 'test record',
    }

SOURCE_TYPES = {
    0: 'no source',
    1: 'impulsive',
    2: 'vibro',
    }

TEST_RECORD_TYPES = {
    0: 'normal record',
    1: 'field (sensor) noise',
    2: 'field (sensor) tilt',
    3: 'field (sensor) crosstalk',
    4: 'instrument noise',
    5: 'instrument distortion',
    6: 'instrument gain/phase',
    7: 'instrument crosstalk',
    8: 'instrument common mode',
    9: 'synthetic',
    10: 'field (sensor) pulse',
    11: 'instrument pulse',
    12: 'field (sensor) distortion',
    13: 'instrument gravity',
    14: 'field (sensor) leakage',
    15: 'field (sensor) resistance',
    }

SPREAD_TYPES = {
    0: None,
    1: 'generic',
    2: 'absolute',
    }

NOISE_ELIMINATION_TYPES = {
    1: 'off',
    2: 'diversity stack',
    3: 'historic',
    4: 'enhanced diversity stack',
    }

HISTORIC_EDITING_TYPES = {
    1: 'zeroing',
    2: 'clipping',
    }

THRESHOLD_TYPES = {
    0: None,
    1: 'hold',
    2: 'var',
    }

PROCESS_TYPES = {
    1: 'no operation (raw data)',
    2: 'stack',
    3: 'correlation after stack',
    4: 'correlation before stack',
    }

FILTER_TYPES = {
    1: 'minimum phase',
    2: 'linear phase',
    # values found in files but not understood
    3: 'Unknwon',
    }

OPERATING_MODES = {
    0b10000: 'standard',
    0b01000: 'microseismic',
    0b00100: 'slip-sweep',
    0b00010: 'SQC dump (VSR)',
    0b00001: 'guidance (navigation)',
    }

DUMP_TYPES = {
    0: 'normal dump',
    1: 'raw dump',
    2: 'extra dump',
    }

SENSOR_TYPES = {
    0: 'not defined',
    1: 'hydrophone',
    2: 'geophone, vertical',
    3: 'geophone, horizontal, inline',
    4: 'geophone, horizontal, crossline',
    5: 'geophone, horizontal, other',
    6: 'accelerometer, vertical',
    7: 'accelerometer, horizontal, inline',
    8: 'accelerometer, horizontal, crossline',
    9: 'accelerometer, horizontal, other',
    }

UNIT_TYPES = {
    0x00: 'not identified',
    0x01: 'FDU',
    0x03: 'RAU',
    0x1C: 'DSU',
    0x20: 'VE464',
    }

SUBUNIT_TYPES = {
    0x01: 'FDU1-408',
    0x0F: 'FDU2S',
    0x15: 'FDU-428',
    0x16: 'DSU3-428',
    0x17: 'QT-428',
    0x1F: 'RAU 0x1E DSUGPS',
    0x21: 'DSU1-428, short',
    0x22: 'DSU3BV-428',
    0x24: 'DSU1-428, long',
    0x25: 'DSU3-SA',
    0x26: 'RAU-428',
    # other values found in files, but not documented:
    0x65: '0x65-WhatTheHell',  # not in the SEGD Doc
    0x66: 'DSU-QuietSeisMEMS',  # not in the SEGD Doc
    # sanity value:
    0: None,
    }

CHANNEl_TYPES = {
    0: 'geophone',
    1: 'hydrophone',
    }

CONTROL_UNIT_TYPES = {
    0x30: 'LAUX-428',
    0x31: 'LCI-428',
    0x50: 'RAU',
    0x51: 'RAU-D',
    # sanity value:
    0: None,
    # other values found in files, but not documented:
    0xA4: 'WTU-508XT',  # not in the SEGD Doc
    0x06: 'Unknown0x06',
    0x03: 'Unknown0x03',
    }

CHANNEL_EDITED_STATUSES = {
    0: None,
    1: 'dead',
    2: 'acquisition/retrieve error',
    3: 'noise edition',
    }

CHANNEL_PROCESSES = {
    1: 'raw data',
    2: 'aux stack',
    3: 'correlation, negative part',
    4: 'correlation, positive part',
    5: 'normal correlation',
    6: 'seis stack',
    }

CHANNEL_GAIN_SCALES = {
    # subunit_type    unit               channel_gain_scale_code 1 or 2
    'FDU':          {'unit': 'mV_RMS',   1: 1600,  2: 400},
    'RAU-428':      {'unit': 'mV_RMS',   1: 1600,  2: 400},
    'DSU-428':      {'unit': 'm/s/s',    1: 5,     2: None},
    'DSU3-SA':      {'unit': 'm/s/s',    1: 5,     2: None},
    'RAU':          {'unit': 'mV_peak',  1: 2500,  2: 650},
    }

CHANNEL_FILTERS = {
    # subunit_type?    channel_filter_code 1 or 2
    'FDU':            {1: '0.8FN minimum phase', 2: '0.8FN linear phase'},
    'RAU-428':        {1: '0.8FN minimum phase', 2: '0.8FN linear phase'},
    'DSU-428':        {1: '0.8FN minimum phase', 2: '0.8FN linear phase'},
    'DSU3-SA':        {1: '0.8FN minimum phase', 2: '0.8FN linear phase'},
    'RAU':            {1: '0.9FN minimum phase', 2: '0.9FN linear phase'},
    }

# instrument and orientation codes matching sensor types
INSTRUMENT_ORIENTATION_CODES = {
    0: '',  # not defined
    1: 'DH',  # hydrophone
    2: 'HZ',  # geophone, vertical
    3: 'H1',  # geophone, horizontal, in-line
    4: 'H2',  # geophone, horizontal, crossline
    5: 'H3',  # geophone, horizontal, other
    6: 'NZ',  # accelerometer, vertical
    7: 'N1',  # accelerometer, horizontal, in-line
    8: 'N2',  # accelerometer, horizontal, crossline
    9: 'N3',  # accelerometer, horizontal, other
    }


def band_codes(sampling_rate) -> str:
    """band codes matching sample rate, for a short-period instrument"""
    if sampling_rate >= 1000.:
        return 'G'
    if sampling_rate >= 250.:
        return 'D'
    if sampling_rate >= 80.:
        return 'E'
    if sampling_rate >= 10.:
        return 'S'
