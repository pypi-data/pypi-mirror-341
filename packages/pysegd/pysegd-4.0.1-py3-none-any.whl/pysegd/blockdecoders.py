from pysegd.decoding import BlockDecoder, TypeDecoderBuilder

from pysegd.headerfields import FORMAT_CODES, RECORD_TYPES, DESCALE_MULTIPLIER, SOURCE_TYPES, TEST_RECORD_TYPES, \
    SPREAD_TYPES, NOISE_ELIMINATION_TYPES, THRESHOLD_TYPES, PROCESS_TYPES, FILTER_TYPES, DUMP_TYPES, SENSOR_TYPES, \
    UNIT_TYPES, SUBUNIT_TYPES, CHANNEl_TYPES, CONTROL_UNIT_TYPES, CHANNEL_EDITED_STATUSES, CHANNEL_PROCESSES, \
    CHANNEL_GAIN_SCALES, CHANNEL_FILTERS

from pysegd.typedecoders import \
    NoDecoder, \
    BCDDecoder, LeftBCDDecoder, RightBCDDecoder, \
    BoolDecoder, UIntDecoder, Uint32ArrayDecoder, \
    FloatDecoder, DoubleDecoder, \
    AsciiDecoder,  IntThenFractionDecoder, \
    TimeDecoder, GPSTimeOfAcquisitionDecoder, FirstTimeingWordDecoder, \
    FileNumberDecoder, GeneralConstantsDecoder, \
    BaseScanIntervalDecoder, \
    RecLenUintDecoder, RevisionBCDDecoder, \
    StackSignUIntDecoder, OperatingModeUIntDecoder, \
    TimeBreakWindowDecoder, \
    TraceData32bitIEEEDemulDecoder


class GeneralHeaderBlock1Decoder(BlockDecoder):

    buffer_structure = {
        'file_number':                    TypeDecoderBuilder(FileNumberDecoder, 0, 2),
        'format_code':                    TypeDecoderBuilder(BCDDecoder, 2, 2, table=FORMAT_CODES, raise_on_key_error=True),
        'general_constants':              TypeDecoderBuilder(GeneralConstantsDecoder, 4, 6),
        'n_additional_blocks':            TypeDecoderBuilder(LeftBCDDecoder, 11, 1),
        'time':                           TypeDecoderBuilder(TimeDecoder, 10, 6),
        'manufacture_code':               TypeDecoderBuilder(BCDDecoder, 16, 1),
        'manufacture_serial_number':      TypeDecoderBuilder(BCDDecoder, 17, 2),
        'bytes_per_scan':                 TypeDecoderBuilder(BCDDecoder, 19, 3),
        'base_scan_interval_in_ms':       TypeDecoderBuilder(BaseScanIntervalDecoder, 22, 1),
        'polarity':                       TypeDecoderBuilder(LeftBCDDecoder, 23, 1),
        'not_used_23L-24':                TypeDecoderBuilder(NoDecoder, 23, 2),
        'rec_type':                       TypeDecoderBuilder(LeftBCDDecoder, 25, 1, table=RECORD_TYPES),
        'reclen':                         TypeDecoderBuilder(RecLenUintDecoder, 25, 2),
        'scan_type_per_record':           TypeDecoderBuilder(BCDDecoder, 27, 1),
        'n_channel_sets_per_record':      TypeDecoderBuilder(BCDDecoder, 28, 1),
        'n_sample_skew_32bit_extensions': TypeDecoderBuilder(BCDDecoder, 29, 1),
        'extended_header_length':         TypeDecoderBuilder(BCDDecoder, 30, 1),
        # If more than 99 External Header blocks are used,
        # then this field external_header_length is set to FF and General Header block #2 (bytes 8-9)
        # indicates the number of External Header blocks.
        'external_header_length':         TypeDecoderBuilder(BCDDecoder, 31, 1, table={0xFFF: None}, raise_on_key_error=False),
        }

    def bytes(self) -> bytes:

        bytes_out = BlockDecoder.bytes(self)

        # place n_additional_blocks in the left side of byte #11
        b_n_additional_blocks = dict.__getitem__(self, "n_additional_blocks").encoded_value
        byte_11 = bytes([(b_n_additional_blocks[0] & 0xF0) | (bytes_out[11] & 0x0F)])

        b_rec_type = dict.__getitem__(self, "rec_type").encoded_value
        byte_25 = bytes([(b_rec_type[0] & 0xF0) | (bytes_out[25] & 0x0F)])

        bytes_out = bytearray(bytes_out)
        bytes_out[11:12] = byte_11
        bytes_out[25:26] = byte_25
        bytes_out = bytes(bytes_out)
        return bytes_out


