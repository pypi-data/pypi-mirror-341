#!/usr/bin/env python
from pysegd.segdfile import SegdFile
import multiprocessing as mp
import os.path

help_message = """
segddecim.py -d 2 file1.segd [file2.segd [ ... ] ]
"""


def _decimate_segd_file(args):
    """ NO CONTROL HERE !!"""
    segd_filename_in, segd_filename_out, decim_rate, allow_overwrite = args

    segdfile = SegdFile(segd_filename_in)
    segdfile.decimate(
        detrend=True,
        retrend=True,
        decim_rate=decim_rate,
        anti_alias=0.90,
        anti_alias_order=16.,
        anti_alias_zerophase=True)

    print(f'{segd_filename_in} > {segd_filename_out}')
    segdfile.write(segd_filename_out, allow_overwrite=allow_overwrite)


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    file_list_in = []
    file_list_out = []
    decim_rate = -1
    allow_overwrite = False

    while len(args):
        arg = args.pop(0)
        if arg == "-d":
            decim_rate = int(args.pop(0))

        elif arg == "-f":
            allow_overwrite = True  # WARNING !!!

        elif arg.endswith('.segd'):
            assert os.path.isfile(arg), IOError(arg)
            file_list_in.append(arg)

        else:
            raise ValueError(f'param {arg} not understood')

    if decim_rate == -1:
        raise Exception(help_message)

    for segd_filename_in in file_list_in:
        segd_filename_out = os.path.basename(segd_filename_in).replace('.segd', '') + f"_decim{decim_rate}.segd"
        if os.path.isfile(segd_filename_out):
            if not allow_overwrite:
                raise Exception(f'the output {segd_filename_out} exists, use -f to force overwriting')
        file_list_out.append(segd_filename_out)

    assert len(file_list_in) == len(file_list_out) > 0, Exception(help_message)

    jobs = ((segd_filename_in, segd_filename_out, decim_rate, allow_overwrite)
            for segd_filename_in, segd_filename_out in zip(file_list_in, file_list_out))


    with mp.Pool(6) as pool:
        pool.map(_decimate_segd_file, iterable=jobs)


