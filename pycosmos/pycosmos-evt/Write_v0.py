import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path
from obspy import read_inventory, read_events, read

parser = argparse.ArgumentParser()
 # Parse for filepaths with input to generate a v0 and where to save the output
parser.add_argument("--staxml", type=Path, help="Filepath to STATIONXML file.")
parser.add_argument("--quakeml", type=Path, help="Filepath to QuakeML file.")
parser.add_argument("--mseed", type=Path, help="Filepath to MiniSeed file.")
parser.add_argument("--out", type=Path, help="Filepath where the .v0 file will be saved.")

 # Parse for variables that can be modified by user.
parser.add_argument("--event", type=ascii, help="Assign a name to the event.")
parser.add_argument("--lsb", type=float, help="Value of the Least Significant Bit (LSB) in micro-volts.")
parser.add_argument("--damp", type=float, help="Value of the Sensor damping (fraction of critical).")                    
parser.add_argument("--sens", type=float, help="Value of the Sensor sensitivity in volts/g for accelerometer.")
args = parser.parse_args()

# Read StationXML file 
inv = read_inventory('%s' % args.staxml, format="STATIONXML")
   #inv = read_inventory('/home/lvelez/pyCosmos/ADJ1.staxml')


#Read QuakeML file
cat = read_events('%s' % args.quakeml, format="QUAKEML")
   #cat = read_events('/home/lvelez/pyCosmos/quakeml.xml')

# Read MiniSeed file
#mseed = read('%s' % args.mseed) 
evt = read('/home/lvelez/17-jul-2021-4.5/GNC2/aaw098.evt')
stats_evt = evt[0].stats.pop('kinemetrics_evt')
   #mseed = read('/home/lvelez/pyCosmos/mona.mseed' )
chn_total = int(stats_evt.nchannels)
# for i in evt[chn_total].stats.channel:
#  chn_total+=1


class Write_v0():

 def __init__(self,chn=0):
  self.chn = chn
 
 def write_v0(chn):  
  

# Read StationXML file 
   inv = read_inventory('%s' % args.staxml, format="STATIONXML")
   #inv = read_inventory('/home/lvelez/pyCosmos/ADJ1.staxml')
   net = inv[0]
   sta = net[0]
   #chn = sta[0]

   event = cat[0]
   origin = event.origins[0]
   mag = event.magnitudes[0].mag
   msecs = origin.time.microsecond / 1000000
   secs = origin.time.second + msecs
   #event_date = origin.time
   frmt_date=origin.time.strftime('%Y%m%d%H')
   event_desc = cat[0].event_descriptions
   sta_code = "", net.code, "-", sta.code
   sta_cd = "".join(sta_code)
   chan_azim = int(sta[chn+1].azimuth)

# Read MiniSeed file 
   evt_chn = evt[chn].stats.channel
   duration = evt[0].stats.endtime - evt[0].stats.starttime
   max_acc = max(evt[chn].data)

   # if evt_chn == 0:
   #    evt_chan = 'HNZ'
   # elif evt_chn == 1:
   #    evt_chn = 'HNN'
   # elif evt_chn == 2:
   #    evt_chan = 'HNE'


   # Time variables
   event_year = origin.time.year
   event_month_hdr = origin.time.strftime('%b')
   event_day = origin.time.day
   event_day_hdr = origin.time.strftime('%a')
   event_year = origin.time.year
   event_date = origin.time.strftime('%Y/%m/%d')
   event_hr_hdr = origin.time.strftime('%H:%M')
   origin_dt_frmt = origin.time.strftime('%Y/%m/%d %H:%M:%S')  
   pretrig_secs = 60
   postdetrig_secs = duration - pretrig_secs
   rcrd_secs = ((origin.time.hour*3600) + (origin.time.minute*60) + (origin.time.second)) - pretrig_secs
   rcrd_start_hour = str(timedelta(seconds=rcrd_secs))
   rcrd_start_date = event_date +" "+ rcrd_start_hour
   current_date = datetime.now()
   current_dt_frmt = current_date.strftime('%Y-%m-%d %H:%M:%S')

   # Network and Station Variables
   network_code = 54 # Strong Motion Network Code


   # Misc
   record_id = "",sta.code ,".",net.code,".01"
   rc_id = ''.join(record_id)
   
   