class GeneralHeaderBlock2Decoder(BlockDecoder):

    buffer_structure = {
        'expanded_file_number':         TypeDecoderBuilder(UIntDecoder, 0, 3),
        'not_used_3-6':                 TypeDecoderBuilder(NoDecoder, 3, 4),
        'external_header_blocks':       TypeDecoderBuilder(UIntDecoder, 7, 2),
        'not_used_9':                   TypeDecoderBuilder(NoDecoder, 9, 1),
        'segd_revision_number':         TypeDecoderBuilder(RevisionBCDDecoder, 10, 2),
        'no_blocks_of_general_trailer': TypeDecoderBuilder(UIntDecoder, 12, 2),
        'extended_record_length_in_ms': TypeDecoderBuilder(UIntDecoder, 14, 3),
        'not_used_17':                  TypeDecoderBuilder(NoDecoder, 17, 1),
        'general_header_block_number':  TypeDecoderBuilder(UIntDecoder, 18, 1),
        'not_used_19-31':               TypeDecoderBuilder(NoDecoder, 19, 13),
        }

    # no need to overwrite the default bytes method


class GeneralHeaderBlock3Decoder(BlockDecoder):

    buffer_structure = {
        'expanded_file_number':         TypeDecoderBuilder(UIntDecoder, 0, 3),
        'source_line_number':           TypeDecoderBuilder(IntThenFractionDecoder, 3, 5),
        'source_point_number':          TypeDecoderBuilder(IntThenFractionDecoder, 8, 5),
        'source_point_index':           TypeDecoderBuilder(UIntDecoder, 13, 1),
        'phase_control':                TypeDecoderBuilder(UIntDecoder, 14, 1),
        'vibrator_type':                TypeDecoderBuilder(UIntDecoder, 15, 1),
        'phase_angle':                  TypeDecoderBuilder(UIntDecoder, 16, 2),
        'general_header_block_number':  TypeDecoderBuilder(UIntDecoder, 18, 1),
        'source_set_number':            TypeDecoderBuilder(UIntDecoder, 19, 1),
        'not_used_20-31':               TypeDecoderBuilder(NoDecoder, 20, 12),
    }
    # no need to overwrite the default bytes method


class ScanTypeHeaderBlockDecoder(BlockDecoder):

    buffer_structure = {
        'scan_type_header':                     TypeDecoderBuilder(BCDDecoder, 0, 1),
        'channel_set_number':                   TypeDecoderBuilder(BCDDecoder, 1, 1),
        'channel_set_starting_time':            TypeDecoderBuilder(UIntDecoder, 2, 2),
        'channel_set_end_time':                 TypeDecoderBuilder(UIntDecoder, 4, 2),
        'descale_multiplier_in_mV':             TypeDecoderBuilder(UIntDecoder, 6, 2, table=DESCALE_MULTIPLIER, flip_byte=True),
        'number_of_channels':                   TypeDecoderBuilder(BCDDecoder, 8, 2),
        'channel_type_id':                      TypeDecoderBuilder(LeftBCDDecoder, 10, 1),
        'number_of_subscans_exponent':          TypeDecoderBuilder(LeftBCDDecoder, 11, 1),
        'channel_gain_control_method':          TypeDecoderBuilder(RightBCDDecoder, 11, 1),
        'alias_filter_freq_at_m3dB_in_Hz':      TypeDecoderBuilder(BCDDecoder, 12, 2),
        'alias_filter_slope_in_dB_per_octave':  TypeDecoderBuilder(BCDDecoder, 14, 2),
        'lowcut_filter_freq_in_Hz':             TypeDecoderBuilder(BCDDecoder, 16, 2),
        'lowcut_filter_slope_in_dB_per_octave': TypeDecoderBuilder(BCDDecoder, 18, 2),
        'first_notch_freq':                     TypeDecoderBuilder(BCDDecoder, 20, 2),
        'second_notch_freq':                    TypeDecoderBuilder(BCDDecoder, 22, 2),
        'third_notch_freq':                     TypeDecoderBuilder(BCDDecoder, 24, 2),
        'extended_channel_set_number':          TypeDecoderBuilder(BCDDecoder, 26, 2),
        'extended_header_flag':                 TypeDecoderBuilder(LeftBCDDecoder, 28, 1),
        'trace_header_extensions':              TypeDecoderBuilder(RightBCDDecoder, 28, 1),
        'vertical_stack':                       TypeDecoderBuilder(UIntDecoder, 29, 1),
        'streamer_cable_number':                TypeDecoderBuilder(UIntDecoder, 30, 1),
        'array_forming':                        TypeDecoderBuilder(UIntDecoder, 31, 1),
        }
    # no need to overwrite the default bytes method


