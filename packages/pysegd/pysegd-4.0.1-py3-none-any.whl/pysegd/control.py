from seispy import Stream
import sys

sample_file = sys.argv[1]

import matplotlib.pyplot as plt
st0 = Stream().from_segd(sample_file)
st1 = st0.copy()
for tr in st1:
    tr.detrend().decimate(decim_rate=4, anti_alias=0.95, anti_alias_order=4, anti_alias_zerophase=True)

st2 = Stream().from_segd("toto.pysegd")

st0.show(plt.gca(), color="k")
st1.show(plt.gca(), color="g")
st2.show(plt.gca(), color="r")

plt.show()