# Parameters for Text Header

   text_params = [event_desc[0].text, event_day_hdr,event_month_hdr, event_day, event_year,
    event_hr_hdr, origin.latitude, origin.longitude, origin.depth, event.magnitudes[0].mag,
    origin_dt_frmt, network_code,sta_cd, sta.site.name, sta.latitude, 
    sta.longitude, chn+1, chn_total, rcrd_start_date, chan_azim,
    int(duration), max_acc, current_dt_frmt]



# Parameters of Integer Header
   int_params = [0, 1, 50, 120, 1, -999, -999, 0, -999, -999, # 1-10
    42, -999, -999, -999, -999, 1, -999, -999, 1, -999, # 11-20
   -999, -999, -999, -999, -999, -999, -999, -999, -999, 109, # 21-30
    3, -999, -999, -999, 24, 24, -999, -999, -999, origin.time.year, # 31-40                               ##Trying to modify 35,36 to 0 from 24 
   -999, origin.time.month, origin.time.day, origin.time.hour, origin.time.minute, 5, 8, -999, -999, -999, # 41-50
   -999, 20, -999, chan_azim, -999, -999, -999, -999, -999, -999, # 51-60                                  
   -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, # 61-70
   -999, -999, -999, -999, 1, 0, -999, -999, -999, -999, # 71-80
   -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, # 81-90
   -999, -999, -999, -999, -999, -999, -999, -999, -999, -999] # 91-100

# Parameters of Real Header
   real_params = [sta.latitude, sta.longitude, sta.elevation, -999.0, -999.0, # 1-5
   -999.0, -999.0, -999.0, -999.0, origin.latitude, # 6-10
   origin.longitude, origin.depth/1000, -999, -999.0, mag, # 11-15
   -999.0, 20.121995, 81.129693, -999.0, -999.0, #16-20                   ## Modified 17 & 18 from default              ##
   -999.0,  0.298024, -999.0, pretrig_secs, postdetrig_secs, # 21-25      ## Modified 22 from 2.38 to 0.298024          ##
   80.0, -999.0, -999.0, -999.0, secs, # 26-30                            ## Modified 26 from default                   ##
   -999.0,-999.0, -999.0, 0.005, duration, # 31-35       ##  34 = mseed[chn].stats.delta                                          ##
   -999.0, -999.0, -999.0, -999.0, 200,    # 36-40                        ## Modified 40 from 0 to nat freq 210 Hz      ##
    0.697089, 5.0, -999.0, -999.0, -999.0, # 41-45                        ## May need to change 42 value                ##
   -999.0, 1.0, -999.0, -999.0, 0.0,       # 46-50                        ##                                            ##
   -999.0, -999.0, -999.0, -999.0, -999.0, # 51-55                        ##                                            ## 
   -999.0, -999.0, -999.0, -999.0, -999.0, # 56-60                        ##                                            ##
   -999.0, 5.0, duration, max_acc, -999.0, # 61-65                        ## May need 65 time at max value              ##
   -0.0, -999.0, -999.0, -999.0, -999.0,   # 66-70                        ## Modified 66 from default                   ##
   -999.0, -999.0, -999.0, -999.0, -999.0, # 71-75
   -999.0, -999.0, -999.0, -999.0, -999.0, # 76-80
   -999.0, -999.0, -999.0, -999.0, -999.0, # 81-85
   -999.0, -999.0, -999.0, -999.0, -999.0, # 86-90
   -999.0, -999.0, -999.0, -999.0, -999.0, # 91-95 
   -999.0, -999.0, -999.0, -999.0, -999.0] # 95-100


# Assign a name to the v0 file using the network code, station code, and channel.
   
   if args.out != None:
    parent_dir = '%s' % args.out
   else:
    parent_dir = '/home/lvelez/pyCosmos/PyCosMan_v0/out'   
    dir_name = "",parent_dir,"/",net.code,"",sta.code,"-",frmt_date
    dn = ''.join(dir_name)

   file_name = "",net.code,"",sta.code,"-",frmt_date,"-",".v0"
   file = ''.join(file_name)
   file_path = "",dn,"/",file

   if os.path.exists(dn) == True:
    pass
   else:
     os.mkdir(dn) 
   
   fn = ''.join(file_path)    