class ExtendedHeaderBlockDecoder(BlockDecoder):

    buffer_structure = {
        "acquisition_length_in_ms":                 TypeDecoderBuilder(UIntDecoder, 0, 4),
        "sample_interval_in_microsec":              TypeDecoderBuilder(UIntDecoder, 4, 4),
        "total_number_of_traces":                   TypeDecoderBuilder(UIntDecoder, 8, 4),
        "number_of_auxes":                          TypeDecoderBuilder(UIntDecoder, 12, 4),
        "number_of_seis_traces":                    TypeDecoderBuilder(UIntDecoder, 16, 4),
        "number_of_dead_seis_traces":               TypeDecoderBuilder(UIntDecoder, 20, 4),
        "number_of_live_seis_traces":               TypeDecoderBuilder(UIntDecoder, 24, 4),
        "type_of_source":                           TypeDecoderBuilder(UIntDecoder, 28, 4, table=SOURCE_TYPES),
        "number_of_samples_in_trace":               TypeDecoderBuilder(UIntDecoder, 32, 4),
        "shot_number":                              TypeDecoderBuilder(UIntDecoder, 36, 4),
        "TB_window_in_s":                           TypeDecoderBuilder(FloatDecoder, 40, 4),
        "test_record_type":                         TypeDecoderBuilder(UIntDecoder, 44, 4, table=TEST_RECORD_TYPES),
        "spread_first_line":                        TypeDecoderBuilder(UIntDecoder, 48, 4),
        "spread_first_number":                      TypeDecoderBuilder(UIntDecoder, 52, 4),
        "spread_number":                            TypeDecoderBuilder(UIntDecoder, 56, 4),
        "spread_type_code":                         TypeDecoderBuilder(UIntDecoder, 60, 4, table=SPREAD_TYPES),
        "time_break_in_us":                         TypeDecoderBuilder(UIntDecoder, 64, 4),
        "uphole_time_in_us":                        TypeDecoderBuilder(UIntDecoder, 68, 4),
        "blaster_id":                               TypeDecoderBuilder(UIntDecoder, 72, 4),
        "blaster_status":                           TypeDecoderBuilder(UIntDecoder, 76, 4),
        "refraction_delay_in_ms":                   TypeDecoderBuilder(UIntDecoder, 80, 4),
        "TB_to_T0_time_in_us":                      TypeDecoderBuilder(UIntDecoder, 84, 4),
        "internal_time_break":                      TypeDecoderBuilder(BoolDecoder, 88, 4),
        "prestack_within_field_units":              TypeDecoderBuilder(BoolDecoder, 92, 4),
        "noise_elimination_type":                   TypeDecoderBuilder(UIntDecoder, 96, 4, table=NOISE_ELIMINATION_TYPES),
        "low_trace_percentage":                     TypeDecoderBuilder(UIntDecoder, 100, 4),
        "low_trace_value_in_dB":                    TypeDecoderBuilder(UIntDecoder, 104, 4),
        "value1":                                   TypeDecoderBuilder(UIntDecoder, 108, 4),
        "value2":                                   TypeDecoderBuilder(UIntDecoder, 112, 4),
        "noisy_trace_percentage":                   TypeDecoderBuilder(UIntDecoder, 116, 4),
        "value3":                                   TypeDecoderBuilder(UIntDecoder, 120, 4),
        "value4":                                   TypeDecoderBuilder(UIntDecoder, 124, 4),
        "threshold_hold_per_var":                   TypeDecoderBuilder(UIntDecoder, 128, 4, table=THRESHOLD_TYPES),
        "value5":                                   TypeDecoderBuilder(UIntDecoder, 132, 4),
        "value6":                                   TypeDecoderBuilder(UIntDecoder, 136, 4),
        "type_of_process":                          TypeDecoderBuilder(UIntDecoder, 140, 4, table=PROCESS_TYPES),
        "acquisition_type_tables":                  TypeDecoderBuilder(Uint32ArrayDecoder, 144, 32 * 4),
        "threshold_type_tables":                    TypeDecoderBuilder(Uint32ArrayDecoder, 272, 32 * 4),
        "stacking_fold":                            TypeDecoderBuilder(UIntDecoder, 400, 4),
        'not_used_404-483':                         TypeDecoderBuilder(NoDecoder, 404, 80),
        "record_length_in_ms":                      TypeDecoderBuilder(UIntDecoder, 484, 4),
        "autocorrelation_peak_time_in_ms":          TypeDecoderBuilder(UIntDecoder, 488, 4),
        'not_used_492-495':                         TypeDecoderBuilder(NoDecoder, 492, 4),
        "correlation_pilot_number":                 TypeDecoderBuilder(UIntDecoder, 496, 4),
        "pilot_length_in_ms":                       TypeDecoderBuilder(UIntDecoder, 500, 4),
        "sweep_length_in_ms":                       TypeDecoderBuilder(UIntDecoder, 504, 4),
        "acquisition_number":                       TypeDecoderBuilder(UIntDecoder, 508, 4),
        "max_of_max_aux":                           TypeDecoderBuilder(FloatDecoder, 512, 4),
        "max_of_max_seis":                          TypeDecoderBuilder(FloatDecoder, 516, 4),
        "dump_stacking_fold":                       TypeDecoderBuilder(UIntDecoder, 520, 4),
        "tape_label":                               TypeDecoderBuilder(AsciiDecoder, 524, 6),
        'not_used_530-540': TypeDecoderBuilder(NoDecoder, 530, 10),
        "tape_number":                              TypeDecoderBuilder(UIntDecoder, 540, 4),
        "software_version":                         TypeDecoderBuilder(AsciiDecoder, 544, 6),
        "not_used_550-559":                         TypeDecoderBuilder(NoDecoder, 550, 10),
        "date":                                     TypeDecoderBuilder(AsciiDecoder, 560, 12),
        "source_easting":                           TypeDecoderBuilder(DoubleDecoder, 572, 8),
        "source_northing":                          TypeDecoderBuilder(DoubleDecoder, 580, 8),
        "source_elevation":                         TypeDecoderBuilder(FloatDecoder, 588, 4),
        "slip_sweep_mode_used":                     TypeDecoderBuilder(BoolDecoder, 592, 4),
        "files_per_tape":                           TypeDecoderBuilder(UIntDecoder, 596, 4),
        "file_count":                               TypeDecoderBuilder(UIntDecoder, 600, 4),
        "acquisition_error_description":            TypeDecoderBuilder(AsciiDecoder, 604, 160),
        "filter_type":                              TypeDecoderBuilder(UIntDecoder, 764, 4, table=FILTER_TYPES),
        "stack_is_dumped":                          TypeDecoderBuilder(BoolDecoder, 768, 4),
        "stack_sign":                               TypeDecoderBuilder(StackSignUIntDecoder, 772, 4),
        "PRM_tilt_correction_used":                 TypeDecoderBuilder(BoolDecoder, 776, 4),
        "swath_name":                               TypeDecoderBuilder(AsciiDecoder, 780, 64),
        "operating_mode_code":                      TypeDecoderBuilder(OperatingModeUIntDecoder, 844, 4),
        'reserved_848-851':                         TypeDecoderBuilder(NoDecoder, 848, 4),
        "no_log":                                   TypeDecoderBuilder(BoolDecoder, 852, 4),
        "listening_time_in_ms":                     TypeDecoderBuilder(UIntDecoder, 856, 4),
        "type_of_dump":                             TypeDecoderBuilder(UIntDecoder, 860, 4, table=DUMP_TYPES),
        'reserved_864-867':                         TypeDecoderBuilder(NoDecoder, 864, 4),
        "swath_id":                                 TypeDecoderBuilder(UIntDecoder, 868, 4),
        "seismic_trace_offset_removal_is_disabled": TypeDecoderBuilder(BoolDecoder, 872, 4),
        "gps_time_of_acquisition":                  TypeDecoderBuilder(GPSTimeOfAcquisitionDecoder, 876, 8),
        'reserved_884-963':                         TypeDecoderBuilder(NoDecoder, 884, 80),
        'not_used_964-1023':                        TypeDecoderBuilder(NoDecoder, 964, 60),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # rename fields value? into appropriate names
        if self.noise_elimination_type == 'off':
            pass

        elif self.noise_elimination_type == 'diversity stack':
            self['number_of_windows'] = self['value1']

        elif self.noise_elimination_type == 'historic':
            self['historic_editing_type_code'] = self['value2']
            self['historic_range'] = self['value3']
            self['historic_taper_length_2_exponent'] = self['value4']
            self['historic_threshold_init_value'] = self['value5']
            self['historic_zeroing_length'] = self['value6']

        elif self.noise_elimination_type == 'enhanced diversity stack':
            self['window_length'] = self['value1']
            self['overlap'] = self['value2']

        else:
            raise Exception

        # do not remove these values for read-write symetry
        # del self['value1'], self['value2'], self['value3'], \
        #     self['value4'],  self['value5'],  self['value6']

    def bytes(self) -> bytes:
        bytes_out = super(ExtendedHeaderBlockDecoder, self).bytes()
        assert len(bytes_out) == 1024, (len(bytes_out), self.buffer_length)
        return bytes_out


class ExternalHeaderBlockDecoder(BlockDecoder):

    buffer_structure = {}

    def __init__(self, buffer: bytes, **kwargs):
        super(ExternalHeaderBlockDecoder, self).__init__(buffer=buffer, **kwargs)
        self['external_header'] = AsciiDecoder(0, len(buffer)).from_buffer(buffer)


class TraceHeaderBlockDecoder(BlockDecoder):
    buffer_structure = {
        'file_number':                  TypeDecoderBuilder(FileNumberDecoder, 0, 2),  # TypeDecoderBuilder(BCDDecoder, 0, 2, table={0xFFFF: None}, raise_on_key_error=False),
        'scan_type_number':             TypeDecoderBuilder(BCDDecoder, 2, 1),
        'channel_set_number':           TypeDecoderBuilder(BCDDecoder, 3, 1),
        'trace_number':                 TypeDecoderBuilder(BCDDecoder, 4, 2),
        'first_timing_word_in_ms':      TypeDecoderBuilder(FirstTimeingWordDecoder, 6, 3),
        'trace_header_extension':       TypeDecoderBuilder(UIntDecoder, 9, 1),
        'sample_skew':                  TypeDecoderBuilder(UIntDecoder, 10, 1),
        'trace_edit':                   TypeDecoderBuilder(UIntDecoder, 11, 1),
        'time_break_window':            TypeDecoderBuilder(TimeBreakWindowDecoder, 12, 3),
        'extended_channel_set_number':  TypeDecoderBuilder(UIntDecoder, 15, 1),
        'extended_file_number':         TypeDecoderBuilder(UIntDecoder, 17, 3),
        }


class TraceHeaderExternalBlock1Decoder(BlockDecoder):
    buffer_structure = {
        'receiver_line_number':             TypeDecoderBuilder(UIntDecoder, 0, 3, table={0xFFFFF: None}, raise_on_key_error=False),
        'receiver_point_number':            TypeDecoderBuilder(UIntDecoder, 3, 3, table={0xFFFFF: None}, raise_on_key_error=False),
        'receiver_point_index':             TypeDecoderBuilder(UIntDecoder, 6, 1),
        'number_of_samples_per_trace':      TypeDecoderBuilder(UIntDecoder, 7, 3),
        'extended_receiver_line_number':    TypeDecoderBuilder(IntThenFractionDecoder, 10, 5),
        'extended_receiver_point_number':   TypeDecoderBuilder(IntThenFractionDecoder, 15, 5),
        'sensor_type':                      TypeDecoderBuilder(UIntDecoder, 20, 1, table=SENSOR_TYPES),
        'not_used_21-31':                   TypeDecoderBuilder(NoDecoder, 21, 11),
        }


class TraceHeaderExternalBlock2Decoder(BlockDecoder):
    buffer_structure = {
        'receiver_easting':                   TypeDecoderBuilder(DoubleDecoder, 0, 8),
        'receiver_northing':                  TypeDecoderBuilder(DoubleDecoder, 8, 8),
        'receiver_elevation':                 TypeDecoderBuilder(FloatDecoder, 16, 4),
        'sensor_type_number':                 TypeDecoderBuilder(UIntDecoder, 20, 1),
        'DSD_identification_number':          TypeDecoderBuilder(UIntDecoder, 24, 4),
        'extended_trace_number':              TypeDecoderBuilder(UIntDecoder, 28, 4),
        'not_used_21-23':                     TypeDecoderBuilder(NoDecoder, 21, 4),
        }


class TraceHeaderExternalBlock3Decoder(BlockDecoder):
    buffer_structure = {
        'resistance_low_limit':         TypeDecoderBuilder(FloatDecoder, 0, 4),
        'resistance_high_limit':        TypeDecoderBuilder(FloatDecoder, 4, 4),
        'resistance_calue_in_ohms':     TypeDecoderBuilder(FloatDecoder, 8, 4),
        'tilt_limit':                   TypeDecoderBuilder(FloatDecoder, 12, 4),
        'tilt_value':                   TypeDecoderBuilder(FloatDecoder, 16, 4),
        'resistance_error':             TypeDecoderBuilder(BoolDecoder, 20, 1),
        'tilt_error':                   TypeDecoderBuilder(BoolDecoder, 21, 1),
        'not_used_22-31': TypeDecoderBuilder(NoDecoder, 22, 10),
        }


class TraceHeaderExternalBlock4Decoder(BlockDecoder):
    buffer_structure = {
        'capacitance_low_limit':               TypeDecoderBuilder(FloatDecoder, 0, 4),
        'capacitance_high_limit':              TypeDecoderBuilder(FloatDecoder, 4, 4),
        'capacitance_value_in_nano_farads':    TypeDecoderBuilder(FloatDecoder, 8, 4),
        'cutoff_low_limit':                    TypeDecoderBuilder(FloatDecoder, 12, 4),
        'cutoff_high_limit':                   TypeDecoderBuilder(FloatDecoder, 16, 4),
        'cutoff_value_in_Hz':                  TypeDecoderBuilder(FloatDecoder, 20, 4),
        'capacitance_error':                   TypeDecoderBuilder(BoolDecoder, 24, 1),
        'cutoff_error':                        TypeDecoderBuilder(BoolDecoder, 25, 1),
        'not_used_26-31': TypeDecoderBuilder(NoDecoder, 26, 6),

    }


class TraceHeaderExternalBlock5Decoder(BlockDecoder):
    buffer_structure = {
        'leakage_limit':                                 TypeDecoderBuilder(FloatDecoder, 0, 4),
        'leakage_value_in_megahoms':                     TypeDecoderBuilder(FloatDecoder, 4, 4),
        'instrument_longitude':                          TypeDecoderBuilder(DoubleDecoder, 8, 8),
        'instrument_latitude':                           TypeDecoderBuilder(DoubleDecoder, 16, 8),
        'leakage_error':                                 TypeDecoderBuilder(BoolDecoder, 24, 1),
        'instrument_horizontal_position_accuracy_in_mm': TypeDecoderBuilder(UIntDecoder, 25, 3),
        'instrument_elevation_in_mm':                    TypeDecoderBuilder(FloatDecoder, 28, 4),
        }


class TraceHeaderExternalBlock6Decoder(BlockDecoder):
    buffer_structure = {
        'unit_type':              TypeDecoderBuilder(UIntDecoder, 0, 1, table=UNIT_TYPES, raise_on_key_error=False),
        'unit_serial_number':     TypeDecoderBuilder(UIntDecoder, 1, 3),
        'channel_number':         TypeDecoderBuilder(UIntDecoder, 4, 1),
        'not_used_5-7': TypeDecoderBuilder(NoDecoder, 5, 3),
        'assembly_type':          TypeDecoderBuilder(UIntDecoder, 8, 1),
        'assembly_serial_number': TypeDecoderBuilder(UIntDecoder, 9, 3),
        'location_in_assembly':   TypeDecoderBuilder(UIntDecoder, 12, 1),
        'not_used_13-15': TypeDecoderBuilder(NoDecoder, 13, 3),
        'subunit_type':           TypeDecoderBuilder(UIntDecoder, 16, 1, table=SUBUNIT_TYPES, raise_on_key_error=False),
        'channel_type':           TypeDecoderBuilder(UIntDecoder, 17, 1, table=CHANNEl_TYPES, raise_on_key_error=True),
        'not_used_18-19': TypeDecoderBuilder(NoDecoder, 18, 2),
        'sensor_sensitivity_in_mV_per_m_per_s_per_s': TypeDecoderBuilder(FloatDecoder, 20, 4),
        'not_used_24-31': TypeDecoderBuilder(NoDecoder, 24, 8),
        }


class TraceHeaderExternalBlock7Decoder(BlockDecoder):
    buffer_structure = {
        "control_unit_type":                      TypeDecoderBuilder(UIntDecoder, 0, 1, table=CONTROL_UNIT_TYPES, raise_on_key_error=False),
        "control_unit_serial_number":             TypeDecoderBuilder(UIntDecoder, 1, 3),
        "channel_gain_scale_code":                TypeDecoderBuilder(UIntDecoder, 4, 1),
        "channel_filter_code":                    TypeDecoderBuilder(UIntDecoder, 5, 1),
        "channel_data_error_overscaling":         TypeDecoderBuilder(UIntDecoder, 6, 1),
        "channel_edited_status":                  TypeDecoderBuilder(UIntDecoder, 7, 1, table=CHANNEL_EDITED_STATUSES),
        "channel_sample_to_mV_conversion_factor": TypeDecoderBuilder(FloatDecoder, 8, 4),
        "number_of_stacks_noisy":                 TypeDecoderBuilder(UIntDecoder, 12, 1),
        "number_of_stacks_low":                   TypeDecoderBuilder(UIntDecoder, 13, 1),
        "channel_type_id":                        TypeDecoderBuilder(UIntDecoder, 14, 1, table={1: 'seis', 9: 'aux'}),
        "channel_process":                        TypeDecoderBuilder(UIntDecoder, 15, 1, table=CHANNEL_PROCESSES),
        'trace_max_value':                        TypeDecoderBuilder(FloatDecoder, 16, 4),
        'trace_max_time_in_us':                   TypeDecoderBuilder(UIntDecoder, 20, 4),
        'number_of_interpolations':               TypeDecoderBuilder(UIntDecoder, 24, 4),
        'seismic_trace_offset_value':             TypeDecoderBuilder(UIntDecoder, 28, 4),
        }

    def __init__(self, buffer: bytes, subunit_type: str, **kwargs):
        super(TraceHeaderExternalBlock7Decoder, self).__init__(buffer=buffer, **kwargs)

        # sanity check against corrupted values for 'subunit_type'
        self.channel_gain_scale_unit = None
        self.channel_gain_scale_value = None
        self.channel_filter_value = None
        if subunit_type in CHANNEL_GAIN_SCALES.keys():
            self.channel_gain_scale_unit = CHANNEL_GAIN_SCALES[subunit_type]['unit']
            self.channel_gain_scale_value = CHANNEL_GAIN_SCALES[subunit_type][self.channel_gain_scale_code]
            self.channel_filter_value = CHANNEL_FILTERS[subunit_type][self.channel_filter_code]


class TraceDataBlockDecoder(BlockDecoder):

    buffer_structure = {}  # data length unknown yet

    def __init__(self, buffer: bytes, **kwargs):
        super(TraceDataBlockDecoder, self).__init__(buffer=bytes([]), **kwargs)

        self['data_array'] = TraceData32bitIEEEDemulDecoder(npts=len(buffer) // 4).from_buffer(buffer=buffer)

    @property
    def npts(self):
        """for data decoders, I expect them to know their number of samples dynamically"""
        decoder = self.get_decoder('data_array')
        return decoder.npts
