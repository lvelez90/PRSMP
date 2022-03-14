import argparse
from datetime import datetime, timedelta
from pathlib import Path
from obspy import read_inventory, read_events, read
from utils import *

""" We start by parsing the command line for the formats and filepaths to be
 used as specified by the user. """
 
parser = argparse.ArgumentParser()
parser.add_argument("--staxml", type= Path ,
                    help="Path to STATIONXML file.")
parser.add_argument("--quakeml", type= Path,
                    help="Path to QuakeML file.")
parser.add_argument("--mseed", type= Path,
                    help="Path to MiniSEED file.")

args = parser.parse_args()

#inv = read_inventory('%s' % args.staxml, format="STATIONXML")
inv =  read_inventory('/home/lvelez/17-jul-2021-4.5/prsmp/data/PR_GNC1.xml')
net = inv[0]
sta = net[0]
chn = sta[0]

#cat = read_events('%s' % args.quakeml, format="QUAKEML")
cat = read_events('/home/lvelez/17-jul-2021-4.5/prsmp/data/Test.xml', format="QUAKEML")
event = cat[0]
origin = event.origins[0]
mag = event.magnitudes[0].mag
hdr_origin_date = origin.time.strftime('%a%b%d%Y%Z')
event_timezone = origin.time.strftime('%Z')
origin_date_frmt = origin.time.strftime('%Y/%m/%d %H:%M:%S')




# i = 0
# list_chans = []
# for x in range(0,num_chans + 1):
#     chan_evt = evt[i].stats.pop('kinemetrics_evt')
#     list_chans.append(chan_evt.chan_id)
#     print(i,x)
#     i += 1
mseed = read('/home/lvelez/17-jul-2021-4.5/prsmp/data.mseed')
endtime= mseed[0].stats.endtime
starttime = mseed[0].stats.starttime
time_diff = mseed[0].stats.endtime - mseed[0].stats.starttime

data_array = mseed[0].data
data_size = data_array.size
data_col = 8

chans = 3
k = 0

# for k, v in sorted(mseed[0].stats.mseed.items()):
#  print("'%s': %s" % (k, str(v)))

# stat = mseed[0].stats
# print(stat)

# print(cat[0].event_descriptions)

# event_desc = cat[0].event_descriptions
# print(event_desc[0].text)

evt = read('/home/lvelez/17-jul-2021-4.5/GNC2/aaw098.evt')
data_array = evt[0].data
stats_evt = evt[2].stats.pop('kinemetrics_evt')
print(stats_evt)
#pretrig = evt[0].stats.triggertime - evt[0].stats.starttime
duration = evt[0].stats.endtime - evt[0].stats.starttime
#delta = evt[chn].stats.delta
chn_total = int(stats_evt.nchannels)

for i in range(0,chn_total):
    stats_evt
    print(i)



 