# Write Text Header to text file
   with open(fn, "w") as f:
    print("Acceleration counts       (Format v01.20 with 13 text lines)"
    "\nRecord of",text_params[0]," of ",text_params[1],"",text_params[2], "", text_params[3],",",text_params[4],"",text_params[5],"UTC"
    "\nHypocenter", text_params[6],"  ",text_params[7]," H=", int(text_params[8]*0.001),"km", "Ml:", text_params[9], 
    "\nOrigin:", text_params[10],"   UTC"
    "\nStatn No:",text_params[11], "         Code:",text_params[12],"",text_params[13],
    "\nCoords:", text_params[14], "", text_params[15],"Site Geology:"
    "\nRecorder: Unk            (",text_params[16], "Chns of ",text_params[17]," at Sta) Sensor: (see comment)  "
    "\nRcrd start time:",text_params[18],"UTC (Q=?) RcrdId:"
    "\nSta Chan:",text_params[19],"deg       Location:"
    "\nRaw record length =",text_params[20],"sec,   Uncor max = ",text_params[21],"   , at  Unk sec. "
    "\nProcessed",text_params[22],"AST"
    "\nNo filtering!"
    "\nValues used when parameter of data value is unknown/unspecified:   -999, -999.000", file = f)

# Write Integer header into file.
   int_size = len(int_params)
   int_col = 10
   int_lines = int_size // int_col
   i = 0

   with open(fn, "a") as f:
    print(" 100 Integer-header values follow on  10 lines, Format = (10I8)", file = f)
    for z in range(0, int_lines):
     print(f"{int_params[i]:8}{int_params[i+1]:8}{int_params[i+2]:8}{int_params[i+3]:8}{int_params[i+4]:8}{int_params[i+5]:8}{int_params[i+6]:8}{int_params[i+7]:8}{int_params[i+8]:8}{int_params[i+9]:8}", file = f)  
     i += int_col

# Write Real header into file.
   real_size = len(real_params)
   real_col = 5
   real_lines = real_size // real_col
   j = 0

   with open(fn, "a") as f:
    print(" 100 Real-header values follow on  20 lines, Format = (5F15.6)", file = f)
    for y in range(0, real_lines):
     print(f"{real_params[j]:15.6f}{real_params[j+1]:15.6f}{real_params[j+2]:15.6f}{real_params[j+3]:15.6f}{real_params[j+4]:15.6f}", file = f)
     j += real_col
     
# Write comment lines into file.
   with open(fn, "a") as f:
     print("    3 Comment line(s) follow, each starting with a |"
     "\n| RcrdId:",rc_id,
     "\n| Sensor:",sta[chn+1].sensor.model,"s/n:",sta[chn+1].sensor.serial_number,
     "\n|<SCNL>",rc_id,"    <AUTH>", current_date, file = f)    

# Write acceleration data into file.
   data_array = evt[chn].data
   data_size = data_array.size
   k = 0
   j = 0
   with open (fn, "a") as f:
    print("  ", data_size, "acceleration pts, approx  ",int(duration), "secs, units=counts (50),Format=(8F11.6)", file = f)
    for i in range(0,data_size):
     try:
      if j == 0 and data_array[i] >= 0:                     #First column of data and positive value
       print(f"    {data_array[i]:6.6f}", end=" ", file =f)
       j += 1
      elif j != 0 and data_array[i] >= 0:
       print(f"  {data_array[i]:6.6f}", end=" ", file =f)
       j += 1
      elif j == 0 and data_array[i] < 0:                    #First column of data and negative value
       print(f"   {data_array[i]:6.6f}", end=" ", file =f) 
       j += 1
      elif j !=0 and data_array[i] < 0:
       print(f" {data_array[i]:6.6f}", end=" ", file =f) 
       j += 1
      if j == 8:
       j = 0
       print("",file = f) 
      k += 8
     except IndexError:
      break
   with open(fn, "a") as f:  
    print('End-of-data for 1', 'acceleration', file = f)
    
